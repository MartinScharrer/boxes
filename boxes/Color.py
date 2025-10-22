class Color:
    BLACK   = [ 0.0, 0.0, 0.0 ]
    BLUE    = [ 0.0, 0.0, 1.0 ]
    GREEN   = [ 0.0, 1.0, 0.0 ]
    RED     = [ 1.0, 0.0, 0.0 ]
    CYAN    = [ 0.0, 1.0, 1.0 ]
    YELLOW  = [ 1.0, 1.0, 0.0 ]
    MAGENTA = [ 1.0, 0.0, 1.0 ]
    WHITE   = [ 1.0, 1.0, 1.0 ]

    # TODO: Make this configurable
    OUTER_CUT = BLACK
    INNER_CUT = BLUE
    ANNOTATIONS = RED
    ETCHING = GREEN
    ETCHING_DEEP = CYAN


from enum import Enum

class LightBurnColor(Enum):
    """LightBurn's layer colors
       Source: https://docs.lightburnsoftware.com/2.0/Reference/UI/ColorPalette/#rgb-and-hex-codes-for-the-lightburn-color-palette
    """
    C00 = (0.0, 0.0, 0.0)  # black (#000000)
    C01 = (0.0, 0.0, 1.0)  # blue (#0000FF)
    C02 = (1.0, 0.0, 0.0)  # red (#FF0000)
    C03 = (0.0, 0.8784313725490196, 0.0)  # green (#00E000)
    C04 = (0.8156862745098039, 0.8156862745098039, 0.0)  # yellow-olive (#D0D000)
    C05 = (1.0, 0.5019607843137255, 0.0)  # orange (#FF8000)
    C06 = (0.0, 0.8784313725490196, 0.8784313725490196)  # cyan (#00E0E0)
    C07 = (1.0, 0.0, 1.0)  # magenta (#FF00FF)
    C08 = (0.7058823529411765, 0.7058823529411765, 0.7058823529411765)  # light gray (#B4B4B4)
    C09 = (0.0, 0.0, 0.6274509803921569)  # dark blue (#0000A0)
    C10 = (0.6274509803921569, 0.0, 0.0)  # dark red (#A00000)
    C11 = (0.0, 0.6274509803921569, 0.0)  # dark green (#00A000)
    C12 = (0.6274509803921569, 0.6274509803921569, 0.0)  # olive (#A0A000)
    C13 = (0.7529411764705882, 0.5019607843137255, 0.0)  # golden brown (#C08000)
    C14 = (0.0, 0.6274509803921569, 1.0)  # sky blue (#00A0FF)
    C15 = (0.6274509803921569, 0.0, 0.6274509803921569)  # purple (#A000A0)
    C16 = (0.5019607843137255, 0.5019607843137255, 0.5019607843137255)  # gray (#808080)
    C17 = (0.49019607843137253, 0.5294117647058824, 0.7254901960784313)  # lavender blue (#7D87B9)
    C18 = (0.7333333333333333, 0.4666666666666667, 0.5176470588235295)  # rose brown (#BB7784)
    C19 = (0.2901960784313726, 0.43529411764705883, 0.8901960784313725)  # cobalt blue (#4A6FE3)
    C20 = (0.8274509803921568, 0.24705882352941178, 0.41568627450980394)  # pink red (#D33F6A)
    C21 = (0.5490196078431373, 0.8431372549019608, 0.5490196078431373)  # light green (#8CD78C)
    C22 = (0.9411764705882353, 0.7254901960784313, 0.5529411764705883)  # peach (#F0B98D)
    C23 = (0.9647058823529412, 0.7686274509803922, 0.8823529411764706)  # light pink (#F6C4E1)
    C24 = (0.9803921568627451, 0.6196078431372549, 0.8313725490196079)  # pink (#FA9ED4)
    C25 = (0.3137254901960784, 0.0392156862745098, 0.47058823529411764)  # dark violet (#500A78)
    C26 = (0.7058823529411765, 0.35294117647058826, 0.0)  # brown (#B45A00)
    C27 = (0.0, 0.2784313725490196, 0.32941176470588235)  # teal (#004754)
    C28 = (0.5254901960784314, 0.9803921568627451, 0.5333333333333333)  # neon green (#86FA88)
    C29 = (1.0, 0.8588235294117647, 0.4)  # light yellow (#FFDB66)
    T1 = (0.9529411764705882, 0.4117647058823529, 0.14901960784313725)  # tool 1 orange (#F36926)
    T2 = (0.047058823529411764, 0.5882352941176471, 0.8509803921568627)  # tool 2 blue (#0C96D9)

    # Named Colors (aliases)
    BLACK = C00.value
    BLUE = C01.value
    RED = C02.value
    GREEN = C03.value
    YELLOW_OLIVE = C04.value
    ORANGE = C05.value
    CYAN = C06.value
    MAGENTA = C07.value
    LIGHT_GRAY = C08.value
    DARK_BLUE = C09.value
    DARK_RED = C10.value
    DARK_GREEN = C11.value
    OLIVE = C12.value
    GOLDEN_BROWN = C13.value
    SKY_BLUE = C14.value
    PURPLE = C15.value
    GRAY = C16.value
    LAVENDER_BLUE = C17.value
    ROSE_BROWN = C18.value
    COBALT_BLUE = C19.value
    PINK_RED = C20.value
    LIGHT_GREEN = C21.value
    PEACH = C22.value
    LIGHT_PINK = C23.value
    PINK = C24.value
    DARK_VIOLET = C25.value
    BROWN = C26.value
    TEAL = C27.value
    NEON_GREEN = C28.value
    LIGHT_YELLOW = C29.value
    TOOL_ORANGE = T1.value
    TOOL_BLUE = T2.value

    @classmethod
    def from_rgb(cls, rgb_tuple, tol=1e-6):
        """
        Return the LightBurnColor matching the given (r, g, b) float tuple.
        Allows a small tolerance for floating-point rounding.
        """
        r, g, b = rgb_tuple
        for color in cls:
            cr, cg, cb = color.value
            if abs(cr - r) < tol and abs(cg - g) < tol and abs(cb - b) < tol:
                return color
        return None

    @classmethod
    def index_from_rgb(cls, rgb_tuple):
        """Return the index (0-29) of the LightBurnColor member matching the given (r, g, b) tuple."""
        color = cls.from_rgb(rgb_tuple)
        if color is not None:
            idx = int(color.name[1:])
            if color.name.startswith('T'):
                idx += 29  # Tool colors T1, T2 mapped to 30, 31
            return idx
        return None
