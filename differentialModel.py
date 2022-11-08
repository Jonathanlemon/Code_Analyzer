import xml.etree.ElementTree as ET
import hashlib
import utilities
from threading import Thread

#This class represents a differential scan operation
class differentialModel:
    def __init__(self, myPath):
        self.realPath = myPath
        self.type = "differentialModel"
        self.processingState = True
        self.terminalOutput = ""
        self.progressValue = 0.0

        self.settingsCompatability = True

        self.baseFile = ""
        self.currentFile = ""
        self.reportFile = self.realPath + "/../reports/differentialReport.pdf"

        self.newBugs = []
        self.fixedBugs = []
        self.baseTable = {}

        self.logFile = ""

    def setBaseFile(self, base):
        self.baseFile = base

    def setCurrentFile(self, changedFile):
        self.currentFile = changedFile

    def setReportFile(self, name):
        self.reportFile = self.realPath + "/../reports/" + name + ".pdf"

    def resetAll(self):
        self.baseFile = ""
        self.currentFile = ""
        self.baseTable = {}
        self.newBugs = []
        self.fixedBugs = []
        self.processingState = True
        self.terminalOutput = ""
        self.progressValue = 0.0
        self.settingsCompatability = True
        self.reportFile = self.realPath + "/../reports/differentialReport.pdf"
    
    def generateLogFile(self):
        self.logFile = utilities.generateLogFile(self)

    def loadFromFiles(self):
        self.baseTree = ET.parse(self.baseFile)
        self.baseRoot = self.baseTree.getroot()
        self.baseTable = {}

        self.currentTree = ET.parse(self.currentFile)
        self.currentRoot = self.currentTree.getroot()

    def loadBaseErrors(self):
        self.terminalOutput = "Processing base anomalies...\n" + self.terminalOutput
        for error in self.baseRoot.findall("./errors/error"):
            hashVal = self.hashString(self.toString(error))
            if hashVal in self.baseTable.keys():
                self.baseTable[hashVal].append(error)
            else:
                self.baseTable[hashVal] = [error]

    def compareElements(self):
        self.terminalOutput = "Comparing anomalies...\n" + self.terminalOutput
        for error in self.currentRoot.findall("./errors/error"):
            hashVal = self.hashString(self.toString(error))
            if hashVal in self.baseTable.keys():
                if len(self.baseTable[hashVal]) > 1:
                    self.baseTable[hashVal].pop()
                else:
                    del self.baseTable[hashVal]
                continue
            else:
                self.newBugs.append(error)

        for x in self.baseTable:
            for y in range(len(self.baseTable[x])):
                self.fixedBugs.append(self.baseTable[x][y])

    #Generates unique string representation of each error to prepare it for hashing. Does not use line number or col number, since these will change from adding new code in the file, which would give a false positive for a new bug, since the location would change.
    def toString(self, error):
        value = str(error.get("id") + " : " + error.get("severity") + " : " + error.get("msg") + " : " + str(error.get("cwe")))

        if error.find("symbol") != None:
            value += " : " + error.find("symbol").text

        if error.find("location") != None:
            for loc in error.findall("location"):
                value += " : " + loc.get("file")
                if loc.find("info") != None:
                    value += " : " + loc.get("info") 

        return value

    def hashString(self, input):
        return hashlib.sha256(input.encode("utf-8")).hexdigest()

    def buildXML(self):
        self.terminalOutput = "Building XML File...\n" + self.terminalOutput

        root = ET.Element("results")

        #Populate new and fixed bugs
        new = ET.SubElement(root, "new")
        fixed = ET.SubElement(root, "fixed")
        for error in self.newBugs:
            error.set("type", "New Bug")
            new.append(error)
        for error in self.fixedBugs:
            error.set("type", "Fixed Bug")
            fixed.append(error)

        #Populate settings
        oldSettings = ET.SubElement(root, "oldSettings")
        newSettings = ET.SubElement(root, "newSettings")
        oldSettings.append(self.baseRoot.find("settings"))
        newSettings.append(self.currentRoot.find("settings"))

        #Populate targets
        oldTargets = ET.SubElement(root, "oldTargets")
        newTargets = ET.SubElement(root, "newTargets")
        oldTargets.append(self.baseRoot.find("targets"))
        newTargets.append(self.baseRoot.find("targets"))

        tree = ET.ElementTree(root)
        tree.write(self.realPath + "/temporary/differentialResults.xml")
        self.terminalOutput = "Wrote file to "+ self.realPath + "/temporary/differentialResults.xml\n" + self.terminalOutput


    def execute(self):
        differentialThread = Thread(target = utilities.runDifferentialMode, args = (self, ))
        differentialThread.start()
        return differentialThread