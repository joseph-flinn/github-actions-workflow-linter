"""Test src/github_actions_workflow_linter/rules/step_approved.py."""

import pytest

from ruamel.yaml import YAML

from src.github_actions_workflow_linter.load import WorkflowBuilder
from src.github_actions_workflow_linter.rules.step_approved import RuleStepUsesApproved
from src.github_actions_workflow_linter.utils import InternalActionsSettings, Settings

yaml = YAML()


@pytest.fixture(name="settings")
def fixture_settings():
    return Settings(
        approved_actions={
            "actions/checkout": {
                "name": "actions/checkout",
                "version": "v4.1.1",
                "sha": "b4ffde65f46336ab88eb53be808477a3936bae11",
            },
            "actions/download-artifact": {
                "name": "actions/download-artifact",
                "version": "v4.1.0",
                "sha": "f44cd7b40bfd40b6aa1cc1b9b5b7bf03d3c67110",
            },
        },
        internal_actions=InternalActionsSettings(
            {
                "enabled": True,
                "org": "flinnsolutions",
                "repos": ["gh-actions", "internal-actions"],
            }
        ),
    )


@pytest.fixture(name="settings_no_internal_actions")
def fixture_settings_no_internal_actions():
    return Settings(
        approved_actions={
            "actions/checkout": {
                "name": "actions/checkout",
                "version": "v4.1.1",
                "sha": "b4ffde65f46336ab88eb53be808477a3936bae11",
            },
            "actions/download-artifact": {
                "name": "actions/download-artifact",
                "version": "v4.1.0",
                "sha": "f44cd7b40bfd40b6aa1cc1b9b5b7bf03d3c67110",
            },
        }
    )


@pytest.fixture(name="approved_workflow")
def fixture_approved_workflow():
    workflow = """\
---
on:
  workflow_dispatch:

jobs:
  job-key:
    runs-on: ubuntu-22.04
    steps:
      - name: Checkout Branch
        uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1

      - name: Test GitHub Org Action
        uses: flinnsolutions/gh-actions/create-release@main

      - name: Test internal GitHub Org Action
        uses: flinnsolutions/internal-actions/get-keyvault-secrets@main

      - name: Test Local Repo Action
        uses: ./actions/test-action

      - name: Test Run Action
        run: echo "test"
"""
    return WorkflowBuilder.build(workflow=yaml.load(workflow), from_file=False)


@pytest.fixture(name="unapproved_workflow")
def fixture_unapproved_workflow():
    workflow = """\
---
on:
  workflow_dispatch:

jobs:
  job-key:
    runs-on: ubuntu-22.04
    steps:
      - name: Checkout Branch
        uses: azure/login@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1

      - name: Checkout Branch
        uses: joseph-flinn/action-DNE@main

      - name: Checkout Branch with Ref
        uses: joseph-flinn/subfolder/action-DNE@main
        with:
            ref: main

"""
    return WorkflowBuilder.build(workflow=yaml.load(workflow), from_file=False)


@pytest.fixture(name="rule")
def fixture_rule(settings):
    return RuleStepUsesApproved(settings=settings)


@pytest.fixture(name="rule_no_internal_actions")
def fixture_rule_no_internal_actions(settings_no_internal_actions):
    return RuleStepUsesApproved(settings=settings_no_internal_actions)


def test_rule_on_unapproved_workflow(rule, unapproved_workflow):
    result, message = rule.fn(unapproved_workflow.jobs["job-key"].steps[0])
    assert result is False
    assert "New Action detected" in message

    result, message = rule.fn(unapproved_workflow.jobs["job-key"].steps[1])
    assert result is False
    assert "New Action detected" in message

    result, message = rule.fn(unapproved_workflow.jobs["job-key"].steps[2])
    assert result is False
    assert "New Action detected" in message


def test_rule_on_approved_workflow(rule, approved_workflow):
    result, _ = rule.fn(approved_workflow.jobs["job-key"].steps[0])
    assert result is True

    result, _ = rule.fn(approved_workflow.jobs["job-key"].steps[1])
    assert result is True

    result, _ = rule.fn(approved_workflow.jobs["job-key"].steps[2])
    assert result is True

    result, _ = rule.fn(approved_workflow.jobs["job-key"].steps[3])
    assert result is True

    result, _ = rule.fn(approved_workflow.jobs["job-key"].steps[4])
    assert result is True


def test_rule_no_internal_actions_on_approved_workflow(
    rule_no_internal_actions, approved_workflow
):
    result, _ = rule_no_internal_actions.fn(approved_workflow.jobs["job-key"].steps[0])
    assert result is True

    result, _ = rule_no_internal_actions.fn(approved_workflow.jobs["job-key"].steps[1])
    assert result is False

    result, _ = rule_no_internal_actions.fn(approved_workflow.jobs["job-key"].steps[2])
    assert result is False

    result, _ = rule_no_internal_actions.fn(approved_workflow.jobs["job-key"].steps[3])
    assert result is True

    result, _ = rule_no_internal_actions.fn(approved_workflow.jobs["job-key"].steps[4])
    assert result is True


def test_fail_compatibility(rule, approved_workflow):
    finding = rule.execute(approved_workflow)
    assert "Workflow not compatible with" in finding.description

    finding = rule.execute(approved_workflow.jobs["job-key"])
    assert "Job not compatible with" in finding.description
