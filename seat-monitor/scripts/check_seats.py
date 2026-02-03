#!/usr/bin/env python3
"""
Check seat availability for airline bookings via browser automation.
Outputs structured seat map data.
"""

import argparse
import json
import sys
from datetime import datetime

# Airline-specific implementations
AIRLINES = {
    'cathay': {
        'name': 'Cathay Pacific',
        'manage_url': 'https://www.cathaypacific.com/cx/en_HK/manage-booking/manage-booking.html',
        'supported': True
    },
    'united': {
        'name': 'United Airlines',
        'manage_url': 'https://www.united.com/en/us/manageres/mytrips',
        'supported': False
    },
    'ba': {
        'name': 'British Airways',
        'manage_url': 'https://www.britishairways.com/travel/managebooking/public/en_gb',
        'supported': False
    }
}


def check_cathay_seats(pnr: str, lastname: str, browser_func=None) -> dict:
    """
    Check seat availability for Cathay Pacific booking.
    
    This function is designed to be called with OpenClaw's browser automation.
    When called standalone, it outputs browser instructions.
    
    Args:
        pnr: Booking reference (e.g., "F8HM27")
        lastname: Passenger last name
        browser_func: Optional browser automation function
    
    Returns:
        dict with seat map data or browser instructions
    """
    
    instructions = {
        'airline': 'cathay',
        'method': 'browser_automation',
        'steps': [
            {
                'action': 'navigate',
                'url': AIRLINES['cathay']['manage_url']
            },
            {
                'action': 'wait',
                'selector': 'input[name="bookingReference"], input[id="bookingRef"]',
                'timeout': 10000
            },
            {
                'action': 'type',
                'selector': 'input[name="bookingReference"], input[id="bookingRef"]',
                'text': pnr
            },
            {
                'action': 'type', 
                'selector': 'input[name="lastName"], input[id="lastName"]',
                'text': lastname
            },
            {
                'action': 'click',
                'selector': 'button[type="submit"], .retrieve-booking-btn'
            },
            {
                'action': 'wait',
                'selector': '.booking-details, .trip-card',
                'timeout': 15000
            },
            {
                'action': 'snapshot',
                'note': 'Capture booking overview'
            },
            {
                'action': 'click',
                'selector': 'a[href*="seat"], button:has-text("Seat"), .seat-selection-link',
                'note': 'Navigate to seat selection'
            },
            {
                'action': 'wait',
                'selector': '.seat-map, .cabin-layout, svg[class*="seat"]',
                'timeout': 15000
            },
            {
                'action': 'snapshot',
                'note': 'Capture seat map - parse for availability'
            }
        ],
        'parsing': {
            'available_indicators': ['.seat-available', '.seat-free', '[data-status="available"]'],
            'occupied_indicators': ['.seat-occupied', '.seat-taken', '[data-status="occupied"]'],
            'blocked_indicators': ['.seat-blocked', '.seat-unavailable', '[data-status="blocked"]'],
            'selected_indicators': ['.seat-selected', '.seat-current', '[data-status="selected"]']
        },
        'notes': [
            'Cathay may require cookie consent - accept if prompted',
            'Login may be required for some modifications',
            'Seat map is typically in SVG or grid layout',
            'Look for data-seat-id or aria-label for seat identifiers'
        ]
    }
    
    return instructions


def parse_seat_map_html(html: str, airline: str) -> dict:
    """
    Parse seat map HTML to extract availability.
    
    This is a template - actual parsing depends on airline HTML structure.
    """
    # Placeholder - actual implementation would use BeautifulSoup
    # and airline-specific selectors
    return {
        'parsed': False,
        'note': 'HTML parsing requires BeautifulSoup - use browser snapshot instead',
        'raw_html_length': len(html) if html else 0
    }


def format_seat_map(seats: list, cabin: str = 'business') -> str:
    """Format seat data as ASCII seat map."""
    if not seats:
        return "No seat data available"
    
    output = []
    output.append(f"\n{cabin.upper()} CLASS SEAT MAP")
    output.append("=" * 40)
    
    # Group by row
    rows = {}
    for seat in seats:
        row = seat.get('row', '?')
        if row not in rows:
            rows[row] = []
        rows[row].append(seat)
    
    # Sort and display
    for row_num in sorted(rows.keys(), key=lambda x: int(x) if x.isdigit() else 999):
        row_seats = sorted(rows[row_num], key=lambda x: x.get('letter', 'Z'))
        row_str = f"Row {row_num:>2}: "
        
        for seat in row_seats:
            letter = seat.get('letter', '?')
            status = seat.get('status', 'unknown')
            
            if status == 'available':
                icon = '✅'
            elif status == 'occupied':
                icon = '❌'
            elif status == 'blocked':
                icon = '🔒'
            elif status == 'selected':
                icon = '⭐'
            else:
                icon = '❓'
            
            row_str += f"[{letter}:{icon}] "
        
        output.append(row_str)
    
    output.append("")
    output.append("Legend: ✅ Available | ❌ Occupied | 🔒 Blocked | ⭐ Selected")
    
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description='Check airline seat availability')
    parser.add_argument('--airline', required=True, choices=list(AIRLINES.keys()),
                       help='Airline code')
    parser.add_argument('--pnr', required=True, help='Booking reference')
    parser.add_argument('--lastname', required=True, help='Passenger last name')
    parser.add_argument('--output', choices=['json', 'instructions', 'text'],
                       default='instructions', help='Output format')
    
    args = parser.parse_args()
    
    airline_info = AIRLINES.get(args.airline)
    if not airline_info:
        print(f"Error: Unknown airline '{args.airline}'", file=sys.stderr)
        sys.exit(1)
    
    if not airline_info['supported']:
        print(f"Error: {airline_info['name']} not yet supported", file=sys.stderr)
        sys.exit(1)
    
    # Get instructions for browser automation
    if args.airline == 'cathay':
        result = check_cathay_seats(args.pnr, args.lastname)
    else:
        result = {'error': f'No implementation for {args.airline}'}
    
    # Output
    if args.output == 'json':
        print(json.dumps(result, indent=2))
    elif args.output == 'instructions':
        print(f"\n🎫 SEAT CHECK: {airline_info['name']}")
        print(f"Booking: {args.pnr} / {args.lastname}")
        print(f"URL: {airline_info['manage_url']}")
        print("\nBrowser automation steps:")
        for i, step in enumerate(result.get('steps', []), 1):
            action = step.get('action', '?')
            detail = step.get('url') or step.get('selector') or step.get('text') or step.get('note', '')
            print(f"  {i}. {action}: {detail[:60]}...")
        print("\nUse OpenClaw browser tool to execute these steps.")
    else:
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
