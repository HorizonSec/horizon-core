"""
Unit tests for OCSF enumerations module.

Tests all enumeration types and utility functions for OCSF v1.3.0 schema.
"""

import unittest

from horizon_core.reporting.models.ocsf.enums import (
    ActivityID,
    Confidence,
    ConfidenceID,
    Severity,
    SeverityID,
    Status,
    StatusID,
    get_confidence_by_id,
    get_severity_by_id,
    get_status_by_id,
)


class TestActivityID(unittest.TestCase):
    """Test cases for ActivityID enumeration."""

    def test_activity_id_values(self):
        """Test that ActivityID enum has correct values."""
        self.assertEqual(ActivityID.UNKNOWN.value, 0)
        self.assertEqual(ActivityID.CREATE.value, 1)
        self.assertEqual(ActivityID.UPDATE.value, 2)
        self.assertEqual(ActivityID.CLOSE.value, 3)
        self.assertEqual(ActivityID.OTHER.value, 99)

    def test_activity_id_names(self):
        """Test that ActivityID enum has correct names."""
        self.assertEqual(ActivityID.UNKNOWN.name, "UNKNOWN")
        self.assertEqual(ActivityID.CREATE.name, "CREATE")
        self.assertEqual(ActivityID.UPDATE.name, "UPDATE")
        self.assertEqual(ActivityID.CLOSE.name, "CLOSE")
        self.assertEqual(ActivityID.OTHER.name, "OTHER")

    def test_activity_id_uniqueness(self):
        """Test that all ActivityID values are unique."""
        values = [item.value for item in ActivityID]
        self.assertEqual(len(values), len(set(values)))


class TestSeverityID(unittest.TestCase):
    """Test cases for SeverityID enumeration."""

    def test_severity_id_values(self):
        """Test that SeverityID enum has correct values."""
        self.assertEqual(SeverityID.UNKNOWN.value, 0)
        self.assertEqual(SeverityID.INFORMATIONAL.value, 1)
        self.assertEqual(SeverityID.LOW.value, 2)
        self.assertEqual(SeverityID.MEDIUM.value, 3)
        self.assertEqual(SeverityID.HIGH.value, 4)
        self.assertEqual(SeverityID.CRITICAL.value, 5)
        self.assertEqual(SeverityID.FATAL.value, 6)
        self.assertEqual(SeverityID.OTHER.value, 99)

    def test_severity_id_names(self):
        """Test that SeverityID enum has correct names."""
        self.assertEqual(SeverityID.UNKNOWN.name, "UNKNOWN")
        self.assertEqual(SeverityID.INFORMATIONAL.name, "INFORMATIONAL")
        self.assertEqual(SeverityID.LOW.name, "LOW")
        self.assertEqual(SeverityID.MEDIUM.name, "MEDIUM")
        self.assertEqual(SeverityID.HIGH.name, "HIGH")
        self.assertEqual(SeverityID.CRITICAL.name, "CRITICAL")
        self.assertEqual(SeverityID.FATAL.name, "FATAL")
        self.assertEqual(SeverityID.OTHER.name, "OTHER")

    def test_severity_ordering(self):
        """Test that severity values are in correct order."""
        self.assertLess(SeverityID.UNKNOWN.value, SeverityID.INFORMATIONAL.value)
        self.assertLess(SeverityID.INFORMATIONAL.value, SeverityID.LOW.value)
        self.assertLess(SeverityID.LOW.value, SeverityID.MEDIUM.value)
        self.assertLess(SeverityID.MEDIUM.value, SeverityID.HIGH.value)
        self.assertLess(SeverityID.HIGH.value, SeverityID.CRITICAL.value)
        self.assertLess(SeverityID.CRITICAL.value, SeverityID.FATAL.value)


class TestSeverity(unittest.TestCase):
    """Test cases for Severity enumeration."""

    def test_severity_values(self):
        """Test that Severity enum has correct string values."""
        self.assertEqual(Severity.UNKNOWN.value, "Unknown")
        self.assertEqual(Severity.INFORMATIONAL.value, "Informational")
        self.assertEqual(Severity.LOW.value, "Low")
        self.assertEqual(Severity.MEDIUM.value, "Medium")
        self.assertEqual(Severity.HIGH.value, "High")
        self.assertEqual(Severity.CRITICAL.value, "Critical")
        self.assertEqual(Severity.FATAL.value, "Fatal")
        self.assertEqual(Severity.OTHER.value, "Other")

    def test_severity_string_representation(self):
        """Test string representations of severity levels."""
        self.assertEqual(str(Severity.HIGH.value), "High")
        self.assertEqual(str(Severity.CRITICAL.value), "Critical")


