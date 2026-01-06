#!/usr/bin/env python3
"""
Generate README.md from YAML entry files.

This script reads YAML entry files from configured table directories,
validates them, and generates a comprehensive README.md file with
tables showing all entries and their quality evaluations.

Usage:
    python generate_readme.py [--validate-only] [--verbose]
"""

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

try:
    import yaml
except ImportError:
    print(
        "ERROR: PyYAML is required. Install with: pip install pyyaml", file=sys.stderr
    )
    sys.exit(1)


# === CONFIGURATION ===
TABLE_DIRECTORIES = [
    "links/zkp",
    "links/zkp-circuits",
    "links/communication-didcomm",
    "links/vc-formats",
]  # Explicit list - update as new tables are added
REQUIRED_FIELDS = ["name", "organization", "url", "language", "purpose"]
OPTIONAL_FIELDS = ["note"]
EVALUATION_CRITERIA = [
    "software_structure",
    "unit_tests_ci_cd",
    "license_ownership",
    "amenity_to_change",
    "documentation",
    "probable_support",
]

# Repository root directory
REPO_ROOT = Path(__file__).parent.parent
HEADER_FILE = REPO_ROOT / "HEADER.md"
FOOTER_FILE = REPO_ROOT / "FOOTER.md"
README_FILE = REPO_ROOT / "README.md"


# === DATA STRUCTURES ===
class ValidationError:
    """Represents a validation error."""

    def __init__(self, file_path: Path, field: str, message: str):
        self.file_path = file_path
        self.field = field
        self.message = message

    def __str__(self) -> str:
        return f"{self.file_path.name}: {self.field} - {self.message}"


class Entry:
    """Represents a single entry from YAML file."""

    def __init__(self, file_path: Path, data: Dict[str, Any]):
        self.file_path = file_path
        self.data = data
        self._quality_score: Optional[float] = None

    @property
    def name(self) -> str:
        return self.data.get("name", "")

    @property
    def organization(self) -> str:
        return self.data.get("organization", "")

    @property
    def url(self) -> str:
        return self.data.get("url", "")

    @property
    def language(self) -> str:
        return self.data.get("language", "")

    @property
    def purpose(self) -> str:
        return self.data.get("purpose", "")

    @property
    def note(self) -> str:
        return self.data.get("note", "")

    @property
    def quality_score(self) -> float:
        """Calculate quality score (cached)."""
        if self._quality_score is None:
            criteria = self.data.get("evaluation_criteria", {})
            values = [criteria.get(c, 0) for c in EVALUATION_CRITERIA]
            self._quality_score = sum(values) / len(values) if values else 0.0
        return self._quality_score

    def to_table_row(self) -> str:
        """Convert entry to markdown table row."""
        name_linked = f"[{escape_table_cell(self.name)}]({self.url})"
        org = escape_table_cell(self.organization)
        lang = escape_table_cell(self.language)
        purpose = escape_table_cell(truncate_text(self.purpose, 200))
        quality = f"{self.quality_score:.1f}/5.0"
        note = escape_table_cell(truncate_text(self.note, 150))

        return f"| {name_linked} | {org} | {lang} | {purpose} | {quality} | {note} |"


