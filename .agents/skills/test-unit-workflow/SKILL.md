---
name: test-unit-workflow
description: "Discover the repo's test ecosystem, then identify, generate, and
  validate unit tests to meet the org-defined coverage threshold. Unit tests
  exercise individual functions, methods, and classes in isolation -- no
  external dependencies, no network, no database."
version: "1.1"
type: workflow
mandatory: false
requires:
  - session-recorder
triggers:
  - "unit test"
  - "unit tests"
---

# Unit Test Workflow

## Role

Act as a test engineer specializing in unit testing. You understand the
difference between unit tests and integration/component tests: unit tests
exercise a single function, method, or class in isolation using mocks and
stubs for all external dependencies.

## Task

Bring unit test coverage to the org-defined threshold by first discovering
the repo's testing ecosystem, then identifying coverage gaps, generating
new unit tests, and validating them.

## Context Setup

### What Qualifies as a Unit Test
- Tests a single function, method, or class
- No database connections, no network calls, no filesystem I/O
- External dependencies are mocked/stubbed
- Executes in milliseconds
- Lives in the location dictated by the repo's established conventions
  (discovered in Step 1)

### Edge Cases: Ensuring True Unit Test Isolation

**Tests that do NOT qualify as unit tests:**
- Tests that connect to databases (even local/test databases)
- Tests that make HTTP/network requests (even to localhost)
- Tests that read/write files from disk
- Tests that depend on external services (Redis, message queues, etc.)
- Tests that spawn child processes or shells
- Tests that require Docker containers or test infrastructure
- Tests that depend on environment variables pointing to real resources
- Tests that sleep/wait for async operations to complete

**Validation checkpoints during workflow:**
1. **During discovery (Step 1)** — identify and flag integration tests
   masquerading as unit tests:
   - Look for database imports/connections in test files
   - Look for HTTP client usage without mocking
   - Look for file I/O operations (open, read, write)
   - Check for container orchestration in test setup
   
2. **During gap analysis (Step 3)** — exclude integration test coverage
   from unit test metrics. If the repo conflates unit and integration
   tests, report this to the user and ask whether to:
   - Separate them into distinct suites
   - Focus only on true unit tests
   - Skip this workflow and use integration test workflow instead

3. **During generation (Step 4)** — ensure all generated tests are
   properly isolated:
   - Mock all database connections and queries
   - Mock all HTTP clients and network calls
   - Mock all file system operations
   - Mock all environment variable reads
   - Use in-memory data structures instead of external stores
   - Validate that mocks are used for ALL external boundaries

4. **During validation (Step 5)** — verify tests run in isolation:
   - Tests should pass without network connectivity
   - Tests should pass without database running
   - Tests should pass in parallel execution
   - Each test execution should be < 100ms

### From ARC Configuration (if available)
- If `test-guidance.arc.md` exists, read it for any org-defined test
  framework, assertion library, mocking patterns, and file naming
  conventions. These take precedence over discovered conventions.

### Coverage Threshold Detection
Determine the required coverage threshold:
1. **Check for `guardrails.arc.yaml` (optional)** - if exists, read 
   `test-coverage.unit-threshold` value
2. **If not found, auto-detect from project configuration:**
   - Check package.json/pyproject.toml/jest.config.js/go.mod for coverage config
   - Scan CI configuration files (.github/workflows, .gitlab-ci.yml, Makefile)
   - Look for test commands with coverage flags (e.g., `--coverage-threshold`)
3. **Default to 80% if no threshold found**
- **Always verify and report the detected threshold before evaluating coverage**

## Process Loop

### Step 1: Discover Test Ecosystem

Before writing any tests, understand what already exists. Do not assume
any language, framework, or tooling. Probe the repo to determine:

1. **Language(s) and runtime** — inspect source file extensions, package
   manifests, lock files, and build configs to identify the primary
   language(s) in use.

2. **Framework type** — detect if the repo uses a specialized framework
   requiring specific test tooling:
   - Check for Ansible collection markers: `galaxy.yml`, `plugins/`, `roles/`
   - Check for web frameworks: Django (`manage.py`), Rails (`config/application.rb`),
     Spring Boot (`pom.xml` with Spring), etc.
   - Note the framework type to determine appropriate test runner and validation

3. **Test framework and assertion library** — look for framework-specific
   config files, dependency declarations, and import statements in
   existing test files. Examples of signals (not an exhaustive list):
   - Dependency manifests: `package.json`, `requirements.txt`,
     `pyproject.toml`, `go.mod`, `Gemfile`, `pom.xml`, `build.gradle`,
     `Cargo.toml`, `mix.exs`, etc.
   - Framework config files: `jest.config.*`, `pytest.ini`, `setup.cfg`,
     `.rspec`, `vitest.config.*`, `phpunit.xml`, etc.

4. **Test file naming conventions** — examine existing test files to
   determine the naming pattern the repo uses (e.g., suffix, prefix,
   directory placement). Adopt whatever convention is already in use.

