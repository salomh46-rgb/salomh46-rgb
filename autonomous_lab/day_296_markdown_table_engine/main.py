"""
Dynamic Markdown & ASCII Table Engine
Author: Javohirbek Asqarov (Jasper) & Autonomous AI Engine
"""

from typing import List, Dict, Any

class MarkdownTableEngine:
    """
    Renders structured tabular data into beautifully aligned GitHub-Flavored Markdown tables.
    """
    @staticmethod
    def render(headers: List[str], rows: List[List[Any]]) -> str:
        if not headers:
            return ""

        str_headers = [str(h) for h in headers]
        str_rows = [[str(cell) for cell in row] for row in rows]

        col_widths = [len(h) for h in str_headers]
        for row in str_rows:
            for i, cell in enumerate(row):
                if i < len(col_widths):
                    col_widths[i] = max(col_widths[i], len(cell))

        # Format header
        header_line = "| " + " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(str_headers)) + " |"
        separator_line = "| " + " | ".join("-" * col_widths[i] for i in range(len(str_headers))) + " |"

        # Format rows
        row_lines = []
        for row in str_rows:
            padded_row = [row[i].ljust(col_widths[i]) if i < len(row) else "".ljust(col_widths[i]) for i in range(len(str_headers))]
            row_lines.append("| " + " | ".join(padded_row) + " |")

        return "\n".join([header_line, separator_line] + row_lines)
