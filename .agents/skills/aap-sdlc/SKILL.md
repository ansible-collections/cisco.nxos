---
name: aap-sdlc
description: "Single entry point for the AAP SDLC framework. Routes user requests
  to the correct workflow or skill. Use when the developer invokes any SDLC
  workflow: story implementation, epic breakdown, code review, PR review,
  Jira operations, or git operations. Also supports orchestrator mode where
  the user provides a Jira issue key and the skill determines the correct
  workflow based on the issue type."
version: "1.0"
mandatory: true
---

# AAP SDLC

`workflows.toon` is the source of truth. Always read it before executing.

## Loading workflows.toon

Read `~/.claude/skills/aap-sdlc/workflows.toon` directly. Do NOT use
find, Explore, or any search to locate it. If not found there, try
`.claude/skills/aap-sdlc/workflows.toon` (project-level). If neither
exists, tell the user the skills are not installed.

## Skill locations

Skills are installed at `~/.claude/skills/` as a flat directory
structure. Each skill is a direct subdirectory — NOT nested under
`aap-sdlc/`. Examples:
- `~/.claude/skills/code-review/SKILL.md`
- `~/.claude/skills/review-pr-workflow/SKILL.md`
- `~/.claude/skills/git-workflow/SKILL.md`

To check if a skill is installed, read its SKILL.md directly.
Do NOT use `ls`, `find`, or any directory listing commands.

## Mode detection

- **"update"** → run Update
- **Jira issue key** without action (e.g., `PROJ-12345`) → run Orchestrate
- **Specific action** (e.g., "review PR") → run Execute
- Ambiguous → ask user

## Update (harness repo maintainers only)

Regenerate `workflows.toon` from SKILL.md front matter. Only run this
in the harness repo — not in developer project repos.

1. Run `python3 scripts/generate-workflows-toon.py` from the harness repo root
2. Commit the updated `workflows.toon`

## Orchestrate

1. Verify `jira-integration` skill installed → if not, offer to install
2. Fetch the Jira issue via curl (see `jira-integration` skill):
   ```bash
   curl -s -u "${JIRA_USERNAME}:${JIRA_API_TOKEN}" \
     "${JIRA_URL}/rest/api/3/issue/<ISSUE_KEY>" | jq '.'
   ```
   Extract: type, summary, status, acceptance criteria, assignee
3. Read `workflows.toon` → match issue type against `row.jira_types` → matched row
4. If no match → tell user, stop
5. Continue to Execute with matched row

## Execute

1. Read `workflows.toon` → match user intent against `row.triggers` → matched row
   (skip this step if coming from Orchestrate — row is already matched)
2. If no match → list available workflows, ask user
3. For each skill in `row.requires`: verify installed → if not, offer to install
4. Summarize to user and use AskUserQuestion to confirm:
   - Show: Workflow name, required skills, brief action description
   - Options: "Yes, proceed" / "No, cancel"
   - Always use AskUserQuestion — never plain text y/n prompts
5. For each skill in `row.requires`: read its SKILL.md
6. Read `row.skill_name` SKILL.md
7. Execute following all loaded skills exactly and in order. Do not skip steps.
8. After completion, summarize results to user

## Install

When offering to install missing skills:

```
npx skills add https://gitlab.cee.redhat.com/aap-agentic-tooling/harness.git --skill <name> --agent claude-code --yes
```

After install completes → re-read `workflows.toon` → continue.
Do NOT regenerate the toon — the shipped version already contains all workflow mappings.

## Feedback

When this skill is finished, use the feedback skill in auto mode, unless another skill will collect feedback later.
