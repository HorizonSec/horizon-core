"""
Unit tests for OCSF events module.

Tests the main OCSF event classes: VulnerabilityFinding, ComplianceFinding, and DetectionFinding.
"""

import unittest
from datetime import datetime

from horizon_core.reporting.models.ocsf.base_objects import Metadata
from horizon_core.reporting.models.ocsf.enums import ActivityID, SeverityID
from horizon_core.reporting.models.ocsf.events import (
    ComplianceFinding,
    DetectionFinding,
    VulnerabilityFinding,
)
from horizon_core.reporting.models.ocsf.finding_objects import FindingInfo
from horizon_core.reporting.models.ocsf.vulnerability_objects import (
    CVE,
    CVSS,
    CWE,
    AffectedPackage,
    Vulnerability,
)


class TestVulnerabilityFinding(unittest.TestCase):
    """Test cases for VulnerabilityFinding event class."""

    def test_vulnerability_finding_creation_minimal(self):
        """Test creating a VulnerabilityFinding with minimal required fields."""
        metadata = Metadata(version="1.3.0")
        finding_info = FindingInfo(uid="vuln-001")
        event_time = datetime(2024, 1, 1, 12, 0, 0)

        vuln_finding = VulnerabilityFinding(
            metadata=metadata,
            severity_id=SeverityID.HIGH,
            time=event_time,
            type_uid=200201,
            activity_id=ActivityID.CREATE,
            finding_info=finding_info,
            vulnerabilities=[],
        )

        self.assertEqual(vuln_finding.metadata, metadata)
        self.assertEqual(vuln_finding.severity_id, SeverityID.HIGH)
        self.assertEqual(vuln_finding.time, event_time)
        self.assertEqual(vuln_finding.type_uid, 200201)
        self.assertEqual(vuln_finding.activity_id, ActivityID.CREATE)
        self.assertEqual(vuln_finding.finding_info, finding_info)
        self.assertEqual(vuln_finding.vulnerabilities, [])

        # Test defaults
        self.assertEqual(vuln_finding.category_uid, 2)
        self.assertEqual(vuln_finding.class_uid, 2002)
        self.assertIsNone(vuln_finding.activity_name)
        self.assertEqual(vuln_finding.category_name, "Findings")
        self.assertEqual(vuln_finding.class_name, "Vulnerability Finding")

    def test_vulnerability_finding_creation_full(self):
        """Test creating a VulnerabilityFinding with all fields populated."""
        metadata = Metadata(version="1.3.0", product={"name": "Security Scanner", "version": "2.1.0"})

        finding_info = FindingInfo(
            uid="vuln-critical-001",
            title="Critical Buffer Overflow",
            desc="Buffer overflow vulnerability in network service",
        )

        # Create vulnerability objects
        cwe = CWE(uid="CWE-787")
        cvss = CVSS(version="3.1", base_score=9.8, vector_string="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H")
        cve = CVE(uid="CVE-2024-0001", cvss=cvss, cwe=cwe)

        affected_package = AffectedPackage(name="network-service", version="1.0.0")
        vulnerability = Vulnerability(cve=cve, cwe=cwe, affected_packages=[affected_package], severity="Critical")

        event_time = datetime(2024, 1, 15, 14, 30, 0)
        start_time = datetime(2024, 1, 15, 14, 25, 0)
        end_time = datetime(2024, 1, 15, 14, 35, 0)

        vuln_finding = VulnerabilityFinding(
            metadata=metadata,
            severity_id=SeverityID.CRITICAL,
            time=event_time,
            type_uid=200201,
            activity_id=ActivityID.CREATE,
            finding_info=finding_info,
            vulnerabilities=[vulnerability],
            activity_name="Create",
            count=1,
            duration=600000,  # 10 minutes in milliseconds
            end_time=end_time,
            message="Critical vulnerability detected in network service",
            start_time=start_time,
            comment="Requires immediate attention",
            confidence_score=95,
        )

        self.assertEqual(vuln_finding.metadata.product["name"], "Security Scanner")
        self.assertEqual(vuln_finding.severity_id, SeverityID.CRITICAL)
        self.assertEqual(vuln_finding.activity_name, "Create")
        self.assertEqual(vuln_finding.count, 1)
        self.assertEqual(vuln_finding.duration, 600000)
        self.assertEqual(vuln_finding.end_time, end_time)
        self.assertEqual(vuln_finding.message, "Critical vulnerability detected in network service")
        self.assertEqual(vuln_finding.start_time, start_time)
        self.assertEqual(vuln_finding.comment, "Requires immediate attention")
        self.assertEqual(vuln_finding.confidence_score, 95)
        self.assertEqual(len(vuln_finding.vulnerabilities), 1)
        self.assertEqual(vuln_finding.vulnerabilities[0].cve.uid, "CVE-2024-0001")

    def test_vulnerability_finding_with_multiple_vulnerabilities(self):
        """Test VulnerabilityFinding with multiple vulnerabilities."""
        metadata = Metadata(version="1.3.0")
        finding_info = FindingInfo(uid="multi-vuln-001")

        # Create multiple vulnerabilities
        vuln1 = Vulnerability(cve=CVE(uid="CVE-2024-0001"), severity="High")

        vuln2 = Vulnerability(cve=CVE(uid="CVE-2024-0002"), severity="Critical")

        vuln_finding = VulnerabilityFinding(
            metadata=metadata,
            severity_id=SeverityID.CRITICAL,
            time=datetime.now(),
            type_uid=200201,
            activity_id=ActivityID.CREATE,
            finding_info=finding_info,
            vulnerabilities=[vuln1, vuln2],
        )

        self.assertEqual(len(vuln_finding.vulnerabilities), 2)
        self.assertEqual(vuln_finding.vulnerabilities[0].cve.uid, "CVE-2024-0001")
        self.assertEqual(vuln_finding.vulnerabilities[1].cve.uid, "CVE-2024-0002")

    def test_vulnerability_finding_activity_types(self):
        """Test VulnerabilityFinding with different activity types."""
        metadata = Metadata(version="1.3.0")
        finding_info = FindingInfo(uid="activity-test")
        base_time = datetime(2024, 1, 1, 12, 0, 0)

        activities = [(ActivityID.CREATE, 200201), (ActivityID.UPDATE, 200202), (ActivityID.CLOSE, 200203)]

        for activity_id, type_uid in activities:
            vuln_finding = VulnerabilityFinding(
                metadata=metadata,
                severity_id=SeverityID.MEDIUM,
                time=base_time,
                type_uid=type_uid,
                activity_id=activity_id,
                finding_info=finding_info,
                vulnerabilities=[],
            )

            self.assertEqual(vuln_finding.activity_id, activity_id)
            self.assertEqual(vuln_finding.type_uid, type_uid)


