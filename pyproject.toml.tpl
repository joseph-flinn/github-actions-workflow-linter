[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "github_actions_workflow_linter"
dynamic = ["version"]
authors = []
description = "Custom GitHub Action Workflow Linter"
readme = "README.md"
requires-python = ">=3.11"
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: OS Independent",
]

dependencies = [
$DEPS
]

[project.urls]
Homepage = "https://github.com/joseph-flinn/github-actions-workflow-linter"
Issues = "https://github.com/joseph-flinn/github-actions-workflow-linter/issues"

[project.scripts]
gawl = "github_actions_workflow_linter.cli:main"

[tool.hatch.build.targets.wheel]
packages = ["src/github_actions_workflow_linter"]

[tool.hatch.version]
path = "src/github_actions_workflow_linter/__about__.py"
