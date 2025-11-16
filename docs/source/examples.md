# Examples

This section provides practical examples of using Horizon Core's components including secure logging, CLI framework functionality, and OCSF models for security event reporting.

## OCSF Models

### Basic Vulnerability Finding

```python
from horizon_core.reporting.models.ocsf import (
    VulnerabilityFinding,
    Vulnerability,
    CVE,
    CVSS,
    Severity,
    SeverityID,
    Status,
    StatusID,
    Metadata
)
from dataclasses import asdict
from datetime import datetime

# Create a basic vulnerability finding
finding = VulnerabilityFinding(
    metadata=Metadata(
        version="1.3.0",
        product={"name": "HorizonSec Scanner", "version": "2.0.0"}
    ),
    time=datetime.now(),
    severity_id=SeverityID.HIGH,
    severity=Severity.HIGH,
    status_id=StatusID.NEW,
    status=Status.NEW,
    vulnerabilities=[
        Vulnerability(
            title="SQL Injection in User Login",
            desc="User input is not properly sanitized in the login form",
            cve=CVE(uid="CVE-2024-12345"),
            cvss=CVSS(
                version="3.1",
                base_score=9.8,
                vector_string="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H"
            )
        )
    ]
)

# Convert to dictionary for JSON serialization
finding_dict = asdict(finding)
print(f"Vulnerability finding: {finding_dict}")
```

### Compliance Finding

```python
from horizon_core.reporting.models.ocsf import (
    ComplianceFinding,
    FindingInfo,
    ActivityID,
    Metadata
)
from dataclasses import asdict
from datetime import datetime

# Create a compliance finding
compliance_finding = ComplianceFinding(
    metadata=Metadata(version="1.3.0"),
    time=datetime.now(),
    activity_id=ActivityID.CREATE,
    finding_info=FindingInfo(
        title="PCI DSS Compliance Violation",
        desc="Credit card data stored in plain text without encryption",
        uid="COMP-2024-001"
    ),
    compliance={
        "requirements": ["PCI DSS 3.2.1 Requirement 3.4"],
        "controls": ["Data Protection"],
        "status": "Non-Compliant"
    }
)

print(f"Compliance finding: {asdict(compliance_finding)}")
```

### Detection Finding

```python
from horizon_core.reporting.models.ocsf import (
    DetectionFinding,
    FindingInfo,
    ActivityID,
    Metadata,
    File,
    User
)
from dataclasses import asdict
from datetime import datetime

# Create a detection finding
detection_finding = DetectionFinding(
    metadata=Metadata(version="1.3.0"),
    time=datetime.now(),
    activity_id=ActivityID.CREATE,
    finding_info=FindingInfo(
        title="Malicious File Detected",
        desc="Suspicious executable detected in user directory"
    ),
    resources=[
        File(
            name="malicious.exe",
            path="/home/user/downloads/malicious.exe",
            size=1024000,
            hashes={
                "MD5": "5d41402abc4b2a76b9719d911017c592",
                "SHA256": "e3b0c44298fc1c149afbf4c8996fb924"
            }
        )
    ],
    actor=User(
        name="suspicious_user",
        uid="1001"
    )
)

print(f"Detection finding: {asdict(detection_finding)}")
```

### Complex Vulnerability with Affected Packages

```python
from horizon_core.reporting.models.ocsf import (
    VulnerabilityFinding,
    Vulnerability,
    AffectedPackage,
    CVE,
    CVSS,
    CWE,
    Metadata
)
from dataclasses import asdict
from datetime import datetime

# Create a complex vulnerability finding with affected packages
complex_finding = VulnerabilityFinding(
    metadata=Metadata(version="1.3.0"),
    time=datetime.now(),
    vulnerabilities=[
        Vulnerability(
            title="Remote Code Execution in OpenSSL",
            desc="Buffer overflow vulnerability allows remote code execution",
            cve=CVE(
                uid="CVE-2024-67890",
                cvss=CVSS(
                    version="3.1",
                    base_score=9.8,
                    vector_string="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H"
                )
            ),
            cwe=CWE(
                uid="CWE-120",
                caption="Buffer Copy without Checking Size of Input ('Classic Buffer Overflow')"
            ),
            affected_packages=[
                AffectedPackage(
                    name="openssl",
                    version="1.1.1k",
                    architecture="x86_64",
                    package_manager="apt"
                ),
                AffectedPackage(
                    name="libssl1.1",
                    version="1.1.1k-1ubuntu1.2",
                    architecture="x86_64",
                    package_manager="apt"
                )
            ]
        )
    ]
)

print(f"Complex vulnerability: {asdict(complex_finding)}")
```

