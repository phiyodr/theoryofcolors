# Theory of Colours
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from IPython.display import HTML as html_print
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import copy
from stringcolor import cs 
from theoryofcolors.misc import load_color_dict, is_notebook

class ColorCast:
        
    def __init__(self, reference_colors="all"):
        self.color_mapper = load_color_dict(reference_colors) 
        self.color_list = list(self.color_mapper.keys())
    
    ###########
    # string to
    ###########
    
    def string2hex(self, x):
        try:
            color_hex = self.color_mapper[x]
        except:
            print("Error", x)
            color_hex = float("nan")
        return color_hex
    
    def string2rgb(self, x):
        color_hex = self.string2hex(x)
        return self.hex2rgb(color_hex)
     
    def string2hsv(self, x):
        color_hex = self.string2hex(x)
        return self.hex2hsv(color_hex)        
    
    ########
    # hex to
    ########
    
    @staticmethod
    def hex2rgb(x):
        color_rgb = matplotlib.colors.to_rgb(x)
        return color_rgb
    
    def hex2rgbint(self, x):
        color_rgb = self.hex2rgb(x)
        color_rgbint = self.rgb2rgbint(color_rgb)
        return color_rgb
    
    def hex2hsv(self, x):
        color_rgb = self.hex2rgb(x)
        color_hsv = tuple(matplotlib.colors.rgb_to_hsv(color_rgb))
        return color_hsv
    
    ########
    # rgb to
    ########
    
    @staticmethod
    def rgb2hsv(x):
        color_hsv = tuple(matplotlib.colors.rgb_to_hsv(x))
        return color_hsv
    
    def rgb2hex(self, x):
        r, g, b = self.rgb2rgbint(x)
        return "#{:02x}{:02x}{:02x}".format(r, g, b)  
    
    @staticmethod
    def rgb2rgbint(x):
        r, g, b = x
        r, g, b = int(r*255), int(g*255), int(b*255)
        return r, g, b

    ########
    # hsv to
    ########
    
    @staticmethod
    def hsv2rgb(x):
        color_rgb = tuple(matplotlib.colors.hsv_to_rgb(x))
        return rgb
    
    def hsv2rgbint(self, x):
        color_rgb = self.hsv2rgb(x)
        return self.rgb2rgbint(color_rgb)
    
    @staticmethod
    def hsv2hex(self, x):
        color_rgb = tuple(matplotlib.colors.hsv_to_rgb(x))
        r, g, b = self.rgb2rgbint(color_rgb)
        return "#{:02x}{:02x}{:02x}".format(r, g, b)          
    
    #########
    # call
    #########
    
    def __call__(self, x, from_, to_):
        # rgb
        if from_ == "rgb":
            if to_ == "hsv":
                return self.rgb2hsv(x)
            elif to_ == "hex":
                return self.rgb2hex(x)
            elif to_ == "rgbint":
                return self.rgb2rgbint(x)
        # hex
        elif from_ == "hex":
            if to_ == "rgb":
                return self.hex2rgb(x)
            elif to_ == "rgbint":
                return  self.hex2rgbint(x)
            elif to_ == "hsv":
                return self.hex2hsv(x)
        # hsv
        elif from_ == "hsv":
            if to_ == "rgb":
                return self.hsv2reg(x)
            elif to_ == "rgbint":
                return self.rgb2rgbint(x)
            elif to_ == "hex":
                return self.hsv2hex(x)
        # string
        elif from_ == "string":
            if to_ == "rgb":
                return self.string2rgb(x)
            elif to_ == "rgbint":
                color_rgb = self.string2rgb(x)
                return self.rgb2rgbint(color_rgb)
            elif to_ == "hex":
                color_hsv = self.string2hsv(x)
                return self.hsv2hex(color_hsv)
  
if __name__ == '__main__':
    cc = ColorCast()
    cc("#FF0000", "hex", "hsv")
    cc((1.0,0,0), "rgb", "rgbint")
    cc("red00", "string", "rgb")


