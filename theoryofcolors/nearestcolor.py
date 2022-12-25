# Theory of Colours
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
from IPython.display import HTML as html_print
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import copy
from stringcolor import cs 
from theoryofcolors.misc import load_color_dict, is_notebook
from theoryofcolors.colorcast import ColorCast
from copy import deepcopy


class NearestColorViaEmbedding:
    
    def __init__(self, color_string=None, model_name='all-distilroberta-v1', reference_colors="all"):
        self.color_mapper = load_color_dict(reference_colors) 
        self.color_list = list(self.color_mapper.keys())
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.all_color_embeddings = self.model.encode(self.color_list)
        self.color_len = len(self.color_list)
        self.color_string = color_string

        
    def set_color_strings(self, color_string):
        self.color_string = color_string

    def nearest(self, color_string, top_n=5, output=False):
        # Set colors
        if color_string == None:
            color_string = self.color_string
        # Set top_m
        if top_n == None:
            top_n = self.color_len
            
        # Similary 
        color_embeddings = self.model.encode([color_string])
        #import pdb; pdb.set_trace()

        sim_vector = cosine_similarity(color_embeddings, self.all_color_embeddings)[0]#.shape

        # Sort largest first, filter top_n first
        sorted_index_array = np.argsort(sim_vector)[::-1]
        sorted_array = sim_vector[sorted_index_array]
        idxs, vals = sorted_index_array[:top_n], sorted_array[:top_n]

        results_match_strings = []
        results_hex_strings = []
        for idx, val in zip(idxs, vals):
            match_string = self.color_list[idx]
            match_hex = self.color_mapper[match_string]
            #print(idx, val, match_string, match_hex)
            if output:
                display(html_print(f"idx:{idx:4} val={val:.2f} match={cstr(match_string, color=match_hex)}"))
            results_match_strings.append(match_string)
            results_hex_strings.append(match_hex)
        return results_match_strings, results_hex_strings

    def __call__(self, color_string, return_string=True, return_hex=False):
        results_match_strings, results_hex_strings = self.nearest(color_string, 1, False)
        return results_match_strings[0]


    def print(self, color_string, arrow=False):
        res = self.nearest(color_string, 1, False)
        match_string, match_hex = res[0][0], res[1][0]
        if arrow:
            string = f"{color_string} => {self.cstr(match_string, color=match_hex)}"
            if is_notebook():
                display(html_print(string))
            else:
                string = f"{color_string} => {cs(match_string, color=match_hex)}"
                print(string)
        else:
            string = match_string
            if is_notebook():
                display(html_print(string))
            else:
                print(color_string, string, match_string, match_hex)
                print(cs(string, color=match_hex))

    def __str__(self):
        return f'NearestColor with model={self.model_name} for {len(self.color_list)} possible colors.'


    @staticmethod
    def cstr(s, color='red'):
        return "<text style=color:{}>{}</text>".format(color, s)


class NearestColorViaColorSpace:
    """
    Convert RGB, HSV, and HEX colors to nearest string from reference colors.
    Use euclician distance based on RGB or HSV values.
    
    Args:
        reference_colors: Use reference colors from base, xkcd, css4, and all
        similarity_color_space: HSV or RGB
    """

    def __init__(self, reference_colors = "all", similarity_color_space="rgb"):
        assert reference_colors in ["base", "xkcd", "css4", "all"], 'Use reference_colors from ["base", "xkcd", "css4", "all"].'
        assert similarity_color_space in ["rgb", "hsv"],  'Use color_space from ["rgb", "hsv"].'
        self.reference_colors = reference_colors
        self.similarity_color_space = similarity_color_space
        self.cc = ColorCast()

        # reference colors
        color_dict =  load_color_dict(name=reference_colors)
        color_dict_new = {key: self.cc(value, from_="hex", to_=similarity_color_space) for (key, value) in color_dict.items()}
        self.df = pd.DataFrame(color_dict_new).T

    def nearest(self, color=(1.,0.,0.), from_="rgb",  to_="string",  top_k=3):
        """
        Return nearest color from reference colors.
        Use euclician distance using RGB or HSV color space.
        
        Args:
            color: Color definition using color space from `from_`.
            from_: Define color space for `color`
            to_: Define output color space (usually "string").
            top_k: Return top k results
            
        """
        assert from_ in ["rgb", "rgbint", "hex", "hsv"],  'Use from_ from ["rgb", "rgbint", "hex", "hsv"].'
        assert to_ in ["string"],  'Use to_ from ["string"].'
        
        # Input color to color spaces
        if from_== self.similarity_color_space:
            source_color = color
        else:
            source_color = self.cc(color, from_=from_, to_=self.similarity_color_space)
        source_color_new = np.array(source_color).reshape(1, 3)

        # Calc distances
        dist_vector = euclidean_distances(source_color_new, self.df.values)[0]
        best_idxs = self.topk(dist_vector, top_k, False)
        self.df_result = deepcopy(self.df.iloc[best_idxs])
        result_string_list = list(self.df_result.index)
        if to_ == "string":
            return result_string_list
        else:
            result = [self.cc(color_string, from_="string", to_=to_)  for color_string in result_string_list]
            return result

    @staticmethod
    def topk(x, k=5, maximum=True):
        if maximum:
            idxs = np.argpartition(x, -k)[-k:]  # Indices not sorted
            idxs = idxs[np.argsort(x[idxs])][::-1] 
        else:
            idxs = np.argpartition(x, k)[:k]  # Indices not sorted
            idxs[np.argsort(x[idxs])]  
        return idxs
    
    def __call__(self, color):
        
        return self.nearest(color, from_="rgb", to_="string", top_k=1)[0]

    def print(self, color, from_="rgb", arrow=False):
        source_color_asstr = str(color)
        source_color_hex = self.cc(color, from_=from_, to_="hex")

        target_color_str = self.nearest(color, from_=from_, to_="string",  top_k = 1)[0]
        target_color_hex = self.cc(target_color_str, from_="string", to_="hex")
        #print(target_color_str, from_)
        target_color_from_ = self.cc(target_color_str, from_="string", to_=from_)
        #print(target_color_from_)
        target_color_str_ = f"{target_color_str}, {from_}: {self.round_color(target_color_from_)}"
        if arrow:
            string = f"source color: {self.cstr(source_color_asstr, color=source_color_hex)} ====> target color: {self.cstr(target_color_str_, color=target_color_hex)}"
            if is_notebook():
                display(html_print(string))
            else:
                string = f"{cs(source_color_asstr, color=source_color_hex)} => {cs(target_color_str, color=target_color_hex)}"
                print(string)
        else:
            string = match_string
            if is_notebook():
                display(html_print(string))
            else:
                print(color_string, string, match_string, match_hex)
                print(cs(string, color=match_hex))


    @staticmethod
    def cstr(s, color='red'):
        return "<text style=color:{}>{}</text>".format(color, s)
   
    @staticmethod
    def round_color(color, decimal=2):
        color_ = list()
        for v in color:
            color_.append(round(v, decimal))
        return tuple(color_)       


if __name__ == '__main__':
    nc = NearestColorViaEmbedding()
    print(nc)
    nc.print("lightblue")
    nc.print("blue")
    nc.print("darkblue")

    print(nc("green"))
    print(nc("lemon green"))
    print(nc("toxic green"))

