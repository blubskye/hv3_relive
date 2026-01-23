#!/bin/bash
HV3_DIR="$(pwd)"
export TCLLIBPATH="${HV3_DIR}/build-tkhtml ${HV3_DIR}/tclsee"
cd "${HV3_DIR}/htmlwidget/hv"
exec tclsh hv3_main.tcl "$@"
