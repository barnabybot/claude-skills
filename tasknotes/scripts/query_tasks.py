#!/usr/bin/env python3
"""Query TaskNotes and markdown tasks from an Obsidian vault."""

import argparse
import os
import re
import yaml
from datetime import datetime, date
from pathlib import Path
from typing import Optional


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Extract YAML frontmatter from markdown content."""
    if not content.startswith('---'):
        return {}, content
    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}, content
    try:
        fm = yaml.safe_load(parts[1]) or {}
        return fm, parts[2]
    except yaml.YAMLError:
        return {}, content


def parse_date(d) -> Optional[date]:
    """Parse various date formats to date object."""
    if d is None:
        return None
    if isinstance(d, date):
        return d
    if isinstance(d, datetime):
        return d.date()
    if isinstance(d, str):
        for fmt in ['%Y-%m-%d', '%Y/%m/%d', '%d-%m-%Y']:
            try:
                return datetime.strptime(d.split('T')[0], fmt).date()
            except ValueError:
                continue
    return None


def get_tasknotes_tasks(vault_path: Path, filter_type: str = 'all') -> list[dict]:
    """Get tasks from TaskNotes folder."""
    tasks_folder = vault_path / 'TaskNotes' / 'Tasks'
    if not tasks_folder.exists():
        return []

    tasks = []
    today = date.today()

    for md_file in tasks_folder.rglob('*.md'):
        try:
            content = md_file.read_text(encoding='utf-8')
            fm, body = parse_frontmatter(content)

            status = fm.get('status', 'open')
            priority = fm.get('priority', 'normal')
            due = parse_date(fm.get('due'))
            scheduled = parse_date(fm.get('scheduled'))
            title = fm.get('title', md_file.stem)

            # Skip completed tasks unless showing all
            if filter_type != 'all' and status == 'done':
                continue

            task = {
                'type': 'tasknote',
                'title': title,
                'file': str(md_file.relative_to(vault_path)),
                'status': status,
                'priority': priority,
                'due': due,
                'scheduled': scheduled,
                'contexts': fm.get('contexts', []),
                'projects': fm.get('projects', []),
                'overdue': due is not None and due < today and status != 'done',
                'due_today': due is not None and due == today,
                'scheduled_today': scheduled is not None and scheduled <= today,
            }

            # Apply filters
            if filter_type == 'overdue' and not task['overdue']:
                continue
            if filter_type == 'today' and not (task['due_today'] or task['scheduled_today']):
                continue
            if filter_type == 'actionable' and not (
                task['status'] in ['open', 'in-progress'] and
                (task['scheduled'] is None or task['scheduled'] <= today)
            ):
                continue
            if filter_type == 'high-priority' and priority != 'high':
                continue

            tasks.append(task)
        except Exception as e:
            continue

    return tasks


def get_checkbox_tasks(vault_path: Path, filter_type: str = 'all') -> list[dict]:
    """Get checkbox tasks from markdown files (excluding TaskNotes folder)."""
    checkbox_pattern = re.compile(r'^(\s*)- \[([ xX/\-])\]\s+(.+)$', re.MULTILINE)
    date_pattern = re.compile(r'(?:due|by|deadline)[:\s]+(\d{4}-\d{2}-\d{2})', re.IGNORECASE)
    priority_pattern = re.compile(r'(?:priority[:\s]+(\w+)|!!(\w+)|⚠️|🔴|🟡)', re.IGNORECASE)

    tasks = []
    today = date.today()

    # Folders to skip
    skip_folders = {'TaskNotes', '.obsidian', '.trash', 'Templates', 'Attachments'}

    for md_file in vault_path.rglob('*.md'):
        # Skip certain folders
        if any(part in skip_folders for part in md_file.parts):
            continue

        try:
            content = md_file.read_text(encoding='utf-8')
            matches = checkbox_pattern.findall(content)

            for indent, status_char, text in matches:
                is_done = status_char.lower() in ['x', '-']

                # Skip completed unless showing all
                if filter_type != 'all' and is_done:
                    continue

                # Check for due date in task text
                due = None
                due_match = date_pattern.search(text)
                if due_match:
                    due = parse_date(due_match.group(1))

                # Check for priority
                priority = 'normal'
                if '!!' in text or '🔴' in text or 'high' in text.lower():
                    priority = 'high'
                elif '⚠️' in text or '🟡' in text:
                    priority = 'normal'

                task = {
                    'type': 'checkbox',
                    'title': text.strip(),
                    'file': str(md_file.relative_to(vault_path)),
                    'status': 'done' if is_done else 'open',
                    'priority': priority,
                    'due': due,
                    'scheduled': None,
                    'overdue': due is not None and due < today and not is_done,
                    'due_today': due is not None and due == today,
                }

                # Apply filters
                if filter_type == 'overdue' and not task['overdue']:
                    continue
                if filter_type == 'today' and not task['due_today']:
                    continue
                if filter_type == 'high-priority' and priority != 'high':
                    continue
                if filter_type == 'actionable' and is_done:
                    continue

                tasks.append(task)
        except Exception:
            continue

    return tasks


def format_tasks(tasks: list[dict], format_type: str = 'summary') -> str:
    """Format tasks for output."""
    if not tasks:
        return "No tasks found."

    # Sort: overdue first, then by priority, then by due date
    priority_order = {'high': 0, 'normal': 1, 'low': 2, 'none': 3}
    tasks.sort(key=lambda t: (
        not t.get('overdue', False),
        priority_order.get(t.get('priority', 'normal'), 2),
        t.get('due') or date(9999, 12, 31)
    ))

    if format_type == 'json':
        import json
        return json.dumps(tasks, default=str, indent=2)

    lines = []
    for t in tasks:
        status_emoji = {'done': '✅', 'in-progress': '🔄', 'open': '⬜'}.get(t['status'], '⬜')
        priority_emoji = {'high': '🔴', 'normal': '', 'low': '🟢'}.get(t['priority'], '')

        due_str = ''
        if t.get('overdue'):
            due_str = f" ⚠️ OVERDUE (due {t['due']})"
        elif t.get('due_today'):
            due_str = " 📅 TODAY"
        elif t.get('due'):
            due_str = f" (due {t['due']})"

        line = f"{status_emoji} {priority_emoji}{t['title']}{due_str}"
        if format_type == 'detailed':
            line += f"\n   📁 {t['file']}"
        lines.append(line)

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Query tasks from Obsidian vault')
    parser.add_argument('vault_path', help='Path to Obsidian vault')
    parser.add_argument('--filter', choices=['all', 'overdue', 'today', 'actionable', 'high-priority'],
                        default='actionable', help='Filter type')
    parser.add_argument('--source', choices=['all', 'tasknotes', 'checkboxes'],
                        default='all', help='Task source')
    parser.add_argument('--format', choices=['summary', 'detailed', 'json'],
                        default='summary', help='Output format')

    args = parser.parse_args()
    vault_path = Path(args.vault_path).expanduser()

    tasks = []
    if args.source in ['all', 'tasknotes']:
        tasks.extend(get_tasknotes_tasks(vault_path, args.filter))
    if args.source in ['all', 'checkboxes']:
        tasks.extend(get_checkbox_tasks(vault_path, args.filter))

    print(format_tasks(tasks, args.format))


if __name__ == '__main__':
    main()
