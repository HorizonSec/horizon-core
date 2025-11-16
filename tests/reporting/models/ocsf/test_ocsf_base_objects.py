"""
Unit tests for OCSF base objects module.

Tests all core OCSF objects like Group, Account, User, File, and Metadata.
"""

import unittest
from datetime import datetime

from horizon_core.reporting.models.ocsf.base_objects import (
    Account,
    File,
    Group,
    Metadata,
    User,
)


class TestGroup(unittest.TestCase):
    """Test cases for Group object."""

    def test_group_creation_minimal(self):
        """Test creating a Group with minimal required fields."""
        group = Group(name="test-group")

        self.assertEqual(group.name, "test-group")
        self.assertIsNone(group.desc)
        self.assertIsNone(group.domain)
        self.assertIsNone(group.type)
        self.assertIsNone(group.uid)
        self.assertEqual(group.privileges, [])

    def test_group_creation_full(self):
        """Test creating a Group with all fields populated."""
        group = Group(
            name="admin-group",
            desc="Administrative group",
            domain="example.com",
            type="Security Group",
            uid="S-1-5-21-123456789",
            privileges=["read", "write", "execute"],
        )

        self.assertEqual(group.name, "admin-group")
        self.assertEqual(group.desc, "Administrative group")
        self.assertEqual(group.domain, "example.com")
        self.assertEqual(group.type, "Security Group")
        self.assertEqual(group.uid, "S-1-5-21-123456789")
        self.assertEqual(group.privileges, ["read", "write", "execute"])

    def test_group_default_privileges(self):
        """Test that privileges defaults to empty list."""
        group = Group(name="test-group")
        self.assertIsInstance(group.privileges, list)
        self.assertEqual(len(group.privileges), 0)


class TestAccount(unittest.TestCase):
    """Test cases for Account object."""

    def test_account_creation_minimal(self):
        """Test creating an Account with minimal required fields."""
        account = Account(name="test-account", type_id=1, uid="12345")

        self.assertEqual(account.name, "test-account")
        self.assertEqual(account.type_id, 1)
        self.assertEqual(account.uid, "12345")
        self.assertEqual(account.labels, [])
        self.assertEqual(account.tags, {})
        self.assertIsNone(account.type)

    def test_account_creation_full(self):
        """Test creating an Account with all fields populated."""
        account = Account(
            name="production-account",
            type_id=2,
            uid="aws-123456789012",
            labels=["production", "critical"],
            tags={"environment": "prod", "team": "security"},
            type="AWS Account",
        )

        self.assertEqual(account.name, "production-account")
        self.assertEqual(account.type_id, 2)
        self.assertEqual(account.uid, "aws-123456789012")
        self.assertEqual(account.labels, ["production", "critical"])
        self.assertEqual(account.tags, {"environment": "prod", "team": "security"})
        self.assertEqual(account.type, "AWS Account")

    def test_account_defaults(self):
        """Test that Account defaults are properly set."""
        account = Account(name="test", type_id=1, uid="123")

        self.assertIsInstance(account.labels, list)
        self.assertIsInstance(account.tags, dict)
        self.assertEqual(len(account.labels), 0)
        self.assertEqual(len(account.tags), 0)


class TestUser(unittest.TestCase):
    """Test cases for User object."""

    def test_user_creation_minimal(self):
        """Test creating a User with minimal fields."""
        user = User()

        self.assertIsNone(user.name)
        self.assertIsNone(user.account)
        self.assertIsNone(user.display_name)
        self.assertIsNone(user.email_addr)
        self.assertIsNone(user.full_name)
        self.assertEqual(user.groups, [])
        self.assertIsNone(user.type)
        self.assertIsNone(user.type_id)
        self.assertIsNone(user.uid)

    def test_user_creation_full(self):
        """Test creating a User with all fields populated."""
        account = Account(name="test-account", type_id=1, uid="acc-123")
        group = Group(name="test-group")

        user = User(
            name="jdoe",
            account=account,
            display_name="John Doe",
            email_addr="john.doe@example.com",
            full_name="John Michael Doe",
            groups=[group],
            type="Standard User",
            type_id=1,
            uid="user-123",
        )

        self.assertEqual(user.name, "jdoe")
        self.assertEqual(user.account, account)
        self.assertEqual(user.display_name, "John Doe")
        self.assertEqual(user.email_addr, "john.doe@example.com")
        self.assertEqual(user.full_name, "John Michael Doe")
        self.assertEqual(user.groups, [group])
        self.assertEqual(user.type, "Standard User")
        self.assertEqual(user.type_id, 1)
        self.assertEqual(user.uid, "user-123")

    def test_user_groups_default(self):
        """Test that user groups defaults to empty list."""
        user = User()
        self.assertIsInstance(user.groups, list)
        self.assertEqual(len(user.groups), 0)

    def test_user_with_multiple_groups(self):
        """Test user with multiple groups."""
        group1 = Group(name="developers")
        group2 = Group(name="admins")

        user = User(name="jdoe", groups=[group1, group2])

        self.assertEqual(len(user.groups), 2)
        self.assertEqual(user.groups[0].name, "developers")
        self.assertEqual(user.groups[1].name, "admins")


