from IPython import get_ipython
from matplotlib import colors as mcolors
import copy

def is_notebook():
    if get_ipython():
        return True
    else:
        return False


def get_base_dict():
    """Dict from 8 base color names to hex values."""
    base_list = ["blue","red", "green", "cyan", "magenta", "yellow", "black", "white"]
    base_colors = {}
    for color in base_list:
        base_colors[color] = get_css4_dict()[color]    
    return base_colors



def get_xkcd_dict():
    """Dict from 949 xkcd color names to hex values."""
    xkcd_colors_ = mcolors.XKCD_COLORS
    xkcd_colors = {}
    for key, value in xkcd_colors_.items():
        key_clean = key[5:]
        xkcd_colors[key_clean] = value
    return xkcd_colors

def get_css4_dict():
    """Dict from 148 xkcd colors to hex values."""
    return mcolors.CSS4_COLORS

def load_color_dict(name="all"):
    """Dict from color names to hex values."""
    if name == "base":
        # 8 colors
        return get_base_dict()
    elif name == "xkcd":
        # 949 colors (base included)
        return get_xkcd_dict()
    elif name == "css4":
        # 148 colors (base included)
        return get_css4_dict()
    elif name == "all":
        # 1048 colors
        xkcd_colors = get_xkcd_dict()
        css4_colors = get_css4_dict()
        return copy.deepcopy(dict(xkcd_colors, **css4_colors))

if __name__ == '__main__':
    color_list = load_colors("all")
    print(len(color_list))