# cmu_112_graphics.py
# version 0.9.0

# Pre-release for CMU 15-112-s21

# Require Python 3.6 or later
import sys
if ((sys.version_info[0] != 3) or (sys.version_info[1] < 6)):
    raise Exception('cmu_112_graphics.py requires Python version 3.6 or later.')

# Track version and file update timestamp
import datetime
MAJOR_VERSION = 0
MINOR_VERSION = 9.0 # version 0.9.0
LAST_UPDATED  = datetime.date(year=2021, month=4, day=12)

# Pending changes:
#   * Fix Windows-only bug: Position popup dialog box over app window (already works fine on Macs)
#   * Add documentation
#   * integrate sounds (probably from pyGame)
#   * Improved methodIsOverridden to TopLevelApp and ModalApp
#   * Save to animated gif and/or mp4 (with audio capture?)

# Deferred changes:
#   * replace/augment tkinter canvas with PIL/Pillow imageDraw (perhaps with our own fn names)

# Changes in v0.9.0
#  * added simpler top-level modes implementation that does not include mode objects
#  * added ImageDraw and ImageFont to PIL imports

# Changes in v0.8.8
#   * added __repr__ methods so:
#     * print(event) works and prints event.key or event.x + event.y
#     * print(app) works and prints just the user defined app fields

# Changes in v0.8.7
#   * removed modes (for now)

# Changes in v0.8.6
#   * s21

# Changes in v0.8.5
#   * Support loadImage from Modes

# Changes in v0.8.3 + v0.8.4
#   * Use default empty Mode if none is provided
#   * Add KeyRelease event binding
#   * Drop user32.SetProcessDPIAware (caused window to be really tiny on some Windows machines)

# Changes in v0.8.1 + v0.8.2
#   * print version number and last-updated date on load
#   * restrict modifiers to just control key (was confusing with NumLock, etc)
#   * replace hasModifiers with 'control-' prefix, as in 'control-A'
#   * replace app._paused with app.paused, etc (use app._ for private variables)
#   * use improved ImageGrabber import for linux

# Changes in v0.8.0
#   * suppress more modifier keys (Super_L, Super_R, ...)
#   * raise exception on event.keysym or event.char + works with key = 'Enter'
#   * remove tryToInstall

# Changes in v0.7.4
#   * renamed drawAll back to redrawAll :-)

# Changes in v0.7.3
#   * Ignore mousepress-drag-release and defer configure events for drags in titlebar
#   * Extend deferredRedrawAll to 100ms with replace=True and do not draw while deferred
#     (together these hopefully fix Windows-only bug: file dialog makes window not moveable)
#   * changed sizeChanged to not take event (use app.width and app.height)

# Changes in v0.7.2
#   * Singleton App._theRoot instance (hopefully fixes all those pesky Tkinter errors-on-exit)
#   * Use user32.SetProcessDPIAware to get resolution of screen grabs right on Windows-only (fine on Macs)
#   * Replaces showGraphics() with runApp(...), which is a veneer for App(...) [more intuitive for pre-OOP part of course]
#   * Fixes/updates images:
#       * disallows loading images in redrawAll (raises exception)
#       * eliminates cache from loadImage
#       * eliminates app.getTkinterImage, so user now directly calls ImageTk.PhotoImage(image))
#       * also create_image allows magic pilImage=image instead of image=ImageTk.PhotoImage(app.image)

# Changes in v0.7.1
#   * Added keyboard shortcut:
#       * cmd/ctrl/alt-x: hard exit (uses os._exit() to exit shell without tkinter error messages)
#   * Fixed bug: shortcut keys stopped working after an MVC violation (or other exception)
#   * In app.saveSnapshot(), add .png to path if missing
#   * Added: Print scripts to copy-paste into shell to install missing modules (more automated approaches proved too brittle)