### Real-World Security Scanner Integration

```python
from horizon_core.reporting.models.ocsf import (
    VulnerabilityFinding,
    Vulnerability,
    CVE,
    CVSS,
    Metadata,
    SeverityID,
    StatusID
)
from dataclasses import asdict
from datetime import datetime
import json

class SecurityScanner:
    """Example security scanner using OCSF models."""
    
    def __init__(self, scanner_name: str, version: str):
        self.scanner_name = scanner_name
        self.version = version
    
    def create_vulnerability_report(self, scan_results: dict) -> VulnerabilityFinding:
        """Convert scan results to OCSF vulnerability finding."""
        
        vulnerabilities = []
        for vuln_data in scan_results.get('vulnerabilities', []):
            vulnerability = Vulnerability(
                title=vuln_data['title'],
                desc=vuln_data['description'],
                cve=CVE(uid=vuln_data['cve_id']) if vuln_data.get('cve_id') else None,
                cvss=CVSS(
                    version=vuln_data['cvss']['version'],
                    base_score=vuln_data['cvss']['score'],
                    vector_string=vuln_data['cvss']['vector']
                ) if vuln_data.get('cvss') else None
            )
            vulnerabilities.append(vulnerability)
        
        finding = VulnerabilityFinding(
            metadata=Metadata(
                version="1.3.0",
                product={
                    "name": self.scanner_name,
                    "version": self.version
                }
            ),
            time=datetime.now(),
            severity_id=SeverityID(scan_results.get('severity_id', 1)),
            status_id=StatusID.NEW,
            vulnerabilities=vulnerabilities
        )
        
        return finding
    
    def export_findings(self, findings: list, filename: str):
        """Export findings to JSON file."""
        findings_data = [asdict(finding) for finding in findings]
        
        with open(filename, 'w') as f:
            json.dump(findings_data, f, indent=2, default=str)
        
        print(f"Exported {len(findings)} findings to {filename}")

# Usage example
scanner = SecurityScanner("HorizonSec Scanner", "2.0.0")

# Example scan results
scan_data = {
    "severity_id": 4,  # High severity
    "vulnerabilities": [
        {
            "title": "Cross-Site Scripting (XSS)",
            "description": "Reflected XSS vulnerability in search parameter",
            "cve_id": "CVE-2024-11111",
            "cvss": {
                "version": "3.1",
                "score": 6.1,
                "vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N"
            }
        }
    ]
}

# Create and export findings
finding = scanner.create_vulnerability_report(scan_data)
scanner.export_findings([finding], "security_report.json")
```

## Secure Logging

### Basic Usage

#### Simple Logging Setup

```python
from horizon_core import setup_logger
import logging

# Create a basic secure logger
logger = setup_logger("myapp")
logger.info("Application started")
```

#### Custom Log Level

```python
from horizon_core import setup_logger
import logging

# Create a logger with debug level
logger = setup_logger("myapp", level=logging.DEBUG)
logger.debug("Debug information")
logger.info("Information message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")
```

### Sensitive Data Redaction

#### Password Redaction

```python
logger = setup_logger("auth")

# These will be automatically redacted
logger.info("User password is mySecret123")      # → "User password is [REDACTED]"
logger.info("Database password=dbPass456")       # → "Database password=[REDACTED]"
logger.info("Login pwd: userPwd789")             # → "Login pwd: [REDACTED]"
```

#### API Key Redaction

```python
logger = setup_logger("api")

# API keys are automatically detected and redacted
logger.info("API key: sk-abc123def456ghi789")    # → "API key: [REDACTED]"
logger.info("Using apikey=your_key_here")        # → "Using apikey=[REDACTED]"
logger.info("API_KEY is set to mykey123")        # → "API_KEY is set to [REDACTED]"
```

### Token Redaction

```python
logger = setup_logger("security")

# Various token formats are supported
logger.info("JWT token: eyJhbGciOiJIUzI1NiIs...")     # → "JWT token: [REDACTED]"
logger.info("Bearer token=abc123xyz789")              # → "Bearer token=[REDACTED]"  
logger.info("OAuth token is valid_token_123")         # → "OAuth token is [REDACTED]"
```

## Advanced Usage

### Simple Format Mode

For high-performance scenarios where redaction isn't needed:

```python
# Simple format without redaction (faster)
simple_logger = setup_logger("console", simple=True)
simple_logger.info("Quick message")  # Output: "INFO: Quick message"
```

### Custom Logger Configuration

