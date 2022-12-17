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

class NearestColor:
    
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


if __name__ == '__main__':
    nc = NearestColor()
    print(nc)
    nc.print("lightblue")
    nc.print("blue")
    nc.print("darkblue")

    print(nc("green"))
    print(nc("lemon green"))
    print(nc("toxic green"))