# Changes in v0.7
#   * Added some image handling (requires PIL (retained) and pyscreenshot (later removed):
#       * app.loadImage()       # loads PIL/Pillow image from file, with file dialog, or from URL (http or https)
#       * app.scaleImage()      # scales a PIL/Pillow image
#       * app.getTkinterImage() # converts PIL/Pillow image to Tkinter PhotoImage for use in create_image(...)
#       * app.getSnapshot()     # get a snapshot of the canvas as a PIL/Pillow image
#       * app.saveSnapshot()    # get and save a snapshot
#   * Added app._paused, app.togglePaused(), and paused highlighting (red outline around canvas when paused)
#   * Added keyboard shortcuts:
#       * cmd/ctrl/alt-s: save a snapshot
#       * cmd/ctrl/alt-p: pause/unpause
#       * cmd/ctrl/alt-q: quit

# Changes in v0.6:
#   * Added fnPrefix option to TopLevelApp (so multiple TopLevelApp's can be in one file)
#   * Added showGraphics(drawFn) (for graphics-only drawings before we introduce animations)

# Changes in v0.5:
#   * Added:
#       * app.winx and app.winy (and add winx,winy parameters to app.__init__, and sets these on configure events)
#       * app.setSize(width, height)
#       * app.setPosition(x, y)
#       * app.quit()
#       * app.showMessage(message)
#       * app.getUserInput(prompt)
#       * App.lastUpdated (instance of datetime.date)
#   * Show popup dialog box on all exceptions (not just for MVC violations)
#   * Draw (in canvas) "Exception!  App Stopped! (See console for details)" for any exception
#   * Replace callUserMethod() with more-general @_safeMethod decorator (also handles exceptions outside user methods)
#   * Only include lines from user's code (and not our framework nor tkinter) in stack traces
#   * Require Python version (3.6 or greater)

# Changes in v0.4:
#   * Added __setattr__ to enforce Type 1A MVC Violations (setting app.x in redrawAll) with better stack trace
#   * Added app._deferredRedrawAll() (avoids resizing drawing/crashing bug on some platforms)
#   * Added deferredMethodCall() and app._afterIdMap to generalize afterId handling
#   * Use (_ is None) instead of (_ == None)

# Changes in v0.3:
#   * Fixed "event not defined" bug in sizeChanged handlers.
#   * draw "MVC Violation" on Type 2 violation (calling draw methods outside redrawAll)

# Changes in v0.2:
#   * Handles another MVC violation (now detects drawing on canvas outside of redrawAll)
#   * App stops running when an exception occurs (in user code) (stops cascading errors)

# Changes in v0.1:
#   * OOPy + supports inheritance + supports multiple apps in one file + etc
#        * uses import instead of copy-paste-edit starter code + no "do not edit code below here!"
#        * no longer uses Struct (which was non-Pythonic and a confusing way to sort-of use OOP)
#   * Includes an early version of MVC violation handling (detects model changes in redrawAll)
#   * added events:
#       * appStarted (no init-vs-__init__ confusion)
#       * appStopped (for cleanup)
#       * keyReleased (well, sort of works) + mouseReleased
#       * mouseMoved + mouseDragged
#       * sizeChanged (when resizing window)
#   * improved key names (just use event.key instead of event.char and/or event.keysym + use names for 'Enter', 'Escape', ...)
#   * improved function names (renamed redrawAll to drawAll)
#   * improved (if not perfect) exiting without that irksome Tkinter error/bug
#   * app has a title in the titlebar (also shows window's dimensions)
#   * supports Modes and ModalApp (see ModalApp and Mode, and also see TestModalApp example)
#   * supports TopLevelApp (using top-level functions instead of subclasses and methods)
#   * supports version checking with App.majorVersion, App.minorVersion, and App.version
#   * logs drawing calls to support autograding views (still must write that autograder, but this is a very helpful first step)

from tkinter import *
from tkinter import messagebox, simpledialog, filedialog
import inspect, copy, traceback
import sys, os
from io import BytesIO

def failedImport(importName, installName=None):
    installName = installName or importName
    print('**********************************************************')
    print(f'** Cannot import {importName} -- it seems you need to install {installName}')
    print(f'** This may result in limited functionality or even a runtime error.')
    print('**********************************************************')
    print()

try: from PIL import Image, ImageTk, ImageDraw, ImageFont
except ModuleNotFoundError: failedImport('PIL', 'pillow')

if sys.platform.startswith('linux'):
    try: import pyscreenshot as ImageGrabber
    except ModuleNotFoundError: failedImport('pyscreenshot')
