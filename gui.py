from xml.etree.ElementInclude import include
import dearpygui.dearpygui as dpg
import os

GUIPATH = str(os.path.realpath(__file__))[:-7]
WIDTH = 1000
HEIGHT = 618

#Controller for GUI
myController = None

def registerControllerAsObserver(con):
    global myController
    myController = con

def setItemValue(item, val):
    dpg.set_value(item, val)

def toggleShow(item):
    dpg.configure_item(item, show = (not dpg.get_item_configuration(item)["show"]))

def switchScreensGUI(currentScreen, screen2):
    dpg.set_primary_window(currentScreen, False)
    dpg.hide_item(currentScreen)
    dpg.set_primary_window(screen2, True)
    dpg.show_item(screen2)

def getItemValue(item):
    return dpg.get_value(item)

def bindItemTheme(item, theme):
    dpg.bind_item_theme(item, theme)

def getCurrentScreen():
    return dpg.get_active_window()

def getItems(item):
    return dpg.get_item_configuration(item)['items']

def configureItem(name, field, val):
    if field == "items":
        dpg.configure_item(name, items=val)
    if field == "show":
        dpg.configure_item(name, show=val)
    if field == "label":
        dpg.configure_item(name, label=val)



def loadResources():
    #Load image resources
    with dpg.texture_registry(show=False):
        width, height, channels, data = dpg.load_image(str(GUIPATH + "/resources/srtlogo.png"))
        dpg.add_static_texture(width=width, height=height, default_value=data, tag="texture_tag")
        width, height, channels, data = dpg.load_image(str(GUIPATH + "/resources/settings.png"))
        dpg.add_static_texture(width=width, height=height, default_value=data, tag="texture_tag2")
        width, height, channels, data = dpg.load_image(str(GUIPATH + "/resources/home.png"))
        dpg.add_static_texture(width=width, height=height, default_value=data, tag="homeimg")
        width, height, channels, data = dpg.load_image(str(GUIPATH + "/resources/backBtn.png"))
        dpg.add_static_texture(width=width, height=height, default_value=data, tag="backImg")

