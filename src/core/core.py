import uuid
import json
from constants import *

class SerializableList(list) :

    #SerializableList(self,[],'identifier')

    def __init__( self, parent, l, name = '' ) :
        if isinstance(parent, (SerializableEntity)) == False :
            raise Exception('ConventionError', 'SerializableList parent argument must be an instance of SerializableEntity')
        if isinstance(l, (list)) == False :
            raise Exception('ConventionError', 'SerializableList l argument must be an instance of list')
        self.parent = parent
        self.name = name
        list.__init__(self,l)

    def append( self, item ) :
        super(SerializableList, self).append(item)
        try:
            item.parent = self.parent
        except Exception as e:
            pass
        self.parent.property_changed( self.name + '_append', item )

    def remove( self, item ) :
        super(SerializableList, self).remove(item)
        try:
            item.parent = None
        except Exception as e:
            pass
        try:
            self.parent.property_changed( self.name + '_remove', item.id )
        except Exception as e:
            self.parent.property_changed( self.name + '_remove', item )

    def to_dict( self ) :
        items = []
        for item in self.__iter__() :
            if isinstance(item, (int, float, str, bool, tuple)) == False :
                try:
                    items += [item.to_dict()]
                except Exception as e:
                    continue
                continue
            items += [item]
        return items

class SerializableEntity(object) :

    def __init__(self) :
        self.id = str(uuid.uuid4())[:8]
        self.parent = None
        self.watchers = {}

    def add_watcher( self, key, watcher ) :
        if self.watchers.get( key ) == None :
            self.watchers[ key ] = [watcher]
            return True
        if watcher not in self.watchers.get( key ) :
            self.watchers[ key ] += [watcher]
            return True
        return False

    def remove_watcher( self, key, watcher ) :
        if self.watchers.get( key ) == None :
            return False
        if watcher in self.watchers.get( key ) :
            self.watchers[ key ].remove(watcher)
            return True
        return False

    def to_dict( self ) :
        dict = {}
        for key, val in self.__dict__.iteritems() :
            if key == 'parent' :
                continue
            if isinstance(val, (int, float, str, bool, tuple)) == False :
                try:
                    dict[key] = val.to_dict()
                except Exception as e:
                    continue
                continue
            dict[key] = val
        dict['type'] = self.__class__.__name__
        return dict

    def property_changed(self, key, value):
        if self.watchers.get( key ) != None :
            for watcher in self.watchers.get( key ) :
                watcher.watched_property_changed( self, key, value )
        if self.parent != None :
            self.parent.property_changed(self.__class__.__name__, value )

class Game(SerializableEntity) :

    game = None

    def __init__( self ) :
        SerializableEntity.__init__(self)
        self.clients = []

    @staticmethod
    def set_game( game ) :
        Game.game = game

    def update( self, messages ) :
        for player in self.clients :
            for message in messages :
                if message[0] == player.id :
                    player.set_input( message[1] )
            player.update()

    def add_client( self, client ) :
        self.clients += [client]

class Sprite(SerializableEntity) :

    def __init__( self, animations ) :
        SerializableEntity.__init__(self)
        self.animations = SerializableList(self,animations,'animations')

class WatchingEntity() :

    def watched_property_changed( self, object, key, value, type = None ) :
        pass

class Player(WatchingEntity) :

    def __init__(self,id) :
        self.id = id
        self.new_data = {'message': 'Welcome'}
        self.input = {}

    def update(self) :
        pass

    def fetch_data( self ) :
        data = self.new_data
        self.new_data = {}
        return data

    def watched_property_changed( self, object, key, val ) :
        if self.new_data.get( object.id ) == None :
            self.new_data[ object.id ] = {}
        if isinstance(val, (int, float, str, bool, tuple)) == False :
            try:
                self.new_data[ object.id ][ key ] = val.to_dict()
            except Exception as e:
                print 'Cannot set ' + key + ' to new data, unable to_dict'
        else :
            self.new_data[ object.id ][ key ] = val

    def set_input( self, message ) :
        for key, value in message.iteritems():
            if key == 'ku' :
                self.input[value] = 0
            elif key == 'kd' :
                self.input[value] = 1


'''
exit(0)
import time
ts = time.time()
s = Foo()
for n in range(0,1) :
    s['health'] = 2
    s.pos['x'] = 3

slow = time.time() - ts

ts = time.time()
s = Foo()
for n in range(0,1) :
    s.health = 2
    s.pos['x'] = 3

fast = time.time() - ts
print slow, fast
print slow - fast
print '------------'
'''
