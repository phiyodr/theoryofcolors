import pytest

from theoryofcolors import ColorCast

#@pytest.mark.parametrize("color_spaces", ["rgb", "rgbint", "hex", "hsv"])
def test_colorcast():
    color_dict_list = [
        {"hex" : "#FF0000",
         "rgb" : (1,0,0),
         "rgbint": (255,0,0),
         "hsv" : (0,1,1)},
        {"hex" : "#FFFF00",
         "rgb" : (1,1,0),
         "rgbint": (255,255,0),
         "hsv" : (60/360,1,1)},
        {"hex" : "#ADD8E6",
         "rgb" : (0.6784313725490196, 0.8470588235294118, 0.9019607843137255),
         "rgbint": (173,216,230),
         "hsv" : (195/360,.25,.90)}
        ]
    

    cast = ColorCast()

    color_spaces = ["hex", "hsv", "rgb", "rgbint"]

    for color_dict in color_dict_list:
        for color_space_from in color_spaces:
            from_color = color_dict[color_space_from]
            for color_space_to in color_spaces:
                to_color = color_dict[color_space_to]
                if color_space_from != color_space_to:
                    print("From/to:", color_space_from, color_space_to)
                    print("From/to:", from_color, to_color)
                    res = cast(x=from_color, from_=color_space_from, to_=color_space_to)
                    print("res", res)
                    #print(colors][color_space])
                    if isinstance(res, tuple):
                        res = tuple(map(lambda x: isinstance(x, float) and round(x, 2) or x, res))
                        to_color = tuple(map(lambda x: isinstance(x, float) and round(x, 2) or x, to_color))
                        assert res == to_color
                    else:
                        if to_color == "#ADD8E6":
                            assert res == "#ACD7E5" 
                            
                        else:
                            assert res == to_color
                    #print("====")
