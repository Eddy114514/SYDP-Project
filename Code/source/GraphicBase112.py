from cmu_112_graphics import *
import platform


# font base
fontdict = {"TIME": {"RE": "times.ttf", "BOLD": "timesbd.ttf", "ITALIC": "timesi.ttf"},
            "ARIAL": {"RE": "arial.ttf", "BOLD": "arialbd.ttf", "ITALIC": "ariali.ttf"}}


def FontBase(UserInput: tuple[str, int, str]) -> str:
    """
    :param UserInput: str
    :rtype: file-address str
    """
    Fonttype = UserInput[0].upper()
    Fontshowtype = UserInput[2].upper()

    try:
        if(platform.system().lower() == "windows"):
            if (Fontshowtype == ""):
                Fontshowtype = "RE"
            return fontdict[Fonttype][Fontshowtype]
        else:
            return "Times.ttc"


    except BaseException:
        raise Exception("UDF font type or font config, only support Time and Arial, Bold and Italic")


# we shall consider each tk and tk.frame as objects
# label and buttons, etc are elements in it.


class tkObjectList:
    __Objectlist = []
    MasterOfAll = None

    def __init__(self):
        pass

    def addToList(self, obj):
        if (obj.name == "Main"):
            tkObjectList.MasterOfAll = obj

        tkObjectList.__Objectlist.append(obj)

    def getList(self):
        return tkObjectList.__Objectlist

    def removeObject(self, obj):
        tkObjectList.__Objectlist.remove(obj)

    def __repr__(self):
        return "tkObjectList"


class tkObject(tkObjectList):
    def __init__(self, obj, geometry, attr=None, **kwargs):
        super(tkObjectList, self).__init__()
        # define object identities
        self.name = str(obj)
        self.bg = obj.bg
        self.showIndicator = False

        # object_element network
        self.OwnElement = []
        self.OwnObject = []
        self.attrObject = attr

        if (kwargs != {}):  # Frame or MessageBox

            if (self.name == "Frame"):
                # extra parmeters if is Frame
                self.padx = kwargs["padx"]
                self.pady = kwargs["pady"]
                self.bg = kwargs["bg"]
                self.bd = kwargs["bd"]
                self.obejct = obj

                # define by outside pack
                self.packPady = 0
                self.packPadx = 0
                self.anchor = "c"
                self.fill = None

            if (self.name == "Messagebox"):
                self.title = kwargs["title"]
                self.showIndicator = True

        # define object coordinates or relative coordinates
        self.signDimension(geometry)

        self.addToList(self)

    def signDimension(self, geometry):
        self.width = geometry[0]
        self.height = geometry[1]
        if (self.name == "Main"):
            # only window can call it from here
            self.RelativeCoordinate = self.getRelativeCoordinate()  # formate (x,y,width,height)

    def getRelativeCoordinate(self):
        if (self.name in ["Main", "Frame"]):
            if (self.name in ["Main"]):
                return (0, 0, self.width, self.height)  # x,y, width,height
            if (self.name in ["Frame"]):
                # simulate the Superposition function of tkinter
                addUp = 0
                index = self.attrObject.OwnObject.index(self)
                for obj in self.attrObject.OwnObject[:index]:  # find master
                    addUp += obj.RelativeCoordinate[1]
                    addUp += obj.height
                    addUp += obj.pady
                    if (addUp >= self.attrObject.height):
                        raise Exception("Widget Size over Limit")
                x, y = (0, 0)
                attrX, attrY, attrWidth, attrHeight = self.attrObject.RelativeCoordinate

                if (self.anchor == "c"):
                    x = (attrWidth / 2 - self.width / 2) + attrX
                    y = attrY + self.packPady

                elif (self.anchor == "w"):
                    x = attrX
                    y = attrY + self.packPady

                elif (self.anchor == "e"):
                    x = attrWidth
                    y = attrY + self.packPady

                elif (self.anchor == "s"):
                    x = (attrWidth / 2 - self.width / 2) + attrX
                    y = attrHeight - self.packPady

                y += addUp
                if (self.fill != None):
                    # consider cases of X, Y , BOTH
                    if (self.fill.upper() == "X"):
                        x = self.attrObject.RelativeCoordinate[0]
                        self.width = self.attrObject.width

                    elif (self.fill.upper() == "Y"):
                        self.height = self.attrObject.height

                    elif (self.fill.upper() == "BOTH"):
                        x = self.attrObject.RelativeCoordinate[0]
                        self.width = self.attrObject.width
                        self.height = self.attrObject.height

                    else:
                        raise Exception("Fill key not included")
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
                        if (self.OwnElement[index].packAnchor == element.packAnchor):
                            privousElment = self.OwnElement[index]
                            break

                if (privousElment != None):  # not first of its kind
                    xp, x1p, yp, y1p = privousElment.coordinate

                    add = y1p + privousElment.packPady  # y1
                    minus = yp + privousElment.packPady  # y

                if (element.packAnchor != "s"):
                    return (x, x1, add, add + element.height)
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
    app.messageBox = False


