"""Representation for a job in a GitHub Action workflow."""

from dataclasses import dataclass, field
from typing import List, Optional, Self

from dataclasses_json import config, dataclass_json, Undefined, DataClassJsonMixin
from ruamel.yaml.comments import CommentedMap

from .step import Step


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Job(DataClassJsonMixin):
    """Represents a job in a GitHub Action workflow.

    This object contains all of the data that is required to run the current linting
    Rules against. If a new Rule requires a key that is missing, the attribute should
    be added to this class to make it available for use in linting.
    """

    key: str
    runs_on: Optional[str] = field(metadata=config(field_name="runs-on"), default=None)
    name: Optional[str] = None
    env: Optional[CommentedMap] = None
    steps: Optional[List[Step]] = field(default_factory=list)
    uses: Optional[str] = None
    uses_path: Optional[str] = None
    uses_ref: Optional[str] = None
    uses_with: Optional[CommentedMap] = field(
        metadata=config(field_name="with"), default=None
    )
    outputs: Optional[CommentedMap] = None

    def __post_init__(self):
        """Automatically parses the 'uses' string if it exists."""
        if self.uses:
            self.uses = self.uses.replace("\n", "").strip()
            if "@" in self.uses:
                parts = self.uses.split("@", 1)
                self.uses_path = parts[0]
                self.uses_ref = parts[1]


    @classmethod
    def init(cls, key: str, data: CommentedMap) -> Self:
        """Custom dataclass constructor to map job data to a Job."""
        init_data = {
            "key": key,
            "name": data.get("name"),
            "runs-on": data.get("runs-on"),
            "env": data.get("env"),
            "uses": data.get("uses"),
            "outputs": data.get("outputs")
        }

        new_job = cls.from_dict(init_data)

        if "steps" in data:
            new_job.steps = [
                Step.init(idx, new_job.key, step_data)
                for idx, step_data in enumerate(data["steps"])
            ]

        return new_job
