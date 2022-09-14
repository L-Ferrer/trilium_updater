import requests
import json
import win32api
import re
import os
import wget
import zipfile
import shutil

# TODO: Rework path management
# Variables
trilium_dir = 'C:\\Program Files (x86)\\trilium-windows-x64'      # Directory of the 'trilium.exe' file

# Constant
fname = trilium_dir + '\\trilium.exe'
if not os.path.exists(fname):
    root_dir = "C:\\Program Files"
    trilium_dir = "C:\\Program Files\\trilium-windows-x64"
    fname = "C:\\Program Files\\trilium-windows-x64\\trilium.exe"
else:
    root_dir = "C:\\Program Files (x86)"
    trilium_dir = "C:\\Program Files (x86)\\trilium-windows-x64"
    fname = "C:\\Program Files (x86)\\trilium-windows-x64\\trilium.exe"

# Colors
class color:
    red = "\u001b[31m"
    green = "\u001b[32m"
    yellow = "\u001b[33m"
    reset = "\u001b[0m"

# Get local version
def getLocalVersion():
    propName = 'FileVersion'
    props = {'FileVersion': None}

    # backslash as parm returns dictionary of numeric info corresponding to VS_FIXEDFILEINFO struc
    fixedInfo = win32api.GetFileVersionInfo(fname, '\\')
    props['FileVersion'] = "%d.%d.%d.%d" % (fixedInfo['FileVersionMS'] / 65536,
            fixedInfo['FileVersionMS'] % 65536, fixedInfo['FileVersionLS'] / 65536,
            fixedInfo['FileVersionLS'] % 65536)

    # \VarFileInfo\Translation returns list of available (language, codepage)
    # pairs that can be used to retreive string info. We are using only the first pair.
    lang, codepage = win32api.GetFileVersionInfo(fname, '\\VarFileInfo\\Translation')[0]

    # any other must be of the form \StringfileInfo\%04X%04X\parm_name, middle
    # two are language/codepage pair returned from above

    strInfoPath = u'\\StringFileInfo\\%04X%04X\\%s' % (lang, codepage, propName)
    strInfo = {}
    strInfo[propName] = win32api.GetFileVersionInfo(fname, strInfoPath)
    
    # parse data to json
    jsonVer = json.dumps(strInfo)
    jsonVer2 = json.loads(jsonVer)
    localVer = jsonVer2['FileVersion']
    print(f"{color.yellow}[Debug] - Local version: " + localVer + f"{color.reset}")
    return localVer

# Fetch the latest release
def getLatestVersion():
    #response_API = requests.get('https://api.github.com/repos/zadam/trilium/releases/latest')
    #data = response_API.text
    #parse_json = json.loads(data)
    #parse_json = data
    #latest_release = parse_json['tag_name']
    #latest_release = re.search('\d+[.]\d+[.]\d+', getLatestVersion())
    #f_latest_release = int(latest_release.group(0))
    #print(f"{color.yellow}[Debug] - Latest release: " + f_latest_release + f"{color.reset}")
    return "0.54.3" #f_latest_release

# Downloads the latest windows release
def downloadUpdate(latest):
    filename="trilium-windows-x64-"+latest+".zip"
    url = "https://github.com/zadam/trilium/releases/download/v"+latest+"/" + filename
    dest = os.getenv("tmp") + "\\" + filename
    print(f"{color.yellow}[Debug] - Downloading latest release ["+filename+"] from https://github.com/zadam/trilium/releases/tag/v" + latest + "/"+filename)
    print(f"{color.reset}")
    try:
        wget.download(url, dest)
        print(f"{color.yellow}\n[Debug] - Downloaded "+filename+" to" + dest + f"{color.reset}")
    except Exception as e:
        print(f"{color.red}[Error] - Failed to download file\n[Error] - Occurred error: "+str(e)+f"{color.reset}")

# Deletes old files and extracts new ones
def installUpdate(latest):
    filename="trilium-windows-x64-"+latest+".zip"
    target = os.getenv("tmp") + "\\" + filename
    dest = root_dir

    # File deletion
    try:
        shutil.rmtree(root_dir+"\\trilium-windows-x64")
        print(f"{color.yellow}\n[Debug] - Deleted folder "+root_dir+f"\\trilium-windows-x64 {color.reset}")
    except Exception as e:
        print(f"{color.red}[Error] - Failed to delete directory "+root_dir+"\\trilium-windows-x64"+"\n[Error] - Occurred error: "+str(e)+f"{color.reset}")

    # File extraction
    try:
        print(f"{color.yellow}[Debug] - Extracting files to " + dest + f"{color.reset}")
        zipfile.ZipFile(target, "r").extractall(dest)
        zipfile.ZipFile(target, "r").close()
        print(f"{color.yellow}\n[Debug] - Extracted files to"+root_dir+f"\\trilium-windows-x64 {color.reset}")
    except Exception as e:
        print(f"{color.red}[Error] - Failed to extract "+filename+"\n[Error] - Occurred error: "+str(e)+f"{color.reset}")

if not os.path.exists(fname):
    print(f"{color.red}"
        "[Error] - Trilium wasn't found at '" + fname + "'\n"
        f"Please check your [trilium_dir] variable{color.reset}")
    exit(1)

latest = getLatestVersion()
local = getLocalVersion()

if(latest == local):
    print(f"{color.green}Your version of Trilium is up to date.{color.reset}")
    exit(0)

if(latest > local):
    print(f"{color.green}An update of Trilium was found")
    print(f"Updating...{color.reset}")
    #downloadUpdate(latest)
    print(f"{color.yellow}[Debug] - Download complete\n[Debug] - Installing update...{color.reset}")
    installUpdate(latest)
    print(f"{color.green}Installation complete{color.reset}\nUpdated Trilium successfully to v"+ latest)