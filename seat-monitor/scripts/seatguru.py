#!/usr/bin/env python3
"""
SeatGuru seat ratings fetcher and data provider.
Provides seat quality ratings for airline/aircraft combinations.
"""

import argparse
import json
import os
import sys
from pathlib import Path

# SeatGuru URL patterns
SEATGURU_BASE = "https://www.seatguru.com"
SEATGURU_SEARCH = f"{SEATGURU_BASE}/findseatmap/findseatmap.php"

# Pre-loaded seat ratings data
# Ratings: 5=Best, 4=Good, 3=Mixed, 2=Below Average, 1=Avoid
SEAT_DATA = {
    'cathay_a350-1000_business': {
        'aircraft': 'Airbus A350-1000',
        'airline': 'Cathay Pacific',
        'cabin': 'Business',
        'config': '1-2-1',
        'rows': '11-23',
        'seats': {
            # Row 11 - front of cabin, extra quiet
            '11A': {'rating': 5, 'type': 'window', 'notes': 'Front row window, extra storage, quiet'},
            '11C': {'rating': 4, 'type': 'aisle', 'notes': 'Front row aisle, good access'},
            '11D': {'rating': 4, 'type': 'middle', 'notes': 'Front row, couples seat'},
            '11G': {'rating': 4, 'type': 'middle', 'notes': 'Front row, couples seat'},
            '11H': {'rating': 4, 'type': 'aisle', 'notes': 'Front row aisle, good access'},
            '11K': {'rating': 5, 'type': 'window', 'notes': 'Front row window, extra storage, quiet'},
            
            # Row 12-17 - standard business
            '12A': {'rating': 4, 'type': 'window', 'notes': 'Standard window'},
            '12K': {'rating': 4, 'type': 'window', 'notes': 'Standard window'},
            
            # Row 18 - mini-cabin start, slightly quieter
            '18A': {'rating': 5, 'type': 'window', 'notes': 'Mini-cabin front, extra privacy'},
            '18K': {'rating': 5, 'type': 'window', 'notes': 'Mini-cabin front, extra privacy'},
            
            # Row 23 - last row before galley
            '23A': {'rating': 3, 'type': 'window', 'notes': 'Near galley, some noise'},
            '23K': {'rating': 3, 'type': 'window', 'notes': 'Near galley, some noise'},
        },
        'general_notes': [
            'All business class seats are lie-flat with direct aisle access',
            'Window seats (A/K) have more privacy',
            'Middle seats (D/G) best for couples traveling together',
            'Front rows (11, 18) are quietest',
            'Avoid last rows near galley if noise-sensitive'
        ]
    },
    
    'cathay_777-300er_business': {
        'aircraft': 'Boeing 777-300ER',
        'airline': 'Cathay Pacific',
        'cabin': 'Business',
        'config': '1-2-1',
        'rows': '11-23',
        'seats': {
            '11A': {'rating': 5, 'type': 'window', 'notes': 'Bulkhead window, extra legroom'},
            '11K': {'rating': 5, 'type': 'window', 'notes': 'Bulkhead window, extra legroom'},
            '12A': {'rating': 4, 'type': 'window', 'notes': 'Standard window, true window'},
            '12K': {'rating': 4, 'type': 'window', 'notes': 'Standard window, true window'},
            '17A': {'rating': 3, 'type': 'window', 'notes': 'Window misaligned with seat'},
            '17K': {'rating': 3, 'type': 'window', 'notes': 'Window misaligned with seat'},
            '23A': {'rating': 2, 'type': 'window', 'notes': 'Last row, galley noise, limited recline'},
            '23K': {'rating': 2, 'type': 'window', 'notes': 'Last row, galley noise, limited recline'},
        },
        'general_notes': [
            'Reverse herringbone layout with direct aisle access',
            'Window seats offer most privacy',
            'Some window seats have misaligned windows',
            'Avoid row 23 - galley directly behind'
        ]
    },
    
    'cathay_a330-300_business': {
        'aircraft': 'Airbus A330-300',
        'airline': 'Cathay Pacific',
        'cabin': 'Business',
        'config': '1-2-1',
        'rows': '11-20',
        'seats': {
            '11A': {'rating': 5, 'type': 'window', 'notes': 'Bulkhead, extra space'},
            '11K': {'rating': 5, 'type': 'window', 'notes': 'Bulkhead, extra space'},
            '12A': {'rating': 4, 'type': 'window', 'notes': 'Standard window'},
            '12K': {'rating': 4, 'type': 'window', 'notes': 'Standard window'},
            '20A': {'rating': 3, 'type': 'window', 'notes': 'Last row, near galley'},
            '20K': {'rating': 3, 'type': 'window', 'notes': 'Last row, near galley'},
        },
        'general_notes': [
            'Regional business class product',
            'Used on shorter routes (HKG-BKK, HKG-SIN)',
            'All seats have direct aisle access',
            'Front rows recommended for quick deplaning'
        ]
    }
}


