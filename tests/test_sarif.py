"""Tests for SARIF utilities."""

import json
from horizon_core.sarif import (
    SARIFReport,
    Run,
    Tool,
    Result,
    Message,
    Level,
    Kind,
    Location,
    PhysicalLocation,
    Region,
    Rule,
)


def test_sarif_report_creation():
    """Test creating a SARIF report."""
    report = SARIFReport()
    assert report.version == "2.1.0"
    assert len(report.runs) == 0


def test_add_run():
    """Test adding a run to a report."""
    report = SARIFReport()
    tool = Tool(name="TestTool", version="1.0.0")
    run = Run(tool=tool)
    report.add_run(run)
    assert len(report.runs) == 1


def test_result_creation():
    """Test creating a result."""
    result = Result(
        ruleId="TEST001",
        message=Message(text="Test finding"),
        level=Level.WARNING,
    )
    assert result.ruleId == "TEST001"
    assert result.message.text == "Test finding"
    assert result.level == Level.WARNING


def test_location_with_region():
    """Test creating a location with region."""
    region = Region(startLine=10, startColumn=5, endLine=10, endColumn=20)
    physical_location = PhysicalLocation(
        artifactLocation={"uri": "test.py"},
        region=region,
    )
    location = Location(physicalLocation=physical_location)

    loc_dict = location.to_dict()
    assert loc_dict["physicalLocation"]["artifactLocation"]["uri"] == "test.py"
    assert loc_dict["physicalLocation"]["region"]["startLine"] == 10


def test_complete_report():
    """Test creating a complete SARIF report."""
    # Create tool
    tool = Tool(name="TestScanner", version="1.0.0")

    # Create rule
    rule = Rule(
        id="TEST001",
        name="TestRule",
        shortDescription=Message(text="A test rule"),
    )

    # Create result
    region = Region(startLine=5)
    location = Location(
        physicalLocation=PhysicalLocation(
            artifactLocation={"uri": "file.py"},
            region=region,
        )
    )
    result = Result(
        ruleId="TEST001",
        message=Message(text="Test issue found"),
        level=Level.ERROR,
        locations=[location],
    )

    # Create run
    run = Run(tool=tool, results=[result], rules=[rule])

    # Create report
    report = SARIFReport()
    report.add_run(run)

    # Convert to dict and validate structure
    report_dict = report.to_dict()
    assert report_dict["version"] == "2.1.0"
    assert len(report_dict["runs"]) == 1
    assert report_dict["runs"][0]["tool"]["driver"]["name"] == "TestScanner"
    assert len(report_dict["runs"][0]["results"]) == 1
    assert report_dict["runs"][0]["results"][0]["ruleId"] == "TEST001"


def test_sarif_json_serialization():
    """Test SARIF JSON serialization."""
    tool = Tool(name="TestTool", version="1.0.0")
    result = Result(
        ruleId="TEST001",
        message=Message(text="Test finding"),
    )
    run = Run(tool=tool, results=[result])
    report = SARIFReport()
    report.add_run(run)

    json_str = report.to_json()
    parsed = json.loads(json_str)

    assert parsed["version"] == "2.1.0"
    assert len(parsed["runs"]) == 1
