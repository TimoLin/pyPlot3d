## A python script that reads plot3d unformatted file.  
Require numpy and fortranfile:
```shell
pip install numpy
pip install fortranfile
```

## Using:
```shell
python pyPlot3d.py  -plot3d  2-block.dat  

```
## Motivation:  
I want to use python to generate 1-to-1 block interface (topology information) for my CFD code. So I spend some time to figure out how to read fortran unformatted file in Python.  
## Notice:  
The array dimentions in this python script is not like in Fortran. For example:  
Fortran: `x(i,j,k)`  
Python: ` x[k,j,i]`  
So when using it, make sure you put i,j,k in the right place.   
And by the way, in this python script, i,j,k data in the arrays are started from 1 as in Fortran. `x[0,:,:]`, `x[:,0,:]` and `x[:,:,0]` are placeholders and have no meaning. 
