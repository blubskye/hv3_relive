# -*- mode: tcl -*-
# leg20200408: mock the Tclsee package

namespace eval see {
    variable version 0.1
}

package require TclOO

namespace eval see {

    oo::class create seenterp {
	method destroy {} {log seemock:debug I am destroyed now}
	method global args {
	    log seemock:debug global $args}
	method eval args {
	    if {[llength $args]==3 || [llength $args]==1} {
		::log seemock:debug eval {*}$args
	    } else {
		error "wrong number of arguments: $args"
	    }
	}
	method tostring o {
	    log seemock:debug tostring $o
	    return $o
	}
	method debug objects {
	    log seemock:debug objects $objects
	    return $objects
	}
	method make_transient c {
	    log seemock:debug make_transient $c		
	}
	method make_persistent c {
	    log seemock:debug make_persistent $c
	}
	method node args {
	    log seemock:debug node $args
	}
	method dispatch args {
	    log seemock:debug dispatch $args
	    # isPrevented isHandled
	    return {true false}
	}
	method log args {
	    log seemock:debug log $args
	    return "log seemock:debug logger"
	}
    }
    proc interp args {
	# Is called with three args:
	#   ::hv3::DOM::Window
	#   ::hv3::hv3::dom7
	#   ::hv3::hv3::inst1
	#
	# it seems, that we have to do something with
	# ::hv3:hv3::inst1, so that it can be later called as:
	#   document ::hv3::hv3::inst1 ..
	# and
	#   ::hv3::hv3::inst1 args
	# respectively
	log seemock:debug interp $args
	set 1st [lindex $args 0]
	if {[llength $1st]>2} {
	    set name [lindex $1st 2]
	    log seemock:debug installing callback $name
	    proc $name args "::log seemock:debug callback for $name; return"
	}
	seenterp new
    }
    proc class args {
	log seemock:debug class $args
    }
}

package provide Tclseemock $::see::version
