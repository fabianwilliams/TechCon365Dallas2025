"""
Simplified Graph API authentication for demo MCP server.
Uses client credentials or delegated auth with MSAL.
"""

import os
import json
from pathlib import Path
from typing import Optional, Dict, Any
from msal import ConfidentialClientApplication, PublicClientApplication
import logging

logger = logging.getLogger(__name__)

# Token cache location
CACHE_DIR = Path.home() / ".msgraph-mcp"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
TOKEN_CACHE_FILE = CACHE_DIR / "token_cache.json"


class GraphAuthManager:
    """Manage Graph API authentication for demo."""

    def __init__(
        self,
        tenant_id: str,
        client_id: str,
        client_secret: Optional[str] = None,
    ):
        self.tenant_id = tenant_id if tenant_id else "common"  # Default to common for multi-tenant
        self.client_id = client_id
        self.client_secret = client_secret
        self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"

        # Scopes for delegated permissions
        self.scopes = [
            "https://graph.microsoft.com/Mail.Read",
            "https://graph.microsoft.com/Calendars.ReadWrite",
            "https://graph.microsoft.com/User.Read",
        ]

        # Initialize MSAL app
        if client_secret:
            # Confidential client (app-only)
            self.app = ConfidentialClientApplication(
                client_id=client_id,
                client_credential=client_secret,
                authority=self.authority,
            )
        else:
            # Public client (delegated)
            cache = self._load_cache()
            self.app = PublicClientApplication(
                client_id=client_id,
                authority=self.authority,
                token_cache=cache,
            )

    def _load_cache(self):
        """Load token cache from file."""
        from msal import SerializableTokenCache

        cache = SerializableTokenCache()
        if TOKEN_CACHE_FILE.exists():
            try:
                with open(TOKEN_CACHE_FILE, "r") as f:
                    cache.deserialize(f.read())
            except Exception:
                pass  # Ignore cache errors
        return cache

    def _save_cache(self):
        """Save token cache to file."""
        if not hasattr(self.app, "token_cache"):
            return
        
        try:
            if hasattr(self.app.token_cache, "has_state_changed"):
                if self.app.token_cache.has_state_changed:
                    with open(TOKEN_CACHE_FILE, "w") as f:
                        f.write(self.app.token_cache.serialize())
            elif hasattr(self.app.token_cache, "serialize"):
                # Always save if we have serialize method
                with open(TOKEN_CACHE_FILE, "w") as f:
                    f.write(self.app.token_cache.serialize())
        except Exception:
            pass  # Ignore cache save errors

    def get_access_token(self) -> str:
        """Get valid access token."""
        # First, try to load from our simple cache file
        if TOKEN_CACHE_FILE.exists():
            try:
                with open(TOKEN_CACHE_FILE, "r") as f:
                    cache_data = json.load(f)
                    if "access_token" in cache_data:
                        # TODO: Check expiration, but for now just use it
                        return cache_data["access_token"]
            except Exception:
                pass
        
        # Try to get from MSAL cache
        accounts = self.app.get_accounts()
        if accounts:
            result = self.app.acquire_token_silent(self.scopes, account=accounts[0])
            if result and "access_token" in result:
                return result["access_token"]

        # If no client secret, need interactive auth
        if not self.client_secret:
            # Try device flow
            flow = self.app.initiate_device_flow(scopes=self.scopes)
            if "user_code" not in flow:
                raise Exception(
                    "Failed to create device flow. Check client ID and authority."
                )

            print(f"\nDevice code authentication required:")
            print(f"1. Open: {flow['verification_uri']}")
            print(f"2. Enter code: {flow['user_code']}")
            print(f"3. Press Enter after completing authentication...")
            input()

            result = self.app.acquire_token_by_device_flow(flow)
        else:
            # App-only flow with client secret
            result = self.app.acquire_token_for_client(
                scopes=["https://graph.microsoft.com/.default"]
            )

        if "access_token" in result:
            self._save_cache()
            return result["access_token"]
        else:
            error = result.get("error_description", result.get("error", "Unknown error"))
            raise Exception(f"Authentication failed: {error}")

    def ensure_authenticated(self) -> bool:
        """Check if we have valid authentication."""
        try:
            token = self.get_access_token()
            return bool(token)
        except Exception as e:
            logger.error(f"Authentication check failed: {e}")
            return False


def create_auth_manager_from_env() -> GraphAuthManager:
    """Create auth manager from environment variables."""
    tenant_id = os.getenv("TENANT_ID")
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    if not tenant_id or not client_id:
        raise ValueError(
            "Missing required environment variables: TENANT_ID and CLIENT_ID"
        )

    return GraphAuthManager(
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=client_secret,
    )
