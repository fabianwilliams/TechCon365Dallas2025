#!/usr/bin/env python3
"""
Interactive Graph API Authentication Setup
This script handles device code flow authentication and caches the token for MCP server use.
"""

import os
import json
from pathlib import Path
from msal import PublicClientApplication

# Configuration
# Using Microsoft Graph Command Line Tools (public app) for device code flow
# This app is multi-tenant and doesn't require app registration
TENANT_ID = "common"  # Allow any Microsoft tenant
CLIENT_ID = "14d82eec-204b-4c2f-b7e8-296a70dab67e"  # Microsoft Graph Command Line Tools (public app)
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"

# Token cache location (same as MCP server uses)
CACHE_DIR = Path.home() / ".msgraph-mcp"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
TOKEN_CACHE_FILE = CACHE_DIR / "token_cache.json"

# Scopes needed
SCOPES = [
    "https://graph.microsoft.com/Mail.Read",
    "https://graph.microsoft.com/Calendars.ReadWrite",
    "https://graph.microsoft.com/User.Read",
]


def load_cache():
    """Load existing token cache if available."""
    cache = {}
    if TOKEN_CACHE_FILE.exists():
        try:
            with open(TOKEN_CACHE_FILE, "r") as f:
                cache = json.load(f)
            print(f"✅ Found existing token cache at {TOKEN_CACHE_FILE}")
        except Exception as e:
            print(f"⚠️  Could not load cache: {e}")
    return cache


def save_cache(cache_data):
    """Save token cache to file."""
    try:
        with open(TOKEN_CACHE_FILE, "w") as f:
            json.dump(cache_data, f, indent=2)
        print(f"✅ Token cache saved to {TOKEN_CACHE_FILE}")
        # Make it readable only by user
        TOKEN_CACHE_FILE.chmod(0o600)
        return True
    except Exception as e:
        print(f"❌ Failed to save cache: {e}")
        return False


def authenticate():
    """Perform device code authentication flow."""
    print("\n" + "="*60)
    print("🔐 Microsoft Graph API Authentication")
    print("="*60)
    print(f"\nTenant ID: {TENANT_ID[:8]}...")
    print(f"Client ID: {CLIENT_ID[:8]}...")
    print(f"Cache Location: {TOKEN_CACHE_FILE}")
    print("\nScopes requested:")
    for scope in SCOPES:
        print(f"  - {scope}")
    
    # Create MSAL app
    app = PublicClientApplication(
        client_id=CLIENT_ID,
        authority=AUTHORITY,
    )
    
    # Check for existing accounts in cache
    accounts = app.get_accounts()
    if accounts:
        print(f"\n✅ Found {len(accounts)} cached account(s)")
        for i, account in enumerate(accounts, 1):
            print(f"   {i}. {account.get('username', 'Unknown')}")
        
        # Try silent token acquisition
        print("\n🔄 Attempting to refresh token silently...")
        result = app.acquire_token_silent(SCOPES, account=accounts[0])
        
        if result and "access_token" in result:
            print("✅ Token refreshed successfully!")
            save_cache_from_result(result)
            test_token(result["access_token"])
            return True
        else:
            print("⚠️  Silent refresh failed, need to re-authenticate")
    
    # Need interactive authentication
    print("\n" + "="*60)
    print("🔑 DEVICE CODE AUTHENTICATION REQUIRED")
    print("="*60)
    
    # Initiate device flow
    flow = app.initiate_device_flow(scopes=SCOPES)
    
    if "user_code" not in flow:
        print(f"❌ Failed to create device flow")
        print(f"Error: {flow.get('error_description', 'Unknown error')}")
        return False
    
    # Display instructions
    print("\n📱 Please complete authentication:")
    print("="*60)
    print(f"1. Open this URL in your browser:")
    print(f"   {flow['verification_uri']}")
    print(f"\n2. Enter this code:")
    print(f"   >>> {flow['user_code']} <<<")
    print(f"\n3. Sign in with your Microsoft account")
    print("="*60)
    
    input("\n⏸️  Press ENTER after you've completed authentication...")
    
    # Complete the flow
    print("\n🔄 Acquiring token...")
    result = app.acquire_token_by_device_flow(flow)
    
    if "access_token" in result:
        print("\n✅ Authentication successful!")
        save_cache_from_result(result)
        test_token(result["access_token"])
        return True
    else:
        print(f"\n❌ Authentication failed!")
        error = result.get("error_description", result.get("error", "Unknown error"))
        print(f"Error: {error}")
        return False


def save_cache_from_result(result):
    """Save authentication result to cache."""
    cache_data = {
        "access_token": result.get("access_token"),
        "token_type": result.get("token_type"),
        "expires_in": result.get("expires_in"),
        "scope": result.get("scope"),
        "refresh_token": result.get("refresh_token"),
        "id_token": result.get("id_token"),
    }
    save_cache(cache_data)


def test_token(access_token):
    """Test the token by making a simple Graph API call."""
    import requests
    
    print("\n🧪 Testing token with Graph API...")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    
    # Test 1: Get user profile
    try:
        response = requests.get(
            "https://graph.microsoft.com/v1.0/me",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            user = response.json()
            print(f"✅ User Profile: {user.get('displayName')} ({user.get('mail')})")
        else:
            print(f"⚠️  Profile request returned {response.status_code}")
    except Exception as e:
        print(f"⚠️  Profile test failed: {e}")
    
    # Test 2: Check email access
    try:
        response = requests.get(
            "https://graph.microsoft.com/v1.0/me/messages?$top=1",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            email_count = len(data.get("value", []))
            print(f"✅ Email Access: Working ({email_count} message retrieved)")
        else:
            print(f"⚠️  Email request returned {response.status_code}")
    except Exception as e:
        print(f"⚠️  Email test failed: {e}")
    
    # Test 3: Check calendar access
    try:
        response = requests.get(
            "https://graph.microsoft.com/v1.0/me/calendars",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            cal_count = len(data.get("value", []))
            print(f"✅ Calendar Access: Working ({cal_count} calendar(s) found)")
        else:
            print(f"⚠️  Calendar request returned {response.status_code}")
    except Exception as e:
        print(f"⚠️  Calendar test failed: {e}")


def main():
    """Main authentication flow."""
    print("\n🚀 Graph API Authentication Setup for MCP Server\n")
    
    success = authenticate()
    
    if success:
        print("\n" + "="*60)
        print("✅ AUTHENTICATION COMPLETE!")
        print("="*60)
        print(f"\nToken cached at: {TOKEN_CACHE_FILE}")
        print("\nYour MCP server can now use this token!")
        print("\nNext steps:")
        print("  1. Start your Graph MCP server")
        print("  2. The server will automatically use the cached token")
        print("  3. Token will auto-refresh as needed")
        print("\n" + "="*60)
        return 0
    else:
        print("\n" + "="*60)
        print("❌ AUTHENTICATION FAILED")
        print("="*60)
        print("\nPlease try again or check:")
        print("  - Your internet connection")
        print("  - The tenant/client IDs are correct")
        print("  - You have the necessary permissions for your Microsoft account")
        return 1


if __name__ == "__main__":
    exit(main())