# section of Generate Graphic


def timerFired(app):
    if (app.clickObject != None and app.clickObject.clickFlag and str(app.clickObject) == "Entry"):
        app.timeCounter += 10
        if (app.timeCounter >= 20):
            app.timeCounter = 0
            try:
                if (app.clickObject.JVL_color == "white"):
                    app.clickObject.JVL_color = "black"
                else:
                    app.clickObject.JVL_color = "white"
            except:
                print("something might be wrong")

    # check window size
    if ((app.tkObjectList.MasterOfAll.width, app.tkObjectList.MasterOfAll.height) != (app.width, app.height)):
        # reset the windows
        app.tkObjectList.MasterOfAll.signDimension((app.width, app.height))
        # reset all object and its elements
        for tkObject in app.tkObjectList.getList():
            if (tkObject.name != "Main"):
                tkObject.obejct.pack(anchor=tkObject.anchor, padx=tkObject.packPadx, pady=tkObject.packPady)
            for element in tkObject.OwnElement:
                if (element.showIndicator):
                    if (element.isGrid):
                        element.grid(column=element.gridcolum, row=element.gridRow)
                    else:
                        element.pack(anchor=element.packAnchor, padx=element.packPadx, pady=element.packPady)


def redrawAll(app, canvas):
    if (app.messageBox):
        canvas.create_window((100, 150))
    drawWindow(app, canvas)
    drawBase(app, canvas)


def drawWindow(app, canavs):
    tkObject = app.tkObjectList.MasterOfAll
    canavs.create_rectangle(0, 0,
                            app.width, app.height, fill=tkObject.bg)


def drawBase(app, canvas):
    for tkObject in app.tkObjectList.getList():
        if (tkObject.showIndicator):
            if (tkObject.name == "Frame"):
                drawFrame(app, canvas, tkObject)
            for element in tkObject.OwnElement:
                if (str(element) in ["Label", "Button", "Entry"] and element.showIndicator):
                    drawLabel_Button_Entry(app, canvas, element)


def sortX(x, x1):
    if (x >= x1):
        return x1, x
    else:
        return x, x1


def drawFrame(app, canavs, tkobject):
    x, y, width, height = tkobject.RelativeCoordinate
    canavs.create_rectangle(x, y, x + width, y + height, width=tkobject.bd, fill=tkobject.bg)


def drawLabel_Button_Entry(app, canvas, element):
    # draw base of these elements
    x, x1, y, y1 = element.coordinate
    x, x1 = sortX(x, x1)
    xt = abs(x1 - x) / 2 + x
    yt = abs(y1 - y) / 2 + y

    canvas.create_rectangle(x, y,
                            x1, y1,
                            fill=element.bg,
                            width=element.bd)

    if (element.imageAddress != None):
        ResizeImage = element.image.resize((int(element.width), int(element.height)))
        canvas.create_image(element.xImage, element.yImage, image=ImageTk.PhotoImage(ResizeImage))

    elif (element.text != ""):
        font112 = ""
        for ele in element.font:
            font112 += f"{ele} "
        font112.rstrip(" ")
        canvas.create_text(xt, yt, text=element.text, font=font112)

    # configuration base on special type (Button, Entry)

    if (str(element) in ["Button", "Entry"]):
        # draw the border of the button to make it looks like a button and Entry
        # Up part
        canvas.create_line(x, y, x, y1, width=element.bd + 2, fill=element.buttonColorUp)
        canvas.create_line(x, y, x1, y, width=element.bd + 2, fill=element.buttonColorUp)
        # DownPart
        canvas.create_line(x1, y1, x, y1, width=element.bd + 2, fill=element.buttonColorDown)
        canvas.create_line(x1, y1, x1, y, width=element.bd + 2, fill=element.buttonColorDown)
        # draw the button/Entry border
        canvas.create_rectangle(x, y,
                                x1, y1, outline="lightgray")

        # draw configuration on Entry
        if (str(element) == "Entry"):
            xJ = x
            yJ = y + 2
            y1J = y1 - 2
            VLX = 0
            # a vertical line
            if (element.ElementStore != ""):
                full_width, h = element.Inputfont.getsize(element.ElementStore)
                VLX, height = element.Inputfont.getsize(element.ElementStore[:element.strTrack])
                full_width += len(element.ElementStore) * 1.6
                VLX += len(element.ElementStore[:element.strTrack]) * 1.6
                # only work for digits, but enough
                # can't find better way to get the size of characters
                canvas.create_text(xJ, yt, text=element.ElementStore, font=f"Time {element.InputFontSize}",
                                   anchor="w")
            if (element.clickFlag):
                canvas.create_line(xJ + VLX + 1, yJ, xJ + VLX + 1, y1J, fill=app.clickObject.JVL_color, width=1)


