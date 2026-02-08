---
name: podcast-transcript
description: "Fetch full podcast transcripts from YouTube, format as Obsidian notes with highlights and key quotes. Use when user wants a podcast transcript, says 'get transcript', 'transcribe podcast', 'full transcript', or references podcast notes they want expanded into full transcripts. Works with any podcast that has a YouTube version."
---

# Podcast Transcript

Fetch podcast transcripts from YouTube and create formatted Obsidian notes in `Clippings/Podcasts/`.

## Vault

`/Users/barnabyrobson/Library/Mobile Documents/iCloud~md~obsidian/Documents/Core`

## Arguments

- `/podcast-transcript` — Interactive: ask which episode
- `/podcast-transcript <file-path>` — Process a user's notes file about an episode (extracts show/guest/topics to find the episode)
- `/podcast-transcript <youtube-url>` — Direct YouTube URL

## Prerequisites

- `yt-dlp` (Homebrew): `which yt-dlp`
- `youtube_transcript_api` (python3.11): `/opt/homebrew/opt/python@3.11/bin/python3.11 -c "from youtube_transcript_api import YouTubeTranscriptApi"`

## Batch Mode

For processing entire folders (e.g., "process all podcasts"), use this workflow instead of per-file:

1. **Close Obsidian first** — per vault CLAUDE.md, Obsidian caches files and silently reverts external changes:
   ```bash
   osascript -e 'quit app "Obsidian"' && sleep 2
   rm -f ".obsidian/workspace.json" ".obsidian/workspace-mobile.json"
   ```

2. **Pre-fetch channel listings** to `/tmp/` files (parallelize all channels):
   ```bash
   yt-dlp --flat-playlist --print "%(id)s|%(title)s|%(upload_date)s" "https://www.youtube.com/@CHANNEL/videos" --playlist-end 200 > /tmp/CHANNEL_videos.txt
   ```

3. **Build a master mapping** (JSON file at `/tmp/`) with: old filename, show, guest, episode, matched yt_id, search hints for unmatched.

4. **Dispatch parallel Opus agents** grouped by show (e.g., Tim Ferriss batch, All-In batch, BG2 batch). Each agent handles: YouTube lookup, transcript download, rename, key quotes, note formatting.

5. **Download transcripts FIRST** before file processing — `youtube_transcript_api` hits IP blocks after ~30-40 requests in quick succession. If blocked (HTTP 429 / IpBlocked), add a `[!info] Transcript unavailable` callout and move on. The file structure is ready for transcript insertion later.

6. **Reopen Obsidian** when all agents complete: `open -a Obsidian`

## Workflow

### 1. Identify the Episode

If given a user notes file, read it to extract: show name, guest(s), key topics discussed.

If given a YouTube URL, extract the video ID directly.

Otherwise, ask the user for show name and episode details.

### 2. Find the YouTube Video ID

**Go straight to yt-dlp channel listing. Do NOT waste rounds on web searches for video IDs.**

```bash
yt-dlp --flat-playlist --print "%(id)s %(title)s %(upload_date)s" "https://www.youtube.com/@CHANNEL/videos" --playlist-end 15
```

#### Known Channel Handles

| Podcast | YouTube Handle | Notes |
|---------|---------------|-------|
| All-In Podcast | `@allin` | Episodes titled with topic list |
| BG2Pod (Gurley & Gerstner) | `@BG2Pod` | |
| Invest Like the Best | `@joincolossus` | **Audio-only for ILTB episodes.** Only Business Breakdowns appears on YouTube. ILTB full episodes are NOT on YouTube — Snipd highlights are often the best available transcript source. |
| Tim Ferriss Show | `@timferriss` | Channel has short clips, not full episodes. Full episodes sometimes on other channels — use `ytsearch` with episode number + guest name. |
| Lex Fridman Podcast | `@lexfridman` | Full episodes available |
| Joe Rogan Experience | `@joerogan` | Full episodes available |
| My First Million | `@MyFirstMillionPod` | |
| 20VC | `@20aboroflove` | May vary |
| The Knowledge Project | `@FarnamStreetBlog` | |
| Acquired | `@AcquiredFM` | |
| WhatIfAltHist | `@WhatIfAltHist` | Rudyard Lynch, history content |
| Founders Podcast | `@FoundersPodcast` | David Senra |
| Y Combinator | `@ycombinator` | Startup advice |
| Odd Lots (Bloomberg) | Search via `ytsearch` | |
| The Drive (Peter Attia) | `@PeterAttiaMD` | |
| In Good Company (Norges Bank) | Search via `ytsearch` | |

