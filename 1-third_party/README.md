# Third-Party Integrations

LinkedIn API integration handler for professional network interactions

## linkedin.py
- **Purpose**: Secure LinkedIn API integration with enterprise-grade features
- **Key Functionality**:
  - OAuth 2.0 client credentials flow
  - Profile data retrieval with field projection
  - Automatic rate limit monitoring
  - Retry logic for transient errors (429, 5xx)

- **Authentication**:
  ```python
  api = LinkedInAPI(client_id="YOUR_CLIENT_ID", client_secret="YOUR_SECRET")
  api.authenticate()  # Returns access token
  ```

- **Rate Limiting**:
  - Monitors X-RateLimit-Remaining header
  - Raises exception when <5 requests remain
  - Built-in retry for 429 responses

- **Dependencies**:
  - requests>=2.26.0
  - urllib3>=1.26.0

- **Usage Example**:
  ```python
  from third_party.linkedin import LinkedInAPI

  # Initialize client
  linkedin = LinkedInAPI(
      client_id="your_client_id",
      client_secret="your_client_secret"
  )

  # Get profile data
  profile = linkedin.get_profile("~")  # ~ for current user
  print(f"Name: {profile['firstName']['localized']['en_US']} "
        f"{profile['lastName']['localized']['en_US']}")
  ```

## Security Practices
- Credentials handled via OAuth 2.0 client credentials flow
- Access tokens never persisted to disk
- All connections use HTTPS with TLS 1.2+
