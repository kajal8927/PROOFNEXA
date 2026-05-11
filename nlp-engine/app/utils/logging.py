import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger("proofnexa-nlp")

def log_safe_text(text: str, max_chars: int = 50) -> str:
    """Truncates text for safe logging without exposing full content."""
    if not text:
        return ""
    if len(text) <= max_chars:
        return text
    return f"{text[:max_chars]}... [truncated, total length: {len(text)}]"
