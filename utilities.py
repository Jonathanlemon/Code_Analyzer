#This file is used to store functions used by multiple other components, including multithreaded operations
import subprocess
import xml.etree.ElementTree as ET
import os
import datetime

realPath = str(os.path.realpath(__file__))[:-13]

#Convert path name to shortened version for navtags
def displayablePathName(path, length):
    if(len(path)>length):
        return "..."+path[-(length-2):]
    return path
#---------------------------------------------------------------------------------------------------------------
#Convert filenames to shortened versions for displaying in selection box
def shortenFileNames(names):
    shortNames = []

    for x in names:
        newName = ""
        for c in x:
            newName = newName + c
            if c == '/':
                newName = ""
        shortNames.append(newName)

    return shortNames
#---------------------------------------------------------------------------------------------------------------
#Return logFile name
def generateLogFile(model):
    if model.type == "analysisModel":
        return realPath + "/logs/analysisLog_" + str(datetime.datetime.now()).replace(' ', '_') + ".txt"
    elif model.type == "differentialModel":
        return realPath + "/logs/differentialLog_" + str(datetime.datetime.now()).replace(' ', '_') + ".txt"
#---------------------------------------------------------------------------------------------------------------
#Log data
def log(file, input):
    logFileHandle = open(file, "a")
    logFileHandle.write(str(datetime.datetime.now()).replace(' ', '_') + " : " + str(input) + "\n\n")
    logFileHandle.close()
#---------------------------------------------------------------------------------------------------------------
#Thread target for Differentiate with Source Code
def doubleOperation(con):
    con.myAnalysis.analyzePrep()
    con.currentOperation="ANALYZE"
    if threadAnalyze(con.myAnalysis) == 0:
        con.currentOperation="DIFFERENTIAL"
        runDifferentialMode(con.myDifferential)