def get_seat_data(airline: str, aircraft: str, cabin: str = 'business') -> dict:
    """
    Get pre-loaded seat data for airline/aircraft/cabin combination.
    
    Args:
        airline: Airline name (e.g., "cathay", "Cathay Pacific")
        aircraft: Aircraft type (e.g., "A350-1000", "777-300ER")
        cabin: Cabin class (e.g., "business", "economy")
    
    Returns:
        dict with seat ratings and notes
    """
    # Normalize inputs
    airline_key = airline.lower().replace(' ', '_').replace('pacific', '').strip('_')
    if 'cathay' in airline.lower():
        airline_key = 'cathay'
    
    aircraft_key = aircraft.lower().replace(' ', '').replace('-', '')
    aircraft_key = aircraft_key.replace('airbus', '').replace('boeing', '').strip()
    
    # Common aircraft name variations
    aircraft_map = {
        'a3501000': 'a350-1000',
        'a350': 'a350-1000',  # default to -1000 for Cathay
        '777300er': '777-300er',
        '773': '777-300er',
        '777': '777-300er',
        'a330300': 'a330-300',
        'a330': 'a330-300',
        '333': 'a330-300',
    }
    aircraft_key = aircraft_map.get(aircraft_key, aircraft_key)
    
    cabin_key = cabin.lower()
    
    # Build lookup key
    lookup_key = f"{airline_key}_{aircraft_key}_{cabin_key}"
    
    if lookup_key in SEAT_DATA:
        return SEAT_DATA[lookup_key]
    
    # Try partial matches
    for key, data in SEAT_DATA.items():
        if airline_key in key and aircraft_key in key:
            return data
    
    return {
        'error': f'No seat data found for {airline} {aircraft} {cabin}',
        'available_configs': list(SEAT_DATA.keys()),
        'suggestion': 'Try fetching from SeatGuru directly'
    }


def get_seat_rating(airline: str, aircraft: str, seat: str, cabin: str = 'business') -> dict:
    """Get rating for a specific seat."""
    data = get_seat_data(airline, aircraft, cabin)
    
    if 'error' in data:
        return data
    
    seat_upper = seat.upper()
    seats = data.get('seats', {})
    
    if seat_upper in seats:
        return {
            'seat': seat_upper,
            'aircraft': data.get('aircraft'),
            **seats[seat_upper]
        }
    
    return {
        'seat': seat_upper,
        'rating': None,
        'notes': 'Seat not in database - likely standard seat'
    }


def rank_available_seats(available_seats: list, airline: str, aircraft: str, 
                         cabin: str = 'business', preference: str = None) -> list:
    """
    Rank available seats by SeatGuru rating.
    
    Args:
        available_seats: List of available seat codes (e.g., ['11A', '12K', '14D'])
        airline: Airline name
        aircraft: Aircraft type
        cabin: Cabin class
        preference: Optional preference filter ('window', 'aisle', 'quiet')
    
    Returns:
        List of seats sorted by rating (best first)
    """
    data = get_seat_data(airline, aircraft, cabin)
    if 'error' in data:
        return [{'seat': s, 'rating': None, 'notes': 'No rating data'} for s in available_seats]
    
    seats_db = data.get('seats', {})
    
    ranked = []
    for seat in available_seats:
        seat_upper = seat.upper()
        if seat_upper in seats_db:
            seat_info = {'seat': seat_upper, **seats_db[seat_upper]}
        else:
            # Default rating for unlisted seats
            seat_info = {
                'seat': seat_upper,
                'rating': 3,  # Assume average
                'type': 'aisle' if seat_upper[-1] in 'CDG' else 'window',
                'notes': 'Standard seat (not in database)'
            }
        ranked.append(seat_info)
    
    # Apply preference filter
    if preference:
        pref_lower = preference.lower()
        if pref_lower in ['window', 'aisle']:
            ranked = [s for s in ranked if s.get('type') == pref_lower] + \
                    [s for s in ranked if s.get('type') != pref_lower]
    
    # Sort by rating (highest first)
    ranked.sort(key=lambda x: x.get('rating', 0), reverse=True)
    
    return ranked


