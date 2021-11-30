# load pickle module
import pickle, os, sys, random

# define dictionary
dict = {}

# 12 possible states to represent all possible pieces
result=[[[random.randint(0,2**256) for i in range(12)]
            # 8*8 chess board
            for j in range(8)]
            for k in range(8)]

# create a binary pickle file 
# f = open(os.path.join(sys.path[0], "zobTable.pkl"),"wb")
f = open(os.path.join(sys.path[0], "check.pkl"),"wb")

# write the python object (dict) to pickle file
# dict=pickle.load(f)
# print(dict)
pickle.dump(dict, f)

# close file
f.close()
