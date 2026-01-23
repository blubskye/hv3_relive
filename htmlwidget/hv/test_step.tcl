package require Tk
package require Tkhtml 3.0
puts "Packages loaded"

source hv3_profile.tcl
puts "Profile loaded"

::hv3::profile::init {}
puts "Profile init"

source snit.tcl
puts "Snit loaded"

source hv3_widgets.tcl
puts "Widgets loaded - ready to exit"
exit
