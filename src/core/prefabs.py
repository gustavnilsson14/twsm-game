from core import *

class WasdPlayer(Player) :

    def __init__(self,id) :
        Player.__init__(self,id)
        self.movement = (0,0)

    def update( self ) :
        Player.update(self)
        self.movement = (0,0)
        if self.input.get(87) == 1 :
            self.movement = ( self.movement[0], self.movement[1]-1 )
        if self.input.get(83) == 1 :
            self.movement = ( self.movement[0], self.movement[1]+1 )
        if self.input.get(65) == 1 :
            self.movement = ( self.movement[0]-1, self.movement[1] )
        if self.input.get(68) == 1 :
            self.movement = ( self.movement[0]+1, self.movement[1] )

class Character(Sprite) :

    def __init__( self, pos, speed, animations ) :
        Sprite.__init__( self, animations )
        self._speed = speed
        self._movement = (0,0)
        self._pos = pos
        self.current_animations = SerializableList(self,[],'current_animations')

    def update( self ) :
        x = self.pos[0] + (self.movement[0] * self.speed)
        y = self.pos[1] + (self.movement[1] * self.speed)
        self.pos = ( x, y )

    def move( self, movement_vector ) :
        self.movement = movement_vector

    @property
    def speed( self ) :
        return self._speed

    @speed.setter
    def speed( self, val ) :
        if val != self._speed :
            self._speed = val
            self.property_changed('speed',val)

    @property
    def movement( self ) :
        return self._movement

    @movement.setter
    def movement( self, val ) :
        if val != self._movement :
            self._movement = val
            self.property_changed('movement',val)

    @property
    def pos( self ) :
        return self._pos

    @pos.setter
    def pos( self, val ) :
        if val != self._pos :
            self._pos = val
            self.property_changed('pos', val)