else:
    try: from PIL import ImageGrab as ImageGrabber
    except ModuleNotFoundError: pass # Our PIL warning is already printed above

try: import requests
except ModuleNotFoundError: failedImport('requests')

def getHash(obj):
    # This is used to detect MVC violations in redrawAll
    # @TODO: Make this more robust and efficient
    try:
        return getHash(obj.__dict__)
    except:
        if (isinstance(obj, list)): return getHash(tuple([getHash(v) for v in obj]))
        elif (isinstance(obj, set)): return getHash(sorted(obj))
        elif (isinstance(obj, dict)): return getHash(tuple([obj[key] for key in sorted(obj)]))
        else:
            try: return hash(obj)
            except: return getHash(repr(obj))

class WrappedCanvas(Canvas):
    # Enforces MVC: no drawing outside calls to redrawAll
    # Logs draw calls (for autograder) in canvas.loggedDrawingCalls
    def __init__(wrappedCanvas, app):
        wrappedCanvas.loggedDrawingCalls = [ ]
        wrappedCanvas.logDrawingCalls = True
        wrappedCanvas.inRedrawAll = False
        wrappedCanvas.app = app
        super().__init__(app._root, width=app.width, height=app.height)

    def log(self, methodName, args, kwargs):
        if (not self.inRedrawAll):
            self.app._mvcViolation('you may not use the canvas (the view) outside of redrawAll')
        if (self.logDrawingCalls):
            self.loggedDrawingCalls.append((methodName, args, kwargs))

    def create_arc(self, *args, **kwargs): self.log('create_arc', args, kwargs); return super().create_arc(*args, **kwargs)
    def create_bitmap(self, *args, **kwargs): self.log('create_bitmap', args, kwargs); return super().create_bitmap(*args, **kwargs)
    def create_line(self, *args, **kwargs): self.log('create_line', args, kwargs); return super().create_line(*args, **kwargs)
    def create_oval(self, *args, **kwargs): self.log('create_oval', args, kwargs); return super().create_oval(*args, **kwargs)
    def create_polygon(self, *args, **kwargs): self.log('create_polygon', args, kwargs); return super().create_polygon(*args, **kwargs)
    def create_rectangle(self, *args, **kwargs): self.log('create_rectangle', args, kwargs); return super().create_rectangle(*args, **kwargs)
    def create_text(self, *args, **kwargs): self.log('create_text', args, kwargs); return super().create_text(*args, **kwargs)
    def create_window(self, *args, **kwargs): self.log('create_window', args, kwargs); return super().create_window(*args, **kwargs)

    def create_image(self, *args, **kwargs):
        self.log('create_image', args, kwargs);
        usesImage = 'image' in kwargs
        usesPilImage = 'pilImage' in kwargs
        if ((not usesImage) and (not usesPilImage)):
            raise Exception('create_image requires an image to draw')
        elif (usesImage and usesPilImage):
            raise Exception('create_image cannot use both an image and a pilImage')
        elif (usesPilImage):
            pilImage = kwargs['pilImage']
            del kwargs['pilImage']
            if (not isinstance(pilImage, Image.Image)):
                raise Exception('create_image: pilImage value is not an instance of a PIL/Pillow image')
            image = ImageTk.PhotoImage(pilImage)
        else:
            image = kwargs['image']
            if (isinstance(image, Image.Image)):
                raise Exception('create_image: image must not be an instance of a PIL/Pillow image\n' +
                    'You perhaps meant to convert from PIL to Tkinter, like so:\n' +
                    '     canvas.create_image(x, y, image=ImageTk.PhotoImage(image))')
        kwargs['image'] = image
        return super().create_image(*args, **kwargs)

