#!/usr/bin/tclsh
package require Tk
lappend auto_path ./build-tkhtml
package require Tkhtml

# Create a simple window with HTML widget
html .h -width 400 -height 300
pack .h

# Set some simple HTML
.h parse -final {<html><body><h1>Test</h1><p>Hello World</p></body></html>}

# Wait a bit then exit
after 1000 {exit 0}

# Start event loop
vwait forever
