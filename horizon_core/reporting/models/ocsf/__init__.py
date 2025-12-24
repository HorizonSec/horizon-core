"""
OCSF Models Package - Clean imports from modular structure
"""

from .base_objects import (
    Account,
    File,
    Group,
    Metadata,
    User,
)
from .common import (
    CVE,
    CVSS,
    CWE,
)
from .enums import (
    ActivityID,
    Confidence,
    ConfidenceID,
    Severity,
    SeverityID,
    Status,
    StatusID,
)
from .events import (
    ComplianceFinding,
    DetectionFinding,
    VulnerabilityFinding,
)
from .finding_objects import (
    FindingInfo,
)
from .vulnerability_objects import (
    AffectedPackage,
    Vulnerability,
)

__version__ = "1.3.0"

__all__ = [
    "ActivityID",
    "SeverityID",
    "Severity",
    "StatusID",
    "Status",
    "ConfidenceID",
    "Confidence",
    "Group",
    "Account",
    "User",
    "File",
    "Metadata",
    "CWE",
    "CVSS",
    "CVE",
    "AffectedPackage",
    "Vulnerability",
    "FindingInfo",
    "VulnerabilityFinding",
    "ComplianceFinding",
    "DetectionFinding",
]
