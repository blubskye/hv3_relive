##### Top of the Tkhtml source tree - the directory with this file in it.
#
#TOP = $(HOME)/work/tkhtml/htmlwidget
TOP = $(CURDIR)

##### BUILD can be DEBUG, RELEASE or MEMDEBUG.
#
BUILD = DEBUG
# BUILD = RELEASE
# BUILD = MEMDEBUG
# BUILD = PROFILE


MKSHLIB = $(CC) -shared
TCLSTUBSLIB_MEMDEBUG  =  "/home/dan/memtcl/lib/libtclstub8.5.a" 
TCLSTUBSLIB_MEMDEBUG += "/home/dan/memtcl/lib/libtkstub8.5.a" 

TCLSTUBSLIB_DEBUG = -L/usr/lib/x86_64-linux-gnu -ltclstub8.6

TCLSTUBSLIB = $(TCLSTUBSLIB_$(BUILD))

STRIP_RELEASE = strip
STRIP_DEBUG = true
STRIP_MEMDEBUG = $(STRIP_DEBUG)
STRIP_PROFILE = $(STRIP_DEBUG)
STRIP = $(STRIP_$(BUILD))

SOURCES = hv3see.c hv3format.c hv3events.c hv3timeout.c hv3bridge.c


##### Javascript libaries - libgc.a and libsee.a
#
JS_SHARED_LIB = libTclsee.so

#JSLIB   = $(HOME)/work/tkhtml/js/lib/libgc.a
#JSLIB  += $(HOME)/work/tkhtml/js/lib/libsee.a -lpthread
#JSFLAGS = -I$(HOME)/work/tkhtml/js/include

#JSLIB  = $(HOME)/javascript/install_nogc/lib/libsee.a
#JSFLAGS = -I$(HOME)/javascript/install_nogc/include -DNO_HAVE_GC

JSLIB   = /usr/local/lib/libgc.a
JSLIB  += /usr/local/lib/libsee.a -lpthread


CLFAGS  = -I/usr/local/include
CFLAGS += -I/usr/include/tcl8.6
CFLAGS += -fPIC -shared

#CFLAGS += -I$(TCL)/include -I. -I$(TOP)/src/
STUBSFLAGS = -DUSE_TCL_STUBS -DUSE_TK_STUBS

# How to run the C compiler:
COMPILE = $(CC) $(CFLAGS) $(STUBSFLAGS)



#-----------------------------------------------------------------------
# Targets to build the binary javascript extension (libtclsee.so) and
# set up a package directory for it. Requires that the following 
# variables are set:
#
#     JS_SHARED_LIB
#     JSLIB
#     JSFLAGS
#
# Building the target "tclsee" creates a directory "tclsee0.1" and
# populates it with a pkgIndex.tcl and shared object file implementing
# the "Tclsee" package.
#
tclsee: $(JS_SHARED_LIB)
	mkdir -p tclsee0.1
	mv $(JS_SHARED_LIB) tclsee0.1
	cp tclseemock.tcl tclsee0.1
	echo 'package ifneeded Tclsee 0.1 [list load [file join $$dir $(JS_SHARED_LIB)]]' > tclsee0.1/pkgIndex.tcl
	echo 'package ifneeded Tclseemock 0.1  [list source [file join $$dir tclseemock.tcl]]' >> tclsee0.1/pkgIndex.tcl

$(JS_SHARED_LIB): tclsee.o
	@echo '$$(MKSHLIB) tclsee.o $(JSLIB) -o $(JS_SHARED_LIB)'
	@$(MKSHLIB) tclsee.o $(JSLIB) $(TCLSTUBSLIB) -o $(JS_SHARED_LIB)
	@echo '$$(STRIP) $(JS_SHARED_LIB)'
	@$(STRIP) $(JS_SHARED_LIB)

tclsee.o: $(SOURCES)
	@echo warning: TOP variable not used $(TOP)
	@echo '$$(COMPILE) $(JSFLAGS) -c $(TOP)/hv3see.c -o $@'
	@$(COMPILE) $(JSFLAGS) -c $(TOP)/hv3see.c -o $@
#
#-----------------------------------------------------------------------


clean:
	rm -f tclsee.o

.PHONY: clean tclsee
