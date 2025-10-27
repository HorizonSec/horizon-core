# Examples

This section provides practical examples of using Horizon Core's secure logging functionality.

## Basic Usage

### Simple Logging Setup

```python
from horizon_core import setup_logger
import logging

# Create a basic secure logger
logger = setup_logger("myapp")
logger.info("Application started")
```

### Custom Log Level

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

## Sensitive Data Redaction

### Password Redaction

```python
logger = setup_logger("auth")

# These will be automatically redacted
logger.info("User password is mySecret123")      # → "User password is [REDACTED]"
logger.info("Database password=dbPass456")       # → "Database password=[REDACTED]"
logger.info("Login pwd: userPwd789")             # → "Login pwd: [REDACTED]"
```

### API Key Redaction

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
from horizon_core.logging import SecureLogger, SensitiveDataFormatter
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
        return "Failed", 401
```