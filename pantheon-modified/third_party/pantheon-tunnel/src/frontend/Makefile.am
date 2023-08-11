AM_CPPFLAGS = -I$(srcdir)/../util -I$(srcdir)/../packet $(CXX11_FLAGS)
AM_CXXFLAGS = $(PICKY_CXXFLAGS)

bin_PROGRAMS = mm-tunnelclient
mm_tunnelclient_SOURCES = tunnelclientshell.cc
mm_tunnelclient_LDADD = -lrt ../packet/libpacket.a ../util/libutil.a
mm_tunnelclient_LDFLAGS = -pthread

bin_PROGRAMS += mm-tunnelserver
mm_tunnelserver_SOURCES = tunnelservershell.cc
mm_tunnelserver_LDADD = -lrt ../packet/libpacket.a ../util/libutil.a
mm_tunnelserver_LDFLAGS = -pthread

install-exec-hook:
	chown root $(DESTDIR)$(bindir)/mm-tunnelclient
	chmod u+s $(DESTDIR)$(bindir)/mm-tunnelclient
	chown root $(DESTDIR)$(bindir)/mm-tunnelserver
	chmod u+s $(DESTDIR)$(bindir)/mm-tunnelserver
