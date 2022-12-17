from theoryofcolors import ColorCast

class ColorComplement:

    @staticmethod
    def complement(r, g, b):
        # https://stackoverflow.com/a/40234924
        def hilo(a, b, c):
            if c < b: b, c = c, b
            if b < a: a, b = b, a
            if c < b: b, c = c, b
            return a + c

        k = hilo(r, g, b)
        return tuple(k - u for u in (r, g, b))
    
    def __call__(self, color, from_="rgb", to_="rgb"):
        """Convert color to complement

        Args:
            color (`string` or `tuple`): Color to complent.
            from_ (`string`): Input color type. Something of "string", "rgb", "hex", "hsv".
            to_ (`string`): Output color type. Something of "string", "rgb", "hex", "hsv".

        """
        cast = ColorCast()
        
        if from_ != "rgb":
            color = cast(color, from_, to_="rgb")
        op = self.complement(*color)
        if from_ != "rgb":
            op = cast(op, from_="rgb", to_=to_)
        return op
   
if __name__ == '__main__':
    comp = ColorComplement()
    comp((1,1,0), "rgb")