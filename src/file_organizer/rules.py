from __future__ import annotations

CATEGORY_EXTENSIONS = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".rtf"},
    "Spreadsheets": {".xls", ".xlsx", ".csv"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Audio": {".mp3", ".wav", ".flac", ".m4a"},
    "Video": {".mp4", ".mkv", ".avi", ".mov", ".webm"},
    "Code": {".py", ".js", ".html", ".css", ".json", ".md"},
}


def category_for_extension(extension: str) -> str:
    extension = extension.lower()

    for category, extensions in CATEGORY_EXTENSIONS.items():
        if extension in extensions:
            return category

    return "Other"