class TestStatusID(unittest.TestCase):
    """Test cases for StatusID enumeration."""

    def test_status_id_values(self):
        """Test that StatusID enum has correct values."""
        self.assertEqual(StatusID.UNKNOWN.value, 0)
        self.assertEqual(StatusID.NEW.value, 1)
        self.assertEqual(StatusID.IN_PROGRESS.value, 2)
        self.assertEqual(StatusID.SUPPRESSED.value, 3)
        self.assertEqual(StatusID.RESOLVED.value, 4)
        self.assertEqual(StatusID.OTHER.value, 99)

    def test_status_id_names(self):
        """Test that StatusID enum has correct names."""
        self.assertEqual(StatusID.UNKNOWN.name, "UNKNOWN")
        self.assertEqual(StatusID.NEW.name, "NEW")
        self.assertEqual(StatusID.IN_PROGRESS.name, "IN_PROGRESS")
        self.assertEqual(StatusID.SUPPRESSED.name, "SUPPRESSED")
        self.assertEqual(StatusID.RESOLVED.name, "RESOLVED")
        self.assertEqual(StatusID.OTHER.name, "OTHER")


class TestStatus(unittest.TestCase):
    """Test cases for Status enumeration."""

    def test_status_values(self):
        """Test that Status enum has correct string values."""
        self.assertEqual(Status.UNKNOWN.value, "Unknown")
        self.assertEqual(Status.NEW.value, "New")
        self.assertEqual(Status.IN_PROGRESS.value, "In Progress")
        self.assertEqual(Status.SUPPRESSED.value, "Suppressed")
        self.assertEqual(Status.RESOLVED.value, "Resolved")
        self.assertEqual(Status.OTHER.value, "Other")

    def test_status_workflow(self):
        """Test that status values represent logical workflow."""
        workflow_statuses = [Status.NEW, Status.IN_PROGRESS, Status.RESOLVED]
        self.assertTrue(all(isinstance(status.value, str) for status in workflow_statuses))


class TestConfidenceID(unittest.TestCase):
    """Test cases for ConfidenceID enumeration."""

    def test_confidence_id_values(self):
        """Test that ConfidenceID enum has correct values."""
        self.assertEqual(ConfidenceID.UNKNOWN.value, 0)
        self.assertEqual(ConfidenceID.LOW.value, 1)
        self.assertEqual(ConfidenceID.MEDIUM.value, 2)
        self.assertEqual(ConfidenceID.HIGH.value, 3)
        self.assertEqual(ConfidenceID.OTHER.value, 99)

    def test_confidence_ordering(self):
        """Test that confidence values are in ascending order."""
        self.assertLess(ConfidenceID.LOW.value, ConfidenceID.MEDIUM.value)
        self.assertLess(ConfidenceID.MEDIUM.value, ConfidenceID.HIGH.value)


class TestConfidence(unittest.TestCase):
    """Test cases for Confidence enumeration."""

    def test_confidence_values(self):
        """Test that Confidence enum has correct string values."""
        self.assertEqual(Confidence.UNKNOWN.value, "Unknown")
        self.assertEqual(Confidence.LOW.value, "Low")
        self.assertEqual(Confidence.MEDIUM.value, "Medium")
        self.assertEqual(Confidence.HIGH.value, "High")
        self.assertEqual(Confidence.OTHER.value, "Other")


