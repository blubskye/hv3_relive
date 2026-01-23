#!/usr/bin/env tclkit
# HV3 Browser for Tcl 9.0

# Add system library paths for Img and sqlite3
if {[file isdirectory /usr/lib64/tcl9.0]} {
    lappend auto_path /usr/lib64/tcl9.0
}
if {[file isdirectory /usr/share/tcl9.0]} {
    lappend auto_path /usr/share/tcl9.0
}

# Add our bundled libraries
lappend auto_path [file join [file dirname [info script]] lib tkhtml3.0]
lappend auto_path [file join [file dirname [info script]] lib tclsee]

# Change to HV3 directory for source file paths
cd [file join [file dirname [info script]] lib hv]

# Source HV3
source [file join [file dirname [info script]] lib hv hv3_main.tcl]