class TestComplianceFinding(unittest.TestCase):
    """Test cases for ComplianceFinding event class."""

    def test_compliance_finding_creation_minimal(self):
        """Test creating a ComplianceFinding with minimal required fields."""
        metadata = Metadata(version="1.3.0")
        finding_info = FindingInfo(uid="compliance-001")
        event_time = datetime(2024, 1, 1, 12, 0, 0)

        compliance_finding = ComplianceFinding(
            metadata=metadata,
            severity_id=SeverityID.MEDIUM,
            time=event_time,
            type_uid=200301,
            activity_id=ActivityID.CREATE,
            finding_info=finding_info,
        )

        self.assertEqual(compliance_finding.metadata, metadata)
        self.assertEqual(compliance_finding.severity_id, SeverityID.MEDIUM)
        self.assertEqual(compliance_finding.time, event_time)
        self.assertEqual(compliance_finding.type_uid, 200301)
        self.assertEqual(compliance_finding.activity_id, ActivityID.CREATE)
        self.assertEqual(compliance_finding.finding_info, finding_info)

        # Test defaults specific to ComplianceFinding
        self.assertEqual(compliance_finding.category_uid, 2)
        self.assertEqual(compliance_finding.class_uid, 2003)
        self.assertEqual(compliance_finding.category_name, "Findings")
        self.assertEqual(compliance_finding.class_name, "Compliance Finding")

    def test_compliance_finding_creation_full(self):
        """Test creating a ComplianceFinding with all optional fields."""
        metadata = Metadata(version="1.3.0", product={"name": "Compliance Scanner", "vendor": "Security Corp"})

        finding_info = FindingInfo(
            uid="compliance-pci-001",
            title="PCI DSS Compliance Violation",
            desc="Unencrypted credit card data storage detected",
            types=["compliance", "pci_dss", "data_protection"],
        )

        compliance_finding = ComplianceFinding(
            metadata=metadata,
            severity_id=SeverityID.HIGH,
            time=datetime(2024, 1, 15, 10, 30, 0),
            type_uid=200301,
            activity_id=ActivityID.CREATE,
            finding_info=finding_info,
            activity_name="Create Compliance Finding",
            category_name="Findings",
            class_name="Compliance Finding",
        )

        self.assertEqual(compliance_finding.metadata.product["name"], "Compliance Scanner")
        self.assertEqual(compliance_finding.finding_info.title, "PCI DSS Compliance Violation")
        self.assertIn("pci_dss", compliance_finding.finding_info.types)
        self.assertEqual(compliance_finding.activity_name, "Create Compliance Finding")

    def test_compliance_finding_severity_levels(self):
        """Test ComplianceFinding with different severity levels."""
        metadata = Metadata(version="1.3.0")
        finding_info = FindingInfo(uid="severity-test")
        base_time = datetime.now()

        severities = [SeverityID.INFORMATIONAL, SeverityID.LOW, SeverityID.MEDIUM, SeverityID.HIGH, SeverityID.CRITICAL]

        for severity in severities:
            compliance_finding = ComplianceFinding(
                metadata=metadata,
                severity_id=severity,
                time=base_time,
                type_uid=200301,
                activity_id=ActivityID.CREATE,
                finding_info=finding_info,
            )

            self.assertEqual(compliance_finding.severity_id, severity)


