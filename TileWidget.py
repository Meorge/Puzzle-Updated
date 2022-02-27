from PyQt6.QtWidgets import QWidget, QMenu, QDialog, QComboBox, QSpinBox, QDialogButtonBox, QGridLayout, QLabel, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QPixmap, QColor, QPainter, QIcon, QPen
from PuzzleApplication import PuzzleApplication

class TileWidget(QWidget):
    def __init__(self):
        super(TileWidget, self).__init__()

        self.tiles = []

        self.size = [1, 1]
        self.setMinimumSize(24, 24)

        self.slope = 0

        self.highlightedRect = QRect()

        self.setAcceptDrops(True)
        self.object = 0


    def clear(self):
        self.tiles = []
        self.size = [1, 1] # [width, height]

        self.slope = 0
        self.highlightedRect = QRect()

        self.update()


    def addColumn(self):
        if self.object >= len(PuzzleApplication.instance().tileset().objects):
            return

        if self.size[0] >= 24:
            return

        self.size[0] += 1
        self.setMinimumSize(self.size[0]*24, self.size[1]*24)

        pix = QPixmap(24,24)
        pix.fill(QColor(0,0,0,0))

        for y in range(self.size[1]):
            self.tiles.insert(((y+1) * self.size[0]) -1, [self.size[0]-1, y, pix])


        curObj = PuzzleApplication.instance().tileset().objects[self.object]
        curObj.width += 1

        for row in curObj.tiles:
            row.append((0, 0, 0))

        self.update()
        self.updateList()


    def removeColumn(self):
        if self.size[0] == 1:
            return

        for y in range(self.size[1]):
            self.tiles.pop(((y+1) * self.size[0])-(y+1))

        self.size[0] = self.size[0] - 1
        self.setMinimumSize(self.size[0]*24, self.size[1]*24)


        curObj = PuzzleApplication.instance().tileset().objects[self.object]
        curObj.width -= 1

        for row in curObj.tiles:
            row.pop()

        self.update()
        self.updateList()


    def addRow(self):
        if self.object >= len(PuzzleApplication.instance().tileset().objects):
            return

        if self.size[1] >= 24:
            return

        self.size[1] += 1
        self.setMinimumSize(self.size[0]*24, self.size[1]*24)

        pix = QPixmap(24,24)
        pix.fill(QColor(0,0,0,0))

        for x in range(self.size[0]):
            self.tiles.append([x, self.size[1]-1, pix])

        curObj = PuzzleApplication.instance().tileset().objects[self.object]
        curObj.height += 1

        curObj.tiles.append([])
        for i in range(0, curObj.width):
            curObj.tiles[len(curObj.tiles)-1].append((0, 0, 0))

        self.update()
        self.updateList()


    def removeRow(self):
        if self.size[1] == 1:
            return

        for x in range(self.size[0]):
            self.tiles.pop()

        self.size[1] -= 1
        self.setMinimumSize(self.size[0]*24, self.size[1]*24)

        curObj = PuzzleApplication.instance().tileset().objects[self.object]
        curObj.height -= 1

        curObj.tiles.pop()

        self.update()
        self.updateList()


    def setObject(self, object):
        self.clear()

        self.size = [object.width, object.height]

        if not object.upperslope[1] == 0:
            if object.upperslope[0] & 2:
                self.slope = 0 - object.lowerslope[1]
            else:
                self.slope = object.upperslope[1]

        x = 0
        y = 0
        for row in object.tiles:
            for tile in row:
                if (PuzzleApplication.instance().tileset().slot == 0) or ((tile[2] & 3) != 0):
                    self.tiles.append([x, y, PuzzleApplication.instance().tileset().tiles[tile[1]].image])
                else:
                    pix = QPixmap(24,24)
                    pix.fill(QColor(0,0,0,0))
                    self.tiles.append([x, y, pix])
                x += 1
            y += 1
            x = 0


        self.object = PuzzleApplication.instance().window.objectList.currentIndex().row()
        self.update()
        self.updateList()


    def contextMenuEvent(self, event):

        TileMenu = QMenu(self)
        self.contX = event.x()
        self.contY = event.y()

        TileMenu.addAction('Set tile...', self.setTile)
        TileMenu.addAction('Set item...', self.setItem)

        TileMenu.exec_(event.globalPos())


    def mousePressEvent(self, event):
        if event.button() == 2:
            return

        if PuzzleApplication.instance().window.tileDisplay.selectedIndexes() == []:
            return

        currentSelected = PuzzleApplication.instance().window.tileDisplay.selectedIndexes()

        ix = 0
        iy = 0
        for modelItem in currentSelected:
            # Update yourself!
            centerPoint = self.contentsRect().center()

            tile = modelItem.row()
            upperLeftX = centerPoint.x() - self.size[0]*12
            upperLeftY = centerPoint.y() - self.size[1]*12

            lowerRightX = centerPoint.x() + self.size[0]*12
            lowerRightY = centerPoint.y() + self.size[1]*12


            x = int((event.x() - upperLeftX)/24 + ix)
            y = int((event.y() - upperLeftY)/24 + iy)

            if event.x() < upperLeftX or event.y() < upperLeftY or event.x() > lowerRightX or event.y() > lowerRightY:
                return

            try:
                self.tiles[(y * self.size[0]) + x][2] = PuzzleApplication.instance().tileset().tiles[tile].image
                PuzzleApplication.instance().tileset().objects[self.object].tiles[y][x] = (PuzzleApplication.instance().tileset().objects[self.object].tiles[y][x][0], tile, PuzzleApplication.instance().tileset().slot)
            except IndexError:
                pass

            ix += 1
            if self.size[0]-1 < ix:
                ix = 0
                iy += 1
            if iy > self.size[1]-1:
                break


        self.update()

        self.updateList()


    def updateList(self):
        # Update the list >.>
        object = PuzzleApplication.instance().window.objmodel.itemFromIndex(PuzzleApplication.instance().window.objectList.currentIndex())
        if not object: return


        tex = QPixmap(self.size[0] * 24, self.size[1] * 24)
        tex.fill(Qt.GlobalColor.transparent)
        painter = QPainter(tex)

        Xoffset = 0
        Yoffset = 0

        for tile in self.tiles:
            painter.drawPixmap(tile[0]*24, tile[1]*24, tile[2])

        painter.end()

        object.setIcon(QIcon(tex))

        PuzzleApplication.instance().window.objectList.update()



    def setTile(self):
        dlg = self.setTileDialog()
        if dlg.exec_() == QDialog.Accepted:
            # Do stuff
            centerPoint = self.contentsRect().center()

            upperLeftX = centerPoint.x() - self.size[0]*12
            upperLeftY = centerPoint.y() - self.size[1]*12

            tile = dlg.tile.value()
            tileset = dlg.tileset.currentIndex()

            x = int((self.contX - upperLeftX) / 24)
            y = int((self.contY - upperLeftY) / 24)

            if tileset != PuzzleApplication.instance().tileset().slot:
                tex = QPixmap(self.size[0] * 24, self.size[1] * 24)
                tex.fill(Qt.GlobalColor.transparent)

                self.tiles[(y * self.size[0]) + x][2] = tex

            PuzzleApplication.instance().tileset().objects[self.object].tiles[y][x] = (PuzzleApplication.instance().tileset().objects[self.object].tiles[y][x][0], tile, tileset)

            self.update()
            self.updateList()


    class setTileDialog(QDialog):

        def __init__(self):
            QDialog.__init__(self)

            self.setWindowTitle('Set tiles')

            self.tileset = QComboBox()
            self.tileset.addItems(['Pa0', 'Pa1', 'Pa2', 'Pa3'])

            self.tile = QSpinBox()
            self.tile.setRange(0, 255)

            self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            self.buttons.accepted.connect(self.accept)
            self.buttons.rejected.connect(self.reject)

            self.layout = QGridLayout()
            self.layout.addWidget(QLabel('Tileset:'), 0,0,1,1, Qt.AlignmentFlag.AlignLeft)
            self.layout.addWidget(QLabel('Tile:'), 0,3,1,1, Qt.AlignmentFlag.AlignLeft)
            self.layout.addWidget(self.tileset, 1, 0, 1, 2)
            self.layout.addWidget(self.tile, 1, 3, 1, 3)
            self.layout.addWidget(self.buttons, 2, 3)
            self.setLayout(self.layout)


    def setItem(self):
        centerPoint = self.contentsRect().center()

        upperLeftX = centerPoint.x() - self.size[0]*12
        upperLeftY = centerPoint.y() - self.size[1]*12

        x = int((self.contX - upperLeftX) / 24)
        y = int((self.contY - upperLeftY) / 24)

        obj = PuzzleApplication.instance().tileset().objects[self.object].tiles[y][x]

        dlg = self.setItemDialog(obj[2] >> 2)
        if dlg.exec_() == QDialog.Accepted:
            # Do stuff
            item = dlg.item.currentIndex()

            PuzzleApplication.instance().tileset().objects[self.object].tiles[y][x] = (obj[0], obj[1], (obj[2] & 3) | (item << 2))

            self.update()
            self.updateList()


    class setItemDialog(QDialog):

        def __init__(self, initialIndex=0):
            QDialog.__init__(self)

            self.setWindowTitle('Set item')

            self.item = QComboBox()
            self.item.addItems([
                'Item specified in tile behavior',
                'Fire Flower',
                'Star',
                'Coin',
                'Vine',
                'Spring',
                'Mini Mushroom',
                'Propeller Mushroom',
                'Penguin Suit',
                'Yoshi',
                'Ice Flower',
                'Unknown (11)',
                'Unknown (12)',
                'Unknown (13)',
                'Unknown (14)'])
            self.item.setCurrentIndex(initialIndex)

            self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            self.buttons.accepted.connect(self.accept)
            self.buttons.rejected.connect(self.reject)

            self.layout = QHBoxLayout()
            self.vlayout = QVBoxLayout()
            self.layout.addWidget(QLabel('Item:'))
            self.layout.addWidget(self.item)
            self.vlayout.addLayout(self.layout)
            self.vlayout.addWidget(self.buttons)
            self.setLayout(self.vlayout)



    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)

        centerPoint = self.contentsRect().center()
        upperLeftX = centerPoint.x() - self.size[0]*12
        lowerRightX = centerPoint.x() + self.size[0]*12

        upperLeftY = centerPoint.y() - self.size[1]*12
        lowerRightY = centerPoint.y() + self.size[1]*12


        painter.fillRect(upperLeftX, upperLeftY, self.size[0] * 24, self.size[1]*24, QColor(205, 205, 255))

        for x, y, pix in self.tiles:
            painter.drawPixmap(upperLeftX + (x * 24), upperLeftY + (y * 24), pix)

        if not self.slope == 0:
            pen = QPen()
#            pen.setStyle(Qt.QDashLine)
            pen.setWidth(1)
            pen.setColor(Qt.GlobalColor.blue)
            painter.setPen(QPen(pen))
            painter.drawLine(upperLeftX, upperLeftY + (abs(self.slope) * 24), lowerRightX, upperLeftY + (abs(self.slope) * 24))

            if self.slope > 0:
                main = 'Main'
                sub = 'Sub'
            elif self.slope < 0:
                main = 'Sub'
                sub = 'Main'

            font = painter.font()
            font.setPixelSize(8)
            font.setFamily('Monaco')
            painter.setFont(font)

            painter.drawText(upperLeftX+1, upperLeftY+10, main)
            painter.drawText(upperLeftX+1, upperLeftY + (abs(self.slope) * 24) + 9, sub)

        painter.end()