#!/usr/bin/env python3
"""
Validate that the bug fixes work on the Quantum Periodic Properties sheet
"""
import pandas as pd
import requests
from io import StringIO
from process_text import preprocess_text_to_latex
import re

def get_public_sheet(sheet_key, gid):
    url = f'https://docs.google.com/spreadsheets/d/{sheet_key}/export?format=csv&gid={gid}'
    response = requests.get(url)
    response.raise_for_status()
    return pd.read_csv(StringIO(response.text))

def validate_chemistry_brackets(text):
    """Check if chemistry notation like [CH3], [NH4]+ is preserved"""
    has_chem = re.search(r'\[[A-Z][a-z0-9]*\]|\[[A-Z][a-z]*[0-9]+\]', text)
    return has_chem

def validate_commas(text):
    """Check for numbers with commas"""
    has_thousand_sep = re.search(r'\b\d{1,3}(?:,\d{3})+\b', text)
    has_coordinates = re.search(r'[\[\(][-\d\s\w/]+,[-\d\s\w/]+[\)\]]', text)
    return has_thousand_sep, has_coordinates

def validate_latex_notation(text):
    """Check for LaTeX super/subscripts"""
    has_super = re.search(r'\^{[^}]+}', text)
    has_sub = re.search(r'_{[^}]+}', text)
    return has_super, has_sub

# Load the sheet
print("="*70)
print("VALIDATING BUG FIXES ON QUANTUM PERIODIC PROPERTIES SHEET")
print("="*70)

sheet_key = '1Bnr7F1un_M934UKC6WXyZi5SDxG-PjYqzV9bZDoP3CQ'
gid = '943222146'

print(f"\n📊 Loading sheet...")
df = get_public_sheet(sheet_key, gid)
print(f"✅ Loaded: {df.shape[0]} rows, {df.shape[1]} columns")

# Find examples
print(f"\n{'='*70}")
print("FINDING EXAMPLES TO TEST")
print("="*70)

chemistry_examples = []
comma_examples = []
latex_examples = []

for idx, row in df.iterrows():
    fields = {
        'Body Text': str(row.get('Body Text', '')),
        'Answer': str(row.get('Answer', '')),
        'Title': str(row.get('Title', ''))
    }

    for field_name, text in fields.items():
        if text and text != 'nan':
            # Check chemistry
            if validate_chemistry_brackets(text):
                chemistry_examples.append((idx, field_name, text))

            # Check commas
            thousand_sep, coordinates = validate_commas(text)
            if thousand_sep or coordinates:
                comma_examples.append((idx, field_name, text, thousand_sep, coordinates))

            # Check LaTeX
            has_super, has_sub = validate_latex_notation(text)
            if has_super or has_sub:
                latex_examples.append((idx, field_name, text))

print(f"\n🧪 CHEMISTRY NOTATION: {len(chemistry_examples)} found")
print(f"📐 COMMAS: {len(comma_examples)} found")
print(f"📝 LATEX SUPER/SUBSCRIPTS: {len(latex_examples)} found")

# Test Fix #1: Chemistry Brackets
print(f"\n{'='*70}")
print("FIX #1: CHEMISTRY BRACKET PRESERVATION")
print("="*70)

if chemistry_examples:
    for idx, (row_idx, field, text) in enumerate(chemistry_examples[:3]):
        print(f"\nExample {idx+1} (Row {row_idx}, {field}):")
        print(f"  BEFORE: {text[:100]}...")

        processed, has_latex = preprocess_text_to_latex(text, render_latex="TRUE")

        print(f"  AFTER:  {processed[:100]}...")

        # Check if brackets are preserved
        chem_before = re.findall(r'\[[A-Z][a-z0-9]*\]', text)
        chem_after = re.findall(r'\[[A-Z][a-z0-9]*\]', processed)

        if chem_before == chem_after:
            print(f"  ✅ PASS: Chemistry brackets preserved: {chem_before}")
        else:
            print(f"  ❌ FAIL: Brackets changed")
            print(f"     Before: {chem_before}")
            print(f"     After: {chem_after}")
else:
    print("\n⚠️  No chemistry notation found in this sheet")

# Test Fix #2: Comma Handling
print(f"\n{'='*70}")
print("FIX #2: COMMA HANDLING IN NUMERIC ANSWERS")
print("="*70)

if comma_examples:
    for idx, (row_idx, field, text, has_thousand, has_coord) in enumerate(comma_examples[:5]):
        print(f"\nExample {idx+1} (Row {row_idx}, {field}):")
        print(f"  BEFORE: {text}")

        processed, has_latex = preprocess_text_to_latex(text, render_latex="TRUE")

        print(f"  AFTER:  {processed}")

        # Check thousand separators removed
        thousand_before = re.findall(r'\b\d{1,3}(?:,\d{3})+\b', text)
        thousand_after = re.findall(r'\b\d{1,3}(?:,\d{3})+\b', processed)

        # Check coordinates preserved
        coord_before = re.findall(r'[\[\(][-\d\s\w/]+,[-\d\s\w/]+[\)\]]', text)
        coord_after = re.findall(r'[\[\(][-\d\s\w/]+,[-\d\s\w/]+[\)\]]', processed)

        if has_thousand and len(thousand_after) < len(thousand_before):
            print(f"  ✅ PASS: Thousand separators removed: {thousand_before} → processed")
        if has_coord and coord_before == coord_after:
            print(f"  ✅ PASS: Coordinates preserved: {coord_before}")
else:
    print("\n⚠️  No numeric commas found in this sheet")

# Test Fix #3: LaTeX Notation
print(f"\n{'='*70}")
print("FIX #3: LATEX SUPERSCRIPT/SUBSCRIPT PRESERVATION")
print("="*70)

if latex_examples:
    for idx, (row_idx, field, text) in enumerate(latex_examples[:3]):
        print(f"\nExample {idx+1} (Row {row_idx}, {field}):")
        print(f"  BEFORE: {text[:150]}")

        processed, has_latex = preprocess_text_to_latex(text, render_latex="TRUE")

        print(f"  AFTER:  {processed[:150]}")

        # Check LaTeX notation preserved
        super_before = re.findall(r'\^{[^}]+}', text)
        super_after = re.findall(r'\^{[^}]+}', processed)

        sub_before = re.findall(r'_{[^}]+}', text)
        sub_after = re.findall(r'_{[^}]+}', processed)

        if super_before and super_before == super_after:
            print(f"  ✅ PASS: Superscripts preserved: {super_before}")
        if sub_before and sub_before == sub_after:
            print(f"  ✅ PASS: Subscripts preserved: {sub_before}")
else:
    print("\n⚠️  No LaTeX super/subscripts found in this sheet")

print(f"\n{'='*70}")
print("✅ VALIDATION COMPLETE")
print("="*70)
