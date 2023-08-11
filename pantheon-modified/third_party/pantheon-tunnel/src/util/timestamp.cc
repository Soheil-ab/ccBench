/* -*-mode:c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

#include <ctime>

#include "timestamp.hh"
#include "exception.hh"

uint64_t raw_timestamp_usecs( void )
{
    timespec ts;
    SystemCall( "clock_gettime", clock_gettime( CLOCK_REALTIME, &ts ) );

    uint64_t usecs = uint64_t( ts.tv_nsec ) / 1000;
    usecs += uint64_t( ts.tv_sec ) * 1000000;
    return usecs;
}

inline uint64_t usec_to_msec( uint64_t timestamp_usec )
{
    return timestamp_usec / 1000;
}

uint64_t initial_timestamp_usecs( void )
{
    static uint64_t initial_usecs = raw_timestamp_usecs();
    return initial_usecs;
}

uint64_t initial_timestamp( void )
{
    return usec_to_msec( initial_timestamp_usecs() );
}

uint64_t timestamp_usecs( void )
{
    return raw_timestamp_usecs() - initial_timestamp_usecs();
}

uint64_t timestamp( void )
{
    return usec_to_msec( timestamp_usecs() );
}
