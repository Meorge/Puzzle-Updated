from PyQt6.QtWidgets import QWidget, QGridLayout, QFormLayout, QGroupBox, \
    QHBoxLayout, QLabel, QCheckBox, QVBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QRect

#############################################################################################
######################### InfoBox Custom Widget to display info to ##########################


class InfoBoxWidget(QWidget):
    def __init__(self, window):
        super(InfoBoxWidget, self).__init__(window)

        # InfoBox
        superLayout = QGridLayout()
        infoLayout = QFormLayout()

        self.imageBox = QGroupBox()
        imageLayout = QHBoxLayout()

        pix = QPixmap(24, 24)
        pix.fill(Qt.GlobalColor.transparent)

        self.coreImage = QLabel()
        self.coreImage.setPixmap(pix)
        self.terrainImage = QLabel()
        self.terrainImage.setPixmap(pix)
        self.parameterImage = QLabel()
        self.parameterImage.setPixmap(pix)


        def updateAllTiles():
            for i in range(256):
                window.tileDisplay.update(window.tileDisplay.model().index(i, 0))
        self.collisionOverlay = QCheckBox('Overlay Collision')
        self.collisionOverlay.clicked.connect(updateAllTiles)


        self.coreInfo = QLabel()
        self.propertyInfo = QLabel('             \n\n\n\n\n')
        self.terrainInfo = QLabel()
        self.paramInfo = QLabel()

        Font = self.font()
        Font.setPointSize(9)

        self.coreInfo.setFont(Font)
        self.propertyInfo.setFont(Font)
        self.terrainInfo.setFont(Font)
        self.paramInfo.setFont(Font)


        self.LabelB = QLabel('Properties:')
        self.LabelB.setFont(Font)

        self.hexdata = QLabel('Hex Data: 0x00 0x00 0x00 0x00\n                0x00 0x00 0x00 0x00')
        self.hexdata.setFont(Font)


        coreLayout = QVBoxLayout()
        terrLayout = QVBoxLayout()
        paramLayout = QVBoxLayout()

        coreLayout.setGeometry(QRect(0,0,40,40))
        terrLayout.setGeometry(QRect(0,0,40,40))
        paramLayout.setGeometry(QRect(0,0,40,40))


        label = QLabel('Core')
        label.setFont(Font)
        coreLayout.addWidget(label, 0, Qt.AlignmentFlag.AlignCenter)

        label = QLabel('Terrain')
        label.setFont(Font)
        terrLayout.addWidget(label, 0, Qt.AlignmentFlag.AlignCenter)

        label = QLabel('Parameters')
        label.setFont(Font)
        paramLayout.addWidget(label, 0, Qt.AlignmentFlag.AlignCenter)

        coreLayout.addWidget(self.coreImage, 0, Qt.AlignmentFlag.AlignCenter)
        terrLayout.addWidget(self.terrainImage, 0, Qt.AlignmentFlag.AlignCenter)
        paramLayout.addWidget(self.parameterImage, 0, Qt.AlignmentFlag.AlignCenter)

        coreLayout.addWidget(self.coreInfo, 0, Qt.AlignmentFlag.AlignCenter)
        terrLayout.addWidget(self.terrainInfo, 0, Qt.AlignmentFlag.AlignCenter)
        paramLayout.addWidget(self.paramInfo, 0, Qt.AlignmentFlag.AlignCenter)

        imageLayout.setContentsMargins(0,4,4,4)
        imageLayout.addLayout(coreLayout)
        imageLayout.addLayout(terrLayout)
        imageLayout.addLayout(paramLayout)

        self.imageBox.setLayout(imageLayout)


        superLayout.addWidget(self.imageBox, 0, 0)
        superLayout.addWidget(self.collisionOverlay, 1, 0)
        infoLayout.addRow(self.LabelB, self.propertyInfo)
        infoLayout.addRow(self.hexdata)
        superLayout.addLayout(infoLayout, 0, 1, 2, 1)
        self.setLayout(superLayout)