# Security Considerations

This section covers the security aspects of Horizon Core's logging system and best practices for secure logging.

## Threat Model

### Information Disclosure Risks

The primary security concern that Horizon Core addresses is **sensitive information disclosure** through log files. Common risks include:

- **Credential Leakage**: Passwords, API keys, and tokens appearing in plain text in logs
- **Personal Data Exposure**: Sensitive user information being logged inadvertently  
- **System Information Disclosure**: Internal system details that could aid attackers
- **Debugging Data Leaks**: Sensitive data accidentally logged during development/debugging

### Attack Scenarios

1. **Log File Access**: Attackers gaining access to log files and extracting sensitive data
2. **Log Aggregation**: Sensitive data being sent to centralized logging systems
3. **Developer Access**: Developers with log access seeing production sensitive data
4. **Backup Exposure**: Log backups containing sensitive information being compromised

## Security Features

### Automatic Redaction

Horizon Core automatically detects and redacts sensitive information patterns:

```python
logger.info("Database password is mySecret123")
# Output: "Database password is [REDACTED]"
```

**Supported Patterns:**
- `password`, `passwd`, `pwd`
- `secret`, `token`, `apikey`, `api_key`
- `auth`, `authorization`, `credential`
- `key`, `private`, `session`, `cookie`
- `jwt`, `bearer`, `oauth`

### Pattern Detection

The system uses regex patterns with word boundaries to ensure accurate detection:

- **"keyword is value"**: `password is secret123` → `password is [REDACTED]`
- **"keyword: value"**: `API key: abc123` → `API key: [REDACTED]`
- **"keyword=value"**: `token=xyz789` → `token=[REDACTED]`

### Case Insensitive Matching

All patterns work regardless of case:

```python
logger.info("PASSWORD is secret")    # → "PASSWORD is [REDACTED]"
logger.info("Api Key: secret")       # → "Api Key: [REDACTED]"
logger.info("TOKEN=secret")          # → "TOKEN=[REDACTED]"
```

## Best Practices

### 1. Always Use Secure Loggers

```python
# ✅ Good: Use secure logger
from horizon_core import setup_logger
logger = setup_logger("myapp")

# ❌ Bad: Use standard logger for sensitive applications  
import logging
logger = logging.getLogger("myapp")
```

### 2. Avoid Simple Mode for Sensitive Data

```python
# ✅ Good: Default mode with redaction
logger = setup_logger("app", level=logging.INFO)

# ⚠️ Caution: Simple mode disables redaction (use only for non-sensitive contexts)
console_logger = setup_logger("console", simple=True)
```

### 3. Review Log Output

Always review log output in development to ensure sensitive data is properly redacted:

```python
logger = setup_logger("test")
logger.info("User admin password is testpass123")
# Verify output shows: "User admin password is [REDACTED]"
```

### 4. Custom Sensitive Patterns

For application-specific sensitive data, consider extending the redaction patterns:

```python
# Current implementation handles common patterns
# For custom patterns, you may need to extend SensitiveDataFormatter
```

### 5. Log Level Considerations

Use appropriate log levels to minimize sensitive data exposure:

```python
# ✅ Good: Use DEBUG for detailed info (filtered out in production)
logger.debug(f"Processing user data: {user_data}")

# ⚠️ Caution: INFO level logs are typically kept in production
logger.info(f"Processing sensitive data: {sensitive_data}")
```

## Limitations and Considerations

### What Is NOT Redacted

The current implementation focuses on common patterns but may not catch:

1. **Base64 Encoded Data**: `password: YWRtaW4xMjM=` (base64 for "admin123")
2. **URL Encoded Data**: `password=admin%2B123`
3. **Custom Formats**: Application-specific sensitive data formats
4. **Numeric IDs**: Social security numbers, credit card numbers (unless containing keywords)
5. **Obfuscated Data**: Intentionally disguised sensitive information

### False Positives Prevention

The system uses word boundaries to prevent false positives:

```python
# ✅ These will NOT be redacted (no false positives)
logger.info("mypassword is value")      # "mypassword" != "password"
logger.info("password:")                # No value to redact
logger.info("password =")               # No value to redact
```

### Performance Considerations

- **Regex Processing**: Each log message is processed through multiple regex patterns
- **Simple Mode**: Use `simple=True` for high-frequency, non-sensitive logging
- **Format Complexity**: More complex patterns = higher processing overhead

## Deployment Security

### Production Environments

