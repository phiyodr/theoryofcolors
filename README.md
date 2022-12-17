# :art: Theory Of Colors

**Functionalities to work with colors**

> Theory of Colours (German: Zur Farbenlehre) is a book by Johann Wolfgang von Goethe about the poet's views on the nature of colours and how these are perceived by humans -- [Wikipedia](https://en.wikipedia.org/wiki/Theory_of_Colours)


## :information_source: Install

* Install from GitHub

```bash
pip install git+https://github.com/phiyodr/theoryofcolors
```

* Install from PyPI

```bash
pip install theoryofcolors
```

## :arrow_right: Functionalities

* `ColorCast`: Cast colors
* `NearestColor`: Find nearest color to any possible color (using text embedding similarity) 
* `ColorComplement`: Return opposite color 

### :one: Convert colors from/to RGB (0-1 floats), RGB (0-255 int) HEX, HSV and strings

```python
from theoryofcolors import ColorCast

cc = ColorCast()

print(cc("#FF0000", from_="hex", to_="hsv"))
print(cc((1.0,0.,0.), "rgb", "rgbint"))
print(cc("red", "string", "rgb"))

```

### :two: Find nearest color to given string

* Similarity is calculated based on text embedding similarity (cosine similarity) between given word a prefined reference list of color names.
* `model_name`: You can use any model from [sentence-transformers](https://www.sbert.net/docs/pretrained_models.html). Default is `all-distilroberta-v1`.
* `reference_colors`: You can choose between four diffrent reference color lists:
	* 8 `base` colors
	* [949](https://blog.xkcd.com/2010/05/03/color-survey-results/) `xkcd` colors
	* 148 `css4` colors
	* `all` colors (1048 colors in total)


```python
from theoryofcolors import NearestColor

nc = NearestColor()

# Nearest output as string
print(nc(color_string="green"))
print(nc("lemon green"))
print(nc("toxic green"))

# Nearest output as colorized string (works in terminal and jupyter notebook)
nc.print("lightblue")
nc.print("blue")
nc.print("darkblue")

# Use an other embedding model
nc = NearestColor(model_name='all-mpnet-base-v2')
nc.print("pink", arrow=True)
nc.print("orange", arrow=True)
nc.print("darkblue", arrow=True)

# Use other reference colors (match to 8 base colors only)
nc = NearestColor(reference_colors="base")
nc.print("pink", arrow=True)
nc.print("orange", arrow=True)
nc.print("darkblue", arrow=True)
```

### :three: Find complement color

```python
from theoryofcolors import ColorComplement

comp = ColorComplement()

comp((1,0,0), from_="rgb", to_="hex")
comp((1,1,1), "rgb")
comp((.5,0,0), "rgb")
```

### :four: Misc

```python
from theoryofcolors.misc import load_color_dict

# Map string to hex
color_mapper = load_color_dict("base") # 8 colors
color_mapper = load_color_dict("xkcd") # 949 colors
color_mapper = load_color_dict("css4") # 148 colors
color_mapper = load_color_dict("all")  # 1048 colors
```


:sunflower: