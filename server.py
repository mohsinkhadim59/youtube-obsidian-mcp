#!/usr/bin/env python3
"""
YouTube Lecture Notes MCP Server for Obsidian
Automatically extracts subtitles, captures screenshots at timestamps,
and generates professional study notes for any YouTube video lecture.
"""

import asyncio
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# MCP SDK imports
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    CallToolResult,
)

# Configuration - UPDATE THESE PATHS
DEFAULT_OBSIDIAN_VAULT = os.environ.get("OBSIDIAN_VAULT_PATH", r"C:\Users\YourUsername\ObsidianVault")
DEFAULT_NOTES_FOLDER = "Lecture Notes"
DEFAULT_IMAGES_FOLDER = "Lecture Notes/images"

server = Server("youtube-notes")


def parse_timestamp(ts: str) -> int:
    """Convert timestamp string (MM:SS or HH:MM:SS) to seconds."""
    parts = ts.strip().split(":")
    if len(parts) == 2:
        return int(parts[0]) * 60 + int(parts[1])
    elif len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    else:
        raise ValueError(f"Invalid timestamp format: {ts}")


def format_timestamp(seconds: int) -> str:
    """Convert seconds to HH:MM:SS format."""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def extract_video_id(url: str) -> str:
    """Extract YouTube video ID from URL."""
    patterns = [
        r'(?:v=|/v/|youtu\.be/)([a-zA-Z0-9_-]{11})',
        r'(?:embed/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError(f"Could not extract video ID from: {url}")


def get_video_info(url: str) -> dict:
    """Get video title and metadata using yt-dlp."""
    result = subprocess.run(
        ["yt-dlp", "--dump-json", "--no-download", url],
        capture_output=True,
        text=True,
        encoding='utf-8'
    )
    if result.returncode != 0:
        raise Exception(f"Failed to get video info: {result.stderr}")
    return json.loads(result.stdout)


def download_subtitles(url: str, output_dir: Path) -> Path:
    """Download subtitles using yt-dlp."""
    output_template = str(output_dir / "%(id)s")
    
    # Try auto-generated subtitles first, then manual
    result = subprocess.run(
        [
            "yt-dlp",
            "--write-auto-sub",
            "--write-sub",
            "--sub-lang", "en",
            "--sub-format", "vtt",
            "--skip-download",
            "--output", output_template,
            url
        ],
        capture_output=True,
        text=True,
        encoding='utf-8'
    )
    
    # Find the subtitle file
    video_id = extract_video_id(url)
    for ext in [".en.vtt", ".en.auto.vtt"]:
        sub_file = output_dir / f"{video_id}{ext}"
        if sub_file.exists():
            return sub_file
    
    raise Exception(f"No subtitles found. stderr: {result.stderr}")


def parse_vtt_subtitles(vtt_path: Path) -> list[dict]:
    """Parse VTT subtitle file into list of {start, end, text}."""
    content = vtt_path.read_text(encoding='utf-8')
    
    # Remove VTT header
    lines = content.split('\n')
    subtitles = []
    current_entry = None
    
    timestamp_pattern = re.compile(
        r'(\d{2}:\d{2}:\d{2}\.\d{3}|\d{2}:\d{2}\.\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}\.\d{3}|\d{2}:\d{2}\.\d{3})'
    )
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines and headers
        if not line or line.startswith('WEBVTT') or line.startswith('Kind:') or line.startswith('Language:'):
            if current_entry and current_entry.get('text'):
                subtitles.append(current_entry)
                current_entry = None
            continue
        
        # Check for timestamp
        match = timestamp_pattern.match(line)
        if match:
            if current_entry and current_entry.get('text'):
                subtitles.append(current_entry)
            
            start_str = match.group(1)
            end_str = match.group(2)
            
            # Parse timestamp to seconds
            def parse_vtt_time(t):
                parts = t.replace('.', ':').split(':')
                if len(parts) == 4:  # HH:MM:SS.mmm
                    return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2]) + int(parts[3]) / 1000
                else:  # MM:SS.mmm
                    return int(parts[0]) * 60 + int(parts[1]) + int(parts[2]) / 1000
            
            current_entry = {
                'start': parse_vtt_time(start_str),
                'end': parse_vtt_time(end_str),
                'text': ''
            }
        elif current_entry is not None and not line.isdigit():
            # Remove VTT formatting tags
            clean_text = re.sub(r'<[^>]+>', '', line)
            clean_text = re.sub(r'&nbsp;', ' ', clean_text)
            if current_entry['text']:
                current_entry['text'] += ' ' + clean_text
            else:
                current_entry['text'] = clean_text
    
    # Add last entry
    if current_entry and current_entry.get('text'):
        subtitles.append(current_entry)
    
    # Merge duplicates and clean up
    merged = []
    for sub in subtitles:
        sub['text'] = sub['text'].strip()
        if not sub['text']:
            continue
        if merged and merged[-1]['text'] == sub['text']:
            merged[-1]['end'] = sub['end']
        else:
            merged.append(sub)
    
    return merged


