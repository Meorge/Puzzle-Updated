
from PyQt6.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QHBoxLayout, \
    QRadioButton, QCheckBox, QComboBox, QLabel, QGridLayout
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize

#############################################################################################
######################### Palette for painting behaviours to tiles ##########################


class PaletteWidget(QWidget):

    def __init__(self, window):
        super(PaletteWidget, self).__init__(window)


        # Core Types Radio Buttons and Tooltips
        self.coreType = QGroupBox()
        self.coreType.setTitle('Core Type:')
        self.coreWidgets = []
        coreLayout = QVBoxLayout()
        rowA = QHBoxLayout()
        rowB = QHBoxLayout()
        rowC = QHBoxLayout()
        rowD = QHBoxLayout()
        rowE = QHBoxLayout()
        rowF = QHBoxLayout()

        path = 'Icons/'

        self.coreTypes = [['Default', QIcon(path + 'Core/Default.png'), 'The standard type for tiles.\n\nAny regular terrain or backgrounds\nshould be of generic type. It has no\n collision properties.'],
                     ['Slope', QIcon(path + 'Core/Slope.png'), 'Defines a sloped tile\n\nSloped tiles have sloped collisions,\nwhich Mario can slide on.\n\nNote: Do NOT set slopes to have solid collision.'],
                     ['Reverse Slope', QIcon(path + 'Core/RSlope.png'), 'Defines an upside-down slope.\n\nSloped tiles have sloped collisions,\nwhich Mario can slide on.\n\nNote: Do NOT set slopes to have solid collision.'],
                     ['Partial Block', QIcon(path + 'Partial/Full.png'), 'Used for blocks with partial collisions.\n\nVery useful for Mini-Mario secret\nareas, but also for providing a more\naccurate collision map for your tiles.'],
                     ['Coin', QIcon(path + 'Core/Coin.png'), 'Creates a coin.\n\nCoins have no solid collision,\nand when touched will disappear\nand increment the coin counter.'],
                     ['Explodable Block', QIcon(path + 'Core/Explode.png'), 'Specifies blocks which can explode.\n\nThese blocks will shatter into componenent\npieces when hit by a bom-omb or meteor.\nThe pieces themselves may be hardcoded\nand must be included in the tileset.\nBehaviour may be sporadic.'],
                     ['Climable Grid', QIcon(path + 'Core/Climb.png'), 'Creates terrain that can be climbed on.\n\nClimable terrain cannot be walked on.\nWhen Mario is overtop of a climable\ntile and the player presses up,\nMario will enter a climbing state.'],
                     ['Spike', QIcon(path + 'Core/Spike.png'), 'Dangerous Spikey spikes.\n\nSpike tiles will damage Mario one hit\nwhen they are touched.'],
                     ['Pipe', QIcon(path + 'Core/Pipe.png'), "Denotes a pipe tile.\n\nPipe tiles are specified according to\nthe part of the pipe. It's important\nto specify the right parts or\nentrances will not function correctly."],
                     ['Rails', QIcon(path + 'Core/Rails.png'), 'Used for all types of rails.\n\nPlease note that Pa3_rail.arc is hardcoded\nto replace rails with 3D models.'],
                     ['Conveyor Belt', QIcon(path + 'Core/Conveyor.png'), 'Defines moving tiles.\n\nMoving tiles will move Mario in one\ndirection or another. Parameters are\nlargely unknown at this time.'],
                     ['Question Block', QIcon(path + 'Core/Qblock.png'), 'Creates question blocks.']]

        i = 0
        for item in range(len(self.coreTypes)):
            self.coreWidgets.append(QRadioButton())
            if i == 0:
                self.coreWidgets[item].setText('Default')
            else:
                self.coreWidgets[item].setIcon(self.coreTypes[item][1])
            self.coreWidgets[item].setIconSize(QSize(24, 24))
            self.coreWidgets[item].setToolTip(self.coreTypes[item][2])
            self.coreWidgets[item].clicked.connect(self.swapParams)
            if i < 2:
                rowA.addWidget(self.coreWidgets[item])
            elif i < 4:
                rowB.addWidget(self.coreWidgets[item])
            elif i < 6:
                rowC.addWidget(self.coreWidgets[item])
            elif i < 8:
                rowD.addWidget(self.coreWidgets[item])
            elif i < 10:
                rowE.addWidget(self.coreWidgets[item])
            else:
                rowF.addWidget(self.coreWidgets[item])
            i += 1

        coreLayout.addLayout(rowA)
        coreLayout.addLayout(rowB)
        coreLayout.addLayout(rowC)
        coreLayout.addLayout(rowD)
        coreLayout.addLayout(rowE)
        coreLayout.addLayout(rowF)
        self.coreType.setLayout(coreLayout)


        # Properties Buttons. I hope this works well!
        self.propertyGroup = QGroupBox()
        self.propertyGroup.setTitle('Properties:')
        propertyLayout = QVBoxLayout()
        self.propertyWidgets = []
        propertyList = [['Solid', QIcon(path + 'Prop/Solid.png'), 'Tiles you can walk on.\n\nThe tiles we be a solid basic square\nthrough which Mario can not pass.'],
                        ['Block', QIcon(path + 'Prop/Break.png'), 'This denotes breakable tiles such\nas brick blocks. It is likely that these\nare subject to the same issues as\nexplodable blocks. They emit a coin\nwhen hit.'],
                        ['Falling Block', QIcon(path + 'Prop/Fall.png'), 'Sets the block to fall after a set period. The\nblock is sadly replaced with a donut lift model.'],
                        ['Ledge', QIcon(path + 'Prop/Ledge.png'), 'A ledge tile with unique properties.\n\nLedges can be shimmied along or\nhung from, but not walked along\nas with normal terrain. Must have the\nledge terrain type set as well.'],
                        ['Meltable', QIcon(path + 'Prop/Melt.png'), 'Supposedly allows melting the tile?']]

        for item in range(len(propertyList)):
            self.propertyWidgets.append(QCheckBox(propertyList[item][0]))
            self.propertyWidgets[item].setIcon(propertyList[item][1])
            self.propertyWidgets[item].setIconSize(QSize(24, 24))
            self.propertyWidgets[item].setToolTip(propertyList[item][2])
            propertyLayout.addWidget(self.propertyWidgets[item])


        self.PassThrough = QRadioButton('Pass-Through')
        self.PassDown = QRadioButton('Pass-Down')
        self.PassNone = QRadioButton('No Passing')

        self.PassThrough.setIcon(QIcon(path + 'Prop/Pup.png'))
        self.PassDown.setIcon(QIcon(path + 'Prop/Pdown.png'))
        self.PassNone.setIcon(QIcon(path + 'Prop/Pnone.png'))

        self.PassThrough.setIconSize(QSize(24, 24))
        self.PassDown.setIconSize(QSize(24, 24))
        self.PassNone.setIconSize(QSize(24, 24))

        self.PassThrough.setToolTip('Allows Mario to jump through the bottom\nof the tile and land on the top.')
        self.PassDown.setToolTip("Allows Mario to fall through the tile but\nbe able to jump up through it. Doesn't seem to actually do anything, though?")
        self.PassNone.setToolTip('Default setting')

        propertyLayout.addWidget(self.PassNone)
        propertyLayout.addWidget(self.PassThrough)
        propertyLayout.addWidget(self.PassDown)

        self.propertyGroup.setLayout(propertyLayout)



        # Terrain Type ComboBox
        self.terrainType = QComboBox()
        self.terrainLabel = QLabel('Terrain Type')

        self.terrainTypes = [['Default', QIcon(path + 'Core/Default.png')],
                        ['Ice', QIcon(path + 'Terrain/Ice.png')],
                        ['Snow', QIcon(path + 'Terrain/Snow.png')],
                        ['Quicksand', QIcon(path + 'Terrain/Quicksand.png')],
                        ['Conveyor Belt Right', QIcon(path + 'Core/Conveyor.png')],
                        ['Conveyor Belt Left', QIcon(path + 'Core/Conveyor.png')],
                        ['Horiz. Climbing Rope', QIcon(path + 'Terrain/Rope.png')],
                        ['Anti Wall Jumps', QIcon(path + 'Terrain/Spike.png')],
                        ['Ledge', QIcon(path + 'Terrain/Ledge.png')],
                        ['Ladder', QIcon(path + 'Terrain/Ladder.png')],
                        ['Staircase', QIcon(path + 'Terrain/Stairs.png')],
                        ['Carpet', QIcon(path + 'Terrain/Carpet.png')],
                        ['Dusty', QIcon(path + 'Terrain/Dust.png')],
                        ['Grass', QIcon(path + 'Terrain/Grass.png')],
                        ['Muffled', QIcon(path + 'Unknown.png')],
                        ['Beach Sand', QIcon(path + 'Terrain/Sand.png')]]

        for item in range(len(self.terrainTypes)):
            self.terrainType.addItem(self.terrainTypes[item][1], self.terrainTypes[item][0])
            self.terrainType.setIconSize(QSize(24, 24))
        self.terrainType.setToolTip('Set the various types of terrain.'
                                    '<ul>'
                                    '<li><b>Default:</b><br>'
                                    'Terrain with no particular properties.</li>'
                                    '<li><b>Ice:</b><br>'
                                    'Will be slippery.</li>'
                                    '<li><b>Snow:</b><br>'
                                    'Will emit puffs of snow and snow noises.</li>'
                                    '<li><b>Quicksand:</b><br>'
                                    'Will slowly swallow Mario. Required for creating the quicksand effect.</li>'
                                    '<li><b>Conveyor Belt Right:</b><br>'
                                    'Mario moves rightwards.</li>'
                                    '<li><b>Conveyor Belt Left:</b><br>'
                                    'Mario moves leftwards.</li>'
                                    '<li><b>Horiz. Rope:</b><br>'
                                    'Must be solid to function. Mario will move hand-over-hand along the rope.</li>'
                                    '<li><b>Anti Wall Jumps:</b><br>'
                                    'Mario cannot wall-jump off of the tile.</li>'
                                    '<li><b>Ledge:</b><br>'
                                    'Must have ledge property set as well.</li>'
                                    '<li><b>Ladder:</b><br>'
                                    'Acts as a pole. Mario will face right or left as he climbs.</li>'
                                    '<li><b>Staircase:</b><br>'
                                    'Does not allow Mario to slide.</li>'
                                    '<li><b>Carpet:</b><br>'
                                    'Will muffle footstep noises.</li>'
                                    '<li><b>Dusty:</b><br>'
                                    'Will emit puffs of dust.</li>'
                                    '<li><b>Muffled:</b><br>'
                                    'Mostly muffles footstep noises.</li>'
                                    '<li><b>Grass:</b><br>'
                                    'Will emit grass-like footstep noises.</li>'
                                    '<li><b>Beach Sand:</b><br>'
                                    "Will create sand tufts around Mario's feet.</li>"
                                    '</ul>'
                                   )



        # Parameters ComboBox
        self.parameters = QComboBox()
        self.parameterLabel = QLabel('Parameters')
        self.parameters.addItem('None')


        GenericParams = [['None', QIcon(path + 'Core/Default.png')],
                         ['Beanstalk Stop', QIcon(path + '/Generic/Beanstopper.png')],
                         ['Dash Coin', QIcon(path + 'Generic/Outline.png')],
                         ['Battle Coin', QIcon(path + 'Generic/Outline.png')],
                         ['Red Block Outline A', QIcon(path + 'Generic/RedBlock.png')],
                         ['Red Block Outline B', QIcon(path + 'Generic/RedBlock.png')],
                         ['Cave Entrance Right', QIcon(path + 'Generic/Cave-Right.png')],
                         ['Cave Entrance Left', QIcon(path + 'Generic/Cave-Left.png')],
                         ['Unknown', QIcon(path + 'Unknown.png')],
                         ['Layer 0 Pit', QIcon(path + 'Unknown.png')]]

        RailParams = [['None', QIcon(path + 'Core/Default.png')],
                      ['Rail: Upslope', QIcon(path + '')],
                      ['Rail: Downslope', QIcon(path + '')],
                      ['Rail: 90 degree Corner Fill', QIcon(path + '')],
                      ['Rail: 90 degree Corner', QIcon(path + '')],
                      ['Rail: Horizontal Rail', QIcon(path + '')],
                      ['Rail: Vertical Rail', QIcon(path + '')],
                      ['Rail: Unknown', QIcon(path + 'Unknown.png')],
                      ['Rail: Gentle Upslope 2', QIcon(path + '')],
                      ['Rail: Gentle Upslope 1', QIcon(path + '')],
                      ['Rail: Gentle Downslope 2', QIcon(path + '')],
                      ['Rail: Gentle Downslope 1', QIcon(path + '')],
                      ['Rail: Steep Upslope 2', QIcon(path + '')],
                      ['Rail: Steep Upslope 1', QIcon(path + '')],
                      ['Rail: Steep Downslope 2', QIcon(path + '')],
                      ['Rail: Steep Downslope 1', QIcon(path + '')],
                      ['Rail: One Panel Circle', QIcon(path + '')],
                      ['Rail: 2x2 Circle Upper Right', QIcon(path + '')],
                      ['Rail: 2x2 Circle Upper Left', QIcon(path + '')],
                      ['Rail: 2x2 Circle Lower Right', QIcon(path + '')],
                      ['Rail: 2x2 Circle Lower Left', QIcon(path + '')],
                      ['Rail: 4x4 Circle Top Left Corner', QIcon(path + '')],
                      ['Rail: 4x4 Circle Top Left', QIcon(path + '')],
                      ['Rail: 4x4 Circle Top Right', QIcon(path + '')],
                      ['Rail: 4x4 Circle Top Right Corner', QIcon(path + '')],
                      ['Rail: 4x4 Circle Upper Left Side', QIcon(path + '')],
                      ['Rail: 4x4 Circle Upper Right Side', QIcon(path + '')],
                      ['Rail: 4x4 Circle Lower Left Side', QIcon(path + '')],
                      ['Rail: 4x4 Circle Lower Right Side', QIcon(path + '')],
                      ['Rail: 4x4 Circle Bottom Left Corner', QIcon(path + '')],
                      ['Rail: 4x4 Circle Bottom Left', QIcon(path + '')],
                      ['Rail: 4x4 Circle Bottom Right', QIcon(path + '')],
                      ['Rail: 4x4 Circle Bottom Right Corner', QIcon(path + '')],
                      ['Rail: Unknown', QIcon(path + 'Unknown.png')],
                      ['Rail: End Stop', QIcon(path + '')]]

        ClimableGridParams = [['None', QIcon(path + 'Core/Default.png')],
                             ['Free Move', QIcon(path + 'Climb/Center.png')],
                             ['Upper Left Corner', QIcon(path + 'Climb/UpperLeft.png')],
                             ['Top', QIcon(path + 'Climb/Top.png')],
                             ['Upper Right Corner', QIcon(path + 'Climb/UpperRight.png')],
                             ['Left Side', QIcon(path + 'Climb/Left.png')],
                             ['Center', QIcon(path + 'Climb/Center.png')],
                             ['Right Side', QIcon(path + 'Climb/Right.png')],
                             ['Lower Left Corner', QIcon(path + 'Climb/LowerLeft.png')],
                             ['Bottom', QIcon(path + 'Climb/Bottom.png')],
                             ['Lower Right Corner', QIcon(path + 'Climb/LowerRight.png')]]


        CoinParams = [['Generic Coin', QIcon(path + 'QBlock/Coin.png')],
                     ['Coin', QIcon(path + 'Unknown.png')],
                     ['Nothing', QIcon(path + 'Unknown.png')],
                     ['Coin', QIcon(path + 'Unknown.png')],
                     ['Pow Block Coin', QIcon(path + 'Coin/POW.png')]]

        ExplodableBlockParams = [['None', QIcon(path + 'Core/Default.png')],
                                ['Stone Block', QIcon(path + 'Explode/Stone.png')],
                                ['Wooden Block', QIcon(path + 'Explode/Wooden.png')],
                                ['Red Block', QIcon(path + 'Explode/Red.png')],
                                ['Unknown', QIcon(path + 'Unknown.png')],
                                ['Unknown', QIcon(path + 'Unknown.png')],
                                ['Unknown', QIcon(path + 'Unknown.png')]]

        PipeParams = [['Vert. Top Entrance Left', QIcon(path + 'Pipes/')],
                      ['Vert. Top Entrance Right', QIcon(path + '')],
                      ['Vert. Bottom Entrance Left', QIcon(path + '')],
                      ['Vert. Bottom Entrance Right', QIcon(path + '')],
                      ['Vert. Center Left', QIcon(path + '')],
                      ['Vert. Center Right', QIcon(path + '')],
                      ['Vert. On Top Junction Left', QIcon(path + '')],
                      ['Vert. On Top Junction Right', QIcon(path + '')],
                      ['Horiz. Left Entrance Top', QIcon(path + '')],
                      ['Horiz. Left Entrance Bottom', QIcon(path + '')],
                      ['Horiz. Right Entrance Top', QIcon(path + '')],
                      ['Horiz. Right Entrance Bottom', QIcon(path + '')],
                      ['Horiz. Center Top', QIcon(path + '')],
                      ['Horiz. Center Bottom', QIcon(path + '')],
                      ['Horiz. On Top Junction Top', QIcon(path + '')],
                      ['Horiz. On Top Junction Bottom', QIcon(path + '')],
                      ['Vert. Mini Pipe Top', QIcon(path + '')],
                      ['Unknown', QIcon(path + 'Unknown.png')],
                      ['Vert. Mini Pipe Bottom', QIcon(path + '')],
                      ['Unknown', QIcon(path + 'Unknown.png')],
                      ['Unknown', QIcon(path + 'Unknown.png')],
                      ['Unknown', QIcon(path + 'Unknown.png')],
                      ['Vert. On Top Mini-Junction', QIcon(path + '')],
                      ['Unknown', QIcon(path + 'Unknown.png')],
                      ['Horiz. Mini Pipe Left', QIcon(path + '')],
                      ['Unknown', QIcon(path + 'Unknown.png')],
                      ['Horiz. Mini Pipe Right', QIcon(path + '')],
                      ['Unknown', QIcon(path + 'Unknown.png')],
                      ['Vert. Mini Pipe Center', QIcon(path + '')],
                      ['Horiz. Mini Pipe Center', QIcon(path + '')],
                      ['Horiz. On Top Mini-Junction', QIcon(path + '')],
                      ['Block Covered Corner', QIcon(path + '')]]

        PartialBlockParams = [['None', QIcon(path + 'Core/Default.png')],
                              ['Upper Left', QIcon(path + 'Partial/UpLeft.png')],
                              ['Upper Right', QIcon(path + 'Partial/UpRight.png')],
                              ['Top Half', QIcon(path + 'Partial/TopHalf.png')],
                              ['Lower Left', QIcon(path + 'Partial/LowLeft.png')],
                              ['Left Half', QIcon(path + 'Partial/LeftHalf.png')],
                              ['Diagonal Downwards', QIcon(path + 'Partial/DiagDn.png')],
                              ['Upper Left 3/4', QIcon(path + 'Partial/UpLeft3-4.png')],
                              ['Lower Right', QIcon(path + 'Partial/LowRight.png')],
                              ['Diagonal Downwards', QIcon(path + 'Partial/DiagDn.png')],
                              ['Right Half', QIcon(path + 'Partial/RightHalf.png')],
                              ['Upper Right 3/4', QIcon(path + 'Partial/UpRig3-4.png')],
                              ['Lower Half', QIcon(path + 'Partial/LowHalf.png')],
                              ['Lower Left 3/4', QIcon(path + 'Partial/LowLeft3-4.png')],
                              ['Lower Right 3/4', QIcon(path + 'Partial/LowRight3-4.png')],
                              ['Full Brick', QIcon(path + 'Partial/Full.png')]]

        SlopeParams = [['Steep Upslope', QIcon(path + 'Slope/steepslopeleft.png')],
                       ['Steep Downslope', QIcon(path + 'Slope/steepsloperight.png')],
                       ['Upslope 1', QIcon(path + 'Slope/slopeleft.png')],
                       ['Upslope 2', QIcon(path + 'Slope/slope3left.png')],
                       ['Downslope 1', QIcon(path + 'Slope/slope3right.png')],
                       ['Downslope 2', QIcon(path + 'Slope/sloperight.png')],
                       ['Steep Upslope 1', QIcon(path + 'Slope/vsteepup1.png')],
                       ['Steep Upslope 2', QIcon(path + 'Slope/vsteepup2.png')],
                       ['Steep Downslope 1', QIcon(path + 'Slope/vsteepdown1.png')],
                       ['Steep Downslope 2', QIcon(path + 'Slope/vsteepdown2.png')],
                       ['Slope Edge (solid)', QIcon(path + 'Slope/edge.png')],
                       ['Gentle Upslope 1', QIcon(path + 'Slope/gentleupslope1.png')],
                       ['Gentle Upslope 2', QIcon(path + 'Slope/gentleupslope2.png')],
                       ['Gentle Upslope 3', QIcon(path + 'Slope/gentleupslope3.png')],
                       ['Gentle Upslope 4', QIcon(path + 'Slope/gentleupslope4.png')],
                       ['Gentle Downslope 1', QIcon(path + 'Slope/gentledownslope1.png')],
                       ['Gentle Downslope 2', QIcon(path + 'Slope/gentledownslope2.png')],
                       ['Gentle Downslope 3', QIcon(path + 'Slope/gentledownslope3.png')],
                       ['Gentle Downslope 4', QIcon(path + 'Slope/gentledownslope4.png')]]

        ReverseSlopeParams = [['Steep Downslope', QIcon(path + 'Slope/Rsteepslopeleft.png')],
                              ['Steep Upslope', QIcon(path + 'Slope/Rsteepsloperight.png')],
                              ['Downslope 1', QIcon(path + 'Slope/Rslopeleft.png')],
                              ['Downslope 2', QIcon(path + 'Slope/Rslope3left.png')],
                              ['Upslope 1', QIcon(path + 'Slope/Rslope3right.png')],
                              ['Upslope 2', QIcon(path + 'Slope/Rsloperight.png')],
                              ['Steep Downslope 1', QIcon(path + 'Slope/Rvsteepdown1.png')],
                              ['Steep Downslope 2', QIcon(path + 'Slope/Rvsteepdown2.png')],
                              ['Steep Upslope 1', QIcon(path + 'Slope/Rvsteepup1.png')],
                              ['Steep Upslope 2', QIcon(path + 'Slope/Rvsteepup2.png')],
                              ['Slope Edge (solid)', QIcon(path + 'Slope/edge.png')],
                              ['Gentle Downslope 1', QIcon(path + 'Slope/Rgentledownslope1.png')],
                              ['Gentle Downslope 2', QIcon(path + 'Slope/Rgentledownslope2.png')],
                              ['Gentle Downslope 3', QIcon(path + 'Slope/Rgentledownslope3.png')],
                              ['Gentle Downslope 4', QIcon(path + 'Slope/Rgentledownslope4.png')],
                              ['Gentle Upslope 1', QIcon(path + 'Slope/Rgentleupslope1.png')],
                              ['Gentle Upslope 2', QIcon(path + 'Slope/Rgentleupslope2.png')],
                              ['Gentle Upslope 3', QIcon(path + 'Slope/Rgentleupslope3.png')],
                              ['Gentle Upslope 4', QIcon(path + 'Slope/Rgentleupslope4.png')]]

        SpikeParams = [['Double Left Spikes', QIcon(path + 'Spike/Left.png')],
                       ['Double Right Spikes', QIcon(path + 'Spike/Right.png')],
                       ['Double Upwards Spikes', QIcon(path + 'Spike/Up.png')],
                       ['Double Downwards Spikes', QIcon(path + 'Spike/Down.png')],
                       ['Long Spike Down 1', QIcon(path + 'Spike/LongDown1.png')],
                       ['Long Spike Down 2', QIcon(path + 'Spike/LongDown2.png')],
                       ['Single Downwards Spike', QIcon(path + 'Spike/SingDown.png')],
                       ['Spike Block', QIcon(path + 'Unknown.png')]]

        ConveyorBeltParams = [['Slow', QIcon(path + 'Unknown.png')],
                              ['Fast', QIcon(path + 'Unknown.png')]]

        QBlockParams = [['Fire Flower', QIcon(path + 'Qblock/Fire.png')],
                       ['Star', QIcon(path + 'Qblock/Star.png')],
                       ['Coin', QIcon(path + 'Qblock/Coin.png')],
                       ['Vine', QIcon(path + 'Qblock/Vine.png')],
                       ['1-Up', QIcon(path + 'Qblock/1up.png')],
                       ['Mini Mushroom', QIcon(path + 'Qblock/Mini.png')],
                       ['Propeller Suit', QIcon(path + 'Qblock/Prop.png')],
                       ['Penguin Suit', QIcon(path + 'Qblock/Peng.png')],
                       ['Ice Flower', QIcon(path + 'Qblock/IceF.png')]]


        self.ParameterList = [GenericParams,
                              SlopeParams,
                              ReverseSlopeParams,
                              PartialBlockParams,
                              CoinParams,
                              ExplodableBlockParams,
                              ClimableGridParams,
                              SpikeParams,
                              PipeParams,
                              RailParams,
                              ConveyorBeltParams,
                              QBlockParams]


        layout = QGridLayout()
        layout.addWidget(self.coreType, 0, 1)
        layout.addWidget(self.propertyGroup, 0, 0, 3, 1)
        layout.addWidget(self.terrainType, 2, 1)
        layout.addWidget(self.parameters, 1, 1)
        self.setLayout(layout)


    def swapParams(self):
        for item in range(12):
            if self.coreWidgets[item].isChecked():
                self.parameters.clear()
                for option in self.ParameterList[item]:
                    self.parameters.addItem(option[1], option[0])