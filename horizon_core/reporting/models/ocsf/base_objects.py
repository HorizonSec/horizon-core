"""
OCSF Base Objects Module

This module contains fundamental OCSF objects that represent core entities
in cybersecurity data models, including users, groups, accounts, files,
and metadata structures.

These objects serve as building blocks for more complex OCSF event types
and finding structures throughout the schema.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

__all__ = [
    "Group",
    "Account",
    "User",
    "File",
    "Metadata",
]


@dataclass
class Group:
    """
    The Group object describes a security group.

    Groups are collections of users or other principals that share common
    access rights and permissions within a system or application.

    Attributes:
        name: The group name (required)
        desc: Optional description of the group's purpose
        domain: The domain where the group is defined (e.g., LDAP, Active Directory)
        type: The group type classification (e.g., "Security Group")
        uid: Unique identifier for the group (e.g., Windows SID)
        privileges: List of specific privileges granted to group members

    Example:
        >>> group = Group(
        ...     name="Administrators",
        ...     desc="System administrators group",
        ...     domain="company.local",
        ...     type="Security Group",
        ...     uid="S-1-5-32-544",
        ...     privileges=["LogonAsService", "BackupPrivilege"]
        ... )
    """

    name: str = field(metadata={"description": "The group name."})
    desc: Optional[str] = field(default=None, metadata={"description": "The group description."})
    domain: Optional[str] = field(
        default=None,
        metadata={
            "description": (
                "The domain where the group is defined. For example: " "the LDAP or Active Directory domain."
            )
        },
    )
    type: Optional[str] = field(default=None, metadata={"description": "The group type, e.g., Security Group."})
    uid: Optional[str] = field(
        default=None,
        metadata={
            "description": (
                "The unique identifier of the group. For example, "
                "for Windows events this is the security identifier (SID) of the group."
            )
        },
    )
    privileges: List[str] = field(default_factory=list, metadata={"description": "The list of group privileges."})


@dataclass
class Account:
    """
    The Account object describes a set of characteristics for an account.

    Accounts represent user accounts, service accounts, or organizational
    accounts across various cloud and on-premises systems.

    Attributes:
        name: The account name (required)
        type_id: Numeric identifier for the account type (required)
        uid: Unique account identifier (required)
        labels: List of labels associated with the account
        tags: Dictionary of key-value tags for the account
        type: Human-readable account type description

    Example:
        >>> account = Account(
        ...     name="production-web-service",
        ...     type_id=10,  # AWS Account type
        ...     uid="123456789012",
        ...     labels=["production", "web-tier"],
        ...     tags={"Environment": "prod", "Team": "platform"},
        ...     type="AWS Account"
        ... )
    """

    name: str = field(
        metadata={
            "description": (
                "The name of the account (e.g. GCP Project name, " "Linux Account name or AWS Account name)."
            )
        }
    )
    type_id: int = field(metadata={"description": "The normalized account type identifier."})
    uid: str = field(
        metadata={
            "description": (
                "The unique identifier of the account (e.g. AWS Account ID, OCID, "
                "GCP Project ID, Azure Subscription ID, Google Workspace Customer ID, "
                "or M365 Tenant UID)."
            )
        }
    )
    labels: List[str] = field(
        default_factory=list, metadata={"description": "The list of labels associated with the account."}
    )
    tags: Dict[str, str] = field(
        default_factory=dict, metadata={"description": "The list of tags associated with the account."}
    )
    type: Optional[str] = field(
        default=None,
        metadata={
            "description": (
                "The account type, normalized to the caption of account_type_id. "
                "In the case of Other, it is defined by the event source."
            )
        },
    )


@dataclass
class User:
    """
    The User object describes characteristics of a user/person or security principal.

    Users represent human users, service accounts, or other security principals
    that can perform actions within systems and applications.

    Attributes:
        name: The username/login name
        account: Associated account information
        display_name: Human-friendly display name
        email_addr: Primary email address
        full_name: Full legal or display name
        groups: List of groups the user belongs to
        type: User type classification
        type_id: Numeric user type identifier
        uid: Unique user identifier (e.g., SID, DN, ARN)

    Example:
        >>> user = User(
        ...     name="jdoe",
        ...     display_name="John Doe",
        ...     email_addr="john.doe@company.com",
        ...     full_name="John Michael Doe",
        ...     type="User",
        ...     type_id=1,
        ...     uid="S-1-5-21-1004336348-1177238915-682003330-1234"
        ... )
    """

    name: Optional[str] = field(default=None, metadata={"description": "The username. For example, janedoe1."})
    account: Optional[Account] = field(
        default=None, metadata={"description": "The account information associated with the user."}
    )
    display_name: Optional[str] = field(
        default=None,
        metadata={
            "description": ("The display name of the user, as reported by the product. " "For example, Jane Doe.")
        },
    )
    email_addr: Optional[str] = field(default=None, metadata={"description": "The user primary email address."})
    full_name: Optional[str] = field(
        default=None,
        metadata={"description": ("The full name of the user, as reported by the product. " "For example, Jane Doe.")},
    )
    groups: List[Group] = field(
        default_factory=list, metadata={"description": "The groups that the user is a member of."}
    )
    type: Optional[str] = field(
        default=None, metadata={"description": "The type of the user. For example, System, AWS IAM User, etc."}
    )
    type_id: Optional[int] = field(default=None, metadata={"description": "The normalized user type identifier."})
    uid: Optional[str] = field(
        default=None,
        metadata={
            "description": (
                "The unique user identifier. For example, the Windows user SID, " "ActiveDirectory DN or AWS user ARN."
            )
        },
    )


@dataclass
class File:
    """
    The File object represents metadata associated with a file in a computer system.

    Files are fundamental objects in cybersecurity, representing data stored
    on filesystems that may be subject to analysis, access control, or monitoring.

    Attributes:
        name: The filename (required)
        type_id: Numeric file type identifier (required)
        confidentiality: Data confidentiality classification
        confidentiality_id: Numeric confidentiality level
        created_time: File creation timestamp
        desc: File description from filesystem
        mime_type: MIME type of the file content
        modified_time: Last modification timestamp
        owner: User who owns the file
        parent_folder: Parent directory path
        path: Full file path
        size: File size in bytes
        type: Human-readable file type
        uid: Unique file identifier from storage system
        version: File version string

    Example:
        >>> file_obj = File(
        ...     name="malware.exe",
        ...     type_id=8,  # Executable file
        ...     path=r"C:\\temp\\malware.exe",
        ...     size=1048576,
        ...     type="Executable File",
        ...     created_time=datetime.now()
        ... )
    """

    name: str = field(metadata={"description": "The name of the file. For example: svchost.exe"})
    type_id: int = field(metadata={"description": "The file type ID."})
    confidentiality: Optional[str] = field(
        default=None,
        metadata={"description": ("The file content confidentiality, normalized to the " "confidentiality_id value.")},
    )
    confidentiality_id: Optional[int] = field(
        default=None,
        metadata={"description": ("The normalized identifier of the file content " "confidentiality indicator.")},
    )
    created_time: Optional[datetime] = field(
        default=None, metadata={"description": "The time when the file was created."}
    )
    desc: Optional[str] = field(
        default=None, metadata={"description": "The description of the file, as returned by file system."}
    )
    mime_type: Optional[str] = field(
        default=None,
        metadata={
            "description": ("The Multipurpose Internet Mail Extensions (MIME) type of " "the file, if applicable.")
        },
    )
    modified_time: Optional[datetime] = field(
        default=None, metadata={"description": "The time when the file was last modified."}
    )
    owner: Optional[User] = field(default=None, metadata={"description": "The user that owns the file/object."})
    parent_folder: Optional[str] = field(
        default=None,
        metadata={"description": ("The parent folder in which the file resides. " r"For example: c:\windows\system32")},
    )
    path: Optional[str] = field(
        default=None,
        metadata={"description": ("The full path to the file. " r"For example: c:\windows\system32\svchost.exe")},
    )
    size: Optional[int] = field(default=None, metadata={"description": "The size of data, in bytes."})
    type: Optional[str] = field(default=None, metadata={"description": "The file type."})
    uid: Optional[str] = field(
        default=None, metadata={"description": "The unique identifier of the file as defined by the storage system."}
    )
    version: Optional[str] = field(
        default=None, metadata={"description": "The file version. For example: 8.0.7601.17514"}
    )
    security_descriptor: Optional[str] = field(
        default=None, metadata={"description": "The security descriptor string for the file."}
    )
    signature: Optional[Dict[str, Any]] = field(
        default=None, metadata={"description": "The digital signature information for the file."}
    )
    xattributes: Optional[Dict[str, Any]] = field(
        default=None, metadata={"description": "Extended attributes associated with the file."}
    )


@dataclass
class Metadata:
    """
    The Metadata object associated with events or findings.

    Metadata provides context about how events were generated, including
    the source product, schema version, and various identifiers used
    for correlation and analysis.

    Attributes:
        version: OCSF schema version in SemVer format (required)
        product: Details about the product that generated the event
        profiles: List of OCSF profiles used to create the event
        event_code: Event code as reported by the source
        log_name: Name of the log source (e.g., syslog file, Windows log)
        log_provider: Logging service or provider that created the log
        original_time: Original event time as reported by source system

    Example:
        >>> metadata = Metadata(
        ...     version="1.3.0",
        ...     product={"name": "ACME Security Scanner", "version": "2.1.0"},
        ...     profiles=["security", "vulnerability"],
        ...     event_code="VULN_001",
        ...     log_name="security.log"
        ... )
    """

    version: str = field(
        metadata={
            "description": ("The version of the OCSF schema, in Semantic Versioning " "Specification (SemVer) format.")
        }
    )
    product: Optional[Dict[str, Any]] = field(
        default=None, metadata={"description": "The details about the product that reported the event."}
    )
    profiles: List[str] = field(
        default_factory=list, metadata={"description": "The list of profiles used to create the event."}
    )
    event_code: Optional[str] = field(
        default=None, metadata={"description": "The event code as reported by the event source."}
    )
    log_name: Optional[str] = field(
        default=None, metadata={"description": "The event log name. For example, syslog file name or Windows log name."}
    )
    log_provider: Optional[str] = field(
        default=None, metadata={"description": "The logging provider or logging service that logged the event."}
    )
    original_time: Optional[str] = field(
        default=None, metadata={"description": "The original event time as reported by the event source."}
    )
    log_level: Optional[str] = field(
        default=None, metadata={"description": "The log level or severity level of the event."}
    )
    logged_time: Optional[datetime] = field(
        default=None, metadata={"description": "The time when the event was logged."}
    )
    modified_time: Optional[datetime] = field(
        default=None, metadata={"description": "The time when the event metadata was last modified."}
    )
    processed_time: Optional[datetime] = field(
        default=None, metadata={"description": "The time when the event was processed."}
    )
    sequence: Optional[int] = field(default=None, metadata={"description": "The sequence number of the event."})
    tenant_uid: Optional[str] = field(default=None, metadata={"description": "The unique identifier of the tenant."})
    uid: Optional[str] = field(default=None, metadata={"description": "The unique identifier of the event."})