def capture_screenshot(url: str, timestamp_seconds: int, output_path: Path) -> bool:
    """Capture a screenshot at the given timestamp using yt-dlp + ffmpeg."""
    temp_dir = output_path.parent / "temp"
    temp_dir.mkdir(exist_ok=True)
    
    # Download a small segment around the timestamp
    temp_video = temp_dir / "temp_segment.mp4"
    
    # Use yt-dlp to get the direct URL, then ffmpeg to extract frame
    result = subprocess.run(
        ["yt-dlp", "-g", "-f", "best[height<=720]", url],
        capture_output=True,
        text=True,
        encoding='utf-8'
    )
    
    if result.returncode != 0:
        return False
    
    video_url = result.stdout.strip().split('\n')[0]
    
    # Use ffmpeg to extract the frame
    result = subprocess.run(
        [
            "ffmpeg",
            "-ss", str(timestamp_seconds),
            "-i", video_url,
            "-vframes", "1",
            "-q:v", "2",
            "-y",
            str(output_path)
        ],
        capture_output=True,
        text=True
    )
    
    return output_path.exists()


def get_subtitle_at_timestamp(subtitles: list[dict], timestamp_seconds: int, context_window: int = 30) -> str:
    """Get subtitle text around a specific timestamp."""
    relevant = []
    for sub in subtitles:
        if sub['start'] >= timestamp_seconds - 5 and sub['start'] <= timestamp_seconds + context_window:
            relevant.append(sub['text'])
    return ' '.join(relevant)


