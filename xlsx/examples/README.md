# XLSX Examples

Sample Python scripts for common Excel operations using openpyxl.

## Files

| Example | Description |
|---------|-------------|
| `create_report.py` | Generate a formatted report with headers, data, and totals |
| `read_and_filter.py` | Read existing workbook, filter rows, write results |
| `multi_sheet.py` | Create workbook with multiple sheets and cross-references |

## Requirements

```bash
pip install openpyxl
```

## Quick Start

```python
from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws['A1'] = 'Hello'
ws['B1'] = 'World'
wb.save('output.xlsx')
```
