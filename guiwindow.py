
import dill as pickle
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImage, QFont, QPainter
from PyQt5.QtCore import Qt, QTimer
import human # dont delete this import
from gameworld import world, worldcell
import gameworld.worldloader
import global_params
import time
import os
from copy import deepcopy, copy
import json
from ai.groupai.task.taskgroupcreatecaravan import TaskGroupCreateCaravan
from ai.groupai.task.caravan.taskgroupcaravanmove import TaskGroupCaravanMove
from ai.groupai.interaction.interactiongroupbattle import InteractionGroupBattle
from ai.groupai.task.caravan.army.armytypes.armyterritoryannexcampaign import ArmyTerritoryAnnexCampaign
from ai.groupai.task.caravan.army.armytypes.armyannihilatecampaign import ArmyAnnihilateCampaign
import multiprocessing
from entities.group import Group
from entities.groupbase import GroupType
from enum import Enum
from ai.need import NEED_TYPE
import copy
from ai.humanai.relationships.information.informationlocationpeople import InformationLocationPeople



json_save = {'fast':False, "startup_map" : "", "player_output_select_id" : -2, "group_output_select_id" : -2}


class GROUP_OUTPUT_TYPE(Enum):
    DEFAULT = 0
    BUFFER_FACTORS = 1
    INVENTORY = 2
    SOCIAL_HUMAN = 3
    SOCIAL_GROUP = 4
    RESOURCES = 5
    TASKS = 6
    TASKS_DEBUG = 7

class PLAYER_OUTPUT_TYPE(Enum):
    DEFAULT = 0
    SKILLS = 1
    INVENTORY = 2
    SOCIAL_HUMAN = 3
    SOCIAL_GROUP = 4
    TASK = 5


WINDOW_X = 50
WINDOW_Y = 50
WINDOW_HEIGHT = 1000
WINDOW_WIDTH = 1700

WORLD_RENDER_SCALE_WIDTH = 1000
WORLD_RENDER_SCALE_HEIGHT = 1000

TICK_MS = 1
WORLD_INSTANCE = world.World()

# with open("filename_pi.obj",'rb') as file_object:
#     raw_data = file_object.read()
#
# WORLD_INSTANCE = pickle.loads(raw_data)

GLOBAL_CLOCK = 0



class GUIWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initGUI()

        self.playerFocusId = None
        self.run_fast = False
        self.updateGame = False
        self.placeMode = False
        self.changeStockpileMode = False
        self.takeTerritoryMode = False
        self.socialiseGroupsTriggerMode = False
        self.createCaravanMode = False
        self.moveCaravanMode = False
        self.campaignTerritoryAnnexMode = False
        self.campaignAnnihilateMode = False
        self.transferTerritoryMode = False
        self.show_buffer_factors_only = False
        self.show_human_inventory_only = False
        self.specificPlayerDebug = None
        self.groupOutputType = GROUP_OUTPUT_TYPE.DEFAULT
        self.playerOutputType = PLAYER_OUTPUT_TYPE.DEFAULT

        if json_save["startup_map"] == "":
            WORLD_INSTANCE.init_world()
            self.initWorld()

        """
        Timer is the "animation" loop
        """
        self.timer = QTimer(self)
        self.timer.setSingleShot(False)
        self.timer.setInterval(TICK_MS)  # in milliseconds, so 5000 = 5 seconds
        self.timer.timeout.connect(self.update)
        self.timer.start()
        self.toggleTimer()
        self.last_click_position = ()
        self.FPS = 0
        self.updateGroupCombo()
        self.loadJSONSettings()


    def loadJSONSettings(self):
        global json_save
        try:
            # read the data back in
            with open('settings.json', 'r') as fobj:
                json_save = json.load(fobj)

            if json_save["fast"]:
                self.togglePerformance()


        # print(self.groupOutputSelectGroup.checkedId())
        # print(self.groupOutputSelectGroup.button(self.groupOutputSelectGroup.checkedId()).option)

            if json_save["group_output_select_id"]:
                self.groupOutputSelectGroup.button(int(json_save["group_output_select_id"])).setChecked(True)


            if json_save["player_output_select_id"]:
                self.playerOutputSelectGroup.button(int(json_save["player_output_select_id"])).setChecked(True)


            if json_save["startup_map"] != "":
                map_name = json_save["startup_map"]
                self.loadSelectedWorld(map_name)
                self.load_map_on_startup.setChecked(True)
                json_save["startup_map"] = map_name
                self.saveJSONSettings()


            self.updateGroupCombo()
            self.updateTextInfo()
        except:
            # any error means we either dont have file or it is corrupt - reset it
            self.saveJSONSettings()

    def saveJSONSettings(self):
        # serialize the data to user-data.txt
        with open('settings.json', 'w') as fobj:
            json.dump(json_save, fobj)



    def toggleTimer(self):
        if self.updateGame:
            self.updateGame = False
            self.startGame.setEnabled(True)
            self.stopGame.setEnabled(False)

        else:
            self.updateGame = True
            self.startGame.setEnabled(False)
            self.stopGame.setEnabled(True)

    def togglePerformance(self):
        global json_save
        if not self.run_fast:
            self.run_fast = not self.run_fast
            self.lowperformance.setEnabled(True)
            self.highperformance.setEnabled(False)
        else:
            self.run_fast = not self.run_fast
            self.lowperformance.setEnabled(False)
            self.highperformance.setEnabled(True)
        self.updateTextInfo()
        json_save["fast"] = self.run_fast
        self.saveJSONSettings()



    """
    Inialises some GUI 
    """
    def initGUI(self):
        self.setGeometry(WINDOW_X,WINDOW_Y,WINDOW_WIDTH, WINDOW_HEIGHT)
        self.pixmap_label = QLabel()
        self.pixmap_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.pixmap_label.resize(500,500)
        self.pixmap_label.setAlignment(Qt.AlignRight)
        self.pixmap_label.mouseMoveEvent = self.getCoords

        self.setCentralWidget(self.pixmap_label)


        font = QFont()
        font.setPointSize(8)

        self.npcTextBrowser = QTextBrowser(self)
        self.npcTextBrowser.setGeometry(0, 40, 700, 410)

        self.groupTextBrowser = QTextBrowser(self)
        self.groupTextBrowser.setGeometry(0, 490, 700, 410)

        self.npcTextBrowser.setFont(font)
        self.groupTextBrowser.setFont(font)


        # self.toggle_bf = QCheckBox("Show Buffer Factors only", self)
        # self.toggle_bf.setChecked(False)
        # self.toggle_bf.stateChanged.connect(self.toggleBufferFactor)
        # self.toggle_bf.setGeometry(0, 450, 300, 50)

        self.groupOutputSelectGroup = QButtonGroup(self)

        self.groupOutputSelect1 = QRadioButton("Default", self)
        self.groupOutputSelect1.setChecked(True)
        self.groupOutputSelect1.option = GROUP_OUTPUT_TYPE.DEFAULT
        self.groupOutputSelect1.setGeometry(0, 450, 300, 50)
        self.groupOutputSelect1.toggled.connect(self.groupOutputChange)
        self.groupOutputSelectGroup.addButton(self.groupOutputSelect1)

        self.groupOutputSelect2 = QRadioButton("Buffer factors", self)
        self.groupOutputSelect2.option = GROUP_OUTPUT_TYPE.BUFFER_FACTORS
        self.groupOutputSelect2.setGeometry(70, 450, 300, 50)
        self.groupOutputSelect2.toggled.connect(self.groupOutputChange)
        self.groupOutputSelectGroup.addButton(self.groupOutputSelect2)

        self.groupOutputSelect3 = QRadioButton("Inventory", self)
        self.groupOutputSelect3.option = GROUP_OUTPUT_TYPE.INVENTORY
        self.groupOutputSelect3.setGeometry(160, 450, 300, 50)
        self.groupOutputSelect3.toggled.connect(self.groupOutputChange)
        self.groupOutputSelectGroup.addButton(self.groupOutputSelect3)

        self.groupOutputSelect4 = QRadioButton("Social (human)", self)
        self.groupOutputSelect4.option = GROUP_OUTPUT_TYPE.SOCIAL_HUMAN
        self.groupOutputSelect4.setGeometry(240, 450, 300, 50)
        self.groupOutputSelect4.toggled.connect(self.groupOutputChange)
        self.groupOutputSelectGroup.addButton(self.groupOutputSelect4)

        self.groupOutputSelect5 = QRadioButton("Social (group)", self)
        self.groupOutputSelect5.option = GROUP_OUTPUT_TYPE.SOCIAL_GROUP
        self.groupOutputSelect5.setGeometry(340, 450, 300, 50)
        self.groupOutputSelect5.toggled.connect(self.groupOutputChange)
        self.groupOutputSelectGroup.addButton(self.groupOutputSelect5)

        self.groupOutputSelect6 = QRadioButton("Resources", self)
        self.groupOutputSelect6.option = GROUP_OUTPUT_TYPE.RESOURCES
        self.groupOutputSelect6.setGeometry(440, 450, 300, 50)
        self.groupOutputSelect6.toggled.connect(self.groupOutputChange)
        self.groupOutputSelectGroup.addButton(self.groupOutputSelect6)

        self.groupOutputSelect7 = QRadioButton("Tasks", self)
        self.groupOutputSelect7.option = GROUP_OUTPUT_TYPE.TASKS
        self.groupOutputSelect7.setGeometry(520, 450, 300, 50)
        self.groupOutputSelect7.toggled.connect(self.groupOutputChange)
        self.groupOutputSelectGroup.addButton(self.groupOutputSelect7)

        self.groupOutputSelect8 = QRadioButton("Tasks Debug", self)
        self.groupOutputSelect8.option = GROUP_OUTPUT_TYPE.TASKS_DEBUG
        self.groupOutputSelect8.setGeometry(600, 450, 300, 50)
        self.groupOutputSelect8.toggled.connect(self.groupOutputChange)
        self.groupOutputSelectGroup.addButton(self.groupOutputSelect8)


        self.playerOutputSelectGroup = QButtonGroup(self)

        self.playerOutputSelect1 = QRadioButton("Default", self)
        self.playerOutputSelect1.setChecked(True)
        self.playerOutputSelect1.option = PLAYER_OUTPUT_TYPE.DEFAULT
        self.playerOutputSelect1.setGeometry(0, 0, 300, 50)
        self.playerOutputSelect1.toggled.connect(self.playerOutputChange)
        self.playerOutputSelectGroup.addButton(self.playerOutputSelect1)

        self.playerOutputSelect2 = QRadioButton("Skills", self)
        self.playerOutputSelect2.option = PLAYER_OUTPUT_TYPE.SKILLS
        self.playerOutputSelect2.setGeometry(100, 0, 300, 50)
        self.playerOutputSelect2.toggled.connect(self.playerOutputChange)
        self.playerOutputSelectGroup.addButton(self.playerOutputSelect2)

        self.playerOutputSelect3 = QRadioButton("Inventory", self)
        self.playerOutputSelect3.option = PLAYER_OUTPUT_TYPE.INVENTORY
        self.playerOutputSelect3.setGeometry(200, 0, 300, 50)
        self.playerOutputSelect3.toggled.connect(self.playerOutputChange)
        self.playerOutputSelectGroup.addButton(self.playerOutputSelect3)

        self.playerOutputSelect5 = QRadioButton("Social (human)", self)
        self.playerOutputSelect5.option = PLAYER_OUTPUT_TYPE.SOCIAL_HUMAN
        self.playerOutputSelect5.setGeometry(300, 0, 300, 50)
        self.playerOutputSelect5.toggled.connect(self.playerOutputChange)
        self.playerOutputSelectGroup.addButton(self.playerOutputSelect5)


        self.playerOutputSelect6 = QRadioButton("Social (group)", self)
        self.playerOutputSelect6.option = PLAYER_OUTPUT_TYPE.SOCIAL_GROUP
        self.playerOutputSelect6.setGeometry(400, 0, 300, 50)
        self.playerOutputSelect6.toggled.connect(self.playerOutputChange)
        self.playerOutputSelectGroup.addButton(self.playerOutputSelect6)

        self.playerOutputSelect7 = QRadioButton("Tasks", self)
        self.playerOutputSelect7.option = PLAYER_OUTPUT_TYPE.TASK
        self.playerOutputSelect7.setGeometry(500, 0, 300, 50)
        self.playerOutputSelect7.toggled.connect(self.playerOutputChange)
        self.playerOutputSelectGroup.addButton(self.playerOutputSelect7)


        self.rerender_group_territories = QCheckBox("Rerender Group Territories", self)
        self.rerender_group_territories.setChecked(False)
        self.rerender_group_territories.stateChanged.connect(self.toggle_render_group_territories)
        self.rerender_group_territories.setGeometry(550, 660, 300, 50)

        self.rerender_group_territories = QCheckBox("Render Group Territories on top", self)
        self.rerender_group_territories.setChecked(False)
        self.rerender_group_territories.stateChanged.connect(self.toggle_render_group_territories_on_top)
        self.rerender_group_territories.setGeometry(550, 690, 300, 50)


        self.rerender_group_sleeper_locations = QCheckBox("Rerender Group Sleepers", self)
        self.rerender_group_sleeper_locations.setChecked(False)
        self.rerender_group_sleeper_locations.stateChanged.connect(self.toggle_render_group_sleeper_cells)
        self.rerender_group_sleeper_locations.setGeometry(550, 720, 300, 50)


        self.rerender_player_locations = QCheckBox("Rerender player locations", self)
        self.rerender_player_locations.setChecked(True)
        self.rerender_player_locations.stateChanged.connect(self.toggle_rerender_player_locations)
        self.rerender_player_locations.setGeometry(550, 750, 300, 50)


        self.colourSelectGroup = QButtonGroup(self)

        self.colourSelect1 = QRadioButton("Default", self)
        self.colourSelect1.setChecked(True)
        self.colourSelect1.option = worldcell.PersonRenderType.DEFAULT
        self.colourSelect1.setGeometry(550, 780, 300, 50)
        self.colourSelect1.toggled.connect(self.colourSelectChange)
        self.colourSelectGroup.addButton(self.colourSelect1)


        self.colourSelect2 = QRadioButton("Group", self)
        self.colourSelect2.option = worldcell.PersonRenderType.GROUP
        self.colourSelect2.setGeometry(550, 810, 300, 50)
        self.colourSelect2.toggled.connect(self.colourSelectChange)
        self.colourSelectGroup.addButton(self.colourSelect2)


        self.colourSelect3 = QRadioButton("Attribute", self)
        self.colourSelect3.option = worldcell.PersonRenderType.ATTRIBUTE
        self.colourSelect3.setGeometry(550, 840, 300, 50)
        self.colourSelect3.toggled.connect(self.colourSelectChange)
        self.colourSelectGroup.addButton(self.colourSelect3)

        self.colourSelect4 = QRadioButton("State", self)
        self.colourSelect4.option = worldcell.PersonRenderType.STATE
        self.colourSelect4.setGeometry(550, 870, 300, 50)
        self.colourSelect4.toggled.connect(self.colourSelectChange)
        self.colourSelectGroup.addButton(self.colourSelect4)






        self.stopGame = QPushButton('Stop', self)
        self.stopGame.setGeometry(0, 900, 150, 50)
        self.stopGame.setFont(font)
        self.stopGame.clicked.connect(self.toggleTimer)

        self.startGame = QPushButton('Start', self)
        self.startGame.setGeometry(150, 900, 150, 50)
        self.startGame.setFont(font)
        self.startGame.clicked.connect(self.toggleTimer)

        self.highperformance = QPushButton('High Performance', self)
        self.highperformance.setGeometry(300, 900, 150, 50)
        self.highperformance.setFont(font)
        self.highperformance.clicked.connect(self.togglePerformance)


        self.lowperformance = QPushButton('Low Performance', self)
        self.lowperformance.setGeometry(450, 900, 150, 50)
        self.lowperformance.setFont(font)
        self.lowperformance.clicked.connect(self.togglePerformance)

        self.lowperformance.setEnabled(False)
        self.highperformance.setEnabled(True)




        self.viewAllPlayerDebug = QPushButton('View All Player Debug', self)
        self.viewAllPlayerDebug.setGeometry(1500, 700, 200, 50)
        self.viewAllPlayerDebug.setFont(font)
        self.viewAllPlayerDebug.clicked.connect(self.removeSpecificPlayerDebug)

        self.viewPlayerDebug = QPushButton('View Player Debug', self)
        self.viewPlayerDebug.setGeometry(1500, 750, 200, 50)
        self.viewPlayerDebug.setFont(font)
        self.viewPlayerDebug.clicked.connect(self.setSpecificPlayerDebug)


        self.viewWholeMap = QPushButton('View Entire Map', self)
        self.viewWholeMap.setGeometry(1500, 800, 200, 50)
        self.viewWholeMap.setFont(font)
        self.viewWholeMap.clicked.connect(self.removePlayerView)

        self.viewPlayerMap = QPushButton('View Player Map', self)
        self.viewPlayerMap.setGeometry(1500, 850, 200, 50)
        self.viewPlayerMap.setFont(font)
        self.viewPlayerMap.clicked.connect(self.updatePlayerView)

        self.playerSelect = QComboBox(self)
        self.playerSelect.setGeometry(1500, 900, 200, 50)


        self.groupSelect = QComboBox(self)
        self.groupSelect.setGeometry(900, 0, 200, 50)

        self.changeStockpileLocation = QPushButton('Change stockpile location', self)
        self.changeStockpileLocation.setGeometry(1100, 0, 150, 50)
        self.changeStockpileLocation.setFont(font)
        self.changeStockpileLocation.clicked.connect(self.changeStockpileLocationTrigger)

        self.socialiseGroups = QPushButton('Socialise', self)
        self.socialiseGroups.setGeometry(1100, 50, 150, 50)
        self.socialiseGroups.setFont(font)
        self.socialiseGroups.clicked.connect(self.socialiseGroupsTrigger)

        self.transferTerritory = QPushButton('Transfer Territory', self)
        self.transferTerritory.setGeometry(1100, 100, 150, 50)
        self.transferTerritory.setFont(font)
        self.transferTerritory.clicked.connect(self.transferTerritoryTrigger)

        self.takeTerritory = QPushButton('Take territory', self)
        self.takeTerritory.setGeometry(1100, 150, 150, 50)
        self.takeTerritory.setFont(font)
        self.takeTerritory.clicked.connect(self.takeTerritoryTrigger)

        self.takeTerritoryStatsMode = QCheckBox('Stats mode', self)
        self.takeTerritoryStatsMode.setGeometry(1100, 190, 150, 50)
        self.takeTerritoryStatsMode.setChecked(False)

        self.createCaravan = QPushButton('Create Caravan (50%)', self)
        self.createCaravan.setGeometry(1250, 0, 150, 50)
        self.createCaravan.setFont(font)
        self.createCaravan.clicked.connect(self.createCaravanTrigger)

        self.moveCaravan = QPushButton('Move Caravan', self)
        self.moveCaravan.setGeometry(1250, 50, 150, 50)
        self.moveCaravan.setFont(font)
        self.moveCaravan.clicked.connect(self.moveCaravanTrigger)


        self.startCampaignTerritoryAnnex = QPushButton('Campaign Territory Annex', self)
        self.startCampaignTerritoryAnnex.setGeometry(1250, 100, 150, 50)
        self.startCampaignTerritoryAnnex.setFont(font)
        self.startCampaignTerritoryAnnex.clicked.connect(self.startCampaignTerritoryAnnexTrigger)

        self.startCampaignAnnihilate = QPushButton('Campaign Annihilate', self)
        self.startCampaignAnnihilate.setGeometry(1250, 150, 150, 50)
        self.startCampaignAnnihilate.setFont(font)
        self.startCampaignAnnihilate.clicked.connect(self.startCampaignAnnihilateTrigger)




        self.disbandGroup = QPushButton('Disband', self)
        self.disbandGroup.setGeometry(1000, 50, 100, 50)
        self.disbandGroup.setFont(font)
        self.disbandGroup.clicked.connect(self.disband)

        self.refreshGroups = QPushButton('Refresh groups', self)
        self.refreshGroups.setGeometry(900, 50, 100, 50)
        self.refreshGroups.setFont(font)
        self.refreshGroups.clicked.connect(self.refreshGroupCombo)

        self.uniqueGroupColours = QPushButton('Reset Colours', self)
        self.uniqueGroupColours.setGeometry(900, 100, 100, 50)
        self.uniqueGroupColours.setFont(font)
        self.uniqueGroupColours.clicked.connect(self.makeGroupColoursUnique)


        self.saveFileSelect = QComboBox(self)
        self.saveFileSelect.setGeometry(1400, 0, 200, 50)




        self.loadSaveFile = QPushButton('Load', self)
        self.loadSaveFile.setGeometry(1600, 0, 100, 50)
        self.loadSaveFile.setFont(font)
        self.loadSaveFile.clicked.connect(lambda: self.loadSelectedWorld(self.saveFileSelect.currentText()))

        self.load_map_on_startup = QCheckBox("Load on startup", self)
        self.load_map_on_startup.setChecked(False)
        self.load_map_on_startup.stateChanged.connect(self.toggle_load_map_on_startup)
        self.load_map_on_startup.setGeometry(1550, 100, 300, 50)


        self.saveWorldFile = QPushButton('Save', self)
        self.saveWorldFile.setGeometry(1600, 50, 100, 50)
        self.saveWorldFile.setFont(font)
        self.saveWorldFile.clicked.connect(self.saveCurrentWorld)

        self.saveNameInput = QTextEdit(self)
        self.saveNameInput.setText("untitled_world")
        self.saveNameInput.setGeometry(1400, 50, 200, 25)
        self.saveNameInput.setFont(font)

        self.readSaveFiles()

    def removeSpecificPlayerDebug(self):
        self.specificPlayerDebug = None

    def setSpecificPlayerDebug(self):
        self.specificPlayerDebug = int(self.playerSelect.currentText())


    # def toggleBufferFactor(self):
    #     self.show_buffer_factors_only = not self.show_buffer_factors_only
    #     json_save["bf_only"] = self.show_buffer_factors_only
    #     self.saveJSONSettings()

    def toggleInventoryOnly(self):
        self.show_human_inventory_only = not self.show_human_inventory_only
        json_save["inv_only"] = self.show_human_inventory_only
        self.saveJSONSettings()

    def takeTerritoryTrigger(self):
        self.takeTerritoryMode = True
        self.togglePlaceMode()

    def createCaravanTrigger(self):
        self.createCaravanMode = True
        self.togglePlaceMode()

    def moveCaravanTrigger(self):
        self.moveCaravanMode = True
        self.togglePlaceMode()

    def socialiseGroupsTrigger(self):
        self.socialiseGroupsTriggerMode = True
        self.togglePlaceMode()

    def startCampaignTerritoryAnnexTrigger(self):

        self.campaignTerritoryAnnexMode = True
        self.togglePlaceMode()

    def startCampaignAnnihilateTrigger(self):

        self.campaignAnnihilateMode = True
        self.togglePlaceMode()


    def changeStockpileLocationTrigger(self):
        self.changeStockpileMode = True
        self.togglePlaceMode()

    def transferTerritoryTrigger(self):
        self.transferTerritoryMode = True
        self.togglePlaceMode()

    def togglePlaceMode(self):
        self.placeMode = not self.placeMode
        # self.setEnabled(not self.placeMode)
        self.changeStockpileLocation.setEnabled(not self.placeMode)
        self.takeTerritory.setEnabled(not self.placeMode)
        self.socialiseGroups.setEnabled(not self.placeMode)
        self.createCaravan.setEnabled(not self.placeMode)
        self.moveCaravan.setEnabled(not self.placeMode)
        self.startCampaignTerritoryAnnex.setEnabled(not self.placeMode)
        self.startCampaignAnnihilate.setEnabled(not self.placeMode)
        self.transferTerritory.setEnabled(not self.placeMode)

    def disband(self):
        WORLD_INSTANCE.groups[int(self.groupSelect.currentText())].disband_group()


        self.updateGroupCombo()

    def refreshGroupCombo(self):


        self.updateGroupCombo()


    def makeGroupColoursUnique(self):
        counter = 0
        for group in WORLD_INSTANCE.groups.values():
            group.colour = global_params.group_colour_palette[counter]
            counter += 1
        WORLD_INSTANCE.apply_territory_map()
        WORLD_INSTANCE.display = WORLD_INSTANCE.data_to_colour_map(WORLD_INSTANCE.world)



    def updateGroupCombo(self):
        self.groupSelect.clear()
        for group in list(WORLD_INSTANCE.groups.keys()):
            self.groupSelect.addItem(str(group))
        self.groupSelect.update()


    def readSaveFiles(self):
        self.saveFileSelect.clear()
        for file in os.listdir('worldsavefiles'):
            self.saveFileSelect.addItem(file)
        self.saveFileSelect.update()

    def loadSelectedWorld(self, save_name):
        global WORLD_INSTANCE
        file_name = "worldsavefiles\\%s" % save_name
        with open(file_name,'rb') as file_object:
            raw_data = file_object.read()
        WORLD_INSTANCE = pickle.loads(raw_data)
        self.updateGroupCombo()


    def saveCurrentWorld(self):
        file_name = "worldsavefiles\\%s.obj" % self.saveNameInput.toPlainText()
        # with open(file_name,'wb') as file_object:
        #     pickle.dump(self, file_object)

        file_pi = open(file_name, 'wb')
        pickle.dump(WORLD_INSTANCE, file_pi)
        file_pi.close()
        self.readSaveFiles()



    def toggle_load_map_on_startup(self):
        global json_save
        if json_save["startup_map"] != "":
            json_save["startup_map"] = ""
        else:
            json_save["startup_map"] = self.saveFileSelect.currentText()
        self.saveJSONSettings()

    def toggle_render_group_territories(self):
        WORLD_INSTANCE.rerender_group_territories = not WORLD_INSTANCE.rerender_group_territories
        WORLD_INSTANCE.display = WORLD_INSTANCE.data_to_colour_map(WORLD_INSTANCE.world)

    def toggle_render_group_territories_on_top(self):
        WORLD_INSTANCE.rerender_group_territories_on_top = not WORLD_INSTANCE.rerender_group_territories_on_top
        WORLD_INSTANCE.display = WORLD_INSTANCE.data_to_colour_map(WORLD_INSTANCE.world)

    def toggle_rerender_player_locations(self):
        WORLD_INSTANCE.rerender_player_locations = not WORLD_INSTANCE.rerender_player_locations
        WORLD_INSTANCE.display = WORLD_INSTANCE.data_to_colour_map(WORLD_INSTANCE.world)


    def toggle_render_group_sleeper_cells(self):
        WORLD_INSTANCE.rerender_group_sleeper_cells = not WORLD_INSTANCE.rerender_group_sleeper_cells
        WORLD_INSTANCE.display = WORLD_INSTANCE.data_to_colour_map(WORLD_INSTANCE.world)

    def colourSelectChange(self):
        self.colourSelect = self.sender()
        worldcell.Cell.PERSONRENDERTYPE = self.colourSelect.option
        WORLD_INSTANCE.display = WORLD_INSTANCE.data_to_colour_map(WORLD_INSTANCE.world)

    def groupOutputChange(self):
        self.groupOutputSelect = self.sender()
        self.groupOutputType = self.groupOutputSelect.option
        json_save["group_output_select_id"] = self.groupOutputSelectGroup.checkedId()
        self.saveJSONSettings()

    def playerOutputChange(self):
        self.playerOutputSelect = self.sender()
        self.playerOutputType = self.playerOutputSelect.option
        json_save["player_output_select_id"] = self.playerOutputSelectGroup.checkedId()
        self.saveJSONSettings()

    """
    Sets player view variable
    """
    def updatePlayerView(self):
        self.playerFocusId = int(self.playerSelect.currentText())

    """
    Sets player view variable
    """
    def removePlayerView(self):
        self.playerFocusId = None

    """
    Initalsie world here by specifying how many players etc.
    """
    def initWorld(self):

        gameworld.worldloader.spawn_group((89, 88), 15)
        gameworld.worldloader.spawn_group((69, 87), 15)
        # gameworld.worldloader.spawn_group((79, 60), 15)
        # gameworld.worldloader.spawn_group((43, 19), 4)




        for i in range(len( WORLD_INSTANCE.humanDict.values())):
            self.playerSelect.addItem("%s"%i)


    """
    Update function.
    Currently ticks and renders
    """
    def update(self):
        start_time = time.time() # start time of the loop
        global GLOBAL_CLOCK
        GLOBAL_CLOCK += 1
        if self.updateGame:
            WORLD_INSTANCE.tick()

        if self.playerFocusId is None:
            self.setImage(WORLD_INSTANCE.get_display())
        else:
            """
            Currently doesn't draw players
            """
            self.setImage(WORLD_INSTANCE.data_to_colour_map(WORLD_INSTANCE.humanDict[self.playerFocusId].get_personal_map_array()))

        if not self.run_fast and self.updateGame:
            self.updateTextInfo()

        if GLOBAL_CLOCK % global_params.daily_ticks == 0:
            GLOBAL_CLOCK = 0
        try:
            self.FPS = round(1.0 / (time.time() - start_time))
        except:
            self.FPS = 999

    """
    Pass in numpy array will draw it to the big display
    """
    def setImage(self, image):
        self.qimage = QImage(image, image.shape[1], image.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap(self.qimage)
        pixmap = pixmap.scaled(WORLD_RENDER_SCALE_WIDTH, WORLD_RENDER_SCALE_HEIGHT, Qt.KeepAspectRatio)
        font = QFont()
        font.setPointSize(30)
        fontsmall = QFont()
        fontsmall.setPointSize(15)
        painter = QPainter(pixmap)
        painter.setFont(font)
        painter.drawText(10, 50, "%sFPS" % str(self.FPS))
        painter.drawText(10, 100, "%s" % str(self.last_click_position))
        if self.last_click_position is not ():
            if self.last_click_position[0] < 128 and self.last_click_position[1] < 128:
                painter.setFont(fontsmall)
                i = 0
                for line in str(WORLD_INSTANCE.world[self.last_click_position[0]][self.last_click_position[1]]).split("\n"):
                    painter.drawText(10, 130 + i, "%s" % line)
                    i += 25
                painter.setFont(font)
        painter.drawText(10, 350, "Day: %s" % str(WORLD_INSTANCE.time_day))
        painter.drawText(10, 400, "Hour: %s" % str(WORLD_INSTANCE.time_hour))
        painter.drawText(10, 450, "Tick: %s" % str(WORLD_INSTANCE.time_ticks))

        painter.end()
        self.pixmap_label.setPixmap(pixmap)


    def getCoords(self, event):
        x = event.pos().x()
        y = event.pos().y()
        # depending on what kind of value you like (arbitary examples)
        self.last_click_position = (int(y / (WORLD_RENDER_SCALE_HEIGHT / WORLD_INSTANCE.world.shape[0])), int((x - 700) / (WORLD_RENDER_SCALE_WIDTH / WORLD_INSTANCE.world.shape[1])))



        if self.placeMode:

            if self.changeStockpileMode:
                WORLD_INSTANCE.groups[int(self.groupSelect.currentText())].set_stockpile_location(self.last_click_position)
                self.changeStockpileMode = False
            if self.createCaravanMode:
                parent_group = WORLD_INSTANCE.groups[int(self.groupSelect.currentText())]

                caravan_group = Group(self.last_click_position, GroupType.RALLY_POINT, parent_group)
                task = TaskGroupCreateCaravan(parent_group, caravan_group, set(list(parent_group.members)[:len(parent_group.members)//2]))
                parent_group.add_task(task)
                self.createCaravanMode = False
            if  self.campaignTerritoryAnnexMode:
                original_group = WORLD_INSTANCE.groups[int(self.groupSelect.currentText())]
                campaign = ArmyTerritoryAnnexCampaign(original_group, self.last_click_position)
                campaign.begin()
                self.campaignTerritoryAnnexMode = False
            if  self.campaignAnnihilateMode:
                original_group = WORLD_INSTANCE.groups[int(self.groupSelect.currentText())]
                target_group = WORLD_INSTANCE.groups[WORLD_INSTANCE.world[self.last_click_position[0]][self.last_click_position[1]].territory]
                campaign = ArmyAnnihilateCampaign(original_group, target_group)
                campaign.begin()
                self.campaignAnnihilateMode = False
            if self.moveCaravanMode:
                parent_group = WORLD_INSTANCE.groups[int(self.groupSelect.currentText())]
                task = TaskGroupCaravanMove(parent_group, self.last_click_position, move_stockpile=True)
                parent_group.add_task(task)
                self.moveCaravanMode = False
            if self.socialiseGroupsTriggerMode:
                original_group = WORLD_INSTANCE.groups[int(self.groupSelect.currentText())]
                target_group = WORLD_INSTANCE.groups[WORLD_INSTANCE.world[self.last_click_position[0]][self.last_click_position[1]].territory]
                observe_groups(original_group, target_group)
                self.socialiseGroupsTriggerMode = False
            if self.transferTerritoryMode:
                original_group = WORLD_INSTANCE.groups[int(self.groupSelect.currentText())]
                target_group = WORLD_INSTANCE.groups[WORLD_INSTANCE.world[self.last_click_position[0]][self.last_click_position[1]].territory]
                WORLD_INSTANCE.transfer_territories(original_group, target_group)
                original_group.disband_group()
                self.transferTerritoryMode = False
            if self.takeTerritoryMode:
                info = WORLD_INSTANCE.groups[int(self.groupSelect.currentText())].knowledge_group_territory_nodes.take_over_territory(frozenset({self.last_click_position}), list(WORLD_INSTANCE.groups.keys()), self.takeTerritoryStatsMode.isChecked())

                self.takeTerritoryMode = False
                self.msg = QMessageBox()
                output = ""
                for stats in info:
                    output += str(stats)
                    output += "\n\n"
                self.msg.setText(output)
                self.msg.setWindowTitle("Group Territory Takeover Info")
                self.msg.setStandardButtons(QMessageBox.Ok)
                self.retMsg = self.msg.exec_()


            self.togglePlaceMode()
        else:
            if WORLD_INSTANCE.world[self.last_click_position[0]][self.last_click_position[1]].territory is not None:
                self.groupSelect.setCurrentText(str(WORLD_INSTANCE.world[self.last_click_position[0]][self.last_click_position[1]].territory))






    """
    Text box update info
    """
    def updateTextInfo(self):
        self.npcTextBrowser.clear()
        self.groupTextBrowser.clear()
        text = ""
        textgroup = ""
        for idnumber, group in sorted(WORLD_INSTANCE.groups.items()):
            textgroup += "group %s\n" % group.id_number
            if self.groupOutputType == GROUP_OUTPUT_TYPE.DEFAULT:
                textgroup += group.get_debug_info() + "\n"
            elif self.groupOutputType == GROUP_OUTPUT_TYPE.BUFFER_FACTORS:
                textgroup += group.get_buffer_factor_info() + "\n"
            elif self.groupOutputType == GROUP_OUTPUT_TYPE.INVENTORY:
                textgroup += str(group.stockpile_contents) + "\n"
                textgroup += group.knowledge_group_item_inventory.to_string() + "\n"
            elif self.groupOutputType == GROUP_OUTPUT_TYPE.SOCIAL_HUMAN:
                textgroup += group.human_opinions.to_string(3) + "\n"
            elif self.groupOutputType == GROUP_OUTPUT_TYPE.SOCIAL_GROUP:
                textgroup += group.group_opinions.to_string(3) + "\n"
            elif self.groupOutputType == GROUP_OUTPUT_TYPE.RESOURCES:
                textgroup += group.knowledge_cell_locations.to_string() + "\n"
                textgroup += group.knowledge_group_territory_nodes.to_string() + "\n"
            elif self.groupOutputType == GROUP_OUTPUT_TYPE.TASKS:
                textgroup += group.format_task_info() + "\n"
            elif self.groupOutputType == GROUP_OUTPUT_TYPE.TASKS_DEBUG:
                textgroup += group.format_task_info_debug() + "\n"
            textgroup += "\n"


        if self.specificPlayerDebug is None:


            for human in WORLD_INSTANCE.humanDict.values():
                text += "human %s\n" % human.id_number
                if self.playerOutputType == PLAYER_OUTPUT_TYPE.DEFAULT:
                    text += human.get_debug_info() + "\n"
                elif self.playerOutputType == PLAYER_OUTPUT_TYPE.SKILLS:
                    text += str(human.skills) + "\n"
                    text += "knowledge_cells: %s\n" % human.knowledge_cell_locations.to_string()
                elif self.playerOutputType == PLAYER_OUTPUT_TYPE.INVENTORY:
                    text += human.inventory.to_string() + "\n"
                    text += "score: %s \n" % human.needs[NEED_TYPE.TRAIN].current_kit_score
                elif self.playerOutputType == PLAYER_OUTPUT_TYPE.SOCIAL_HUMAN:
                    text += "personality: %s\n" % human.personality.to_string()
                    text += "emotions: %s\n" % human.emotions.to_string()
                    text += "%s" % human.get_current_interaction_to_string()
                    text += human.knowledge_of_people.human_opinions.to_string(3)
                elif self.playerOutputType == PLAYER_OUTPUT_TYPE.SOCIAL_GROUP:
                    text += "group: %s\n" % human.group.id_number
                    text += human.knowledge_groups.group_opinions.to_string(3)
                elif self.playerOutputType == PLAYER_OUTPUT_TYPE.TASK:
                    text += "personality: %s\n" % human.personality.to_string()
                    text += "emotions: %s\n" % human.emotions.to_string()
                    text += "needs: %s\n" % human.needs.values()
                    text += "need_change: %s\n" % human.need_change_debug
                    text += "highest_need: %s\n" % human.current_highest_need
                    text += "current task: %s\n" % human.current_task
                    text += "actions: %s\n" % human.actions
                    text += "current action: %s\n" % human.current_action
                    text += "time on current action: %s\n" % human.time_on_current_action
                text += "\n"

        else:
            text += "human %s\n" % WORLD_INSTANCE.humanDict[self.specificPlayerDebug].id_number
            text += WORLD_INSTANCE.humanDict[self.specificPlayerDebug].get_debug_info() + "\n"




        text += "world\n"
        text += WORLD_INSTANCE.get_debug_info()
        self.npcTextBrowser.setText(text)
        self.groupTextBrowser.setText(textgroup)




"""
FOR DEBUG
Makes two groups aware of each other's members locations.
Helps facitliate intergroup interactions
"""
def observe_groups(group1, group2):
    locations_initators = set([member.location for member in group1.members])
    locations_participants = set([member.location for member in group2.members])

    for member in list(group1.members):
        for location in locations_participants:

            cell = (WORLD_INSTANCE.world[location[0]][location[1]])

            current_people_on_cell_copy = copy.deepcopy(cell.people_on_cell)
            if member.id_number in current_people_on_cell_copy:
                current_people_on_cell_copy.remove(member.id_number)

            InformationLocationPeople(location, current_people_on_cell_copy).register_to_knowledge(member)

    for member in list(group2.members):
        for location in locations_initators:

            cell = (WORLD_INSTANCE.world[location[0]][location[1]])

            current_people_on_cell_copy = copy.deepcopy(cell.people_on_cell)
            if member.id_number in current_people_on_cell_copy:
                current_people_on_cell_copy.remove(member.id_number)

            InformationLocationPeople(location, current_people_on_cell_copy).register_to_knowledge(member)