#!/usr/bin/env python3
"""
MCP Server for Microsoft Graph API Integration.

This server provides tools to interact with Microsoft 365 via Graph API,
including email access and calendar management.
"""

from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime, timedelta
import json
import os
from pydantic import BaseModel, Field, ConfigDict
from mcp.server.fastmcp import FastMCP
import requests

from graph_auth import create_auth_manager_from_env

# Initialize the MCP server
mcp = FastMCP("msgraph_mcp")

# Constants
GRAPH_API_BASE = "https://graph.microsoft.com/v1.0"
CHARACTER_LIMIT = 25000

# Initialize auth manager
try:
    auth_manager = create_auth_manager_from_env()
except Exception as e:
    print(f"Warning: Could not initialize auth manager: {e}")
    print("Set TENANT_ID, CLIENT_ID, and optionally CLIENT_SECRET environment variables")
    auth_manager = None


# Enums
class ResponseFormat(str, Enum):
    """Output format for tool responses."""
    MARKDOWN = "markdown"
    JSON = "json"


# Pydantic Models
class ReadEmailsInput(BaseModel):
    """Input model for reading emails."""
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)

    limit: Optional[int] = Field(
        default=10,
        description="Number of emails to retrieve",
        ge=1,
        le=50
    )
    folder: Optional[str] = Field(
        default="inbox",
        description="Email folder to read from (e.g., 'inbox', 'sent')"
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format"
    )


class SearchEmailsInput(BaseModel):
    """Input model for searching emails."""
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)

    query: str = Field(
        ...,
        description="Search query (e.g., sender email, subject keywords, 'from:john@example.com')",
        min_length=1,
        max_length=200
    )
    limit: Optional[int] = Field(
        default=10,
        description="Maximum results to return",
        ge=1,
        le=50
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format"
    )


class CreateCalendarEventInput(BaseModel):
    """Input model for creating calendar events."""
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)

    subject: str = Field(
        ...,
        description="Event title/subject (e.g., 'Meeting with John', 'Conference Session 87')",
        min_length=1,
        max_length=255
    )
    start_datetime: str = Field(
        ...,
        description="Start date and time in ISO format (e.g., '2025-11-06T09:00:00') or natural format"
    )
    end_datetime: Optional[str] = Field(
        default=None,
        description="End date and time (optional, defaults to 1 hour after start)"
    )
    location: Optional[str] = Field(
        default=None,
        description="Event location (e.g., 'Room G7', 'Teams Meeting')",
        max_length=255
    )
    body: Optional[str] = Field(
        default=None,
        description="Event description/body text",
        max_length=2000
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format"
    )


class GetCalendarEventsInput(BaseModel):
    """Input model for getting calendar events."""
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)

    start_date: Optional[str] = Field(
        default=None,
        description="Start date filter (e.g., '2025-11-06', defaults to today)"
    )
    end_date: Optional[str] = Field(
        default=None,
        description="End date filter (optional, defaults to 7 days from start)"
    )
    limit: Optional[int] = Field(
        default=20,
        description="Maximum events to return",
        ge=1,
        le=100
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format"
    )


# Helper functions
def _get_headers() -> Dict[str, str]:
    """Get headers with auth token."""
    if not auth_manager:
        raise Exception("Auth manager not initialized. Check environment variables.")

    token = auth_manager.get_access_token()
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


def _handle_api_error(e: Exception) -> str:
    """Consistent error formatting."""
    if isinstance(e, requests.HTTPError):
        status = e.response.status_code
        if status == 401:
            return "Error: Authentication failed. Token may be expired. Please re-authenticate."
        elif status == 403:
            return "Error: Permission denied. Check that required Graph API permissions are granted."
        elif status == 404:
            return "Error: Resource not found. Please verify the request."
        elif status == 429:
            return "Error: Rate limit exceeded. Please wait before making more requests."
        return f"Error: API request failed with status {status}"
    return f"Error: {type(e).__name__} - {str(e)}"


def _format_email_markdown(email: Dict[str, Any]) -> str:
    """Format a single email as markdown."""
    lines = []
    lines.append(f"### {email.get('subject', '(No subject)')}")
    lines.append("")

    sender = email.get("from", {}).get("emailAddress", {})
    lines.append(f"**From**: {sender.get('name', 'Unknown')} <{sender.get('address', 'unknown')}>")

    received = email.get("receivedDateTime", "")
    if received:
        lines.append(f"**Received**: {received}")

    if email.get("hasAttachments"):
        lines.append(f"**Attachments**: Yes")

    # Preview of body
    body_preview = email.get("bodyPreview", "")
    if body_preview:
        preview = body_preview[:200] + "..." if len(body_preview) > 200 else body_preview
        lines.append(f"\n{preview}")

    lines.append("")
    return "\n".join(lines)


