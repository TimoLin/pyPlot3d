#/usr/bin/python

# This is a python script 
import numpy as np
import fortranfile as ff
import sys
import os

class block:
    # self.block_no
    # self.id
    # self.jd
    # self.kd
    def __init__(self, n, id, jd, kd):
        self.block_no = n
        self.idim = id
        self.jdim = jd
        self.kdim = kd
        self.size = id*jd*kd
        size_array = (id+1)*(jd+1)*(kd+1)# +1 means 0 to the array beginer as a placeholder
        # Notice: the array dims should be (k,j,i) not like in the fortran (i,j,k)
        self.x = np.arange(size_array, dtype='float').reshape(kd+1, jd+1, id+1)
        self.y = np.arange(size_array, dtype='float').reshape(kd+1, jd+1, id+1)
        self.z = np.arange(size_array, dtype='float').reshape(kd+1, jd+1, id+1)

def plot3d_read(file):

    global b
    
    # the endian depends on your machine or you plot3d file. 
    # Tested for icemcfd 18.0 and 19.0 plot3d unforamtted file, 'Big endian'='>' option should be used!
    f = ff.FortranFile(file, endian='>')

    header = f.readInts()
    nblocks = header[0]

    dims = f.readInts()
    # put dims into idim jdim kdim
    idim = np.arange(nblocks+1, dtype='int32')
    jdim = np.arange(nblocks+1, dtype='int32')
    kdim = np.arange(nblocks+1, dtype='int32')
    # set index[0] to be 0, as a placeholder. so the index will begin from 1 as in fortran
    idim[0] = 0
    jdim[0] = 0
    kdim[0] = 0
    # get the i j k dims from dims
    i = 0
    for n in range(1,nblocks+1):
        idim[n] = dims[i]
        jdim[n] = dims[i+1]
        kdim[n] = dims[i+2]
        if n < nblocks:
            i += 3

    # create block_mesh class for each block
    b = [] #create a blank list
    b.append(block(0,0,0,0)) #placeholder

    for n in range(1,nblocks+1):
        #temp = block(n,idim[n],jdim[n],kdim[n])
        b.append(block(n,idim[n],jdim[n],kdim[n]))
        #b.append(temp)
    print ' Total blocks:', nblocks

    print (' Initializing block mesh arrays ')
    for n in range(1,nblocks+1):
        print ' Block ',n
        print ' Idim:',idim[n],' Jdim:',jdim[n],' Kdim:',kdim[n]

    ptr = list(range(nblocks+2))
    ptr[0] = 0 #placeholder
    ptr[1] = 0 # first block pointer equals to 0
    for n in range(1,nblocks+1):
        ptr[n+1] = ptr[n] + b[n].size*3
    # read the mesh cooridinates into 'data'
    
    data = np.arange(ptr[-1],dtype='float32')
    data = f.readReals('f')

    for n in range(1,nblocks+1):
        temp = np.arange(b[n].size,dtype='float32')

        start = ptr[n]
        end = start + b[n].size - 1
        temp = data[start:end].copy()
        #print data[start:end]

        temp.resize(kdim[n],jdim[n],idim[n]) #its okay if you use b[n].idim. equal with idim[n]
        b[n].x[1:,1:,1:] = temp[0:,0:,0:]
        #print temp

        start = end +1
        end = start + b[n].size-1
        temp = data[start:end].copy()        
        temp.resize(kdim[n],jdim[n],idim[n]) #its okay if you use b[n].idim. equal with idim[n]
        b[n].y[1:,1:,1:] = temp[0:,0:,0:]

        start = end +1
        end = start + b[n].size-1
        temp = data[start:end].copy()
        temp.resize(kdim[n],jdim[n],idim[n]) #its okay if you use b[n].idim. equal with idim[n]
        b[n].z[1:,1:,1:] = temp[0:,0:,0:]
        #print b[n].x[12,5,5],b[n].size,ptr[n],b[n].block_no
    print (' Read block mesh data into arrays ')

    print (' Plot3d file read complete ')

def main():
    if '-plot3d' in sys.argv:
        plot3d_file = sys.argv[sys.argv.index('-plot3d')+1]
        print(' Plot3d file is :'+plot3d_file)
    else:
        print(' Hey, I need the plot3d file name! ')
        print(' Please use: \"-plot3d filename\" ')
        exit()
    plot3d_read(plot3d_file)

if __name__ == '__main__':
    main()