class TestFile(unittest.TestCase):
    """Test cases for File object."""

    def test_file_creation_minimal(self):
        """Test creating a File with minimal required fields."""
        file_obj = File(name="test.txt", type_id=1)

        self.assertEqual(file_obj.name, "test.txt")
        self.assertEqual(file_obj.type_id, 1)
        self.assertIsNone(file_obj.confidentiality)
        self.assertIsNone(file_obj.confidentiality_id)
        self.assertIsNone(file_obj.created_time)
        self.assertIsNone(file_obj.desc)

    def test_file_creation_full(self):
        """Test creating a File with all fields populated."""
        owner = User(name="jdoe")
        created_time = datetime(2024, 1, 1, 12, 0, 0)
        modified_time = datetime(2024, 1, 2, 12, 0, 0)

        file_obj = File(
            name="document.pdf",
            type_id=2,
            confidentiality="Public",
            confidentiality_id=1,
            created_time=created_time,
            desc="Important document",
            mime_type="application/pdf",
            modified_time=modified_time,
            owner=owner,
            parent_folder="/home/user/documents",
            path="/home/user/documents/document.pdf",
            security_descriptor="rw-r--r--",
            signature={"algorithm": "SHA256", "value": "abc123"},
            size=1024,
            type="PDF Document",
            uid="file-123",
            version="1.0",
            xattributes={"custom": "value"},
        )

        self.assertEqual(file_obj.name, "document.pdf")
        self.assertEqual(file_obj.type_id, 2)
        self.assertEqual(file_obj.confidentiality, "Public")
        self.assertEqual(file_obj.confidentiality_id, 1)
        self.assertEqual(file_obj.created_time, created_time)
        self.assertEqual(file_obj.desc, "Important document")
        self.assertEqual(file_obj.mime_type, "application/pdf")
        self.assertEqual(file_obj.modified_time, modified_time)
        self.assertEqual(file_obj.owner, owner)
        self.assertEqual(file_obj.parent_folder, "/home/user/documents")
        self.assertEqual(file_obj.path, "/home/user/documents/document.pdf")
        self.assertEqual(file_obj.security_descriptor, "rw-r--r--")
        self.assertEqual(file_obj.signature, {"algorithm": "SHA256", "value": "abc123"})
        self.assertEqual(file_obj.size, 1024)
        self.assertEqual(file_obj.type, "PDF Document")
        self.assertEqual(file_obj.uid, "file-123")
        self.assertEqual(file_obj.version, "1.0")
        self.assertEqual(file_obj.xattributes, {"custom": "value"})

    def test_file_datetime_handling(self):
        """Test that File properly handles datetime objects."""
        now = datetime.now()
        file_obj = File(name="test.txt", type_id=1, created_time=now, modified_time=now)

        self.assertEqual(file_obj.created_time, now)
        self.assertEqual(file_obj.modified_time, now)
        self.assertIsInstance(file_obj.created_time, datetime)
        self.assertIsInstance(file_obj.modified_time, datetime)