def bindResources():
    #Load font resources
    with dpg.font_registry():
        large_font = dpg.add_font(str(GUIPATH+"/resources/montserrat.otf"), 38)
        small_font = dpg.add_font(str(GUIPATH+"/resources/montserrat.otf"), 20)
        smallest_font = dpg.add_font(str(GUIPATH+"/resources/montserrat.otf"), 14)

    dpg.bind_font(small_font)
    dpg.bind_item_font("analyzeTag", large_font)
    dpg.bind_item_font("differentiateTag", large_font)
    dpg.bind_item_font("operationTag", large_font)

    dpg.bind_item_font("localTag", large_font)
    dpg.bind_item_font("repoTag", large_font)
    dpg.bind_item_font("buildTag", large_font)

    dpg.bind_item_font("signature", smallest_font)

    #Themes
    with dpg.theme(tag="globalTheme"):
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, [30,30,30,255])
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, [30,30,30,255])
            dpg.add_theme_color(dpg.mvThemeCol_Button, [30,30,30,255])
            dpg.add_theme_color(dpg.mvThemeCol_Text, [255,255,255,200])
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, [10, 10, 10, 255])
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [20, 20, 20, 255])
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, [100, 100, 100, 255])
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, [100, 100, 100, 255])
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, [30, 30, 30, 255])
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, [30, 30, 30, 255])
            dpg.add_theme_color(dpg.mvThemeCol_Border, [0,0,0,255])
            
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0, 0)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 3, 0)
            dpg.add_theme_style(dpg.mvStyleVar_ScrollbarSize, 20)
            dpg.add_theme_style(dpg.mvStyleVar_ScrollbarRounding, 0)
            dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 3)


    with dpg.theme(tag="navboxActive"):
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, [100, 100, 100, 255])
            


    with dpg.theme(tag="buttonAsText"):
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_Text, [255,255,255,200])
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, [30, 30, 30, 255])
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [30, 30, 30, 255])
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, [30,30,30,255])

    with dpg.theme(tag="noBorder"):
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_Text, [255,255,255,200])
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, [30, 30, 30, 255])
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [30, 30, 30, 255])
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, [30,30,30,255])
            dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 0)

    with dpg.theme(tag="selectionBox"):
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, [30, 30, 30, 255])
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, [30, 30, 30, 255])
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, [30, 30, 30, 255])

    with dpg.theme(tag="imgButtonsBorder"):
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 3, 3)

    with dpg.theme(tag="progressScreenTheme"):
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, [0,0,0,255])
            dpg.add_theme_color(dpg.mvThemeCol_PlotHistogram, [0,255,0,255])
            dpg.add_theme_color(dpg.mvThemeCol_Text, [0,255,0,255])

    dpg.bind_theme("globalTheme")

    dpg.bind_item_theme("progressBar", "progressScreenTheme")
    dpg.bind_item_theme("terminalOutput", "progressScreenTheme")

    dpg.bind_item_theme("analyzeTag", "buttonAsText")
    dpg.bind_item_theme("differentiateTag", "buttonAsText")
    dpg.bind_item_theme("operationTag", "buttonAsText")

    dpg.bind_item_theme("localTag", "buttonAsText")
    dpg.bind_item_theme("repoTag", "buttonAsText")
    dpg.bind_item_theme("buildTag", "buttonAsText")

    dpg.bind_item_theme("sourceCodeTag", "buttonAsText")
    dpg.bind_item_theme("savedScansTag", "buttonAsText")
    

    dpg.bind_item_theme("selection", "selectionBox")
    dpg.bind_item_theme("selection2", "selectionBox")
    dpg.bind_item_theme("selection3", "selectionBox")
    dpg.bind_item_theme("localSelection", "selectionBox")
    dpg.bind_item_theme("includeSelection", "selectionBox")
    dpg.bind_item_theme("excludeSelection", "selectionBox")

    
    dpg.bind_item_theme("baseBtnTag", "noBorder")
    dpg.bind_item_theme("currentBtnTag", "noBorder")

    dpg.bind_item_theme("baseTag", "noBorder")
    dpg.bind_item_theme("currentTag", "noBorder")

    dpg.bind_item_theme("addTag2", "noBorder")
    dpg.bind_item_theme("addTag3", "noBorder")

    for item in dpg.get_all_items():
        if dpg.get_item_info(item)["type"] == "mvAppItemType::mvImageButton":
            dpg.bind_item_theme(item, "imgButtonsBorder")



























