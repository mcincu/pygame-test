import pygame
from engine.engine import *

class MainScene(Scene):

    def __init__(self,screen):
        Scene.__init__(self,screen)

        #Mapita  
        self.map=Tilemap()
        self.map.loadTMXMap("data/map2.tmx")
        self.add("map",self.map)
        #Enano
        self.enano=PlayableCharacter()
        self.add("pc",self.enano)
        #Selector
        self.selector=MapCursor(self.map)
        self.add("selector",self.selector)
        #Glyph texto
        self.glyph = TextBox("Hola, {link miguel; {red; miguel}}",40,60)
        self.glyph.addEntry("miguel","Miguel es un ciruja del pueblo. Es bueno, aunque le gusta demasiado la droga aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

        self.add("glyphtexto",self.glyph)

class MapCursor(Sprite):

    def __init__(self,mapData, x=0,y=0):
        Sprite.__init__(self)
        self.process_input=True 
        self.images={}
        self.images['red']=SpriteUtils.loadImage("selector.png")
        self.images['green']=SpriteUtils.loadImage("selector_green.png")
        self.images['cross']=SpriteUtils.loadImage("selector_cross.png")
        self.enabled=True
        self.loadImage("selector_green.png")
        self.map_x=0
        self.map_y=0
        self.mapData=mapData

    def switchEnabled(self,solid):
        if solid=='true':
            self.enabled=False
            self.changeImage(self.images['red'])
        else:
            self.enabled=True
            self.changeImage(self.images['green'])

    def processInput(self,event, handled):
        if event.type == pygame.MOUSEMOTION:
            evx,evy= event.pos
            map_x=evx//config.SPRITE_WIDTH
            map_y=evy//config.SPRITE_HEIGHT
            if not (self.map_x==map_x and self.map_y==map_y):
                self.map_x=map_x
                self.map_y=map_y
                self.moveSprite(self.map_x*config.SPRITE_WIDTH,self.map_y*config.SPRITE_HEIGHT)
                self.switchEnabled(self.mapData.getTileProperty(self.map_x, self.map_y,'solid'))  
        if event.type == pygame.MOUSEBUTTONUP and self.enabled:
            move_event=self.fireEvent({"name":"Move To Cell","target":["pc"],"map_x": self.map_x, "map_y":self.map_y , "mapData":self.mapData})
            if not move_event['response']:
                self.changeImage(self.images['cross'])
        return True

class PlayableCharacter(Actor):
    def __init__(self,x=0,y=0):
        Actor.__init__(self)
        self.process_events=True
        self.loadImageFromSheet("pjs.png",0,2,config.SPRITE_WIDTH,config.SPRITE_HEIGHT)
        self.text2 = Text("Saca la mano de ahi carajo!")
        self.text2.moveSprite(self.x-int(self.text2.rect.width/2),self.y-16)
        self.add("name",self.text2,self.x-int(self.text2.rect.width/2),self.y-16)
        self.eventHandlers= {"Move To Cell" : self.moveToCell}

    def moveToCell(self,event):
        move_able=self.moveTo(event['map_x'], event['map_y'], event['mapData'])
        event['response']=move_able
        return event

