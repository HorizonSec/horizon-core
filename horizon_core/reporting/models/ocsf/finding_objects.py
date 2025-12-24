"""
OCSF Finding Objects Module

This module contains objects that describe metadata and information
related to security findings, including supporting data sources,
timing information, and finding classifications.

These objects provide context and metadata that enrich security findings
with additional information needed for analysis and response.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

__all__ = [
    "FindingInfo",
]


@dataclass
class FindingInfo:
    """
    The Finding Information object describes metadata related to a security finding.

    FindingInfo provides essential metadata about security findings including
    identifiers, timing information, data sources, and classification details
    that help security teams understand and prioritize findings.

    Attributes:
        uid: Unique identifier of the finding (required)
        created_time: When the finding was initially created
        data_sources: List of data sources used to generate the finding
        desc: Detailed description of the finding
        first_seen_time: When the finding was first observed
        last_seen_time: When the finding was most recently observed
        modified_time: When the finding metadata was last modified
        src_url: URL pointing to the source or origin of the finding
        title: Brief title summarizing the finding
        types: List of finding type classifications
        uid_alt: Alternative unique identifier for the finding

    Example:
        >>> finding_info = FindingInfo(
        ...     uid="finding-12345",
        ...     title="Critical SQL Injection Vulnerability",
        ...     desc="SQL injection vulnerability in user login form",
        ...     created_time=datetime.now(),
        ...     data_sources=["static_analysis", "dynamic_testing"],
        ...     types=["Code Quality", "Security"]
        ... )
    """

    uid: str = field(metadata={"description": "The unique identifier of the reported finding."})
    created_time: Optional[datetime] = field(
        default=None, metadata={"description": "The time when the finding was created."}
    )
    data_sources: List[str] = field(
        default_factory=list, metadata={"description": "A list of data sources utilized in generation of the finding."}
    )
    desc: Optional[str] = field(default=None, metadata={"description": "The description of the reported finding."})
    first_seen_time: Optional[datetime] = field(
        default=None, metadata={"description": "The time when the finding was first observed."}
    )
    last_seen_time: Optional[datetime] = field(
        default=None, metadata={"description": "The time when the finding was most recently observed."}
    )
    modified_time: Optional[datetime] = field(
        default=None, metadata={"description": "The time when the finding was last modified."}
    )
    src_url: Optional[str] = field(
        default=None, metadata={"description": "The URL pointing to the source of the finding."}
    )
    title: Optional[str] = field(
        default=None, metadata={"description": "A title or a brief phrase summarizing the reported finding."}
    )
    types: List[str] = field(
        default_factory=list, metadata={"description": "One or more types of the reported finding."}
    )
    uid_alt: Optional[str] = field(
        default=None, metadata={"description": "The alternative unique identifier of the reported finding."}
    )
    product_uid: Optional[str] = field(
        default=None, metadata={"description": "The unique identifier of the product that generated the finding."}
    )
    related_events: List[Dict[str, Any]] = field(
        default_factory=list, metadata={"description": "List of events related to this finding."}
    )
    remediation: Optional[str] = field(
        default=None, metadata={"description": "Remediation information for the finding."}
    )
    supporting_data: Optional[Dict[str, Any]] = field(
        default=None, metadata={"description": "Additional supporting data for the finding."}
    )
