#!/bin/bash
#
# Targeted Tcl_Size fixer - only fixes specific known issues
#

cd /home/blubskye/Downloads/h3vmodern/htmlwidget/src

echo "=== Targeted Tcl_Size Fixes ==="
echo ""

# htmltcl.c - Line 1409
echo "[1/3] Fixing htmltcl.c..."
sed -i '1409s/^\(\s*\)int nObj;/\1Tcl_Size nObj;/' htmltcl.c

# htmltcl.c - Line 1673
sed -i '1673s/^\(\s*\)int nHtml;/\1Tcl_Size nHtml;/' htmltcl.c

# htmltcl.c - Line 2186
sed -i '2186s/^\(\s*\)int n;/\1Tcl_Size n;/' htmltcl.c

# Add stdarg.h to htmltcl.c if not present
if ! grep -q "#include <stdarg.h>" htmltcl.c; then
    sed -i '/#include <assert.h>/a #include <stdarg.h>' htmltcl.c
fi

echo "  ✓ htmltcl.c fixed"
echo ""

echo "[2/3] Fixing htmldecode.c..."
# htmldecode.c fixes
sed -i 's/^\(\s*\)int nData;/\1Tcl_Size nData;/' htmldecode.c
sed -i 's/^\(\s*\)int nIn;/\1Tcl_Size nIn;/' htmldecode.c
sed -i 's/^\(\s*\)int nInput;/\1Tcl_Size nInput;/' htmldecode.c
echo "  ✓ htmldecode.c fixed"
echo ""

echo "[3/3] Fixing htmltree.c..."
# htmltree.c fixes
sed -i 's/^\(\s*\)int nNew;/\1Tcl_Size nNew;/' htmltree.c
echo "  ✓ htmltree.c fixed"
echo ""

echo "=== Complete ==="
echo "Run 'make' to test"
