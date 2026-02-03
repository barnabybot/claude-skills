---
name: seat-monitor
description: Monitor airline seat availability and find the best seats for flights. Use when the user wants to check seat maps, find premium/good seats, monitor for seat availability changes, or get seat recommendations based on SeatGuru ratings. Supports Cathay Pacific (priority), with extensible architecture for other airlines.
---

# Seat Monitor Skill

## Purpose

This skill helps find and monitor airline seat availability:
- Fetch seat maps from airline websites (browser automation)
- Cross-reference with SeatGuru seat ratings
- Identify best available seats by preference (window, aisle, legroom, recline)
- Monitor for seat availability changes
- Alert when preferred seats become available

## When to Use This Skill

- User asks to "check seat availability" or "find good seats"
- User wants to "monitor seats" for upcoming flights
- User asks about "best seats" on a specific aircraft/route
- User mentions seat preferences (legroom, window, quiet, etc.)
- User wants to know which seats to avoid (bad recline, galley, lavatory)
- User has a flight booking and wants to optimize seating

## Supported Airlines

| Airline | Status | Method | Notes |
|---------|--------|--------|-------|
| Cathay Pacific | ✅ Full | Browser automation | Requires booking reference |
| United | 🔜 Planned | Browser automation | Coming soon |
| British Airways | 🔜 Planned | Browser automation | Coming soon |
| American Airlines | 🔜 Planned | Browser automation | Coming soon |

## Required Information

To check seats, you need:
1. **Booking reference** (PNR) - e.g., "F8HM27"
2. **Last name** - for authentication
3. **Airline** - which carrier to check

## Workflow

### 1. Check Current Seat Map

```bash
# Check seat availability for a Cathay Pacific flight
python scripts/check_seats.py \
  --airline cathay \
  --pnr F8HM27 \
  --lastname ROBSON
```

### 2. Get SeatGuru Ratings

```bash
# Get seat ratings for a specific aircraft
python scripts/seatguru.py \
  --airline "Cathay Pacific" \
  --aircraft "A350-1000" \
  --cabin business
```

### 3. Find Best Available Seats

```bash
# Cross-reference availability with ratings
python scripts/find_best.py \
  --airline cathay \
  --pnr F8HM27 \
  --lastname ROBSON \
  --preference window \
  --min-rating 4
```

### 4. Monitor for Changes

```bash
# Set up monitoring (runs via cron)
python scripts/monitor.py \
  --airline cathay \
  --pnr F8HM27 \
  --lastname ROBSON \
  --target-seats "11A,11K,12A,12K" \
  --notify
```

## SeatGuru Data

### Rating Scale
- **5 (Green)**: Best seats - extra legroom, favorable location
- **4 (Light Green)**: Good seats - no issues
- **3 (Yellow)**: Mixed - some trade-offs
- **2 (Orange)**: Below average - some issues
- **1 (Red)**: Avoid - limited recline, noise, proximity to lavatory

### Seat Attributes
- `legroom`: Extra, Standard, Limited
- `recline`: Full, Limited, None
- `window`: True window, No window, Misaligned
- `proximity`: Galley, Lavatory, Exit, Bulkhead
- `width`: Standard, Narrow, Extra wide
- `power`: AC, USB, None
- `storage`: Standard, Limited, Extra

### Pre-loaded Aircraft Data

Common aircraft configurations are in `data/`:
- `cathay_a350-1000.json` - Cathay A350-1000 seat map & ratings
- `cathay_777-300er.json` - Cathay 777-300ER seat map & ratings

## Browser Automation

The skill uses browser automation to access airline seat maps:

### Cathay Pacific Flow
1. Navigate to cathaypacific.com/managebooking
2. Enter booking reference and last name
3. Click "Manage Booking"
4. Navigate to seat selection
5. Parse seat map HTML for availability
6. Extract seat status (available, occupied, blocked, selected)

### Browser Requirements
- Uses OpenClaw's browser tool with `profile="openclaw"`
- Headless Chromium in sandbox
- Handles cookie consent and login flows

## Example Usage

### Check Seats for Upcoming Flight

User: "Check what seats are available on my CX784 flight next week"

Claude will:
1. Get booking details (PNR: F8HM27, flight: CX784 Feb 12)
2. Use browser to access Cathay manage booking
3. Navigate to seat map
4. Parse available seats
5. Cross-reference with SeatGuru ratings for A330-300
6. Report best available options

### Find Best Window Seat

User: "Find me the best window seat available on my HKG-SFO flight"

Claude will:
1. Identify flight and booking reference
2. Load SeatGuru ratings for the aircraft type
3. Check current seat availability
4. Filter for window seats
5. Rank by SeatGuru rating
6. Recommend top 3 options with reasons

### Monitor for Premium Seats

User: "Let me know if 11A or 11K opens up on my upcoming Cathay flight"

Claude will:
1. Record monitoring request
2. Set up periodic check (via cron or heartbeat)
3. Compare availability against baseline
4. Alert when target seats become available

## Output Format

### Seat Map Summary
```
SEAT AVAILABILITY - CX784 (A350-1000)
=====================================
Business Class:

Row 11: [A:✅] [C:❌] [D:❌] [G:❌] [H:❌] [K:✅]
Row 12: [A:❌] [C:❌] [D:✅] [G:❌] [H:✅] [K:❌]
Row 14: [A:✅] [C:✅] [D:❌] [G:✅] [H:✅] [K:✅]

Legend: ✅ Available | ❌ Occupied | 🔒 Blocked

BEST AVAILABLE (by SeatGuru rating):
1. 11A - ⭐⭐⭐⭐⭐ Window, extra storage, quiet
2. 11K - ⭐⭐⭐⭐⭐ Window, extra storage, quiet
3. 14A - ⭐⭐⭐⭐ Window, standard
```

### Monitoring Alert
```
🎫 SEAT ALERT - CX784 Feb 12

Seat 11A is now AVAILABLE!
Rating: ⭐⭐⭐⭐⭐
Notes: Window seat, forward cabin, extra storage space

[Select this seat now on cathaypacific.com]
```

## Configuration

Create `config.json` for persistent settings:

```json
{
  "default_airline": "cathay",
  "preferences": {
    "seat_type": "window",
    "min_rating": 4,
    "avoid": ["lavatory", "galley", "limited_recline"]
  },
  "monitoring": {
    "check_interval_hours": 4,
    "notify_channel": "whatsapp"
  },
  "bookings": [
    {
      "pnr": "F8HM27",
      "lastname": "ROBSON",
      "airline": "cathay",
      "flights": ["CX784"]
    }
  ]
}
```

## Limitations

- **Authentication**: Requires valid booking reference
- **Rate limits**: Avoid checking too frequently (>1x per hour)
- **Airline changes**: Seat maps may change without notice
- **SeatGuru accuracy**: Ratings may be outdated for reconfigured aircraft
- **Paid seats**: Some seats may require purchase (not reflected in basic availability)

## Extending to New Airlines

To add a new airline:
1. Create `scripts/airlines/<airline>_seats.py`
2. Implement `get_seat_map(pnr, lastname)` function
3. Add aircraft configs to `data/<airline>_<aircraft>.json`
4. Update airline list in this skill doc

## Related Skills

- **gog** - Check calendar for flight times
- **email-processor** - Parse e-ticket emails for booking details
