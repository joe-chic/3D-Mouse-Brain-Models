import numpy as np

A = np.array([np.array([[-1,-5],[5,7]]),
              np.array([[-6,9],[9,-8]]),
              np.array([[-6,-9],[-26,-8]])])

print(A,'\n')

for dim in range(len(A)):
    A[dim][ (np.array(A[dim,:,0]) > 0) | (np.array(A[dim,:,1]) > 0) ] = 0

for dim1 in range(len(A)):
    for dim2 in range(A.shape[1]):
        A[dim1,dim2,:] = min(A[dim1,dim2,0],A[dim1,dim2,1])

A = np.delete(A,0,axis=2)

print(A,'\n')

print(A.shape,'\n')

A = np.reshape(A,(1,A.shape[0]*A.shape[1]))
A = A.squeeze()

print(A[0],'\n')