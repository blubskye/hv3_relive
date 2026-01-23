package require Tk
lappend auto_path ./build-tkhtml
package require Tkhtml

# Create a simple window with HV3 HTML widget
html .h -width 400 -height 300
pack .h

# Load some simple HTML
.h parse -final {
    <html><body>
    <h1 style="color: blue;">SUCCESS!</h1>
    <p>HV3 Browser is working on Tcl 9.0!</p>
    </body></html>
}

after 2000 exit
