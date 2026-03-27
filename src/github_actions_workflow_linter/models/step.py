"""Representation for a job step in a GitHub Action workflow."""

from dataclasses import dataclass, field
from typing import Optional, Self

from dataclasses_json import config, dataclass_json, Undefined, DataClassJsonMixin
from ruamel.yaml.comments import CommentedMap


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Step(DataClassJsonMixin):
    """Represents a step in a GitHub Action workflow job.

    This object contains all of the data that is required to run the current linting
    Rules against. If a new Rule requires a key that is missing, the attribute should
    be added to this class to make it available for use in linting.
    """

    key: int
    job: str
    name: Optional[str] = None
    env: Optional[CommentedMap] = None
    uses: Optional[str] = None
    uses_path: Optional[str] = None
    uses_ref: Optional[str] = None
    uses_comment: Optional[str] = None
    uses_version: Optional[str] = None
    uses_with: Optional[CommentedMap] = field(
        metadata=config(field_name="with"), default=None
    )
    run: Optional[str] = None

    def __post_init__(self):
        """Automatically parses optional data."""

        if self.uses:
            if "@" in self.uses:
                parts = self.uses.split("@", 1)
                self.uses_path = parts[0]
                self.uses_ref = parts[1]
        if self.uses_comment:
            self.uses_version = self.uses_comment.split(" ")[-1]


    @classmethod
    def init(cls, idx: int, job: str, data: CommentedMap) -> Self:
        """Custom dataclass constructor to map a job step data to a Step."""
        init_data = {
            "key": idx,
            "job": job,
            **data
        }

        if "uses" in data:
            if "uses" in data.ca.items and data.ca.items["uses"][2]:
                init_data["uses_comment"] = data.ca.items["uses"][2].value.replace("\n", "")
                init_data["uses_version"] = init_data["uses_comment"].split(" ")[-1]
            else:
                init_data["uses_path"] = data["uses"]

        return cls.from_dict(init_data)
