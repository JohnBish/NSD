import sys, json, os.path
from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import CardMaker
from pandac.PandaModules import NodePath
from pandac.PandaModules import TextureStage
from pandac.PandaModules import WindowProperties
from direct.showbase.DirectObject import DirectObject
from direct.interval.IntervalGlobal import *
from direct.task import Task
from pandac.PandaModules import WindowProperties

RESOLUTION = RESX, RESY = 1920, 1080


class NSDApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.keys = ReadKeys()

        self.wp = WindowProperties()
        self.wp.setFullscreen(1)
        self.wp.setSize(RESOLUTION)
        self.openMainWindow()
        self.win.requestProperties(self.wp)
        self.graphicsEngine.openWindows()
        self.setBackgroundColor(0, 0, 0)
        self.disableMouse()
        self.props = WindowProperties()
        self.props.setCursorHidden(True)
        self.win.requestProperties(self.props)
        self.title()

    def title(self):
        #Removes title and loads current room
        def destroyTitle(task):
            card.removeNode()
            startGame()

        def startGame():
            if os.path.isfile('saves/location.json'):
                self.directToRoom()
            else:
                self.homeFirst()

        #Loads title animation
        titleText = self.loader.loadTexture('resources/titleText.avi')
        titleText.setLoopCount(1)
        titleText.play()

        #Displays title
        cm = CardMaker('titleText')
        cm.setFrameFullscreenQuad()
        cm.setUvRange(titleText)
        # noinspection PyArgumentList
        card = NodePath(cm.generate())
        card.reparentTo(self.render2d)
        card.setTexture(titleText)
        self.taskMgr.doMethodLater(5.6, destroyTitle, 'endTitle')

    def saveRoom(self, cr):
        with open('saves/location.json', 'w+') as outfile:
            saveInfo = {'currentRoom' : cr }
            json.dump(saveInfo, outfile, sort_keys = True, indent = 4,
               ensure_ascii = False)

    def directToRoom(self):
        with open('saves/location.json') as df:
            data = json.load(df)

    def homeFirst(self):
        self.homeRoom()

    def homeRoom(self):
        self.saveRoom("1")
        #scene = self.loader.loadModel("resources/homeRoom.egg")
        #scene.reparentTo(self.render)


class ReadKeys(DirectObject):
    def __init__(self):
        self.accept('escape', sys.exit)

app = NSDApp()
app.run()
