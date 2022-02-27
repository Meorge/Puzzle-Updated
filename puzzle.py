#!/usr/bin/env python3

from ObjectList import ObjectList
from PuzzleApplication import PuzzleApplication
from Tileset import TilesetClass
import archive
import lz77
import os, os.path
import struct
import sys

from ctypes import create_string_buffer
try:
    from PyQt6 import QtCore, QtGui, QtWidgets
except ImportError:
    from PySide2 import QtCore, QtGui, QtWidgets
Qt = QtCore.Qt

from PaletteWidget import PaletteWidget
from InfoBoxWidget import InfoBoxWidget
from DisplayWidget import displayWidget

try:
    import nsmblib
    HaveNSMBLib = True
except ImportError:
    HaveNSMBLib = False


if hasattr(QtCore, 'pyqtSlot'): # PyQt
    QtCoreSlot = QtCore.pyqtSlot
    QtCoreSignal = QtCore.pyqtSignal
else: # PySide2
    QtCoreSlot = QtCore.Slot
    QtCoreSignal = QtCore.Signal


########################################################
# To Do:
#
#   - Object Editor
#       - Moving objects around
#
#   - Make UI simpler for Pop
#   - fix up conflicts with different types of parameters
#   - C speed saving
#   - quick settings for applying to mulitple slopes
#
########################################################

def module_path():
    """
    This will get us the program's directory, even if we are frozen
    using PyInstaller
    """

    if hasattr(sys, 'frozen') and hasattr(sys, '_MEIPASS'):  # PyInstaller
        if sys.platform == 'darwin':  # macOS
            # sys.executable is /x/y/z/puzzle.app/Contents/MacOS/puzzle
            # We need to return /x/y/z/puzzle.app/Contents/Resources/

            macos = os.path.dirname(sys.executable)
            if os.path.basename(macos) != 'MacOS':
                return None

            return os.path.join(os.path.dirname(macos), 'Resources')

        else:  # Windows, Linux
            return os.path.dirname(sys.executable)

    if __name__ == '__main__':
        return os.path.dirname(os.path.abspath(__file__))

    return None



#############################################################################################
##################### Object List Widget and Model Setup with Painter #######################






def SetupObjectModel(self, objects, tiles):
    self.clear()

    count = 0
    for object in objects:
        tex = QtGui.QPixmap(object.width * 24, object.height * 24)
        tex.fill(Qt.GlobalColor.transparent)
        painter = QtGui.QPainter(tex)

        Xoffset = 0
        Yoffset = 0

        for i in range(len(object.tiles)):
            for tile in object.tiles[i]:
                if (PuzzleApplication.instance().tileset().slot == 0) or ((tile[2] & 3) != 0):
                    painter.drawPixmap(Xoffset, Yoffset, tiles[tile[1]].image)
                Xoffset += 24
            Xoffset = 0
            Yoffset += 24

        painter.end()

        item = QtGui.QStandardItem(QtGui.QIcon(tex), 'Object {0}'.format(count))
        item.setEditable(False)
        self.appendRow(item)

        count += 1

#############################################################################################
################## Python-based RGB5a3 Decoding code from my BRFNT program ##################


RGB4A3LUT = []
RGB4A3LUT_NoAlpha = []
def PrepareRGB4A3LUTs():
    global RGB4A3LUT, RGB4A3LUT_NoAlpha

    RGB4A3LUT = [None] * 0x10000
    RGB4A3LUT_NoAlpha = [None] * 0x10000
    for LUT, hasA in [(RGB4A3LUT, True), (RGB4A3LUT_NoAlpha, False)]:

        # RGB4A3
        for d in range(0x8000):
            if hasA:
                alpha = d >> 12
                alpha = alpha << 5 | alpha << 2 | alpha >> 1
            else:
                alpha = 0xFF
            red = ((d >> 8) & 0xF) * 17
            green = ((d >> 4) & 0xF) * 17
            blue = (d & 0xF) * 17
            LUT[d] = blue | (green << 8) | (red << 16) | (alpha << 24)

        # RGB555
        for d in range(0x8000):
            red = d >> 10
            red = red << 3 | red >> 2
            green = (d >> 5) & 0x1F
            green = green << 3 | green >> 2
            blue = d & 0x1F
            blue = blue << 3 | blue >> 2
            LUT[d + 0x8000] = blue | (green << 8) | (red << 16) | 0xFF000000

PrepareRGB4A3LUTs()


