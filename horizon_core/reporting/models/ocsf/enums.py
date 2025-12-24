"""
OCSF Enumerations Module

This module contains all the enumeration types used throughout the OCSF schema.
These enums provide standardized values for various attributes like activities,
severity levels, statuses, and confidence levels.

The enums follow OCSF v1.3.0 specifications with proper integer values
and string representations as defined in the official schema.
"""

from enum import Enum, unique
from typing import Dict

__all__ = [
    "ActivityID",
    "SeverityID",
    "Severity",
    "StatusID",
    "Status",
    "ConfidenceID",
    "Confidence",
    "get_severity_by_id",
    "get_status_by_id",
    "get_confidence_by_id",
]


@unique
class ActivityID(Enum):
    """
    The normalized identifier of the finding activity.

    These values represent the lifecycle states of security findings
    as they are processed through detection, investigation, and resolution.

    Values:
        UNKNOWN (0): The activity is unknown
        CREATE (1): The finding is being created
        UPDATE (2): The finding is being updated
        CLOSE (3): The finding is being closed/resolved
        OTHER (99): Any other activity not covered by standard values
    """

    UNKNOWN = 0
    CREATE = 1
    UPDATE = 2
    CLOSE = 3
    OTHER = 99


@unique
class SeverityID(Enum):
    """
    The normalized identifier of the event/finding severity.

    Represents the severity level of security events and findings
    using standardized numeric values that can be used for sorting
    and filtering by severity.

    Values:
        UNKNOWN (0): Severity is unknown or not determined
        INFORMATIONAL (1): Informational events with no immediate impact
        LOW (2): Low severity events requiring minimal attention
        MEDIUM (3): Medium severity events requiring attention
        HIGH (4): High severity events requiring prompt attention
        CRITICAL (5): Critical events requiring immediate attention
        FATAL (6): Fatal events indicating system compromise
        OTHER (99): Any other severity not covered by standard levels
    """

    UNKNOWN = 0
    INFORMATIONAL = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    CRITICAL = 5
    FATAL = 6
    OTHER = 99


@unique
class Severity(Enum):
    """
    The event/finding severity normalized to human-readable captions.

    These string values correspond to the SeverityID numeric values
    and provide human-readable severity descriptions for display purposes.

    Values correspond to SeverityID enum values:
        UNKNOWN: "Unknown"
        INFORMATIONAL: "Informational"
        LOW: "Low"
        MEDIUM: "Medium"
        HIGH: "High"
        CRITICAL: "Critical"
        FATAL: "Fatal"
        OTHER: "Other"
    """

    UNKNOWN = "Unknown"
    INFORMATIONAL = "Informational"
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"
    FATAL = "Fatal"
    OTHER = "Other"


@unique
class StatusID(Enum):
    """
    The normalized status identifier of the Finding.

    Represents the current state of a security finding through its
    lifecycle from discovery to resolution or archival.

    Values:
        UNKNOWN (0): Status is unknown
        NEW (1): Finding is newly discovered and unprocessed
        IN_PROGRESS (2): Finding is being actively investigated or remediated
        SUPPRESSED (3): Finding has been suppressed (false positive or accepted risk)
        RESOLVED (4): Finding has been resolved or remediated
        ARCHIVED (5): Finding has been archived for historical purposes
        DELETED (6): Finding has been deleted from the system
        OTHER (99): Any other status not covered by standard values
    """

    UNKNOWN = 0
    NEW = 1
    IN_PROGRESS = 2
    SUPPRESSED = 3
    RESOLVED = 4
    ARCHIVED = 5
    DELETED = 6
    OTHER = 99


@unique
class Status(Enum):
    """
    The normalized status of the Finding with human-readable captions.

    These string values correspond to the StatusID numeric values
    and provide human-readable status descriptions for display purposes.

    Values correspond to StatusID enum values:
        UNKNOWN: "Unknown"
        NEW: "New"
        IN_PROGRESS: "In Progress"
        SUPPRESSED: "Suppressed"
        RESOLVED: "Resolved"
        ARCHIVED: "Archived"
        DELETED: "Deleted"
        OTHER: "Other"
    """

    UNKNOWN = "Unknown"
    NEW = "New"
    IN_PROGRESS = "In Progress"
    SUPPRESSED = "Suppressed"
    RESOLVED = "Resolved"
    ARCHIVED = "Archived"
    DELETED = "Deleted"
    OTHER = "Other"


