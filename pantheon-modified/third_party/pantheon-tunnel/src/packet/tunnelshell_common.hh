#ifndef TUNNELSHELL_COMMON_HH
#define TUNNELSHELL_COMMON_HH

#include <string>
#include <fcntl.h>
#include <unistd.h>

#include <memory>
#include <iostream>
#include <fstream>

#include "exception.hh"
#include "file_descriptor.hh"
#include "util.hh"
#include "timestamp.hh"

using namespace std;

struct wrapped_packet_header {
    uint64_t uid;
};

void check_interface_for_binding( const std::string &prog_name, const std::string &if_name );

int get_mtu( const std::string & if_name );

void send_wrapper_only_datagram( FileDescriptor &connected_socket, const uint64_t uid );

double pretty_microseconds( uint64_t usecs );

void initialize_logfile( std::unique_ptr<std::ofstream>& log, const std::string &log_name, int argc, char *argv[], std::string log_type );

#endif /* TUNNELSHELL_COMMON_HH */
