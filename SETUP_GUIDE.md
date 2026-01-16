<div align="center">

<img src="assets/youtube-logo.png" width="60" alt="YouTube" />
<img src="assets/claude-logo.png" width="60" alt="Claude AI" />
<img src="assets/obsidian-logo.png" width="60" alt="Obsidian" />

# YouTube Lecture Notes MCP - Setup Guide

### Automatically extract subtitles, capture screenshots, and generate professional study notes from any YouTube lecture video.

</div>

---

## What Can You Learn?

This tool works for **any** YouTube tutorial or lecture:
- 🐍 **Programming**: Python, JavaScript, Web Development
- 🎨 **Creative Skills**: Video Editing, Photoshop, Blender
- 📊 **Professional**: Excel, Data Analysis, Business
- 🔬 **Academic**: Math, Science, Engineering
- 🌐 **IT & Networking**: CCNA, CompTIA, Cloud Computing
- 🎓 **And literally anything else on YouTube!**

---

## Prerequisites (Install These First)

### 1. Python 3.10+
Download from: https://www.python.org/downloads/
⚠️ During installation, CHECK "Add Python to PATH"

### 2. FFmpeg (Required for Screenshots)

**Option A - Using winget (Recommended):**
```powershell
winget install ffmpeg
```

**Option B - Using Chocolatey:**
```powershell
choco install ffmpeg
```

**Option C - Manual Installation:**
1. Download from: https://www.gyan.dev/ffmpeg/builds/
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to your System PATH

### 3. yt-dlp (YouTube Downloader)
```powershell
pip install yt-dlp
```

---

## Quick Installation (Automated)

### Option 1: Run the Installer Script

1. Download this repository
2. Open PowerShell in the folder
3. Run:
```powershell
.\install.ps1
```

The script will:
- ✅ Check all prerequisites
- ✅ Install Python packages
- ✅ Set up directories
- ✅ Generate Claude config for you

---

## Manual Installation

### Step 1: Download the MCP Server

Save `server.py` to a permanent location:
```
C:\Users\YourUsername\mcp-servers\youtube-lecture-notes\server.py
```

### Step 2: Install Python Dependencies

Open PowerShell and run:
```powershell
pip install mcp yt-dlp
```

### Step 3: Configure Claude Desktop

1. Open Claude Desktop
2. Go to **Settings** (gear icon) → **Developer** → **Edit Config**
3. This opens `claude_desktop_config.json`
4. Add the youtube-notes server configuration:

```json
{
  "mcpServers": {
    "youtube-notes": {
      "command": "python",
      "args": [
        "C:\\Users\\YourUsername\\mcp-servers\\youtube-lecture-notes\\server.py"
      ],
      "env": {
        "OBSIDIAN_VAULT_PATH": "C:\\Users\\YourUsername\\Documents\\ObsidianVault"
      }
    }
  }
}
```

**IMPORTANT:** Replace the paths with YOUR actual paths:
- `server.py` path → Where you saved the server file
- `OBSIDIAN_VAULT_PATH` → Your Obsidian vault location

**Note:** Use double backslashes `\\` in the JSON file!

### Step 4: Restart Claude Desktop

Close and reopen Claude Desktop for changes to take effect.

---

## Usage Examples

Once set up, just talk to Claude naturally!

### Example 1: Python Tutorial
```
Hey Claude, process this Python tutorial for me:
https://www.youtube.com/watch?v=XXXXX

Capture screenshots at: 2:30, 8:15, 15:00, 22:45
This is Day 1 of my Python learning journey.
```

### Example 2: Video Editing Course
```
Process this Premiere Pro lecture:
https://www.youtube.com/watch?v=XXXXX

Timestamps: 1:20, 5:00, 12:30, 18:00, 25:00
Day 5
```

### Example 3: Preview Subtitles First
```
Can you get the subtitles for this video first so I can see what's covered?
https://www.youtube.com/watch?v=XXXXX
```

### Example 4: Custom Organization
```
Configure my paths:
- Vault: D:\MyNotes\Obsidian
- Notes folder: Learning/Web Development
- Images folder: Learning/Web Development/screenshots
```