class App(object):
    majorVersion = MAJOR_VERSION
    minorVersion = MINOR_VERSION
    version = f'{majorVersion}.{minorVersion}'
    lastUpdated = LAST_UPDATED
    _theRoot = None # singleton Tkinter root object

    ####################################
    # User Methods:
    ####################################
    def redrawAll(app, canvas): pass      # draw (view) the model in the canvas
    def appStarted(app): pass           # initialize the model (app.xyz)
    def appStopped(app): pass           # cleanup after app is done running
    def keyPressed(app, event): pass    # use event.key
    def keyReleased(app, event): pass   # use event.key
    def mousePressed(app, event): pass  # use event.x and event.y
    def mouseReleased(app, event): pass # use event.x and event.y
    def mouseMoved(app, event): pass    # use event.x and event.y
    def mouseDragged(app, event): pass  # use event.x and event.y
    def timerFired(app): pass           # respond to timer events
    def sizeChanged(app): pass          # respond to window size changes

    ####################################
    # Implementation:
    ####################################

    def __init__(app, width=300, height=300, x=0, y=0, title=None, autorun=True, mvcCheck=True, logDrawingCalls=True):
        app.winx, app.winy, app.width, app.height = x, y, width, height
        app.timerDelay = 100     # milliseconds
        app.mouseMovedDelay = 50 # ditto
        app._title = title
        app._mvcCheck = mvcCheck
        app._logDrawingCalls = logDrawingCalls
        app._running = app._paused = False
        app._mousePressedOutsideWindow = False
        if autorun: app.run()

    def __repr__(app):
        keys = set(app.__dict__.keys())
        keyValues = [ ]
        for key in sorted(keys - app._ignoredFields):
            keyValues.append(f'{key}={app.__dict__[key]}')
        return f'App({", ".join(keyValues)})'

    def setSize(app, width, height):
        app._root.geometry(f'{width}x{height}')

    def setPosition(app, x, y):
        app._root.geometry(f'+{x}+{y}')

    def showMessage(app, message):
        messagebox.showinfo('showMessage', message, parent=app._root)

    def getUserInput(app, prompt):
        return simpledialog.askstring('getUserInput', prompt)

    def loadImage(app, path=None):
        if (app._canvas.inRedrawAll):
            raise Exception('Cannot call loadImage in redrawAll')
        if (path is None):
            path = filedialog.askopenfilename(initialdir=os.getcwd(), title='Select file: ',filetypes = (('Image files','*.png *.gif *.jpg'),('all files','*.*')))
            if (not path): return None
        if (path.startswith('http')):
            response = requests.request('GET', path) # path is a URL!
            image = Image.open(BytesIO(response.content))
        else:
            image = Image.open(path)
        return image

    def scaleImage(app, image, scale, antialias=False):
        # antialiasing is higher-quality but slower
        resample = Image.ANTIALIAS if antialias else Image.NEAREST
        return image.resize((round(image.width*scale), round(image.height*scale)), resample=resample)

    def getSnapshot(app):
        app._showRootWindow()
        x0 = app._root.winfo_rootx() + app._canvas.winfo_x()
        y0 = app._root.winfo_rooty() + app._canvas.winfo_y()
        result = ImageGrabber.grab((x0,y0,x0+app.width,y0+app.height))
        return result

    def saveSnapshot(app):
        path = filedialog.asksaveasfilename(initialdir=os.getcwd(), title='Select file: ',filetypes = (('png files','*.png'),('all files','*.*')))
        if (path):
            # defer call to let filedialog close (and not grab those pixels)
            if (not path.endswith('.png')): path += '.png'
            app._deferredMethodCall(afterId='saveSnapshot', afterDelay=0, afterFn=lambda:app.getSnapshot().save(path))

    def _togglePaused(app):
        app._paused = not app._paused

    def quit(app):
        app._running = False
        app._root.quit() # break out of root.mainloop() without closing window!

    def __setattr__(app, attr, val):
        d = app.__dict__
        d[attr] = val
        canvas = d.get('_canvas', None)
        if (d.get('running', False) and
            d.get('mvcCheck', False) and
            (canvas is not None) and
            canvas.inRedrawAll):
            app._mvcViolation(f'you may not change app.{attr} in the model while in redrawAll (the view)')

    def _printUserTraceback(app, exception, tb):
        stack = traceback.extract_tb(tb)
        lines = traceback.format_list(stack)
        inRedrawAllWrapper = False
        printLines = [ ]
        for line in lines:
            if (('"cmu_112_graphics.py"' not in line) and
                ('/cmu_112_graphics.py' not in line) and
                ('\\cmu_112_graphics.py' not in line) and
                ('/tkinter/' not in line) and
                ('\\tkinter\\' not in line)):
                printLines.append(line)
            if ('redrawAllWrapper' in line):
                inRedrawAllWrapper = True
        if (len(printLines) == 0):
            # No user code in trace, so we have to use all the code (bummer),
            # but not if we are in a redrawAllWrapper...
            if inRedrawAllWrapper:
                printLines = ['    No traceback available. Error occurred in redrawAll.\n']
            else:
                printLines = lines
        print('Traceback (most recent call last):')
        for line in printLines: print(line, end='')
        print(f'Exception: {exception}')

    def _safeMethod(appMethod):
        def m(*args, **kwargs):
            app = args[0]
            try:
                return appMethod(*args, **kwargs)
            except Exception as e:
                app._running = False
                app._printUserTraceback(e, sys.exc_info()[2])
                if ('_canvas' in app.__dict__):
                    app._canvas.inRedrawAll = True # not really, but stops recursive MVC Violations!
                    app._canvas.create_rectangle(0, 0, app.width, app.height, fill=None, width=10, outline='red')
                    app._canvas.create_rectangle(10, app.height-50, app.width-10, app.height-10,
                                                 fill='white', outline='red', width=4)
                    app._canvas.create_text(app.width/2, app.height-40, text=f'Exception! App Stopped!', fill='red', font='Arial 12 bold')
                    app._canvas.create_text(app.width/2, app.height-20, text=f'See console for details', fill='red', font='Arial 12 bold')
                    app._canvas.update()
                app.showMessage(f'Exception: {e}\nClick ok then see console for details.')
        return m

    def _methodIsOverridden(app, methodName):
        return (getattr(type(app), methodName) is not getattr(App, methodName))

    def _mvcViolation(app, errMsg):
        app._running = False
        raise Exception('MVC Violation: ' + errMsg)

    @_safeMethod
    def _redrawAllWrapper(app):
        if (not app._running): return
        if ('deferredRedrawAll' in app._afterIdMap): return # wait for pending call
        app._canvas.inRedrawAll = True
        app._canvas.delete(ALL)
        width,outline = (10,'red') if app._paused else (0,'white')
        app._canvas.create_rectangle(0, 0, app.width, app.height, fill='white', width=width, outline=outline)
        app._canvas.loggedDrawingCalls = [ ]
        app._canvas.logDrawingCalls = app._logDrawingCalls
        hash1 = getHash(app) if app._mvcCheck else None
        try:
            app.redrawAll(app._canvas)
            hash2 = getHash(app) if app._mvcCheck else None
            if (hash1 != hash2):
                app._mvcViolation('you may not change the app state (the model) in redrawAll (the view)')
        finally:
            app._canvas.inRedrawAll = False
        app._canvas.update()

    def _deferredMethodCall(app, afterId, afterDelay, afterFn, replace=False):
        def afterFnWrapper():
            app._afterIdMap.pop(afterId, None)
            afterFn()
        id = app._afterIdMap.get(afterId, None)
        if ((id is None) or replace):
            if id: app._root.after_cancel(id)
            app._afterIdMap[afterId] = app._root.after(afterDelay, afterFnWrapper)

    def _deferredRedrawAll(app):
        app._deferredMethodCall(afterId='deferredRedrawAll', afterDelay=100, afterFn=app._redrawAllWrapper, replace=True)

    @_safeMethod
    def _appStartedWrapper(app):
        app.appStarted()
        app._redrawAllWrapper()

    _keyNameMap = { '\t':'Tab', '\n':'Enter', '\r':'Enter', '\b':'Backspace',
                   chr(127):'Delete', chr(27):'Escape', ' ':'Space' }

    @staticmethod
    def _useEventKey(attr):
        raise Exception(f'Use event.key instead of event.{attr}')

    @staticmethod
    def _getEventKeyInfo(event, keysym, char):
        key = c = char
        hasControlKey = (event.state & 0x4 != 0)
        if ((c in [None, '']) or (len(c) > 1) or (ord(c) > 255)):
            key = keysym
            if (key.endswith('_L') or
                key.endswith('_R') or
                key.endswith('_Lock')):
                key = 'Modifier_Key'
        elif (c in App._keyNameMap):
            key = App._keyNameMap[c]
        elif ((len(c) == 1) and (1 <= ord(c) <= 26)):
            key = chr(ord('a')-1 + ord(c))
            hasControlKey = True
        if hasControlKey and (len(key) == 1):
            # don't add control- prefix to Enter, Tab, Escape, ...
            key = 'control-' + key
        return key

    class EventWrapper(Event):
        def __init__(self, event):
            for key in event.__dict__:
                if (not key.startswith('__')):
                    self.__dict__[key] = event.__dict__[key]

    class MouseEventWrapper(EventWrapper):
        def __repr__(self):
            return f'Event(x={self.x}, y={self.y})'

    class KeyEventWrapper(EventWrapper):
        def __init__(self, event):
            keysym, char = event.keysym, event.char
            del event.keysym
            del event.char
            super().__init__(event)
            self.key = App._getEventKeyInfo(event, keysym, char)
        def __repr__(self):
            return f'Event(key={repr(self.key)})'
        keysym = property(lambda *args: App._useEventKey('keysym'),
                          lambda *args: App._useEventKey('keysym'))
        char =   property(lambda *args: App._useEventKey('char'),
                          lambda *args: App._useEventKey('char'))

    @_safeMethod
    def _keyPressedWrapper(app, event):
        event = App.KeyEventWrapper(event)
        if (event.key == 'control-s'):
            app.saveSnapshot()
        elif (event.key == 'control-p'):
            app._togglePaused()
            app._redrawAllWrapper()
        elif (event.key == 'control-q'):
            app.quit()
        elif (event.key == 'control-x'):
            os._exit(0) # hard exit avoids tkinter error messages
        elif (app._running and
              (not app._paused) and
              app._methodIsOverridden('keyPressed') and
              (not event.key == 'Modifier_Key')):
            app.keyPressed(event)
            app._redrawAllWrapper()

    @_safeMethod
    def _keyReleasedWrapper(app, event):
        if (not app._running) or app._paused or (not app._methodIsOverridden('keyReleased')): return
        event = App.KeyEventWrapper(event)
        if (not event.key == 'Modifier_Key'):
            app.keyReleased(event)
            app._redrawAllWrapper()

    @_safeMethod
    def _mousePressedWrapper(app, event):
        if (not app._running) or app._paused: return
        if ((event.x < 0) or (event.x > app.width) or
            (event.y < 0) or (event.y > app.height)):
            app._mousePressedOutsideWindow = True
        else:
            app._mousePressedOutsideWindow = False
            app._mouseIsPressed = True
            app._lastMousePosn = (event.x, event.y)
            if (app._methodIsOverridden('mousePressed')):
                event = App.MouseEventWrapper(event)
                app.mousePressed(event)
                app._redrawAllWrapper()

    @_safeMethod
    def _mouseReleasedWrapper(app, event):
        if (not app._running) or app._paused: return
        app._mouseIsPressed = False
        if app._mousePressedOutsideWindow:
            app._mousePressedOutsideWindow = False
            app._sizeChangedWrapper()
        else:
            app._lastMousePosn = (event.x, event.y)
            if (app._methodIsOverridden('mouseReleased')):
                event = App.MouseEventWrapper(event)
                app.mouseReleased(event)
                app._redrawAllWrapper()

    @_safeMethod
    def _timerFiredWrapper(app):
        if (not app._running) or (not app._methodIsOverridden('timerFired')): return
        if (not app._paused):
            app.timerFired()
            app._redrawAllWrapper()
        app._deferredMethodCall(afterId='_timerFiredWrapper', afterDelay=app.timerDelay, afterFn=app._timerFiredWrapper)

    @_safeMethod
    def _sizeChangedWrapper(app, event=None):
        if (not app._running): return
        if (event and ((event.width < 2) or (event.height < 2))): return
        if (app._mousePressedOutsideWindow): return
        app.width,app.height,app.winx,app.winy = [int(v) for v in app._root.winfo_geometry().replace('x','+').split('+')]
        if (app._lastWindowDims is None):
            app._lastWindowDims = (app.width, app.height, app.winx, app.winy)
        else:
            newDims =(app.width, app.height, app.winx, app.winy)
            if (app._lastWindowDims != newDims):
                app._lastWindowDims = newDims
                app.updateTitle()
                app.sizeChanged()
                app._deferredRedrawAll() # avoid resize crashing on some platforms

    @_safeMethod
    def _mouseMotionWrapper(app):
        if (not app._running): return
        mouseMovedExists = app._methodIsOverridden('mouseMoved')
        mouseDraggedExists = app._methodIsOverridden('mouseDragged')
        if ((not app._paused) and
            (not app._mousePressedOutsideWindow) and
            (((not app._mouseIsPressed) and mouseMovedExists) or
             (app._mouseIsPressed and mouseDraggedExists))):
            class MouseMotionEvent(object): pass
            event = MouseMotionEvent()
            root = app._root
            event.x = root.winfo_pointerx() - root.winfo_rootx()
            event.y = root.winfo_pointery() - root.winfo_rooty()
            event = App.MouseEventWrapper(event)
            if ((app._lastMousePosn !=  (event.x, event.y)) and
                (event.x >= 0) and (event.x <= app.width) and
                (event.y >= 0) and (event.y <= app.height)):
                if (app._mouseIsPressed): app.mouseDragged(event)
                else: app.mouseMoved(event)
                app._lastMousePosn = (event.x, event.y)
                app._redrawAllWrapper()
        if (mouseMovedExists or mouseDraggedExists):
            app._deferredMethodCall(afterId='mouseMotionWrapper', afterDelay=app.mouseMovedDelay, afterFn=app._mouseMotionWrapper)

    def updateTitle(app):
        app._title = app._title or type(app).__name__
        app._root.title(f'{app._title} ({app.width} x {app.height})')

    def getQuitMessage(app):
        appLabel = type(app).__name__
        if (app._title != appLabel):
            if (app._title.startswith(appLabel)):
                appLabel = app._title
            else:
                appLabel += f" '{app._title}'"
        return f"*** Closing {appLabel}.  Bye! ***\n"

    def _showRootWindow(app):
        root = app._root
        root.update(); root.deiconify(); root.lift(); root.focus()

    def _hideRootWindow(app):
        root = app._root
        root.withdraw()

    @_safeMethod
    def run(app):
        app._mouseIsPressed = False
        app._lastMousePosn = (-1, -1)
        app._lastWindowDims= None # set in sizeChangedWrapper
        app._afterIdMap = dict()
        # create the singleton root window
        if (App._theRoot is None):
            App._theRoot = Tk()
            App._theRoot.createcommand('exit', lambda: '') # when user enters cmd-q, ignore here (handled in keyPressed)
            App._theRoot.protocol('WM_DELETE_WINDOW', lambda: App._theRoot.app.quit()) # when user presses 'x' in title bar
            App._theRoot.bind("<Button-1>", lambda event: App._theRoot.app._mousePressedWrapper(event))
            App._theRoot.bind("<B1-ButtonRelease>", lambda event: App._theRoot.app._mouseReleasedWrapper(event))
            App._theRoot.bind("<KeyPress>", lambda event: App._theRoot.app._keyPressedWrapper(event))
            App._theRoot.bind("<KeyRelease>", lambda event: App._theRoot.app._keyReleasedWrapper(event))
            App._theRoot.bind("<Configure>", lambda event: App._theRoot.app._sizeChangedWrapper(event))
        else:
            App._theRoot.canvas.destroy()
        app._root = root = App._theRoot # singleton root!
        root.app = app
        root.geometry(f'{app.width}x{app.height}+{app.winx}+{app.winy}')
        app.updateTitle()
        # create the canvas
        root.canvas = app._canvas = WrappedCanvas(app)
        app._canvas.pack(fill=BOTH, expand=YES)
        # initialize, start the timer, and launch the app
        app._running = True
        app._paused = False
        app._ignoredFields = set(app.__dict__.keys()) | {'_ignoredFields'}
        app._appStartedWrapper()
        app._timerFiredWrapper()
        app._mouseMotionWrapper()
        app._showRootWindow()
        root.mainloop()
        app._hideRootWindow()
        app._running = False
        for afterId in app._afterIdMap: app._root.after_cancel(app._afterIdMap[afterId])
        app._afterIdMap.clear() # for safety
        app.appStopped()
        print(app.getQuitMessage())

