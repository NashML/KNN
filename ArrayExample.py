
# coding: utf-8

# In[61]:

import cmath
import math
import numpy as np
import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')


# In[83]:

class array_resp:
    def __init__(self, N):
        self.points = np.array([1.0, 0.0], ndmin=2)
        self.dist = 0.23
        for idx in range(1,N):
            loc = [math.cos((2*math.pi/N)*idx), math.sin((2*math.pi/N)*idx)]
            self.points = self.dist * np.concatenate((self.points, np.array(loc, ndmin=2)), axis=0)
    
    def calc_response(self, theta):
        doa_vector = np.array([0.70710678 * math.cos(theta), 0.70710678 * math.sin(theta)], ndmin=2)
        rel_dist = np.dot(self.points, doa_vector.T)
        arr_resp = np.exp(-1j * rel_dist)
        return np.angle(arr_resp).T
    
    def build_table(self, npoints):
        self.table = self.calc_response(0.0)
        self.doa = np.array([0.0], ndmin=1)
        step = 2.0*math.pi/npoints
        angle = step
        while (angle < 2 * cmath.pi):
            self.table = np.concatenate((self.table, self.calc_response(angle)), axis=0)
            self.doa = np.concatenate((self.doa, np.array([angle], ndmin=1)), axis=0)
            angle += step
    
    def print_table(self):
        for resp in self.table:
            print resp
    
    def calc_distance(self, response):
        return np.linalg.norm(self.table - response, axis=1)
    
    def find_nearest(self, response):
        distances = self.calc_distance(response)
        min_index = np.argmin(distances)
        return self.doa[min_index]
    
    def convert_to_degrees(self, val):
        return 360.0 * val / (2.0 * math.pi)
    


# In[87]:

arg = array_resp(5)
arg.build_table(360)
clean_response = arg.calc_response(0.75)
noisy_response = clean_response + 0.1 * np.random.random(clean_response.shape)
distances = arg.calc_distance(noisy_response)
print noisy_response
print arg.convert_to_degrees(0.75)
plt.plot(arg.convert_to_degrees(arg.doa), arg.calc_distance(noisy_response)); plt.show()
print arg.convert_to_degrees(arg.find_nearest(noisy_response))


# In[88]:




# In[ ]:



