<div align="center">

# 📝 YouTube Lecture Notes MCP

<img src="assets/youtube-logo.png" width="80" alt="YouTube" />
<img src="assets/claude-logo.png" width="80" alt="Claude AI" />
<img src="assets/obsidian-logo.png" width="80" alt="Obsidian" />

### Automatically generate professional study notes from YouTube videos

**YouTube** + **Claude AI** + **Obsidian** = Supercharged Learning

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
![Last Commit](https://img.shields.io/github/last-commit/mohsinkhadim59/Networking-Basics-By-Cisco?style=flat&label=Updated&labelColor=555&color=red)
![Views](https://komarev.com/ghpvc/?username=mohsinkhadim59&repo=Networking-Basics-By-Cisco&style=flat&label=Views&color=blueviolet)
</div>

---

> Never manually take screenshots and paste them into notes again! This MCP server integrates with Claude Desktop to automatically extract subtitles, capture screenshots at key timestamps, and generate beautifully formatted Obsidian notes from any YouTube tutorial or lecture.

---

## ✨ Features

-  **Auto-extract subtitles** from any YouTube video with captions
-  **Capture screenshots** at timestamps you specify
-  **Generate structured notes** in Obsidian markdown format
-  **Organized metadata** with tags, dates, and video links
-  **Full transcripts** included with timestamps
-  **Preview subtitles** before processing
-  **Customizable paths** for your Obsidian vault organization
-  **Works with Claude AI** for natural language interaction

---

## 🎯 Perfect For

Learn from YouTube videos on **any** topic:

| Category                       | Examples                                        |
| ------------------------------ | ----------------------------------------------- |
|  **Programming**             | Python, JavaScript, React, Web Development      |
|  **Creative Skills**         | Photoshop, Premiere Pro, Blender, Video Editing |
|  **Business & Productivity** | Excel, Data Analysis, Project Management        |
|  **Academic**                | Math, Physics, Chemistry, Biology               |
|  **IT & Networking**         | CCNA, AWS, CompTIA, Cybersecurity               |
|  **Personal Development**    | Languages, Fitness, Cooking, Music              |

---

## 🚀 Quick Start

### Prerequisites

Before installation, make sure you have:

1. **Python 3.10+** - [Download here](https://www.python.org/downloads/)
   - ⚠️ Check "Add Python to PATH" during installation
2. **FFmpeg** - For capturing video screenshots
3. **Claude Desktop** - [Get it here](https://claude.ai/download)
4. **Obsidian** (optional but recommended) - [Download](https://obsidian.md/)

### Installation

#### Option 1: Automated Install (Recommended)

1. Clone or download this repository
2. Open PowerShell in the project folder
3. Run the installer:

```powershell
.\install.ps1
```

The script will:

- ✅ Check all prerequisites
- ✅ Install required Python packages
- ✅ Set up directory structure
- ✅ Generate Claude Desktop configuration

#### Option 2: Manual Install

See the detailed [SETUP_GUIDE.md](SETUP_GUIDE.md) for step-by-step instructions.

---

## 💡 Usage

Once installed, just talk to Claude naturally in Claude Desktop!

### Example 1: Process a Python Tutorial

```
Hey Claude, process this Python tutorial:
https://www.youtube.com/watch?v=rfscVS0vtbw

Capture screenshots at: 2:30, 8:15, 15:00, 22:45, 35:00
This is Day 1 of my learning journey.
```

### Example 2: Preview Before Processing

```
Can you show me the subtitles for this video first?
https://www.youtube.com/watch?v=example

Then I'll tell you which timestamps to capture.
```

### Example 3: Custom Organization

```
Configure my YouTube notes:
- Vault: D:\Learning\Obsidian
- Notes folder: Courses/Web Development
- Images folder: Courses/Web Development/assets
```

---

## What You Get

Each processed video creates:

### 1. Markdown Note File

```
Day 01 - Complete Python Course for Beginners.md
```

### 2. Screenshot Images

```
day1_abc123_1_150s.jpg
day1_abc123_2_495s.jpg
day1_abc123_3_900s.jpg
```

### 3. Structured Content

```markdown
---
date: 2026-01-16
day: 1
tags: [lecture, video-notes, learning]
video: "https://youtube.com/watch?v=..."
---

# Day 1: Complete Python Course for Beginners

> **Source**: [freeCodeCamp.org](https://youtube.com/...) > **Duration**: 4:26:54
> **Study Date**: 2026-01-16

## Summary

[Automatic summary from transcript]

## Key Concepts & Notes

### Timestamp 02:30

![Screenshot](images/day1_xxx_1_150s.jpg)

**Context from lecture:**

> In this section, we cover variables and data types...

**Key Points:**

- [Your notes here]

## Key Terms & Definitions

| Term | Definition |
| ---- | ---------- |
|      |            |

## Review Questions

1.
2.

## Personal Notes & Observations

[Your thoughts]

## Full Transcript

[Complete timestamped transcript]
```

---

## 🛠️ Available Tools

The MCP server provides three tools accessible through Claude:

### 1. `process_youtube_lecture`

Main tool to process a video:

- Extracts subtitles
- Captures screenshots at your timestamps
- Generates complete Obsidian note

**Parameters:**

- `url` - YouTube video URL (required)
- `timestamps` - Comma-separated times like "5:30, 12:00, 25:00" (required)
- `day_number` - Your study day number (required)
- `vault_path` - Custom vault path (optional)
- `notes_folder` - Custom notes folder (optional)
- `images_folder` - Custom images folder (optional)

### 2. `get_video_subtitles`

Preview the full transcript before processing:

- Returns complete subtitles with timestamps
- Helps you identify key moments

**Parameters:**

- `url` - YouTube video URL (required)

### 3. `configure_paths`

Set or view your default paths:

- Configure Obsidian vault location
- Set custom folder structure

**Parameters:**

- `vault_path` - New vault path (optional)
- `notes_folder` - New notes folder (optional)
- `images_folder` - New images folder (optional)

---

## 📂 File Structure

After installation, your files will be organized like this:

```
C:\Users\YourName\
├── mcp-servers\
│   └── youtube-lecture-notes\
│       ├── server.py
│       └── claude_config_snippet.json
│
└── Documents\
    └── ObsidianVault\
        └── Lecture Notes\
            ├── Day 01 - Python Basics.md
            ├── Day 02 - Advanced Functions.md
            └── images\
                ├── day1_xxx_1_150s.jpg
                ├── day1_xxx_2_495s.jpg
                └── day2_xxx_1_300s.jpg
```

---

## 🔧 Troubleshooting

### Common Issues

**"python is not recognized"**

- Reinstall Python and check "Add to PATH"
- Or specify full path in config: `C:\\Python312\\python.exe`

**"ffmpeg is not recognized"**

- Install FFmpeg: `winget install ffmpeg`
- Restart terminal after installation
- Verify: `ffmpeg -version`

**"No subtitles found"**

- Check if the video has captions enabled on YouTube
- Try with a different video to test
- Some videos may not have subtitles available

**MCP not connecting**

- Verify paths in `claude_desktop_config.json` use double backslashes `\\`
- Restart Claude Desktop completely
- Check Claude Desktop logs in Settings > Developer

**Screenshots not capturing**

- Ensure FFmpeg is installed correctly
- Video may be region-restricted
- Some videos block downloading

For more help, see the [SETUP_GUIDE.md](SETUP_GUIDE.md) or open an issue on GitHub.

---

## 🎓 Tips for Best Results

1. **Preview first** - Use `get_video_subtitles` to scan content before choosing timestamps
2. **Pick key moments** - Choose 4-6 important timestamps per video (don't overdo it!)
3. **Watch at 2x speed** - Quickly identify where major concepts are introduced
4. **Fill in blanks** - The notes provide structure, but add your own insights
5. **Organize with tags** - Customize the `tags:` in frontmatter for your topics
6. **Review regularly** - Use the review questions section to test yourself

---

## 🎨 Customize Your Note Style

The generated notes are **fully customizable** to match your personal learning style and preferences!

### What You Can Customize

#### 1. **Note Structure & Sections**

- Add custom sections for your needs (code snippets, formulas, workflows)
- Reorder sections to match your thinking process
- Remove sections you don't use
- Create templates for different topics

#### 2. **Formatting & Style**

- Change heading styles and hierarchy
- Customize emoji usage and visual markers
- Adjust table layouts for terms and definitions
- Modify YAML frontmatter tags and metadata

#### 3. **Organization**

- Custom folder structures by topic, difficulty, or course
- Tag systems for easy filtering and linking
- Naming conventions that work for you
- Integration with your existing Obsidian vault structure

#### 4. **Content Enhancement**

- Add your own code blocks with syntax highlighting
- Include links to external resources
- Embed additional images or diagrams
- Create internal wiki-links to related notes

### How to Customize

**See the comprehensive [CUSTOMIZATION.md](CUSTOMIZATION.md) guide for:**

- Step-by-step customization instructions
- Pre-made templates for different learning styles
- Topic-specific note structures (programming, design, business, etc.)
- Advanced Obsidian integration tips
- Examples of customized notes

**Quick customization tips:**

- Edit `server.py` lines 254-349 to change the default note template
- Modify tags in the frontmatter after generation
- Use Obsidian templates for post-processing
- Create Obsidian CSS snippets for custom styling

💡 **Your notes, your way** - Start with the default structure and evolve it as you discover what works best for your learning!

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

- 🐛 Report bugs
- 💡 Suggest new features
- 🔧 Submit pull requests
- 📖 Improve documentation

---

## Acknowledgments

Built with:

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube download tool
- [FFmpeg](https://ffmpeg.org/) - Video processing
- [Obsidian](https://obsidian.md/) - Knowledge management

---

## 📚 Documentation

- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Detailed installation and setup instructions
- **[CLAUDE.md](CLAUDE.md)** - Instructions for Claude AI on how to use this MCP effectively
- **[EXAMPLE_NOTE.md](EXAMPLE_NOTE.md)** - Sample note structure and template
- **[CUSTOMIZATION.md](CUSTOMIZATION.md)** - Complete guide to customizing your note style

---

## 📬 Support & Community

- **Documentation**: Check [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **For Claude AI**: See [CLAUDE.md](CLAUDE.md) for usage guidelines
- **Issues**: [Report bugs here](https://github.com/mohsinkhadim59/youtube-obsidian-mcp/issues)
- **Discussions**: Share your use cases and tips
- **License**: [MIT License](License)

---

<div align="center">

**Made with ❤️ for learners everywhere** by [Mohsin Khadim](https://github.com/mohsinkhadim59)

</div>
