import json
import win32api
import os
import wget
import zipfile
import requests
import re

# TODO: Docker API - https://docs.docker.com/engine/api/sdk/examples/

# Variable
trilium_dir = '/home/pi'      # Target directory for the docker execute script

# Constant
fname = trilium_dir + '/run_trilium.sh'

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
    print(f"[Debug] - Found local version: " + localVer + f" at "+fname)
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
    except Exception:
        print(f"[Error] - Failed to fetch repository information.")
        exit(2)
    print(f"[Debug] - Latest release: " + f_latest_release)
    return f_latest_release

# Downloads the latest windows release
def downloadUpdate(latest):
    filename="trilium-windows-x64-"+latest+".zip"
    url = "https://github.com/zadam/trilium/releases/download/v"+latest+"/" + filename
    dest = os.getenv("tmp") + "\\" + filename
    print(f"[Debug] - Downloading latest release ["+filename+"] from https://github.com/zadam/trilium/releases/tag/v" + latest + "/"+filename)
    try:
        wget.download(url, dest)
        print(f"\n[Debug] - Downloaded "+filename+" to" + dest)
    except Exception:
        print(f"[Error] - Failed to download file.")
        exit(3)

# Deletes old files and extracts new ones
def installUpdate(latest):
    filename="trilium-windows-x64-"+latest+".zip"
    target = os.getenv("tmp") + "\\" + filename
    dest = os.getenv("tmp")
    tmp = os.getenv("tmp") + "\\" + filename

    # File extraction
    try:
        print(f"[Debug] - Extracting files to " + dest)
        zipfile.ZipFile(target, "r").extractall(dest)
        zipfile.ZipFile(target, "r").close()
        print(f"\n[Debug] - Extracted files to "+dest)
    except Exception:
        print(f"[Error] - Failed to extract "+filename+".")
        exit(4)

    # Deletion of temporary zip
    try:
        print(f"[Debug] - Deleting temporary file "+tmp)
        os.remove(tmp)
        print(f"[Debug] - Temporary file deleted")
    except Exception:
        print(f"[Error] - Failed to delete temporary file "+tmp+".")
        exit(5)

if not os.path.exists(fname):
    print("[Error] - Trilium wasn't found at '" + trilium_dir + "'\n"
        f"Please check your [trilium_dir] variable")
    exit(6)

latest = getLatestVersion()
local = getLocalVersion()

if(latest == local):
    print(f"[Info] - Your version of Trilium is up to date.")
    exit(1)
else:
    print(f"An update of Trilium was found")
    print(f"Updating...")
    downloadUpdate(latest)
    print(f"[Debug] - Download complete\n[Debug] - Installing update...")
    installUpdate(latest)