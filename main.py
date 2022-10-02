import sys
import requests
import re
import os
from os.path import exists

# if false: nodejs is added to PATH via link
# if True: nodejs is added by adding the direct executable to the PATH
DIRECT_CALLING = False

# get the most recent NodeJS version from the website
def getNodeVersion(LTS = False):
    r = requests.get('https://nodejs.org/en/download/releases/')
    if r.status_code == 200:
        try:
            siteText = r.text

            # get the most recent version
            matchRE = r'<td data-label="Version">Node.js (.+)</td>'
            nodeVersion = re.search(matchRE, siteText).group(1)

            return nodeVersion
        except:
            return 'Error'
    else:
        return 'Error'

# install the most recent NodeJS version
def installVersion(versionNumber, overwriteNode = False):
    nodejsPATHExec = "node" if overwriteNode else "nodejs"
    currentVersion = os.popen(f"{nodejsPATHExec} --version").read()[1:]


    if (currentVersion != versionNumber):
        # install nvm version
        if (exists(f"node-v{versionNumber}-linux-x64.tar.gz")):
            os.remove(f"node-v{versionNumber}-linux-x64.tar.gz")

        if (exists("/opt/nodejs")):
            os.system(f"sudo rm -r /opt/nodejs")
        
        if (exists("/usr/bin/nodejs")):
            os.system(f"sudo rm /usr/bin/nodejs")

        os.system(f"wget https://nodejs.org/dist/v{versionNumber}/node-v{versionNumber}-linux-x64.tar.gz")
        os.system(f"tar -xvzf node-v{versionNumber}-linux-x64.tar.gz")
        os.system(f"sudo mv node-v{versionNumber}-linux-x64 /opt/nodejs")

        if (DIRECT_CALLING):
            os.system(f"sudo cp /opt/nodejs/bin/node /usr/bin/{nodejsPATHExec}")
        else:
            os.system(f"sudo ln -s /opt/nodejs/bin/node /usr/bin/{nodejsPATHExec}")
    else:
        print("NodeJS is currently up to date")

def printHelp():
    helpPage = """
    Help page for Python Auto Update (PAU)

    Usage: python3 ./main.py [version]
    Options for version: latest
                         [version number]
    
    Optional Flags:
        --overwrite-node
        This will overwrite your node execuatable. By default, NodeJS-Update creates a new NodeJS executable under the exec PATH name nodejs.
        This will flag will instead replace node in your PATH. Use with caution.
    """

    print(helpPage)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        printHelp()
        exit()

    if (sys.argv[1] == "latest"):
        nodeVersion = getNodeVersion(LTS = True)
    else:
        nodeVersion = sys.argv[1]

    # check if the version could be fetched
    if (nodeVersion == 'Error'):
        print("Could not fetch NodeJS version")
        exit()
    
    print(f"Installing NodeJS Version {nodeVersion}")
    installVersion(nodeVersion, overwriteNode = False)

    print("")
    print("NodeJS installation complete")
    print("Installed as nodejs, check by running")
    print("$ nodejs --version")