```python
from horizon_core.logger import SecureLogger, SensitiveDataFormatter
import logging

# Create a custom secure logger
logger = SecureLogger("custom-app")
logger.setLevel(logging.INFO)

# Add custom handler with file output
handler = logging.FileHandler("app.log")
formatter = SensitiveDataFormatter("%(asctime)s [%(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info("Custom configured logger with file output")
```

### Error-Safe Logging

The SecureLogger handles various error conditions gracefully:

```python
logger = setup_logger("robust")

# These won't crash your application
logger.info("Missing argument: %s")           # Graceful handling
logger.info(None)                             # Converts to string
logger.info({"key": "value"})                 # Converts objects to string
logger.info("Too many %s %s", "one")         # Handles mismatched args
```

## Real-World Scenarios

### Web Application Logging

```python
from horizon_core import setup_logger
import logging

# Set up logger for a web application
app_logger = setup_logger("webapp", level=logging.INFO)

def authenticate_user(username, password):
    app_logger.info(f"Authentication attempt for user: {username}")
    
    # This password will be automatically redacted
    app_logger.debug(f"User {username} password is {password}")
    
    if verify_credentials(username, password):
        app_logger.info(f"User {username} authenticated successfully")
        return True
    else:
        app_logger.warning(f"Authentication failed for user: {username}")
        return False

def api_request(api_key, endpoint):
    # API key will be automatically redacted
    app_logger.info(f"API request to {endpoint} with key: {api_key}")
    
    try:
        response = make_request(endpoint, api_key)
        app_logger.info(f"API request successful: {response.status_code}")
        return response
    except Exception as e:
        app_logger.error(f"API request failed: {str(e)}")
        raise
```

### Microservice Logging

```python
from horizon_core import setup_logger
import logging

# Set up structured logging for microservices
service_logger = setup_logger("user-service", level=logging.INFO)

class UserService:
    def __init__(self):
        self.logger = service_logger
    
    def create_user(self, user_data):
        self.logger.info(f"Creating user: {user_data.get('username')}")
        
        # Sensitive data in user_data will be redacted if logged
        self.logger.debug(f"User data: {user_data}")
        
        try:
            user_id = self.save_user(user_data)
            self.logger.info(f"User created successfully with ID: {user_id}")
            return user_id
        except Exception as e:
            self.logger.error(f"Failed to create user: {str(e)}")
            raise
    
    def authenticate(self, username, password):
        self.logger.info(f"Authenticating user: {username}")
        
        # Password will be automatically redacted
        self.logger.debug(f"Auth attempt - username: {username}, password: {password}")
        
        return self.check_credentials(username, password)
```

## Integration with Existing Code

### Replacing Standard Logging

```python
# Before: Standard logging
import logging
logging.basicConfig(level=logging.INFO)  
logger = logging.getLogger(__name__)

# After: Secure logging (drop-in replacement)
from horizon_core import setup_logger
logger = setup_logger(__name__, level=logging.INFO)

# All existing logging calls work the same way
logger.info("Application started")
logger.error("Something went wrong")
```

### Flask Application Integration

```python
from flask import Flask
from horizon_core import setup_logger

app = Flask(__name__)

# Replace Flask's default logger with secure logger
app.logger = setup_logger("flask-app", level=logging.INFO)

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    
    # Password will be automatically redacted
    app.logger.info(f"Login attempt - user: {username}, password: {password}")
    
    if authenticate(username, password):
        app.logger.info(f"User {username} logged in successfully")
        return "Success"
    else:
        app.logger.warning(f"Failed login attempt for user: {username}")
        return "Failed"
```

## CLI Framework

### Basic CLI Application

```python
from horizon_core.cli_wrapper import CLI

# Create a basic CLI application
cli = CLI("MyTool", "A security analysis tool", "1.0.0")

# Add a simple command
@cli.add_command
def scan():
    """Run security scan."""
    print("Running security scan...")
    print("Scan completed!")

# Run the application
if __name__ == "__main__":
    cli.run()
```

### CLI with Custom ASCII Art

```python
from horizon_core.cli_wrapper import CLI

# Custom ASCII art for branding
ascii_art = """
 _____ _____ _____ _____ _____ 
|     |   __| __  |  |  |     |
| | | |   __|    -|  |  | | | |
|_|_|_|_____|__|__|_____|_|_|_|
"""

cli = CLI(
    app_name="MyTool",
    app_description="Advanced Security Scanner", 
    version="2.1.0",
    ascii_art=ascii_art
)

@cli.add_command
def analyze():
    """Analyze security vulnerabilities."""
    print("Starting vulnerability analysis...")
    
if __name__ == "__main__":
    cli.run()
```