def _format_event_markdown(event: Dict[str, Any]) -> str:
    """Format a calendar event as markdown."""
    lines = []
    lines.append(f"### {event.get('subject', '(No subject)')}")
    lines.append("")

    start = event.get("start", {}).get("dateTime", "")
    end = event.get("end", {}).get("dateTime", "")
    if start:
        lines.append(f"**Start**: {start}")
    if end:
        lines.append(f"**End**: {end}")

    location = event.get("location", {}).get("displayName")
    if location:
        lines.append(f"**Location**: {location}")

    organizer = event.get("organizer", {}).get("emailAddress", {})
    if organizer:
        lines.append(f"**Organizer**: {organizer.get('name', 'Unknown')}")

    body = event.get("body", {}).get("content", "")
    if body:
        # Strip HTML tags for preview
        import re
        body_text = re.sub('<[^<]+?>', '', body)
        preview = body_text[:200] + "..." if len(body_text) > 200 else body_text
        lines.append(f"\n{preview}")

    lines.append("")
    return "\n".join(lines)


# Tool implementations
@mcp.tool(
    name="graph_read_emails",
    annotations={
        "title": "Read Recent Emails",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True
    }
)
async def graph_read_emails(params: ReadEmailsInput) -> str:
    """Read recent emails from Microsoft 365 mailbox.

    Retrieves the most recent emails from the specified folder, showing sender,
    subject, receive time, and a preview of the content.

    Args:
        params (ReadEmailsInput): Contains limit, folder, and response_format

    Returns:
        str: Formatted list of emails or error message

    Examples:
        - "Show me my recent emails"
        - "Get the last 20 emails from inbox"
        - "Show emails from sent folder"
    """
    try:
        headers = _get_headers()

        # Map folder names
        folder_map = {
            "inbox": "inbox",
            "sent": "sentitems",
            "drafts": "drafts",
            "deleted": "deleteditems",
        }
        folder_id = folder_map.get(params.folder.lower(), params.folder)

        url = f"{GRAPH_API_BASE}/me/mailFolders/{folder_id}/messages"
        url += f"?$top={params.limit}&$orderby=receivedDateTime desc"
        url += "&$select=subject,from,receivedDateTime,bodyPreview,hasAttachments"

        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        data = response.json()
        emails = data.get("value", [])

        if not emails:
            return f"No emails found in {params.folder}"

        if params.response_format == ResponseFormat.MARKDOWN:
            lines = [f"# Recent Emails from {params.folder.capitalize()}", ""]
            lines.append(f"Found {len(emails)} emails\n")
            for email in emails:
                lines.append(_format_email_markdown(email))
            return "\n".join(lines)
        else:
            return json.dumps({"folder": params.folder, "count": len(emails), "emails": emails}, indent=2)

    except Exception as e:
        return _handle_api_error(e)


@mcp.tool(
    name="graph_search_emails",
    annotations={
        "title": "Search Emails",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True
    }
)
async def graph_search_emails(params: SearchEmailsInput) -> str:
    """Search emails by keyword, sender, or subject.

    Performs a search across email content to find matching messages.
    Supports searching by sender email, subject keywords, or body content.

    Args:
        params (SearchEmailsInput): Contains query, limit, and response_format

    Returns:
        str: Formatted search results or error message

    Examples:
        - "Search emails for 'TechCon'"
        - "Find emails from john@example.com"
        - "Search for emails about Session 87"
    """
    try:
        headers = _get_headers()

        # Use search endpoint
        url = f"{GRAPH_API_BASE}/me/messages"
        url += f"?$search=\"{params.query}\""
        url += f"&$top={params.limit}&$orderby=receivedDateTime desc"
        url += "&$select=subject,from,receivedDateTime,bodyPreview,hasAttachments"

        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        data = response.json()
        emails = data.get("value", [])

        if not emails:
            return f"No emails found matching '{params.query}'"

        if params.response_format == ResponseFormat.MARKDOWN:
            lines = [f"# Email Search Results: '{params.query}'", ""]
            lines.append(f"Found {len(emails)} emails\n")
            for email in emails:
                lines.append(_format_email_markdown(email))
            return "\n".join(lines)
        else:
            return json.dumps({"query": params.query, "count": len(emails), "emails": emails}, indent=2)

    except Exception as e:
        return _handle_api_error(e)