# === VALIDATION ===
def validate_entry(file_path: Path, data: Dict[str, Any]) -> List[ValidationError]:
    """Validate a single entry. Returns list of ValidationErrors."""
    errors = []

    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(
                ValidationError(file_path, field, "Field is required but missing")
            )
        elif not data[field] or (
            isinstance(data[field], str) and not data[field].strip()
        ):
            errors.append(
                ValidationError(file_path, field, "Field is required but empty")
            )

    # Validate URL format
    if "url" in data and data["url"]:
        try:
            result = urlparse(data["url"])
            if not all([result.scheme, result.netloc]):
                errors.append(
                    ValidationError(
                        file_path, "url", f"Invalid URL format: {data['url']}"
                    )
                )
        except Exception as e:
            errors.append(
                ValidationError(file_path, "url", f"URL parsing error: {str(e)}")
            )

    # Check evaluation criteria
    if "evaluation_criteria" not in data:
        errors.append(
            ValidationError(
                file_path, "evaluation_criteria", "Section is required but missing"
            )
        )
    else:
        criteria = data["evaluation_criteria"]
        if not isinstance(criteria, dict):
            errors.append(
                ValidationError(
                    file_path, "evaluation_criteria", "Must be a dictionary"
                )
            )
        else:
            # Check all required criteria are present
            for criterion in EVALUATION_CRITERIA:
                if criterion not in criteria:
                    errors.append(
                        ValidationError(
                            file_path,
                            f"evaluation_criteria.{criterion}",
                            "Criterion is required but missing",
                        )
                    )
                else:
                    value = criteria[criterion]
                    # Check if integer
                    if not isinstance(value, int):
                        errors.append(
                            ValidationError(
                                file_path,
                                f"evaluation_criteria.{criterion}",
                                f"Must be integer 1-5, got {type(value).__name__}: {value}",
                            )
                        )
                    # Check if in range 1-5
                    elif value < 1 or value > 5:
                        errors.append(
                            ValidationError(
                                file_path,
                                f"evaluation_criteria.{criterion}",
                                f"Must be integer 1-5, got {value}",
                            )
                        )

    return errors


def check_duplicates(entries: List[Entry]) -> List[ValidationError]:
    """Check for duplicate entry names within a table."""
    errors = []
    names_seen = {}

    for entry in entries:
        name_lower = entry.name.lower()
        if name_lower in names_seen:
            other_entry = names_seen[name_lower]
            errors.append(
                ValidationError(
                    entry.file_path,
                    "name",
                    f'Duplicate name "{entry.name}" found in {entry.file_path.name} and {other_entry.file_path.name}',
                )
            )
        else:
            names_seen[name_lower] = entry

    return errors


# === FILE OPERATIONS ===
def load_yaml_files(directory: Path) -> List[Entry]:
    """Load all YAML files from directory."""
    entries = []
    yaml_files = list(directory.glob("*.yaml")) + list(directory.glob("*.yml"))

    for yaml_file in yaml_files:
        try:
            with open(yaml_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                if data is None:
                    data = {}
                entries.append(Entry(yaml_file, data))
        except yaml.YAMLError as e:
            line_info = (
                f" at line {e.problem_mark.line + 1}"
                if hasattr(e, "problem_mark") and e.problem_mark
                else ""
            )
            print(
                f"ERROR: {yaml_file.name}: YAML syntax error{line_info}",
                file=sys.stderr,
            )
            print(f"  {str(e)}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(
                f"ERROR: {yaml_file.name}: Failed to read file: {str(e)}",
                file=sys.stderr,
            )
            sys.exit(1)

    return entries


def read_markdown_file(file_path: Path) -> str:
    """Read a markdown file or return empty string if missing."""
    if not file_path.exists():
        return ""

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"WARNING: Failed to read {file_path}: {str(e)}", file=sys.stderr)
        return ""


# === MARKDOWN GENERATION ===
def escape_table_cell(text: str) -> str:
    """Escape special characters for markdown tables."""
    if not text:
        return ""
    # Replace pipe characters
    text = text.replace("|", "\\|")
    # Replace newlines with spaces
    text = text.replace("\n", " ").replace("\r", " ")
    # Trim whitespace
    return text.strip()


def truncate_text(text: str, max_length: int) -> str:
    """Truncate text to maximum length with ellipsis."""
    if not text:
        return ""
    text = text.strip()
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."


def generate_table(entries: List[Entry]) -> str:
    """Generate markdown table from entries."""
    if not entries:
        return "*No entries yet.*\n"

    # Sort entries by name (case-insensitive)
    sorted_entries = sorted(entries, key=lambda e: e.name.lower())

    # Generate table header
    table_lines = [
        "| Name | Organization | Language | Purpose | Quality | Note |",
        "|------|--------------|----------|---------|---------|------|",
    ]

    # Generate table rows
    for entry in sorted_entries:
        table_lines.append(entry.to_table_row())

    return "\n".join(table_lines) + "\n"


