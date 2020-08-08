#ifndef __MAIN_H__
#define __MAIN_H__

#include <windows.h>

/*  To use this exported function of dll, include this header
 *  in your project.
 */

#ifdef BUILD_DLL
    #define DLL_EXPORT __declspec(dllexport)
#else
    #define DLL_EXPORT __declspec(dllimport)
#endif


#ifdef __cplusplus
extern "C"
{
#endif

void DLL_EXPORT spread_fire(int width);

int DLL_EXPORT get_at(int index);

void DLL_EXPORT setup_height_map(int width, int height);

#ifdef __cplusplus
}
#endif

#endif // __MAIN_H__
