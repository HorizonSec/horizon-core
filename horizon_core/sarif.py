"""
SARIF schema definitions - Standard format for security findings.

This module provides utilities for working with SARIF (Static Analysis Results
Interchange Format) for reporting security findings.

SARIF is a standard format for the output of static analysis tools.
See: https://sarifweb.azurewebsites.net/
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Any
import json


class Level(str, Enum):
    """SARIF result level."""

    NONE = "none"
    NOTE = "note"
    WARNING = "warning"
    ERROR = "error"


class Kind(str, Enum):
    """SARIF result kind."""

    NOT_APPLICABLE = "notApplicable"
    PASS = "pass"
    FAIL = "fail"
    REVIEW = "review"
    OPEN = "open"


@dataclass
class Region:
    """A region within a file."""

    startLine: int
    startColumn: Optional[int] = None
    endLine: Optional[int] = None
    endColumn: Optional[int] = None


@dataclass
class PhysicalLocation:
    """A physical location in a file."""

    artifactLocation: Dict[str, str]
    region: Optional[Region] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {"artifactLocation": self.artifactLocation}
        if self.region:
            region_dict = {"startLine": self.region.startLine}
            if self.region.startColumn:
                region_dict["startColumn"] = self.region.startColumn
            if self.region.endLine:
                region_dict["endLine"] = self.region.endLine
            if self.region.endColumn:
                region_dict["endColumn"] = self.region.endColumn
            result["region"] = region_dict
        return result


@dataclass
class Location:
    """A location where a result was found."""

    physicalLocation: PhysicalLocation

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {"physicalLocation": self.physicalLocation.to_dict()}


@dataclass
class Message:
    """A message string."""

    text: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {"text": self.text}


@dataclass
class Result:
    """A SARIF result."""

    ruleId: str
    message: Message
    level: Level = Level.WARNING
    kind: Kind = Kind.FAIL
    locations: List[Location] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {
            "ruleId": self.ruleId,
            "message": self.message.to_dict(),
            "level": self.level.value,
            "kind": self.kind.value,
        }
        if self.locations:
            result["locations"] = [loc.to_dict() for loc in self.locations]
        return result


@dataclass
class Rule:
    """A SARIF rule definition."""

    id: str
    name: str
    shortDescription: Message
    fullDescription: Optional[Message] = None
    helpUri: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {
            "id": self.id,
            "name": self.name,
            "shortDescription": self.shortDescription.to_dict(),
        }
        if self.fullDescription:
            result["fullDescription"] = self.fullDescription.to_dict()
        if self.helpUri:
            result["helpUri"] = self.helpUri
        return result


@dataclass
class Tool:
    """A SARIF tool."""

    name: str
    version: str
    informationUri: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        driver = {
            "name": self.name,
            "version": self.version,
        }
        if self.informationUri:
            driver["informationUri"] = self.informationUri
        return {"driver": driver}


@dataclass
class Run:
    """A SARIF run."""

    tool: Tool
    results: List[Result] = field(default_factory=list)
    rules: List[Rule] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        run_dict = {
            "tool": self.tool.to_dict(),
            "results": [r.to_dict() for r in self.results],
        }
        if self.rules:
            run_dict["tool"]["driver"]["rules"] = [r.to_dict() for r in self.rules]
        return run_dict


@dataclass
class SARIFReport:
    """A complete SARIF report."""

    runs: List[Run] = field(default_factory=list)
    version: str = "2.1.0"
    schema: str = "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json"

    def add_run(self, run: Run) -> None:
        """Add a run to the report."""
        self.runs.append(run)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "version": self.version,
            "$schema": self.schema,
            "runs": [r.to_dict() for r in self.runs],
        }

    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=indent)

    def save(self, filepath: str) -> None:
        """Save report to file."""
        with open(filepath, "w") as f:
            f.write(self.to_json())
