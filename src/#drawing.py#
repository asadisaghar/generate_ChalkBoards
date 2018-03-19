import sys
import numpy as np
import scipy.ndimage as spim

class drawing(object):
    def __init__(self, label, idx, array, w=28, h=28, verbose=False):
        self.label = label
        self.idx = idx
        self.array = np.reshape(array, (h, w))
        self.h, self.w = self.array.shape
        self.verbose = verbose
        self.rotation_angle = 0
        self.zoom_scale = 1
        self.is_transposed = False
        
    def rotate(self, probability):
        """Rotate by a random angle (<90 degrees)"""
        prob = np.random.random()
        if prob<=probability:
            rotation_angle = 90.*np.random.random()
            if self.verbose:
                print("Rotating the drawing by", rotation_angle, "degrees")
            self.array = spim.rotate(self.array, rotation_angle)
            self.h, self.w = self.array.shape
            self.rotation_angle = rotation_angle

    def scale(self, probability, max_zoom_scale, min_zoom_scale):
        """Scale the drawing up or down (zoom in/out)"""
        prob = np.random.random()
        if prob<=probability:
            zoom_scale = (max_zoom_scale - min_zoom_scale) * np.random.random() + min_zoom_scale 
            if self.verbose:
                print("Scaling the drawing by a factor of", zoom_scale)
            self.array = spim.zoom(self.array, zoom_scale)
            self.h, self.w = self.array.shape
            self.zoom_scale = zoom_scale
                    
    def transpose(self, probability):
        """Transpose the image"""
        prob = np.random.random()
        if prob<=probability:
            if self.verbose:
                print("Transposing the drawing")
            self.array = self.array.T
            self.is_transposed = True
                
    
class email(drawing):
    def __init__(self):
        pass
    
