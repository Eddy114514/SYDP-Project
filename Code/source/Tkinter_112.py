from GraphicBase112 import *


class Tk:
    def __init__(self, bg="#f0f0f0"):
        self.title = ""
        self.bg = bg
        className = str(self)
        if (className in ["Main"]):
            self.attr_obj = None
            self.showIndicator = True
        if (className in ["Frame"]):
            self.showIndicator = False

        if (className in ["Main", "Frame"]):
            self.CreateObject()
        elif (className in ["Button", "Label", "Entry"]):
            self.showIndicator = False
            self.AddToObject()

    def CreateObject(self):
        self.object = tkObject(self, self.geometry)
        self.object.showIndicator = self.showIndicator

    def AddToObject(self):
        self.attr_obj.object.addElement(self)

    def configure(self, **kwargs):
        OwnEle = self.attr_obj.object.OwnElement
        replaceIndex = OwnEle.index(self)
        for keyword in kwargs:
            if (keyword == "bg"):
                self.bg = kwargs[keyword]
            if (keyword == "text"):
                self.text = kwargs[keyword]

        OwnEle[replaceIndex] = self

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
            if (str(self) == "Entry"):
                self.JVL_color = "black"
            self.pairImage()

    def grid(self, column=0, row=0):
        self.showIndicator = True
        self.gridRow = row
        self.gridcolum = column
        self.isGrid = True
        if (str(self) == "Entry"):
            self.JVL_color = "black"

        self.coordinate = self.attr_obj.gridFrame(self, column=column, row=row)
        self.pairImage()

    def destroy(self):
        self.attr_obj.object.OwnElement.remove(self)
        del self


class Label(Tk):
    def __init__(self, master, anchor="c", bg=None, bd=0, text="",
                 font=(), padx=1, pady=1,
                 width=0, height=0, image=None):
        # master declare
        self.attr_obj = master
        super(Label, self).__init__()

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

        self.setFont(font)
        self.PairText()

        # image
        self.imageAddress = image

        # grid
        self.isGrid = False

    def pairImage(self):
        if (self.imageAddress != None):
            self.text = ""  # if image, then no text
            x, x1, y, y1 = self.coordinate
            self.xImage = x + (x1 - x) / 2
            self.yImage = y + (y1 - y) / 2
            PILImage = Image.open(self.imageAddress)
            self.image = PILImage

    # leanred how to use ImageFont of Pillow library from
    # https://codeantenna.com/a/Lb2aX5Xcqp
    # This is a Chinese website
    def setFont(self, font):
        if (str(self) == "Entry"):
            return None  # save time
        if (font == ()):
            # consider default setting
            # format: font-type, font-size, font-config
            self.font = ("Time", 10, "bold")  # in pixel
        font = ImageFont.truetype(f"{FontBase(self.font)}", self.font[1] + 5)
        self.fontLength, self.fontHeight = font.getsize(self.text)

    def PairText(self):
        # to make the label(box) can contain.
        if (self.fontHeight > self.height):
            self.height = self.fontHeight + 2 * self.pady
        if (self.fontLength > self.width):
            self.width = self.fontLength + 2 * self.padx

    def __repr__(self):
        return "Label"


class Button(Label):
    # the ONLY difference is that the button have an "Animation"
    # and it shall call the function or method when click it
    # and according to the tkinter characteristic
    # the mouseclick and mouse-release shall have same location:
    def __init__(self, master, anchor="c", bg=None, bd=0, text="",
                 font=(), padx=1, pady=1,
                 width=0, height=0, image=None, command=None, destroySelf=False):
        Label.__init__(self, master, anchor=anchor, bg=bg, bd=bd, text=text,
                       font=font, padx=padx, pady=pady,
                       width=width, height=height,
                       image=image)
        self.command = command
        self.clickFlag = False
        self.buttonColorUp = "white"
        self.buttonColorDown = "black"
        self.destroySelf = destroySelf

    def PairText(self):

        if (self.text == ""):
            return None
        # to make the text can be contained.
        while (self.fontHeight > self.height or self.fontLength > self.width):
            if (self.font[1] <= 6):  # if too small, then pair box
                self.height = self.fontHeight
                self.width = self.fontLength
                break
            else:  # diminish the font to pair the box
                self.font = (self.font[0], self.font[1] - 1, self.font[-1])
                self.setFont(self.font)

    def executeCommand(self):
        if (self.command != None):
            self.command()
            if (self.destroySelf):
                self.destroy()

    def __repr__(self):
        return "Button"