5. **Test runner command** — check for test scripts or targets in the
   repo's build/task system:
   - Task runners: `Makefile`, `package.json` scripts, `Taskfile.yml`,
     `Rakefile`, `Justfile`, etc.
   - Framework-specific runners: `ansible-test units` (Ansible collections),
     `go test`, `pytest`, `npm test`, `mvn test`, `rake test`, etc.
   - If no explicit target exists, determine the framework's default
     run command from the discovered test framework.
   - Ensure the command targets unit tests specifically, not integration/e2e tests

6. **Coverage tooling** — identify how coverage is collected and reported:
   - Look for coverage configuration in framework configs, CI
     definitions, or dedicated coverage config files.
   - Determine the command to produce a coverage report.
   - If no coverage tool is configured, select the standard coverage
     tool for the discovered language/framework.

7. **Mocking patterns** — examine existing test files for mocking/stubbing
   libraries or patterns already in use. Adopt the same approach for new
   tests.

8. **Validate test isolation** — scan existing test files for violations
   of unit test isolation principles:
   - Search for database connection patterns (e.g., `createConnection`,
     `MongoClient`, `psycopg2.connect`, `sql.Open`)
   - Search for HTTP client usage (e.g., `axios`, `fetch`, `requests.get`,
     `http.Client`)
   - Search for file I/O (e.g., `fs.readFile`, `open()`, `ioutil.ReadFile`)
   - Search for container/process spawning (e.g., `docker`, `subprocess`,
     `exec`)
   - Flag any tests that violate isolation and report to user

**Present the discovered ecosystem to the user for confirmation before
proceeding:**
```
Discovered test ecosystem:
  Language:          <detected>
  Framework type:    <e.g., Ansible collection, Django, Rails, generic Python, etc.>
  Test framework:    <detected>
  Assertion style:   <detected>
  Mocking library:   <detected>
  Test file pattern: <detected>
  Test run command:  <framework-specific command for unit tests>
  Coverage command:  <detected>
  Coverage threshold: <detected or default 80%>
  
Isolation validation:
  ✓ <n> tests properly isolated
  ⚠ <n> tests with potential isolation violations
  [List any violations found]

Proceed? (yes / correct anything)
```

If the repo contains no existing tests or test infrastructure, ask the
user which framework and tooling to bootstrap before continuing.

### Step 2: Identify Existing Tests
- Scan the repo for existing unit test files using the naming pattern
  discovered in Step 1
- Run existing unit tests using the discovered test run command
- Capture the coverage report using the discovered coverage command

### Step 3: Analyze Coverage Gaps
- Parse the coverage report to identify files, functions, and branches
  with missing coverage
- Prioritize gaps: critical business logic first, then utilities, then
  generated code (which may be excluded)
- Present the coverage summary to the user:
  ```
  Current unit coverage: <current>% (target: <threshold>%)
  Top uncovered files:
    <file path>   <x>% covered
    <file path>   <y>% covered
    <file path>   <z>% covered
  ```

### Step 4: Generate Tests
- For each uncovered function/method, generate unit tests matching the
  conventions and patterns discovered in Step 1
- Follow the repo's existing test style: assertion patterns, test
  grouping structure, and naming conventions
- Use the repo's established mocking library/patterns for all external
  dependencies
- Write tests to the correct location per the discovered file placement
  conventions
- **Enforce strict isolation** for all generated tests:
  - Mock database connections, queries, and transactions
  - Mock HTTP clients, requests, and responses
  - Mock file system operations (read, write, delete)
  - Mock environment variable access when they reference external resources
  - Mock time/date functions for deterministic testing
  - Mock random number generators for predictable results
  - Ensure no network sockets, no disk I/O, no subprocess execution

### Step 5: Validate
- **Use framework-specific test runner** discovered in Step 1:
  - For Ansible collections: use `ansible-test units` with appropriate options
  - For other frameworks: use the discovered test run command
  - Ensure the command runs only unit tests (not integration/e2e tests)
- Run the full unit test suite including newly generated tests
- **Verify isolation** of newly generated tests:
  - Check execution time (flag any test > 100ms as potentially non-isolated)
  - Run tests in parallel to ensure no shared state dependencies
  - If possible, run tests with network disabled to verify no external calls
- Capture the updated coverage report using framework-specific tooling
- Report results:
  ```
  Unit coverage: <before>% -> <after>% (+<delta>%)
  Tests: <n> passed, <n> failed, <n> skipped
  Test execution time: <avg>ms per test (flagged if > 100ms avg)
  Isolation check: [PASS/FAIL with details]
  Remaining gap: <n>% below target (<threshold>%)
  ```

### Step 6: Review
- Present each generated test file to the user for review
- Flag any tests that required complex mocking (may indicate the code
  under test needs refactoring)
- If coverage target not met -> return to Step 3 with updated gaps
- If coverage target met -> report success

## Stop Conditions

- Unit test coverage meets or exceeds the guardrails-defined threshold
- All unit tests pass
- OR the user explicitly stops the loop