def generate_notes(
    video_info: dict,
    subtitles: list[dict],
    timestamps: list[int],
    image_paths: list[Path],
    day_number: int,
    obsidian_vault: Path,
    images_folder: str
) -> str:
    """Generate professional Obsidian-formatted notes."""

    title = video_info.get('title', 'Video Lecture')
    duration = video_info.get('duration', 0)
    upload_date = video_info.get('upload_date', '')
    channel = video_info.get('channel', 'Unknown')
    video_url = video_info.get('webpage_url', '')

    # Format date
    today = datetime.now().strftime("%Y-%m-%d")

    # Build the note content
    note = f"""---
date: {today}
day: {day_number}
tags: [lecture, video-notes, learning]
video: "{video_url}"
---

# Day {day_number}: {title}

> **Source**: [{channel}]({video_url})
> **Duration**: {format_timestamp(duration)}
> **Study Date**: {today}

---

## 📋 Summary

"""
    
    # Generate summary from full subtitles
    full_text = ' '.join([s['text'] for s in subtitles])
    # Truncate for summary section (will be filled by Claude when processing)
    note += f"*[Auto-generated from lecture transcript - {len(full_text.split())} words]*\n\n"
    
    note += "---\n\n## 📝 Key Concepts & Notes\n\n"
    
    # Add sections for each timestamp with screenshot
    for i, (ts, img_path) in enumerate(zip(timestamps, image_paths), 1):
        ts_formatted = format_timestamp(ts)
        context = get_subtitle_at_timestamp(subtitles, ts, context_window=60)
        
        # Relative path for Obsidian
        rel_img_path = img_path.relative_to(obsidian_vault)
        obsidian_img_link = str(rel_img_path).replace('\\', '/')
        
        note += f"""### Timestamp {ts_formatted}

![[{obsidian_img_link}]]

**Context from lecture:**
> {context[:500]}{'...' if len(context) > 500 else ''}

**Key Points:**
- 

---

"""
    
    note += """## 🔑 Key Terms & Definitions

| Term | Definition |
|------|------------|
|  |  |

---

## ✅ Review Questions

1. 
2. 
3. 

---

## 📚 Additional Resources

- 

---

## 💭 Personal Notes & Observations

"""
    
    # Add full transcript at the end (collapsible)
    note += f"""
---

<details>
<summary>📜 Full Transcript</summary>

"""
    
    # Add transcript with timestamps
    current_minute = -1
    for sub in subtitles:
        minute = int(sub['start'] // 60)
        if minute != current_minute and minute % 5 == 0:
            current_minute = minute
            note += f"\n**[{format_timestamp(int(sub['start']))}]**\n\n"
        note += sub['text'] + ' '
    
    note += "\n\n</details>\n"
    
    return note


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="process_youtube_lecture",
            description="""Process a YouTube lecture video and create Obsidian notes.
            
            Extracts subtitles, captures screenshots at specified timestamps,
            and generates professional study notes in your Obsidian vault.
            
            Required parameters:
            - url: YouTube video URL
            - timestamps: Comma-separated timestamps (e.g., "5:30, 12:45, 25:00")
            - day_number: The day number for your study schedule
            
            Optional parameters:
            - vault_path: Path to your Obsidian vault (uses default if not specified)
            - notes_folder: Folder within vault for notes (default: "Lecture Notes")
            - images_folder: Folder for screenshots (default: "Lecture Notes/images")
            """,
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "YouTube video URL"
                    },
                    "timestamps": {
                        "type": "string",
                        "description": "Comma-separated timestamps for screenshots (e.g., '5:30, 12:45, 25:00')"
                    },
                    "day_number": {
                        "type": "integer",
                        "description": "Day number in your study schedule"
                    },
                    "vault_path": {
                        "type": "string",
                        "description": "Path to Obsidian vault (optional)"
                    },
                    "notes_folder": {
                        "type": "string",
                        "description": "Folder for notes within vault (optional)"
                    },
                    "images_folder": {
                        "type": "string",
                        "description": "Folder for images within vault (optional)"
                    }
                },
                "required": ["url", "timestamps", "day_number"]
            }
        ),
        Tool(
            name="get_video_subtitles",
            description="""Get the full subtitles/transcript of a YouTube video.
            
            Useful for reviewing the content before deciding on timestamps.
            
            Parameters:
            - url: YouTube video URL
            """,
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "YouTube video URL"
                    }
                },
                "required": ["url"]
            }
        ),
        Tool(
            name="configure_paths",
            description="""View or update the default paths for Obsidian vault and folders.
            
            Parameters:
            - vault_path: New default path for Obsidian vault (optional)
            - notes_folder: New default notes folder (optional)
            - images_folder: New default images folder (optional)
            
            If no parameters provided, returns current configuration.
            """,
            inputSchema={
                "type": "object",
                "properties": {
                    "vault_path": {
                        "type": "string",
                        "description": "Path to Obsidian vault"
                    },
                    "notes_folder": {
                        "type": "string",
                        "description": "Folder for notes within vault"
                    },
                    "images_folder": {
                        "type": "string",
                        "description": "Folder for images within vault"
                    }
                },
                "required": []
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool calls."""
    
    if name == "configure_paths":
        global DEFAULT_OBSIDIAN_VAULT, DEFAULT_NOTES_FOLDER, DEFAULT_IMAGES_FOLDER
        
        if arguments.get("vault_path"):
            DEFAULT_OBSIDIAN_VAULT = arguments["vault_path"]
        if arguments.get("notes_folder"):
            DEFAULT_NOTES_FOLDER = arguments["notes_folder"]
        if arguments.get("images_folder"):
            DEFAULT_IMAGES_FOLDER = arguments["images_folder"]
        
        return [TextContent(
            type="text",
            text=f"""Current configuration:
- Vault Path: {DEFAULT_OBSIDIAN_VAULT}
- Notes Folder: {DEFAULT_NOTES_FOLDER}
- Images Folder: {DEFAULT_IMAGES_FOLDER}"""
        )]
    
    elif name == "get_video_subtitles":
        url = arguments["url"]
        
        try:
            # Get video info
            video_info = get_video_info(url)
            title = video_info.get('title', 'Unknown')
            duration = video_info.get('duration', 0)
            
            # Download subtitles to temp directory
            temp_dir = Path.home() / ".youtube-notes-temp"
            temp_dir.mkdir(exist_ok=True)
            
            sub_file = download_subtitles(url, temp_dir)
            subtitles = parse_vtt_subtitles(sub_file)
            
            # Format output
            output = f"# {title}\n"
            output += f"Duration: {format_timestamp(duration)}\n\n"
            output += "## Transcript:\n\n"
            
            current_minute = -1
            for sub in subtitles:
                minute = int(sub['start'] // 60)
                if minute != current_minute:
                    current_minute = minute
                    output += f"\n**[{format_timestamp(int(sub['start']))}]** "
                output += sub['text'] + ' '
            
            return [TextContent(type="text", text=output)]
            
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    elif name == "process_youtube_lecture":
        url = arguments["url"]
        timestamps_str = arguments["timestamps"]
        day_number = arguments["day_number"]
        vault_path = Path(arguments.get("vault_path", DEFAULT_OBSIDIAN_VAULT))
        notes_folder = arguments.get("notes_folder", DEFAULT_NOTES_FOLDER)
        images_folder = arguments.get("images_folder", DEFAULT_IMAGES_FOLDER)
        
        try:
            # Parse timestamps
            timestamps = [parse_timestamp(ts.strip()) for ts in timestamps_str.split(",")]
            
            # Create directories
            notes_dir = vault_path / notes_folder
            images_dir = vault_path / images_folder
            notes_dir.mkdir(parents=True, exist_ok=True)
            images_dir.mkdir(parents=True, exist_ok=True)
            
            # Get video info
            video_info = get_video_info(url)
            video_id = extract_video_id(url)
            title = video_info.get('title', 'Video Lecture')
            
            # Download subtitles
            temp_dir = Path.home() / ".youtube-notes-temp"
            temp_dir.mkdir(exist_ok=True)
            sub_file = download_subtitles(url, temp_dir)
            subtitles = parse_vtt_subtitles(sub_file)
            
            # Capture screenshots
            image_paths = []
            for i, ts in enumerate(timestamps, 1):
                img_name = f"day{day_number}_{video_id}_{i}_{ts}s.jpg"
                img_path = images_dir / img_name
                
                success = capture_screenshot(url, ts, img_path)
                if success:
                    image_paths.append(img_path)
                else:
                    # Create placeholder if screenshot fails
                    image_paths.append(img_path)
            
            # Generate notes
            notes_content = generate_notes(
                video_info=video_info,
                subtitles=subtitles,
                timestamps=timestamps,
                image_paths=image_paths,
                day_number=day_number,
                obsidian_vault=vault_path,
                images_folder=images_folder
            )
            
            # Save notes
            safe_title = re.sub(r'[<>:"/\\|?*]', '', title)[:50]
            note_filename = f"Day {day_number:02d} - {safe_title}.md"
            note_path = notes_dir / note_filename
            note_path.write_text(notes_content, encoding='utf-8')
            
            return [TextContent(
                type="text",
                text=f"""✅ Successfully created notes!

**Video:** {title}
**Note saved to:** {note_path}
**Screenshots captured:** {len([p for p in image_paths if p.exists()])} of {len(timestamps)}
**Transcript length:** {len(subtitles)} segments

The note includes:
- Video metadata and link
- Screenshots at your specified timestamps
- Context from subtitles around each timestamp
- Full transcript (collapsible)
- Sections for key terms, review questions, and personal notes

Open Obsidian to view and edit your notes!"""
            )]
            
        except Exception as e:
            import traceback
            return [TextContent(
                type="text",
                text=f"Error processing video: {str(e)}\n\n{traceback.format_exc()}"
            )]
    
    return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
