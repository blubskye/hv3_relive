#!/usr/bin/env python3
"""
Automated Tcl_Size fixer for Tcl 9.0 compatibility
Fixes int → Tcl_Size type mismatches in Tcl API calls
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple

def find_function_variables(content: str, func_name: str, param_index: int) -> List[Tuple[str, int]]:
    """Find variables passed to specific Tcl function parameters"""
    issues = []

    # Pattern to match function calls
    pattern = rf'{func_name}\s*\([^)]*&(\w+)[^)]*\)'

    for match in re.finditer(pattern, content):
        var_name = match.group(1)
        # Find the declaration of this variable
        # Look backwards from the function call
        content_before = content[:match.start()]

        # Look for variable declaration
        decl_patterns = [
            rf'int\s+{var_name}\s*[;=]',
            rf'int\s+{var_name}\s*,',
        ]

        for decl_pattern in decl_patterns:
            if re.search(decl_pattern, content_before):
                line_num = content[:match.start()].count('\n') + 1
                issues.append((var_name, line_num))
                break

    return issues

def fix_file(filepath: Path) -> bool:
    """Fix Tcl_Size issues in a single file"""
    try:
        content = filepath.read_text()
        original_content = content
        changes_made = False

        # Functions that need Tcl_Size* parameters
        tcl_size_funcs = [
            'Tcl_GetStringFromObj',
            'Tcl_ListObjGetElements',
            'Tcl_SplitList',
        ]

        # Find all variables that need to be changed
        vars_to_fix = set()
        for func in tcl_size_funcs:
            issues = find_function_variables(content, func, 2)
            for var_name, line_num in issues:
                vars_to_fix.add(var_name)
                print(f"  Line {line_num}: Variable '{var_name}' used with {func}")

        # Fix variable declarations
        for var_name in vars_to_fix:
            # Pattern to match: int varname [=;,]
            patterns = [
                (rf'\bint\s+({var_name})\s*;', r'Tcl_Size \1;'),
                (rf'\bint\s+({var_name})\s*,', r'Tcl_Size \1,'),
                (rf'\bint\s+({var_name})\s*=', r'Tcl_Size \1 ='),
            ]

            for pattern, replacement in patterns:
                new_content = re.sub(pattern, replacement, content)
                if new_content != content:
                    content = new_content
                    changes_made = True
                    print(f"    Fixed declaration of: {var_name}")

        if changes_made:
            filepath.write_text(content)
            return True

    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

    return False

def main():
    src_dir = Path("/home/blubskye/Downloads/h3vmodern/htmlwidget/src")

    print("=== Automated Tcl_Size Fixer ===\n")

    if not src_dir.exists():
        print(f"Error: Source directory not found: {src_dir}")
        return 1

    c_files = list(src_dir.glob("*.c"))
    print(f"Found {len(c_files)} C files to check\n")

    fixed_count = 0
    for c_file in sorted(c_files):
        print(f"Checking: {c_file.name}")
        if fix_file(c_file):
            fixed_count += 1
            print(f"  ✓ Fixed\n")
        else:
            print(f"  - No changes needed\n")

    print(f"=== Summary ===")
    print(f"Files modified: {fixed_count}/{len(c_files)}")
    print(f"\nRun 'make' to test compilation")

    return 0

if __name__ == "__main__":
    sys.exit(main())
