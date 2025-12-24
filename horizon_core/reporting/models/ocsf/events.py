"""
OCSF Events Module

This module contains the main OCSF event classes for the Findings category,
including vulnerability findings, compliance findings, and detection findings.

These event classes represent the top-level structures for security events
and findings as defined in the OCSF schema specification.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from horizon_core.reporting.models.ocsf.base_objects import Metadata
from horizon_core.reporting.models.ocsf.enums import (
    ActivityID,
    Confidence,
    ConfidenceID,
    Severity,
    SeverityID,
    Status,
    StatusID,
)
from horizon_core.reporting.models.ocsf.finding_objects import FindingInfo
from horizon_core.reporting.models.ocsf.vulnerability_objects import Vulnerability

__all__ = [
    "VulnerabilityFinding",
    "ComplianceFinding",
    "DetectionFinding",
]


@dataclass
class VulnerabilityFinding:
    """
    The Vulnerability Finding event reports weaknesses in information systems.

    Vulnerability Finding events are notifications about security weaknesses
    identified in systems, applications, or infrastructure that could be
    exploited by threat actors. These events follow OCSF class 2002.

    Required Attributes:
        metadata: Event metadata including schema version and source product
        severity_id: Numeric severity level (0-6, 99)
        time: Event occurrence or finding creation time
        type_uid: Event type identifier for vulnerability findings
        activity_id: Finding activity (CREATE, UPDATE, CLOSE, etc.)
        finding_info: Core finding metadata and identifiers
        vulnerabilities: List of vulnerability details

    Optional Attributes:
        category_uid: Event category (default: 2 for Findings)
        class_uid: Event class (default: 2002 for Vulnerability Finding)
        Various timing, status, confidence, and descriptive fields

    Example:
        >>> vuln_finding = VulnerabilityFinding(
        ...     metadata=Metadata(version="1.3.0"),
        ...     severity_id=SeverityID.HIGH,
        ...     time=datetime.now(),
        ...     type_uid=200201,  # Vulnerability Finding Create
        ...     activity_id=ActivityID.CREATE,
        ...     finding_info=FindingInfo(uid="vuln-001"),
        ...     vulnerabilities=[vulnerability_obj]
        ... )
    """

    # Required fields per OCSF schema
    metadata: Metadata = field(metadata={"description": "The metadata associated with the event or a finding."})
    severity_id: SeverityID = field(
        metadata={"description": "The normalized identifier of the event/finding severity."}
    )
    time: datetime = field(
        metadata={"description": "The normalized event occurrence time or the finding creation time."}
    )
    type_uid: int = field(
        metadata={"description": "The event/finding type ID. It identifies the event semantics and structure."}
    )
    activity_id: ActivityID = field(metadata={"description": "The normalized identifier of the finding activity."})
    finding_info: FindingInfo = field(
        metadata={"description": "Describes the supporting information about a generated finding."}
    )
    vulnerabilities: List[Vulnerability] = field(
        metadata={"description": "This object describes vulnerabilities reported in a security finding."}
    )

    # Optional fields with OCSF-compliant defaults
    category_uid: int = field(default=2, metadata={"description": "The category unique identifier of the event."})
    class_uid: int = field(
        default=2002,
        metadata={
            "description": (
                "The unique identifier of a class. A class describes the attributes " "available in an event."
            )
        },
    )
    activity_name: Optional[str] = field(
        default=None,
        metadata={"description": "The finding activity name, as defined by the activity_id."},
    )
    category_name: Optional[str] = field(
        default="Findings",
        metadata={"description": "The event category name, as defined by category_uid value."},
    )
    class_name: Optional[str] = field(
        default="Vulnerability Finding",
        metadata={"description": "The event class name, as defined by class_uid value."},
    )
    count: Optional[int] = field(
        default=None,
        metadata={
            "description": (
                "The number of times that events in the same logical group occurred "
                "during the event Start Time to End Time period."
            )
        },
    )
    duration: Optional[int] = field(
        default=None,
        metadata={
            "description": (
                "The event duration or aggregate time, the amount of time the event "
                "covers from start_time to end_time in milliseconds."
            )
        },
    )
    end_time: Optional[datetime] = field(
        default=None,
        metadata={"description": "The time of the most recent event included in the finding."},
    )
    message: Optional[str] = field(
        default=None,
        metadata={"description": "The description of the event/finding, as defined by the source."},
    )
    raw_data: Optional[str] = field(
        default=None,
        metadata={"description": "The raw event/finding data as received from the source."},
    )
    severity: Optional[Severity] = field(
        default=None,
        metadata={
            "description": ("The event/finding severity, normalized to the caption of " "the severity_id value.")
        },
    )
    start_time: Optional[datetime] = field(
        default=None,
        metadata={"description": "The time of the least recent event included in the finding."},
    )
    status: Optional[Status] = field(
        default=None,
        metadata={
            "description": (
                "The normalized status of the Finding set by the consumer "
                "normalized to the caption of the status_id value."
            )
        },
    )
    status_code: Optional[str] = field(
        default=None,
        metadata={"description": "The event status code, as reported by the event source."},
    )
    status_detail: Optional[str] = field(
        default=None,
        metadata={
            "description": ("The status detail contains additional information about the " "event/finding outcome.")
        },
    )
    status_id: Optional[StatusID] = field(
        default=None,
        metadata={"description": "The normalized status identifier of the Finding, set by the consumer."},
    )
    timezone_offset: Optional[int] = field(
        default=None,
        metadata={
            "description": (
                "The number of minutes that the reported event time is ahead or "
                "behind UTC, in the range -1,080 to +1,080."
            )
        },
    )
    type_name: Optional[str] = field(
        default=None,
        metadata={"description": "The event/finding type name, as defined by the type_uid."},
    )
    comment: Optional[str] = field(default=None, metadata={"description": "A user provided comment about the finding."})
    confidence: Optional[Confidence] = field(
        default=None,
        metadata={"description": "The confidence, normalized to the caption of the confidence_id value."},
    )
    confidence_id: Optional[ConfidenceID] = field(
        default=None,
        metadata={
            "description": ("The normalized confidence refers to the accuracy of the rule " "that created the finding.")
        },
    )
    confidence_score: Optional[int] = field(
        default=None,
        metadata={"description": "The confidence score as reported by the event source."},
    )


@dataclass
class ComplianceFinding:
    """
    Compliance Finding events describe results of compliance evaluations.

    Compliance Finding events represent the results of evaluations performed
    against resources to assess compliance with policies, standards, regulations,
    or organizational requirements. These events follow OCSF class 2003.

    Required Attributes:
        metadata: Event metadata including schema version and source product
        severity_id: Numeric severity level of the compliance finding
        time: Event occurrence or finding creation time
        type_uid: Event type identifier for compliance findings
        activity_id: Finding activity (CREATE, UPDATE, CLOSE, etc.)
        finding_info: Core finding metadata and identifiers

    Optional Attributes:
        category_uid: Event category (default: 2 for Findings)
        class_uid: Event class (default: 2003 for Compliance Finding)
        Various descriptive and classification fields

    Example:
        >>> compliance_finding = ComplianceFinding(
        ...     metadata=Metadata(version="1.3.0"),
        ...     severity_id=SeverityID.MEDIUM,
        ...     time=datetime.now(),
        ...     type_uid=200301,  # Compliance Finding Create
        ...     activity_id=ActivityID.CREATE,
        ...     finding_info=FindingInfo(uid="compliance-001")
        ... )
    """

    # Required fields per OCSF schema
    metadata: Metadata = field(metadata={"description": "The metadata associated with the event or a finding."})
    severity_id: SeverityID = field(
        metadata={"description": "The normalized identifier of the event/finding severity."}
    )
    time: datetime = field(
        metadata={"description": "The normalized event occurrence time or the finding creation time."}
    )
    type_uid: int = field(
        metadata={"description": "The event/finding type ID. It identifies the event semantics and structure."}
    )
    activity_id: ActivityID = field(metadata={"description": "The normalized identifier of the finding activity."})
    finding_info: FindingInfo = field(
        metadata={"description": "Describes the supporting information about a generated finding."}
    )

    # Optional fields with OCSF-compliant defaults
    category_uid: int = field(default=2, metadata={"description": "The category unique identifier of the event."})
    class_uid: int = field(
        default=2003,
        metadata={
            "description": (
                "The unique identifier of a class. A class describes the attributes " "available in an event."
            )
        },
    )
    activity_name: Optional[str] = field(
        default=None,
        metadata={"description": "The finding activity name, as defined by the activity_id."},
    )
    category_name: Optional[str] = field(
        default="Findings",
        metadata={"description": "The event category name, as defined by category_uid value."},
    )
    class_name: Optional[str] = field(
        default="Compliance Finding",
        metadata={"description": "The event class name, as defined by class_uid value."},
    )


@dataclass
class DetectionFinding:
    """
    Detection Finding events describe detections or alerts from security products.

    Detection Finding events represent detections or alerts generated by security
    products such as antivirus, IDS/IPS, SIEM, EDR, or other security monitoring
    tools. These events follow OCSF class 2004.

    Required Attributes:
        metadata: Event metadata including schema version and source product
        severity_id: Numeric severity level of the detection
        time: Event occurrence or finding creation time
        type_uid: Event type identifier for detection findings
        activity_id: Finding activity (CREATE, UPDATE, CLOSE, etc.)
        finding_info: Core finding metadata and identifiers

    Optional Attributes:
        category_uid: Event category (default: 2 for Findings)
        class_uid: Event class (default: 2004 for Detection Finding)
        Various descriptive and classification fields

    Example:
        >>> detection_finding = DetectionFinding(
        ...     metadata=Metadata(version="1.3.0"),
        ...     severity_id=SeverityID.HIGH,
        ...     time=datetime.now(),
        ...     type_uid=200401,  # Detection Finding Create
        ...     activity_id=ActivityID.CREATE,
        ...     finding_info=FindingInfo(uid="detection-001")
        ... )
    """

    # Required fields per OCSF schema
    metadata: Metadata = field(metadata={"description": "The metadata associated with the event or a finding."})
    severity_id: SeverityID = field(
        metadata={"description": "The normalized identifier of the event/finding severity."}
    )
    time: datetime = field(
        metadata={"description": "The normalized event occurrence time or the finding creation time."}
    )
    type_uid: int = field(
        metadata={"description": "The event/finding type ID. It identifies the event semantics and structure."}
    )
    activity_id: ActivityID = field(metadata={"description": "The normalized identifier of the finding activity."})
    finding_info: FindingInfo = field(
        metadata={"description": "Describes the supporting information about a generated finding."}
    )

    # Optional fields with OCSF-compliant defaults
    category_uid: int = field(default=2, metadata={"description": "The category unique identifier of the event."})
    class_uid: int = field(
        default=2004,
        metadata={
            "description": (
                "The unique identifier of a class. A class describes the attributes " "available in an event."
            )
        },
    )
    activity_name: Optional[str] = field(
        default=None,
        metadata={"description": "The finding activity name, as defined by the activity_id."},
    )
    category_name: Optional[str] = field(
        default="Findings",
        metadata={"description": "The event category name, as defined by category_uid value."},
    )
    class_name: Optional[str] = field(
        default="Detection Finding",
        metadata={"description": "The event class name, as defined by class_uid value."},
    )
