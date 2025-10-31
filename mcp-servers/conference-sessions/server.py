#!/usr/bin/env python3
"""
MCP Server for TechCon365 Dallas 2025 Conference Sessions.

This server provides tools to search and query conference session data
including speakers, tracks, locations, and session details.
"""

from typing import Optional, List, Dict, Any
from enum import Enum
from pathlib import Path
import json
import sqlite3
from pydantic import BaseModel, Field, ConfigDict
from mcp.server.fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP("conference_sessions_mcp")

# Constants
DB_PATH = Path(__file__).parent / "sessions.db"
CHARACTER_LIMIT = 25000  # Maximum response size in characters

# Enums
class ResponseFormat(str, Enum):
    """Output format for tool responses."""
    MARKDOWN = "markdown"
    JSON = "json"


class LevelFilter(str, Enum):
    """Session level filter options."""
    INTRO = "Intro/Overview"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"
    ALL = "All"


# Pydantic Models for Input Validation
class SearchSessionsInput(BaseModel):
    """Input model for session search operations."""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True
    )

    query: str = Field(
        ...,
        description="Search query to match against session titles, descriptions, speakers, and tracks (e.g., 'Copilot', 'Power Automate', 'AI')",
        min_length=2,
        max_length=200
    )
    track: Optional[str] = Field(
        default=None,
        description="Filter by track (e.g., 'Copilot / AI', 'Power Automate', 'SharePoint')"
    )
    level: Optional[LevelFilter] = Field(
        default=None,
        description="Filter by session level"
    )
    location: Optional[str] = Field(
        default=None,
        description="Filter by room/location (e.g., 'Room G7', 'Room G1')"
    )
    limit: Optional[int] = Field(
        default=20,
        description="Maximum number of results to return",
        ge=1,
        le=100
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' for human-readable or 'json' for machine-readable"
    )


class GetSessionInput(BaseModel):
    """Input model for getting a specific session by ID."""
    model_config = ConfigDict(validate_assignment=True)

    session_id: int = Field(
        ...,
        description="Unique session ID number (e.g., 1, 42, 182)",
        ge=1
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format"
    )


class ListInput(BaseModel):
    """Input model for list operations."""
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format"
    )


class FilterByLocationInput(BaseModel):
    """Input model for filtering sessions by location."""
    model_config = ConfigDict(str_strip_whitespace=True)

    location: str = Field(
        ...,
        description="Room or location name (e.g., 'Room G7', 'G1', 'Expo Hall')",
        min_length=1,
        max_length=100
    )
    limit: Optional[int] = Field(
        default=20,
        description="Maximum results to return",
        ge=1,
        le=100
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format"
    )


class FilterByLevelInput(BaseModel):
    """Input model for filtering sessions by level."""
    level: LevelFilter = Field(
        ...,
        description="Session level filter"
    )
    limit: Optional[int] = Field(
        default=20,
        description="Maximum results to return",
        ge=1,
        le=100
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format"
    )


