from PyQt6.QtCore import QAbstractListModel, QModelIndex, Qt, QMimeData, QByteArray, QDataStream, QIODevice
from PyQt6.QtGui import QIcon, QPixmap
#############################################################################################
############################ Subclassed one dimension Item Model ############################


class PiecesModel(QAbstractListModel):
    def __init__(self, parent=None):
        super(PiecesModel, self).__init__(parent)

        self.pixmaps = []

    def supportedDragActions(self):
        super().supportedDragActions()
        return Qt.DropAction.CopyAction | Qt.DropAction.MoveAction | Qt.DropAction.LinkAction

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        if role == Qt.ItemDataRole.DecorationRole:
            return QIcon(self.pixmaps[index.row()])

        if role == Qt.ItemDataRole.UserRole:
            return self.pixmaps[index.row()]

        return None

    def addPieces(self, pixmap):
        row = len(self.pixmaps)

        self.beginInsertRows(QModelIndex(), row, row)
        self.pixmaps.insert(row, pixmap)
        self.endInsertRows()

    def flags(self,index):
        if index.isValid():
            return (Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable |
                    Qt.ItemFlag.ItemIsDragEnabled)

    def clear(self):
        row = len(self.pixmaps)

        del self.pixmaps[:]


    def mimeTypes(self):
        return ['image/x-tile-piece']


    def mimeData(self, indexes):
        mimeData = QMimeData()
        encodedData = QByteArray()

        stream = QDataStream(encodedData, QIODevice.WriteOnly)

        for index in indexes:
            if index.isValid():
                pixmap = QPixmap(self.data(index, Qt.ItemDataRole.UserRole))
                stream << pixmap

        mimeData.setData('image/x-tile-piece', encodedData)
        return mimeData


    def rowCount(self, parent):
        if parent.isValid():
            return 0
        else:
            return len(self.pixmaps)

    def supportedDragActions(self):
        return Qt.DropAction.CopyAction | Qt.DropAction.MoveAction