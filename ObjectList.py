from PyQt6.QtWidgets import QListView
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QPalette

class ObjectList(QListView):

    def __init__(self, parent=None):
        super(ObjectList, self).__init__(parent)
        self.setViewMode(QListView.ViewMode.IconMode)
        self.setIconSize(QSize(96,96))
        self.setGridSize(QSize(114,114))
        self.setMovement(QListView.Movement.Static)
        self.setBackgroundRole(QPalette.ColorRole.BrightText)
        self.setWrapping(False)
        self.setMinimumHeight(140)
        self.setMaximumHeight(140)