# Shared utility functions
def _get_db_connection() -> sqlite3.Connection:
    """Get database connection with row factory."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def _format_session_markdown(session: Dict[str, Any]) -> str:
    """Format a single session as markdown."""
    lines = []
    lines.append(f"## [{session['id']}] {session['title']}")
    lines.append("")
    if session.get('speakers'):
        lines.append(f"**Speaker(s)**: {session['speakers']}")
    if session.get('track'):
        lines.append(f"**Track**: {session['track']}")
    if session.get('level'):
        lines.append(f"**Level**: {session['level']}")
    if session.get('location'):
        lines.append(f"**Location**: {session['location']}")
    if session.get('time_slot'):
        lines.append(f"**Time**: {session['time_slot']}")
    if session.get('day'):
        lines.append(f"**Day**: {session['day']}")
    if session.get('description'):
        # Truncate long descriptions
        desc = session['description']
        if len(desc) > 500:
            desc = desc[:500] + "..."
        lines.append(f"\n{desc}")
    lines.append("")
    return "\n".join(lines)


def _check_character_limit(result: str, data: List[Dict], format_type: str) -> str:
    """Check character limit and truncate if needed."""
    if len(result) <= CHARACTER_LIMIT:
        return result

    # Truncate to half the results
    truncated_count = max(1, len(data) // 2)

    if format_type == "markdown":
        lines = ["# Search Results (Truncated)", ""]
        lines.append(f"⚠️ Response truncated from {len(data)} to {truncated_count} results due to size limits.")
        lines.append(f"Use more specific filters or adjust the 'limit' parameter to see different results.\n")
        for session in data[:truncated_count]:
            lines.append(_format_session_markdown(session))
        return "\n".join(lines)
    else:
        return json.dumps({
            "truncated": True,
            "total_found": len(data),
            "showing": truncated_count,
            "message": "Response truncated. Use more specific filters or pagination.",
            "sessions": data[:truncated_count]
        }, indent=2)


def _handle_error(e: Exception) -> str:
    """Consistent error formatting across all tools."""
    if isinstance(e, sqlite3.Error):
        return f"Database error: {str(e)}. Please try again or contact support."
    return f"Error: {type(e).__name__} - {str(e)}"


# Tool definitions
@mcp.tool(
    name="conference_search_sessions",
    annotations={
        "title": "Search Conference Sessions",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def conference_search_sessions(params: SearchSessionsInput) -> str:
    """Search for conference sessions by keywords, track, level, or location.

    This tool performs full-text search across session titles, descriptions, speakers,
    and tracks. It supports multiple filters to narrow down results.

    Args:
        params (SearchSessionsInput): Validated input parameters containing:
            - query (str): Search string to match (e.g., "Copilot", "AI", "Power Platform")
            - track (Optional[str]): Filter by specific track
            - level (Optional[LevelFilter]): Filter by session level
            - location (Optional[str]): Filter by room/location
            - limit (Optional[int]): Max results, between 1-100 (default: 20)
            - response_format (ResponseFormat): Output format (default: markdown)

    Returns:
        str: Formatted search results containing session details

        Success markdown response:
        # Search Results: 'query'
        Found X sessions (showing Y)

        ## [ID] Session Title
        **Speaker(s)**: Name(s)
        **Track**: Track name
        **Level**: Level
        **Location**: Room
        **Time**: Time slot
        **Day**: Day of week
        Description...

        Success JSON response:
        {
            "total": int,      # Total matches found
            "count": int,      # Number in this response
            "sessions": [...]  # Array of session objects
        }

        Error response:
        "Error: <message>" or "No sessions found matching '<query>'"

    Examples:
        - Use when: "Find all AI-related sessions" -> query="AI"
        - Use when: "Show Copilot sessions in Room G7" -> query="Copilot", location="Room G7"
        - Use when: "Find beginner Power Automate sessions" -> query="Power Automate", level="Intro/Overview"
        - Don't use when: You have a specific session ID (use conference_get_session instead)
    """
    try:
        conn = _get_db_connection()
        cursor = conn.cursor()

        # Build search query
        sql = """
            SELECT s.* FROM sessions s
            INNER JOIN sessions_fts fts ON s.id = fts.rowid
            WHERE sessions_fts MATCH ?
        """
        query_params = [params.query]

        if params.track:
            sql += " AND s.track LIKE ?"
            query_params.append(f"%{params.track}%")

        if params.level:
            sql += " AND s.level = ?"
            query_params.append(params.level.value)

        if params.location:
            sql += " AND s.location LIKE ?"
            query_params.append(f"%{params.location}%")

        sql += f" LIMIT {params.limit}"

        cursor.execute(sql, query_params)
        sessions = [dict(row) for row in cursor.fetchall()]
        conn.close()

        if not sessions:
            return f"No sessions found matching '{params.query}'"

        # Format response
        if params.response_format == ResponseFormat.MARKDOWN:
            lines = [f"# Conference Session Search: '{params.query}'", ""]
            lines.append(f"Found {len(sessions)} sessions\n")

            for session in sessions:
                lines.append(_format_session_markdown(session))

            result = "\n".join(lines)
            return _check_character_limit(result, sessions, "markdown")

        else:
            # JSON format
            response = {
                "total": len(sessions),
                "count": len(sessions),
                "sessions": sessions
            }
            result = json.dumps(response, indent=2)
            return _check_character_limit(result, sessions, "json")

    except Exception as e:
        return _handle_error(e)


@mcp.tool(
    name="conference_get_session",
    annotations={
        "title": "Get Session Details by ID",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def conference_get_session(params: GetSessionInput) -> str:
    """Get detailed information about a specific conference session by its ID.

    Args:
        params (GetSessionInput): Contains session_id and response_format

    Returns:
        str: Complete session details or error message
    """
    try:
        conn = _get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sessions WHERE id = ?", (params.session_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return f"Session ID {params.session_id} not found. Try using conference_search_sessions to find available sessions."

        session = dict(row)

        if params.response_format == ResponseFormat.MARKDOWN:
            return _format_session_markdown(session)
        else:
            return json.dumps(session, indent=2)

    except Exception as e:
        return _handle_error(e)


@mcp.tool(
    name="conference_list_tracks",
    annotations={
        "title": "List All Conference Tracks",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def conference_list_tracks(params: ListInput) -> str:
    """List all available conference tracks.

    Returns a complete list of all tracks at the conference, useful for
    understanding what topics are covered and for filtering searches.

    Args:
        params (ListInput): Contains response_format

    Returns:
        str: List of all tracks in requested format
    """
    try:
        conn = _get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT track, COUNT(*) as session_count
            FROM sessions
            WHERE track IS NOT NULL AND track != ''
            GROUP BY track
            ORDER BY track
        """)
        tracks = cursor.fetchall()
        conn.close()

        if params.response_format == ResponseFormat.MARKDOWN:
            lines = ["# Conference Tracks", ""]
            lines.append(f"Total tracks: {len(tracks)}\n")
            for track in tracks:
                lines.append(f"- **{track['track']}** ({track['session_count']} sessions)")
            return "\n".join(lines)
        else:
            return json.dumps([{"track": t["track"], "session_count": t["session_count"]} for t in tracks], indent=2)

    except Exception as e:
        return _handle_error(e)