class TestUtilityFunctions(unittest.TestCase):
    """Test cases for enum utility functions."""

    def test_get_severity_by_id(self):
        """Test severity lookup by ID."""
        self.assertEqual(get_severity_by_id(SeverityID.HIGH.value), Severity.HIGH.value)
        self.assertEqual(get_severity_by_id(SeverityID.CRITICAL.value), Severity.CRITICAL.value)
        self.assertEqual(get_severity_by_id(SeverityID.UNKNOWN.value), Severity.UNKNOWN.value)

    def test_get_severity_by_id_invalid(self):
        """Test severity lookup with invalid input."""
        result = get_severity_by_id(999)  # Invalid ID should return default
        self.assertEqual(result, Severity.UNKNOWN.value)

    def test_get_status_by_id(self):
        """Test status lookup by ID."""
        self.assertEqual(get_status_by_id(StatusID.NEW.value), Status.NEW.value)
        self.assertEqual(get_status_by_id(StatusID.IN_PROGRESS.value), Status.IN_PROGRESS.value)
        self.assertEqual(get_status_by_id(StatusID.RESOLVED.value), Status.RESOLVED.value)

    def test_get_status_by_id_invalid(self):
        """Test status lookup with invalid input."""
        result = get_status_by_id(999)  # Invalid ID should return default
        self.assertEqual(result, Status.UNKNOWN.value)

    def test_get_confidence_by_id(self):
        """Test confidence lookup by ID."""
        self.assertEqual(get_confidence_by_id(ConfidenceID.LOW.value), Confidence.LOW.value)
        self.assertEqual(get_confidence_by_id(ConfidenceID.MEDIUM.value), Confidence.MEDIUM.value)
        self.assertEqual(get_confidence_by_id(ConfidenceID.HIGH.value), Confidence.HIGH.value)

    def test_get_confidence_by_id_invalid(self):
        """Test confidence lookup with invalid input."""
        result = get_confidence_by_id(999)  # Invalid ID should return default
        self.assertEqual(result, Confidence.UNKNOWN.value)


class TestEnumIntegration(unittest.TestCase):
    """Integration tests for enum relationships."""

    def test_severity_id_to_severity_mapping(self):
        """Test that severity ID maps correctly to severity string."""
        test_cases = [
            (SeverityID.LOW.value, Severity.LOW.value),
            (SeverityID.MEDIUM.value, Severity.MEDIUM.value),
            (SeverityID.HIGH.value, Severity.HIGH.value),
            (SeverityID.CRITICAL.value, Severity.CRITICAL.value),
        ]

        for severity_id, expected_severity in test_cases:
            self.assertEqual(get_severity_by_id(severity_id), expected_severity)

    def test_status_id_to_status_mapping(self):
        """Test that status ID maps correctly to status string."""
        test_cases = [
            (StatusID.NEW.value, Status.NEW.value),
            (StatusID.IN_PROGRESS.value, Status.IN_PROGRESS.value),
            (StatusID.SUPPRESSED.value, Status.SUPPRESSED.value),
            (StatusID.RESOLVED.value, Status.RESOLVED.value),
        ]

        for status_id, expected_status in test_cases:
            self.assertEqual(get_status_by_id(status_id), expected_status)

    def test_confidence_id_to_confidence_mapping(self):
        """Test that confidence ID maps correctly to confidence string."""
        test_cases = [
            (ConfidenceID.LOW.value, Confidence.LOW.value),
            (ConfidenceID.MEDIUM.value, Confidence.MEDIUM.value),
            (ConfidenceID.HIGH.value, Confidence.HIGH.value),
        ]

        for confidence_id, expected_confidence in test_cases:
            self.assertEqual(get_confidence_by_id(confidence_id), expected_confidence)

    def test_all_enums_have_unknown_and_other(self):
        """Test that all enums have UNKNOWN and OTHER values."""
        # Test ActivityID
        self.assertTrue(hasattr(ActivityID, "UNKNOWN"))
        self.assertTrue(hasattr(ActivityID, "OTHER"))
        self.assertEqual(ActivityID.UNKNOWN.value, 0)
        self.assertEqual(ActivityID.OTHER.value, 99)

        # Test SeverityID
        self.assertTrue(hasattr(SeverityID, "UNKNOWN"))
        self.assertTrue(hasattr(SeverityID, "OTHER"))
        self.assertEqual(SeverityID.UNKNOWN.value, 0)
        self.assertEqual(SeverityID.OTHER.value, 99)

        # Test StatusID
        self.assertTrue(hasattr(StatusID, "UNKNOWN"))
        self.assertTrue(hasattr(StatusID, "OTHER"))
        self.assertEqual(StatusID.UNKNOWN.value, 0)
        self.assertEqual(StatusID.OTHER.value, 99)

        # Test ConfidenceID
        self.assertTrue(hasattr(ConfidenceID, "UNKNOWN"))
        self.assertTrue(hasattr(ConfidenceID, "OTHER"))
        self.assertEqual(ConfidenceID.UNKNOWN.value, 0)
        self.assertEqual(ConfidenceID.OTHER.value, 99)


if __name__ == "__main__":
    unittest.main()
