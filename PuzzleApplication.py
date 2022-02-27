from PyQt6.QtWidgets import QApplication
from Tileset import TilesetClass

class PuzzleApplication(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.__tileset: TilesetClass = TilesetClass()

    def tileset(self) -> TilesetClass:
        return self.__tileset

    def setTileset(self, tileset: TilesetClass):
        self.__tileset = tileset
