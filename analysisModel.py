import os
import settings
import copy
import utilities
from threading import Thread

#This class contains both generic and specific members for containing and manipulating data involved in static code analysis
#The class has been designed to represent a single "analysis operation" instance. After each "analysis operation", the model is reset
class analysisModel:
    def __init__(self, myPath):
        self.realPath = myPath
        self.type = "analysisModel"

        #Boolean to represent if the model is "done" analyzing. True unless it is currently executing
        self.processingState = True

        self.terminalOutput = ""
        self.progressValue = 0.0

        #Boolean to determine if pdf and html report should be generated. Only false when doing differentiate with source code
        self.fullOperation = True

        #Each analysis operation has a log file where it logs output from the analysis operation and related processes
        self.logFile = ""

        #Load default settings upon init
        self.settings=settings.settings()
        self.settings.loadSettingsFromJson(self.realPath + "/settings.json")
        #Temp settings to contain changes made in GUI
        self.tempSettings = copy.deepcopy(self.settings)

        #Members to contain file reference information
        self.errorFile = self.realPath + "/temporary/output.xml"
        self.reportFile = self.realPath + "/../reports/analysisReport.pdf"

        #Member to be used to force kill an analysis subprocess in the event of cancellation
        self.forceKillSignal = False

        #Command to be executed in shell to run cppcheck
        self.executeCommand = self.realPath + "/" + self.settings.getSettings("enginePath")
        #Flags for cppcheck
        self.flags = []
        #Filenames of files to be analyzed
        self.filenames = []

        #Flag to determine type of analysis
        self.analysisType = "STANDARD"

    #Completely reset model
    def fullReset(self):
        self.fullOperation = True
        self.processingState = True
        self.terminalOutput = ""
        self.progressValue = 0.0

        #Each analysis operation has a log file where it logs output from the analysis operation and related processes
        self.logFile = ""

        #Load default settings upon init
        self.settings=settings.settings()
        self.settings.loadSettingsFromJson(self.realPath + "/settings.json")
        self.tempSettings = copy.deepcopy(self.settings)

        #Members to contain file reference information
        self.errorFile = self.realPath + "/temporary/output.xml"
        self.reportFile = self.realPath + "/../reports/analysisReport.pdf"

        #Member to be used to force kill an analysis subprocess in the event of cancellation
        self.forceKillSignal = False

        self.executeCommand = self.realPath + "/" + self.settings.getSettings("enginePath")
        self.flags = []
        self.filenames = []

        #Flag to determine type of analysis
        self.analysisType = "STANDARD"

    #Set flag to only analyze, and not generate pdf or html (Used for differentiate with source code)
    def limitOperation(self):
        self.fullOperation = False

    #Renames the output xml file
    def setErrorFile(self, fname):
        self.errorFile = self.realPath + "/../SavedScans/"+fname+".xml"

    def getFilenames(self):
        return self.filenames

    def getProcessingState(self):
        return self.processingState

    #If cancelling an ongoing operation
    def setForceKill(self):
        self.forceKillSignal = True

    #Depending on type of analysis, STANDARD, REPOSCAN, BUILDSCAN
    def setAnalysisType(self, mode):
        self.analysisType = mode

    def setReportFile(self, file):
        self.reportFile = self.realPath + "/../reports/"+file+".pdf"

    #If a folder doesn't exist for this repository, create one
    def checkForBuildDirectory(self):
        name = utilities.shortenFileNames(self.filenames)[0]
        if not os.path.isdir(self.realPath + "/temporary/builds/" + name):
            os.system("mkdir "+self.realPath + "/temporary/builds/" + name)

    def resetSelection(self):
        self.filenames = []

    #Add a file/directory/location as target for analysis
    def addFile(self, fileName, path):
        if fileName[0] == "/":
            fileName = fileName[1:]
        fileName = path + "/" + fileName
        if fileName not in self.filenames:
            self.filenames.append(fileName)


    #Used to manipulate temporary settings
    def setTempSettings(self, name, value):
        self.tempSettings.setSettings(name, value)

    #Save temporary settings
    def saveTempSettings(self):
        self.settings = copy.deepcopy(self.tempSettings)
        self.settings.writeSettingsToJson(self.realPath + "/settings.json")

    def resetTempSettings(self):
        self.tempSettings = copy.deepcopy(self.settings)

    #Clear builds directory from previous repositories
    def clearCache(self):
        os.system("rm -rf " +self.realPath+"/temporary")
        os.mkdir(self.realPath+"/temporary")
        os.mkdir(self.realPath+"/temporary/builds")
        os.mkdir(self.realPath+"/temporary/htmlreports")


    def generateLogFile(self):
        self.logFile = utilities.generateLogFile(self)

    #Process settings, flags, etc to create final analyze command
    def analyzePrep(self):
        self.generateLogFile()

        #Assemble flags based on settings
        if self.analysisType == "BUILDSCAN":
            self.checkForBuildDirectory()
            self.flags.append("--cppcheck-build-dir=" + self.realPath + "/temporary/builds/" + utilities.shortenFileNames(self.filenames)[0])
            self.flags.append("--project=" + self.filenames[0] + "/compile_commands.json")

        elif self.analysisType == "REPOSCAN":
            self.checkForBuildDirectory()
            self.flags.append("--cppcheck-build-dir=" + self.realPath + "/temporary/builds/" + utilities.shortenFileNames(self.filenames)[0])
            if "unusedFunction" not in self.settings.getSettings("enables"):
                self.flags.append("-j5")

        #Process analyzer settings
        for flag in self.settings.getSettings("flags"):
            if flag == "enables":
                if self.settings.getSettings("flags")["enables"] != []:
                    enableFlag = "--enable="
                    for x in self.settings.getSettings("flags")["enables"]:
                        enableFlag += x+","
                    self.flags.append(enableFlag[0:-1])
            else:
                stringFlag = "--"+flag
                if self.settings.getSettings("flags")[flag] != "":
                    stringFlag += "="+str(self.settings.getSettings("flags")[flag])
                self.flags.append(stringFlag)

        for x in self.settings.getSettings("excludes"):
            self.flags.append("-i" + x + "/")

        for x in self.settings.getSettings("includes"):
            self.flags.append("-I" + x + "/")

        for x in self.settings.getSettings("suppressions"):
            self.flags.append("--suppress=" + x)

        if len(self.settings.getSettings("defines")) > 0:
            self.flags.append("--force")

        for x in self.settings.getSettings("defines"):
            self.flags.append("-D" + x)

        self.flags.append("--output-file=" + self.errorFile)

    def execute(self):
        #Begin analysis, sending reference to itself for accessing relevant data
        analysisThread = Thread(target = utilities.threadAnalyze, args = (self, ))
        analysisThread.start() 