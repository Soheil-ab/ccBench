/* -*-mode:c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

#ifndef TIMESTAMP_HH
#define TIMESTAMP_HH

#include <cstdint>

uint64_t timestamp( void );
uint64_t initial_timestamp( void );

uint64_t timestamp_usecs( void );
uint64_t initial_timestamp_usecs( void );

#endif /* TIMESTAMP_HH */
