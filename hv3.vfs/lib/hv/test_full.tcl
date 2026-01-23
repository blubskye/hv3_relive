package require Tk
package require Tkhtml 3.0

source hv3_profile.tcl
::hv3::profile::init {}

source snit.tcl
source hv3_widgets.tcl
source hv3_encodings.tcl
puts "Encodings loaded"

source hv3_log.tcl  
puts "Log loaded"

source hv3_string.tcl
puts "String loaded"

source hv3_uri.tcl
puts "URI loaded"

puts "All files loaded successfully - creating widget..."
::hv3::hv3 .hv3
puts "Widget created!"
exit
