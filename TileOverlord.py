from PyQt6.QtWidgets import QWidget, QPushButton, QComboBox, QLabel, QGridLayout, QMessageBox
from PyQt6.QtGui import QPixmap, QPainter, QStandardItem, QIcon
from PyQt6.QtCore import Qt, pyqtSlot
from PuzzleApplication import PuzzleApplication
from TileWidget import TileWidget
#############################################################################################
############################ Tile widget for drag n'drop Objects ############################


class TileOverlord(QWidget):

    def __init__(self):
        super(TileOverlord, self).__init__()

        # Setup Widgets
        self.tiles = TileWidget()

        self.addObject = QPushButton('Add')
        self.removeObject = QPushButton('Remove')

        self.addRow = QPushButton('+')
        self.removeRow = QPushButton('-')

        self.addColumn = QPushButton('+')
        self.removeColumn = QPushButton('-')

        self.tilingMethod = QComboBox()
        self.tilesetType = QLabel('Pa0')

        self.tilingMethod.addItems(['Repeat',
                                    'Stretch Center',
                                    'Stretch X',
                                    'Stretch Y',
                                    'Repeat Bottom',
                                    'Repeat Top',
                                    'Repeat Left',
                                    'Repeat Right',
                                    'Upward slope',
                                    'Downward slope',
                                    'Downward reverse slope',
                                    'Upward reverse slope'])


        # Connections
        self.addObject.released.connect(self.addObj)
        self.removeObject.released.connect(self.removeObj)
        self.addRow.released.connect(self.tiles.addRow)
        self.removeRow.released.connect(self.tiles.removeRow)
        self.addColumn.released.connect(self.tiles.addColumn)
        self.removeColumn.released.connect(self.tiles.removeColumn)

        self.tilingMethod.activated.connect(self.setTiling)


        # Layout
        layout = QGridLayout()

        layout.addWidget(self.tilesetType, 0, 0, 1, 3)
        layout.addWidget(self.tilingMethod, 0, 3, 1, 3)

        layout.addWidget(self.addObject, 0, 6, 1, 1)
        layout.addWidget(self.removeObject, 0, 7, 1, 1)

        layout.setRowMinimumHeight(1, 40)

        layout.setRowStretch(1, 1)
        layout.setRowStretch(2, 5)
        layout.setRowStretch(5, 5)
        layout.addWidget(self.tiles, 2, 1, 4, 6)

        layout.addWidget(self.addColumn, 3, 7, 1, 1)
        layout.addWidget(self.removeColumn, 4, 7, 1, 1)
        layout.addWidget(self.addRow, 6, 3, 1, 1)
        layout.addWidget(self.removeRow, 6, 4, 1, 1)

        self.setLayout(layout)




    def addObj(self):
        PuzzleApplication.instance().tileset().addObject()

        pix = QPixmap(24, 24)
        pix.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pix)
        painter.drawPixmap(0, 0, PuzzleApplication.instance().tileset().tiles[0].image)
        painter.end()

        count = len(PuzzleApplication.instance().tileset().objects)
        PuzzleApplication.instance().window.objmodel.appendRow(QStandardItem(QIcon(pix), 'Object {0}'.format(count-1)))
        index = PuzzleApplication.instance().window.objectList.currentIndex()
        PuzzleApplication.instance().window.objectList.setCurrentIndex(index)
        self.setObject(index)

        PuzzleApplication.instance().window.objectList.update()
        self.update()


    def removeObj(self):
        if not PuzzleApplication.instance().tileset().objects:
            return

        index = PuzzleApplication.instance().window.objectList.currentIndex()

        if index.row() == -1:
            return

        PuzzleApplication.instance().tileset().removeObject(index.row())
        PuzzleApplication.instance().window.objmodel.removeRow(index.row())

        index = PuzzleApplication.instance().window.objectList.currentIndex()
        if index.row() == -1:
            self.tiles.clear()
        else:
            PuzzleApplication.instance().window.objectList.setCurrentIndex(index)
            self.setObject(index)

        PuzzleApplication.instance().window.objectList.update()
        self.update()


    def setObject(self, index):
        object = PuzzleApplication.instance().tileset().objects[index.row()]

        width = len(object.tiles[0])-1
        height = len(object.tiles)-1
        Xuniform = True
        Yuniform = True
        Xstretch = False
        Ystretch = False

        for tile in object.tiles[0]:
            if tile[0] != object.tiles[0][0][0]:
                Xuniform = False

        for tile in object.tiles:
            if tile[0][0] != object.tiles[0][0][0]:
                Yuniform = False

        if object.tiles[0][0][0] == object.tiles[0][width][0] and Xuniform == False:
            Xstretch = True

        if object.tiles[0][0][0] == object.tiles[height][0][0] and Xuniform == False:
            Ystretch = True



        if object.upperslope[0] != 0:
            if object.upperslope[0] == 0x90:
                self.tilingMethod.setCurrentIndex(8)
            elif object.upperslope[0] == 0x91:
                self.tilingMethod.setCurrentIndex(9)
            elif object.upperslope[0] == 0x92:
                self.tilingMethod.setCurrentIndex(10)
            elif object.upperslope[0] == 0x93:
                self.tilingMethod.setCurrentIndex(11)

        else:
            if Xuniform and Yuniform:
                self.tilingMethod.setCurrentIndex(0)
            elif Xstretch and Ystretch:
                self.tilingMethod.setCurrentIndex(1)
            elif Xstretch:
                self.tilingMethod.setCurrentIndex(2)
            elif Ystretch:
                self.tilingMethod.setCurrentIndex(3)
            elif Xuniform and Yuniform == False and object.tiles[0][0][0] == 0:
                self.tilingMethod.setCurrentIndex(4)
            elif Xuniform and Yuniform == False and object.tiles[height][0][0] == 0:
                self.tilingMethod.setCurrentIndex(5)
            elif Xuniform == False and Yuniform and object.tiles[0][0][0] == 0:
                self.tilingMethod.setCurrentIndex(6)
            elif Xuniform == False and Yuniform and object.tiles[0][width][0] == 0:
                self.tilingMethod.setCurrentIndex(7)


        self.tiles.setObject(object)

