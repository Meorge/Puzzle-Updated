
#############################################################################################
########################## Tileset Class and Tile/Object Subclasses #########################

class TilesetClass():
    '''Contains Tileset data. Inits itself to a blank tileset.
    Methods: addTile, removeTile, addObject, removeObject, clear'''

    class Tile():
        def __init__(self, image, noalpha, bytelist):
            '''Tile Constructor'''

            self.image = image
            self.noalpha = noalpha
            self.byte0 = bytelist[0]
            self.byte1 = bytelist[1]
            self.byte2 = bytelist[2]
            self.byte3 = bytelist[3]
            self.byte4 = bytelist[4]
            self.byte5 = bytelist[5]
            self.byte6 = bytelist[6]
            self.byte7 = bytelist[7]


    class Object():

        def __init__(self, height, width, uslope, lslope, tilelist):
            '''Tile Constructor'''

            self.height = height
            self.width = width

            self.upperslope = uslope
            self.lowerslope = lslope

            self.tiles = tilelist


    def __init__(self):
        '''Constructor'''

        self.tiles = []
        self.objects = []
        self.unknownFiles = {}

        self.slot = 0


    def addTile(self, image, noalpha, bytelist = (0, 0, 0, 0, 0, 0, 0, 0)):
        '''Adds an tile class to the tile list with the passed image or parameters'''

        self.tiles.append(self.Tile(image, noalpha, bytelist))


    def addObject(self, height = 1, width = 1,  uslope = [0, 0], lslope = [0, 0], tilelist = [[(0, 0, 0)]]):
        '''Adds a new object'''

        global Tileset

        if tilelist == [[(0, 0, 0)]]:
            tilelist = [[(0, 0, Tileset.slot)]]

        self.objects.append(self.Object(height, width, uslope, lslope, tilelist))


    def removeObject(self, index):
        '''Removes an Object by Index number. Don't use this much, because we want objects to preserve their ID.'''

        self.objects.pop(index)


    def clear(self):
        '''Clears the tileset for a new file'''

        self.tiles = []
        self.objects = []
        self.unknownFiles = {}