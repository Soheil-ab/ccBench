AM_CPPFLAGS = $(CXX11_FLAGS)
AM_CXXFLAGS = $(PICKY_CXXFLAGS)

noinst_LIBRARIES = libutil.a

libutil_a_SOURCES = exception.hh ezio.cc ezio.hh                               \
        file_descriptor.hh file_descriptor.cc netdevice.cc netdevice.hh        \
	timestamp.cc timestamp.hh                                              \
        child_process.hh child_process.cc signalfd.hh signalfd.cc              \
        socket.cc socket.hh address.cc address.hh                              \
        system_runner.hh system_runner.cc                         \
        util.hh util.cc                               \
        interfaces.hh interfaces.cc                                            \
        poller.hh poller.cc             \
        event_loop.hh event_loop.cc                                            \
        socketpair.hh socketpair.cc autoconnect_socket.hh
