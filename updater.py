import json
import win32api
import os
import wget
import zipfile
import requests
import re

# TODO: Error handling in batch script
# TODO: Rework path management
# TODO: Python 3.9 and 3.10 support
#* optional: Implement github api authentication

# Variables
trilium_dir = 'C:\\Program Files\\trilium-windows-x64'      # Directory of the 'trilium.exe' file

# Constant
fname = trilium_dir + '\\trilium.exe'
root_dir = "C:\\Program Files"

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
    print(f"{color.yellow}[Debug] - Found local version: " + localVer + f" at "+fname+f"{color.reset}")
    return localVer

# Fetch the latest release
def getLatestVersion():
    try:
        response_API = requests.get('https://api.github.com/repos/zadam/trilium/releases/latest')
        data = response_API.text
        parse_json = json.loads(data)
        latest_release = parse_json['tag_name']
        __latest_release = re.search('\d+[.]\d+[.]\d+', latest_release)
        f_latest_release = __latest_release.group(0)
    except Exception as e:
        print(f"{color.red}[Error] - Failed to fetch repository information\n[Error] - Occurred error: "+str(e)+f"{color.reset}")
        exit(2)
    print(f"{color.yellow}[Debug] - Latest release: " + f_latest_release + f"{color.reset}")
    return f_latest_release

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
        exit(3)

# Deletes old files and extracts new ones
def installUpdate(latest):
    filename="trilium-windows-x64-"+latest+".zip"
    target = os.getenv("tmp") + "\\" + filename
    dest = os.getenv("tmp")
    tmp = os.getenv("tmp") + "\\" + filename

    # File extraction
    try:
        print(f"{color.yellow}[Debug] - Extracting files to " + dest + f"{color.reset}")
        zipfile.ZipFile(target, "r").extractall(dest)
        zipfile.ZipFile(target, "r").close()
        print(f"{color.yellow}\n[Debug] - Extracted files to "+dest+f"{color.reset}")
    except Exception as e:
        print(f"{color.red}[Error] - Failed to extract "+filename+"\n[Error] - Occurred error: "+str(e)+f"{color.reset}")
        exit(5)

    # Deletion of temporary zip
    try:
        print(f"{color.yellow}[Debug] - Deleting temporary file "+tmp+f"{color.reset}")
        os.remove(tmp)
        print(f"{color.yellow}[Debug] - Temporary file deleted {color.reset}")
    except Exception as e:
        print(f"{color.red}[Error] - Failed to delete temporary file "+tmp+"\n[Error] - Occurred error: "+str(e)+f"{color.reset}")
        exit(6)

if not os.path.exists(fname):
    print(f"{color.red}"
        "[Error] - Trilium wasn't found at '" + trilium_dir + "'\n"
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
    downloadUpdate(latest)
    print(f"{color.yellow}[Debug] - Download complete\n[Debug] - Installing update...{color.reset}")
    installUpdate(latest)