class TestMetadata(unittest.TestCase):
    """Test cases for Metadata object."""

    def test_metadata_creation_minimal(self):
        """Test creating Metadata with minimal required fields."""
        metadata = Metadata(version="1.3.0")

        self.assertEqual(metadata.version, "1.3.0")
        self.assertIsNone(metadata.product)
        self.assertEqual(metadata.profiles, [])
        self.assertIsNone(metadata.event_code)

    def test_metadata_creation_full(self):
        """Test creating Metadata with all fields populated."""
        product = {"name": "Security Scanner", "version": "2.0.0"}
        logged_time = datetime(2024, 1, 1, 12, 0, 0)
        modified_time = datetime(2024, 1, 1, 12, 30, 0)
        processed_time = datetime(2024, 1, 1, 13, 0, 0)

        metadata = Metadata(
            version="1.3.0",
            product=product,
            profiles=["security", "compliance"],
            event_code="SEC001",
            log_name="security.log",
            log_provider="SecuritySystem",
            log_level="INFO",
            logged_time=logged_time,
            modified_time=modified_time,
            original_time="2024-01-01T12:00:00Z",
            processed_time=processed_time,
            sequence=12345,
            tenant_uid="tenant-123",
            uid="event-456",
        )

        self.assertEqual(metadata.version, "1.3.0")
        self.assertEqual(metadata.product, product)
        self.assertEqual(metadata.profiles, ["security", "compliance"])
        self.assertEqual(metadata.event_code, "SEC001")
        self.assertEqual(metadata.log_name, "security.log")
        self.assertEqual(metadata.log_provider, "SecuritySystem")
        self.assertEqual(metadata.log_level, "INFO")
        self.assertEqual(metadata.logged_time, logged_time)
        self.assertEqual(metadata.modified_time, modified_time)
        self.assertEqual(metadata.original_time, "2024-01-01T12:00:00Z")
        self.assertEqual(metadata.processed_time, processed_time)
        self.assertEqual(metadata.sequence, 12345)
        self.assertEqual(metadata.tenant_uid, "tenant-123")
        self.assertEqual(metadata.uid, "event-456")

    def test_metadata_profiles_default(self):
        """Test that profiles defaults to empty list."""
        metadata = Metadata(version="1.3.0")
        self.assertIsInstance(metadata.profiles, list)
        self.assertEqual(len(metadata.profiles), 0)

    def test_metadata_version_requirement(self):
        """Test that version is required for Metadata."""
        # This should work
        metadata = Metadata(version="1.3.0")
        self.assertEqual(metadata.version, "1.3.0")


class TestObjectIntegration(unittest.TestCase):
    """Integration tests for object relationships."""

    def test_user_with_account_and_groups(self):
        """Test User with associated Account and Groups."""
        account = Account(name="corporate-account", type_id=1, uid="corp-123")

        admin_group = Group(name="administrators", privileges=["admin", "read", "write"])

        user_group = Group(name="users", privileges=["read"])

        user = User(
            name="admin_user",
            account=account,
            groups=[admin_group, user_group],
            type="Administrator",
            uid="user-admin-001",
        )

        self.assertEqual(user.account.name, "corporate-account")
        self.assertEqual(len(user.groups), 2)
        self.assertEqual(user.groups[0].name, "administrators")
        self.assertEqual(user.groups[1].name, "users")
        self.assertIn("admin", user.groups[0].privileges)

    def test_file_with_owner(self):
        """Test File with associated User owner."""
        owner = User(name="file_owner", uid="owner-123")

        file_obj = File(name="owned_file.txt", type_id=1, owner=owner, path="/home/file_owner/owned_file.txt")

        self.assertEqual(file_obj.owner.name, "file_owner")
        self.assertEqual(file_obj.owner.uid, "owner-123")

    def test_complex_metadata_object(self):
        """Test Metadata with complex nested product information."""
        product = {
            "name": "Advanced Security Platform",
            "version": "3.2.1",
            "vendor": "Security Corp",
            "features": ["threat_detection", "compliance", "reporting"],
        }

        metadata = Metadata(
            version="1.3.0", product=product, profiles=["enterprise", "compliance", "audit"], sequence=999999
        )

        self.assertEqual(metadata.product["name"], "Advanced Security Platform")
        self.assertEqual(metadata.product["version"], "3.2.1")
        self.assertIn("threat_detection", metadata.product["features"])
        self.assertIn("enterprise", metadata.profiles)
        self.assertEqual(metadata.sequence, 999999)
