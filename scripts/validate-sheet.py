#!/usr/bin/env python3
"""
Easy Sheet Validation Tool

Usage:
    python3 validate-sheet.py <google_sheet_url> [sheet_name]

Examples:
    python3 validate-sheet.py "https://docs.google.com/spreadsheets/d/1ABC123/edit"
    python3 validate-sheet.py "https://docs.google.com/spreadsheets/d/1ABC123/edit" "Sheet1"
"""

import sys
import re
import os
import pandas as pd

def extract_sheet_key(url):
    """Extract sheet key from Google Sheets URL"""
    pattern = r'/spreadsheets/d/([a-zA-Z0-9-_]+)'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def validate_sheet_format(sheet_key, sheet_name=None):
    """Validate Google Sheet format without requiring credentials"""
    try:
        # Try to access the sheet as CSV (works for public sheets)
        if sheet_name:
            # For specific sheet/tab
            csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_key}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
        else:
            # For first sheet
            csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_key}/export?format=csv"

        print(f"📊 Validating sheet: {sheet_key}")
        if sheet_name:
            print(f"📋 Tab: {sheet_name}")

        try:
            df = pd.read_csv(csv_url)
        except Exception as e:
            print(f"❌ Cannot access sheet. Make sure it's publicly viewable or use credentials.")
            print(f"   Error: {e}")
            return False

        if df.empty:
            print("❌ Sheet is empty")
            return False

        print(f"📈 Found {len(df)} rows")

        # Check required headers
        required_headers = [
            "Problem Name", "Row Type", "Title", "Body Text",
            "Answer", "answerType", "HintID", "Dependency",
            "mcChoices", "Images (space delimited)", "Parent",
            "OER src", "openstax KC", "KC", "Taxonomy"
        ]

        missing_headers = [h for h in required_headers if h not in df.columns]

        if missing_headers:
            print("❌ Missing required headers:")
            for header in missing_headers:
                print(f"   - {header}")
            return False

        print("✅ All required headers present")

        # Check for problems without steps
        errors = []
        warnings = []

        if 'Row Type' in df.columns and 'Problem Name' in df.columns:
            problems = df[df['Row Type'] == 'problem']['Problem Name'].dropna().unique()

            for problem in problems:
                problem_rows = df[df['Problem Name'] == problem]
                steps = problem_rows[problem_rows['Row Type'] == 'step']

                if len(steps) == 0:
                    warnings.append(f"Problem '{problem}' has no steps")

        # Check for empty required fields
        for idx, row in df.iterrows():
            if row.get('Row Type') == 'problem' and pd.isna(row.get('Problem Name')):
                errors.append(f"Row {idx + 2}: Problem row missing Problem Name")

            if row.get('Row Type') in ['step', 'scaffold'] and pd.isna(row.get('Answer')):
                warnings.append(f"Row {idx + 2}: Step/scaffold missing answer")

        # Report results
        if errors:
            print(f"❌ Found {len(errors)} errors:")
            for error in errors[:5]:  # Show first 5 errors
                print(f"   - {error}")
            if len(errors) > 5:
                print(f"   ... and {len(errors) - 5} more errors")

        if warnings:
            print(f"⚠️ Found {len(warnings)} warnings:")
            for warning in warnings[:5]:  # Show first 5 warnings
                print(f"   - {warning}")
            if len(warnings) > 5:
                print(f"   ... and {len(warnings) - 5} more warnings")

        if not errors and not warnings:
            print("✅ No issues found!")

        return len(errors) == 0

    except Exception as e:
        print(f"❌ Validation failed: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    sheet_url = sys.argv[1]
    sheet_name = sys.argv[2] if len(sys.argv) > 2 else None

    # Extract sheet key from URL
    sheet_key = extract_sheet_key(sheet_url)

    if not sheet_key:
        print("❌ Invalid Google Sheets URL format")
        print("Expected format: https://docs.google.com/spreadsheets/d/SHEET_ID/...")
        sys.exit(1)

    print("🔍 OATutor Sheet Validator")
    print("=" * 40)

    success = validate_sheet_format(sheet_key, sheet_name)

    print("=" * 40)
    if success:
        print("✅ Validation passed! Sheet format is valid.")
        print("\n💡 To generate content from this sheet:")
        print(f"   cd content_script")
        if sheet_name:
            print(f"   python3 process_sheet.py online {sheet_key} '{sheet_name}'")
        else:
            print(f"   python3 process_sheet.py online {sheet_key}")
    else:
        print("❌ Validation failed. Please fix the issues above.")

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()