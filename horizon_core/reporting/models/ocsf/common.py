from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

__all__ = ["CWE", "CVSS", "CVE"]


@dataclass
class CWE:
    """
    Common Weakness Enumeration (CWE) object for software system weaknesses.

    CWE represents a weakness in a software system that can be exploited by
    a threat actor. CWEs provide a unified, measurable set of software
    weaknesses that enable more effective discussion and analysis.

    Attributes:
        uid: CWE identifier (required) - format "CWE-XXX"
        caption: Human-readable caption for the CWE
        src_url: URL to the official CWE specification

    Example:
        >>> cwe = CWE(
        ...     uid="CWE-79",
        ...     caption="Cross-site Scripting",
        ...     src_url="https://cwe.mitre.org/data/definitions/79.html"
        ... )
    """

    uid: str = field(
        metadata={
            "description": (
                "The Common Weakness Enumeration unique number assigned to a "
                "specific weakness. A CWE Identifier begins CWE followed by a "
                "sequence of digits that acts as a unique identifier. "
                "For example: CWE-123."
            )
        }
    )
    caption: Optional[str] = field(
        default=None,
        metadata={"description": ("The caption assigned to the Common Weakness Enumeration " "unique identifier.")},
    )
    url: Optional[str] = field(
        default=None,
        metadata={
            "description": ("URL pointing to the CWE Specification. For more information " "see https://cwe.mitre.org/")
        },
    )


@dataclass
class CVSS:
    """
    Common Vulnerability Scoring System (CVSS) scoring information.

    CVSS provides a way to capture the principal characteristics of a vulnerability
    and produce a numerical score reflecting its severity. The score can then be
    translated into a qualitative representation (e.g., Low, Medium, High, Critical).

    Attributes:
        base_score: CVSS base score from 0.0 to 10.0 (required)
        version: CVSS version used (required) - e.g., "3.1", "4.0"
        depth: CVSS scoring depth/variant (e.g., "Temporal", "Environmental")
        metrics: Detailed CVSS metrics breakdown
        overall_score: Overall/final CVSS score including temporal/environmental
        severity: Qualitative severity rating (e.g., "High", "Critical")
        vector_string: CVSS vector string representation

    Example:
        >>> cvss = CVSS(
        ...     base_score=7.5,
        ...     version="3.1",
        ...     severity="High",
        ...     vector_string="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N"
        ... )
    """

    base_score: float = field(metadata={"description": "The CVSS base score, which ranges from 0.0 to 10.0."})
    version: str = field(metadata={"description": "The CVSS version. For example: 3.0, 3.1."})
    depth: Optional[str] = field(
        default=None,
        metadata={
            "description": (
                "The CVSS depth represents the CVSS variant used to calculate "
                "the vector string. Example: Temporal, Environmental."
            )
        },
    )
    metrics: Optional[List[Dict[str, Any]]] = field(default=None, metadata={"description": "The CVSS metrics."})
    overall_score: Optional[float] = field(
        default=None,
        metadata={
            "description": (
                "The CVSS overall score, which ranges from 0.0 to 10.0. "
                "In a CVSS Base scoring, this is equivalent to the Base Score."
            )
        },
    )
    severity: Optional[str] = field(
        default=None,
        metadata={
            "description": (
                "The Common Vulnerability Scoring System (CVSS) Qualitative "
                "Severity Rating. A textual representation of the numeric score."
            )
        },
    )
    vector_string: Optional[str] = field(
        default=None,
        metadata={"description": ("The CVSS vector string is a text representation of a set of " "CVSS metrics.")},
    )


@dataclass
class CVE:
    """
    Common Vulnerabilities and Exposures (CVE) object for publicly disclosed vulnerabilities.

    CVE represents publicly disclosed cybersecurity vulnerabilities with standardized
    identifiers that enable consistent tracking and communication across organizations.

    Attributes:
        uid: CVE identifier (required) - format "CVE-YYYY-NNNNN"
        created_time: When the CVE record was created
        cvss: List of CVSS scoring information
        desc: Brief description of the vulnerability
        modified_time: When the CVE record was last updated
        references: List of reference URLs with additional information
        related_cwes: List of related CWE weaknesses
        title: Brief title summarizing the CVE
        type: Vulnerability type classification

    Example:
        >>> cve = CVE(
        ...     uid="CVE-2021-44228",
        ...     desc="Apache Log4j2 JNDI features do not protect against attacker controlled LDAP",
        ...     title="Log4Shell - Apache Log4j2 Remote Code Execution",
        ...     created_time=datetime(2021, 12, 9)
        ... )
    """

    uid: str = field(
        metadata={
            "description": (
                "The Common Vulnerabilities and Exposures unique number assigned "
                "to a specific computer vulnerability. A CVE Identifier begins with "
                "4 digits representing the year followed by a sequence of digits that "
                "acts as a unique identifier. For example: CVE-2021-12345."
            )
        }
    )
    created_time: Optional[datetime] = field(
        default=None,
        metadata={
            "description": (
                "The Record Creation Date identifies when the CVE ID was issued to a "
                "CVE Numbering Authority (CNA) or the CVE Record was published on the "
                "CVE List."
            )
        },
    )
    cvss: Optional[CVSS] = field(
        default=None,
        metadata={
            "description": (
                "The CVSS object details Common Vulnerability Scoring System (CVSS) "
                "scores from the advisory that are related to the vulnerability."
            )
        },
    )
    desc: Optional[str] = field(default=None, metadata={"description": "A brief description of the CVE Record."})
    modified_time: Optional[datetime] = field(
        default=None,
        metadata={"description": "The Record Modified Date identifies when the CVE record was last updated."},
    )
    references: Optional[List[str]] = field(
        default=None,
        metadata={"description": "A list of reference URLs with additional information about the CVE Record."},
    )
    cwe: Optional[CWE] = field(
        default=None,
        metadata={
            "description": ("Describes the Common Weakness Enumeration (CWE) details " "related to the CVE Record.")
        },
    )
    title: Optional[str] = field(
        default=None, metadata={"description": "A title or a brief phrase summarizing the CVE record."}
    )
    type: Optional[str] = field(
        default=None,
        metadata={
            "description": ("The vulnerability type as selected from a large dropdown menu " "during CVE refinement.")
        },
    )
    product: Optional[str] = field(
        default=None, metadata={"description": "The product name that contains the vulnerability."}
    )
