#!/bin/bash
# HV3 Browser Launcher Script
# This script sets up the environment and launches the HV3 browser

# Get the directory where this script is located
HV3_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Add Tkhtml3 package to the auto_path
export TCLLIBPATH="${HV3_DIR}/build-tkhtml ${TCLLIBPATH}"

# Add Tclsee package to the auto_path (if needed for JavaScript support)
export TCLLIBPATH="${HV3_DIR}/tclsee ${TCLLIBPATH}"

# Run HV3
cd "${HV3_DIR}/htmlwidget/hv"
exec tclsh hv3_main.tcl "$@"
