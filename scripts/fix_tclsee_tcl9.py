#!/usr/bin/env python3
"""
Fix Tclsee for Tcl 9.0 compatibility
- Fix int -> Tcl_Size for Tcl_ListObjGetElements calls
"""

import re
from pathlib import Path

file_path = Path("/home/blubskye/Downloads/h3vmodern/tclsee/hv3see.c")

with open(file_path, 'r') as f:
    content = f.read()

# Find all Tcl_ListObjGetElements calls and track variables
pattern = r'Tcl_ListObjGetElements\([^,]+,\s*[^,]+,\s*&(\w+),'
matches = re.findall(pattern, content)

print(f"Found {len(matches)} Tcl_ListObjGetElements calls")
print(f"Variables to fix: {set(matches)}")

# For each variable, find its declaration and change int to Tcl_Size
for var_name in set(matches):
    # Look for: int var_name; or int var_name,
    old_patterns = [
        (rf'\bint\s+{var_name}\s*;', f'Tcl_Size {var_name};'),
        (rf'\bint\s+{var_name}\s*,', f'Tcl_Size {var_name},'),
    ]

    for pattern, replacement in old_patterns:
        new_content = re.sub(pattern, replacement, content)
        if new_content != content:
            print(f"  Fixed: int {var_name}")
            content = new_content
            break

with open(file_path, 'w') as f:
    f.write(content)

print("\nDone!")
