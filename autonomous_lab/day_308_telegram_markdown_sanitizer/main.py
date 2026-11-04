"""
Telegram MarkdownV2 & Entity Safe Sanitizer
Author: Javohirbek Asqarov (Jasper) & Autonomous AI Engine
"""

import re

class TelegramSanitizer:
    """
    Sanitizes raw text to conform with Telegram Bot API MarkdownV2 specifications.
    """
    # Reserved characters in Telegram MarkdownV2: _ * [ ] ( ) ~ ` > # + - = | { } . !
    RESERVED_PATTERN = re.compile(r'([_*\[\]()~`>#+\-=|{}.!\\])')

    @classmethod
    def escape_markdown_v2(cls, text: str) -> str:
        """Escapes all reserved characters with preceding backslash."""
        if not text:
            return ""
        return cls.RESERVED_PATTERN.sub(r'\\\1', text)

    @classmethod
    def format_code_block(cls, code: str, language: str = "") -> str:
        """Safely wraps code within backticks escaping internal backticks."""
        clean_code = code.replace("\\", "\\\\").replace("`", "\\`")
        return f"```{language}\n{clean_code}\n```"
