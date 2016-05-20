// An interleaved version of Histogram to
// reduce the memory latency,
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

unsigned int histVect0[ HIST_LEN ] = { 0 };
unsigned int histVect1[ HIST_LEN ] = { 0 };
unsigned int histVect2[ HIST_LEN ] = { 0 };
unsigned int histVect3[ HIST_LEN ] = { 0 };
unsigned int histVect4[ HIST_LEN ] = { 0 };
unsigned int histVect5[ HIST_LEN ] = { 0 };
unsigned int histVect6[ HIST_LEN ] = { 0 };
unsigned int histVect7[ HIST_LEN ] = { 0 };
/*********************************/

int main( int argc, char *argv[] ){
    unsigned int    i=0;
    unsigned char   v0,v1,v2,v3,v4,v5,v6,v7;
    unsigned        c0,c1,c2,c3,c4,c5,c6,c7;

    // Try to preload the counter value using this macro
    #ifdef PLD
    unsigned char   pi0, pi1, pi2, pi3, pi4, pi5, pi6, pi7;
    unsigned int   *pc0, *pc1, *pc2, *pc3, *pc4, *pc5, *pc6, *pc7;
    #endif

    unsigned char   *preLoad;
    for (i=0; i< ROWS * COLS /8 ; i=i+8) {

        #ifdef PREI128
        /*Preload the data imgData[i+128] for later use*/
        preLoad = imgData + i;
        asm(  "PLD [%0,#128]"::"r"(preLoad) );

        #elif PREI64
        /*Preload the data imgData[i+128] for later use*/
        preLoad = imgData + i;
        asm(  "PLD [%0,#64]"::"r"(preLoad) );

        #elif PREI16
        /*Preload the data imgData[i+128] for later use*/
        preLoad = imgData + i;
        asm(  "PLD [%0,#16]"::"r"(preLoad) );
        #endif

        //load the data value
        v0= imgData[i + 0];
        v1= imgData[i + 1];
        v2= imgData[i + 2];
        v3= imgData[i + 3];
        v4= imgData[i + 4];
        v5= imgData[i + 5];
        v6= imgData[i + 6];
        v7= imgData[i + 7];

        #ifdef PLD
        pi0= imgData[i + PLD + 0];
        pi1= imgData[i + PLD + 1];
        pi2= imgData[i + PLD + 2];
        pi3= imgData[i + PLD + 3];
        pi4= imgData[i + PLD + 4];
        pi5= imgData[i + PLD + 5];
        pi6= imgData[i + PLD + 6];
        pi7= imgData[i + PLD + 7];
        #endif

        //get the count
        c0= histVect0[ v0 ];
        c1= histVect1[ v1 ];
        c2= histVect2[ v2 ];
        c3= histVect3[ v3 ];
        c4= histVect4[ v4 ];
        c5= histVect5[ v5 ];
        c6= histVect6[ v6 ];
        c7= histVect7[ v7 ];

        #ifdef PLD
        pc0= histVect0 + pi0;
        pc1= histVect1 + pi1;
        pc2= histVect2 + pi2;
        pc3= histVect3 + pi3;
        pc4= histVect4 + pi4;
        pc5= histVect5 + pi5;
        pc6= histVect6 + pi6;
        pc7= histVect7 + pi7;
        #endif

        // increase the count
        c0= c0 +  1;
        c1= c1 +  1;
        c2= c2 +  1;
        c3= c3 +  1;
        c4= c4 +  1;
        c5= c5 +  1;
        c6= c6 +  1;
        c7= c7 +  1;

        #ifdef PLD
        asm(  "PLD [%0]"::"r"(pc0) );
        asm(  "PLD [%0]"::"r"(pc1) );
        asm(  "PLD [%0]"::"r"(pc2) );
        asm(  "PLD [%0]"::"r"(pc3) );
        asm(  "PLD [%0]"::"r"(pc4) );
        asm(  "PLD [%0]"::"r"(pc5) );
        asm(  "PLD [%0]"::"r"(pc6) );
        asm(  "PLD [%0]"::"r"(pc7) );
        #endif

        // store back the count
        histVect0[ v0 ] = c0;
        histVect1[ v1 ] = c1;
        histVect2[ v2 ] = c2;
        histVect3[ v3 ] = c3;
        histVect4[ v4 ] = c4;
        histVect5[ v5 ] = c5;
        histVect6[ v6 ] = c6;
        histVect7[ v7 ] = c7;
    }
// Using the NO_MERGE to test the const of the
// Merge operation

#ifndef NO_MERGE
    for ( i=0; i< HIST_LEN; i++) {
        histVect0[ i ] =\
            histVect0[ i ] +\
            histVect1[ i ] +\
            histVect2[ i ] +\
            histVect3[ i ] +\
            histVect4[ i ] +\
            histVect5[ i ] +\
            histVect6[ i ] +\
            histVect7[ i ];
    }
#endif
    return 0;
}
