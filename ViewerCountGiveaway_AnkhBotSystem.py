#---------------------------------------
#	Import Libraries
#---------------------------------------
import clr, sys, json, os, codecs, time
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")
from ast import literal_eval
#---------------------------------------
#	[Required]	Script Information
#---------------------------------------
ScriptName = "ViewerCountGiveaway"
Website = ""
Creator = "Yaz12321"
Version = "1.0"
Description = "Get a notification when viewer count reaches certain numbers"

settingsFile = os.path.join(os.path.dirname(__file__), "settings.json")

#---------------------------------------
#   Version Information
#---------------------------------------

# Version:

# > 1.0< 
    # Official Release

class Settings:
    # Tries to load settings from file if given 
    # The 'default' variable names need to match UI_Config
    def __init__(self, settingsFile = None):
        if settingsFile is not None and os.path.isfile(settingsFile):
            with codecs.open(settingsFile, encoding='utf-8-sig',mode='r') as f:
                self.__dict__ = json.load(f, encoding='utf-8-sig') 
        else: #set variables if no settings file
            self.OnlyLive = False
            self.count = "(25,50,100)"
            self.giveaway = "(25,50,100)"
            self.Delay = 1
            

            
    # Reload settings on save through UI
    def ReloadSettings(self, data):
        self.__dict__ = json.loads(data, encoding='utf-8-sig')
        return

    # Save settings to files (json and js)
    def SaveSettings(self, settingsFile):
        with codecs.open(settingsFile,  encoding='utf-8-sig',mode='w+') as f:
            json.dump(self.__dict__, f, encoding='utf-8-sig')
        with codecs.open(settingsFile.replace("json", "js"), encoding='utf-8-sig',mode='w+') as f:
            f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8-sig')))
        return


#---------------------------------------
# Initialize Data on Load
#---------------------------------------
def Init():
    # Globals
    global MySettings

    # Load in saved settings
    MySettings = Settings(settingsFile)

    global t
    t = time.time()
    global n
    n = 0
    global trigger
    trigger = 1
    global wasonline
    wasonline = False

    # End of Init
    return

#---------------------------------------
# Reload Settings on Save
#---------------------------------------
def ReloadSettings(jsonData):
    # Globals
    global MySettings

    # Reload saved settings
    MySettings.ReloadSettings(jsonData)

    # End of ReloadSettings
    return



def Execute(data):

    return

def Check():
    if MySettings.OnlyLive:

        #set run permission
        startCheck = Parent.IsLive()
    
    else: #set run permission
        startCheck = True


    if startCheck:
        if trigger == 1:
            VC = Parent.GetViewerList()
            count = literal_eval(MySettings.count)

            if len(VC) > count[n]:
                global n
                Parent.SendStreamWhisper(Parent.GetChannelName().lower(),"Viewer Count: {}".format(count[n]))
                
                global n
                n = n + 1


            if n == len(count):
                global trigger
                trigger = 0
        global t
        t = time.time()

    return
def Reset():
    global t
    t = time.time()
    global n
    n = 0
    global trigger
    trigger = 1
    global wasonline
    wasonline = False
    return

def ScriptToggled(status):
    Reset()

    return

def Tick():
    if Parent.IsLive():
        global wasonline
        wasonline = True
    elif wasonline:
        Reset()
            
    if time.time() > t + MySettings.Delay:
       
        Check()
    return


    

def UpdateSettings():
    with open(m_ConfigFile) as ConfigFile:
        MySettings.__dict__ = json.load(ConfigFile)
    return
