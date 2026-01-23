package require Tk
source hv3_main.tcl

# Override gui_build to catch errors
rename gui_build original_gui_build
proc gui_build {widget_array} {
    if {[catch {original_gui_build $widget_array} err]} {
        puts "ERROR in gui_build: $err"
        puts $::errorInfo
        exit 1
    } else {
        puts "GUI built successfully!"
        after 2000 {
            puts "Checking widgets..."
            puts "Toolbar exists: [winfo exists .toolbar]"
            puts "Notebook exists: [winfo exists .notebook]"
            puts "Status exists: [winfo exists .status]"
            exit 0
        }
    }
}
