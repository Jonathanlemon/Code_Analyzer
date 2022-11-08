import os

class navigationModel:
    def __init__(self, myPath):
        #Used to navigate file system
        self.realPath = myPath
        self.navigationPath = myPath
        self.validFileTypes = [".cpp", ".cxx", ".cc", ".c++", ".h", ".ipp", ".ixx", ".tpp", ".txx", ".c"]

    #Returns current path in filesystem
    def getNavPath(self):
        return self.navigationPath

    def resetAll(self):
        self.navigationPath = self.realPath

    #Returns list of navigable files/directories based on the path    
    def getFiles(self, onlyDir=False):
        allEntries = os.listdir(self.navigationPath)
        invalids = []
        #If onlyDir is True, only return directory values
        for x in range(len(allEntries)):
            if allEntries[x][0] == ".":
                invalids.append(allEntries[x])

            elif os.path.isdir(self.navigationPath + '/' + allEntries[x]):
                allEntries[x] = '/'+allEntries[x]

            elif os.path.splitext(str(self.navigationPath + '/' + allEntries[x]))[1] not in self.validFileTypes:
                invalids.append(allEntries[x])

            elif onlyDir:
                invalids.append(allEntries[x])

        allEntries.insert(0, "/..") 
        for x in invalids:
            allEntries.remove(x)
        return sorted(allEntries)

    #Exit a directory in file system
    def exitPath(self):
        if(len(self.navigationPath) > 1):
            while(self.navigationPath[-1] != '/'):
                self.navigationPath = self.navigationPath[:-1]
            if len(self.navigationPath) > 1:
                self.navigationPath = self.navigationPath[:-1]
    
    #Go into a particular directory in file system
    def enterPath(self, dirName):
        if os.path.isdir(self.navigationPath + dirName):
            if(len(self.navigationPath) == 1):
                self.navigationPath = ''
            self.navigationPath += dirName

    def checkForRepo(self, path2):
        if ".git" in os.listdir(self.navigationPath + "/" + path2):
            return True
        else:
            return False