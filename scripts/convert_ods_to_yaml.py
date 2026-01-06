#!/usr/bin/env python3
"""
Convert Libraries.ods to structured YAML entry files.

This script reads the Libraries.ods spreadsheet and converts each entry
into the YAML format expected by generate_readme.py.

The ODS file uses a 1-3 rating scale, which is converted to 1-5 scale
by multiplying by 5/3 and rounding to the nearest integer.
"""

import pandas as pd
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
import re

# ODS file location
ODS_FILE = Path(__file__).parent.parent / 'Libraries.ods'
LINKS_DIR = Path(__file__).parent.parent / 'links'

# Category mapping based on Overview sheet structure
# Format: (start_row, end_row, directory_name, category_title)
CATEGORIES = [
    (2, 11, 'zkp', 'Zero-Knowledge Libraries',
     'Libraries focused on zero-knowledge proofs, including proof systems, cryptographic primitives, and ZK-specific constructs.'),
    (13, 16, 'zkp-circuits', 'Zero-Knowledge Circuit Frameworks',
     'Frameworks and DSLs for writing zero-knowledge circuits and constraint systems.'),
    (18, 24, 'communication-didcomm', 'Communication Protocols - DIDComm',
     'Libraries implementing DIDComm protocols for secure, privacy-preserving communication in decentralized identity systems.'),
    (26, 29, 'communication-oid4vc', 'Communication Protocols - OpenID for Verifiable Credentials',
     'Implementations of OpenID4VC and OpenID4VP protocols for issuing and verifying credentials.'),
    (31, 36, 'vc-formats', 'Verifiable Credential Formats',
     'Libraries supporting various VC formats including SD-JWT, mDoc/CBOR, and W3C VC Data Model implementations.'),
]

# Evaluation criteria mapping (ODS row index to YAML field name)
CRITERIA_MAPPING = {
    1: 'software_structure',
    2: 'unit_tests_ci_cd',
    3: 'license_ownership',
    4: 'amenity_to_change',
    5: 'documentation',
    6: 'probable_support',
}


def convert_rating_1_3_to_1_5(rating: float) -> int:
    """Convert rating from 1-3 scale to 1-5 scale."""
    if pd.isna(rating) or rating == 0:
        return 3  # Default to middle value if missing

    # Convert 1-3 to 1-5 by multiplying by 5/3
    converted = rating * (5.0 / 3.0)

    # Round to nearest integer and clamp to 1-5 range
    result = max(1, min(5, round(converted)))
    return result


def sanitize_filename(name: str) -> str:
    """Convert name to valid filename (kebab-case)."""
    # Remove special characters and convert to lowercase
    name = re.sub(r'[^\w\s-]', '', name.lower())
    # Replace spaces and underscores with hyphens
    name = re.sub(r'[\s_]+', '-', name)
    # Remove duplicate hyphens
    name = re.sub(r'-+', '-', name)
    # Strip leading/trailing hyphens
    name = name.strip('-')
    return name


def read_overview(ods_file: Path) -> pd.DataFrame:
    """Read the Overview sheet."""
    df = pd.read_excel(ods_file, sheet_name='Overview', engine='odf')
    return df


def read_entry_criteria(ods_file: Path, sheet_name: str) -> Optional[Dict[str, int]]:
    """Read evaluation criteria from an entry sheet."""
    try:
        df = pd.read_excel(ods_file, sheet_name=sheet_name, engine='odf', header=None)

        criteria = {}
        for row_idx, yaml_field in CRITERIA_MAPPING.items():
            if row_idx < len(df):
                rating = df.iloc[row_idx, 1]  # Column 1 contains ratings
                criteria[yaml_field] = convert_rating_1_3_to_1_5(rating)
            else:
                criteria[yaml_field] = 3  # Default value

        return criteria
    except Exception as e:
        print(f"Warning: Could not read criteria from sheet '{sheet_name}': {e}")
        # Return default criteria
        return {field: 3 for field in CRITERIA_MAPPING.values()}


def get_category_for_row(row_idx: int) -> Optional[tuple]:
    """Get category info for a given row index in Overview sheet."""
    for start, end, dir_name, title, description in CATEGORIES:
        if start <= row_idx <= end:
            return (dir_name, title, description)
    return None


