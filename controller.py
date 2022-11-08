import gui
import analysisModel
import differentialModel
import navigationModel
import os
import utilities
import copy
import settings
from threading import Thread

class controller:

    def __init__(self):
        #Stores previously clicked filename (navigation box)
        self.prevClick = ""
        #Stores previous screen
        self.prevScreen = ""
        #Stores previously clicked widget
        self.prevItem = ""
        #Stores currently clicked widget
        self.item = ""

        #Path to this file
        self.realPath = str(os.path.realpath(__file__))[:-14]

        #Will either be "ANALYZE" "DIFFERENTIAL" or "BOTH"
        self.currentOperation = ""

        self.myAnalysis = analysisModel.analysisModel(self.realPath)
        self.myDifferential = differentialModel.differentialModel(self.realPath)
        self.myNavigation = navigationModel.navigationModel(self.realPath)

        gui.beginGUI(self)

    def notifyController(self, item):
        self.item = item
        #SCREEN CHANGING
        if (
            item == "homeBtn" or item == "texture_tag2" or item == "localScanBtn" or item == "repoScanBtn" 
            or item == "buildScanBtn" or item =="analysisOperationBtn" or item =="differentialOperationBtn"
            or item == "currentAsSave" or item == "baseAsSave" or item == "currentAsLocal" or item == "loadSettingsBtn" or item == "backBtn"
            ):
            screenMap = {
                "homeBtn": "mainScreen",

                "analysisOperationBtn": "analysisOperationScreen",
                "differentialOperationBtn": "differentialOperationScreen",

                "texture_tag2": "settingsScreen",

                "localScanBtn": "localScanScreen",
                "repoScanBtn": "repoScanScreen",
                "buildScanBtn": "buildScanScreen",

                "baseAsSave": "savedScanScreen",
                "currentAsSave": "savedScanScreen",
                "loadSettingsBtn": "savedScanScreen",

                "currentAsLocal": "localSelectScreen",
                "backBtn": self.prevScreen
            }
            if item == "backBtn":
                if self.prevItem == "loadSettingsBtn":
                    self.loadSettings()
                    screenMap["backBtn"] = "settingsScreen"
                elif gui.getCurrentScreen() == "localScanScreen" or gui.getCurrentScreen() == "repoScanScreen" or gui.getCurrentScreen() == "buildScanScreen":
                    screenMap["backBtn"] = "analysisOperationScreen"

            self.switchScreens(gui.getCurrentScreen(), screenMap[item])

        #Cancel from progress screen
        elif item == "cancelBtn" or item == "yesBtn" or item =="noBtn":
            if(item == "cancelBtn" and self.isFinishedProcessing()):
                self.switchScreens(gui.getCurrentScreen(), "mainScreen")
            else:
                gui.toggleShow("yesBtn")
                gui.toggleShow("noBtn")
                gui.toggleShow("cancelLabel")
                gui.toggleShow("cancelBtn")
                if item == "yesBtn":
                    self.switchScreens(gui.getCurrentScreen(), "mainScreen")

        #ADD BUTTONS
        elif (
            item == "addBtn" or item == "addBtn2" or item == "addBtn3"
            or item == "includeAddBtn" or item =="excludeAddBtn"
            or item == "selectLocalBtn"
            ):
            self.addButtonCallback(item)

        #NAVBOX CLICKS
        elif (
            item == "navbox" or item == "navbox2" or item == "navbox3"
            or item == "navboxSettings" or item == "localNavbox"
            ):
            self.navCallback(item)

        #ANALYZE BUTTON
        elif item == "analyzeBtn" or item == "analyzeBtn2" or item == "analyzeBtn3":
            self.currentOperation = "ANALYZE"
            self.analyzeBtnCallback()

        #CLEAR SELECTION BUTTONS
        elif item == "clearSelectionBtn" or item == "clearSelectionBtn2" or item == "clearSelectionBtn3" or item == "clearLocalBox":
            self.resetSelection()

        elif item == "clearIncludesBtn":
            self.myAnalysis.setTempSettings("includes", [])
            gui.configureItem("includeSelection", "items", [])

        elif item == "savedScans":
            gui.bindItemTheme("savedScans", "navboxActive")
            gui.configureItem("selectScanBtn", "show", True)

        elif item == "clearExcludesBtn":
            self.myAnalysis.setTempSettings("excludes", [])
            gui.configureItem("excludeSelection", "items", [])

        #SAVING SETTINGS
        elif item == "saveSettingsBtn":
            self.updateTempSettings()
            self.myAnalysis.saveTempSettings()

        #CLEAR CACHE
        elif item == "clearCacheBtn":
            self.myAnalysis.clearCache()
        
        #Clear Logs
        elif item == "clearLogBtn":
            os.system("rm -rf " +self.realPath+"/logs")
            os.mkdir(self.realPath+"/logs")

        #Handles clicking the "select" or "Confirm" buttons from the selector screens
        elif item == "selectScanBtn" or item == "confirmLocalBox":
            nextScreen = self.prevScreen
            if self.prevItem == "loadSettingsBtn":
                self.myAnalysis.tempSettings.loadSettingsFromXML(self.realPath + "/../SavedScans/" + gui.getItemValue("savedScans"))
                self.loadSettings()
                nextScreen = "settingsScreen"

            elif self.prevItem == "baseAsSave":
                self.myDifferential.setBaseFile(self.realPath + "/../SavedScans/" + gui.getItemValue("savedScans"))
                gui.configureItem("baseTag", "label", "Base: " + gui.getItemValue("savedScans"))
                gui.configureItem("baseTag", "show", True)

            elif self.prevItem == "currentAsSave":
                self.myDifferential.setCurrentFile(self.realPath + "/../SavedScans/" + gui.getItemValue("savedScans"))
                gui.configureItem("currentTag", "label", "Current: " + gui.getItemValue("savedScans"))
                gui.configureItem("currentTag", "show", True)

            elif item == "confirmLocalBox":
                if len(self.myAnalysis.getFilenames()) > 0:
                    self.myDifferential.currentFile = self.realPath + "/temporary/output.xml"
                    currentSelection = "Current: \n["
                    files = utilities.shortenFileNames(self.myAnalysis.getFilenames())
                    for file in files:
                        currentSelection = currentSelection + file + "\n"
                    currentSelection = currentSelection[:-1] + "]"
                    gui.configureItem("currentTag", "label", currentSelection)
                    gui.configureItem("currentTag", "show", True)
                else:
                    self.myDifferential.currentFile = ""
                    gui.configureItem("currentTag", "label", "")
                    gui.configureItem("currentTag", "show", False)

            if self.myDifferential.baseFile != "" and self.myDifferential.currentFile != "":
                gui.configureItem("diffExecuteBtn", "show", True)
            else:
                gui.configureItem("diffExecuteBtn", "show", False)

            if self.myDifferential.currentFile == self.realPath + "/temporary/output.xml" and self.myDifferential.baseFile != "":
                gui.configureItem("useBaseSettings", "show", True)
            else:
                gui.configureItem("useBaseSettings", "show", False)
                gui.setItemValue("useBaseSettings", False)

            self.switchScreens(gui.getCurrentScreen(), nextScreen)



        #Run differential operation button
        elif item == "diffExecuteBtn":
            if(gui.getItemValue("saveDiffReport")):
                self.myDifferential.setReportFile(gui.getItemValue("diffReportName"))

            baseSettings = settings.settings()
            baseSettings.loadSettingsFromXML(self.myDifferential.baseFile)

            self.switchScreens(gui.getCurrentScreen(), "progressScreen")

            if self.myDifferential.currentFile == self.realPath + "/temporary/output.xml":
                #Current analyzer settings different than base settings
                if gui.getItemValue("useBaseSettings"):
                    self.myAnalysis.settings = copy.deepcopy(baseSettings)

                doubleThread = Thread(target = utilities.doubleOperation, args = (self, ))
                self.myAnalysis.limitOperation()
                self.currentOperation = "BOTH"
                #If the settings are different, then set the compatability flag = false to signify different settings for the two scans
                if baseSettings.toString() != self.myAnalysis.settings.toString():
                    self.myDifferential.settingsCompatability = False
                doubleThread.start() 
            else:
                currentSettings = settings.settings()
                currentSettings.loadSettingsFromXML(self.myDifferential.currentFile)
                #Perform standard differential
                self.currentOperation = "DIFFERENTIAL"
                if baseSettings.toString() != currentSettings.toString():
                    self.myDifferential.settingsCompatability = False
                self.myDifferential.execute()


        if(item != "savedScans"):
            self.prevItem = item





    #Callback for navbox navigation
    def navCallback(self, sender):
        #Make buttons available if condition is met
        gui.bindItemTheme(sender, "navboxActive")
        if gui.getItemValue(sender) != "/.." and os.path.isdir(self.myNavigation.getNavPath()+"/"+gui.getItemValue(sender)):
            if sender == "navbox2":
                if self.myNavigation.checkForRepo(gui.getItemValue(sender)):
                    gui.configureItem("addTag2", "show", False)
                    gui.configureItem("addBtn2", "show", True)
                else:
                    gui.configureItem("addBtn2", "show", False)
                    gui.configureItem("addTag2", "show", True)

            if sender == "navbox3":
                if "compile_commands.json" in os.listdir(self.myNavigation.getNavPath() + "/" + gui.getItemValue(sender)):
                    gui.configureItem("addTag3", "show", False)
                    gui.configureItem("addBtn3", "show", True)
                else:
                    gui.configureItem("addBtn3", "show", False)
                    gui.configureItem("addTag3", "show", True)

        #Check for entering and exiting directories
        if gui.getItemValue(sender) == "/.." and gui.getItemValue(sender) == self.prevClick:
            self.myNavigation.exitPath()
            gui.bindItemTheme(sender, "globalTheme")
            self.updateNavboxes()
            self.prevClick = ""

        elif gui.getItemValue(sender)[0] == "/" and gui.getItemValue(sender) == self.prevClick:
            self.myNavigation.enterPath(gui.getItemValue(sender))
            gui.bindItemTheme(sender, "globalTheme")
            self.updateNavboxes()
            self.prevClick = ""

        #Record previous click
        else:
            self.prevClick = gui.getItemValue(sender)





    #Callback for add/selecting buttons
    def addButtonCallback(self, sender):
        #Map button to value
        values = {
            "addBtn": gui.getItemValue("navbox"),
            "addBtn2": gui.getItemValue("navbox2"),
            "addBtn3": gui.getItemValue("navbox3"),
            "includeAddBtn": gui.getItemValue("navboxSettings"),
            "excludeAddBtn": gui.getItemValue("navboxSettings"),
            "selectLocalBtn": gui.getItemValue("localNavbox")
        }
        #Only process as long as /.. isnt the value
        if values[sender] != "/..":
            #Add file to local scan selection
            if sender == "addBtn" or sender == "selectLocalBtn":
                self.myAnalysis.addFile(values[sender], self.myNavigation.getNavPath())

            #Repository scan and Build scan only allow one selection per analysis
            if sender == "addBtn2" or sender == "addBtn3":
                self.myAnalysis.resetSelection()
                self.myAnalysis.addFile(values[sender], self.myNavigation.getNavPath())

            #Settings add buttons
            elif sender == "includeAddBtn":
                val = self.myAnalysis.tempSettings.getSettings("includes")
                contraVal = self.myAnalysis.tempSettings.getSettings("excludes")

                if self.myNavigation.getNavPath() == "/":
                    values[sender] = values[sender][1:0]

                if self.myNavigation.getNavPath()+values[sender] not in val:
                    if self.myNavigation.getNavPath()+values[sender] not in contraVal:
                        val.insert(0, self.myNavigation.getNavPath()+values[sender])

                self.myAnalysis.setTempSettings("includes", val)

            elif sender == "excludeAddBtn":
                val = self.myAnalysis.tempSettings.getSettings("excludes")
                contraVal = self.myAnalysis.tempSettings.getSettings("includes")

                if self.myNavigation.getNavPath() == "/":
                    values[sender] = values[sender][1:0]

                if self.myNavigation.getNavPath()+values[sender] not in val:
                    if self.myNavigation.getNavPath()+values[sender] not in contraVal:
                        val.insert(0, self.myNavigation.getNavPath()+values[sender])

                self.myAnalysis.setTempSettings("excludes", val)

        #Reconfigure selections to show new values
        self.updateSelections()







    #Callback for switching screens
    def switchScreens(self, currentScreen, screen2):
        self.prevClick = ""
        self.myNavigation.resetAll()
        self.updateNavboxes()

        if screen2 == "settingsScreen":
            self.loadSettings()

        elif currentScreen == "settingsScreen":
            self.myAnalysis.resetTempSettings()
            if screen2 == "mainScreen":
                screen2 = self.prevScreen

        else:
            if screen2 == "mainScreen" or self.item == "backBtn":
                self.resetAll()
            #Configure analysis types if necessary
            if screen2 == "buildScanScreen":
                self.myAnalysis.setAnalysisType("BUILDSCAN")
            elif screen2 == "repoScanScreen":
                self.myAnalysis.setAnalysisType("REPOSCAN")
            elif screen2 != "progressScreen":
                self.myAnalysis.setAnalysisType("STANDARD")

            if currentScreen == "progressScreen":
                if self.currentOperation == "ANALYZE":
                    self.myAnalysis.setForceKill()

        gui.switchScreensGUI(currentScreen, screen2)

        if currentScreen != "savedScanScreen" and currentScreen != "settingsScreen":
            self.prevScreen = currentScreen







    #Resetting things
    def resetAll(self):
        self.myAnalysis.fullReset()
        self.myNavigation.resetAll()
        self.myDifferential.resetAll()
        self.prevClick = ""
        self.prevItem = ""

        self.updateNavboxes()
        self.updateSelections()

        gui.configureItem("addBtn2", "show", False)
        gui.configureItem("addBtn3", "show", False)
        gui.configureItem("addTag2", "show", True)
        gui.configureItem("addTag3", "show", True)
        gui.configureItem("baseTag", "show", False)
        gui.configureItem("currentTag", "show", False)
        gui.configureItem("diffExecuteBtn", "show", False)

        gui.setItemValue("localSaveScan", False)
        gui.setItemValue("repoSaveScan", False)
        gui.setItemValue("buildSaveScan", False)

        gui.setItemValue("localScanName", "myScanName")
        gui.setItemValue("repoScanName", "myScanName")
        gui.setItemValue("buildScanName", "myScanName")
        gui.configureItem("localScanName", "show", False)
        gui.configureItem("repoScanName", "show", False)
        gui.configureItem("buildScanName", "show", False)

        gui.setItemValue("localSaveReport",False)
        gui.setItemValue("repoSaveReport", False)
        gui.setItemValue("buildSaveReport", False)

        gui.setItemValue("localReportName", "report")
        gui.setItemValue("repoReportName", "report")
        gui.setItemValue("buildReportName", "report")
        gui.configureItem("localReportName", "show", False)
        gui.configureItem("repoReportName", "show", False)
        gui.configureItem("buildReportName", "show", False)

        gui.setItemValue("useBaseSettings", False)
        gui.configureItem("useBaseSettings", "show", False)

        gui.setItemValue("saveDiffReport", False)
        gui.configureItem("diffReportName", "show", False)
        gui.setItemValue("diffReportName", "diffReport")

        

    #Refresh GUI elements in settings screen to show temp settings
    def loadSettings(self):
        gui.configureItem("navboxSettings", "items", self.myNavigation.getFiles(True))
        gui.setItemValue("navtagSettings", utilities.displayablePathName(self.myNavigation.getNavPath(), 35))

        includeList = []
        excludeList = []
        for x in self.myAnalysis.tempSettings.getSettings("includes"):
            includeList.insert(0, utilities.displayablePathName(x, 25))
        for x in self.myAnalysis.tempSettings.getSettings("excludes"):
            excludeList.insert(0, utilities.displayablePathName(x, 25))
        gui.configureItem("includeSelection", "items", includeList)
        gui.configureItem("excludeSelection", "items", excludeList)

        gui.setItemValue("enable_styleBox", "style" in self.myAnalysis.tempSettings.getSettings("flags")["enables"])
        gui.setItemValue("enable_performanceBox", "performance" in self.myAnalysis.tempSettings.getSettings("flags")["enables"])
        gui.setItemValue("enable_portabilityBox", "portability" in self.myAnalysis.tempSettings.getSettings("flags")["enables"])
        gui.setItemValue("enable_informationBox", "information" in self.myAnalysis.tempSettings.getSettings("flags")["enables"])
        gui.setItemValue("enable_unusedFunctionsBox", "unusedFunction" in self.myAnalysis.tempSettings.getSettings("flags")["enables"])
        gui.setItemValue("enable_missingIncludesBox", "missingInclude" in self.myAnalysis.tempSettings.getSettings("flags")["enables"])

        suppressionString = ""
        for id in self.myAnalysis.tempSettings.getSettings("suppressions"):
            suppressionString = suppressionString + id + "\n"
        gui.setItemValue("suppressionsInput", suppressionString)

        definesString = ""
        for id in self.myAnalysis.tempSettings.getSettings("defines"):
            definesString = definesString + id + "\n"
        gui.setItemValue("definesInput", definesString)



    #Reset selection elements
    def resetSelection(self):
        self.myAnalysis.resetSelection()
        gui.configureItem("selection", "items", [])
        gui.configureItem("selection2", "items", [])
        gui.configureItem("selection3", "items", [])
        gui.configureItem("localSelection", "items", [])

    #Update selection elements
    def updateSelections(self):
        gui.configureItem("selection", "items", utilities.shortenFileNames(self.myAnalysis.getFilenames()))
        gui.configureItem("selection2", "items", utilities.shortenFileNames(self.myAnalysis.getFilenames()))
        gui.configureItem("selection3", "items", utilities.shortenFileNames(self.myAnalysis.getFilenames()))
        gui.configureItem("localSelection", "items", utilities.shortenFileNames(self.myAnalysis.getFilenames()))
        includeList = []
        excludeList = []
        for x in self.myAnalysis.tempSettings.getSettings("includes"):
            includeList.insert(0, utilities.displayablePathName(x, 25))
        for x in self.myAnalysis.tempSettings.getSettings("excludes"):
            excludeList.insert(0, utilities.displayablePathName(x, 25))
        gui.configureItem("includeSelection", "items", includeList)
        gui.configureItem("excludeSelection", "items", excludeList)

    #Update navigation boxes in gui
    def updateNavboxes(self):
        gui.configureItem("navbox", "items", self.myNavigation.getFiles())
        gui.configureItem("navbox2", "items", self.myNavigation.getFiles())
        gui.configureItem("navbox3", "items", self.myNavigation.getFiles())
        gui.configureItem("savedScans", "items", os.listdir(self.realPath+"/../SavedScans"))
        gui.configureItem("localNavbox", "items", self.myNavigation.getFiles())
        gui.configureItem("navboxSettings", "items", self.myNavigation.getFiles(True))
        gui.configureItem("selectScanBtn", "show", False)

        gui.setItemValue("navtag", utilities.displayablePathName(self.myNavigation.getNavPath(), 50))
        gui.setItemValue("navtag2", utilities.displayablePathName(self.myNavigation.getNavPath(), 50))
        gui.setItemValue("navtag3", utilities.displayablePathName(self.myNavigation.getNavPath(), 50))
        gui.setItemValue("localNavtag", utilities.displayablePathName(self.myNavigation.getNavPath(), 50))
        gui.setItemValue("navtagSettings", utilities.displayablePathName(self.myNavigation.getNavPath(), 35))

        gui.configureItem("addBtn2", "show", False)
        gui.configureItem("addBtn3", "show", False)
        gui.configureItem("addTag2", "show", True)
        gui.configureItem("addTag3", "show", True)

        #Reset themes to not show selection
        gui.bindItemTheme("localNavbox", "globalTheme")
        gui.bindItemTheme("savedScans", "globalTheme")
        gui.bindItemTheme("navboxSettings", "globalTheme")
        gui.bindItemTheme("navbox", "globalTheme")
        gui.bindItemTheme("navbox2", "globalTheme")
        gui.bindItemTheme("navbox3", "globalTheme")

    #Commit non-navbox widgets to temp settings
    def updateTempSettings(self):
        enables=[]
        if gui.getItemValue("enable_styleBox") == True:
            enables.insert(0, "style")
        if gui.getItemValue("enable_performanceBox") == True:
            enables.insert(0, "performance")
        if gui.getItemValue("enable_portabilityBox") == True:
            enables.insert(0, "portability")
        if gui.getItemValue("enable_informationBox") == True:
            enables.insert(0, "information")
        if gui.getItemValue("enable_unusedFunctionsBox") == True:
            enables.insert(0, "unusedFunction")
        if gui.getItemValue("enable_missingIncludesBox") == True:
            enables.insert(0, "missingInclude")

        self.myAnalysis.tempSettings.setSettings("enables", enables)

        suppressionList = []
        for x in gui.getItemValue("suppressionsInput").split("\n"):
            if len(x) > 1:
                suppressionList.append(x)
            
        self.myAnalysis.tempSettings.setSettings("suppressions", suppressionList)

        definesList = []
        for x in gui.getItemValue("definesInput").split("\n"):
            if len(x) > 1:
                definesList.append(x)
            
        self.myAnalysis.tempSettings.setSettings("defines", definesList)

    #Return current operation terminal output
    def getTerminalOutput(self):
        if self.currentOperation == "ANALYZE":
            return self.myAnalysis.terminalOutput
        elif self.currentOperation == "DIFFERENTIAL":
            return self.myDifferential.terminalOutput

    #Return current operation progress
    def getProgressValue(self):
        if self.currentOperation == "ANALYZE":
            return float(self.myAnalysis.progressValue)
        elif self.currentOperation == "DIFFERENTIAL":
            return float(self.myDifferential.progressValue)
        else:
            return 0.0

    #Return true if no current operation is ongoing, false otherwise
    def isFinishedProcessing(self):
        if self.currentOperation == "ANALYZE":
            return self.myAnalysis.getProcessingState()
        if self.currentOperation == "DIFFERENTIAL":
            return self.myDifferential.processingState
    
    #Callback for analyze button
    def analyzeBtnCallback(self):
        if gui.getCurrentScreen() == "repoScanScreen":
            if gui.getItemValue("repoSaveScan"):
                self.myAnalysis.setErrorFile(gui.getItemValue("repoScanName"))
            if gui.getItemValue("repoSaveReport"):
                self.myAnalysis.setReportFile(gui.getItemValue("repoReportName"))


        if gui.getCurrentScreen() == "buildScanScreen":
            if gui.getItemValue("buildSaveScan"):
                self.myAnalysis.setErrorFile(gui.getItemValue("buildScanName"))
            if gui.getItemValue("buildSaveReport"):
                self.myAnalysis.setReportFile(gui.getItemValue("buildReportName"))


        if gui.getCurrentScreen() == "localScanScreen":
            if gui.getItemValue("localSaveScan"):
                self.myAnalysis.setErrorFile(gui.getItemValue("localScanName"))
            if gui.getItemValue("localSaveReport"):
                self.myAnalysis.setReportFile(gui.getItemValue("localReportName"))


        self.myAnalysis.analyzePrep()
        self.myAnalysis.execute()
        self.switchScreens(gui.getCurrentScreen(), "progressScreen")