def format_seat_recommendations(ranked_seats: list, top_n: int = 5) -> str:
    """Format ranked seats as readable recommendations."""
    if not ranked_seats:
        return "No seat data available"
    
    output = []
    output.append("\n🎯 SEAT RECOMMENDATIONS (Best → Worst)")
    output.append("=" * 45)
    
    for i, seat in enumerate(ranked_seats[:top_n], 1):
        rating = seat.get('rating', '?')
        stars = '⭐' * rating if isinstance(rating, int) else '❓'
        seat_type = seat.get('type', 'unknown')
        notes = seat.get('notes', '')
        
        output.append(f"\n{i}. Seat {seat['seat']} - {stars}")
        output.append(f"   Type: {seat_type.title()}")
        if notes:
            output.append(f"   Notes: {notes}")
    
    return "\n".join(output)


def fetch_seatguru_data(airline: str, flight: str = None, aircraft: str = None) -> dict:
    """
    Instructions for fetching fresh data from SeatGuru.
    
    This returns browser automation instructions since SeatGuru
    requires JavaScript rendering.
    """
    return {
        'method': 'browser_automation',
        'url': SEATGURU_SEARCH,
        'steps': [
            {'action': 'navigate', 'url': SEATGURU_SEARCH},
            {'action': 'type', 'selector': '#airline', 'text': airline},
            {'action': 'click', 'selector': '.search-btn, button[type="submit"]'},
            {'action': 'wait', 'selector': '.seat-map, .seatmap'},
            {'action': 'snapshot', 'note': 'Parse seat ratings from page'}
        ],
        'notes': [
            'SeatGuru uses heavy JavaScript - browser automation required',
            'Seat colors: Green=Good, Yellow=Mixed, Red=Bad',
            'Hover/click on seats for detailed notes',
            'Consider caching results to avoid repeated fetches'
        ]
    }


def main():
    parser = argparse.ArgumentParser(description='SeatGuru seat ratings')
    parser.add_argument('--airline', required=True, help='Airline name')
    parser.add_argument('--aircraft', help='Aircraft type (e.g., A350-1000)')
    parser.add_argument('--cabin', default='business', help='Cabin class')
    parser.add_argument('--seat', help='Specific seat to look up')
    parser.add_argument('--available', nargs='+', help='List of available seats to rank')
    parser.add_argument('--preference', choices=['window', 'aisle'],
                       help='Seat preference for ranking')
    parser.add_argument('--output', choices=['json', 'text'], default='text',
                       help='Output format')
    
    args = parser.parse_args()
    
    # Specific seat lookup
    if args.seat:
        if not args.aircraft:
            print("Error: --aircraft required for seat lookup", file=sys.stderr)
            sys.exit(1)
        result = get_seat_rating(args.airline, args.aircraft, args.seat, args.cabin)
    
    # Rank available seats
    elif args.available:
        if not args.aircraft:
            print("Error: --aircraft required for ranking", file=sys.stderr)
            sys.exit(1)
        result = rank_available_seats(args.available, args.airline, args.aircraft,
                                      args.cabin, args.preference)
        if args.output == 'text':
            print(format_seat_recommendations(result))
            sys.exit(0)
    
    # Get all seat data for aircraft
    elif args.aircraft:
        result = get_seat_data(args.airline, args.aircraft, args.cabin)
    
    # List available configs
    else:
        result = {
            'available_configurations': list(SEAT_DATA.keys()),
            'usage': 'Provide --aircraft to get seat data'
        }
    
    # Output
    if args.output == 'json':
        print(json.dumps(result, indent=2))
    else:
        if isinstance(result, dict):
            if 'error' in result:
                print(f"Error: {result['error']}")
            elif 'seats' in result:
                print(f"\n{result.get('airline', '')} {result.get('aircraft', '')}")
                print(f"Cabin: {result.get('cabin', '')} | Config: {result.get('config', '')}")
                print(f"Rows: {result.get('rows', '')}")
                print("\nGeneral Notes:")
                for note in result.get('general_notes', []):
                    print(f"  • {note}")
                print(f"\n{len(result.get('seats', {}))} seats in database")
            else:
                print(json.dumps(result, indent=2))
        else:
            print(result)


if __name__ == '__main__':
    main()