def init():
    global myController
    #General Setup for main screen
    dpg.create_context()
    dpg.create_viewport(title='SRT Code Analyzer', width=WIDTH, height=HEIGHT, resizable=False)
    dpg.setup_dearpygui()
    dpg.show_viewport()

    loadResources()

    #Create main screen
    with dpg.window(tag="mainScreen", width=WIDTH, height=HEIGHT, no_background=True):
        #Add widgets
        dpg.add_image(texture_tag="texture_tag", width=750)
        dpg.add_image_button(texture_tag="homeimg", pos=[914,0], callback= lambda: myController.notifyController("homeBtn"))
        dpg.add_image_button(texture_tag="texture_tag2", pos=[828,0], callback= lambda: myController.notifyController("texture_tag2"))

        dpg.add_button(tag="operationTag", pos=[-3,83], width=1003, height=85,  label="Select an Operation")

        dpg.add_button(tag="analysisOperationBtn", pos=[250,218], width=500, height=150, show=True, label="Analyze", callback=lambda: myController.notifyController("analysisOperationBtn"))
        dpg.add_button(tag="differentialOperationBtn", pos=[250,418], width=500, height=150, show=True, label="Differentiate", callback=lambda: myController.notifyController("differentialOperationBtn"))



    with dpg.window(tag="analysisOperationScreen", width=WIDTH, height=HEIGHT, show=False):
        #Add widgets
        dpg.add_image(texture_tag="texture_tag", width=750)
        dpg.add_image_button(texture_tag="homeimg", pos=[914,0], callback= lambda: myController.notifyController("homeBtn"))
        dpg.add_image_button(texture_tag="texture_tag2", pos=[828,0], callback= lambda: myController.notifyController("texture_tag2"))

        dpg.add_button(tag="analyzeTag", pos=[-3,83], width=1003, height=85, show=True, label="Analyze")


        dpg.add_button(tag="localScanBtn", label="Local Select - (Files and Folders)", width=1000, height=150, pos=[0,168], callback=lambda: myController.notifyController("localScanBtn"))
        dpg.add_button(tag="repoScanBtn", label="Git Repository Select", width=1000, height=150, pos=[0,318], callback=lambda: myController.notifyController("repoScanBtn"))
        dpg.add_button(tag="buildScanBtn", label="Compiled Project Select - (CMake \"compile_commands.json\" Required)", width=1000, height=150, pos=[0,468], callback=lambda: myController.notifyController("buildScanBtn"))







    with dpg.window(tag="differentialOperationScreen", width=WIDTH, height=HEIGHT, show=False):
        dpg.add_image(texture_tag="texture_tag", width=750)
        dpg.add_image_button(texture_tag="homeimg", pos=[914,0], callback= lambda: myController.notifyController("homeBtn"))
        dpg.add_image_button(texture_tag="texture_tag2", pos=[828,0], callback= lambda: myController.notifyController("texture_tag2"))

        dpg.add_button(tag="differentiateTag", pos=[-3,83], width=1003, height=85, show=True, label="Differentiate")

        dpg.add_button(tag="baseBtnTag", pos=[0,220], width=500, show=True, label="Base Selection (Old Version)")
        dpg.add_button(tag="currentBtnTag", pos=[500,220], show=True, width=500, label="Current Selection (New Version)")

        dpg.add_button(tag="baseAsSave", label="Load from Saved Scan", width=200, height=50, pos=[150,258], callback=lambda: myController.notifyController("baseAsSave"))
        dpg.add_button(tag="currentAsSave", label="Load from Saved Scan", width=200, height=50, pos=[650,258], callback=lambda: myController.notifyController("currentAsSave"))
        dpg.add_button(tag="currentAsLocal", label="Load as Source Code", width=200, height=50, pos=[650,328], callback=lambda: myController.notifyController("currentAsLocal"))

        dpg.add_button(tag="baseTag", pos=[0,420], width = 500, label="Base: ", show=False)
        dpg.add_button(tag="currentTag", pos=[500,420], width = 500, label="Current: ", show=False)

        dpg.add_button(tag="diffExecuteBtn", label="Compare", width=200, height=50, pos=[400,518], callback=lambda: myController.notifyController("diffExecuteBtn"))

        dpg.add_checkbox(tag="useBaseSettings", label="Apply Settings from Base", pos=[650,518], show=False, callback=lambda: myController.notifyController("useBaseSettings"))

        dpg.add_input_text(tag = "diffReportName", pos=[10, 570], show = False, default_value="diffReport", width=150)
        dpg.add_checkbox(tag="saveDiffReport", label="Save Report As...", pos=[10,540], default_value = False, callback=lambda: toggleShow("diffReportName"))

























    with dpg.window(tag = "localScanScreen", width = WIDTH, height = HEIGHT, show = False):
        #Add widgets
        dpg.add_image(texture_tag="texture_tag", width=750)
        dpg.add_image_button(texture_tag="homeimg", pos=[914,0], callback= lambda: myController.notifyController("homeBtn"))
        dpg.add_image_button(texture_tag="texture_tag2", pos=[828,0], callback=lambda: myController.notifyController("texture_tag2"))

        dpg.add_button(tag="localTag", pos=[-3,83], width=1003, height=85,  label="Local Scan")

        dpg.add_image_button(texture_tag="backImg", width=50, height=50, pos=[920,535], callback=lambda: myController.notifyController("backBtn"))

        dpg.add_button(tag="addBtn", label="Add Selection", width=200, height=50, pos=[150,450], callback=lambda: myController.notifyController("addBtn"))
        dpg.add_text(tag="navtag", pos=[78,190], show=True, default_value=GUIPATH)
        dpg.add_text(tag="selectionTag", pos=[578,190], show=True, default_value="Selection:")
        dpg.add_listbox(tag="navbox", items=[], show=True, pos=[75,210], width=350, num_items=8, callback = lambda: myController.notifyController("navbox"))
        dpg.add_listbox(tag="selection", show=True, pos=[575,210], width=350, num_items=8)
        dpg.add_button(tag="clearSelectionBtn", label="Clear Selection", width=200, height=50, pos=[650,450], callback=lambda: myController.notifyController("clearSelectionBtn"))
        dpg.add_button(tag="analyzeBtn", label="Analyze", width=200, height=50, pos=[400,518], callback=lambda: myController.notifyController("analyzeBtn"))

        dpg.add_input_text(tag = "localScanName", pos=[10, 570], show = False, default_value="myScanName", width=150)
        dpg.add_checkbox(tag="localSaveScan", label="Save Scan", pos=[10,540], default_value = False, callback=lambda: toggleShow("localScanName"))

        dpg.add_input_text(tag = "localReportName", pos=[170, 570], show = False, default_value="report", width=150)
        dpg.add_checkbox(tag="localSaveReport", label="Save Report As..", pos=[170,540], default_value = False, callback=lambda: toggleShow("localReportName"))

    with dpg.window(tag = "repoScanScreen", width = WIDTH, height = HEIGHT, show = False):
        #Add widgets
        dpg.add_image(texture_tag="texture_tag", width=750)
        dpg.add_image_button(texture_tag="homeimg", pos=[914,0], callback= lambda: myController.notifyController("homeBtn"))
        dpg.add_image_button(texture_tag="texture_tag2", pos=[828,0], callback= lambda: myController.notifyController("texture_tag2"))

        dpg.add_button(tag="repoTag", pos=[-3,83], width=1003, height=85,  label="Git Repository Scan")

        dpg.add_image_button(texture_tag="backImg", width=50, height=50, pos=[920,535], callback=lambda: myController.notifyController("backBtn"))

        dpg.add_button(tag="addBtn2", label="Select Repository", width=200, height=50, pos=[150,450], callback=lambda: myController.notifyController("addBtn2"), show=False)
        dpg.add_button(tag="addTag2", label="Please Select a valid Git Repository", width=400, height=50, pos=[50,450])

        dpg.add_text(tag="navtag2", pos=[78,190], show=True, default_value=GUIPATH)
        dpg.add_text(tag="selectionTag2", pos=[578,190], show=True, default_value="Selection:")
        dpg.add_listbox(tag="navbox2", items=[], show=True, pos=[75,210], width=350, num_items=8, callback = lambda: myController.notifyController("navbox2"))
        dpg.add_listbox(tag="selection2", show=True, pos=[575,210], width=350, num_items=8)
        dpg.add_button(tag = "clearSelectionBtn2", label="Clear Selection", width=200, height=50, pos=[650,450], callback=lambda: myController.notifyController("clearSelectionBtn2"))
        dpg.add_button(tag="analyzeBtn2", label="Analyze", width=200, height=50, pos=[400,518], callback=lambda: myController.notifyController("analyzeBtn2"))

        dpg.add_input_text(tag = "repoScanName", pos=[10, 570], show = False, default_value="myScanName", width=150)
        dpg.add_checkbox(tag="repoSaveScan", label="Save Scan", pos=[10,540], default_value = False, callback=lambda: toggleShow("repoScanName"))

        dpg.add_input_text(tag = "repoReportName", pos=[170, 570], show = False, default_value="report", width=150)
        dpg.add_checkbox(tag="repoSaveReport", label="Save Report As..", pos=[170,540], default_value = False, callback=lambda: toggleShow("repoReportName"))

    with dpg.window(tag = "buildScanScreen", width = WIDTH, height = HEIGHT, show = False):
        #Add widgets
        dpg.add_image(texture_tag="texture_tag", width=750)
        dpg.add_image_button(texture_tag="homeimg", pos=[914,0], callback= lambda: myController.notifyController("homeBtn"))
        dpg.add_image_button(texture_tag="texture_tag2", pos=[828,0], callback= lambda: myController.notifyController("texture_tag2"))

        dpg.add_image_button(texture_tag="backImg", width=50, height=50, pos=[920,535], callback=lambda: myController.notifyController("backBtn"))

        dpg.add_button(tag="buildTag", pos=[-3,83], width=1003, height=85,  label="Compiled Project Scan")
        
        dpg.add_button(tag="addBtn3", label="Select Built Path", width=200, height=50, pos=[150,450], callback=lambda: myController.notifyController("addBtn3"), show=False)
        dpg.add_button(tag="addTag3", label="Please Select a valid Built Path", width=400, height=50, pos=[50,450])

        dpg.add_text(tag="navtag3", pos=[78,190], show=True, default_value=GUIPATH)
        dpg.add_text(tag="selectionTag3", pos=[578,190], show=True, default_value="Selection:")
        dpg.add_listbox(tag="navbox3", items=[], show=True, pos=[75,210], width=350, num_items=8, callback = lambda: myController.notifyController("navbox3"))
        dpg.add_listbox(tag="selection3", show=True, pos=[575,210], width=350, num_items=8)
        dpg.add_button(tag="clearSelectionBtn3", label="Clear Selection", width=200, height=50, pos=[650,450], callback=lambda: myController.notifyController("clearSelectionBtn3"))
        dpg.add_button(tag="analyzeBtn3", label="Analyze", width=200, height=50, pos=[400,518], callback=lambda: myController.notifyController("analyzeBtn3"))

        dpg.add_input_text(tag = "buildScanName", pos=[10, 570], show = False, default_value="myScanName", width=150)
        dpg.add_checkbox(tag="buildSaveScan", label="Save Scan", pos=[10,540], default_value = False, callback=lambda: toggleShow("buildScanName"))

        dpg.add_input_text(tag = "buildReportName", pos=[170, 570], show = False, default_value="report", width=150)
        dpg.add_checkbox(tag="buildSaveReport", label="Save Report As..", pos=[170,540], default_value = False, callback=lambda: toggleShow("buildReportName"))






































    #Create the Differential Scan Screen
    with dpg.window(tag="savedScanScreen", width=WIDTH, height=HEIGHT, show=False):
        #Add widgets
        dpg.add_image(texture_tag="texture_tag", width=750)
        dpg.add_image_button(texture_tag="homeimg", pos=[914,0], callback= lambda: myController.notifyController("homeBtn"))

        dpg.add_button(tag="savedScansTag", pos=[-3,83], width=1003, height=85,  label="Saved Scans")

        dpg.add_image_button(texture_tag="backImg", width=50, height=50, pos=[920,535], callback=lambda: myController.notifyController("backBtn"))

        dpg.add_listbox(tag="savedScans", items=os.listdir(GUIPATH+"/../SavedScans"), show=True, pos=[325,250], width=350, num_items=8, callback=lambda: myController.notifyController("savedScans"))
        dpg.add_button(tag="selectScanBtn", label="Select", width=200, height=50, pos=[400,460], callback=lambda: myController.notifyController("selectScanBtn"), show=False)



    #Create the Differential Scan Screen
    with dpg.window(tag="localSelectScreen", width=WIDTH, height=HEIGHT, show=False):
        #Add widgets
        dpg.add_image(texture_tag="texture_tag", width=750)
        dpg.add_image_button(texture_tag="homeimg", pos=[914,0], callback= lambda: myController.notifyController("homeBtn"))

        dpg.add_button(tag="sourceCodeTag", pos=[-3,83], width=1003, height=85,  label="Select Source Code")

        dpg.add_text(tag="localNavtag", pos=[75,230], show=True, default_value=GUIPATH)
        dpg.add_listbox(tag="localNavbox", items=[], show=True, pos=[75,250], width=350, num_items=8, callback=lambda: myController.notifyController("localNavbox"))
        dpg.add_button(tag="selectLocalBtn", label="Select", width=200, height=50, pos=[150,460], callback=lambda: myController.notifyController("selectLocalBtn"))

        dpg.add_text(pos=[575,230], show=True, default_value="Selection:")
        dpg.add_listbox(tag="localSelection", show=True, items=[], pos=[575,250], width=350, num_items=8)
        dpg.add_button(tag = "clearLocalBox", label="Clear Selection", width=200, height=50, pos=[650,460], callback=lambda: myController.notifyController("clearLocalBox"))

        dpg.add_button(tag = "confirmLocalBox", label="Done", width=200, height=50, pos=[400,518], callback=lambda: myController.notifyController("confirmLocalBox"))

        dpg.add_image_button(texture_tag="backImg", width=50, height=50, pos=[920,535], callback=lambda: myController.notifyController("backBtn"))




























    with dpg.window(tag = "settingsScreen", width = WIDTH, height = HEIGHT, show = False):
        #Add widgets
        dpg.add_image(texture_tag="texture_tag", width=750)
        dpg.add_image_button(texture_tag="homeimg", pos=[914,0], callback= lambda: myController.notifyController("homeBtn"))

        dpg.add_text(tag="navtagSettings", pos=[10,140], show=True, default_value=GUIPATH)
        dpg.add_listbox(tag="navboxSettings", items=[], show=True, pos=[10,160], width=250, num_items=7, callback = lambda: myController.notifyController("navboxSettings"))
        dpg.add_button(tag="includeAddBtn", label="Add To Include Paths", width=188, height=50,  pos=[267,185], callback=lambda: myController.notifyController("includeAddBtn"), show=True)
        dpg.add_button(tag="excludeAddBtn", label="Add To Exclude List", width=188, height=50, pos=[267,260], callback=lambda: myController.notifyController("excludeAddBtn"), show=True)
        dpg.add_button(tag="clearIncludesBtn", label="Clear Include Paths", width=200, height=50, pos=[485,340], callback=lambda: myController.notifyController("clearIncludesBtn"))
        dpg.add_button(tag="clearExcludesBtn", label="Clear Exclude List", width=200, height=50, pos=[735,340], callback=lambda: myController.notifyController("clearExcludesBtn"))

        dpg.add_text(tag="includeTag", pos=[460,140], show=True, default_value="Include Paths:")
        dpg.add_listbox(tag="includeSelection", show=True, pos=[460,160], width=250, num_items=7)
        dpg.add_text(tag="excludeTag", pos=[710,140], show=True, default_value="Exclude Paths:")
        dpg.add_listbox(tag="excludeSelection", show=True, pos=[710,160], width=250, num_items=7)


        dpg.add_text(tag="enablesTag", pos=[10,440], show=True, default_value="Additional Checks:")
        dpg.add_checkbox(tag="enable_styleBox", label="Style", pos=[10,470])
        dpg.add_checkbox(tag="enable_performanceBox", label="Performance", pos=[10,490])
        dpg.add_checkbox(tag="enable_portabilityBox", label="Portability", pos=[10,510])
        dpg.add_checkbox(tag="enable_informationBox", label="Information", pos=[10,530])
        dpg.add_checkbox(tag="enable_unusedFunctionsBox", label="Unused Functions", pos=[10,550])
        dpg.add_checkbox(tag="enable_missingIncludesBox", label="Missing Includes", pos=[10,570])


        dpg.add_text(tag="suppressionsTag", pos=[250,425], show=True, default_value="Suppressions:\n(1 fault ID per line)")
        dpg.add_input_text(tag="suppressionsInput", pos=[250,470], width=250, height=130, multiline=True)

        dpg.add_text(tag="signature", pos=[5,600], show=True, default_value="Created by Jonathan Lemon")

        dpg.add_text(tag="definesTag", pos=[550,425], show=True, default_value="Preprocessor Definitions:\n(1 definition per line)")
        dpg.add_input_text(tag="definesInput", pos=[550,470], width=250, height=130, multiline=True)

        dpg.add_button(tag="saveSettingsBtn", label="Save", width=83, height=83, pos=[828,0], callback=lambda: myController.notifyController("saveSettingsBtn"))
        dpg.add_button(tag="loadSettingsBtn", label="Import", width=83, height=83, pos=[742,0], callback=lambda: myController.notifyController("loadSettingsBtn"))

        dpg.add_button(tag="clearCacheBtn", label="Clear Cache", width=125, height=50, pos=[850,488], callback=lambda: myController.notifyController("clearCacheBtn"))
        dpg.add_button(tag="clearLogBtn", label="Clear Logs", width=125, height=50, pos=[850,548], callback=lambda: myController.notifyController("clearLogBtn"))

    with dpg.window(tag = "progressScreen", width = WIDTH, height = HEIGHT, show = False):
        #Add widgets
        dpg.add_image(texture_tag="texture_tag", width=750)
        dpg.add_image_button(tag="cancelBtn", texture_tag="homeimg", pos=[914,0], callback= lambda: myController.notifyController("cancelBtn"))

        dpg.add_button(tag="yesBtn", label="Yes", pos=[914,0], width=83, height = 41, show = False, callback = lambda: myController.notifyController("yesBtn"))
        dpg.add_button(tag="noBtn", label="No", pos=[914,41], width=83, height = 42, show = False, callback = lambda: myController.notifyController("noBtn"))
        dpg.add_text(tag="cancelLabel", default_value="Cancel?", pos=[828,30], show=False)
        dpg.add_input_text(tag="terminalOutput", readonly=True, pos=[10,100], width=980, height=400, multiline=True)
        dpg.add_progress_bar(tag="progressBar", pos=[10,518], width=980, height=90, default_value=0.0)

        dpg.add_image_button(texture_tag="backImg", tag="backBtnProg", width=50, height=50, show=False, pos=[920,535], callback=lambda: myController.notifyController("backBtn"))

    bindResources()

    dpg.set_primary_window("mainScreen", True)





