#---------------------------------------------------------------------------------------------------------------
#Thread target for Analyze operation
def threadAnalyze(copy):
    log(copy.logFile, "threadAnalyze() called")

    #Prepare analysis state variables
    copy.processingState = False
    copy.terminalOutput = ""
    copy.progressValue = 0.0
    copy.forceKillSignal = False
    validAnalysisPerformed = True

    command = [copy.executeCommand]
    command += copy.flags
    if copy.analysisType != "BUILDSCAN":
        command += copy.filenames
    #Perform Analysis
    log(copy.logFile, command)
    proc = subprocess.Popen(command, shell=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    for line in iter(proc.stdout.readline, ''):
        #If analysis is to be cancelled via forceKillSignal set to true
        if copy.forceKillSignal == True:
            log(copy.logFile, copy.terminalOutput)
            fname = copy.errorFile
            copy.fullReset()
            proc.kill()
            os.system("rm -f "+fname)
            return;

        copy.terminalOutput = line + copy.terminalOutput

        if not line:
            break

        #Watch for a specific error
        if "cppcheck: error:" in line:
            log(copy.logFile, line)
            validAnalysisPerformed=False

        #Get progress data from output for reporting
        x = str(line).find('%')
        if x!= -1:
            copy.progressValue = float(int(str(line)[x-2:x])/100.0)

    #Finish analysis
    proc.stdout.close()
    log(copy.logFile, "STDERR: " + proc.communicate()[1])
    proc.wait()

    #If the analysis was successful, continue processing further
    if validAnalysisPerformed:
        if("missingInclude" in copy.settings.getSettings("flags")["enables"]):
                expandMissingIncludes(copy)

        addSettingsToXML(copy)

        if(copy.fullOperation):
            reportHTML(copy)
            threadGenerateReport(copy)
            os.system("xdg-open " + copy.realPath + "/temporary/htmlreports/index.html > /dev/null 2>&1")
            os.system("xdg-open " + copy.reportFile)
    else:
        copy.terminalOutput = "Something went wrong!\n" + copy.terminalOutput

    log(copy.logFile, copy.terminalOutput)
    #Reset analysis state variables
    output=copy.terminalOutput
    copy.fullReset()
    copy.terminalOutput = output

    if not validAnalysisPerformed:
            return 1
    return 0
#---------------------------------------------------------------------------------------------------------------
#Function for analyze thread to generate and open pdf report after completing analysis
def threadGenerateReport(copy):
    log(copy.logFile, "threadGenerateReport() called")
    #Generate Output Report
    copy.terminalOutput = "Generating PDF Report...\n" + copy.terminalOutput

    command = ["perl"]
    command.append(copy.realPath + "/generateReportFromXML.pl")
    command.append(copy.analysisType)
    command.append(copy.errorFile)
    command.append(copy.reportFile)

    log(copy.logFile, command)
    #Execute perl script with proper command line arguments for sending necessary data
    proc = subprocess.Popen(command, shell=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.stdout.close()
    log(copy.logFile, "STDERR: " + proc.communicate()[1])
    proc.wait()

    #Finish and open report
    copy.terminalOutput = "Done!\n" + copy.terminalOutput
#---------------------------------------------------------------------------------------------------------------
#If missing includes setting is set, go find the list of include files that couldn't be found, and put them in xml
def expandMissingIncludes(copy):
    log(copy.logFile, "expandMissingIncludes() called")
    copy.terminalOutput = "Expanding missing include files...\n" + copy.terminalOutput

    tree = ET.parse(copy.errorFile)
    root = tree.getroot()
    expandedErrors = []

    for error in root.findall("./errors/error"):
        if error.get("msg") == "Cppcheck cannot find all the include files (use --check-config for details)":
            root.find("errors").remove(error)
            updatedTree = ET.ElementTree(root)
            updatedTree.write(copy.errorFile)
            break

    command = [copy.executeCommand]
    command += copy.flags
    if copy.analysisType != "BUILDSCAN":
        command += copy.filenames

    newCommand = command[:]
    newCommand.insert(1, "--check-config")
    for flag in command:
        if "--output-file" in flag:
            newCommand.remove(flag)
            newCommand.insert(len(command)-3, "--output-file=" + copy.realPath + "/temporary/missings.xml")
        if "--cppcheck-build-dir" in flag:
            newCommand.remove(flag)

    log(copy.logFile, newCommand)
    proc = subprocess.Popen(newCommand, shell=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for line in iter(proc.stdout.readline, ''):
        if not line:
            break
        copy.terminalOutput = line + copy.terminalOutput

    proc.stdout.close()
    log(copy.logFile, "STDERR: " + proc.communicate()[1])
    proc.wait()


    tree2 = ET.parse(copy.realPath + "/temporary/missings.xml")
    root2 = tree2.getroot()

    for error in root2.findall("./errors/error"):
        if "Please note" not in str(error.get("msg")):
            expandedErrors.append(error)

    if expandedErrors == []:
        return
 
    errors = root.find("errors")
    for error in expandedErrors:
        errors.append(error)

    tree = ET.ElementTree(root)
    tree.write(copy.errorFile)
    os.system("rm -f " +copy.realPath+"/temporary/missings.xml")
#---------------------------------------------------------------------------------------------------------------
#Generate HTML report
def reportHTML(copy):
    os.system("rm -rf " +copy.realPath+"/temporary/htmlreports")
    os.system("mkdir " +copy.realPath+"/temporary/htmlreports")
    log(copy.logFile, "reportHTML() called")
    log(copy.logFile, [copy.realPath + "/../engine/cppcheck-2.8/htmlreport/cppcheck-htmlreport", "--file="+copy.errorFile, "--report-dir=" + copy.realPath + "/temporary/htmlreports"])
    proc = subprocess.Popen([copy.realPath + "/../engine/cppcheck-2.8/htmlreport/cppcheck-htmlreport", "--file="+copy.errorFile, "--report-dir=" + copy.realPath + "/temporary/htmlreports"], shell=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    copy.terminalOutput = "Creating HTML Report...\n"+copy.terminalOutput

    log(copy.logFile, "STDERR: " + proc.communicate()[1])
    proc.wait()
    copy.terminalOutput = "Done!\n"+copy.terminalOutput
#---------------------------------------------------------------------------------------------------------------
#Function to include settings information and analysis targets to output xml file for access via perl script and inclusion in report
def addSettingsToXML(copy):
    log(copy.logFile, "addSettingsToXML() called")
    copy.terminalOutput = "Writing settings to XML output...\n" + copy.terminalOutput

    tree = ET.parse(copy.errorFile)
    root = tree.getroot()
    settings = ET.SubElement(root, "settings")
    targets = ET.SubElement(root, "targets")

    includes = copy.settings.getSettings("includes")
    excludes = copy.settings.getSettings("excludes")
    suppressions = copy.settings.getSettings("suppressions")
    defines = copy.settings.getSettings("defines")
    enables = copy.settings.getSettings("flags")["enables"]

    for include in includes:
        ET.SubElement(settings, "includes").set("value", include)
    for exclude in excludes:
        ET.SubElement(settings, "excludes").set("value", exclude)
    for suppression in suppressions:
        ET.SubElement(settings, "suppressions").set("value", suppression)
    for enable in enables:
        ET.SubElement(settings, "enables").set("value", enable)
    for define in defines:
        ET.SubElement(settings, "defines").set("value", define)
    for target in copy.filenames:
        ET.SubElement(targets, "target").set("value", target)

    tree = ET.ElementTree(root)
    tree.write(copy.errorFile)
#---------------------------------------------------------------------------------------------------------------
#Thread target for differentiate operation
def runDifferentialMode(copy):
    copy.processingState = False
    copy.terminalOutput = ""
    copy.progressValue = 0.0
    copy.generateLogFile()
    copy.loadFromFiles()
    copy.loadBaseErrors()
    copy.compareElements()
    copy.buildXML()
    

    log(copy.logFile, "Differential Scan Executed")

    copy.progressValue = 0.5
  

    copy.terminalOutput = "Generating Differential Report...\n" + copy.terminalOutput
    command = ["perl", copy.realPath + "/generateDifferentialReport.pl", realPath + "/temporary/differentialResults.xml", copy.reportFile]
    if not copy.settingsCompatability:
        command.append("SETTINGSDIFFERENT")

    proc = subprocess.Popen(command, shell=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    log(copy.logFile, "Generating Differential Report...")
    log(copy.logFile, "STDERR: " + proc.communicate()[1])
    proc.wait()
    copy.terminalOutput = "Done!\n" + copy.terminalOutput
    copy.progressValue = 1.0
    copy.processingState = True
    os.system("xdg-open " + copy.reportFile)
    copy.resetAll()
#---------------------------------------------------------------------------------------------------------------
