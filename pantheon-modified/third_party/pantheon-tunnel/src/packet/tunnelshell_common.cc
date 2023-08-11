#include <string>
#include <iomanip>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <net/if.h>

#include <memory>
#include <iostream>
#include <fstream>

#include "tunnelshell_common.hh"
#include "exception.hh"
#include "file_descriptor.hh"
#include "timestamp.hh"
#include "socket.hh"

using namespace std;

void check_interface_for_binding( const std::string &prog_name, const std::string &if_name ) {
    /* verify interface exists and has rp filtering disabled before binding to an interface */
    const std::string interface_rpf_path = "/proc/sys/net/ipv4/conf/" + if_name + "/rp_filter";
    const std::string all_rpf_path = "/proc/sys/net/ipv4/conf/all/rp_filter";

    if ( access( interface_rpf_path.c_str(), R_OK ) == -1 ) {
        throw std::runtime_error( prog_name + ": can't read " + interface_rpf_path + ", interface \"" + if_name + "\" probably doesn't exist" );
    }
    FileDescriptor rpf_interface( SystemCall( "open " + interface_rpf_path, open( interface_rpf_path.c_str(), O_RDONLY ) ) );
    FileDescriptor rpf_all( SystemCall( "open " + all_rpf_path, open( all_rpf_path.c_str(), O_RDONLY ) ) );

    if ( rpf_interface.read() != "0\n" or rpf_all.read() != "0\n" ) {
        throw std::runtime_error( prog_name + ": Please run \"sudo sysctl -w net.ipv4.conf.all.rp_filter=0\" and \"sudo sysctl -w net.ipv4.conf." + if_name + ".rp_filter=0\" to use specified interface");
    }
}

int get_mtu( const string & if_name )
{
  ifreq ifr;
  zero( ifr );
  strncpy( ifr.ifr_name, if_name.c_str(), sizeof(ifr.ifr_name) );

  /* use a temporary socket */
  UDPSocket temp;
  SystemCall( "ioctl " + if_name, ioctl( temp.fd_num(), SIOCGIFMTU, static_cast<void *>( &ifr ) ) );

  return ifr.ifr_mtu;
}

void send_wrapper_only_datagram( FileDescriptor &connected_socket, const uint64_t uid ) {
    const wrapped_packet_header to_send = { uid };
    connected_socket.write( std::string( (char *) &to_send, sizeof(to_send) ) );
}

inline std::string shell_quote( const std::string & arg )
{
    std::string ret = "'";
    for ( const auto & ch : arg ) {
        if ( ch != '\'' ) {
            ret.push_back( ch );
        } else {
            ret += "'\\''";
        }
    }
    ret += "'";

    return ret;
}

double pretty_microseconds( uint64_t usecs )
{
    return double( usecs ) / double ( 1000 );
}

inline std::string pretty_command_line( int argc, char *argv[] )
{
    std::string command_line { shell_quote( argv[ 0 ] ) }; /* for the log file */
    for ( int i = 1; i < argc; i++ ) {
        command_line += std::string( " " ) + shell_quote( argv[ i ] );
    }
    return command_line;
}

void initialize_logfile( std::unique_ptr<std::ofstream>& log, const std::string &log_name, int argc, char *argv[], std::string log_type )
{
    /* open logfiles if called for */
    if ( not log_name.empty() ) {
        log.reset( new std::ofstream( log_name ) );
        if ( not log->good() ) {
            throw runtime_error( log_name + ": error opening for writing" );
        }
    }
    
    if ( log ) {
        *log << "# " + pretty_command_line( argc, argv ) + " " + log_type + ": " << std::setprecision(3) << std::fixed << pretty_microseconds( initial_timestamp_usecs() ) << endl;
    }
}