@mcp.tool(
    name="conference_list_speakers",
    annotations={
        "title": "List All Speakers",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def conference_list_speakers(params: ListInput) -> str:
    """List all conference speakers.

    Returns a list of all speakers presenting at the conference,
    useful for finding sessions by a specific person.

    Args:
        params (ListInput): Contains response_format

    Returns:
        str: List of all speakers
    """
    try:
        conn = _get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT speakers, COUNT(*) as session_count
            FROM sessions
            WHERE speakers IS NOT NULL AND speakers != '' AND speakers != 'TBD'
            GROUP BY speakers
            ORDER BY speakers
        """)
        speakers = cursor.fetchall()
        conn.close()

        if params.response_format == ResponseFormat.MARKDOWN:
            lines = ["# Conference Speakers", ""]
            lines.append(f"Total speakers: {len(speakers)}\n")
            for speaker in speakers:
                lines.append(f"- **{speaker['speakers']}** ({speaker['session_count']} session{'s' if speaker['session_count'] > 1 else ''})")
            return "\n".join(lines)
        else:
            return json.dumps([{"speaker": s["speakers"], "session_count": s["session_count"]} for s in speakers], indent=2)

    except Exception as e:
        return _handle_error(e)


@mcp.tool(
    name="conference_get_sessions_by_location",
    annotations={
        "title": "Get Sessions by Location",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def conference_get_sessions_by_location(params: FilterByLocationInput) -> str:
    """Get all sessions happening in a specific room or location.

    Useful for planning your schedule around a specific room or finding
    what's happening nearby.

    Args:
        params (FilterByLocationInput): Contains location, limit, and response_format

    Returns:
        str: List of sessions in the specified location
    """
    try:
        conn = _get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM sessions
            WHERE location LIKE ?
            LIMIT ?
        """, (f"%{params.location}%", params.limit))
        sessions = [dict(row) for row in cursor.fetchall()]
        conn.close()

        if not sessions:
            return f"No sessions found in location matching '{params.location}'"

        if params.response_format == ResponseFormat.MARKDOWN:
            lines = [f"# Sessions in {params.location}", ""]
            lines.append(f"Found {len(sessions)} sessions\n")
            for session in sessions:
                lines.append(_format_session_markdown(session))
            return "\n".join(lines)
        else:
            return json.dumps({"location": params.location, "count": len(sessions), "sessions": sessions}, indent=2)

    except Exception as e:
        return _handle_error(e)


@mcp.tool(
    name="conference_get_sessions_by_level",
    annotations={
        "title": "Get Sessions by Level",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def conference_get_sessions_by_level(params: FilterByLevelInput) -> str:
    """Get all sessions at a specific difficulty level.

    Filter sessions by expertise level to find content appropriate
    for your experience level.

    Args:
        params (FilterByLevelInput): Contains level, limit, and response_format

    Returns:
        str: List of sessions at the specified level
    """
    try:
        conn = _get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM sessions
            WHERE level = ?
            LIMIT ?
        """, (params.level.value, params.limit))
        sessions = [dict(row) for row in cursor.fetchall()]
        conn.close()

        if not sessions:
            return f"No sessions found at level '{params.level.value}'"

        if params.response_format == ResponseFormat.MARKDOWN:
            lines = [f"# {params.level.value} Sessions", ""]
            lines.append(f"Found {len(sessions)} sessions\n")
            for session in sessions:
                lines.append(_format_session_markdown(session))
            result = "\n".join(lines)
            return _check_character_limit(result, sessions, "markdown")
        else:
            response = {"level": params.level.value, "count": len(sessions), "sessions": sessions}
            result = json.dumps(response, indent=2)
            return _check_character_limit(result, sessions, "json")

    except Exception as e:
        return _handle_error(e)


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