**If the channel handle is unknown**: Search with `yt-dlp --flat-playlist --print "%(id)s %(title)s" "ytsearch10:SHOW_NAME GUEST_NAME"`. If ytsearch returns 0 results (it's unreliable), fall back to web search for the channel handle, then use channel listing.

**Verify the match**: For ambiguous results, check metadata:
```bash
yt-dlp --print "%(title)s %(description).200s %(upload_date)s %(duration)s" "https://www.youtube.com/watch?v=VIDEO_ID"
```

### 3. Fetch Transcript

```python
/opt/homebrew/opt/python@3.11/bin/python3.11 -c "
from youtube_transcript_api import YouTubeTranscriptApi
ytt = YouTubeTranscriptApi()
transcript = ytt.fetch('VIDEO_ID')
full_text = '\n'.join([entry.text for entry in transcript])
with open('/tmp/podcast_transcript.txt', 'w') as f:
    f.write(full_text)
print(f'Saved: {len(full_text)} chars, {len(transcript)} segments')
"
```

### 4. Create the Obsidian Note

**Destination**: `Clippings/Podcasts/`

**Naming convention** (universal, date-first for chronological sorting):

`YYYY-MM-DD - Show Name - Guest Name.md`

Examples:
- `2023-09-07 - Tim Ferriss Show - Nassim Taleb & Scott Patterson.md`
- `2024-03-01 - All-In Podcast - E168 Can Google Save Itself, Abolish HR, Reddit IPO.md`
- `2024-06-22 - BG2 Pod - Ep11 Coatue Recap, Tesla ISS Controversy.md`
- `2024-08-13 - WhatIfAltHist - History 102 Ancient Greece.md`
- `2025-06-10 - Invest Like the Best - Bill Gurley.md`

For All-In/BG2, include episode number + brief topic in the guest/title position.

**Dispatch a Task agent** (`mode: dontAsk`, `model: opus`) to process the transcript. The agent needs:
1. The transcript file path
2. The user's notes file path (if one exists, for highlighting)
3. Episode metadata (show, guest, episode number, URL, date)

#### Agent Prompt Template

Provide the agent with:

**Frontmatter** (adapt to show):
```yaml
---
created: YYYY-MM-DD
categories:
  - "[[Podcast episodes]]"
type: "[[Podcasts]]"
topics: [assign 3-6 relevant topics as wikilinks]
show: "[[Show Name]]"
guests:
  - "[[Guest Name]]"
author:
  - "[[Host Name]]"
episode: NNN
url: https://www.youtube.com/watch?v=VIDEO_ID
published: YYYY-MM-DD
rating:
---
```

**Note structure**:

1. `## Key Quotes & Learning Points` — 8-12 blockquotes with attribution. Prioritise quotes matching the user's notes, then add other standout insights.

2. `## Notes` — Preserve the user's existing notes here exactly as they were. If the file has Snipd highlights, keep those too. Always include this section even if empty (for future note-taking).

3. `## Transcript` — Full transcript, cleaned up:
   - Merge short lines into flowing paragraphs
   - Add speaker labels where identifiable (YouTube auto-transcripts use `>>` for speaker changes)
   - `==Highlight==` passages that correspond to the user's notes
   - Add `[[wikilinks]]` on first mention of notable people, companies, concepts
   - Add `---` between major topic shifts

### 5. Verify

After the agent finishes, spot-check:
- Frontmatter is valid YAML
- Highlights exist (search for `==`)
- Key quotes section has content
- File is in `Clippings/Podcasts/`

## Blocked Services

These DO NOT work for podcast discovery. Skip them:
- `WebFetch` on youtube.com, x.com, happyscribe.com — all blocked
- `yt-dlp ytsearch:` — unreliable, often returns 0 results

## Tips

- YouTube auto-transcripts don't label speakers. The agent must infer from context (host intros, topic expertise, voice patterns in text).
- Some podcasts aren't on YouTube (audio-only). For these, note the gap and suggest the user provide a direct transcript or audio file.
- If user has existing notes about the episode, always cross-reference them for highlights — that's the primary value-add over a raw transcript.
