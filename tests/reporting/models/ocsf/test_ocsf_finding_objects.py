"""
Unit tests for OCSF finding objects module.

Tests the FindingInfo object which contains metadata about security findings.
"""

import unittest
from datetime import datetime

from horizon_core.reporting.models.ocsf.finding_objects import (
    FindingInfo,
)


class TestFindingInfo(unittest.TestCase):
    """Test cases for FindingInfo object."""

    def test_finding_info_creation_minimal(self):
        """Test creating a FindingInfo with minimal required fields."""
        finding_info = FindingInfo(uid="finding-123")

        self.assertEqual(finding_info.uid, "finding-123")
        self.assertIsNone(finding_info.created_time)
        self.assertEqual(finding_info.data_sources, [])
        self.assertIsNone(finding_info.desc)
        self.assertIsNone(finding_info.first_seen_time)
        self.assertIsNone(finding_info.last_seen_time)
        self.assertIsNone(finding_info.modified_time)
        self.assertIsNone(finding_info.product_uid)
        self.assertEqual(finding_info.related_events, [])
        self.assertIsNone(finding_info.remediation)
        self.assertIsNone(finding_info.src_url)
        self.assertIsNone(finding_info.supporting_data)
        self.assertIsNone(finding_info.title)
        self.assertEqual(finding_info.types, [])

    def test_finding_info_creation_full(self):
        """Test creating a FindingInfo with all fields populated."""
        created_time = datetime(2024, 1, 1, 12, 0, 0)
        first_seen_time = datetime(2024, 1, 1, 10, 0, 0)
        last_seen_time = datetime(2024, 1, 1, 14, 0, 0)
        modified_time = datetime(2024, 1, 1, 13, 0, 0)

        supporting_data = {"scan_engine": "SecurityScanner v2.1", "rule_id": "R001", "confidence_score": 95}

        related_events = [{"event_id": "evt-001", "type": "network_scan"}, {"event_id": "evt-002", "type": "file_scan"}]

        finding_info = FindingInfo(
            uid="vuln-finding-456",
            created_time=created_time,
            data_sources=["network_scanner", "file_scanner", "vulnerability_db"],
            desc="Critical vulnerability detected in system component",
            first_seen_time=first_seen_time,
            last_seen_time=last_seen_time,
            modified_time=modified_time,
            product_uid="scanner-product-789",
            related_events=related_events,
            remediation="Apply security patch version 2.1.5 or higher",
            src_url="https://security.example.com/findings/vuln-finding-456",
            supporting_data=supporting_data,
            title="Critical Buffer Overflow Vulnerability",
            types=["vulnerability", "security", "buffer_overflow"],
        )

        self.assertEqual(finding_info.uid, "vuln-finding-456")
        self.assertEqual(finding_info.created_time, created_time)
        self.assertEqual(finding_info.data_sources, ["network_scanner", "file_scanner", "vulnerability_db"])
        self.assertEqual(finding_info.desc, "Critical vulnerability detected in system component")
        self.assertEqual(finding_info.first_seen_time, first_seen_time)
        self.assertEqual(finding_info.last_seen_time, last_seen_time)
        self.assertEqual(finding_info.modified_time, modified_time)
        self.assertEqual(finding_info.product_uid, "scanner-product-789")
        self.assertEqual(finding_info.related_events, related_events)
        self.assertEqual(finding_info.remediation, "Apply security patch version 2.1.5 or higher")
        self.assertEqual(finding_info.src_url, "https://security.example.com/findings/vuln-finding-456")
        self.assertEqual(finding_info.supporting_data, supporting_data)
        self.assertEqual(finding_info.title, "Critical Buffer Overflow Vulnerability")
        self.assertEqual(finding_info.types, ["vulnerability", "security", "buffer_overflow"])

    def test_finding_info_defaults(self):
        """Test that FindingInfo defaults are properly set."""
        finding_info = FindingInfo(uid="test-123")

        self.assertIsInstance(finding_info.data_sources, list)
        self.assertIsInstance(finding_info.related_events, list)
        self.assertIsInstance(finding_info.types, list)

        self.assertEqual(len(finding_info.data_sources), 0)
        self.assertEqual(len(finding_info.related_events), 0)
        self.assertEqual(len(finding_info.types), 0)

    def test_finding_info_datetime_handling(self):
        """Test that FindingInfo properly handles datetime objects."""
        now = datetime.now()
        yesterday = datetime(2024, 1, 1, 12, 0, 0)

        finding_info = FindingInfo(
            uid="datetime-test", created_time=now, first_seen_time=yesterday, last_seen_time=now, modified_time=now
        )

        self.assertEqual(finding_info.created_time, now)
        self.assertEqual(finding_info.first_seen_time, yesterday)
        self.assertEqual(finding_info.last_seen_time, now)
        self.assertEqual(finding_info.modified_time, now)

        self.assertIsInstance(finding_info.created_time, datetime)
        self.assertIsInstance(finding_info.first_seen_time, datetime)
        self.assertIsInstance(finding_info.last_seen_time, datetime)
        self.assertIsInstance(finding_info.modified_time, datetime)

    def test_finding_info_data_sources(self):
        """Test FindingInfo with various data sources."""
        data_sources = [
            "vulnerability_scanner",
            "network_monitor",
            "log_analyzer",
            "threat_intelligence",
            "compliance_checker",
        ]

        finding_info = FindingInfo(uid="multi-source-finding", data_sources=data_sources)

        self.assertEqual(len(finding_info.data_sources), 5)
        self.assertIn("vulnerability_scanner", finding_info.data_sources)
        self.assertIn("threat_intelligence", finding_info.data_sources)
        self.assertEqual(finding_info.data_sources, data_sources)

    def test_finding_info_types(self):
        """Test FindingInfo with various finding types."""
        finding_types = [
            "vulnerability",
            "compliance_violation",
            "security_misconfiguration",
            "malware_detection",
            "data_breach",
        ]

        finding_info = FindingInfo(uid="multi-type-finding", types=finding_types)

        self.assertEqual(len(finding_info.types), 5)
        self.assertIn("vulnerability", finding_info.types)
        self.assertIn("data_breach", finding_info.types)
        self.assertEqual(finding_info.types, finding_types)

    def test_finding_info_supporting_data(self):
        """Test FindingInfo with complex supporting data."""
        supporting_data = {
            "scanner_info": {"name": "VulnScan Pro", "version": "3.2.1", "engine": "Static Analysis"},
            "detection_rules": [{"rule_id": "R001", "severity": "High"}, {"rule_id": "R045", "severity": "Critical"}],
            "metrics": {"confidence_score": 98, "false_positive_probability": 0.02, "severity_score": 9.5},
            "environment": {"os": "Linux", "architecture": "x86_64", "kernel_version": "5.4.0"},
        }

        finding_info = FindingInfo(uid="complex-data-finding", supporting_data=supporting_data)

        self.assertEqual(finding_info.supporting_data, supporting_data)
        self.assertEqual(finding_info.supporting_data["scanner_info"]["name"], "VulnScan Pro")
        self.assertEqual(finding_info.supporting_data["metrics"]["confidence_score"], 98)
        self.assertEqual(len(finding_info.supporting_data["detection_rules"]), 2)

    def test_finding_info_related_events(self):
        """Test FindingInfo with related events."""
        related_events = [
            {
                "event_id": "evt-001",
                "type": "network_connection",
                "timestamp": "2024-01-01T12:00:00Z",
                "source_ip": "192.168.1.100",
            },
            {
                "event_id": "evt-002",
                "type": "file_modification",
                "timestamp": "2024-01-01T12:05:00Z",
                "file_path": "/etc/passwd",
            },
            {
                "event_id": "evt-003",
                "type": "process_execution",
                "timestamp": "2024-01-01T12:10:00Z",
                "command": "nc -l -p 4444",
            },
        ]

        finding_info = FindingInfo(
            uid="event-related-finding", related_events=related_events, title="Suspicious Activity Chain"
        )

        self.assertEqual(len(finding_info.related_events), 3)
        self.assertEqual(finding_info.related_events[0]["event_id"], "evt-001")
        self.assertEqual(finding_info.related_events[1]["type"], "file_modification")
        self.assertEqual(finding_info.related_events[2]["command"], "nc -l -p 4444")

    def test_finding_info_remediation(self):
        """Test FindingInfo with detailed remediation information."""
        remediation_text = """
        To remediate this vulnerability:
        1. Update the affected package to version 2.1.5 or higher
        2. Restart the affected services
        3. Verify the fix by running the security scan again
        4. Monitor for any unusual activity

        Additional resources:
        - Security advisory: https://example.com/advisory/123
        - Patch documentation: https://example.com/docs/patch-guide
        """

        finding_info = FindingInfo(
            uid="remediation-finding", remediation=remediation_text.strip(), title="Package Vulnerability Remediation"
        )

        self.assertIsNotNone(finding_info.remediation)
        self.assertIn("Update the affected package", finding_info.remediation)
        self.assertIn("version 2.1.5", finding_info.remediation)
        self.assertIn("https://example.com/advisory/123", finding_info.remediation)

    def test_finding_info_url_handling(self):
        """Test FindingInfo with source URL."""
        test_urls = [
            "https://security.example.com/findings/123",
            "https://dashboard.security-platform.com/vuln/456",
            "https://internal.corp.com/security/findings?id=789",
        ]

        for url in test_urls:
            finding_info = FindingInfo(uid=f"url-test-{hash(url)}", src_url=url)
            self.assertEqual(finding_info.src_url, url)

    def test_finding_info_uid_formats(self):
        """Test FindingInfo with various UID formats."""
        uid_formats = [
            "finding-123",
            "vuln-2024-001",
            "COMPLIANCE-VIOLATION-456",
            "sec_finding_789",
            "f1nd1ng-w1th-numb3rs-123",
        ]

        for uid in uid_formats:
            finding_info = FindingInfo(uid=uid)
            self.assertEqual(finding_info.uid, uid)

    def test_finding_info_comprehensive_example(self):
        """Test a comprehensive FindingInfo example with realistic data."""
        finding_info = FindingInfo(
            uid="VULN-2024-001-CRITICAL",
            created_time=datetime(2024, 1, 15, 14, 30, 0),
            first_seen_time=datetime(2024, 1, 15, 14, 30, 0),
            last_seen_time=datetime(2024, 1, 15, 16, 45, 0),
            modified_time=datetime(2024, 1, 15, 15, 15, 0),
            data_sources=["nessus_scanner", "qualys_vmdr", "rapid7_nexpose"],
            desc="Critical remote code execution vulnerability in Apache Struts framework",
            product_uid="security-platform-v2.1",
            title="Apache Struts RCE Vulnerability - CVE-2023-50164",
            types=["vulnerability", "rce", "web_application"],
            src_url="https://security-platform.company.com/findings/VULN-2024-001-CRITICAL",
            remediation="Upgrade Apache Struts to version 2.5.33 or 6.3.0 immediately",
            supporting_data={
                "cvss_score": 9.8,
                "exploit_available": True,
                "affected_systems": 15,
                "business_impact": "High",
            },
            related_events=[
                {"type": "vulnerability_scan", "scanner": "nessus"},
                {"type": "threat_intel_match", "source": "mitre_cve"},
            ],
        )

        # Verify all components
        self.assertEqual(finding_info.uid, "VULN-2024-001-CRITICAL")
        self.assertEqual(finding_info.title, "Apache Struts RCE Vulnerability - CVE-2023-50164")
        self.assertEqual(len(finding_info.data_sources), 3)
        self.assertEqual(len(finding_info.types), 3)
        self.assertEqual(finding_info.supporting_data["cvss_score"], 9.8)
        self.assertTrue(finding_info.supporting_data["exploit_available"])
        self.assertEqual(len(finding_info.related_events), 2)
