#include <stdio.h>
/*
A global array contains image data

unsigned char  imgData[][] ={ ... } 
*/
#include "imgData.h"

/*********************************/
/*Parameter of the images.       
the image size must bigger then the
L2 cache.
*/
#define ROWS        1024 
#define COLS        1024 
#define BIT_WIDTH   8
#define HIST_LEN    (1<<BIT_WIDTH)

unsigned int histVect[ HIST_LEN ] = { 0 };
/*********************************/

int main( int argc, char *argv[] ){
    int i=0;

    for( i=0; i< ROWS * COLS ; i++)
        histVect[ imgData[i] ] += 1;
    
    return 0;
}

