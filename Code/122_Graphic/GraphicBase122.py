from cmu_112_graphics import *


# we shall consider each tk and tk.frame as objects
# label and buttons and etc are elements in it.
class tkObjectList:
    __Objectlist = []

    def __init__(self):
        pass

    def addToList(self, obj):
        tkObjectList.__Objectlist.append(obj)

    def getList(self):
        return tkObjectList.__Objectlist

    def __repr__(self):
        return "tkObjectList"


class tkObject(tkObjectList):
    def __init__(self, obj, geometry, attr=None, **kwargs):
        super(tkObjectList, self).__init__()
        self.name = str(obj)

        self.signDimension(geometry)
        self.showIndicator = False

        self.OwnElement = []
        self.OwnObject = []
        self.attrObject = attr

        if (kwargs != {}):  # Frame
            self.anchor = kwargs["anchor"]
            self.packPadx = kwargs["packPadx"]
            self.packPady = kwargs["packPady"]
            self.bg = kwargs["bg"]

        self.addToList(self)

    def signDimension(self, geometry):
        self.width = geometry[0]
        self.height = geometry[1]

        self.RelativeCoordinate = self.getRelativeCoordinate()  # formate (x,y,width,height)

    def getRelativeCoordinate(self):
        if (self.name in ["Main", "Frame"]):
            if (self.name in ["Main"]):
                return (0, 0, self.width, self.height)  # x,y, width,height
            if (self.name in ["Frame"]):
                # simulate the Superposition function of tkinter
                addUp = 0
                for object in self.attrObject.OwnObject:
                    addUp += object.height
                    addUp += object.packPady
                    if (addUp >= self.attrObject.height):
                        raise Exception("Widget Size over Limit")
                x, y = (0, 0)
                attrX, attrY, attrWidth, attrHeight = self.attrObject.RelativeCoordinate

                if (self.anchor == "c"):
                    x = (attrWidth / 2 - self.width / 2) + attrX
                    y = attrY

                if (self.anchor == "w"):
                    x = attrX
                    y = attrY

                if (self.anchor == "e"):
                    x = attrWidth
                    y = attrY

                if (self.anchor == "s"):
                    x = (attrWidth / 2 - self.width / 2) + attrX
                    y = attrHeight

                y += addUp

                return (x, y, self.width, self.height)

    def addElement(self, element):
        self.OwnElement.append(element)

    def getElementRelativeCoordinate(self, element):
        # explain: the label is composed by at lease one rectangle, the text is not necessary but rectangle mush be drawn.
        # thus, we need the 4 coordinate of rectangle, x,x1,y,y1
        # and the coordinate of text, xt,yt
        # all x,x1,xt,y,y1,yt depend on the master x,y,width,height, which are xM,yM,widthM,heightM
        xM, yM, widthM, heightM = self.RelativeCoordinate
        # configure the box's dimension
        if (element.packAnchor == "c"):
            x = xM + (widthM / 2 - element.width / 2)
            x1 = xM + (widthM / 2 + element.width / 2)
            y = yM + element.packPady
            y1 = yM + element.height + element.packPady
        if (element.packAnchor == "w"):
            x = xM + element.packPadx
            x1 = xM + element.width + element.packPadx
            y = yM + element.packPady
            y1 = yM + element.height + element.packPady
        if (element.packAnchor == "e"):
            x = widthM - element.packPadx
            x1 = widthM - element.packPadx - element.width
            y = yM + element.packPady
            y1 = yM + element.height + element.packPady
        if (element.packAnchor == "s"):
            x = xM + (widthM / 2 - element.width / 2)
            x1 = xM + (heightM / 2 + element.width / 2)
            y = heightM - element.packPady
            y1 = heightM - element.height - element.packPady

        try:

            # get the nth element of OwnElement's coordinate set's height value
            add = yM
            minus = heightM

            if (len(self.OwnElement) == 1):  # first element
                return (x, x1, y, y1)

            else:
                index = self.OwnElement.index(element)
                privousElment = None
                while (index > 0):
                    index -= 1
                    if (element.packAnchor == "s"
                            and self.OwnElement[index].packAnchor == element.packAnchor):
                        privousElment = self.OwnElement[index]
                        break
                    elif (element.packAnchor in ["c", "w", "e"]):
                        if (self.OwnElement[index].packAnchor in ["c", "w", "e"]):
                            privousElment = self.OwnElement[index]
                            break

                if (privousElment != None):  # not first of its kind
                    add = privousElment.coordinate[-1]  # y1
                    minus = privousElment.coordinate[-2]  # y

                if (element.packAnchor != "s"):
                    return (x, x1, y + add, y1 + add)
                elif (element.packAnchor == "s"):
                    return (x, x1, minus - element.height, minus)




        except BaseException:
            raise Exception("Unknown anchor input!")

    def __repr__(self):
        return "tkObject"


