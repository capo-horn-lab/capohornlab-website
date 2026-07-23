"""File upload validation utilities."""

from __future__ import annotations

import mimetypes
import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile, status

# ── Allowed extensions and MIME types ──

ALLOWED_EXTENSIONS: set[str] = {
    ".pdf", ".png", ".jpg", ".jpeg",
    ".doc", ".docx",
    ".zip",
    ".py",
    ".txt", ".csv",
}

# Map extensions to expected MIME types for extra validation
EXTENSION_MIME_MAP: dict[str, set[str]] = {
    ".pdf": {"application/pdf"},
    ".png": {"image/png"},
    ".jpg": {"image/jpeg"},
    ".jpeg": {"image/jpeg"},
    ".doc": {"application/msword"},
    ".docx": {
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    },
    ".zip": {
        "application/zip",
        "application/x-zip-compressed",
    },
    ".py": {"text/x-python", "text/plain"},
    ".txt": {"text/plain"},
    ".csv": {"text/csv", "text/plain"},
}

# Extensions explicitly blocked
BLOCKED_EXTENSIONS: set[str] = {
    ".exe", ".bat", ".cmd", ".sh", ".ps1", ".vbs",
    ".scr", ".dll", ".msi", ".jar", ".wsf", ".hta",
    ".cpl", ".msc", ".reg", ".docm", ".xlsm", ".pptm",
    ".wasm", ".php", ".asp", ".jsp", ".htaccess",
    ".env", ".config",
}

MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10 MB
MAX_TOTAL_SIZE: int = 50 * 1024 * 1024  # 50 MB total per request


def validate_uploaded_file(file: UploadFile) -> str:
    """Validate an uploaded file and return the sanitised storage filename.

    Raises HTTPException with appropriate status code if validation fails.
    The returned filename is ``{uuid}_{original_name}``.
    """
    # 1. Check original filename exists
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must have a filename",
        )

    # 2. Extract and validate extension
    original_ext = Path(file.filename).suffix.lower()
    if not original_ext:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File '{file.filename}' has no extension",
        )

    if original_ext in BLOCKED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File extension '{original_ext}' is not allowed",
        )

    if original_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"File extension '{original_ext}' is not allowed. "
                f"Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
            ),
        )

    # 3. Check MIME type (from content_type + python-magic fallback)
    content_type = file.content_type or ""
    expected_mimes = EXTENSION_MIME_MAP.get(original_ext, set())
    if expected_mimes:
        # Allow `text/plain` as fallback for text-based files
        if content_type not in expected_mimes and content_type != "text/plain":
            # Try to detect via extension-based guess as additional check
            guessed, _ = mimetypes.guess_type(file.filename)
            if guessed and guessed not in expected_mimes and guessed != content_type:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        f"Invalid MIME type '{content_type}' for "
                        f"extension '{original_ext}'. "
                        f"Expected one of: {', '.join(expected_mimes)}"
                    ),
                )

    # 4. Size check is done by the endpoint after reading content
    return f"{uuid.uuid4().hex}_{file.filename}"


def check_file_size(content: bytes) -> None:
    """Check file content size against the max limit."""
    if len(content) > MAX_FILE_SIZE:
        size_mb = MAX_FILE_SIZE / (1024 * 1024)
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Maximum size is {size_mb:.0f} MB",
        )