---

## What Gets Created

### 1. Note File (in your notes folder)
```
Day 01 - Complete Python Course for Beginners.md
```

### 2. Screenshots (in your images folder)
```
day1_videoID_1_150s.jpg
day1_videoID_2_495s.jpg
...
```

### 3. Note Structure

```markdown
---
date: 2026-01-16
day: 1
tags: [lecture, video-notes, learning]
video: "https://youtube.com/..."
---

# Day 1: Complete Python Course for Beginners

> **Source**: [Channel Name](url)
> **Duration**: 45:30
> **Study Date**: 2026-01-16

---

## 📋 Summary
[Auto-generated transcript summary]

---

## 📝 Key Concepts & Notes

### Timestamp 02:30
![[Lecture Notes/images/day1_xxx_1_150s.jpg]]

**Context from lecture:**
> [Subtitle text around this timestamp]

**Key Points:**
- [Fill in your notes here]

---

[More timestamps...]

---

## 🔑 Key Terms & Definitions
| Term | Definition |
|------|------------|
|  |  |

---

## ✅ Review Questions
1.
2.
3.

---

## 💭 Personal Notes & Observations

---

<details>
<summary>📜 Full Transcript</summary>
[Complete video transcript with timestamps]
</details>
```

---

## Troubleshooting

### "python is not recognized"
- Reinstall Python and check "Add to PATH"
- Or use full path: `C:\\Python312\\python.exe`

### "ffmpeg is not recognized"
- Install ffmpeg using one of the methods above
- Restart your terminal after installation
- Verify: `ffmpeg -version`

### "No subtitles found"
- The video might not have subtitles/captions enabled
- Try a different video to test
- Check if subtitles are available on YouTube

### Screenshots not capturing
- Make sure ffmpeg is properly installed
- Check if the video is available in your region
- Some videos may have download restrictions

### MCP not connecting in Claude
- Check the paths in `claude_desktop_config.json`
- Make sure to use double backslashes `\\`
- Restart Claude Desktop after config changes
- Check Claude Desktop logs for errors

---

## File Organization

After setup, your Obsidian vault will look like:

```
ObsidianVault/
├── Lecture Notes/
│   ├── Day 01 - Python Basics.md
│   ├── Day 02 - Functions and Loops.md
│   ├── Day 03 - Object Oriented Programming.md
│   └── images/
│       ├── day1_xxx_1_150s.jpg
│       ├── day1_xxx_2_495s.jpg
│       ├── day2_xxx_1_300s.jpg
│       └── ...
```

You can customize the folder structure using the `configure_paths` tool!

---

## Tips for Best Results

1. **Watch the video first** on 2x speed to identify key moments
2. **Use the subtitle preview** to find where important topics start
3. **Pick 4-6 timestamps** per video for major concepts
4. **Fill in the "Key Points"** section after watching
5. **Complete the review questions** to test yourself later
6. **Customize tags** to organize by topic (python, excel, photoshop, etc.)

---

## How Claude Uses This Tool

Claude AI has access to comprehensive instructions in [CLAUDE.md](CLAUDE.md) that guide it to:
- Help you choose optimal timestamps by analyzing transcripts
- Suggest best practices for note organization
- Guide you through custom configurations
- Provide topic-specific advice (programming vs. creative vs. academic content)

You can simply ask Claude naturally, and it will use the MCP tools effectively.

---

## Additional Resources

- 📖 **[README.md](README.md)** - Project overview and quick start
- 🤖 **[CLAUDE.md](CLAUDE.md)** - Detailed instructions for Claude AI
- 📝 **[EXAMPLE_NOTE.md](EXAMPLE_NOTE.md)** - Sample note template
- 🎨 **[CUSTOMIZATION.md](CUSTOMIZATION.md)** - Customize notes to your learning style

---

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all prerequisites are installed
3. Double-check your config paths
4. Review [CLAUDE.md](CLAUDE.md) for usage best practices
5. Open an issue on GitHub

---

## License

MIT License - Feel free to use and modify!
