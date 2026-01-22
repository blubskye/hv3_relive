<div align="center">

![HV3 Revive Logo](hv3_revivelogo.png)

# 🦋 HV3 Browser Revival 🦋

### *Bringing a legendary Tcl/Tk HTML browser back to life*

[![License: BSD-3-Clause](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Tcl/Tk](https://img.shields.io/badge/Tcl%2FTk-9.0-brightgreen.svg)](https://www.tcl.tk/)
[![Status](https://img.shields.io/badge/Status-Compiling%20Successfully-success.svg)]()

*Reviving history, one compile at a time* ✨

---

</div>

## 📖 About

HV3 is a **Tcl/Tk-based web browser** featuring a custom HTML rendering engine (Tkhtml3), HTTP proxy (Polipo), and JavaScript support (Tclsee with SEE). This project brings these components back to life for **Tcl 9.0** compatibility.

This project was extremely challenging to track down all the required sources and get them compiling on modern systems. The sources here represent a significant effort to preserve this piece of web browser history.

---

## 🎯 Project Status

### ✅ Successfully Compiled Components

| Component | Description | Status | Size |
|-----------|-------------|--------|------|
| **Polipo** 🌐 | HTTP proxy with caching | ✅ Complete | 727 KB |
| **Tkhtml3/HV3** 🎨 | HTML rendering engine | ✅ Complete | 400 KB |
| **Tclsee** ⚡ | JavaScript bridge (SEE) | ✅ Complete | 718 KB |

All three core components now compile successfully on modern Linux systems with Tcl 9.0!

---

## 🏗️ Components

### 🌐 Polipo (HTTP Proxy)
- **Location:** `polipo/`
- **License:** MIT
- **Purpose:** Caching HTTP proxy server
- **Binary:** `polipo/polipo` (727K)
- **Status:** ✅ Fully functional

### 🎨 Tkhtml3/HV3 (HTML Rendering Engine)
- **Location:** `htmlwidget/` & `build-tkhtml/`
- **License:** BSD 3-Clause
- **Purpose:** Tk-based HTML rendering widget
- **Library:** `build-tkhtml/libTkhtml3.0.so` (400K)
- **Status:** ✅ All 22 source files compiled
- **Tcl 9.0 Fixes:** Complete compatibility layer implemented

### ⚡ Tclsee (JavaScript Bridge)
- **Location:** `tclsee/`
- **License:** BSD 3-Clause
- **Purpose:** JavaScript execution via SEE (Simple ECMAScript Engine)
- **Library:** `tclsee/tclsee0.1/libTclsee.so` (718K)
- **Dependencies:** SEE, Boehm GC
- **Status:** ✅ Fully compiled with Unicode conversion fixes

---

## 💻 System Requirements

### 📋 Prerequisites

- **OS:** Linux (tested on Fedora 43)
- **Compiler:** GCC 15+ or compatible
- **Tcl:** 9.0.2+
- **Tk:** 9.0.2+
- **Libraries:** sqlite-devel, openssl-devel, gc-devel

### 🔧 Development Tools
```bash
# Fedora/RHEL
sudo dnf install tcl-devel tk-devel sqlite-devel openssl-devel gc-devel

# Ubuntu/Debian
sudo apt install tcl-dev tk-dev libsqlite3-dev libssl-dev libgc-dev

# Arch
sudo pacman -S tcl tk sqlite openssl gc
```

---

## 🚀 Building

### 📦 Quick Start

```bash
# Clone the repository
git clone https://github.com/blubskye/hv3_relive.git
cd hv3_relive

# Build all components (see individual sections below)
```

### 1️⃣ Building Polipo

```bash
cd polipo
make
# Binary: ./polipo (727K)
```

### 2️⃣ Building Tkhtml3

```bash
# Configure
cd htmlwidget
mkdir ../build-tkhtml
cd ../build-tkhtml
../htmlwidget/configure --with-tcl=/usr/lib64 --with-tk=/usr/lib64

# Build
make

# Output: libTkhtml3.0.so (400K)
```

### 3️⃣ Building SEE (for Tclsee)

```bash
# Clone and build SEE
cd /tmp
git clone https://github.com/adamnemecek/see-mirror.git see
cd see

# Configure with compatibility flags
CFLAGS="-Wno-error=implicit-function-declaration -Wno-error=builtin-declaration-mismatch -fPIC" \
  ./configure --prefix=/usr/local

# Build
touch config.status Makefile
make CFLAGS="-Wno-error=implicit-function-declaration -Wno-error=builtin-declaration-mismatch -fPIC"

# Install
sudo make install
```

### 4️⃣ Building Tclsee

```bash
cd tclsee
make

# Output: tclsee0.1/libTclsee.so (718K)
```

---

## 🚀 Running HV3

### 📍 Binary Locations

After building, you'll find the compiled components at:

| Component | Location | Type |
|-----------|----------|------|
| **Polipo** | `polipo/polipo` | Binary (727KB) |
| **Tkhtml3** | `build-tkhtml/libTkhtml3.0.so` | Shared Library (400KB) |
| **Tkhtml3 Package** | `build-tkhtml/pkgIndex.tcl` | Tcl Package Index |
| **Tclsee** | `tclsee/tclsee0.1/libTclsee.so` | Shared Library (718KB) |
| **Tclsee Package** | `tclsee/tclsee0.1/pkgIndex.tcl` | Tcl Package Index |

### ▶️ Launching the Browser

Use the provided launcher script:

```bash
./run-hv3.sh
```

The launcher script automatically:
- Sets up package paths for Tkhtml3 and Tclsee
- Launches the HV3 browser with proper environment

### 🎯 Manual Launch

If you prefer to run manually:

```bash
cd htmlwidget/hv
export TCLLIBPATH="../../build-tkhtml ../../tclsee"
tclsh hv3_main.tcl
```

### 📋 Runtime Requirements

- **Tcl/Tk 9.0+** - Required
- **Tkhtml3 package** - Built in `build-tkhtml/`
- **Optional packages:**
  - `Img` - For additional image format support (PNG, JPEG, GIF)
  - `sqlite3` - For cookies and history
  - `Tclsee` - For JavaScript support

### ⚡ Optional: Start Polipo Proxy

For improved performance with caching:

```bash
# In a separate terminal
cd polipo
./polipo
```

Then configure HV3 to use the proxy at `localhost:8123`

---

## 🔨 Tcl 9.0 Compatibility Fixes

This project includes extensive compatibility fixes for Tcl 9.0:

### 🛠️ Major Changes Addressed

| Issue | Solution | Files Affected |
|-------|----------|----------------|
| **CONST macro removed** | Added compatibility defines | `html.h`, `hv3see.c`, `hv3events.c` |
| **int → Tcl_Size** | Updated API call parameters | 18+ files |
| **Tk_Offset → offsetof** | Replaced macro calls | `htmlhash.c`, `htmlprop.c`, `htmltext.c` |
| **Tk_PhotoPutBlock API** | Added new parameters | `htmlimage.c` |
| **Hash function signatures** | `unsigned int → size_t` | `htmlhash.c` |
| **Unicode char size** | `SEE_char_t (16-bit) → Tcl_UniChar (32-bit)` | `hv3see.c`, conversion helpers added |
| **HtmlHeapDebug** | Added `HTML_DEBUG` guards | `htmltcl.c` |

### 📝 Compatibility Layer

The project includes a comprehensive compatibility layer in `htmlwidget/src/html.h`:

```c
/* Tcl 9.0 compatibility */
#ifndef CONST
#define CONST const
#endif

#if !defined(TCL_SIZE_MAX)
typedef int Tcl_Size;
#define Tcl_GetSizeIntFromObj Tcl_GetIntFromObj
#define Tcl_NewSizeIntObj Tcl_NewIntObj
#endif
```

---

## 📚 Documentation

- **Build Notes:** [`COMPILE_NOTES.md`](COMPILE_NOTES.md) - Detailed compilation issues and solutions
- **Scripts:** `scripts/` - Automation scripts for fixing compatibility issues
  - `fix_tcl9_compat.sh` - Automated Tcl 9.0 compatibility fixes
  - `fix_tcl_size_issues.py` - Python script for Tcl_Size conversions
  - `targeted_tcl_size_fix.sh` - Targeted fixes for specific files
  - `fix_tclsee_tcl9.py` - Tclsee-specific Tcl 9.0 fixes

---

## 🗺️ Roadmap

- ✅ **Phase 1:** Compile all components for Tcl 9.0
- 🚧 **Phase 2:** OpenSSL/TLS integration for modern HTTPS support
- 📋 **Phase 3:** Runtime testing and bug fixes
- 🎨 **Phase 4:** Modern web standards support
- 🚀 **Phase 5:** Package and distribute

---

## 📜 Licenses

### Main Components

| Component | License | Copyright |
|-----------|---------|-----------|
| **Tkhtml3/HV3** | BSD 3-Clause | Dan Kennedy, 2005-2008 |
| **Tclsee** | BSD 3-Clause | Dan Kennedy |
| **Polipo** | MIT | Juliusz Chroboczek |
| **SEE** | BSD-style | David Leonard |
| **Boehm GC** | MIT-style | Various contributors |

See individual LICENSE files in each component directory for full license text.

---

## 👨‍💻 Credits

### 💙 Revival Project

| Contributor | Role |
|-------------|------|
| **blubskye** | Project lead, source hunting, Tcl 9.0 porting |
| **Claude Sonnet 4.5** | AI assistant for code analysis and fixes |

### 🌟 Original Authors

- **Dan Kennedy** - Tkhtml3/HV3, Tclsee
- **Juliusz Chroboczek** - Polipo
- **David Leonard** - SEE (Simple ECMAScript Engine)
- **Hans Boehm** - Boehm-Demers-Weiser Garbage Collector

*Standing on the shoulders of giants* 🙏

---

## 🔗 Resources

- **Original Tkhtml3:** http://tkhtml.tcl.tk/ (archived)
- **SEE Mirror:** https://github.com/adamnemecek/see-mirror
- **Tcl/Tk:** https://www.tcl.tk/
- **Project Repository:** https://github.com/blubskye/hv3_relive

---

## ⚠️ Known Issues

- 🔨 Full browser runtime not yet tested
- 🌐 No HTTPS/TLS support yet (OpenSSL integration planned)
- 🎨 Modern CSS/HTML5 features not supported
- ⚡ JavaScript support limited to ECMAScript 3 (SEE limitation)

---

## 🤝 Contributing

Contributions welcome! This is a preservation and modernization project. Areas needing help:

- 🔐 OpenSSL/TLS integration
- 🐛 Bug fixes and testing
- 📖 Documentation improvements
- 🎨 Modern web standards support
- 🚀 Performance optimizations

---

<div align="center">

### 🦋 *Preserving web browser history, one commit at a time* 🦋

**Made with determination and a love for vintage software** 💙

*"The butterfly has emerged from its cocoon"* ✨

---

⭐ *Star this repo if you appreciate software preservation!* ⭐

</div>
