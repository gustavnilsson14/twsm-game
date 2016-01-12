from core import *
from prefabs import *

class Warrior(WasdPlayer) :

    def __init__( self, id, x, y ) :
        Player.__init__( self, id )
        self.character = Character( (0,0), 5, ['idle','move','attack'] )

    def update( self ) :
        WasdPlayer.update(self)
        self.character.move(self.movement)
        self.character.update()

class Arena(Game) :

    def __init__( self ) :
        Game.__init__(self)
        self.players = []

    def update( self, messages ) :
        Game.update(self, messages)

    def add_client( self, client ) :
        player = Warrior(client, 15, 15)
        Game.add_client( self, player )
        for other_player in self.clients :
            other_player.character.add_watcher('pos', player)
            other_player.character.add_watcher('list_remove', player)
            other_player.character.add_watcher('list_append', player)
            player.character.add_watcher('pos', other_player)
            player.character.add_watcher('list_append', other_player)
            player.character.add_watcher('list_remove', other_player)

def get_game() :
    return Arena()