####################################
# TopLevelApp:
# (with top-level functions not subclassses and methods)
####################################

class TopLevelApp(App):
    _apps = dict() # maps fnPrefix to app

    def __init__(app, fnPrefix='', **kwargs):
        if (fnPrefix in TopLevelApp._apps):
            print(f'Quitting previous version of {fnPrefix} TopLevelApp.')
            TopLevelApp._apps[fnPrefix].quit()
        if ((fnPrefix != '') and ('title' not in kwargs)):
            kwargs['title'] = f"TopLevelApp '{fnPrefix}'"
        TopLevelApp._apps[fnPrefix] = app
        app._fnPrefix = fnPrefix
        app._callersGlobals = inspect.stack()[1][0].f_globals
        app.mode = None
        super().__init__(**kwargs)

    def _callFn(app, fn, *args):
        if (app.mode != None) and (app.mode != ''):
            fn = app.mode + '_' + fn
        fn = app._fnPrefix + fn
        if (fn in app._callersGlobals): app._callersGlobals[fn](*args)

    def redrawAll(app, canvas): app._callFn('redrawAll', app, canvas)
    def appStarted(app): app._callFn('appStarted', app)
    def appStopped(app): app._callFn('appStopped', app)
    def keyPressed(app, event): app._callFn('keyPressed', app, event)
    def keyReleased(app, event): app._callFn('keyReleased', app, event)
    def mousePressed(app, event): app._callFn('mousePressed', app, event)
    def mouseReleased(app, event): app._callFn('mouseReleased', app, event)
    def mouseMoved(app, event): app._callFn('mouseMoved', app, event)
    def mouseDragged(app, event): app._callFn('mouseDragged', app, event)
    def timerFired(app): app._callFn('timerFired', app)
    def sizeChanged(app): app._callFn('sizeChanged', app)

