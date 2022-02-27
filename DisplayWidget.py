from PyQt6.QtWidgets import QListView, QAbstractItemView, \
    QAbstractItemDelegate, QStyle
from PyQt6.QtGui import QPalette, QMouseEvent, QColor, QPolygon, QBrush, \
    QPainter, QPixmap
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QPoint
from os.path import dirname, abspath
from sys import argv

from PuzzleApplication import PuzzleApplication

#############################################################################################
######################## List Widget with custom painter/MouseEvent #########################


class displayWidget(QListView):

    mouseMoved = pyqtSignal(int, int)

    def __init__(self, parent=None, window=None):
        super(displayWidget, self).__init__(parent)

        self.setMinimumWidth(424)
        self.setMaximumWidth(424)
        self.setMinimumHeight(404)
        self.setDragEnabled(True)
        self.setViewMode(QListView.ViewMode.IconMode)
        self.setIconSize(QSize(24,24))
        self.setGridSize(QSize(25,25))
        self.setMovement(QListView.Movement.Static)
        self.setAcceptDrops(False)
        self.setDropIndicatorShown(True)
        self.setResizeMode(QListView.ResizeMode.Adjust)
        self.setUniformItemSizes(True)
        self.setBackgroundRole(QPalette.ColorRole.BrightText)
        self.setMouseTracking(True)
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.setItemDelegate(self.TileItemDelegate(window))


    def mouseMoveEvent(self, event: QMouseEvent):
        QListView.mouseMoveEvent(self, event)
        self.mouseMoved.emit(event.pos().x(), event.pos().y())


    class TileItemDelegate(QAbstractItemDelegate):
        """Handles tiles and their rendering"""

        def __init__(self, window):
            """Initialises the delegate"""
            QAbstractItemDelegate.__init__(self)
            self.__window = window

        def paint(self, painter, option, index):
            """Paints an object"""

            # TODO: get Tileset variable here somehow
            p = index.model().data(index, Qt.ItemDataRole.DecorationRole)
            painter.drawPixmap(option.rect.x(), option.rect.y(), p.pixmap(24,24))

            x = option.rect.x()
            y = option.rect.y()


            # Collision Overlays
            info = self.__window.infoDisplay
            curTile = PuzzleApplication.instance().tileset().tiles[index.row()]

            if info.collisionOverlay.isChecked():
                path = dirname(abspath(argv[0])) + '/Icons/'

                # Sets the colour based on terrain type
                if curTile.byte2 & 16:      # Red
                    colour = QColor(255, 0, 0, 120)
                elif curTile.byte5 == 1:    # Ice
                    colour = QColor(0, 0, 255, 120)
                elif curTile.byte5 == 2:    # Snow
                    colour = QColor(0, 0, 255, 120)
                elif curTile.byte5 == 3:    # Quicksand
                    colour = QColor(128,64,0, 120)
                elif curTile.byte5 == 4:    # Conveyor
                    colour = QColor(128,128,128, 120)
                elif curTile.byte5 == 5:    # Conveyor
                    colour = QColor(128,128,128, 120)
                elif curTile.byte5 == 6:    # Rope
                    colour = QColor(128,0,255, 120)
                elif curTile.byte5 == 7:    # Half Spike
                    colour = QColor(128,0,255, 120)
                elif curTile.byte5 == 8:    # Ledge
                    colour = QColor(128,0,255, 120)
                elif curTile.byte5 == 9:    # Ladder
                    colour = QColor(128,0,255, 120)
                elif curTile.byte5 == 10:    # Staircase
                    colour = QColor(255, 0, 0, 120)
                elif curTile.byte5 == 11:    # Carpet
                    colour = QColor(255, 0, 0, 120)
                elif curTile.byte5 == 12:    # Dust
                    colour = QColor(128,64,0, 120)
                elif curTile.byte5 == 13:    # Grass
                    colour = QColor(0, 255, 0, 120)
                elif curTile.byte5 == 14:    # Unknown
                    colour = QColor(255, 0, 0, 120)
                elif curTile.byte5 == 15:    # Beach Sand
                    colour = QColor(128, 64, 0, 120)
                else:                       # Brown?
                    colour = QColor(64, 30, 0, 120)


                # Sets Brush style for fills
                if curTile.byte2 & 4:        # Climbing Grid
                    style = Qt.BrushStyle.DiagCrossPattern
                elif curTile.byte3 & 16:     # Breakable
                    style = Qt.BrushStyle.VerPattern
                else:
                    style = Qt.BrushStyle.SolidPattern


                brush = QBrush(colour, style)
                painter.setBrush(brush)
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)


                # Paints shape based on other junk
                if curTile.byte3 & 32: # Slope
                    if curTile.byte7 == 0:
                        painter.drawPolygon(QPolygon([QPoint(x, y + 24),
                                                            QPoint(x + 24, y + 24),
                                                            QPoint(x + 24, y)]))
                    elif curTile.byte7 == 1:
                        painter.drawPolygon(QPolygon([QPoint(x, y),
                                                            QPoint(x + 24, y + 24),
                                                            QPoint(x, y + 24)]))
                    elif curTile.byte7 == 2:
                        painter.drawPolygon(QPolygon([QPoint(x, y + 24),
                                                            QPoint(x + 24, y + 24),
                                                            QPoint(x + 24, y + 12)]))
                    elif curTile.byte7 == 3:
                        painter.drawPolygon(QPolygon([QPoint(x, y + 24),
                                                            QPoint(x, y + 12),
                                                            QPoint(x + 24, y),
                                                            QPoint(x + 24, y + 24)]))
                    elif curTile.byte7 == 4:
                        painter.drawPolygon(QPolygon([QPoint(x, y + 24),
                                                            QPoint(x, y),
                                                            QPoint(x + 24, y + 12),
                                                            QPoint(x + 24, y + 24)]))
                    elif curTile.byte7 == 5:
                        painter.drawPolygon(QPolygon([QPoint(x, y + 12),
                                                            QPoint(x + 24, y + 24),
                                                            QPoint(x, y + 24)]))
                    elif curTile.byte7 == 10:
                        painter.drawPolygon(QPolygon([QPoint(x, y),
                                                            QPoint(x, y + 24),
                                                            QPoint(x + 24, y + 24),
                                                            QPoint(x + 24, y)]))
                    elif curTile.byte7 == 11:
                        painter.drawPolygon(QPolygon([QPoint(x, y + 24),
                                                            QPoint(x + 24, y + 18),
                                                            QPoint(x + 24, y + 24)]))
                    elif curTile.byte7 == 12:
                        painter.drawPolygon(QPolygon([QPoint(x + 24, y + 24),
                                                            QPoint(x + 24, y + 12),
                                                            QPoint(x, y + 18),
                                                            QPoint(x, y + 24)]))
                    elif curTile.byte7 == 13:
                        painter.drawPolygon(QPolygon([QPoint(x + 24, y + 24),
                                                            QPoint(x + 24, y + 6),
                                                            QPoint(x, y + 12),
                                                            QPoint(x, y + 24)]))
                    elif curTile.byte7 == 14:
                        painter.drawPolygon(QPolygon([QPoint(x + 24, y + 24),
                                                            QPoint(x + 24, y),
                                                            QPoint(x, y + 6),
                                                            QPoint(x, y + 24)]))
                    elif curTile.byte7 == 15:
                        painter.drawPolygon(QPolygon([QPoint(x + 24, y + 24),
                                                            QPoint(x + 24, y + 6),
                                                            QPoint(x, y),
                                                            QPoint(x, y + 24)]))
                    elif curTile.byte7 == 16:
                        painter.drawPolygon(QPolygon([QPoint(x + 24, y + 24),
                                                            QPoint(x + 24, y + 12),
                                                            QPoint(x, y + 6),
                                                            QPoint(x, y + 24)]))
                    elif curTile.byte7 == 17:
                        painter.drawPolygon(QPolygon([QPoint(x + 24, y + 24),
                                                            QPoint(x + 24, y + 18),
                                                            QPoint(x, y + 12),
                                                            QPoint(x, y + 24)]))
                    elif curTile.byte7 == 18:
                        painter.drawPolygon(QPolygon([QPoint(x + 24, y + 24),
                                                            QPoint(x, y + 18),
                                                            QPoint(x, y + 24)]))

                elif curTile.byte3 & 64: # Reverse Slope
                    if curTile.byte7 == 0:
                        painter.drawPolygon(QPolygon([QPoint(x, y),
                                                            QPoint(x + 24, y + 24),
                                                            QPoint(x + 24, y)]))
                    elif curTile.byte7 == 1:
                        painter.drawPolygon(QPolygon([QPoint(x, y + 24),
                                                            QPoint(x, y),
                                                            QPoint(x + 24, y)]))
                    elif curTile.byte7 == 2:
                        painter.drawPolygon(QPolygon([QPoint(x + 24, y),
                                                            QPoint(x, y),
                                                            QPoint(x + 24, y + 12)]))
                    elif curTile.byte7 == 3:
                        painter.drawPolygon(QPolygon([QPoint(x, y),
                                                            QPoint(x, y + 12),
                                                            QPoint(x + 24, y + 24),
                                                            QPoint(x + 24, y)]))
                    elif curTile.byte7 == 4:
                        painter.drawPolygon(QPolygon([QPoint(x, y + 24),
                                                            QPoint(x, y),
                                                            QPoint(x + 24, y),
                                                            QPoint(x + 24, y + 12)]))
                    elif curTile.byte7 == 5:
                        painter.drawPolygon(QPolygon([QPoint(x, y + 12),
                                                            QPoint(x, y),
                                                            QPoint(x + 24, y)]))
                    elif curTile.byte7 == 10:
                        painter.drawPolygon(QPolygon([QPoint(x, y),
                                                            QPoint(x, y + 24),
                                                            QPoint(x + 24, y + 24),
                                                            QPoint(x + 24, y)]))
                    elif curTile.byte7 == 11:
                        painter.drawPolygon(QPolygon([QPoint(x, y),
                                                            QPoint(x + 24, y),
                                                            QPoint(x + 24, y + 6)]))
                    elif curTile.byte7 == 12:
                        painter.drawPolygon(QPolygon([QPoint(x, y),
                                                            QPoint(x + 24, y),
                                                            QPoint(x + 24, y + 12),
                                                            QPoint(x, y + 6)]))
                    elif curTile.byte7 == 13:
                        painter.drawPolygon(QPolygon([QPoint(x, y),
                                                            QPoint(x + 24, y),
                                                            QPoint(x + 24, y + 18),
                                                            QPoint(x, y + 12)]))
                    elif curTile.byte7 == 14:
                        painter.drawPolygon(QPolygon([QPoint(x, y),
                                                            QPoint(x + 24, y),
                                                            QPoint(x + 24, y + 24),
                                                            QPoint(x, y + 18)]))
                    elif curTile.byte7 == 15:
                        painter.drawPolygon(QPolygon([QPoint(x, y),
                                                            QPoint(x + 24, y),
                                                            QPoint(x + 24, y + 18),
                                                            QPoint(x, y + 24)]))
                    elif curTile.byte7 == 16:
                        painter.drawPolygon(QPolygon([QPoint(x, y),
                                                            QPoint(x + 24, y),
                                                            QPoint(x + 24, y + 12),
                                                            QPoint(x, y + 18)]))
                    elif curTile.byte7 == 17:
                        painter.drawPolygon(QPolygon([QPoint(x, y),
                                                            QPoint(x + 24, y),
                                                            QPoint(x + 24, y + 6),
                                                            QPoint(x, y + 12)]))
                    elif curTile.byte7 == 18:
                        painter.drawPolygon(QPolygon([QPoint(x, y),
                                                            QPoint(x + 24, y),
                                                            QPoint(x, y + 6)]))

                elif curTile.byte2 & 8: # Partial
                    if curTile.byte7 == 1:
                        painter.drawPolygon(QPolygon([QPoint(x, y),
                                                            QPoint(x + 12, y),
                                                            QPoint(x + 12, y + 12),
                                                            QPoint(x, y + 12)]))
                    elif curTile.byte7 == 2:
                        painter.drawPolygon(QPolygon([QPoint(x + 12, y),
                                                            QPoint(x + 24, y),
                                                            QPoint(x + 24, y + 12),
                                                            QPoint(x + 12, y + 12)]))
                    elif curTile.byte7 == 3:
                        painter.drawPolygon(QPolygon([QPoint(x, y),
                                                            QPoint(x + 24, y),
                                                            QPoint(x + 24, y + 12),
                                                            QPoint(x, y + 12)]))
                    elif curTile.byte7 == 4:
                        painter.drawPolygon(QPolygon([QPoint(x, y + 12),
                                                            QPoint(x + 12, y + 12),
                                                            QPoint(x + 12, y + 24),
                                                            QPoint(x, y + 24)]))
                    elif curTile.byte7 == 5:
                        painter.drawPolygon(QPolygon([QPoint(x, y),
                                                            QPoint(x + 12, y),
                                                            QPoint(x + 12, y + 24),
                                                            QPoint(x, y + 24)]))
                    elif curTile.byte7 == 6:
                        painter.drawPolygon(QPolygon([QPoint(x, y + 24),
                                                            QPoint(x + 12, y + 24),
                                                            QPoint(x + 12, y),
                                                            QPoint(x + 24, y),
                                                            QPoint(x + 24, y + 12),
                                                            QPoint(x, y + 12)]))
                    elif curTile.byte7 == 7:
                        painter.drawPolygon(QPolygon([QPoint(x, y),
                                                            QPoint(x + 24, y),
                                                            QPoint(x + 24, y + 12),
                                                            QPoint(x + 12, y + 12),
                                                            QPoint(x + 12, y + 24),
                                                            QPoint(x, y + 24)]))
                    elif curTile.byte7 == 8:
                        painter.drawPolygon(QPolygon([QPoint(x + 12, y + 12),
                                                            QPoint(x + 24, y + 12),
                                                            QPoint(x + 24, y + 24),
                                                            QPoint(x + 12, y + 24)]))
                    elif curTile.byte7 == 9:
                        painter.drawPolygon(QPolygon([QPoint(x + 24, y),
                                                            QPoint(x + 24, y + 12),
                                                            QPoint(x, y + 12),
                                                            QPoint(x, y + 24),
                                                            QPoint(x + 12, y + 24),
                                                            QPoint(x + 12, y)]))
                    elif curTile.byte7 == 10:
                        painter.drawPolygon(QPolygon([QPoint(x + 12, y),
                                                            QPoint(x + 24, y),
                                                            QPoint(x + 24, y + 24),
                                                            QPoint(x + 12, y + 24)]))
                    elif curTile.byte7 == 11:
                        painter.drawPolygon(QPolygon([QPoint(x, y),
                                                            QPoint(x + 24, y),
                                                            QPoint(x + 24, y + 24),
                                                            QPoint(x + 12, y + 24),
                                                            QPoint(x + 12, y + 12),
                                                            QPoint(x, y + 12)]))
                    elif curTile.byte7 == 12:
                        painter.drawPolygon(QPolygon([QPoint(x, y + 12),
                                                            QPoint(x + 24, y + 12),
                                                            QPoint(x + 24, y + 24),
                                                            QPoint(x, y + 24)]))
                    elif curTile.byte7 == 13:
                        painter.drawPolygon(QPolygon([QPoint(x, y),
                                                            QPoint(x + 12, y),
                                                            QPoint(x + 12, y + 12),
                                                            QPoint(x + 24, y + 12),
                                                            QPoint(x + 24, y + 24),
                                                            QPoint(x, y + 24)]))
                    elif curTile.byte7 == 14:
                        painter.drawPolygon(QPolygon([QPoint(x + 24, y + 24),
                                                            QPoint(x + 24, y),
                                                            QPoint(x + 12, y),
                                                            QPoint(x + 12, y + 12),
                                                            QPoint(x, y + 12),
                                                            QPoint(x, y + 24)]))
                    elif curTile.byte7 == 15:
                        painter.drawPolygon(QPolygon([QPoint(x, y),
                                                            QPoint(x + 24, y),
                                                            QPoint(x + 24, y + 24),
                                                            QPoint(x, y + 24)]))

                elif curTile.byte2 & 0x40: # Solid-on-bottom
                    painter.drawPolygon(QPolygon([QPoint(x, y + 24),
                                                        QPoint(x + 24, y + 24),
                                                        QPoint(x + 24, y + 18),
                                                        QPoint(x, y + 18)]))

                    painter.drawPolygon(QPolygon([QPoint(x + 15, y),
                                                        QPoint(x + 15, y + 12),
                                                        QPoint(x + 18, y + 12),
                                                        QPoint(x + 12, y + 17),
                                                        QPoint(x + 6, y + 12),
                                                        QPoint(x + 9, y + 12),
                                                        QPoint(x + 9, y)]))

                elif curTile.byte2 & 0x80: # Solid-on-top
                    painter.drawPolygon(QPolygon([QPoint(x, y),
                                                        QPoint(x + 24, y),
                                                        QPoint(x + 24, y + 6),
                                                        QPoint(x, y + 6)]))

                    painter.drawPolygon(QPolygon([QPoint(x + 15, y + 24),
                                                        QPoint(x + 15, y + 12),
                                                        QPoint(x + 18, y + 12),
                                                        QPoint(x + 12, y + 7),
                                                        QPoint(x + 6, y + 12),
                                                        QPoint(x + 9, y + 12),
                                                        QPoint(x + 9, y + 24)]))

                elif curTile.byte2 & 16: # Spikes
                    if curTile.byte7 == 0:
                        painter.drawPolygon(QPolygon([QPoint(x + 24, y),
                                                            QPoint(x + 24, y + 12),
                                                            QPoint(x, y + 6)]))
                        painter.drawPolygon(QPolygon([QPoint(x + 24, y + 12),
                                                            QPoint(x + 24, y + 24),
                                                            QPoint(x, y + 18)]))
                    if curTile.byte7 == 1:
                        painter.drawPolygon(QPolygon([QPoint(x, y),
                                                            QPoint(x, y + 12),
                                                            QPoint(x + 24, y + 6)]))
                        painter.drawPolygon(QPolygon([QPoint(x, y + 12),
                                                            QPoint(x, y + 24),
                                                            QPoint(x + 24, y + 18)]))
                    if curTile.byte7 == 2:
                        painter.drawPolygon(QPolygon([QPoint(x, y + 24),
                                                            QPoint(x + 12, y + 24),
                                                            QPoint(x + 6, y)]))
                        painter.drawPolygon(QPolygon([QPoint(x + 12, y + 24),
                                                            QPoint(x + 24, y + 24),
                                                            QPoint(x + 18, y)]))
                    if curTile.byte7 == 3:
                        painter.drawPolygon(QPolygon([QPoint(x, y),
                                                            QPoint(x + 12, y),
                                                            QPoint(x + 6, y + 24)]))
                        painter.drawPolygon(QPolygon([QPoint(x + 12, y),
                                                            QPoint(x + 24, y),
                                                            QPoint(x + 18, y + 24)]))
                    if curTile.byte7 == 4:
                        painter.drawPolygon(QPolygon([QPoint(x, y),
                                                            QPoint(x + 24, y),
                                                            QPoint(x + 18, y + 24),
                                                            QPoint(x + 6, y + 24)]))
                    if curTile.byte7 == 5:
                        painter.drawPolygon(QPolygon([QPoint(x + 6, y),
                                                            QPoint(x + 18, y),
                                                            QPoint(x + 12, y + 24)]))
                    if curTile.byte7 == 6:
                        painter.drawPolygon(QPolygon([QPoint(x, y),
                                                            QPoint(x + 24, y),
                                                            QPoint(x + 12, y + 24)]))

                elif curTile.byte3 & 2: # Coin
                    if curTile.byte7 == 0:
                        painter.drawPixmap(option.rect, QPixmap(path + 'Coin/Coin.png'))
                    if curTile.byte7 == 4:
                        painter.drawPixmap(option.rect, QPixmap(path + 'Coin/POW.png'))

                elif curTile.byte3 & 8: # Exploder
                    if curTile.byte7 == 1:
                        painter.drawPixmap(option.rect, QPixmap(path + 'Explode/Stone.png'))
                    if curTile.byte7 == 2:
                        painter.drawPixmap(option.rect, QPixmap(path + 'Explode/Wood.png'))
                    if curTile.byte7 == 3:
                        painter.drawPixmap(option.rect, QPixmap(path + 'Explode/Red.png'))

                elif curTile.byte1 & 2: # Falling
                    painter.drawPixmap(option.rect, QPixmap(path + 'Prop/Fall.png'))

                elif curTile.byte3 & 4: # QBlock
                    if curTile.byte7 == 0:
                        painter.drawPixmap(option.rect, QPixmap(path + 'QBlock/FireF.png'))
                    if curTile.byte7 == 1:
                        painter.drawPixmap(option.rect, QPixmap(path + 'QBlock/Star.png'))
                    if curTile.byte7 == 2:
                        painter.drawPixmap(option.rect, QPixmap(path + 'QBlock/Coin.png'))
                    if curTile.byte7 == 3:
                        painter.drawPixmap(option.rect, QPixmap(path + 'QBlock/Vine.png'))
                    if curTile.byte7 == 4:
                        painter.drawPixmap(option.rect, QPixmap(path + 'QBlock/1up.png'))
                    if curTile.byte7 == 5:
                        painter.drawPixmap(option.rect, QPixmap(path + 'QBlock/Mini.png'))
                    if curTile.byte7 == 6:
                        painter.drawPixmap(option.rect, QPixmap(path + 'QBlock/Prop.png'))
                    if curTile.byte7 == 7:
                        painter.drawPixmap(option.rect, QPixmap(path + 'QBlock/Peng.png'))
                    if curTile.byte7 == 8:
                        painter.drawPixmap(option.rect, QPixmap(path + 'QBlock/IceF.png'))

                elif curTile.byte3 & 1: # Solid
                    painter.drawRect(option.rect)

                else: # No fill
                    pass


            # Highlight stuff.
            colour = option.palette.highlight().color()
            colour.setAlpha(80)

            if option.state & QStyle.StateFlag.State_Selected:
                painter.fillRect(option.rect, colour)


        def sizeHint(self, option, index):
            """Returns the size for the object"""
            return QSize(24,24)