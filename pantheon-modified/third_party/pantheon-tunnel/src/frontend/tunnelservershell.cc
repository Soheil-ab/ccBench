/* -*-mode:c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

#include <vector>
#include <string>
#include <iostream>
#include <fstream>
#include <getopt.h>

#include "autoconnect_socket.hh"
#include "tunnelshell_common.hh"
#include "tunnelshell.hh"
#include "interfaces.hh"
#include "timestamp.hh"

using namespace std;
using namespace PollerShortNames;

void usage_error( const string & program_name )
{
    cerr << "Usage: " << program_name << " [OPTION]... [COMMAND]" << endl;
    cerr << endl;
    cerr << "Options = --ingress-log=FILENAME --egress-log=FILENAME --interface=INTERFACE --mtu=MTU" << endl;
    cerr << endl;
    cerr << "MTU is 1500 bytes by default, but will use the detected value on the interface if --interface is given. --mtu will override all." << endl;

    throw runtime_error( "invalid arguments" );
}

int main( int argc, char *argv[] )
{
    try {
        /* clear environment while running as root */
        char ** const user_environment = environ;
        environ = nullptr;

        check_requirements( argc, argv );

        if ( argc < 1 ) {
            usage_error( argv[ 0 ] );
        }

        const option command_line_options[] = {
            { "ingress-log", required_argument, nullptr, 'n' },
            { "egress-log",  required_argument, nullptr, 'e' },
            { "interface",   required_argument, nullptr, 'i' },
            { "mtu",         required_argument, nullptr, 'm' },
            { 0,                             0, nullptr,  0  }
        };

        string ingress_log_name, egress_log_name, if_name, mtu;

        while ( true ) {
            const int opt = getopt_long( argc, argv, "",
                                         command_line_options, nullptr );
            if ( opt == -1 ) { /* end of options */
                break;
            }

            switch ( opt ) {
            case 'n':
                ingress_log_name = optarg;
                break;
            case 'e':
                egress_log_name = optarg;
                break;
            case 'i':
                if_name = optarg;
                break;
            case 'm':
                mtu = optarg;
                break;
            case '?':
                usage_error( argv[ 0 ] );
                break;
            default:
                throw runtime_error( "getopt_long: unexpected return value " +
                                     to_string( opt ) );
            }
        }

        if ( optind > argc ) {
            usage_error( argv[ 0 ] );
        }

        vector< string > command;

        if ( optind == argc ) {
            command.push_back( shell_path() );
        } else {
            for ( int i = optind; i < argc; i++ ) {
                command.push_back( argv[ i ] );
            }
        }

        Address local_private_address, client_private_address;
        tie(local_private_address, client_private_address) = two_unassigned_addresses();

        AutoconnectSocket listening_socket;

        int mtu_size = 1500;

        if ( !if_name.empty() ) {
            /* bind the listening socket to a specified interface */
            check_interface_for_binding( string( argv[ 0 ] ), if_name );
            listening_socket.bind( if_name );

            if ( mtu.empty() ) {
                mtu_size = get_mtu( if_name );
            }
        }

        if ( !mtu.empty() ) {
            mtu_size = stoi( mtu );
        }

        /* bind the listening socket to an available address/port, and print out what was bound */
        listening_socket.bind( Address() );

        std::unique_ptr<std::ofstream> ingress_log, egress_log;
        initialize_logfile( ingress_log, ingress_log_name, argc, argv, "ingress" );
        initialize_logfile( egress_log, egress_log_name, argc, argv, "egress" );

        cout << "mm-tunnelclient localhost " << listening_socket.local_address().port() << " ";
        cout << client_private_address.ip() << " " << local_private_address.ip();
        cout << endl;

        Poller client_poll;

        client_poll.add_action( Poller::Action( listening_socket, Direction::In,
                    [&] () {
                    const string client_packet = listening_socket.read();
                    const wrapped_packet_header client_header = *( (wrapped_packet_header *) client_packet.data() );
                    if (client_packet.length() == sizeof(wrapped_packet_header) && client_header.uid == (uint64_t) -1) {
                        cout << "Tunnelserver got connection from tunnelclient" << endl;
                        send_wrapper_only_datagram( listening_socket, (uint64_t) -2 );
                        return ResultType::Exit;
                    } else {
                        cerr << "Tunnelserver received packet with unidentifiable contents" << endl;
                        return ResultType::Continue;
                    }
                    } ) );
        client_poll.poll( -1 );

        TunnelShell tunnelserver( mtu_size );
        tunnelserver.start_link( user_environment, listening_socket,
                                 local_private_address, client_private_address,
                                 ingress_log, egress_log,
                                 "[tunnelserver] ", command );
        return tunnelserver.wait_for_exit();
    } catch ( const exception & e ) {
        cerr << "Tunnelserver got an exception: ";
        print_exception( e );
        return EXIT_FAILURE;
    }
}