def create_yaml_entry(row: pd.Series, row_idx: int, sheet_name: str) -> Optional[Dict[str, Any]]:
    """Create a YAML entry dictionary from an Overview row and its corresponding sheet."""
    # Skip rows without a name
    if pd.isna(row['Name']) or str(row['Name']).strip() == '':
        return None

    # Get category
    category_info = get_category_for_row(row_idx)
    if category_info is None:
        print(f"Warning: Row {row_idx} ('{row['Name']}') does not belong to any category, skipping")
        return None

    # Read evaluation criteria from the entry's individual sheet
    criteria = read_entry_criteria(ODS_FILE, sheet_name)

    # Build YAML entry
    entry = {
        'name': str(row['Name']).strip(),
        'organization': str(row['Organization']).strip() if pd.notna(row['Organization']) else 'Unknown',
        'url': str(row['URL']).strip() if pd.notna(row['URL']) else '',
        'language': str(row['Language']).strip() if pd.notna(row['Language']) else 'Unknown',
        'purpose': str(row['Purpose']).strip() if pd.notna(row['Purpose']) else '',
        'evaluation_criteria': criteria,
    }

    # Add optional note field
    if pd.notna(row['Note']) and str(row['Note']).strip():
        entry['note'] = str(row['Note']).strip()

    return entry, category_info[0]  # Return entry and directory name


def create_directory_structure():
    """Create the links/ directory structure with README files."""
    LINKS_DIR.mkdir(exist_ok=True)

    for start, end, dir_name, title, description in CATEGORIES:
        category_dir = LINKS_DIR / dir_name
        category_dir.mkdir(exist_ok=True)

        # Create README.md for this category
        readme_path = category_dir / 'README.md'
        readme_content = f"""## {title}

{description}
"""
        readme_path.write_text(readme_content)
        print(f"Created {readme_path}")


def main():
    """Main conversion function."""
    print("Converting Libraries.ods to YAML entries...")
    print(f"Reading from: {ODS_FILE}")
    print(f"Writing to: {LINKS_DIR}")
    print()

    # Create directory structure
    create_directory_structure()
    print()

    # Read overview
    df_overview = read_overview(ODS_FILE)

    # Get all sheet names to find entry sheets
    xls = pd.ExcelFile(ODS_FILE, engine='odf')
    entry_sheets = {name: name for name in xls.sheet_names if name not in ['Overview', 'xx_placeholder']}

    # Process each row in overview
    entries_by_category = {cat[1]: [] for cat in CATEGORIES}  # category dir_name -> list of entries

    for idx, row in df_overview.iterrows():
        # Try to find corresponding sheet
        # Sheet names are like "1_Arkworks-crypto-primitives", "2_mattrglobal-crypto", etc.
        sheet_name = None
        for possible_sheet in entry_sheets.keys():
            # Match by checking if the name appears in the sheet name
            if pd.notna(row['Name']):
                name_normalized = str(row['Name']).lower().replace(' ', '').replace('-', '').replace('_', '')
                sheet_normalized = possible_sheet.lower().replace(' ', '').replace('-', '').replace('_', '')
                if name_normalized in sheet_normalized or sheet_normalized.endswith(name_normalized):
                    sheet_name = possible_sheet
                    break

        if sheet_name is None:
            # Try matching by number prefix
            for possible_sheet in entry_sheets.keys():
                if possible_sheet.startswith(f"{idx-1}_") or possible_sheet.startswith(f"{idx}_"):
                    sheet_name = possible_sheet
                    break

        if sheet_name is None:
            print(f"Warning: Could not find sheet for row {idx}: {row['Name']}")
            continue

        # Create YAML entry
        result = create_yaml_entry(row, idx, sheet_name)
        if result is None:
            continue

        entry, category_dir = result

        # Generate filename
        filename = sanitize_filename(entry['name']) + '.yaml'
        file_path = LINKS_DIR / category_dir / filename

        # Write YAML file
        with open(file_path, 'w') as f:
            yaml.dump(entry, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

        print(f"Created: {file_path}")

    print()
    print("Conversion complete!")
    print(f"Created entries in {LINKS_DIR}")
    print()
    print("Next steps:")
    print("1. Review the generated YAML files")
    print("2. Update scripts/generate_readme.py to include the new table directories")
    print("3. Run: python3 scripts/generate_readme.py")


if __name__ == '__main__':
    main()
