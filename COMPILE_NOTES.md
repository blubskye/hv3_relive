# Compilation Notes for HV3 Revival

## Build Environment
- **OS**: Fedora 43 (Linux 6.18.5-200.fc43.x86_64)
- **Compiler**: GCC 15.2.1
- **Tcl Version**: 9.0.2
- **Tk Version**: 9.0.2

## Tcl 9.0 Compatibility Changes

The original HV3/Tkhtml3 code was written for Tcl/Tk 8.5-8.6. Tcl 9.0 introduced several breaking API changes that required fixes:

### 1. Removed Macros (htmlwidget/src/html.h)
Added compatibility layer for removed macros:
```c
#ifndef CONST
#define CONST const
#endif
#ifndef CONST86
#define CONST86 const
#endif
#ifndef VOID
#define VOID void
#endif
```

### 2. Tcl_Size Type Changes
Tcl 9.0 changed many API functions from `int` to `Tcl_Size` (typedef for `long int`).
Added compatibility typedef for older Tcl versions:
```c
#if !defined(TCL_SIZE_MAX)
typedef int Tcl_Size;
#define Tcl_GetSizeIntFromObj Tcl_GetIntFromObj
#define Tcl_NewSizeIntObj Tcl_NewIntObj
#endif
```

**Affected Functions:**
- `Tcl_GetStringFromObj(obj, &len)` - len changed from `int*` to `Tcl_Size*`
- `Tcl_ListObjGetElements(interp, obj, &count, &items)` - count changed to `Tcl_Size*`

**Files Modified:**
- css.c (lines 2537, 2582, 3657, 3666, 4578)
- csssearch.c (line 157)
- htmlimage.c (line 363)
- htmlparse.c (line 1464)
- htmlprop.c (lines 2711, 3014)

### 3. Hash Function Signatures (htmlhash.c)
Hash functions changed from returning `unsigned int` to `size_t`:
```c
// Old:
static unsigned int hashCaseInsensitiveKey(...)

// New:
static size_t hashCaseInsensitiveKey(...)
```

### 4. Tk_Offset Macro Removed
Replaced all uses of `Tk_Offset(type, field)` with standard `offsetof(type, field)`:
- htmlhash.c (lines 407, 409)
- htmlprop.c (multiple instances via sed replacement)
- htmltcl.c (multiple instances via sed replacement)

### 5. Tk_PhotoPutBlock API Change (htmlimage.c)
Tcl 9.0 added two parameters to `Tk_PhotoPutBlock`:
```c
// Old signature:
Tk_PhotoPutBlock(handle, blockPtr, x, y, width, height)

// New signature:
Tk_PhotoPutBlock(interp, handle, blockPtr, x, y, width, height, compRule)
```

### 6. Old K&R C Style Function Declarations
Fixed lemon parser generator (tools/lemon.c) to compile with modern GCC:
- Modified Makefile to use `-std=gnu89` with warnings disabled for lemon.c
- This allows the old-style function definitions to compile

## Successfully Compiled Components

### Polipo (HTTP Proxy)
- **Status**: ✅ Compiled successfully
- **Binary**: polipo/polipo (727K)
- **Issues**: Minor warnings only (format truncation, old-style definitions in md5.c)

### Tkhtml3 Widget
**Successfully Compiled Files:**
- css.c
- csssearch.c
- cssdynamic.c
- htmlfloat.c
- htmlhash.c
- htmlimage.c
- htmlparse.c
- htmlprop.c

**In Progress:**
- htmltcl.c (5 remaining Tcl_Size errors)
- Additional source files pending

## Build Process

1. **Polipo**:
   ```bash
   cd polipo
   make
   ```

2. **Tkhtml3**:
   ```bash
   mkdir build-tkhtml
   cd build-tkhtml
   ../htmlwidget/configure --with-tcl=/usr/lib64 --with-tk=/usr/lib64
   make
   ```

## Remaining Work

1. Fix remaining `Tcl_Size` type mismatches in:
   - htmltcl.c (lines 1409, 1673, 2186)
   - Other pending source files

2. Add missing includes:
   - `<stdarg.h>` for va_start in htmltcl.c

3. Resolve undefined function references:
   - `HtmlHeapDebug` in htmltcl.c

4. Complete compilation of remaining source files

5. Link final shared library

## Automated Fix Script

See `scripts/fix_tcl9_compat.sh` for automated fixing of remaining Tcl_Size issues.

## Notes

- All changes maintain backward compatibility with Tcl 8.6 through the compatibility layer
- The codebase contains extensive old-style K&R C function definitions (warnings only)
- Original license files preserved (BSD-3-Clause for Tkhtml3/Tclsee, MIT for Polipo)