# --------------------------------------------------
# ------------------MVC_PART------------------------
# --------------------------------------------------

def appStarted(app):
    app.tkObjectList = tkObjectList()
    app.clickFlag = False
    app.clickObject = None
    app.timeCounter = 0


# section of Generate Graphic

def redrawAll(app, canvas):
    drawBase(app, canvas)


def drawBase(app, canvas):
    for tkObject in app.tkObjectList.getList():
        if (tkObject.showIndicator):
            for element in tkObject.OwnElement:

                if (str(element) in ["Label", "Button", "Entry"] and element.showIndicator):
                    drawLabel_Button_Entry(app, canvas, element)


def drawLabel_Button_Entry(app, canvas, element):
    # draw base of these elements
    x, x1, y, y1 = element.coordinate
    xt = (x1 - x) / 2 + x
    yt = (y1 - y) / 2 + y

    canvas.create_rectangle(x, y,
                            x1, y1,
                            fill=element.bg,
                            width=element.bd)
    if (element.text != ""):
        font122 = ""
        for ele in element.font:
            font122 += f"{ele} "
        font122.rstrip(" ")
        canvas.create_text(xt, yt, text=element.text, font=font122)

    # configuration base on special type (Button, Entry)

    if (str(element) in ["Button", "Entry"]):
        # draw the border of the button to make it looks like a button and Entry
        # Up part
        canvas.create_line(x, y, x, y1, width=element.bd + 1, fill=element.buttonColorUp)
        canvas.create_line(x, y, x1, y, width=element.bd + 1, fill=element.buttonColorUp)
        # DownPart
        canvas.create_line(x1, y1, x, y1, width=element.bd + 1, fill=element.buttonColorDown)
        canvas.create_line(x1, y1, x1, y, width=element.bd + 1, fill=element.buttonColorDown)
        # draw the button/Entry border
        canvas.create_rectangle(x - 1, y - 1,
                                x1 + 1, y1 + 1, outline="gray")
        # draw configuration on Entry
        if (str(element) == "Entry" and element.clickFlag):
            # @TODO: finish this text adding part
            xJ, yJ, y1J = x, y, y1  # a vertical line
            for elementStr in element.ElementStore:
                pass


def mousePressed(app, event):
    # consider the animation of click
    keyX = event.x
    keyY = event.y
    for tkObject in app.tkObjectList.getList():
        if (tkObject.showIndicator):
            for element in tkObject.OwnElement:
                if (str(element) == "Button"):
                    # Button don't need click-flag for constant happening event
                    x, x1, y, y1 = element.coordinate
                    if (checkMouse((x, x1, y, y1), (keyX, keyY))):
                        app.clickObject = element
                        element.buttonColorUp = "white"
                        element.buttonColorDown = "gray"
                    # Entry need click-flag for constant happening event
                elif (str(element) == "Entry"):
                    if (checkMouse((element.coordinate), (keyX, keyY))):
                        app.clickObject = element
                        element.clickFlag = True
                    else:
                        element.clickFlag = False


def mouseReleased(app, event):
    if (app.clickObject != None):
        if (str(app.clickObject) == "Button"):
            app.clickObject.buttonColorUp = "gray"
            app.clickObject.buttonColorDown = "white"
            # tkinter characteristic: only when the cursor released at the button area, call command
            if (checkMouse(app.clickObject.coordinate, (event.x, event.y))):
                app.clickObject.executeCommand()
                app.clickObject = None


def mouseMoved(app, event):
    pass


def timerFried(app):
    if (app.clickObject.clickFlag):
        app.timeCounter += 100
        if (app.timeCounter >= 200):
            app.timeCounter = 0
            app.clickObject.JVL_color = "white" if app.clickObject.JVL_color == "black" else "white"


def checkMouse(coordinate, mouse):
    x, x1, y, y1 = coordinate
    keyX, keyY = mouse
    if (x <= keyX <= x1 and y <= keyY <= y1):
        return True
    return False


def keyPressed(app, event):
    pass


def main(w, d, title=""):
    if (title == ""):
        runApp(width=w, height=d)
    else:
        runApp(width=w, height=d, title=title)
