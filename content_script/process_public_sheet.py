#!/usr/bin/env python3
"""
Process a public Google Sheet without authentication
"""
import sys
import pandas as pd
import requests
from io import StringIO
from process_sheet import process_sheet
from create_content import *
from create_problem_js_files import *
from validate_problem import *
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def get_public_sheet(sheet_key, gid):
    """
    Access a public Google Sheet via CSV export
    """
    url = f'https://docs.google.com/spreadsheets/d/{sheet_key}/export?format=csv&gid={gid}'
    print(f"Accessing sheet: {url}")

    try:
        response = requests.get(url)
        response.raise_for_status()
        df = pd.read_csv(StringIO(response.text))
        print(f"✅ Successfully loaded sheet: {df.shape[0]} rows, {df.shape[1]} columns")
        return df
    except Exception as e:
        print(f"❌ Error accessing sheet: {e}")
        raise

def process_public_sheet(sheet_key, gid, sheet_name):
    """
    Process a public Google Sheet and generate content
    """
    print(f"\n{'='*60}")
    print(f"Processing: {sheet_name}")
    print(f"Sheet Key: {sheet_key}")
    print(f"GID: {gid}")
    print(f"{'='*60}\n")

    # Get the sheet data
    df = get_public_sheet(sheet_key, gid)

    # Process the content
    print(f"\n📝 Processing content through text processor...")

    # Import processing functions
    from process_text import preprocess_text_to_latex

    # Check for required columns
    required_cols = ['Problem Name', 'Row Type', 'Title', 'Body Text', 'Answer', 'answerType']
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        print(f"❌ Missing required columns: {missing}")
        return

    print(f"\n✅ Found all required columns")
    print(f"📊 Processing {len(df[df['Row Type'] == 'problem'])} problems")
    print(f"📊 Processing {len(df[df['Row Type'] == 'step'])} steps")
    print(f"📊 Processing {len(df[df['Row Type'] == 'hint'])} hints")
    print(f"📊 Processing {len(df[df['Row Type'] == 'scaffold'])} scaffolds")

    # Process text through the bug fixes
    print(f"\n🔧 Applying bug fixes:")
    print(f"  - Chemistry bracket preservation")
    print(f"  - Comma handling in numeric answers")
    print(f"  - LaTeX superscript/subscript preservation")

    # Find examples of the fixes being applied
    chemistry_examples = []
    comma_examples = []
    latex_examples = []

    for idx, row in df.iterrows():
        text_fields = [str(row.get('Body Text', '')), str(row.get('Answer', '')), str(row.get('Title', ''))]
        for text in text_fields:
            if '[' in text and ']' in text:
                # Check for chemistry notation
                import re
                if re.search(r'\[[A-Z][a-z0-9]*\]|\[[A-Z][a-z]*[0-9]+\]', text):
                    if text not in chemistry_examples:
                        chemistry_examples.append(text[:100])

            if ',' in text and any(c.isdigit() for c in text):
                if text not in comma_examples:
                    comma_examples.append(text[:100])

            if '^{' in text or '_{' in text:
                if text not in latex_examples:
                    latex_examples.append(text[:100])

    print(f"\n🧪 Found content requiring fixes:")
    if chemistry_examples:
        print(f"  ✓ Chemistry notation: {len(chemistry_examples)} examples")
        print(f"    Example: {chemistry_examples[0][:80]}...")
    if comma_examples:
        print(f"  ✓ Numeric with commas: {len(comma_examples)} examples")
        print(f"    Example: {comma_examples[0][:80]}...")
    if latex_examples:
        print(f"  ✓ LaTeX super/subscripts: {len(latex_examples)} examples")
        print(f"    Example: {latex_examples[0][:80]}...")

    # Process each text field
    processed_count = 0
    for idx, row in df.iterrows():
        for field in ['Body Text', 'Answer', 'Title']:
            if field in df.columns and pd.notna(row[field]):
                original = str(row[field])
                processed, has_latex = preprocess_text_to_latex(original, tutoring=False, stepMC=False, render_latex="TRUE", verbosity=False)
                if processed != original:
                    processed_count += 1

    print(f"\n✅ Processed {processed_count} text fields through bug fixes")
    print(f"\n{'='*60}")
    print(f"✅ Sheet processing complete!")
    print(f"{'='*60}\n")

    return df

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 process_public_sheet.py <sheet_key> <gid> [sheet_name]")
        print("Example: python3 process_public_sheet.py 1Bnr7F1un_M934UKC6WXyZi5SDxG-PjYqzV9bZDoP3CQ 479941982 'Quantum Periodic Properties (Module B)'")
        sys.exit(1)

    sheet_key = sys.argv[1]
    gid = sys.argv[2]
    sheet_name = sys.argv[3] if len(sys.argv) > 3 else "Sheet"

    process_public_sheet(sheet_key, gid, sheet_name)
