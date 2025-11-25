"""
Unit tests for OCSF vulnerability objects module.

Tests vulnerability-related objects like CWE, CVSS, CVE, AffectedPackage, and Vulnerability.
"""

import unittest
from datetime import datetime

from horizon_core.reporting.models.ocsf.common import CVE, CVSS, CWE


class TestCWE(unittest.TestCase):
    """Test cases for CWE (Common Weakness Enumeration) object."""

    def test_cwe_creation_minimal(self):
        """Test creating a CWE with minimal required fields."""
        cwe = CWE(uid="CWE-787")

        self.assertEqual(cwe.uid, "CWE-787")
        self.assertIsNone(cwe.url)

    def test_cwe_creation_full(self):
        """Test creating a CWE with all fields populated."""
        cwe = CWE(uid="CWE-787", url="https://cwe.mitre.org/data/definitions/787.html")

        self.assertEqual(cwe.uid, "CWE-787")
        self.assertEqual(cwe.url, "https://cwe.mitre.org/data/definitions/787.html")

    def test_cwe_common_weaknesses(self):
        """Test creating CWE objects for common weaknesses."""
        test_cases = [
            "CWE-79",  # Cross-site Scripting
            "CWE-89",  # SQL Injection
            "CWE-787",  # Out-of-bounds Write
            "CWE-20",  # Improper Input Validation
        ]

        for cwe_id in test_cases:
            cwe = CWE(uid=cwe_id)
            self.assertEqual(cwe.uid, cwe_id)
            self.assertTrue(cwe.uid.startswith("CWE-"))


class TestCVSS(unittest.TestCase):
    """Test cases for CVSS (Common Vulnerability Scoring System) object."""

    def test_cvss_creation_minimal(self):
        """Test creating a CVSS with minimal required fields."""
        cvss = CVSS(version="3.1", base_score=7.5, vector_string="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N")

        self.assertEqual(cvss.version, "3.1")
        self.assertEqual(cvss.base_score, 7.5)
        self.assertEqual(cvss.vector_string, "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N")
        self.assertIsNone(cvss.overall_score)

    def test_cvss_creation_full(self):
        """Test creating a CVSS with all fields populated."""
        cvss = CVSS(
            version="3.1",
            base_score=7.5,
            vector_string="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N",
            overall_score=8.2,
        )

        self.assertEqual(cvss.version, "3.1")
        self.assertEqual(cvss.base_score, 7.5)
        self.assertEqual(cvss.vector_string, "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N")
        self.assertEqual(cvss.overall_score, 8.2)

    def test_cvss_score_ranges(self):
        """Test CVSS score validation and ranges."""
        # Test various score ranges
        test_scores = [0.0, 3.9, 6.9, 8.9, 10.0]

        for score in test_scores:
            cvss = CVSS(version="3.1", base_score=score, vector_string="CVSS:3.1/AV:L/AC:H/PR:H/UI:R/S:U/C:L/I:L/A:L")
            self.assertEqual(cvss.base_score, score)
            self.assertTrue(0.0 <= cvss.base_score <= 10.0)

    def test_cvss_versions(self):
        """Test different CVSS versions."""
        versions = ["2.0", "3.0", "3.1", "4.0"]

        for version in versions:
            cvss = CVSS(
                version=version, base_score=5.0, vector_string=f"CVSS:{version}/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N"
            )
            self.assertEqual(cvss.version, version)


class TestCVE(unittest.TestCase):
    """Test cases for CVE (Common Vulnerabilities and Exposures) object."""

    def test_cve_creation_minimal(self):
        """Test creating a CVE with minimal required fields."""
        cve = CVE(uid="CVE-2021-44228")

        self.assertEqual(cve.uid, "CVE-2021-44228")
        self.assertIsNone(cve.created_time)
        self.assertIsNone(cve.cvss)
        self.assertIsNone(cve.cwe)

    def test_cve_creation_full(self):
        """Test creating a CVE with all fields populated."""
        created_time = datetime(2021, 12, 9, 0, 0, 0)
        modified_time = datetime(2021, 12, 10, 0, 0, 0)

        cvss = CVSS(version="3.1", base_score=10.0, vector_string="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H")

        cwe = CWE(uid="CWE-502")

        cve = CVE(
            uid="CVE-2021-44228",
            created_time=created_time,
            cvss=cvss,
            cwe=cwe,
            modified_time=modified_time,
            product="Apache Log4j",
            type="Remote Code Execution",
        )

        self.assertEqual(cve.uid, "CVE-2021-44228")
        self.assertEqual(cve.created_time, created_time)
        self.assertEqual(cve.cvss, cvss)
        self.assertEqual(cve.cwe, cwe)
        self.assertEqual(cve.modified_time, modified_time)
        self.assertEqual(cve.product, "Apache Log4j")
        self.assertEqual(cve.type, "Remote Code Execution")

    def test_cve_with_relationships(self):
        """Test CVE with associated CVSS and CWE objects."""
        cvss = CVSS(version="3.1", base_score=9.8, vector_string="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H")

        cwe = CWE(uid="CWE-78", url="https://cwe.mitre.org/data/definitions/78.html")

        cve = CVE(uid="CVE-2023-12345", cvss=cvss, cwe=cwe)

        self.assertEqual(cve.cvss.base_score, 9.8)
        self.assertEqual(cve.cwe.uid, "CWE-78")
        self.assertEqual(cve.cvss.version, "3.1")

    def test_cve_id_format(self):
        """Test CVE ID format validation."""
        valid_cve_ids = ["CVE-2021-44228", "CVE-2023-0001", "CVE-1999-0001", "CVE-2024-99999"]

        for cve_id in valid_cve_ids:
            cve = CVE(uid=cve_id)
            self.assertEqual(cve.uid, cve_id)
            self.assertTrue(cve.uid.startswith("CVE-"))
