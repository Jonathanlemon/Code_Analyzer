import json
import xml.etree.ElementTree as ET

#Class to contain and mutate settings for cppcheck via settings.json file
class settings:
    def __init__(self):
        #General
        self.flags = {"enables": [], "language": "c++", "xml": ""}
        self.enginePath = "../engine/cppcheck-2.8/cppcheck"
        self.includes = []
        self.excludes = []
        self.suppressions = []
        self.defines = []

    def loadSettingsFromJson(self, fname):
        f = open(fname)
        data = json.load(f)

        self.flags = data["flags"]
        self.enginePath = data["enginePath"]
        self.includes = data["includes"]
        self.excludes = data["excludes"]
        self.suppressions = data["suppressions"]
        self.defines = data["defines"]

        f.close()

    def writeSettingsToJson(self, fname):
        f = open(fname, "r+")

        data = json.load(f)
        data["flags"] = self.flags
        data["includes"] = self.includes
        data["excludes"] = self.excludes
        data["suppressions"] = self.suppressions
        data["enginePath"] = self.enginePath
        data["defines"] = self.defines
  
        f.seek(0)
        f.write(json.dumps(data))
        f.truncate()
        f.close()

    def setSettings(self, name, value):
        if name == "flags":
            self.flags = value
        elif name == "enginePath":
            self.enginePath = value
        elif name == "includes":
            self.includes = value
        elif name == "excludes":
            self.excludes = value
        elif name == "suppressions":
            self.suppressions = value
        elif name == "enables":
            self.flags["enables"] = value
        elif name == "defines":
            self.defines = value

    def getSettings(self, name):
        if name == "flags":
            return self.flags
        elif name == "enginePath":
            return self.enginePath
        elif name == "includes":
            return self.includes
        elif name == "excludes":
            return self.excludes
        elif name == "suppressions":
            return self.suppressions
        elif name == "enables":
            return self.flags["enables"]
        elif name == "defines":
            return self.defines


    def loadSettingsFromXML(self, fname):
        tree = ET.parse(fname)
        root = tree.getroot()

        includes = []
        excludes = []
        suppressions = []
        defines = []
        enables = []

        for setting in root.find("./settings"):
            if(setting.tag == "includes"):
                includes.append(setting.get("value"))
            if(setting.tag == "excludes"):
                excludes.append(setting.get("value"))
            if(setting.tag == "suppressions"):
                suppressions.append(setting.get("value"))
            if(setting.tag == "defines"):
                defines.append(setting.get("value"))
            if(setting.tag == "enables"):
                enables.append(setting.get("value"))

        self.setSettings("includes", includes)
        self.setSettings("excludes", excludes)
        self.setSettings("suppressions", suppressions)
        self.setSettings("defines", defines)
        self.setSettings("enables", enables)

    def toString(self):
        return str(self.flags) + ":" + str(self.enginePath) + str(self.includes) + ":" + str(self.excludes) + ":" + str(self.suppressions) + ":" + str(self.defines)
