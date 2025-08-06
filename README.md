# FastAPI Auth0 Login with DynamoDB Integration

This project is a secure FastAPI web application that implements authentication using Auth0 (including Google SSO), and stores user profile data in AWS DynamoDB. It is designed as a minimal, cloud-native example for building authenticated APIs that are ready for extension with activity tracking or analytics.

## Features

- Auth0 login support (including Google and other identity providers)
- User sessions with secure cookies
- User profile retrieved from Auth0's `/userinfo` endpoint
- First-time login profiles saved in DynamoDB
- Fully asynchronous FastAPI backend
- Easy to extend with additional features like user activity logging or analytics

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/your-username/fastapi-auth0-dynamodb.git
cd fastapi-auth0-dynamodb
```

### 2. Create a `.env` file

```env
AUTH0_CLIENT_ID=your_client_id
AUTH0_CLIENT_SECRET=your_client_secret
AUTH0_DOMAIN=your-auth0-domain.auth0.com
AUTH0_CALLBACK_URL=http://localhost:8000/callback
```

> Do not commit this file. Always use `.gitignore` to keep it private.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
uvicorn main:app --reload
```

Go to [http://localhost:8000/login](http://localhost:8000/login) in your browser.

## AWS DynamoDB Setup

1. Go to the AWS Console and open DynamoDB.
2. Create a new table named `users`.
3. Set the partition key to `sub` (String).
4. Make sure your AWS credentials are configured via `aws configure`.

## Project Stack

| Layer       | Technology          |
|-------------|----------------------|
| Backend     | FastAPI (Python)     |
| Auth        | Auth0 (OIDC, Google) |
| Database    | AWS DynamoDB         |
| Sessions    | Starlette middleware |
| HTTP client | Authlib + HTTPX      |

## Potential Extensions

- Track user actions (page visits, button clicks)
- Add MongoDB for content or config storage
- Export login activity to Snowflake
- Build a frontend dashboard with user data

## License

This project is intended for demonstration, interview, and educational purposes.
