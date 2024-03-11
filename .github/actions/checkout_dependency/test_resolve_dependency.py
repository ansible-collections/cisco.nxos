#!/usr/bin/env python3
"""Module used to test resolve_dependency.py script."""

import os
import string

from pathlib import PosixPath
from random import choice
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from resolve_dependency import get_pr_merge_commit_sha
from resolve_dependency import main
from resolve_dependency import resolve_ref


@pytest.mark.parametrize(
    "pr_body,match",
    [
        ("Depends-On: https://github.com/my_org/my_collection/pull/12345", True),
        (
            "Depends-On: https://github.com/my_org/my_collection/pull/12345\n"
            "Depends-On: https://github.com/my_org/my_collection/pull/67890",
            True,
        ),
        (
            "Depends-On: https://github.com/another_org/my_collection/pull/4000\n"
            "Depends-On: https://github.com/my_org/my_collection/pull/12345",
            True,
        ),
        (
            "Depends-On: https://github.com/my_org/my_collection/pull/12345\n"
            "Depends-On: https://github.com/my_org/my_collection/pull/67890",
            True,
        ),
        ("Depends-On: https://github.com/another_org/my_collection/pull/12345", False),
        ("Depends-On: https://github.com/my_org/my_collection2/pull/12345", False),
        ("Depends-On: https://github.com/my_org/my_collection/pull", False),
    ],
)
def test_resolve_ref(pr_body: str, match: bool) -> None:
    """Test resolve_ref function.

    :param pr_body: pull request body
    :param match: whether a depends-on should be found or not
    """
    expected = 12345 if match else 0
    assert resolve_ref(pr_body, "my_org/my_collection") == expected


class FakePullRequest:
    # pylint: disable=too-few-public-methods
    """Class to simulate PullRequest Object."""

    def __init__(self, mergeable: bool) -> None:
        """Class constructor.

        :param mergeable: whether the pull request is mergeable or not
        """
        self.mergeable = mergeable
        self.merge_commit_sha = self.generate_commit_sha()

    @staticmethod
    def generate_commit_sha(length: int = 16) -> str:
        """Generate random commit sha.

        :param length: The length of the generated string
        :returns: The generated commit sha
        """
        data = string.ascii_letters + string.digits
        return "".join([choice(data) for _ in range(length)])


@pytest.mark.parametrize("mergeable", [True, False])
@patch("resolve_dependency.Github")
def test_get_pr_merge_commit_sha(m_github: MagicMock, mergeable: bool) -> None:
    """Test get_pr_merge_commit_sha function.

    :param m_github: The github module
    :param mergeable: whether the pull request is mergeable or not
    """
    github_obj = MagicMock()
    m_github.return_value = github_obj

    os.environ["GITHUB_TOKEN"] = "unittest_github_token"

    m_github_repo = MagicMock()
    github_obj.get_repo = MagicMock()
    github_obj.get_repo.return_value = m_github_repo

    local_pr = FakePullRequest(mergeable=mergeable)
    m_github_repo.get_pull = MagicMock()
    m_github_repo.get_pull.return_value = local_pr

    repository = "my_testing_repository"
    pr_number = 12345

    if mergeable:
        assert get_pr_merge_commit_sha(repository, pr_number) == local_pr.merge_commit_sha
    else:
        with pytest.raises(ValueError):
            get_pr_merge_commit_sha(repository, pr_number)

    m_github.assert_called_once_with("unittest_github_token")
    github_obj.get_repo.assert_called_once_with(repository)
    m_github_repo.get_pull.assert_called_once_with(pr_number)


@pytest.mark.parametrize("repository", [True, False])
@pytest.mark.parametrize("resolve_ref_pr", [0, 1])
@patch("resolve_dependency.get_pr_merge_commit_sha")
@patch("resolve_dependency.resolve_ref")
def test_main(
    m_resolve_ref: MagicMock,
    m_get_pr_merge_commit_sha: MagicMock,
    repository: bool,
    resolve_ref_pr: int,
    tmp_path: PosixPath,
) -> None:
    """Test main function.

    :param m_resolve_ref: The resolve_ref mock function
    :param m_get_pr_merge_commit_sha: The get_pr_merge_commit_sha mock function
    :param repository: whether the repository is defined on environment variable or not
    :param resolve_ref_pr: The pull request number
    :param tmp_path: The temporary path for file to create for test
    """
    pr_body = "My pull request body - this is a sample for unit tests"
    repository_name = "my_test_repository"
    os.environ["RESOLVE_REF_PR_BODY"] = pr_body

    gh_output_file = tmp_path / "github_output.txt"
    env_update = {"GITHUB_OUTPUT": str(gh_output_file)}
    if repository:
        env_update.update({"RESOLVE_REF_REPOSITORY": repository_name})

    m_resolve_ref.return_value = resolve_ref_pr
    merge_commit_sha = FakePullRequest.generate_commit_sha()
    m_get_pr_merge_commit_sha.return_value = merge_commit_sha

    with patch.dict(os.environ, env_update):
        main()

    if not repository:
        m_resolve_ref.assert_not_called()
        m_get_pr_merge_commit_sha.assert_not_called()
        assert not gh_output_file.exists()
    elif not resolve_ref_pr:
        m_resolve_ref.assert_called_once_with(pr_body, repository_name)
        m_get_pr_merge_commit_sha.assert_not_called()
        assert not gh_output_file.exists()
    else:
        m_resolve_ref.assert_called_once_with(pr_body, repository_name)
        m_get_pr_merge_commit_sha.assert_called_once_with(repository_name, resolve_ref_pr)
        assert gh_output_file.exists()
        # gh_output_file.read_text() == f"merge_commit_sha={merge_commit_sha}\n"