#        print 'Object {0}, Width: {1} / Height: {2}, Slope {3}/{4}'.format(index.row(), object.width, object.height, object.upperslope, object.lowerslope)
#        for row in object.tiles:
#            print 'Row: {0}'.format(row)
#        print ''

    @pyqtSlot(int)
    def setTiling(self, listindex):
        index = PuzzleApplication.instance().window.objectList.currentIndex()
        object = PuzzleApplication.instance().tileset().objects[index.row()]


        if listindex == 0: # Repeat
            ctile = 0
            crow = 0

            for row in object.tiles:
                for tile in row:
                    object.tiles[crow][ctile] = (0, tile[1], tile[2])
                    ctile += 1
                crow += 1
                ctile = 0

            object.upperslope = [0, 0]
            object.lowerslope = [0, 0]
            self.tiles.slope = 0
            self.tiles.update()

        if listindex == 1: # Stretch Center

            if object.width < 3 and object.height < 3:
                reply = QMessageBox.information(self, "Warning", "An object must be at least 3 tiles\nwide and 3 tiles tall to apply stretch center.")
                self.setObject(index)
                return

            ctile = 0
            crow = 0

            for row in object.tiles:
                for tile in row:
                    if crow == 0 and ctile == 0:
                        object.tiles[crow][ctile] = (0, tile[1], tile[2])
                    elif crow == 0 and ctile == object.width-1:
                        object.tiles[crow][ctile] = (0, tile[1], tile[2])
                    elif crow == object.height-1 and ctile == object.width-1:
                        object.tiles[crow][ctile] = (0, tile[1], tile[2])
                    elif crow == object.height-1 and ctile == 0:
                        object.tiles[crow][ctile] = (0, tile[1], tile[2])
                    elif crow == 0 or crow == object.height-1:
                        object.tiles[crow][ctile] = (1, tile[1], tile[2])
                    elif ctile == 0 or ctile == object.width-1:
                        object.tiles[crow][ctile] = (2, tile[1], tile[2])
                    else:
                        object.tiles[crow][ctile] = (3, tile[1], tile[2])
                    ctile += 1
                crow += 1
                ctile = 0

            object.upperslope = [0, 0]
            object.lowerslope = [0, 0]
            self.tiles.slope = 0
            self.tiles.update()

        if listindex == 2: # Stretch X

            if object.width < 3:
                reply = QMessageBox.information(self, "Warning", "An object must be at least 3 tiles\nwide to apply stretch X.")
                self.setObject(index)
                return

            ctile = 0
            crow = 0

            for row in object.tiles:
                for tile in row:
                    if ctile == 0:
                        object.tiles[crow][ctile] = (0, tile[1], tile[2])
                    elif ctile == object.width-1:
                        object.tiles[crow][ctile] = (0, tile[1], tile[2])
                    else:
                        object.tiles[crow][ctile] = (1, tile[1], tile[2])
                    ctile += 1
                crow += 1
                ctile = 0

            object.upperslope = [0, 0]
            object.lowerslope = [0, 0]
            self.tiles.slope = 0
            self.tiles.update()

        if listindex == 3: # Stretch Y

            if object.height < 3:
                reply = QMessageBox.information(self, "Warning", "An object must be at least 3 tiles\ntall to apply stretch Y.")
                self.setObject(index)
                return

            ctile = 0
            crow = 0

            for row in object.tiles:
                for tile in row:
                    if crow == 0:
                        object.tiles[crow][ctile] = (0, tile[1], tile[2])
                    elif crow == object.height-1:
                        object.tiles[crow][ctile] = (0, tile[1], tile[2])
                    else:
                        object.tiles[crow][ctile] = (2, tile[1], tile[2])
                    ctile += 1
                crow += 1
                ctile = 0

            object.upperslope = [0, 0]
            object.lowerslope = [0, 0]
            self.tiles.slope = 0
            self.tiles.update()

        if listindex == 4: # Repeat Bottom

            if object.height < 2:
                reply = QMessageBox.information(self, "Warning", "An object must be at least 2 tiles\ntall to apply repeat bottom.")
                self.setObject(index)
                return

            ctile = 0
            crow = 0

            for row in object.tiles:
                for tile in row:
                    if crow == object.height-1:
                        object.tiles[crow][ctile] = (2, tile[1], tile[2])
                    else:
                        object.tiles[crow][ctile] = (0, tile[1], tile[2])
                    ctile += 1
                crow += 1
                ctile = 0

            object.upperslope = [0, 0]
            object.lowerslope = [0, 0]
            self.tiles.slope = 0
            self.tiles.update()

        if listindex == 5: # Repeat Top

            if object.height < 2:
                reply = QMessageBox.information(self, "Warning", "An object must be at least 2 tiles\ntall to apply repeat top.")
                self.setObject(index)
                return

            ctile = 0
            crow = 0

            for row in object.tiles:
                for tile in row:
                    if crow == 0:
                        object.tiles[crow][ctile] = (2, tile[1], tile[2])
                    else:
                        object.tiles[crow][ctile] = (0, tile[1], tile[2])
                    ctile += 1
                crow += 1
                ctile = 0

            object.upperslope = [0, 0]
            object.lowerslope = [0, 0]
            self.tiles.slope = 0
            self.tiles.update()

        if listindex == 6: # Repeat Left

            if object.width < 2:
                reply = QMessageBox.information(self, "Warning", "An object must be at least 2 tiles\nwide to apply repeat left.")
                self.setObject(index)
                return

            ctile = 0
            crow = 0

            for row in object.tiles:
                for tile in row:
                    if ctile == 0:
                        object.tiles[crow][ctile] = (1, tile[1], tile[2])
                    else:
                        object.tiles[crow][ctile] = (0, tile[1], tile[2])
                    ctile += 1
                crow += 1
                ctile = 0

            object.upperslope = [0, 0]
            object.lowerslope = [0, 0]
            self.tiles.slope = 0
            self.tiles.update()

        if listindex == 7: # Repeat Right

            if object.width < 2:
                reply = QMessageBox.information(self, "Warning", "An object must be at least 2 tiles\nwide to apply repeat right.")
                self.setObject(index)
                return

            ctile = 0
            crow = 0

            for row in object.tiles:
                for tile in row:
                    if ctile == object.width-1:
                        object.tiles[crow][ctile] = (1, tile[1], tile[2])
                    else:
                        object.tiles[crow][ctile] = (0, tile[1], tile[2])
                    ctile += 1
                crow += 1
                ctile = 0

            object.upperslope = [0, 0]
            object.lowerslope = [0, 0]
            self.tiles.slope = 0
            self.tiles.update()


        if listindex == 8: # Upward Slope
            ctile = 0
            crow = 0
            for row in object.tiles:
                for tile in row:
                    object.tiles[crow][ctile] = (0, tile[1], tile[2])
                    ctile += 1
                crow += 1
                ctile = 0

            object.upperslope = [0x90, 1]
            object.lowerslope = [0x84, object.height - 1]
            self.tiles.slope = 1
            self.tiles.update()

        if listindex == 9: # Downward Slope
            ctile = 0
            crow = 0
            for row in object.tiles:
                for tile in row:
                    object.tiles[crow][ctile] = (0, tile[1], tile[2])
                    ctile += 1
                crow += 1
                ctile = 0

            object.upperslope = [0x91, 1]
            object.lowerslope = [0x84, object.height - 1]
            self.tiles.slope = 1
            self.tiles.update()

        if listindex == 10: # Upward Reverse Slope
            ctile = 0
            crow = 0
            for row in object.tiles:
                for tile in row:
                    object.tiles[crow][ctile] = (0, tile[1], tile[2])
                    ctile += 1
                crow += 1
                ctile = 0

            object.upperslope = [0x92, object.height - 1]
            object.lowerslope = [0x84, 1]
            self.tiles.slope = 0-(object.height-1)
            self.tiles.update()

        if listindex == 11: # Downward Reverse Slope
            ctile = 0
            crow = 0
            for row in object.tiles:
                for tile in row:
                    object.tiles[crow][ctile] = (0, tile[1], tile[2])
                    ctile += 1
                crow += 1
                ctile = 0

            object.upperslope = [0x93, object.height - 1]
            object.lowerslope = [0x84, 1]
            self.tiles.slope = 0-(object.height-1)
            self.tiles.update()