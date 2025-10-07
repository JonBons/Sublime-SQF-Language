// Test preprocessor directives
#define MACRO_NAME "value"
#undef MACRO_NAME

#ifdef DEBUG_MODE
    hint "Debug mode enabled";
#endif

#ifndef RELEASE_MODE
    hint "Not in release mode";
#endif

#include "common.sqf"
#include <some_header.h>

#define MULTILINE_MACRO \
    "This is a multiline \
    macro definition"

#define ANOTHER_MACRO \
    player setPosATL [0,0,0]

#define SIMPLE_MACRO hint "Simple macro"
