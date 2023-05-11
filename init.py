import nuke
import os
import threading
import getpass
import datetime
import re
import time
import os
import json
import sqlite3
#import timelog
import timelog_pruebaDB
#import Test



# AITOR ECHEVESTE TOOLS
nuke.pluginAddPath('./Aitor_Echeveste')
nuke.pluginAddPath('./Aitor_Echeveste/aeRelight2D')

#Catery tools
nuke.pluginAddPath('./Cattery')
nuke.pluginAddPath('./Cattery/MiDaS')
nuke.pluginAddPath('./Cattery/BackgroundMatting')
nuke.pluginAddPath('./Cattery/FaceMakeup')
nuke.pluginAddPath('./Cattery/MODNet')
nuke.pluginAddPath('./Cattery/NAFNet')
nuke.pluginAddPath('./Cattery/RealESRGAN')
nuke.pluginAddPath('./Cattery/TecoGAN')

#Survival kit
nuke.pluginAddPath("./NukeSurvivalToolkit_publicRelease-2.1.1/NukeSurvivalToolkit")

#Backdrop Adjust
Backdrop_path = """./Backdrop_Adjust/"""
nuke.pluginAddPath(Backdrop_path)

#Pixel Fudger
nuke.pluginAddPath('pixelfudger3')

#Stamps Adrian Pueyo
nuke.pluginAddPath("stamps")

#Timelog

#nuke.addOnScriptLoad(timelog.Timelog().start_thread)
nuke.addOnScriptLoad(timelog_pruebaDB.Timelog().start_thread)