class Entry(Button):
    def __init__(self, master, anchor="c", bg="white", bd=0, padx=1, pady=1,
                 width=50, height=10, command=None, deflautReturn=None):
        Button.__init__(self, master, anchor=anchor, bg=bg, bd=bd, width=width, height=height, command=command)
        self.ElementStore = ""
        self.buttonColorUp = "gray"
        self.buttonColorDown = "white"
        self.InputFontSize = 10  # deflaut
        self.determineIFS()
        self.deflautReturn = deflautReturn
        self.strTrack = 0

    def determineIFS(self):

        self.Inputfont = ImageFont.truetype(f"{FontBase(('Time', self.InputFontSize, ''))}", self.InputFontSize)
        self.fontLength, self.fontHeight = self.Inputfont.getsize("J")  # test words
        while (self.fontHeight >= self.height):
            self.InputFontSize -= 1
            self.Inputfont = ImageFont.truetype(f"{FontBase(('Time', self.InputFontSize, ''))}",
                                                self.InputFontSize)
            self.fontLength, self.fontHeight = self.Inputfont.getsize("Hellow World")  # test words

    def get(self):
        # only consider str and int
        if (self.ElementStore == ""):
            return self.deflautReturn

        elif (self.ElementStore.isdigit()):
            if (self.ElementStore.isdecimal()):
                return float(self.ElementStore)
            return int(self.ElementStore)
        else:
            return self.ElementStore

    def executeCommand(self):
        # only execute once
        if (self.command != None):
            self.command()
            self.command = None

    def __repr__(self):
        return "Entry"


class Frame(Tk):
    def __init__(self, master, width=0, height=0, bg=None, bd=0, anchor="c", padx=0, pady=1):
        self.attr_obj = master

        # Frame variable declar
        self.bg = bg
        self.bd = bd
        self.width = width
        self.height = height
        self.anchor = anchor
        self.padx = padx
        self.pady = pady

        self.isGrid = False

        # create Frame Object
        super(Frame, self).__init__(bg=bg)

    def configure(self, **kwargs):
        for keyword in kwargs:
            if (keyword == "bg"):
                self.object.bg = kwargs[keyword]

    def CreateObject(self):

        self.object = tkObject(self, (self.width, self.height), self.attr_obj.object, bg=self.bg,
                               padx=self.padx, pady=self.pady, bd=self.bd)
        self.object.showIndicator = True
        self.object.attrObject.OwnObject.append(self.object)  # connect to master at the Graphic base 112

    def pack(self, anchor="c", pady=0, padx=0, fill=None):
        self.object.packPadx = padx
        self.object.packPady = pady
        self.object.anchor = anchor
        if (fill != None):
            if (fill.upper() not in ["X", "Y", "BOTH"]):
                raise Exception("fill ket not included")
            self.object.fill = fill
        self.object.RelativeCoordinate = self.object.getRelativeCoordinate()

    def columnconfigure(self, col: int, row: int, weight=0):
        self.isGrid = True
        self.row = row
        self.col = col
        self.rowHeight = self.height / (2 * row)
        if (weight == 0):
            self.colWidth = (self.width / col) * 3
        else:
            self.colWidth = (self.width / col) * weight

    def gridFrame(self, element, column=0, row=0):
        Fx = self.object.RelativeCoordinate[0]
        Fy = self.object.RelativeCoordinate[1]
        x = Fx + column * self.colWidth + 10
        x1 = x + element.width
        y = Fy + (row) * self.rowHeight
        y1 = y + element.height
        return x, x1, y, y1

    def destroy(self):
        self.object.removeObject(self.object)
        self.attr_obj.object.OwnObject.remove(self.object)
        del self

    def destroyAllElement(self):
        self.object.OwnElement = []

    def __repr__(self):
        return "Frame"
