from GraphicBase122 import *


class Tk:
    def __init__(self):
        self.title = ""
        className = str(self)
        if (className in ["Main"]):
            self.attr_obj = None
            self.showIndicator = True
        if (className in ["Frame"]):
            self.showIndicator = False

        if (className in ["Main", "Frame"]):

            self.CreateObject()
        elif (className in ["Button", "Label"]):
            self.showIndicator = False
            self.AddToObject()

    def CreateObject(self):
        if (self.attr_obj == None):
            self.object = tkObject(self, self.geometry)
            self.object.showIndicator = self.showIndicator
        else:
            self.object = tkObject(self, self.geometry, self.attr_obj.object,
                                   anchor=self.anchor, bg=self.bg,
                                   packPadx=self.packPadx, packPady=self.packPady)

    def AddToObject(self):
        self.attr_obj.object.addElement(self)

    def __repr__(self):
        return "Main"

    @property
    def geometry(self):
        try:
            geometry = self._geometry.split("*")
            width = geometry[0]
            height = geometry[1]
            return int(width), int(height)
        except AttributeError:
            self._geometry = "500*500"  # Default Setting
            return 500, 500

    @geometry.setter
    def geometry(self, value):
        self._geometry = value
        self.object.signDimension(self.geometry)  # reSet Coordinate

    def mainloop(self):
        width, depth = self.geometry
        title = self.title
        main(width, depth, title)

    # useful methods:

    def pack(self, anchor="c", padx=0, pady=0):
        if (str(self) in ["Label", "Button", "Entry"]):
            self.showIndicator = True
            self.packPady = pady
            self.packPadx = padx
            self.packAnchor = anchor
            self.coordinate = self.attr_obj.object.getElementRelativeCoordinate(self)
            self.JVL_color = "black"


class Label(Tk):
    def __init__(self, master, anchor="c", bg=None, bd=0, text="",
                 font=(), padx=1, pady=1,
                 width=0, height=0, image=None):
        # master declare
        self.attr_obj = master

        # variabel of box declare
        self.bg = bg
        self.bd = bd
        self.packPady = 1
        self.packPadx = 1
        self.packAnchor = "c"
        self.width = width
        self.height = 1.2 if height == 0 else height

        # variable of text declare
        self.anchor = anchor
        self.padx = padx
        self.pady = pady
        self.text = text
        self.font = font

        fontHeight, fontLength = self.setFont(font)
        # to make the label(box) can contain.
        if (fontHeight > self.height):
            self.height = fontHeight + 2 * pady
        if (fontLength > self.width):
            self.width = fontLength + 2 * padx

        super(Label, self).__init__()

    def setFont(self, font):
        # @TODO: maybe rework on the font size, using PIL
        if (font == ()):
            # consider default setting
            # format: font-type, font-size, font-config
            self.font = ("Time", 10, "bold")  # in pixel
        # consider the relation bettwen fontsize and pixcel as (fontsize/72)*96
        fontHeight = self.font[1] * 1.33333333
        fontLength = self.font[1] * 1.33333333 * len(self.text)

        return fontHeight, fontLength

    def __repr__(self):
        return "Label"


class Button(Label):
    # the ONLY difference is that the button have an "Animation"
    # and it shall call the function or method when click it
    # and according to the tkinter characteristic
    # the mouseclick and mouse-release shall have same location:
    def __init__(self, master, anchor="c", bg=None, bd=0, text="",
                 font=(), padx=1, pady=1,
                 width=0, height=0, image=None, command=None):
        Label.__init__(self, master, anchor=anchor, bg=bg, bd=bd, text=text,
                       font=font, padx=padx, pady=pady,
                       width=width, height=height,
                       image=image)
        self.command = command
        self.clickFlag = False
        self.buttonColorUp = "gray"
        self.buttonColorDown = "white"

    # not time for setFont
    """def setFont(self,font):
        # high and width is most important
        pass"""

    def executeCommand(self):
        if (self.command != None):
            self.command()

    def __repr__(self):
        return "Button"


class Entry(Button):
    def __init__(self, master, anchor="c", bg=None, bd=0, padx=1, pady=1,
                 width=0, height=0):
        Button.__init__(self, master, anchor=anchor, bg=bg, bd=bd, width=width, height=height)
        self.ElementStore = []

    def get(self):
        # only consider str and int
        resStr = ""
        isDigitFlag = True
        for element in self.ElementStore:
            if (not element.isDigit and element != "."):
                isDigitFlag = False
            resStr += element
        if (isDigitFlag):
            return float(resStr)
        else:
            return resStr

    def __repr__(self):
        return "Entry"


class Frame(Tk):
    def __init__(self, master, width=0, height=0, bg=None, ):
        self.attr_obj = master
        super(Frame, self).__init__()

        # Frame variable declar
        self.bg = bg
        self.width = width
        self.height = height
        self.geometry = f"{width * height}"

        # variables defined by the pack() method
        self.packPady = 1
        self.packPadx = 1
        self.anchor = "c"

    def __repr__(self):
        return "Frame"

    pass
