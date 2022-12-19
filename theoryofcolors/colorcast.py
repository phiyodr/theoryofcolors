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
    
    #@staticmethod
    #def hex2rgb(x):
    #    color_rgb = matplotlib.colors.to_rgb(x)
    #    return color_rgb

    def hex2rgb(self, x):
        x = x.strip("#") 
        rgb = tuple(int(x[i:i+2], 16) for i in (0, 2, 4))
        rgb = self.rgbint2rgb(rgb)
        return rgb

    
    def hex2rgbint(self, x):
        color_rgb = self.hex2rgb(x)
        color_rgbint = self.rgb2rgbint(color_rgb)
        return color_rgbint
    
    def hex2hsv(self, x):
        color_rgb = self.hex2rgb(x)
        #print("color_rgb", color_rgb)
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
        color_hex = "#{:02x}{:02x}{:02x}".format(r, g, b)  
        return color_hex.upper()          
    
    @staticmethod
    def rgb2rgbint(x):
        r, g, b = x
        r, g, b = int(r*255), int(g*255), int(b*255)
        return r, g, b

    ########
    # rgbint to
    ########

    @staticmethod
    def rgbint2rgb(x):
        r, g, b = x
        r, g, b = r/255, g/255, b/255
        return r, g, b
    
    def rgbint2hsv(self, x):
        x = self.rgbint2rgb(x)
        color_hsv = tuple(matplotlib.colors.rgb_to_hsv(x))
        return color_hsv
    
    @staticmethod
    def rgbint2hex(x):
        r, g, b = x
        color_hex = "#{:02x}{:02x}{:02x}".format(r, g, b)  
        return color_hex.upper()          

    ########
    # hsv to
    ########
    
    @staticmethod
    def hsv2rgb(x):
        color_rgb = tuple(matplotlib.colors.hsv_to_rgb(x))
        return color_rgb
    
    def hsv2rgbint(self, x):
        color_rgb = self.hsv2rgb(x)
        return self.rgb2rgbint(color_rgb)
    
    def hsv2hex(self, x):
        color_rgb = tuple(matplotlib.colors.hsv_to_rgb(x))
        r, g, b = self.rgb2rgbint(color_rgb)
        color_hex = "#{:02x}{:02x}{:02x}".format(r, g, b)
        return color_hex.upper()          
    
    #########
    # call
    #########
    
    def __call__(self, x, from_, to_):
        assert from_ in ["string", "rgb" ,"rgbint", "hex", "hsv"]
        assert to_ in ["rgb" ,"rgbint", "hex", "hsv"]
        # rgb
        if from_ == "rgb":
            if to_ == "hsv":
                return self.rgb2hsv(x)
            elif to_ == "hex":
                return self.rgb2hex(x)
            elif to_ == "rgbint":
                return self.rgb2rgbint(x)
        # rgbint
        if from_ == "rgbint":
            if to_ == "hsv":
                return self.rgbint2hsv(x)
            elif to_ == "hex":
                return self.rgbint2hex(x)
            elif to_ == "rgb":
                return self.rgbint2rgb(x)                
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
                return self.hsv2rgb(x)
            elif to_ == "rgbint":
                return self.hsv2rgbint(x)
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


