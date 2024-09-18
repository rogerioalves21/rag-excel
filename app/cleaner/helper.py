from typing import Final, List
import re

UNICODE_BULLETS: Final[List[str]] = [
    "\u0095",
    "\u2022",
    "\u2023",
    "\u2043",
    "\u3164",
    "\u204C",
    "\u204D",
    "\u2219",
    "\u25CB",
    "\u25CF",
    "\u25D8",
    "\u25E6",
    "\u2619",
    "\u2765",
    "\u2767",
    "\u29BE",
    "\u29BF",
    "\u002D",
    "",
    r"\*",
    "\x95",
    "·",
]

BULLETS_PATTERN = "|".join(UNICODE_BULLETS)
PARAGRAPH_PATTERN = r"\s*\n\s*"

NEW_PARAGRAPH_PATTERN = r"[\n]{1,}|[\r\n]{1,}"


PARAGRAPH_PATTERN_RE = re.compile(
    f"((?:{BULLETS_PATTERN})|{PARAGRAPH_PATTERN})(?!{BULLETS_PATTERN}|$)",
)
# DOUBLE_PARAGRAPH_PATTERN_RE = re.compile("(" + PARAGRAPH_PATTERN + "){2}")
DOUBLE_PARAGRAPH_PATTERN_RE = NEW_PARAGRAPH_PATTERN

UNICODE_BULLETS_RE = re.compile(f"(?:{BULLETS_PATTERN})(?!{BULLETS_PATTERN})")

E_BULLET_PATTERN = re.compile(r"^e(?=\s)", re.MULTILINE)

TWO_OR_MORE_SPACES_NOT_NEW_LINE = r"[^\S\r\n]{2,}"

UNICODE_BULLETS_RE_0W = re.compile(f"(?={BULLETS_PATTERN})(?<!{BULLETS_PATTERN})")