#Render loop
def beginGUI(myController):

    registerControllerAsObserver(myController)
    init()
    myController.resetAll()
    myController.loadSettings()
    while dpg.is_dearpygui_running():
        #Optimization required 
        curScreen = dpg.get_active_window()

        if curScreen == "localScanScreen":
            dpg.configure_item("analyzeBtn", show=myController.myAnalysis.getFilenames() != [])


        elif curScreen == "repoScanScreen":
            dpg.configure_item("analyzeBtn2", show=myController.myAnalysis.getFilenames() != [])


        elif curScreen == "buildScanScreen":
            dpg.configure_item("analyzeBtn3", show=myController.myAnalysis.getFilenames() != [])

        elif curScreen == "progressScreen":
            if(myController.isFinishedProcessing()):
                configureItem("yesBtn", "show", False)
                configureItem("noBtn", "show", False)
                configureItem("cancelLabel", "show", False)
                configureItem("cancelBtn", "show", True)
                configureItem("backBtnProg", "show", True)
                dpg.set_value("terminalOutput", "All Operations Complete\n"+myController.getTerminalOutput())
                dpg.set_value("progressBar", 1.0)
            else:
                dpg.set_value("terminalOutput", myController.getTerminalOutput())
                dpg.set_value("progressBar", myController.getProgressValue())
                configureItem("backBtnProg", "show", False)


        dpg.render_dearpygui_frame()


    dpg.destroy_context()
