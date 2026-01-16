# 🎨 Customization Guide

Make the YouTube Lecture Notes MCP work **your way**! This guide shows you how to customize everything from note structure to formatting to match your personal learning style.

---

## Table of Contents

- [Quick Customization](#quick-customization)
- [Modifying the Note Template](#modifying-the-note-template)
- [Topic-Specific Templates](#topic-specific-templates)
- [Advanced Obsidian Integration](#advanced-obsidian-integration)
- [Folder Organization Strategies](#folder-organization-strategies)
- [Tag Systems](#tag-systems)
- [Custom Sections](#custom-sections)
- [Styling with CSS](#styling-with-css)

---

## Quick Customization

### Change Default Tags

**Location**: `server.py` line 257

**Default**:
```python
tags: [lecture, video-notes, learning]
```

**Examples**:

For programming:
```python
tags: [programming, tutorial, code]
```

For academic:
```python
tags: [university, course, study]
```

For creative:
```python
tags: [creative, tutorial, skills]
```

---

### Change Default Folders

**Location**: `server.py` lines 28-29

**Default**:
```python
DEFAULT_NOTES_FOLDER = "Lecture Notes"
DEFAULT_IMAGES_FOLDER = "Lecture Notes/images"
```

**Examples**:

By topic:
```python
DEFAULT_NOTES_FOLDER = "Learning/Python"
DEFAULT_IMAGES_FOLDER = "Learning/Python/media"
```

By year:
```python
DEFAULT_NOTES_FOLDER = "2026/Courses"
DEFAULT_IMAGES_FOLDER = "2026/Courses/assets"
```

---

### Customize Heading Emojis

**Location**: `server.py` lines 269-327

**Find and replace** emojis to match your style:

| Section | Default | Alternative Options |
|---------|---------|---------------------|
| Summary | 📋 | 📖 💡 🎯 ✍️ |
| Key Concepts | 📝 | 💎 🔑 ⭐ 📌 |
| Terms | 🔑 | 📚 📖 🎓 💡 |
| Review Questions | ✅ | ❓ 🧪 📝 💭 |
| Personal Notes | 💭 | 🧠 💡 ✨ 📓 |
| Transcript | 📜 | 📄 📋 📃 📰 |

---

## Modifying the Note Template

The note template is defined in the `generate_notes()` function in `server.py` (lines 233-349).

### Basic Structure

```python
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
```

### Example: Minimal Template

Replace lines 254-271 with:

```python
note = f"""# {title}

**Date**: {today} | **Day**: {day_number}
**Source**: {video_url}

## Notes

"""
```

### Example: Academic Template

```python
note = f"""---
date: {today}
course: [Your Course Code]
lecture: {day_number}
professor: [{channel}]
tags: [university, {course_code}, lecture-notes]
---

# Lecture {day_number}: {title}

**Course**: [Your Course Name]
**Date**: {today}
**Duration**: {format_timestamp(duration)}
**Textbook Chapter**: [Fill in]

---

## Learning Objectives

-
-
-

## Key Concepts

"""
```

### Example: Professional Development Template

```python
note = f"""---
created: {today}
skill: [Skill Name]
instructor: {channel}
progress: Day {day_number}
tags: [professional-dev, upskilling, career]
---

# {title}

🎯 **Learning Goal**: [What you want to achieve]
⏱️ **Time Investment**: {format_timestamp(duration)}
📅 **Completed**: {today}

---

## Executive Summary

**What I'll Learn**:
-

**Immediate Applications**:
-

---

## Detailed Notes

"""
```

---

## Topic-Specific Templates

### 💻 Programming Template

Add code-specific sections to lines 278-301:

```python
note += """## 🔧 Setup & Prerequisites

**Required**:
-
-

**Optional**:
-

---

## 💻 Code Examples

"""

# Then for each timestamp:
note += f"""### {ts_formatted} - [Topic Name]

![[{obsidian_img_link}]]

**Code**:
```python
# Your code here
```

**Explanation**:
> {context[:500]}

**Key Points**:
-

**Common Errors**:
-

---

"""

# Add at the end:
note += """## 🐛 Debugging Tips

-

## 📚 Documentation Links

-

## 🚀 Next Steps / Practice

- [ ]
- [ ]

"""
```

---

### 🎨 Creative Software Template

```python
note += """## 🎨 Project Overview

**Software**: [Software Name]
**Version**:
**Project Files**:

---

## ⌨️ Keyboard Shortcuts

| Action | Shortcut | Notes |
|--------|----------|-------|
|        |          |       |

---

## 🛠️ Tools & Techniques

"""

# For each timestamp:
note += f"""### {ts_formatted} - [Technique Name]

![[{obsidian_img_link}]]

**Tool Settings**:
-
-

**Workflow**:
1.
2.
3.

**Tips & Tricks**:
-

---

"""

# Add at the end:
note += """## 🎬 Project Ideas

- [ ]
- [ ]

## 💡 Creative Inspiration

-

"""
```

---

### 📊 Business/Productivity Template

```python
note += """## 🎯 Key Takeaways

-
-
-

---

## 📈 Frameworks & Models

"""

# For each timestamp:
note += f"""### {ts_formatted} - [Framework Name]

![[{obsidian_img_link}]]

**Framework Overview**:
> {context[:500]}

**When to Use**:
-

**Steps**:
1.
2.
3.

**Example Application**:
-

---

"""

# Add at the end:
note += """## 📋 Action Items

- [ ]
- [ ]

## 🔗 Resources & Templates

-

## 📊 Metrics to Track

-

"""
```

---

### 🔬 Academic/Science Template

```python
note += """## 🎓 Learning Objectives

By the end of this lecture, I should be able to:
- [ ]
- [ ]

---

## 📐 Formulas & Equations

| Formula | Variables | Application |
|---------|-----------|-------------|
|         |           |             |

---

## 🔬 Key Concepts

"""

# For each timestamp:
note += f"""### {ts_formatted} - [Concept Name]

![[{obsidian_img_link}]]

**Definition**:
> {context[:500]}

**Formula**:
```
[LaTeX or plain text formula]
```

**Derivation**:
1.
2.

**Applications**:
-

**Common Mistakes**:
-

---

"""

# Add at the end:
note += """## 🧮 Practice Problems

1.
   - Solution:

2.
   - Solution:

## 🔗 Related Concepts

- [[Concept 1]]
- [[Concept 2]]

## 📖 Further Reading

-

"""
```

---

## Advanced Obsidian Integration

### Using Dataview for Dynamic Notes

Add to your note frontmatter:
```yaml
---
type: lecture-note
status: in-progress
topic: python
difficulty: beginner
estimated-time: 4h
completed: false
---
```

Then create a dashboard note with Dataview queries:
````markdown
## 📊 Learning Dashboard

### In Progress
```dataview
TABLE day as "Day", difficulty as "Level", estimated-time as "Duration"
FROM #lecture
WHERE status = "in-progress"
SORT day ASC
```

### By Topic
```dataview
TABLE count(rows) as "Count"
FROM #lecture
GROUP BY topic
```
````

---

### Using Templater for Post-Processing

Create an Obsidian template that runs after note generation:

```markdown
<%*
// Auto-fill course information
const course = await tp.system.prompt("Course name?");
tR += `**Course**: ${course}\n`;

// Add study session tracking
const duration = await tp.system.prompt("Study time (minutes)?");
tR += `**Study Duration**: ${duration} min\n`;
%>
```

---

### Creating Wiki-Links Automatically

Modify `server.py` to automatically link common terms:

```python
# Add this function:
def add_wiki_links(text, terms_to_link):
    """Convert terms to wiki-links"""
    for term in terms_to_link:
        text = text.replace(term, f"[[{term}]]")
    return text

# Then in generate_notes():
common_terms = ["Python", "OOP", "function", "class", "variable"]
note_with_links = add_wiki_links(note, common_terms)
```

---

## Folder Organization Strategies

### Strategy 1: By Topic

```
ObsidianVault/
├── Programming/
│   ├── Python/
│   │   ├── Basics/
│   │   ├── Intermediate/
│   │   └── Advanced/
│   └── JavaScript/
├── Design/
│   ├── Photoshop/
│   └── Illustrator/
└── Business/
    └── Excel/
```

**Configure**:
```python
# Ask Claude:
"Configure paths:
- Notes folder: Programming/Python/Basics
- Images folder: Programming/Python/Basics/images"
```

---

### Strategy 2: By Course/Series

```
ObsidianVault/
├── 2026-Courses/
│   ├── Python-Complete-Course/
│   │   ├── Week-1/
│   │   ├── Week-2/
│   │   └── assets/
│   └── Web-Development-Bootcamp/
│       ├── Section-1-HTML/
│       └── Section-2-CSS/
```

---

### Strategy 3: By Date

```
ObsidianVault/
├── 2026/
│   ├── January/
│   │   ├── Week-1/
│   │   └── Week-2/
│   └── February/
└── 2025/
```

---

### Strategy 4: Zettelkasten Method

```
ObsidianVault/
├── 0-Inbox/           # New unprocessed notes
├── 1-Fleeting/        # Quick captures
├── 2-Literature/      # Lecture notes (generated here)
├── 3-Permanent/       # Processed atomic notes
└── 4-Projects/        # Project-specific
```

---

## Tag Systems

### Hierarchical Tags

```yaml
tags:
  - topic/programming/python
  - difficulty/beginner
  - format/video-lecture
  - status/in-progress
  - session/2026-01-16
```

### Flat Tags with Conventions

```yaml
tags: [py-basics, vid-lecture, day-01, 4hrs, freeCodeCamp]
```

### MOC (Map of Content) Tags

```yaml
tags: [lecture, MOC-Python-Learning, resource]
```

---

## Custom Sections

### Adding a "Prerequisites" Section

In `server.py`, after line 272, add:

```python
note += """## 📚 Prerequisites

**Before watching, you should know**:
-
-

**Recommended prior videos**:
-

---

"""
```

---

### Adding a "Timestamp Quick Reference"

After line 277, add:

```python
note += """## ⏱️ Timestamp Quick Reference

"""

for i, ts in enumerate(timestamps, 1):
    ts_formatted = format_timestamp(ts)
    note += f"- **{ts_formatted}** - [Fill in topic]\n"

note += "\n---\n\n"
```

---

### Adding a "Spaced Repetition Schedule"

At the end, before the transcript, add:

```python
note += f"""## 🔄 Review Schedule

- [ ] **Day 1** ({today}): Initial learning ✅
- [ ] **Day 2** ({tomorrow}): Quick review
- [ ] **Day 7**: Practice exercises
- [ ] **Day 30**: Deep review
- [ ] **Day 90**: Final consolidation

---

"""
```

---

## Styling with CSS

Create a CSS snippet in Obsidian: `.obsidian/snippets/lecture-notes.css`

### Example: Colored Sections

```css
/* Color-code different sections */
.markdown-preview-section h2:contains("Summary") {
    color: #4CAF50;
}

.markdown-preview-section h2:contains("Key Concepts") {
    color: #2196F3;
}

.markdown-preview-section h2:contains("Review Questions") {
    color: #FF9800;
}
```

### Example: Highlight Video Timestamp Links

```css
/* Style screenshot captions */
.markdown-preview-section img + p {
    font-size: 0.9em;
    color: #666;
    font-style: italic;
}

/* Style blockquotes (context from lecture) */
blockquote {
    border-left: 4px solid #4CAF50;
    background: #f5f5f5;
    padding: 10px;
}
```

### Example: Custom Frontmatter Display

```css
/* Hide frontmatter in reading mode */
.frontmatter {
    display: none;
}

/* Or style it nicely */
.frontmatter {
    background: #f8f9fa;
    border: 1px solid #dee2e6;
    border-radius: 4px;
    padding: 10px;
    margin-bottom: 20px;
}
```

---

## Complete Customization Example

### Scenario: Data Science Student

**Goal**: Create notes optimized for Python data science tutorials with code, datasets, and visualizations.

**Steps**:

1. **Modify server.py tags** (line 257):
```python
tags: [data-science, python, tutorial, jupyter]
```

2. **Add custom sections** (after line 272):
```python
note += """## 📊 Dataset Information

**Dataset Name**:
**Source**:
**Size**:
**Features**:

---

## 📦 Libraries Used

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
```

---

## 💻 Code & Analysis

"""
```

3. **Modify timestamp sections** (lines 283-301) to include code blocks:
```python
note += f"""### {ts_formatted} - [Analysis Step]

![[{obsidian_img_link}]]

**Objective**:
> {context[:300]}

**Code**:
```python
# Code from this section
```

**Output**:
```
[Expected output]
```

**Interpretation**:
-

---

"""
```

4. **Add custom end sections**:
```python
note += """## 📈 Results & Insights

**Key Findings**:
-

**Visualizations**:
- ![[plot1.png]]

---

## 🔬 Further Analysis Ideas

- [ ]
- [ ]

## 📁 Project Files

- **Notebook**: `analysis.ipynb`
- **Data**: `dataset.csv`
- **Figures**: `results/`

"""
```

5. **Configure folder structure**:
```
Tell Claude: "Configure paths:
- Vault: D:/DataScience/Obsidian
- Notes folder: Projects/Tutorials
- Images folder: Projects/Tutorials/figures"
```

**Result**: Perfectly customized notes for data science learning!

---

## Tips & Best Practices

### Start Simple
1. Use default template initially
2. Identify what you don't use
3. Add what you're missing
4. Iterate gradually

### Keep Consistency
- Use the same structure for similar topics
- Standardize your tags
- Create naming conventions

### Version Control
- Keep backups of your `server.py` customizations
- Document your changes
- Use git to track template evolution

### Community Templates
- Share your templates with others
- Browse community examples
- Adapt what works for you

---

## Getting Help

**Questions about customization?**
- Open an issue with the `customization` label
- Share your template ideas in Discussions
- Check [CLAUDE.md](CLAUDE.md) for AI-assisted customization

---

**Remember**: The best note system is the one you'll actually use. Start with defaults, customize gradually, and make it yours! 🎨
