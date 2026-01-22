# HV3 Browser Revival Project

## Overview

This is a revival project for the HV3 web browser, a Tcl/Tk-based browser that was developed in the mid-2000s. HV3 was notable for its use of the Tkhtml3 HTML rendering engine and its clean architecture.

## Project Components

This project consists of three main components:

### 1. Tkhtml3/HV3 (htmlwidget/)
- **License**: BSD 3-Clause (see `bsd-3-clause.txt`)
- **Description**: The HTML rendering engine (Tkhtml3) and the HV3 browser application
- **Location**: `htmlwidget/` directory
- **Key subdirectories**:
  - `hv/` - HV3 browser application (Tcl scripts and C extensions)
  - `src/` - Tkhtml3 rendering engine C source
  - `tests/` - Test suite
  - `doc/` - Documentation

### 2. Tclsee
- **License**: BSD 3-Clause (see `bsd-3-clause.txt`)
- **Description**: JavaScript/ECMAScript engine bridge for Tcl, based on the SEE (Simple ECMAScript Engine)
- **Location**: `tclsee/` directory
- **Files**: C source files for integrating JavaScript support into HV3
- **Note**: Also includes `tclsee.fossil` - the original Fossil repository

### 3. Polipo
- **License**: MIT (see `mit.txt`)
- **Description**: Caching HTTP proxy server used by HV3 for improved performance
- **Location**: `polipo/` directory
- **Files**: Complete C source code for the proxy server

## Repository

GitHub Repository: https://github.com/blubskye/hv3_relive

## Source Acquisition Notes

These sources were very difficult to track down as the original HV3 project is no longer actively maintained. The components in this repository represent:
- Tkhtml3 Alpha 16 (last major release)
- Tclsee (extracted from Fossil repository)
- Polipo (caching proxy)

## Build Requirements

### Expected Dependencies
- Tcl/Tk 8.5 or later
- C compiler (GCC recommended)
- Standard build tools (make, autoconf)

### Build System
- Tkhtml3/HV3 uses autoconf-based configuration
- See `htmlwidget/configure` and `htmlwidget/COMPILE.txt` for build instructions
- Tclsee includes a Makefile
- Polipo includes its own build system

## Project Status

This is the initial setup phase of the revival project. The source code has been collected and organized.

## Next Steps

1. Document the build process for modern systems
2. Test compilation on current Linux/Unix systems
3. Identify and fix compatibility issues with modern Tcl/Tk versions
4. Update dependencies and build system if needed
5. Create a unified build/install process
6. Test browser functionality
7. Plan modernization efforts (CSS3, HTML5, etc.)

## Historical Context

HV3 was developed primarily by Dan Kennedy and others as an experimental web browser. It aimed to:
- Provide a clean, well-structured HTML rendering engine
- Demonstrate Tcl/Tk capabilities for complex applications
- Offer a lightweight alternative to heavyweight browsers

The project was most active from 2005-2007, with Tkhtml3 Alpha 16 being the last major release.

## License Information

This project contains code under two open-source licenses:
- **BSD 3-Clause**: Tkhtml3/HV3 and Tclsee (see `bsd-3-clause.txt`)
- **MIT License**: Polipo (see `mit.txt`)

All components are freely redistributable and modifiable under their respective licenses.

## Contributing

This is a revival/modernization effort. Contributions are welcome for:
- Build system improvements
- Compatibility fixes
- Bug fixes
- Documentation
- Modernization of web standards support

## Contact

Project maintained at: https://github.com/blubskye/hv3_relive