@unique
class ConfidenceID(Enum):
    """
    The normalized confidence identifier for finding accuracy.

    Represents the confidence level in the accuracy of the rule or
    detection mechanism that created the finding. Higher values
    indicate greater confidence in the finding's validity.

    Values:
        UNKNOWN (0): Confidence level is unknown
        LOW (1): Low confidence in the finding accuracy
        MEDIUM (2): Medium confidence in the finding accuracy
        HIGH (3): High confidence in the finding accuracy
        OTHER (99): Any other confidence level not covered by standard values
    """

    UNKNOWN = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    OTHER = 99


@unique
class Confidence(Enum):
    """
    The confidence normalized to human-readable captions.

    These string values correspond to the ConfidenceID numeric values
    and provide human-readable confidence descriptions for display purposes.

    Values correspond to ConfidenceID enum values:
        UNKNOWN: "Unknown"
        LOW: "Low"
        MEDIUM: "Medium"
        HIGH: "High"
        OTHER: "Other"
    """

    UNKNOWN = "Unknown"
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    OTHER = "Other"


# Utility mapping dictionaries for converting between IDs and string values
_SEVERITY_ID_TO_STRING: Dict[int, str] = {
    SeverityID.UNKNOWN.value: Severity.UNKNOWN.value,
    SeverityID.INFORMATIONAL.value: Severity.INFORMATIONAL.value,
    SeverityID.LOW.value: Severity.LOW.value,
    SeverityID.MEDIUM.value: Severity.MEDIUM.value,
    SeverityID.HIGH.value: Severity.HIGH.value,
    SeverityID.CRITICAL.value: Severity.CRITICAL.value,
    SeverityID.FATAL.value: Severity.FATAL.value,
    SeverityID.OTHER.value: Severity.OTHER.value,
}

_STATUS_ID_TO_STRING: Dict[int, str] = {
    StatusID.UNKNOWN.value: Status.UNKNOWN.value,
    StatusID.NEW.value: Status.NEW.value,
    StatusID.IN_PROGRESS.value: Status.IN_PROGRESS.value,
    StatusID.SUPPRESSED.value: Status.SUPPRESSED.value,
    StatusID.RESOLVED.value: Status.RESOLVED.value,
    StatusID.ARCHIVED.value: Status.ARCHIVED.value,
    StatusID.DELETED.value: Status.DELETED.value,
    StatusID.OTHER.value: Status.OTHER.value,
}

_CONFIDENCE_ID_TO_STRING: Dict[int, str] = {
    ConfidenceID.UNKNOWN.value: Confidence.UNKNOWN.value,
    ConfidenceID.LOW.value: Confidence.LOW.value,
    ConfidenceID.MEDIUM.value: Confidence.MEDIUM.value,
    ConfidenceID.HIGH.value: Confidence.HIGH.value,
    ConfidenceID.OTHER.value: Confidence.OTHER.value,
}


def get_severity_by_id(severity_id: int) -> str:
    """
    Convert a severity ID to its string representation.

    Args:
        severity_id: The numeric severity ID

    Returns:
        The corresponding severity string, or "Unknown" if ID not found

    Example:
        >>> get_severity_by_id(SeverityID.HIGH.value)
        'High'
        >>> get_severity_by_id(99)
        'Other'
    """
    return _SEVERITY_ID_TO_STRING.get(severity_id, Severity.UNKNOWN.value)


def get_status_by_id(status_id: int) -> str:
    """
    Convert a status ID to its string representation.

    Args:
        status_id: The numeric status ID

    Returns:
        The corresponding status string, or "Unknown" if ID not found

    Example:
        >>> get_status_by_id(StatusID.RESOLVED.value)
        'Resolved'
        >>> get_status_by_id(99)
        'Other'
    """
    return _STATUS_ID_TO_STRING.get(status_id, Status.UNKNOWN.value)


def get_confidence_by_id(confidence_id: int) -> str:
    """
    Convert a confidence ID to its string representation.

    Args:
        confidence_id: The numeric confidence ID

    Returns:
        The corresponding confidence string, or "Unknown" if ID not found

    Example:
        >>> get_confidence_by_id(ConfidenceID.HIGH.value)
        'High'
        >>> get_confidence_by_id(99)
        'Other'
    """
    return _CONFIDENCE_ID_TO_STRING.get(confidence_id, Confidence.UNKNOWN.value)