class TestDetectionFinding(unittest.TestCase):
    """Test cases for DetectionFinding event class."""

    def test_detection_finding_creation_minimal(self):
        """Test creating a DetectionFinding with minimal required fields."""
        metadata = Metadata(version="1.3.0")
        finding_info = FindingInfo(uid="detection-001")
        event_time = datetime(2024, 1, 1, 12, 0, 0)

        detection_finding = DetectionFinding(
            metadata=metadata,
            severity_id=SeverityID.HIGH,
            time=event_time,
            type_uid=200401,
            activity_id=ActivityID.CREATE,
            finding_info=finding_info,
        )

        self.assertEqual(detection_finding.metadata, metadata)
        self.assertEqual(detection_finding.severity_id, SeverityID.HIGH)
        self.assertEqual(detection_finding.time, event_time)
        self.assertEqual(detection_finding.type_uid, 200401)
        self.assertEqual(detection_finding.activity_id, ActivityID.CREATE)
        self.assertEqual(detection_finding.finding_info, finding_info)

        # Test defaults specific to DetectionFinding
        self.assertEqual(detection_finding.category_uid, 2)
        self.assertEqual(detection_finding.class_uid, 2004)
        self.assertEqual(detection_finding.category_name, "Findings")
        self.assertEqual(detection_finding.class_name, "Detection Finding")

    def test_detection_finding_creation_full(self):
        """Test creating a DetectionFinding with all optional fields."""
        metadata = Metadata(
            version="1.3.0", product={"name": "EDR Agent", "version": "5.2.1"}, log_name="edr_detections.log"
        )

        finding_info = FindingInfo(
            uid="detection-malware-001",
            title="Malware Detection - Trojan.Generic",
            desc="Suspicious executable with malware characteristics detected",
            types=["malware", "trojan", "endpoint_detection"],
            remediation="Quarantine the file and perform full system scan",
        )

        detection_finding = DetectionFinding(
            metadata=metadata,
            severity_id=SeverityID.CRITICAL,
            time=datetime(2024, 1, 15, 16, 45, 30),
            type_uid=200401,
            activity_id=ActivityID.CREATE,
            finding_info=finding_info,
            activity_name="Malware Detection",
            category_name="Findings",
            class_name="Detection Finding",
        )

        self.assertEqual(detection_finding.metadata.product["name"], "EDR Agent")
        self.assertEqual(detection_finding.metadata.log_name, "edr_detections.log")
        self.assertEqual(detection_finding.finding_info.title, "Malware Detection - Trojan.Generic")
        self.assertIn("endpoint_detection", detection_finding.finding_info.types)
        self.assertEqual(detection_finding.activity_name, "Malware Detection")

    def test_detection_finding_types(self):
        """Test DetectionFinding with various detection types."""
        metadata = Metadata(version="1.3.0")
        base_time = datetime.now()

        detection_types = [
            ("malware-001", ["malware", "virus"]),
            ("intrusion-001", ["intrusion", "network_attack"]),
            ("anomaly-001", ["anomaly", "behavioral"]),
            ("threat-001", ["threat_hunting", "ioc_match"]),
        ]

        for uid, types in detection_types:
            finding_info = FindingInfo(uid=uid, types=types)

            detection_finding = DetectionFinding(
                metadata=metadata,
                severity_id=SeverityID.HIGH,
                time=base_time,
                type_uid=200401,
                activity_id=ActivityID.CREATE,
                finding_info=finding_info,
            )

            self.assertEqual(detection_finding.finding_info.uid, uid)
            self.assertEqual(detection_finding.finding_info.types, types)


