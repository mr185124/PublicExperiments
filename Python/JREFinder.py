import json
import requests

# This script queries the AdoptOpenJDK website and gets the latest OpenJDK8 install and saves it to a text file.
# If the script is run again, it will compare the latest version with the version that was saved during previous attempt
# and will only report the version if it is different.

# Script converted to exe using: "pyinstaller --onefile JREFinder.py"
# Note: PyInstaller can be installed using: "pip install pyinstaller"
# 
# If you don't wish to use this script, you can easily use Open Source utilities such as cURL and jq to query the AdoptOpenJDK website
# directly and get the latest release name.
# 
# Example:
# curl --silent "https://api.adoptopenjdk.net/v3/assets/feature_releases/8/ga?architecture=x32&heap_size=normal&image_type=jre&jvm_impl=hotspot&os=windows&page=0&page_size=10&project=jdk&sort_method=DATE&sort_order=DESC&vendor=adoptopenjdk" | jq-win64.exe .[0].release_name
#
#  curl seems to be included with Windows and jq can be obtained as a Chocolatey package or via https://stedolan.github.io/jq/

def getOldVersion( ):
    try:
        f = open("LastVersion.txt", "r")
        oldVersion = f.readline()
        f.close()
    except:
        #print("File not found")
        oldVersion = ""
    return oldVersion

def saveVersion( newVersionName ):
    try:
        f = open( "LastVersion.txt", "w")
        print(newVersionName)
        f.write(newVersionName)
        f.close
    except:
        print("Couldn't save version name to output file. Check permissions")

 
response = requests.get("https://api.adoptopenjdk.net/v3/assets/feature_releases/8/ga?architecture=x32&heap_size=normal&image_type=jre&jvm_impl=hotspot&os=windows&page=0&page_size=10&project=jdk&sort_method=DATE&sort_order=DESC&vendor=adoptopenjdk")

results = json.loads(response.text)

count = len(results)

if count > 0:
    # retrieve the most recent release. Remember, these are sorted in descending order so the first index should point to it.
    latest = results[0]

    binary = latest["binaries"][0]
    if ( ( binary["os"] == "windows" ) and
         ( binary["architecture"] == "x32" ) and
         ( binary["image_type"] == "jre") and
         ( binary["jvm_impl"] == "hotspot" ) ):
    
        installName = binary["installer"]["name"]
        oldVersion = getOldVersion()

        if ( installName == oldVersion ):
            print( "No new versions found")
        else:
            print("New version found - " + installName)
            saveVersion( installName )
else:
    print("No versions found")
