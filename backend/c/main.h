#include <stddef.h>

#ifndef __MAIN_H__
#define __MAIN_H__

/*  To use this exported function of dll/shared library, include this header
 *  in your project.
 */

#ifdef _WIN32
    #include <windows.h>
    #ifdef BUILD_DLL
        #define DLL_EXPORT __declspec(dllexport)
    #else
        #define DLL_EXPORT __declspec(dllimport)
    #endif
#else
    #ifdef BUILD_DLL
        #define DLL_EXPORT __attribute__((visibility("default")))
    #else
        #define DLL_EXPORT
    #endif
#endif


#ifdef __cplusplus
extern "C"
{
#endif

void DLL_EXPORT spread_fire(int width);

int DLL_EXPORT get_colour_heights(int index);

void DLL_EXPORT setup_height_map(size_t width, size_t height);

#ifdef __cplusplus
}
#endif

#endif // __MAIN_H__
