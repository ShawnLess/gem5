################################################
# Generate the test programe for the histogram

from scipy import misc
import numpy

########################################################
# Generate the image data for gather operations
def genData(fileName):
    babooImg=misc.imread(fileName)

    #Get the gray image data
    grayImg = babooImg[:,:,0]

    (rows, cols) = grayImg.shape

    #Declare the data array
    decHeader="""
unsigned char imgData[%d]={
"""%(rows * cols)

    lineStr=""


    initArray = numpy.reshape( grayImg, (rows, cols/8, 8) )

    for row in  initArray:
        for col in row:
            lineStr += ",\t".join( [ hex(value) for value in col ] ) +",\n"

    #Declare the data array
    endHeader="""
};
"""

    datFile=open("imgData.h","w")
    datFile.write( decHeader + lineStr[:-2] + endHeader )
    datFile.close()

    return (rows, cols)


if __name__ == "__main__":
    (rows, cols) = genData('BABOO.jpg');