@mcp.tool(
    name="graph_create_calendar_event",
    annotations={
        "title": "Create Calendar Event",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True
    }
)
async def graph_create_calendar_event(params: CreateCalendarEventInput) -> str:
    """Create a new event in the user's calendar.

    Adds a calendar event with the specified details. This demonstrates write
    operations and is useful for adding conference sessions to your calendar.

    Args:
        params (CreateCalendarEventInput): Contains event details

    Returns:
        str: Confirmation message with event details or error

    Examples:
        - "Add Session 87 to my calendar for Thursday, November 6 at 9am"
        - "Create a meeting with John tomorrow at 2pm in Room G7"
        - "Schedule Conference Session 127 on November 6 at 2:20pm"
    """
    try:
        headers = _get_headers()

        # Parse datetime
        from dateutil import parser as date_parser

        try:
            start_dt = date_parser.parse(params.start_datetime)
        except Exception:
            return f"Error: Could not parse start date '{params.start_datetime}'. Use format like '2025-11-06T09:00:00' or '2025-11-06 9:00 AM'"

        # Calculate end time if not provided
        if params.end_datetime:
            try:
                end_dt = date_parser.parse(params.end_datetime)
            except Exception:
                return f"Error: Could not parse end date '{params.end_datetime}'"
        else:
            end_dt = start_dt + timedelta(hours=1)

        # Build event object
        event = {
            "subject": params.subject,
            "start": {
                "dateTime": start_dt.strftime("%Y-%m-%dT%H:%M:%S"),
                "timeZone": "Central Standard Time"
            },
            "end": {
                "dateTime": end_dt.strftime("%Y-%m-%dT%H:%M:%S"),
                "timeZone": "Central Standard Time"
            },
        }

        if params.location:
            event["location"] = {"displayName": params.location}

        if params.body:
            event["body"] = {
                "contentType": "text",
                "content": params.body
            }

        # Create event
        url = f"{GRAPH_API_BASE}/me/calendar/events"
        response = requests.post(url, headers=headers, json=event, timeout=30)
        response.raise_for_status()

        created_event = response.json()

        if params.response_format == ResponseFormat.MARKDOWN:
            lines = ["# Calendar Event Created Successfully!", ""]
            lines.append(f"**Subject**: {params.subject}")
            lines.append(f"**Start**: {start_dt.strftime('%B %d, %Y at %I:%M %p')}")
            lines.append(f"**End**: {end_dt.strftime('%B %d, %Y at %I:%M %p')}")
            if params.location:
                lines.append(f"**Location**: {params.location}")
            lines.append(f"\n**Event ID**: {created_event.get('id', 'N/A')}")
            return "\n".join(lines)
        else:
            return json.dumps(created_event, indent=2)

    except Exception as e:
        return _handle_api_error(e)


@mcp.tool(
    name="graph_get_calendar_events",
    annotations={
        "title": "Get Calendar Events",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True
    }
)
async def graph_get_calendar_events(params: GetCalendarEventsInput) -> str:
    """Get calendar events for a date range.

    Retrieves calendar events to verify scheduled meetings and sessions.
    Useful for checking if an event was successfully created.

    Args:
        params (GetCalendarEventsInput): Contains date range, limit, and format

    Returns:
        str: Formatted list of calendar events or error message

    Examples:
        - "Show my calendar for today"
        - "What meetings do I have on November 6?"
        - "Show my calendar for next week"
    """
    try:
        headers = _get_headers()

        # Parse dates
        from dateutil import parser as date_parser

        if params.start_date:
            try:
                start_dt = date_parser.parse(params.start_date)
            except Exception:
                return f"Error: Could not parse start date '{params.start_date}'"
        else:
            start_dt = datetime.now()

        if params.end_date:
            try:
                end_dt = date_parser.parse(params.end_date)
            except Exception:
                return f"Error: Could not parse end date '{params.end_date}'"
        else:
            end_dt = start_dt + timedelta(days=7)

        # Query calendar
        url = f"{GRAPH_API_BASE}/me/calendar/calendarView"
        url += f"?startDateTime={start_dt.strftime('%Y-%m-%dT00:00:00')}"
        url += f"&endDateTime={end_dt.strftime('%Y-%m-%dT23:59:59')}"
        url += f"&$top={params.limit}&$orderby=start/dateTime"

        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        data = response.json()
        events = data.get("value", [])

        if not events:
            date_range = f"{start_dt.strftime('%B %d')} to {end_dt.strftime('%B %d, %Y')}"
            return f"No calendar events found for {date_range}"

        if params.response_format == ResponseFormat.MARKDOWN:
            lines = ["# Calendar Events", ""]
            date_range = f"{start_dt.strftime('%B %d')} to {end_dt.strftime('%B %d, %Y')}"
            lines.append(f"**Date Range**: {date_range}")
            lines.append(f"**Found**: {len(events)} events\n")
            for event in events:
                lines.append(_format_event_markdown(event))
            return "\n".join(lines)
        else:
            return json.dumps({
                "start_date": start_dt.strftime('%Y-%m-%d'),
                "end_date": end_dt.strftime('%Y-%m-%d'),
                "count": len(events),
                "events": events
            }, indent=2)

    except Exception as e:
        return _handle_api_error(e)


if __name__ == "__main__":
    # Check authentication before starting
    if auth_manager and not auth_manager.ensure_authenticated():
        print("\n⚠️  Authentication required!")
        print("Run authentication setup or check environment variables:")
        print("  - TENANT_ID")
        print("  - CLIENT_ID")
        print("  - CLIENT_SECRET (optional)")
        print("\nServer will start but tools may fail without authentication.\n")

    # Run the MCP server
    mcp.run()
