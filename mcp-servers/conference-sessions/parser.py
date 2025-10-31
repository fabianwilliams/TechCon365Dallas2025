"""
Conference sessions data parser.
Parses the extracted markdown from the PDF and creates structured data.
"""

import re
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Session:
    """Represents a conference session"""
    id: int
    title: str
    speakers: str
    track: str
    level: str
    location: str
    time_slot: str
    day: str
    description: str

    def to_dict(self) -> Dict:
        return asdict(self)


class SessionParser:
    """Parse conference sessions from extracted markdown"""

    def __init__(self, markdown_file: str):
        self.markdown_file = markdown_file
        self.sessions: List[Session] = []
        self.current_day = ""

    def parse(self) -> List[Session]:
        """Parse the markdown file and return list of sessions"""
        with open(self.markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split into lines and clean up
        lines = [line.strip() for line in content.split('\n')]

        # State machine for parsing
        i = 0
        session_id = 1

        while i < len(lines):
            line = lines[i]

            # Check for day header (e.g., "Monday, Nov 3, 2025")
            if self._is_day_header(line):
                self.current_day = line
                i += 1
                continue

            # Check for time slot (e.g., "09:00 AM – 05:00 PM")
            if self._is_time_slot(line):
                time_slot = line

                # Next lines should be title, then speakers, track, level, location
                title_lines = []
                i += 1

                # Collect title lines (until we hit "Speakers:")
                while i < len(lines) and not lines[i].startswith('Speakers:'):
                    if lines[i] and lines[i] not in ['Show details', 'Hide details', 'Search sessions...All DaysAll TracksTrack:']:
                        # Filter out UI noise
                        if not re.match(r'^Search sessions\.\.\.', lines[i]):
                            title_lines.append(lines[i])
                    i += 1

                title = ' '.join(title_lines).strip()

                # Skip if this is just registration/coffee break
                if not title or 'Registration' in title:
                    i += 1
                    continue

                # Extract metadata fields (speakers, track, level, location)
                speakers = ""
                track = ""
                level = ""
                location = ""

                # Parse metadata in any order until we hit "Hide details" or "Show details"
                while i < len(lines) and lines[i] not in ['Hide details', 'Show details']:
                    line = lines[i]

                    if line.startswith('Speakers:'):
                        speakers = line.replace('Speakers:', '').strip()
                        i += 1
                    elif 'Track:' in line:
                        # Handle both "Track: ..." and "...Track: ..." patterns
                        track_match = re.search(r'Track:\s*(.+)', line)
                        if track_match:
                            track = track_match.group(1).strip()
                        i += 1
                    elif line.startswith('Level:'):
                        level = line.replace('Level:', '').strip()
                        i += 1
                    elif line.startswith('Location:'):
                        location = line.replace('Location:', '').strip()
                        i += 1
                    else:
                        # Skip other lines (like empty lines or UI noise)
                        i += 1

                # Skip "Hide details" / "Show details"
                while i < len(lines) and lines[i] in ['Hide details', 'Show details']:
                    i += 1

                # Extract description (until next time slot or day)
                description_lines = []
                while i < len(lines):
                    if self._is_time_slot(lines[i]) or self._is_day_header(lines[i]):
                        break
                    if lines[i] and lines[i] not in ['Hide details', 'Show details']:
                        description_lines.append(lines[i])
                    i += 1

                description = ' '.join(description_lines).strip()

                # Create session object
                if title:  # Only add if we have a title
                    session = Session(
                        id=session_id,
                        title=title,
                        speakers=speakers,
                        track=track,
                        level=level,
                        location=location,
                        time_slot=time_slot,
                        day=self.current_day,
                        description=description
                    )
                    self.sessions.append(session)
                    session_id += 1

                continue

            i += 1

        return self.sessions

    def _is_day_header(self, line: str) -> bool:
        """Check if line is a day header like 'Monday, Nov 3, 2025'"""
        # Pattern: Weekday, Month Day, Year
        pattern = r'^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),\s+\w+\s+\d+,\s+\d{4}$'
        return bool(re.match(pattern, line))

    def _is_time_slot(self, line: str) -> bool:
        """Check if line is a time slot like '09:00 AM – 05:00 PM'"""
        # Pattern: HH:MM AM/PM – HH:MM AM/PM
        pattern = r'\d{1,2}:\d{2}\s+(AM|PM)\s+[–-]\s+\d{1,2}:\d{2}\s+(AM|PM)'
        return bool(re.search(pattern, line))

    def print_summary(self):
        """Print a summary of parsed sessions"""
        print(f"\nParsed {len(self.sessions)} sessions")
        print(f"\nFirst few sessions:")
        for session in self.sessions[:3]:
            print(f"\n  [{session.id}] {session.title}")
            print(f"      Speaker: {session.speakers}")
            print(f"      Track: {session.track}")
            print(f"      Level: {session.level}")
            print(f"      Location: {session.location}")
            print(f"      Time: {session.time_slot}")


def main():
    """Test the parser"""
    import sys
    from pathlib import Path

    # Find the sessions file
    project_root = Path(__file__).parent.parent.parent
    sessions_file = project_root / "sessions-extracted.md"

    if not sessions_file.exists():
        print(f"Error: Could not find {sessions_file}")
        sys.exit(1)

    print(f"Parsing {sessions_file}...")
    parser = SessionParser(str(sessions_file))
    sessions = parser.parse()
    parser.print_summary()

    # Print some stats
    print(f"\nTracks found:")
    tracks = set(s.track for s in sessions if s.track)
    for track in sorted(tracks):
        print(f"  - {track}")

    print(f"\nLevels found:")
    levels = set(s.level for s in sessions if s.level)
    for level in sorted(levels):
        print(f"  - {level}")

    print(f"\nLocations found:")
    locations = set(s.location for s in sessions if s.location)
    for location in sorted(locations):
        print(f"  - {location}")


if __name__ == "__main__":
    main()
