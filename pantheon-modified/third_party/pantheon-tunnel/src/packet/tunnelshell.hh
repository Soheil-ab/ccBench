/* -*-mode:c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

#ifndef TUNNELSHELL_HH
#define TUNNELSHELL_HH

#include <string>
#include <fstream>
#include <memory>

#include "tunnelshell_common.hh"
#include "netdevice.hh"
#include "util.hh"
#include "address.hh"
#include "timestamp.hh"
#include "event_loop.hh"
#include "socketpair.hh"
#include "socket.hh"

class TunnelShell
{
    private:
        uint64_t uid_ = 0;
        EventLoop outside_shell_loop;

        int mtu_size_;

    public:
        TunnelShell( int mtu_size = 1500 );

        void start_link( char ** const user_environment, UDPSocket & peer_socket,
                const Address & local_private_address,
                const Address & peer_private_address,
                std::unique_ptr<std::ofstream> &ingress_logfile,
                std::unique_ptr<std::ofstream> &egress_logfile,
                const std::string & shell_prefix,
                const std::vector< std::string > & command );

        int wait_for_exit( void );

        TunnelShell( const TunnelShell & other ) = delete;
        TunnelShell & operator=( const TunnelShell & other ) = delete;
};

#endif /* TUNNELSHELL_HH */
