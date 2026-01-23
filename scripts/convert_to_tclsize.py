#!/usr/bin/env python3
"""
Convert int to Tcl_Size throughout Tkhtml3 codebase.

This script intelligently identifies size-related int variables and converts
them to Tcl_Size for Tcl 9.0 compatibility.
"""

import re
import sys
import os
from pathlib import Path

# Patterns that indicate a variable is size-related and should use Tcl_Size
SIZE_PATTERNS = [
    r'\blength\b', r'\blen\b', r'\bcount\b', r'\bcnt\b',
    r'\bsize\b', r'\bn[A-Z]', r'\bnum\b', r'\bindex\b',
    r'\bidx\b', r'\boffset\b', r'\bwidth\b', r'\bheight\b',
    r'\bnBytes\b', r'\bnChars\b', r'\bnItems\b', r'\bnElements\b',
    r'\bnArgs\b', r'\bnObj\b', r'\biOffset\b', r'\biLeft\b',
    r'\biRight\b', r'\biTop\b', r'\biBottom\b', r'\biWidth\b',
    r'\biHeight\b', r'\bnChild\b', r'\bnProp\b', r'\bnConf\b',
    r'\bnP\b', r'\bnData\b', r'\bnIn\b', r'\bnOut\b',
    r'\bnInput\b', r'\bnOutput\b', r'\bnStyleText\b',
]

# Variables that should NOT be converted (error codes, flags, etc.)
EXCLUDE_PATTERNS = [
    r'\brc\b', r'\bret\b', r'\bresult\b', r'\berror\b',
    r'\bflag\b', r'\bflags\b', r'\bstatus\b', r'\bstate\b',
    r'\btype\b', r'\bkind\b', r'\bmode\b', r'\boption\b',
    r'\beType\b', r'\biType\b', r'\beState\b',
]

def is_size_related(var_name):
    """Check if variable name indicates it's size-related."""
    # Check exclude patterns first
    for pattern in EXCLUDE_PATTERNS:
        if re.search(pattern, var_name, re.IGNORECASE):
            return False

    # Check if matches size patterns
    for pattern in SIZE_PATTERNS:
        if re.search(pattern, var_name, re.IGNORECASE):
            return True

    # Check for common loop counters
    if re.match(r'^[ijk]$', var_name):
        return True

    # Check for 'n' followed by uppercase (nItems, nCount, etc.)
    if re.match(r'^n[A-Z]', var_name):
        return True

    return False

def convert_function_params(content):
    """Convert function parameters from int to Tcl_Size."""
    changes = []

    # Pattern: function parameters like "int length," or "int count)"
    def replace_param(match):
        full_match = match.group(0)
        var_name = match.group(1)

        if is_size_related(var_name):
            replacement = full_match.replace('int ' + var_name, 'Tcl_Size ' + var_name)
            if replacement != full_match:
                changes.append(f"  - Parameter: int {var_name} → Tcl_Size {var_name}")
            return replacement
        return full_match

    # Match function parameters: "int varname," or "int varname)"
    pattern = r'\bint\s+(\w+)\s*[,)]'
    content = re.sub(pattern, replace_param, content)

    return content, changes

def convert_local_variables(content):
    """Convert local variable declarations from int to Tcl_Size."""
    changes = []

    # Pattern: "int length;" or "int i, j, k;"
    def replace_local(match):
        full_match = match.group(0)
        var_names = match.group(1)

        # Split by comma to get individual variable names
        vars_list = [v.strip().split('[')[0].split('=')[0].strip()
                     for v in var_names.split(',')]

        # Check if any variable is size-related
        should_convert = any(is_size_related(v) for v in vars_list)

        if should_convert:
            replacement = full_match.replace('int ', 'Tcl_Size ')
            if replacement != full_match:
                changes.append(f"  - Local var: int {var_names} → Tcl_Size {var_names}")
            return replacement
        return full_match

    # Match local declarations: "int var1, var2;"
    pattern = r'\bint\s+([^;]+);'
    content = re.sub(pattern, replace_local, content)

    return content, changes

def convert_struct_fields(content):
    """Convert structure fields from int to Tcl_Size."""
    changes = []

    # Pattern: struct field "int length;"
    def replace_field(match):
        indent = match.group(1)
        var_name = match.group(2)
        rest = match.group(3)

        if is_size_related(var_name):
            changes.append(f"  - Struct field: int {var_name} → Tcl_Size {var_name}")
            return f"{indent}Tcl_Size {var_name}{rest}"
        return match.group(0)

    # Match struct fields with proper indentation
    pattern = r'(\s+)int\s+(\w+)(\s*;|\s*\[)'
    content = re.sub(pattern, replace_field, content)

    return content, changes

def convert_for_loops(content):
    """Convert for loop counters from int to Tcl_Size."""
    changes = []

    # Pattern: "for (int i = 0; ...)"
    def replace_loop(match):
        var_name = match.group(1)
        rest = match.group(2)

        if is_size_related(var_name):
            changes.append(f"  - Loop counter: int {var_name} → Tcl_Size {var_name}")
            return f"for (Tcl_Size {var_name}{rest}"
        return match.group(0)

    pattern = r'for\s*\(\s*int\s+(\w+)([^)]*\))'
    content = re.sub(pattern, replace_loop, content)

    return content, changes

def process_file(filepath):
    """Process a single C source file."""
    print(f"\nProcessing: {filepath}")

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    original_content = content
    all_changes = []

    # Apply conversions
    content, changes = convert_function_params(content)
    all_changes.extend(changes)

    content, changes = convert_local_variables(content)
    all_changes.extend(changes)

    content, changes = convert_struct_fields(content)
    all_changes.extend(changes)

    content, changes = convert_for_loops(content)
    all_changes.extend(changes)

    if content != original_content:
        # Write back to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"  ✓ Modified ({len(all_changes)} changes)")
        for change in all_changes:
            print(change)
        return len(all_changes)
    else:
        print(f"  - No changes needed")
        return 0

def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
    else:
        target_dir = "../htmlwidget/src"

    src_dir = Path(target_dir)
    if not src_dir.exists():
        print(f"Error: Directory not found: {src_dir}")
        sys.exit(1)

    print(f"Converting int to Tcl_Size in: {src_dir}")
    print("=" * 70)

    # Process all .c files
    c_files = sorted(src_dir.glob("*.c"))
    total_changes = 0

    for c_file in c_files:
        changes = process_file(c_file)
        total_changes += changes

    # Process all .h files
    h_files = sorted(src_dir.glob("*.h"))
    for h_file in h_files:
        changes = process_file(h_file)
        total_changes += changes

    print("\n" + "=" * 70)
    print(f"Conversion complete! Total changes: {total_changes}")
    print("\nNext steps:")
    print("1. Review the changes with: git diff")
    print("2. Rebuild: cd ../build-tkhtml && make")
    print("3. Test: ./run-hv3.sh")

if __name__ == "__main__":
    main()