def RGB4A3Decode(tex, useAlpha=True):
    tx = 0; ty = 0
    iter = tex.__iter__()
    dest = [0] * 262144

    LUT = RGB4A3LUT if useAlpha else RGB4A3LUT_NoAlpha

    # Loop over all texels (of which there are 16384)
    for i in range(16384):
        temp1 = (i // 256) % 8
        if temp1 == 0 or temp1 == 7:
            # Skip every row of texels that is a multiple of 8 or (a
            # multiple of 8) - 1
            # Unrolled loop for performance.
            next(iter); next(iter); next(iter); next(iter)
            next(iter); next(iter); next(iter); next(iter)
            next(iter); next(iter); next(iter); next(iter)
            next(iter); next(iter); next(iter); next(iter)
            next(iter); next(iter); next(iter); next(iter)
            next(iter); next(iter); next(iter); next(iter)
            next(iter); next(iter); next(iter); next(iter)
            next(iter); next(iter); next(iter); next(iter)
        else:
            temp2 = i % 8
            if temp2 == 0 or temp2 == 7:
                # Skip every column of texels that is a multiple of 8
                # or (a multiple of 8) - 1
                # Unrolled loop for performance.
                next(iter); next(iter); next(iter); next(iter)
                next(iter); next(iter); next(iter); next(iter)
                next(iter); next(iter); next(iter); next(iter)
                next(iter); next(iter); next(iter); next(iter)
                next(iter); next(iter); next(iter); next(iter)
                next(iter); next(iter); next(iter); next(iter)
                next(iter); next(iter); next(iter); next(iter)
                next(iter); next(iter); next(iter); next(iter)
            else:
                # Actually render this texel
                for y in range(ty, ty+4):
                    for x in range(tx, tx+4):
                        dest[x + y * 1024] = LUT[next(iter) << 8 | next(iter)]

        # Move on to the next texel
        tx += 4
        if tx >= 1024: tx = 0; ty += 4

    # Convert the list of ARGB color values into a bytes object, and
    # then convert that into a QImage
    return QtGui.QImage(struct.pack('<262144I', *dest), 1024, 256, QtGui.QImage.Format_ARGB32)


def RGB4A3Encode(tex):
    shorts = []
    colorCache = {}
    for ytile in range(0, 256, 4):
        for xtile in range(0, 1024, 4):
            for ypixel in range(ytile, ytile + 4):
                for xpixel in range(xtile, xtile + 4):

                    if xpixel >= 1024 or ypixel >= 256:
                        continue

                    pixel = tex.pixel(xpixel, ypixel)

                    if pixel in colorCache:
                        rgba = colorCache[pixel]

                    else:

                        a = pixel >> 24
                        r = (pixel >> 16) & 0xFF
                        g = (pixel >> 8) & 0xFF
                        b = pixel & 0xFF

                        # See encodingTests.py for verification that these
                        # channel conversion formulas are 100% correct

                        # It'd be nice if we could do
                        # if a < 19:
                        #     rgba = 0
                        # for speed, but that defeats the purpose of the
                        # "Toggle Alpha" setting.

                        if a < 238: # RGB4A3
                            alpha = ((a + 18) << 1) // 73
                            red = (r + 8) // 17
                            green = (g + 8) // 17
                            blue = (b + 8) // 17

                            # 0aaarrrrggggbbbb
                            rgba = blue | (green << 4) | (red << 8) | (alpha << 12)

                        else: # RGB555
                            red = ((r + 4) << 2) // 33
                            green = ((g + 4) << 2) // 33
                            blue = ((b + 4) << 2) // 33

                            # 1rrrrrgggggbbbbb
                            rgba = blue | (green << 5) | (red << 10) | (0x8000)

                        colorCache[pixel] = rgba

                    shorts.append(rgba)

                    if xtile % 32 == 0 or xtile % 32 == 28:
                        shorts.append(rgba)
                        shorts.append(rgba)
                        shorts.append(rgba)
                        break
                if ytile % 32 == 0 or ytile % 32 == 28:
                    shorts.extend(shorts[-4:])
                    shorts.extend(shorts[-8:])
                    break

    return struct.pack('>262144H', *shorts)


#############################################################################################
############ Main Window Class. Takes care of menu functions and widget creation ############

from PiecesModel import PiecesModel
from TileOverlord import TileOverlord

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.alpha = True

        self.name = ''

        self.setupMenus()
        self.setupWidgets()

        self.setuptile()

        self.newTileset()

        self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed,
                QtWidgets.QSizePolicy.Policy.Fixed))
        self.setWindowTitle("New Tileset")


    def setuptile(self):
        self.tileWidget.tiles.clear()
        self.model.clear()

        if self.alpha == True:
            for tile in PuzzleApplication.instance().tileset().tiles:
                self.model.addPieces(tile.image)
        else:
            for tile in PuzzleApplication.instance().tileset().tiles:
                self.model.addPieces(tile.noalpha)


    def newTileset(self):
        '''Creates a new, blank tileset'''

        PuzzleApplication.instance().tileset().clear()
        PuzzleApplication.instance().setTileset(TilesetClass())

        EmptyPix = QtGui.QPixmap(24, 24)
        EmptyPix.fill(Qt.GlobalColor.black)

        for i in range(256):
            PuzzleApplication.instance().tileset().addTile(EmptyPix, EmptyPix)

        self.setuptile()
        self.setWindowTitle('New Tileset')


    def openTileset(self):
        '''Asks the user for a filename, then calls openTilesetFromPath().'''

        path = QtWidgets.QFileDialog.getOpenFileName(self, "Open NSMBW Tileset", '',
                    "Tileset Files (*.arc)")[0]

        if path:
            self.openTilesetFromPath(path)


    def openTilesetFromPath(self, path):
        '''Opens a Nintendo tileset arc and parses the heck out of it.'''
        self.setWindowTitle(os.path.basename(path))
        PuzzleApplication.instance().tileset().clear()

        name = path[str(path).rfind('/')+1:-4]

        with open(path,'rb') as file:
            data = file.read()

        arc = archive.U8()
        arc._load(data)

        Image = None
        behaviourdata = None
        objstrings = None
        metadata = None

        for key, value in arc.files:
            if value is None:
                continue
            elif key.startswith('BG_tex/') and key.endswith('_tex.bin.LZ'):
                Image = arc[key]
            elif key.startswith('BG_chk/d_bgchk_') and key.endswith('.bin'):
                behaviourdata = arc[key]
            elif key.startswith('BG_unt/') and key.endswith('_hd.bin'):
                metadata = arc[key]
            elif key.startswith('BG_unt/') and key.endswith('.bin'):
                objstrings = arc[key]
            else:
                PuzzleApplication.instance().tileset().unknownFiles[key] = arc[key]


        if (Image is None) or (behaviourdata is None) or (objstrings is None) or (metadata is None):
            QtWidgets.QMessageBox.warning(None, 'Error',  'Error - the necessary files were not found.\n\nNot a valid tileset, sadly.')
            return

        # Stolen from Reggie! Loads the Image Data.
        if HaveNSMBLib:
            tiledata = nsmblib.decompress11LZS(Image)
            if hasattr(nsmblib, 'decodeTilesetNoPremultiplication'):
                argbdata = nsmblib.decodeTilesetNoPremultiplication(tiledata)
                dest = QtGui.QImage(argbdata, 1024, 256, 4096, QtGui.QImage.Format.Format_ARGB32)
            else:
                dest = RGB4A3Decode(tiledata)

            if hasattr(nsmblib, 'decodeTilesetNoPremultiplicationNoAlpha'):
                rgbdata = nsmblib.decodeTilesetNoPremultiplicationNoAlpha(tiledata)
                noalphadest = QtGui.QImage(rgbdata, 1024, 256, 4096, QtGui.QImage.Format.Format_ARGB32)
            else:
                noalphadest = RGB4A3Decode(tiledata, False)
        else:
            lz = lz77.LZS11()
            decomp = lz.Decompress11LZS(Image)
            dest = RGB4A3Decode(decomp)
            noalphadest = RGB4A3Decode(decomp, False)

        tileImage = QtGui.QPixmap.fromImage(dest)
        noalpha = QtGui.QPixmap.fromImage(noalphadest)

        # Loads Tile Behaviours

        behaviours = []
        for entry in range(256):
            behaviours.append(struct.unpack_from('>8B', behaviourdata, entry*8))


        # Makes us some nice Tile Classes!
        Xoffset = 4
        Yoffset = 4
        for i in range(256):
            PuzzleApplication.instance().tileset().addTile(tileImage.copy(Xoffset,Yoffset,24,24), noalpha.copy(Xoffset,Yoffset,24,24), behaviours[i])
            Xoffset += 32
            if Xoffset >= 1024:
                Xoffset = 4
                Yoffset += 32


        # Load Objects

        meta = []
        for i in range(len(metadata) // 4):
            meta.append(struct.unpack_from('>H2B', metadata, i * 4))

        tilelist = [[]]
        upperslope = [0, 0]
        lowerslope = [0, 0]
        byte = 0

        for entry in meta:
            offset = entry[0]
            byte = struct.unpack_from('>B', objstrings, offset)[0]
            row = 0

            while byte != 0xFF:

                if byte == 0xFE:
                    tilelist.append([])

                    if (upperslope[0] != 0) and (lowerslope[0] == 0):
                        upperslope[1] = upperslope[1] + 1

                    if lowerslope[0] != 0:
                        lowerslope[1] = lowerslope[1] + 1

                    offset += 1
                    byte = struct.unpack_from('>B', objstrings, offset)[0]

                elif (byte & 0x80):

                    if upperslope[0] == 0:
                        upperslope[0] = byte
                    else:
                        lowerslope[0] = byte

                    offset += 1
                    byte = struct.unpack_from('>B', objstrings, offset)[0]

                else:
                    tilelist[len(tilelist)-1].append(struct.unpack_from('>3B', objstrings, offset))

                    offset += 3
                    byte = struct.unpack_from('>B', objstrings, offset)[0]

            tilelist.pop()

            if (upperslope[0] & 0x80) and (upperslope[0] & 0x2):
                for i in range(lowerslope[1]):
                    pop = tilelist.pop()
                    tilelist.insert(0, pop)

            PuzzleApplication.instance().tileset().addObject(entry[2], entry[1], upperslope, lowerslope, tilelist)

            tilelist = [[]]
            upperslope = [0, 0]
            lowerslope = [0, 0]

        if PuzzleApplication.instance().tileset().objects:
            PuzzleApplication.instance().tileset().slot = PuzzleApplication.instance().tileset().objects[0].tiles[0][0][2] & 3
        else:
            PuzzleApplication.instance().tileset().slot = 1
        self.tileWidget.tilesetType.setText('Pa{0}'.format(PuzzleApplication.instance().tileset().slot))

        self.setuptile()
        SetupObjectModel(self.objmodel, PuzzleApplication.instance().tileset().objects, PuzzleApplication.instance().tileset().tiles)

        self.name = path


    def openImage(self):
        '''Opens an Image from png, and creates a new tileset from it.'''

        path = QtWidgets.QFileDialog.getOpenFileName(self, "Open Image", '',
                    "Image Files (*.png)")[0]

        if not path: return

        tileImage = QtGui.QPixmap()
        if not tileImage.load(path):
            QtWidgets.QMessageBox.warning(self, "Open Image",
                    "The image file could not be loaded.",
                    QtWidgets.QMessageBox.Cancel)
            return


        if tileImage.width() != 384 or tileImage.height() != 384:
            QtWidgets.QMessageBox.warning(self, "Open Image",
                    "The image was not the proper dimensions."
                    "Please resize the image to 384x384 pixels.",
                    QtWidgets.QMessageBox.Cancel)
            return

        noalphaImage = QtGui.QPixmap(384, 384)
        noalphaImage.fill(Qt.GlobalColor.black)
        p = QtGui.QPainter(noalphaImage)
        p.drawPixmap(0, 0, tileImage)
        p.end()
        del p

        x = 0
        y = 0
        for i in range(256):
            PuzzleApplication.instance().tileset().tiles[i].image = tileImage.copy(x*24,y*24,24,24)
            PuzzleApplication.instance().tileset().tiles[i].noalpha = noalphaImage.copy(x*24,y*24,24,24)
            x += 1
            if (x * 24) >= 384:
                y += 1
                x = 0

        self.setuptile()


    def saveImage(self):

        fn = QtWidgets.QFileDialog.getSaveFileName(self, 'Choose a new filename', '', '.png (*.png)')[0]
        if not fn: return

        tex = QtGui.QPixmap(384, 384)
        tex.fill(Qt.GlobalColor.transparent)
        painter = QtGui.QPainter(tex)

        Xoffset = 0
        Yoffset = 0

        for tile in PuzzleApplication.instance().tileset().tiles:
            painter.drawPixmap(Xoffset, Yoffset, tile.image)
            Xoffset += 24
            if Xoffset >= 384:
                Xoffset = 0
                Yoffset += 24

        painter.end()

        tex.save(fn)


    def saveTileset(self):
        if not self.name:
            self.saveTilesetAs()
            return

        outdata = self.saving(os.path.basename(self.name)[:-4])

        if outdata is not None:
            fn = self.name
            with open(fn, 'wb') as f:
                f.write(outdata)


    def saveTilesetAs(self):

        fn = QtWidgets.QFileDialog.getSaveFileName(self, 'Choose a new filename', '', '.arc (*.arc)')[0]
        if not fn: return

        outdata = self.saving(os.path.basename(str(fn))[:-4])

        if outdata is not None:
            self.name = fn
            self.setWindowTitle(os.path.basename(str(fn)))

            with open(fn, 'wb') as f:
                f.write(outdata)


    def saving(self, name):

        # Prepare tiles, objects, object metadata, and textures and stuff into buffers.

        textureBuffer = self.PackTexture()

        if textureBuffer is None:
            # The user canceled the saving process in the "use nsmblib?" dialog
            return None

        tileBuffer = self.PackTiles()
        objectBuffers = self.PackObjects()
        objectBuffer = objectBuffers[0]
        objectMetaBuffer = objectBuffers[1]


        # Make an arc and pack up the files!

        # NOTE: adding the files/folders to the U8 object in
        # alphabetical order is a simple workaround for a wii.py... bug?
        # unintuitive quirk? Whatever. Fixes one of the issues listed
        # in GitHub issue #3 (in the RoadrunnerWMC/Puzzle-Updated repo)

        arcFiles = {}
        arcFiles['BG_tex'] = None
        arcFiles['BG_tex/{0}_tex.bin.LZ'.format(name)] = textureBuffer

        arcFiles['BG_chk'] = None
        arcFiles['BG_chk/d_bgchk_{0}.bin'.format(name)] = tileBuffer

        arcFiles['BG_unt'] = None
        arcFiles['BG_unt/{0}.bin'.format(name)] = objectBuffer
        arcFiles['BG_unt/{0}_hd.bin'.format(name)] = objectMetaBuffer

        arcFiles.update(PuzzleApplication.instance().tileset().unknownFiles)

        arc = archive.U8()
        for name in sorted(arcFiles):
            arc[name] = arcFiles[name]
        return arc._dump()


    def PackTexture(self):

        tex = QtGui.QImage(1024, 256, QtGui.QImage.Format.Format_ARGB32)
        tex.fill(Qt.GlobalColor.transparent)
        painter = QtGui.QPainter(tex)

        Xoffset = 0
        Yoffset = 0

        for tile in PuzzleApplication.instance().tileset().tiles:
            minitex = QtGui.QImage(32, 32, QtGui.QImage.Format.Format_ARGB32)
            minitex.fill(Qt.GlobalColor.transparent)
            minipainter = QtGui.QPainter(minitex)

            minipainter.drawPixmap(4, 4, tile.image)
            minipainter.end()

            # Read colours and DESTROY THEM (or copy them to the edges, w/e)
            for i in range(4,28):

                # Top Clamp
                colour = minitex.pixel(i, 4)
                for p in range(0,5):
                    minitex.setPixel(i, p, colour)

                # Left Clamp
                colour = minitex.pixel(4, i)
                for p in range(0,5):
                    minitex.setPixel(p, i, colour)

                # Right Clamp
                colour = minitex.pixel(i, 27)
                for p in range(27,32):
                    minitex.setPixel(i, p, colour)

                # Bottom Clamp
                colour = minitex.pixel(27, i)
                for p in range(27,32):
                    minitex.setPixel(p, i, colour)

            # UpperLeft Corner Clamp
            colour = minitex.pixel(4, 4)
            for x in range(0,5):
                for y in range(0,5):
                    minitex.setPixel(x, y, colour)

            # UpperRight Corner Clamp
            colour = minitex.pixel(27, 4)
            for x in range(27,32):
                for y in range(0,5):
                    minitex.setPixel(x, y, colour)

            # LowerLeft Corner Clamp
            colour = minitex.pixel(4, 27)
            for x in range(0,5):
                for y in range(27,32):
                    minitex.setPixel(x, y, colour)

            # LowerRight Corner Clamp
            colour = minitex.pixel(27, 27)
            for x in range(27,32):
                for y in range(27,32):
                    minitex.setPixel(x, y, colour)


            painter.drawImage(Xoffset, Yoffset, minitex)

            Xoffset += 32

            if Xoffset >= 1024:
                Xoffset = 0
                Yoffset += 32

        painter.end()

        dest = RGB4A3Encode(tex)

        useNSMBLib = HaveNSMBLib and hasattr(nsmblib, 'compress11LZS')

        if useNSMBLib:
            # There are two versions of nsmblib floating around: the original
            # one, where the compression doesn't work correctly, and a fixed one
            # with correct compression.
            # We're going to show a warning to the user if they have the broken one installed.
            # To detect which one it is, we use the following test data:
            COMPRESSION_TEST = b'\0\1\0\0\0\0\0\0\0\1\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0'

            # The original broken algorithm compresses that incorrectly.
            # So let's compress it, and then decompress it, and see if we
            # got the right output.
            compressionWorking = (nsmblib.decompress11LZS(nsmblib.compress11LZS(COMPRESSION_TEST)) == COMPRESSION_TEST)

            if not compressionWorking:
                # NSMBLib is available, but only with the broken compression algorithm,
                # so the user can choose whether to use it or not

                items = ("Slow Compression, Good Quality", "Fast Compression, but the Image gets damaged")

                item, ok = QtWidgets.QInputDialog.getItem(self, "Choose compression method",
                        "Two methods of compression are available. Choose<br />"
                        "Fast compression for rapid testing. Choose slow<br />"
                        "compression for releases.<br />"
                        "<br />"
                        "To fix the fast compression, download and install<br />"
                        "NSMBLib-Updated (\"pip uninstall nsmblib\", \"pip<br />"
                        "install nsmblib\").\n", items, 0, False)
                if not ok:
                    return None

                if item == "Slow Compression, Good Quality":
                    useNSMBLib = False
                else:
                    useNSMBLib = True

        else:
            # NSMBLib is not available, so we have to use the Python version
            useNSMBLib = False

        if useNSMBLib:
            TexBuffer = nsmblib.compress11LZS(dest)
        else:
            lz = lz77.LZS11()
            TexBuffer = lz.Compress11LZS(dest)

        return TexBuffer


    def PackTiles(self):
        offset = 0
        tilespack = struct.Struct('>8B')
        Tilebuffer = create_string_buffer(2048)
        for tile in PuzzleApplication.instance().tileset().tiles:
            tilespack.pack_into(Tilebuffer, offset, tile.byte0, tile.byte1, tile.byte2, tile.byte3, tile.byte4, tile.byte5, tile.byte6, tile.byte7)
            offset += 8

        return Tilebuffer.raw


    def PackObjects(self):
        objectStrings = []

        o = 0
        for object in PuzzleApplication.instance().tileset().objects:


            # Slopes
            if object.upperslope[0] != 0:

                # Reverse Slopes
                if object.upperslope[0] & 0x2:
                    a = struct.pack('>B', object.upperslope[0])

                    if object.height == 1:
                        iterationsA = 0
                        iterationsB = 1
                    else:
                        iterationsA = object.upperslope[1]
                        iterationsB = object.lowerslope[1] + object.upperslope[1]

                    for row in range(iterationsA, iterationsB):
                        for tile in object.tiles[row]:
                            a = a + struct.pack('>BBB', tile[0], tile[1], tile[2])
                        a = a + b'\xfe'

                    if object.height > 1:
                        a = a + struct.pack('>B', object.lowerslope[0])

                        for row in range(0, object.upperslope[1]):
                            for tile in object.tiles[row]:
                                a = a + struct.pack('>BBB', tile[0], tile[1], tile[2])
                            a = a + b'\xfe'

                    a = a + b'\xff'

                    objectStrings.append(a)


                # Regular Slopes
                else:
                    a = struct.pack('>B', object.upperslope[0])

                    for row in range(0, object.upperslope[1]):
                        for tile in object.tiles[row]:
                            a = a + struct.pack('>BBB', tile[0], tile[1], tile[2])
                        a = a + b'\xfe'

                    if object.height > 1:
                        a = a + struct.pack('>B', object.lowerslope[0])

                        for row in range(object.upperslope[1], object.height):
                            for tile in object.tiles[row]:
                                a = a + struct.pack('>BBB', tile[0], tile[1], tile[2])
                            a = a + b'\xfe'

                    a = a + b'\xff'

                    objectStrings.append(a)


            # Not slopes!
            else:
                a = b''

                for tilerow in object.tiles:
                    for tile in tilerow:
                        a = a + struct.pack('>BBB', tile[0], tile[1], tile[2])

                    a = a + b'\xfe'

                a = a + b'\xff'

                objectStrings.append(a)

            o += 1

        Objbuffer = b''
        Metabuffer = b''
        i = 0
        for a in objectStrings:
            Metabuffer = Metabuffer + struct.pack('>H2B', len(Objbuffer), PuzzleApplication.instance().tileset().objects[i].width, PuzzleApplication.instance().tileset().objects[i].height)
            Objbuffer = Objbuffer + a

            i += 1

        return (Objbuffer, Metabuffer)



    def setupMenus(self):
        fileMenu = self.menuBar().addMenu("&File")

        pixmap = QtGui.QPixmap(60,60)
        pixmap.fill(Qt.GlobalColor.black)
        icon = QtGui.QIcon(pixmap)

        self.action = fileMenu.addAction(icon, "New", self.newTileset, QtGui.QKeySequence.StandardKey.New)
        fileMenu.addAction("Open...", self.openTileset, QtGui.QKeySequence.StandardKey.Open)
        fileMenu.addAction("Import Image...", self.openImage, QtGui.QKeySequence('Ctrl+I'))
        fileMenu.addAction("Export Image...", self.saveImage, QtGui.QKeySequence('Ctrl+E'))
        fileMenu.addAction("Save", self.saveTileset, QtGui.QKeySequence.StandardKey.Save)
        fileMenu.addAction("Save as...", self.saveTilesetAs, QtGui.QKeySequence.StandardKey.SaveAs)
        fileMenu.addAction("Quit", self.close, QtGui.QKeySequence('Ctrl-Q'))

        fileMenu.addSeparator()
        nsmblibAct = fileMenu.addAction('Using NSMBLib' if HaveNSMBLib else 'Not using NSMBLib')
        nsmblibAct.setEnabled(False)

        taskMenu = self.menuBar().addMenu("&Tasks")

        taskMenu.addAction("Set Tileset Slot...", self.setSlot, QtGui.QKeySequence('Ctrl+T'))
        taskMenu.addAction("Toggle Alpha", self.toggleAlpha, QtGui.QKeySequence('Ctrl+Shift+A'))
        taskMenu.addAction("Clear Collision Data", self.clearCollisions, QtGui.QKeySequence('Ctrl+Shift+Backspace'))
        taskMenu.addAction("Clear Object Data", self.clearObjects, QtGui.QKeySequence('Ctrl+Alt+Backspace'))



    def setSlot(self):
        global Tileset

        items = ("Pa0", "Pa1", "Pa2", "Pa3")

        item, ok = QtWidgets.QInputDialog.getItem(self, "Set Tileset Slot",
                "Warning: \n    Setting the tileset slot will override any \n    tiles set to draw from other tilesets.\n\nCurrent slot is Pa%d" % PuzzleApplication.instance().tileset().slot, items, 0, False)
        if ok and item:
            PuzzleApplication.instance().tileset().slot = int(item[2])
            self.tileWidget.tilesetType.setText(item)


            cobj = 0
            crow = 0
            ctile = 0
            for object in PuzzleApplication.instance().tileset().objects:
                for row in object.tiles:
                    for tile in row:
                        if tile != (0,0,0):
                            PuzzleApplication.instance().tileset().objects[cobj].tiles[crow][ctile] = (tile[0], tile[1], (tile[2] & 0xFC) | int(str(item[2])))
                        if tile == (0,0,0) and ctile == 0:
                            PuzzleApplication.instance().tileset().objects[cobj].tiles[crow][ctile] = (tile[0], tile[1], (tile[2] & 0xFC) | int(str(item[2])))
                        ctile += 1
                    crow += 1
                    ctile = 0
                cobj += 1
                crow = 0
                ctile = 0


    def toggleAlpha(self):
        # Replace Alpha Image with non-Alpha images in model
        if self.alpha == True:
            self.alpha = False
        else:
            self.alpha = True

        self.setuptile()

    def clearObjects(self):
        '''Clears the object data'''

        PuzzleApplication.instance().tileset().objects = []

        SetupObjectModel(self.objmodel, PuzzleApplication.instance().tileset().objects, PuzzleApplication.instance().tileset().tiles)

        self.objectList.update()
        self.tileWidget.update()


    def clearCollisions(self):
        '''Clears the collisions data'''

        for tile in PuzzleApplication.instance().tileset().tiles:
            tile.byte0 = 0
            tile.byte1 = 0
            tile.byte2 = 0
            tile.byte3 = 0
            tile.byte4 = 0
            tile.byte5 = 0
            tile.byte6 = 0
            tile.byte7 = 0

        self.updateInfo(0, 0)
        self.tileDisplay.update()


    def setupWidgets(self):
        frame = QtWidgets.QFrame()
        frameLayout = QtWidgets.QGridLayout(frame)

        # Displays the tiles
        self.tileDisplay = displayWidget(self, self)

        # Info Box for tile information
        self.infoDisplay = InfoBoxWidget(self)

        # Sets up the model for the tile pieces
        self.model = PiecesModel(self)
        self.tileDisplay.setModel(self.model)

        # Object List
        self.objectList = ObjectList()
        self.objmodel = QtGui.QStandardItemModel()
        SetupObjectModel(self.objmodel, PuzzleApplication.instance().tileset().objects, PuzzleApplication.instance().tileset().tiles)
        self.objectList.setModel(self.objmodel)

        # Creates the Tab Widget for behaviours and objects
        self.tabWidget = QtWidgets.QTabWidget()
        self.tileWidget = TileOverlord()
        self.paletteWidget = PaletteWidget(self)

        # Second Tab
        self.container = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.objectList)
        layout.addWidget(self.tileWidget)
        self.container.setLayout(layout)

        # Sets the Tabs
        self.tabWidget.addTab(self.paletteWidget, 'Behaviours')
        self.tabWidget.addTab(self.container, 'Objects')

        # Connections do things!
        self.tileDisplay.clicked.connect(self.paintFormat)
        self.tileDisplay.mouseMoved.connect(self.updateInfo)
        self.objectList.clicked.connect(self.tileWidget.setObject)

        # Layout
        frameLayout.addWidget(self.infoDisplay, 0, 0, 1, 1)
        frameLayout.addWidget(self.tileDisplay, 1, 0)
        frameLayout.addWidget(self.tabWidget, 0, 1, 2, 1)
        self.setCentralWidget(frame)


    def updateInfo(self, x, y):

        index = [self.tileDisplay.indexAt(QtCore.QPoint(x, y))]
        curTile = PuzzleApplication.instance().tileset().tiles[index[0].row()]
        info = self.infoDisplay
        palette = self.paletteWidget

        propertyList = []
        propertyText = ''
        coreType = 0

        if curTile.byte3 & 32:
            coreType = 1
        elif curTile.byte3 & 64:
            coreType = 2
        elif curTile.byte2 & 8:
            coreType = 3
        elif curTile.byte3 & 2:
            coreType = 4
        elif curTile.byte3 & 8:
            coreType = 5
        elif curTile.byte2 & 4:
            coreType = 6
        elif curTile.byte2 & 16:
            coreType = 7
        elif curTile.byte1 & 1:
            coreType = 8
        elif 0 > curTile.byte7 > 0x23:
            coretype = 9
        elif curTile.byte5 == 4 or 5:
            coretype = 10
        elif curTile.byte3 & 4:
            coreType = 11

        if curTile.byte3 & 1:
            propertyList.append('Solid')
        if curTile.byte3 & 16:
            propertyList.append('Breakable')
        if curTile.byte2 & 128:
            propertyList.append('Pass-Through')
        if curTile.byte2 & 64:
            propertyList.append('Pass-Down')
        if curTile.byte1 & 2:
            propertyList.append('Falling')
        if curTile.byte1 & 8:
            propertyList.append('Ledge')
        if curTile.byte0 & 2:
            propertyList.append('Meltable')


        if len(propertyList) == 0:
            propertyText = 'None'
        elif len(propertyList) == 1:
            propertyText = propertyList[0]
        else:
            propertyText = propertyList.pop(0)
            for string in propertyList:
                propertyText = propertyText + ', ' + string

        if coreType == 0:
            if curTile.byte7 == 0x23:
                parameter = palette.ParameterList[coreType][1]
            elif curTile.byte7 == 0x28:
                parameter = palette.ParameterList[coreType][2]
            elif curTile.byte7 >= 0x35:
                parameter = palette.ParameterList[coreType][curTile.byte7 - 0x32]
            else:
                parameter = palette.ParameterList[coreType][0]
        else:
            parameter = palette.ParameterList[coreType][curTile.byte7]


        info.coreImage.setPixmap(palette.coreTypes[coreType][1].pixmap(24,24))
        info.terrainImage.setPixmap(palette.terrainTypes[curTile.byte5][1].pixmap(24,24))
        info.parameterImage.setPixmap(parameter[1].pixmap(24,24))

        info.coreInfo.setText(palette.coreTypes[coreType][0])
        info.propertyInfo.setText(propertyText)
        info.terrainInfo.setText(palette.terrainTypes[curTile.byte5][0])
        info.paramInfo.setText(parameter[0])

        info.hexdata.setText('Hex Data: {0} {1} {2} {3}\n                {4} {5} {6} {7}'.format(
                                hex(curTile.byte0), hex(curTile.byte1), hex(curTile.byte2), hex(curTile.byte3),
                                hex(curTile.byte4), hex(curTile.byte5), hex(curTile.byte6), hex(curTile.byte7)))



    def paintFormat(self, index):
        if self.tabWidget.currentIndex() == 1:
            return

        curTile = PuzzleApplication.instance().tileset().tiles[index.row()]
        palette = self.paletteWidget

        if palette.coreWidgets[8].isChecked() == 1 or palette.propertyWidgets[0].isChecked() == 1:
            solid = 1
        else:
            solid = 0

        if palette.coreWidgets[1].isChecked() == 1 or palette.coreWidgets[2].isChecked() == 1:
            solid = 0


        curTile.byte0 = ((palette.propertyWidgets[4].isChecked() << 1))
        curTile.byte1 = ((palette.coreWidgets[8].isChecked()) +
                        (palette.propertyWidgets[2].isChecked() << 1) +
                        (palette.propertyWidgets[3].isChecked() << 3))
        curTile.byte2 = ((palette.coreWidgets[6].isChecked() << 2) +
                        (palette.coreWidgets[3].isChecked() << 3) +
                        (palette.coreWidgets[7].isChecked() << 4) +
                        (palette.PassDown.isChecked() << 6) +
                        (palette.PassThrough.isChecked() << 7))
        curTile.byte3 = ((solid) +
                        (palette.coreWidgets[4].isChecked() << 1) +
                        (palette.coreWidgets[5].isChecked() << 3) +
                        (palette.propertyWidgets[1].isChecked() << 4) +
                        (palette.coreWidgets[1].isChecked() << 5) +
                        (palette.coreWidgets[2].isChecked() << 6) +
                        (palette.coreWidgets[11].isChecked() << 2))
        curTile.byte4 = 0
        if palette.coreWidgets[2].isChecked():
            curTile.byte5 = 4
        curTile.byte5 = palette.terrainType.currentIndex()

        if palette.coreWidgets[0].isChecked():
            params = palette.parameters.currentIndex()
            if params == 0:
                curTile.byte7 = 0
            elif params == 1:
                curTile.byte7 = 0x23
            elif params == 2:
                curTile.byte7 = 0x28
            elif params >= 3:
                curTile.byte7 = params + 0x32
        else:
            curTile.byte7 = palette.parameters.currentIndex()

        self.updateInfo(0, 0)
        self.tileDisplay.update()



#############################################################################################
####################################### Main Function #######################################


if '-nolib' in sys.argv:
    HaveNSMBLib = False
    sys.argv.remove('-nolib')

if __name__ == '__main__':

    import sys

    app = PuzzleApplication(sys.argv)

    # go to the script path
    path = module_path()
    if path is not None:
        os.chdir(path)

    window = MainWindow()

    app.window = window
    if len(sys.argv) > 1:
        window.openTilesetFromPath(sys.argv[1])
    window.show()
    sys.exit(app.exec())
    app.deleteLater()