def mousePressed(app, event):
    # consider the animation of click
    keyX = event.x
    keyY = event.y
    for tkObject in app.tkObjectList.getList():
        if (tkObject.showIndicator):
            for element in tkObject.OwnElement:
                if (element.showIndicator):
                    if (str(element) == "Button"):
                        # Button don't need click-flag for constant happening event
                        x, x1, y, y1 = element.coordinate
                        if (checkMouse((x, x1, y, y1), (keyX, keyY))):
                            app.clickObject = element
                            element.buttonColorUp = "gray"
                            element.buttonColorDown = "white"
                            app.tempSave = element.bg
                            element.bg = app.tkObjectList.MasterOfAll.bg
                        # Entry need click-flag for constant happening event
                    elif (str(element) == "Entry"):
                        if (checkMouse((element.coordinate), (keyX, keyY))):
                            app.clickObject = element
                            element.clickFlag = True
                        else:
                            element.clickFlag = False
                            if (app.clickObject == element):
                                app.clickObject = None


def mouseReleased(app, event):
    if (app.clickObject != None):
        if (str(app.clickObject) == "Button"):
            app.clickObject.bg = app.tempSave
            app.clickObject.buttonColorUp = "white"
            app.clickObject.buttonColorDown = "black"
            # tkinter characteristic: only when the cursor released at the button area, call command
            if (checkMouse(app.clickObject.coordinate, (event.x, event.y))):
                app.clickObject.executeCommand()
                app.clickObject = None


def mouseMoved(app, event):
    pass


def checkMouse(coordinate, mouse):
    x, x1, y, y1 = coordinate
    keyX, keyY = mouse
    if (min(x, x1) <= keyX <= max(x, x1) and min(y, y1) <= keyY <= max(y, y1)):
        return True
    return False


def keyPressed(app, event):
    if (app.clickObject != None and str(app.clickObject) == "Entry"):
        if (event.key not in ["Up", "Right", "Down", "Left"]):
            if (event.key not in ["Tab", "Backspace", "Delete", "Escape"]):
                # normal input
                app.clickObject.executeCommand()
                if (event.key == "Space"):
                    event.key = " "
                app.clickObject.ElementStore = app.clickObject.ElementStore[0:app.clickObject.strTrack] \
                                               + event.key \
                                               + app.clickObject.ElementStore[app.clickObject.strTrack:]
                app.clickObject.strTrack += 1

            if (event.key == "Tab"):
                # change to another Entry&
                masterObject = app.clickObject.attr_obj.object
                index = masterObject.OwnElement.index(app.clickObject)
                for element in masterObject.OwnElement[index + 1:]:
                    if (str(element) == "Entry" and element.showIndicator):
                        # swicth
                        app.clickObject.clickFlag = False
                        app.clickObject = element
                        app.clickObject.clickFlag = True
                        break
            elif (event.key in ["Backspace", "Delete"]):
                # delete
                if (app.clickObject.ElementStore != "" and app.clickObject.strTrack != 0):
                    tempStr = app.clickObject.ElementStore
                    tempI = app.clickObject.strTrack
                    tempStr = tempStr[0:tempI - 1] + tempStr[tempI:]
                    app.clickObject.ElementStore = tempStr
                    app.clickObject.strTrack -= 1



            elif (event.key == "Escape"):
                app.clickObject.clickFlag = False
                app.clickObject = None


        elif (event.key == "Right"):
            if (len(app.clickObject.ElementStore) > app.clickObject.strTrack):
                app.clickObject.strTrack += 1
                print("right")
        elif (event.key == "Left"):
            if app.clickObject.strTrack > 0:
                app.clickObject.strTrack -= 1
                print("left")


def main(w, d, title=""):
    if (title == ""):
        runApp(width=w, height=d)
    else:
        runApp(width=w, height=d, title=title)


def showMessage(text):
    App._theRoot.app.showMessage(text)


def quit():
    App._theRoot.app.quit()