# === MAIN GENERATION ===
def generate_readme(
    table_dirs: List[str], validate_only: bool = False, verbose: bool = False
) -> bool:
    """
    Main generation logic.

    Returns True if successful, False if validation errors found.
    """
    if verbose:
        print(f"Repository root: {REPO_ROOT}")
        print(f"Table directories: {table_dirs}")

    # Collect all validation errors first
    all_errors = []
    all_entries_by_table = {}

    for table_dir_name in table_dirs:
        table_dir = REPO_ROOT / table_dir_name

        if not table_dir.exists() or not table_dir.is_dir():
            print(
                f"ERROR: Table directory '{table_dir_name}' does not exist",
                file=sys.stderr,
            )
            return False

        # Check for README.md in table directory
        table_readme = table_dir / "README.md"
        if not table_readme.exists():
            print(
                f"ERROR: Table directory '{table_dir_name}' missing README.md",
                file=sys.stderr,
            )
            return False

        # Load YAML entries
        if verbose:
            print(f"Loading entries from {table_dir_name}/...")

        entries = load_yaml_files(table_dir)

        if verbose:
            print(f"  Found {len(entries)} entries")

        # Validate each entry
        for entry in entries:
            errors = validate_entry(entry.file_path, entry.data)
            all_errors.extend(errors)

        # Check for duplicates
        duplicate_errors = check_duplicates(entries)
        all_errors.extend(duplicate_errors)

        all_entries_by_table[table_dir_name] = entries

    # Report all validation errors
    if all_errors:
        print(
            f"\nValidation failed with {len(all_errors)} error(s):\n", file=sys.stderr
        )
        for error in all_errors:
            print(f"  {error}", file=sys.stderr)
        return False

    if verbose or validate_only:
        total_entries = sum(len(entries) for entries in all_entries_by_table.values())
        print(f"\n✓ Validation passed! {total_entries} entries validated successfully.")

    if validate_only:
        return True

    # Generate README content
    if verbose:
        print("\nGenerating README.md...")

    readme_parts = []

    # Add header
    header_content = read_markdown_file(HEADER_FILE)
    if header_content:
        readme_parts.append(header_content)
        if not header_content.endswith("\n"):
            readme_parts.append("\n")

    # Add tables for each directory
    for table_dir_name in table_dirs:
        table_readme = REPO_ROOT / table_dir_name / "README.md"
        table_readme_content = read_markdown_file(table_readme)

        if table_readme_content:
            readme_parts.append("\n")
            readme_parts.append(table_readme_content)
            if not table_readme_content.endswith("\n"):
                readme_parts.append("\n")

        readme_parts.append("\n")

        entries = all_entries_by_table[table_dir_name]
        table = generate_table(entries)
        readme_parts.append(table)

    # Add footer
    footer_content = read_markdown_file(FOOTER_FILE)
    if footer_content:
        readme_parts.append("\n")
        readme_parts.append(footer_content)
        if not footer_content.endswith("\n"):
            readme_parts.append("\n")

    # Write README atomically (temp file + rename)
    final_content = "".join(readme_parts)
    temp_file = README_FILE.with_suffix(".tmp")

    try:
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(final_content)

        # Atomic rename
        temp_file.replace(README_FILE)

        if verbose:
            print(f"✓ README.md generated successfully ({len(final_content)} bytes)")

        return True
    except Exception as e:
        print(f"ERROR: Failed to write README.md: {str(e)}", file=sys.stderr)
        if temp_file.exists():
            temp_file.unlink()
        return False


# === CLI ===
def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate README.md from YAML entry files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_readme.py
  python generate_readme.py --validate-only
  python generate_readme.py --verbose
        """,
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only validate entries without generating README",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )

    args = parser.parse_args()

    success = generate_readme(
        TABLE_DIRECTORIES, validate_only=args.validate_only, verbose=args.verbose
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