### CLI with Command Groups

```python
from horizon_core.cli_wrapper import CLI
import typer

cli = CLI("SecuritySuite", "Comprehensive security testing tools", "1.0.0")

# Create command groups
scan_group = cli.add_group("scan", "Scanning operations")
report_group = cli.add_group("report", "Reporting operations")

# Add commands to scan group
@scan_group.command()
def network():
    """Scan network for vulnerabilities."""
    print("Scanning network...")

@scan_group.command()
def web():
    """Scan web applications."""
    print("Scanning web applications...")

# Add commands to report group  
@report_group.command()
def generate():
    """Generate security report."""
    print("Generating report...")

@report_group.command()
def export():
    """Export report to different formats."""
    print("Exporting report...")

if __name__ == "__main__":
    cli.run()
```

### Interactive CLI with Custom Commands

```python
from horizon_core.cli_wrapper import CLI
from rich import print as rprint

cli = CLI("InteractiveTool", "Tool with interactive features", "1.0.0")

# Register interactive commands
def run_scan():
    """Run a comprehensive security scan."""
    rprint("[bold green]Starting security scan...[/bold green]")
    rprint("[yellow]Scanning network interfaces...[/yellow]")
    rprint("[yellow]Checking for vulnerabilities...[/yellow]") 
    rprint("[green]Scan completed successfully![/green]")

def view_results():
    """View scan results."""
    rprint("[bold blue]Scan Results:[/bold blue]")
    rprint("• Found 3 medium severity issues")
    rprint("• Found 1 high severity issue")
    rprint("• System needs patching")

cli.register_interactive_command("scan", run_scan)
cli.register_interactive_command("results", view_results)

# Also add regular CLI commands
@cli.add_command
def quick_scan():
    """Run a quick security scan."""
    print("Running quick scan...")

if __name__ == "__main__":
    cli.run()
```

### Advanced CLI with Argument Parsing

```python
from horizon_core.cli_wrapper import CLI
import typer
from typing import Optional

cli = CLI("AdvancedTool", "Advanced security analysis tool", "1.0.0")

@cli.add_command
def scan_target(
    target: str = typer.Argument(..., help="Target to scan (IP, domain, or URL)"),
    port_range: Optional[str] = typer.Option("1-1000", "--ports", "-p", help="Port range to scan"),
    output_file: Optional[str] = typer.Option(None, "--output", "-o", help="Output file for results"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output")
):
    """Scan a specific target for security issues."""
    if verbose:
        print(f"Scanning target: {target}")
        print(f"Port range: {port_range}")
        if output_file:
            print(f"Output will be saved to: {output_file}")
    
    print(f"Starting scan of {target}...")
    # Scan logic here
    print("Scan completed!")

@cli.add_command  
def generate_report(
    input_file: str = typer.Argument(..., help="Input scan results file"),
    format: str = typer.Option("json", "--format", "-f", help="Report format (json, xml, html)"),
    severity: str = typer.Option("all", "--severity", "-s", help="Filter by severity level")
):
    """Generate a report from scan results."""
    print(f"Generating {format} report from {input_file}")
    print(f"Including {severity} severity findings")
    print("Report generated successfully!")

if __name__ == "__main__":
    cli.run()
```

### CLI Factory Function Usage

```python
from horizon_core.cli_wrapper import create_cli

# Use the factory function for quick CLI creation
cli = create_cli(
    app_name="QuickTool",
    app_description="Quickly created security tool",
    version="0.1.0"
)

@cli.add_command
def test():
    """Test command."""
    print("Test executed!")

if __name__ == "__main__":
    cli.run()
```

### Integration with Secure Logging

```python
from horizon_core.cli_wrapper import CLI
from horizon_core import setup_logger
import typer

# Create CLI with integrated logging
cli = CLI("SecureTool", "Tool with secure logging", "1.0.0")
logger = setup_logger("secure-tool")

@cli.add_command
def secure_operation(
    api_key: str = typer.Option(..., "--api-key", help="API key for authentication"),
    password: str = typer.Option(..., "--password", help="Password for operation")
):
    """Perform secure operation with automatic log redaction."""
    
    # These sensitive values will be automatically redacted in logs
    logger.info(f"Starting secure operation with API key: {api_key}")
    logger.info(f"Using password: {password}")
    
    try:
        # Operation logic here
        logger.info("Secure operation completed successfully")
        print("Operation completed!")
    except Exception as e:
        logger.error(f"Operation failed: {str(e)}")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    cli.run()
```