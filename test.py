'''Used for Debugging/Testing Purposes'''
import pickle
from network import Network

n=Network()
dots=pickle.loads(n.dots)
print(dots)