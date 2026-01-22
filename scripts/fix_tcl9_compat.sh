#!/bin/bash
#
# Automated Tcl 9.0 Compatibility Fixer
#
# This script automatically fixes remaining Tcl_Size compatibility issues
# in the HV3/Tkhtml3 source code for Tcl 9.0.
#

set -e

HTMLWIDGET_SRC="/home/blubskye/Downloads/h3vmodern/htmlwidget/src"
BACKUP_DIR="/home/blubskye/Downloads/h3vmodern/backups/$(date +%Y%m%d_%H%M%S)"

echo "=== Tcl 9.0 Compatibility Auto-Fixer ==="
echo ""

# Create backup
echo "[1/5] Creating backup of source files..."
mkdir -p "$BACKUP_DIR"
cp -r "$HTMLWIDGET_SRC" "$BACKUP_DIR/"
echo "  Backup created at: $BACKUP_DIR"
echo ""

# Fix #1: Replace Tk_Offset with offsetof in all remaining files
echo "[2/5] Replacing Tk_Offset with offsetof..."
find "$HTMLWIDGET_SRC" -name "*.c" -o -name "*.h" | while read file; do
    if grep -q "Tk_Offset" "$file" 2>/dev/null; then
        echo "  Fixing: $(basename $file)"
        sed -i 's/Tk_Offset/offsetof/g' "$file"
    fi
done
echo ""

# Fix #2: Add stdarg.h include where va_start is used
echo "[3/5] Adding stdarg.h includes where needed..."
find "$HTMLWIDGET_SRC" -name "*.c" | while read file; do
    if grep -q "va_start\|va_end\|va_list" "$file" 2>/dev/null; then
        if ! grep -q "#include <stdarg.h>" "$file" 2>/dev/null; then
            echo "  Adding stdarg.h to: $(basename $file)"
            # Add after other system includes
            sed -i '/#include <assert.h>/a #include <stdarg.h>' "$file"
        fi
    fi
done
echo ""

# Fix #3: Find and report files with Tcl_GetStringFromObj using int*
echo "[4/5] Finding Tcl_GetStringFromObj issues..."
echo "  Files that need manual Tcl_Size fixes:"
find "$HTMLWIDGET_SRC" -name "*.c" -exec grep -l "Tcl_GetStringFromObj" {} \; | while read file; do
    # Check if file has int variables used with Tcl_GetStringFromObj
    if grep -B5 "Tcl_GetStringFromObj" "$file" | grep -q "int n\|int len\|int length"; then
        echo "    - $(basename $file)"
        grep -n "Tcl_GetStringFromObj" "$file" | head -3
    fi
done
echo ""

# Fix #4: Find and report files with Tcl_ListObjGetElements using int*
echo "[5/5] Finding Tcl_ListObjGetElements issues..."
echo "  Files that need manual Tcl_Size fixes:"
find "$HTMLWIDGET_SRC" -name "*.c" -exec grep -l "Tcl_ListObjGetElements" {} \; | while read file; do
    # Check if file has int variables used with Tcl_ListObjGetElements
    if grep -B10 "Tcl_ListObjGetElements" "$file" | grep -q "int n\|int count\|int num"; then
        echo "    - $(basename $file)"
        grep -n "Tcl_ListObjGetElements" "$file" | head -3
    fi
done
echo ""

echo "=== Summary ==="
echo "Automatic fixes applied:"
echo "  ✓ Replaced Tk_Offset with offsetof"
echo "  ✓ Added stdarg.h includes where needed"
echo ""
echo "Manual fixes still required:"
echo "  See lists above for files with Tcl_GetStringFromObj/Tcl_ListObjGetElements"
echo "  These need 'int' variables changed to 'Tcl_Size'"
echo ""
echo "Backup location: $BACKUP_DIR"
echo ""
echo "Next step: Run 'make' to test compilation"
