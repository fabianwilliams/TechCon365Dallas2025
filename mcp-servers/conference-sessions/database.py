"""
Database management for conference sessions.
Creates and manages the SQLite database.
"""

import sqlite3
from typing import List, Optional, Dict, Any
from pathlib import Path
from parser import Session, SessionParser


class SessionDatabase:
    """Manage conference sessions database"""

    def __init__(self, db_path: str = "sessions.db"):
        self.db_path = db_path
        self.conn = None

    def connect(self):
        """Connect to the database"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        return self.conn

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

    def create_schema(self):
        """Create database schema"""
        cursor = self.conn.cursor()

        # Drop existing table if it exists
        cursor.execute("DROP TABLE IF EXISTS sessions")

        # Create sessions table
        cursor.execute("""
            CREATE TABLE sessions (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                speakers TEXT,
                track TEXT,
                level TEXT,
                location TEXT,
                time_slot TEXT,
                day TEXT,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create indexes for common queries
        cursor.execute("CREATE INDEX idx_track ON sessions(track)")
        cursor.execute("CREATE INDEX idx_level ON sessions(level)")
        cursor.execute("CREATE INDEX idx_location ON sessions(location)")
        cursor.execute("CREATE INDEX idx_speakers ON sessions(speakers)")
        cursor.execute("CREATE INDEX idx_day ON sessions(day)")

        # Full-text search index for title and description
        cursor.execute("""
            CREATE VIRTUAL TABLE sessions_fts USING fts5(
                title, description, speakers, track,
                content='sessions',
                content_rowid='id'
            )
        """)

        self.conn.commit()
        print("✓ Database schema created")

    def insert_sessions(self, sessions: List[Session]):
        """Insert sessions into database"""
        cursor = self.conn.cursor()

        for session in sessions:
            cursor.execute("""
                INSERT INTO sessions (id, title, speakers, track, level, location, time_slot, day, description)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session.id,
                session.title,
                session.speakers,
                session.track,
                session.level,
                session.location,
                session.time_slot,
                session.day,
                session.description
            ))

            # Insert into FTS table
            cursor.execute("""
                INSERT INTO sessions_fts (rowid, title, description, speakers, track)
                VALUES (?, ?, ?, ?, ?)
            """, (
                session.id,
                session.title,
                session.description,
                session.speakers,
                session.track
            ))

        self.conn.commit()
        print(f"✓ Inserted {len(sessions)} sessions")

    def search_sessions(self, query: str, track: Optional[str] = None,
                       level: Optional[str] = None, location: Optional[str] = None,
                       limit: int = 20) -> List[Dict[str, Any]]:
        """Search sessions with optional filters"""
        cursor = self.conn.cursor()

        # Build query
        sql = """
            SELECT s.* FROM sessions s
            INNER JOIN sessions_fts fts ON s.id = fts.rowid
            WHERE sessions_fts MATCH ?
        """
        params = [query]

        if track:
            sql += " AND s.track LIKE ?"
            params.append(f"%{track}%")

        if level:
            sql += " AND s.level = ?"
            params.append(level)

        if location:
            sql += " AND s.location LIKE ?"
            params.append(f"%{location}%")

        sql += f" LIMIT {limit}"

        cursor.execute(sql, params)
        return [dict(row) for row in cursor.fetchall()]

    def get_session_by_id(self, session_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific session by ID"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM sessions WHERE id = ?", (session_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_all_tracks(self) -> List[str]:
        """Get list of all unique tracks"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT DISTINCT track FROM sessions
            WHERE track IS NOT NULL AND track != ''
            ORDER BY track
        """)
        return [row[0] for row in cursor.fetchall()]

    def get_all_speakers(self) -> List[str]:
        """Get list of all unique speakers"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT DISTINCT speakers FROM sessions
            WHERE speakers IS NOT NULL AND speakers != ''
            ORDER BY speakers
        """)
        return [row[0] for row in cursor.fetchall()]

    def get_sessions_by_location(self, location: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Get sessions in a specific location"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM sessions
            WHERE location LIKE ?
            LIMIT ?
        """, (f"%{location}%", limit))
        return [dict(row) for row in cursor.fetchall()]

    def get_sessions_by_track(self, track: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Get sessions for a specific track"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM sessions
            WHERE track LIKE ?
            LIMIT ?
        """, (f"%{track}%", limit))
        return [dict(row) for row in cursor.fetchall()]

    def get_sessions_by_level(self, level: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Get sessions for a specific level"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM sessions
            WHERE level = ?
            LIMIT ?
        """, (level, limit))
        return [dict(row) for row in cursor.fetchall()]

    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        cursor = self.conn.cursor()

        # Total sessions
        cursor.execute("SELECT COUNT(*) FROM sessions")
        total_sessions = cursor.fetchone()[0]

        # Sessions by level
        cursor.execute("""
            SELECT level, COUNT(*) as count
            FROM sessions
            WHERE level IS NOT NULL AND level != ''
            GROUP BY level
        """)
        by_level = {row[0]: row[1] for row in cursor.fetchall()}

        # Sessions by day
        cursor.execute("""
            SELECT day, COUNT(*) as count
            FROM sessions
            WHERE day IS NOT NULL AND day != ''
            GROUP BY day
        """)
        by_day = {row[0]: row[1] for row in cursor.fetchall()}

        return {
            "total_sessions": total_sessions,
            "by_level": by_level,
            "by_day": by_day
        }


def build_database(markdown_file: str, db_path: str = "sessions.db"):
    """Build the database from markdown file"""
    print(f"Building database from {markdown_file}...")

    # Parse sessions
    parser = SessionParser(markdown_file)
    sessions = parser.parse()
    print(f"✓ Parsed {len(sessions)} sessions")

    # Create database
    db = SessionDatabase(db_path)
    db.connect()
    db.create_schema()
    db.insert_sessions(sessions)

    # Print stats
    stats = db.get_stats()
    print(f"\n📊 Database Statistics:")
    print(f"   Total sessions: {stats['total_sessions']}")
    print(f"   By level: {stats['by_level']}")
    print(f"   By day: {stats['by_day']}")

    db.close()
    print(f"\n✓ Database created at {db_path}")
    return db_path


def main():
    """Build the database"""
    project_root = Path(__file__).parent.parent.parent
    sessions_file = project_root / "sessions-extracted.md"

    if not sessions_file.exists():
        print(f"Error: Could not find {sessions_file}")
        return

    build_database(str(sessions_file))


if __name__ == "__main__":
    main()