####################################
# ModalApp + Mode:
####################################

'''
# For now, only include modes in top-level apps (see above).
class Mode(object):
    def __repr__(self): return f'<{self.__class__.__name__} object>'

class ModalApp(App):
    def __init__(app, *args, **kwargs):
        app._mode = None
        super().__init__(*args, **kwargs)

    def setMode(app, mode):
        if (not isinstance(mode, Mode)):
            raise Exception('mode must be an instance of Mode')
        app._mode = mode

    def _callFn(app, fn, *args):
        if (app._mode == None):
            raise Exception('ModalApp must have a mode (use app.setMode())')
        mode = app._mode
        # method = getattr(mode, fn, None)
        method = mode.__class__.__dict__.get(fn) # get method as fn
        if (method != None):
            method(*args)

    def redrawAll(app, canvas): app._callFn('redrawAll', app, canvas)
    #def appStarted(app): app._callFn('appStarted', app)
    #def appStopped(app): app._callFn('appStopped', app)
    def keyPressed(app, event): app._callFn('keyPressed', app, event)
    def keyReleased(app, event): app._callFn('keyReleased', app, event)
    def mousePressed(app, event): app._callFn('mousePressed', app, event)
    def mouseReleased(app, event): app._callFn('mouseReleased', app, event)
    def mouseMoved(app, event): app._callFn('mouseMoved', app, event)
    def mouseDragged(app, event): app._callFn('mouseDragged', app, event)
    def timerFired(app): app._callFn('timerFired', app)
    def sizeChanged(app): app._callFn('sizeChanged', app)
'''

####################################
# runApp()
####################################

'''
def showGraphics(drawFn, **kwargs):
    class GraphicsApp(App):
        def __init__(app, **kwargs):
            if ('title' not in kwargs):
                kwargs['title'] = drawFn.__name__
            super().__init__(**kwargs)
        def redrawAll(app, canvas):
            drawFn(app, canvas)
    app = GraphicsApp(**kwargs)
'''
runApp = TopLevelApp

print(f'Loaded cmu_112_graphics version {App.version} (last updated {App.lastUpdated})')

if (__name__ == '__main__'):
    try: import cmu_112_graphics_tests
    except: pass
