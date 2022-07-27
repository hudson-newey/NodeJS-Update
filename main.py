import requests
import re
import os

# get the most recent NodeJS version from the website
def getNodeVersion():
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
def installVersion(versionNumber):
    currentVersion = os.popen(f"node --version").read()[1:]

    if (currentVersion != versionNumber):
        # install nvm version
        os.system(f"nvm install {versionNumber}")

        # use updated nvm version
        os.system(f"nvm use {versionNumber}")
    else:
        print("NodeJS is currently up to date")

if __name__ == "__main__":
    nodeVersion = getNodeVersion()

    # check if the version could be fetched
    if (nodeVersion == 'Error'):
        print("Could not fetch NodeJS version")
        exit()
    
    print(f"Installing NodeJS Version {nodeVersion}")
    installVersion(nodeVersion)