class TestEventIntegration(unittest.TestCase):
    """Integration tests for OCSF event classes."""

    def test_finding_event_type_consistency(self):
        """Test that each finding type has consistent class UIDs."""
        metadata = Metadata(version="1.3.0")
        finding_info = FindingInfo(uid="consistency-test")
        event_time = datetime.now()

        # Test class UID consistency
        vuln_finding = VulnerabilityFinding(
            metadata=metadata,
            severity_id=SeverityID.MEDIUM,
            time=event_time,
            type_uid=200201,
            activity_id=ActivityID.CREATE,
            finding_info=finding_info,
            vulnerabilities=[],
        )

        compliance_finding = ComplianceFinding(
            metadata=metadata,
            severity_id=SeverityID.MEDIUM,
            time=event_time,
            type_uid=200301,
            activity_id=ActivityID.CREATE,
            finding_info=finding_info,
        )

        detection_finding = DetectionFinding(
            metadata=metadata,
            severity_id=SeverityID.MEDIUM,
            time=event_time,
            type_uid=200401,
            activity_id=ActivityID.CREATE,
            finding_info=finding_info,
        )

        self.assertEqual(vuln_finding.class_uid, 2002)
        self.assertEqual(compliance_finding.class_uid, 2003)
        self.assertEqual(detection_finding.class_uid, 2004)

        # All should have same category (Findings)
        self.assertEqual(vuln_finding.category_uid, 2)
        self.assertEqual(compliance_finding.category_uid, 2)
        self.assertEqual(detection_finding.category_uid, 2)

    def test_event_lifecycle(self):
        """Test complete lifecycle of a finding event."""
        metadata = Metadata(version="1.3.0")
        finding_info = FindingInfo(uid="lifecycle-001", created_time=datetime(2024, 1, 1, 12, 0, 0))

        # Create event
        create_event = VulnerabilityFinding(
            metadata=metadata,
            severity_id=SeverityID.HIGH,
            time=datetime(2024, 1, 1, 12, 0, 0),
            type_uid=200201,
            activity_id=ActivityID.CREATE,
            finding_info=finding_info,
            vulnerabilities=[],
        )

        # Update event
        update_event = VulnerabilityFinding(
            metadata=metadata,
            severity_id=SeverityID.MEDIUM,  # Severity reduced
            time=datetime(2024, 1, 1, 14, 0, 0),
            type_uid=200202,
            activity_id=ActivityID.UPDATE,
            finding_info=finding_info,
            vulnerabilities=[],
        )

        # Close event
        close_event = VulnerabilityFinding(
            metadata=metadata,
            severity_id=SeverityID.INFORMATIONAL,
            time=datetime(2024, 1, 1, 16, 0, 0),
            type_uid=200203,
            activity_id=ActivityID.CLOSE,
            finding_info=finding_info,
            vulnerabilities=[],
        )

        self.assertEqual(create_event.activity_id, ActivityID.CREATE)
        self.assertEqual(update_event.activity_id, ActivityID.UPDATE)
        self.assertEqual(close_event.activity_id, ActivityID.CLOSE)

        self.assertEqual(create_event.severity_id, SeverityID.HIGH)
        self.assertEqual(update_event.severity_id, SeverityID.MEDIUM)
        self.assertEqual(close_event.severity_id, SeverityID.INFORMATIONAL)

    def test_complex_vulnerability_finding(self):
        """Test a complex VulnerabilityFinding with all components."""
        metadata = Metadata(
            version="1.3.0",
            product={
                "name": "Enterprise Vulnerability Scanner",
                "version": "4.2.1",
                "vendor": "Security Solutions Inc.",
            },
        )

        finding_info = FindingInfo(
            uid="COMPLEX-VULN-2024-001",
            created_time=datetime(2024, 1, 15, 10, 0, 0),
            title="Critical Remote Code Execution in Web Server",
            desc="Buffer overflow vulnerability allows remote code execution",
            types=["vulnerability", "rce", "buffer_overflow"],
            data_sources=["nessus", "openvas", "threat_intel"],
            remediation="Update to version 2.4.8 or apply security patch immediately",
        )

        # Create comprehensive vulnerability
        cwe = CWE(uid="CWE-787", url="https://cwe.mitre.org/data/definitions/787.html")
        cvss = CVSS(
            version="3.1",
            base_score=9.8,
            vector_string="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
            overall_score=9.8,
        )
        cve = CVE(uid="CVE-2024-0001", cvss=cvss, cwe=cwe, created_time=datetime(2024, 1, 10, 0, 0, 0))

        affected_packages = [
            AffectedPackage(name="webserver", version="2.4.7", architecture="x86_64"),
            AffectedPackage(name="webserver-modules", version="2.4.7", architecture="x86_64"),
        ]

        vulnerability = Vulnerability(
            cve=cve,
            cwe=cwe,
            cvss=cvss,
            affected_packages=affected_packages,
            severity="Critical",
            fix_available=True,
            is_exploit_available=True,
            references=[
                "https://nvd.nist.gov/vuln/detail/CVE-2024-0001",
                "https://www.cisa.gov/known-exploited-vulnerabilities-catalog",
            ],
        )

        vuln_finding = VulnerabilityFinding(
            metadata=metadata,
            severity_id=SeverityID.CRITICAL,
            time=datetime(2024, 1, 15, 10, 0, 0),
            type_uid=200201,
            activity_id=ActivityID.CREATE,
            finding_info=finding_info,
            vulnerabilities=[vulnerability],
            message="Critical vulnerability requires immediate patching",
            comment="Exploits available in the wild",
        )

        # Verify complete structure
        self.assertEqual(vuln_finding.finding_info.uid, "COMPLEX-VULN-2024-001")
        self.assertEqual(vuln_finding.vulnerabilities[0].cve.uid, "CVE-2024-0001")
        self.assertEqual(vuln_finding.vulnerabilities[0].cvss.base_score, 9.8)
        self.assertEqual(len(vuln_finding.vulnerabilities[0].affected_packages), 2)
        self.assertTrue(vuln_finding.vulnerabilities[0].fix_available)
        self.assertEqual(vuln_finding.severity_id, SeverityID.CRITICAL)
        self.assertEqual(vuln_finding.message, "Critical vulnerability requires immediate patching")