1. **Log Storage**: Ensure log files are stored securely with appropriate access controls
2. **Transmission**: Use encrypted channels when sending logs to remote systems
3. **Retention**: Implement appropriate log retention and deletion policies
4. **Access Control**: Limit access to log files to authorized personnel only

### Development Environments

1. **Separation**: Use separate logging configurations for development vs production
2. **Testing**: Regularly test that sensitive data redaction is working correctly
3. **Code Review**: Include log statements in security-focused code reviews

### Monitoring and Alerting

Consider implementing monitoring to detect:
- Unusual patterns in log output
- Potential sensitive data leaks
- Failed redaction attempts

## Compliance Considerations

### GDPR and Privacy Laws

- **Data Minimization**: Log only necessary information
- **Right to be Forgotten**: Implement log data deletion capabilities
- **Data Processing**: Consider logs as data processing under privacy regulations

### Industry Standards

- **PCI DSS**: Never log payment card data, even with redaction
- **HIPAA**: Be cautious with any health-related information in logs
- **SOX**: Maintain audit trails while protecting sensitive financial data

## Incident Response

### If Sensitive Data is Logged

1. **Immediate Action**: Stop the logging process if possible
2. **Assessment**: Determine what sensitive data was exposed
3. **Containment**: Secure or delete affected log files
4. **Notification**: Follow incident response procedures for data exposure
5. **Prevention**: Update logging practices to prevent recurrence

### Regular Security Reviews

1. **Log Audits**: Regularly review log output for sensitive data leaks
2. **Pattern Updates**: Update redaction patterns as new sensitive data types are identified
3. **Security Testing**: Include logging security in penetration testing and security assessments

## CLI Framework Security

### Command-Line Argument Security

When using the CLI framework, be aware of security considerations for command-line arguments:

#### Sensitive Arguments

```python
from horizon_core.cli_wrapper import CLI
import typer

cli = CLI("SecurityTool", "Security analysis tool", "1.0.0")

@cli.add_command
def connect(
    password: str = typer.Option(..., "--password", help="Database password"),
    api_key: str = typer.Option(..., "--api-key", help="API key for service")
):
    """Connect to service with credentials."""
    # These will be visible in process lists and shell history!
    logger.info(f"Connecting with password: {password}")  # Will be redacted in logs
    logger.info(f"Using API key: {api_key}")             # Will be redacted in logs
```

#### Security Best Practices for CLI

1. **Avoid Sensitive Arguments**: Don't pass secrets via command-line arguments
   ```bash
   # ❌ Bad: Visible in process list and shell history
   ./tool connect --password secret123 --api-key abc123
   ```

2. **Use Environment Variables**: 
   ```python
   import os
   
   @cli.add_command
   def connect():
       """Connect using environment variables."""
       password = os.getenv("DB_PASSWORD")
       api_key = os.getenv("API_KEY")
       
       if not password or not api_key:
           print("Error: Please set DB_PASSWORD and API_KEY environment variables")
           return
   ```

3. **Use Interactive Prompts**:
   ```python
   from rich.prompt import Prompt
   
   @cli.add_command
   def connect():
       """Connect with interactive password prompt."""
       password = Prompt.ask("Enter password", password=True)  # Hidden input
       api_key = Prompt.ask("Enter API key", password=True)
   ```

4. **Use Configuration Files**:
   ```python
   @cli.add_command
   def connect(config_file: str = typer.Option("config.yaml", "--config")):
       """Connect using configuration file."""
       # Load credentials from secure config file
       config = load_config(config_file)
       password = config.get("password")
       api_key = config.get("api_key")
   ```

### Interactive Mode Security

The interactive mode provides additional security benefits:

- **No Shell History**: Interactive selections don't appear in shell history
- **Guided Input**: Reduces risk of accidentally exposing sensitive data
- **Controlled Environment**: Better control over what information is displayed

### Process Security

When using CLI tools:

1. **Process Lists**: Command-line arguments are visible in process lists (`ps`, `top`, etc.)
2. **Shell History**: Commands are stored in shell history files (`.bash_history`, etc.)
3. **Log Files**: CLI frameworks may log command executions
4. **Memory Dumps**: Sensitive data in memory could be exposed in crash dumps

### Recommendations

1. **Use Environment Variables**: For secrets and sensitive configuration
2. **Interactive Prompts**: For password input and sensitive data entry
3. **Configuration Files**: Store sensitive data in properly secured config files
4. **Audit Logging**: Log CLI usage while ensuring sensitive data is redacted
5. **Process Monitoring**: Monitor for sensitive data exposure in process arguments