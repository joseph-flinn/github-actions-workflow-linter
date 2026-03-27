"""Tests src/github_actions_workflow_linter/utils.py."""

import pytest

from ruamel.yaml import YAML

from .conftest import FIXTURE_DIR

from src.github_actions_workflow_linter.utils import (
    Action,
    Colors,
    InternalActionsSettings,
    LintFinding,
    LintLevels,
    Settings,
)

yaml = YAML()


@pytest.fixture(name="rules_settings_filename")
def fixture_local_settings_rule():
    return f"{FIXTURE_DIR}/settings/test_rules_settings.yaml"


@pytest.fixture(name="full_settings_filename")
def fixture_local_settings_full():
    return f"{FIXTURE_DIR}/settings/test_full_settings.yaml"


def test_action_eq():
    action_def = {"name": "github/checkout", "version": "1.0.0", "sha": "some-sha"}

    action_a = Action(**action_def)
    action_b = Action(**action_def)

    assert (action_a == action_b) is True
    assert (action_a != action_b) is False


def test_action_ne():
    action_a = Action(name="github/checkout", version="1.0.0", sha="some-sha")
    action_b = Action(name="github/checkout", version="1.1.0", sha="some-other-sha")

    assert (action_a == action_b) is False
    assert (action_a != action_b) is True


def test_lint_level():
    warning = LintLevels.WARNING
    assert warning.code == 1
    assert warning.color == Colors.yellow


def test_lint_finding():
    warning = LintFinding(description="<no description>", level=LintLevels.WARNING)
    assert str(warning) == "\x1b[33mwarning\x1b[0m <no description>"

    error = LintFinding(description="<no description>", level=LintLevels.ERROR)
    assert str(error) == "\x1b[31merror\x1b[0m <no description>"


def test_internal_action_settings():
    ia_settings = InternalActionsSettings(
        {"enabled": True, "org": "test-org", "repos": ["actions", "internal-actions"]}
    )

    assert ia_settings.enabled is True
    assert len(ia_settings.repos) == 2
    assert ia_settings.repos == [
        "test-org/actions",
        "test-org/internal-actions",
    ]


def test_settings_builder_default():
    settings = Settings.builder()

    assert len(settings.enabled_rules) == 6
    assert len(settings.approved_actions) == 28


def test_settings_builder_local_rules_min(rules_settings_filename: str):
    settings = Settings.builder(settings_filename=rules_settings_filename)

    assert len(settings.enabled_rules) == 1
    assert len(settings.approved_actions) == 28  # default actions


def test_settings_builder_local_rules_full(full_settings_filename: str):
    settings = Settings.builder(settings_filename=full_settings_filename)

    assert len(settings.enabled_rules) == 1
    assert len(settings.approved_actions) == 2
    assert settings.internal_actions.enabled is True
    assert len(settings.internal_actions.repos) == 1
