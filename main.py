import os
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
from authlib.integrations.starlette_client import OAuth
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError

# Load environment variables from .env
load_dotenv()

# FastAPI app
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="a-very-secret-key")

# Auth0 credentials
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL")

# OAuth setup
oauth = OAuth()
oauth.register(
    name='auth0',
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    server_metadata_url=f'https://{AUTH0_DOMAIN}/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid profile email',
    },
)

# DynamoDB setup
AWS_REGION = os.getenv("AWS_REGION")
dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
users_table = dynamodb.Table('users')

def save_user_to_dynamodb(userinfo: dict):
    print("👉 Connecting to DynamoDB...")

    try:
        print(f"🔍 Checking if user exists: {userinfo['sub']}")
        response = users_table.get_item(Key={'sub': userinfo['sub']})
        print("✅ get_item response received.")

        if 'Item' in response:
            print("✅ User already exists in DynamoDB.")
            return

        print("💾 Saving new user...")
        users_table.put_item(Item=userinfo)
        print("✅ User saved successfully.")

    except ClientError as e:
        print("❌ DynamoDB error:", e.response['Error']['Message'])


@app.get("/")
def home():
    return {"message": "Welcome! Go to /login to authenticate."}

@app.get("/login")
async def login(request: Request):
    return await oauth.auth0.authorize_redirect(request, AUTH0_CALLBACK_URL)

@app.get("/callback")
async def callback(request: Request):
    try:
        token = await oauth.auth0.authorize_access_token(request)

        # Get user info from Auth0
        resp = await oauth.auth0.get(
            f"https://{AUTH0_DOMAIN}/userinfo",
            token=token
        )
        userinfo = resp.json()

        # Save to DynamoDB
        save_user_to_dynamodb(userinfo)

        # Store in session
        request.session['user'] = dict(userinfo)
        return JSONResponse(content=userinfo)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(
        f"https://{AUTH0_DOMAIN}/v2/logout?client_id={AUTH0_CLIENT_ID}&returnTo=http://localhost:8000"
    )
