import os
import json
import zipfile
from subprocess import call
from datetime import datetime

nameOfConfig = 'edConfig.json'
ebextensionsFolder = '.ebextensions'
applicationNamePrefix = 'ElasticDeployApp'


# Init Functions


def checkEbInit():
    isEbInitialized = raw_input("\nIs ElasticBeanstalk already initialized? [y,n]")

    if isEbInitialized == "y":
        print "Ok, great!"

    else:
        print "Ok, then we will set it up"
        call(["eb", "init"])


def getCurrentConfigFile():
    with open(nameOfConfig, 'r') as f:
        return json.load(f)


def createBasicConfigFile():
    basicConfig = {
        "repositories": [],
        "foldersToSkipInApplicationZip": [
            "applications",
            ".elasticbeanstalk",
            ".git"
        ],
        "filesToSkipInApplicationZip": [
            "edConfig.json",
            ".env",
            ".gitignore",
            ".DS_Store",
            "LICENSE",
            "README.md",
            "README.rst",
        ]
    }

    with open(nameOfConfig, 'w') as f:
        json.dump(basicConfig, f, indent=4, sort_keys=True)


def writeToConfigFile(action, key, value):
    configFile = getCurrentConfigFile()

    if action == 'update':
        configFile[key] = value

    elif action == 'append':
        configFile[key].append(value)

    with open(nameOfConfig, 'w') as f:
        json.dump(configFile, f, indent=4, sort_keys=True)


def checkRepos(firstRepo):
    if firstRepo:
        addRepo = raw_input("\nAdd a new repository? [y,n]")
    else:
        addRepo = "y"

    if addRepo == "y":
        pathToRepo = raw_input("Please enter the repo path (WITHOUT 'git clone'). Afterwards we will clone it for you.\n")
        basename = os.path.basename(pathToRepo) # getting the directories basename

        serverName = raw_input("What should be the server name in the vhost.conf?\n")
        serverAliases = raw_input("Which aliases should be added to the vhost.conf? [comma-seperated list]\n")
        commandsBeforeApplicationBuild = raw_input("Which commands should be executed before creating the application? E.g. 'git pull', 'composer update', ...[comma-seperated list]\n")
        foldersToSkipInApplicationZip = raw_input("Which folders should be excluded when building the application? Important: exact path starting from applications root. E.g. 'vendor', 'node_modules', 'assets/sass' ...[comma-seperated list]\n")
        filesToSkipInApplicationZip = raw_input("Which files/folders should be excluded when building the application? Important: exact path starting from applications root. E.g. '.env', '.gitignore', 'assets/js/xyz.js' ...[comma-seperated list]\n")

        installComposerPackages = False
        if "vendor" in foldersToSkipInApplicationZip:
            installComposerPackages = raw_input("I just realized that you excluded the vendor folder. Should I install all composer packages when you deploy? [y,n]\n")

        repo = {
            "path": pathToRepo,
            "name": os.path.splitext(basename)[0],
            "serverName": serverName,
            "serverAliases": [x.strip() for x in serverAliases.split(',')],
            "commandsBeforeApplicationBuild": [
                x.strip() for x in commandsBeforeApplicationBuild.split(',')
            ],
            "foldersToSkipInApplicationZip": [
                x.strip() for x in foldersToSkipInApplicationZip.split(',')
            ],
            "filesToSkipInApplicationZip": [
                x.strip() for x in filesToSkipInApplicationZip.split(',')
            ],
            "installComposerPackages":
                True if installComposerPackages == "y" else False
        }

        # Append to config file
        writeToConfigFile("append", "repositories", repo)

        # Clone to repo
        cloneRepo(pathToRepo)

        # Check if another repo should be added
        addAnotherRepo = raw_input(
            "\nDo you want to add another repo? [y,n]"
        )

        if addAnotherRepo == "y":
            checkRepos(False)

    else:
        print "Okidok, you should add it manually in your config!"


def cloneRepo(pathToRepo):
    call(["git", "clone", pathToRepo])


def createFolderIfNotExists(folderName):
    if not os.path.exists(folderName):
        os.makedirs(folderName)


def createVhostConfig():
    configFile = getCurrentConfigFile()
    repositories = configFile["repositories"]

    createFolderIfNotExists(ebextensionsFolder)

    with open(ebextensionsFolder + '/98ElasticDeploy.config', 'w') as f:
        f.write('files:\n')
        f.write('  "/etc/httpd/conf.d/vhosts.conf":\n')
        f.write('    mode: "000644"\n')
        f.write('    owner: root\n')
        f.write('    group: root\n')
        f.write('    content: |\n')

        f.write('      # This file got automatically generated from ElasticDeploy #\n')

        for repo in repositories:
            f.write('      <VirtualHost *:80>\n')
            f.write('        ServerName ' + repo['serverName'] + '\n')
            for alias in repo["serverAliases"]:
                if alias.strip():
                    f.write('        ServerAlias ' + alias + '\n')

            f.write('        DocumentRoot /var/www/html/'+repo['name']+'\n')
            f.write('      </VirtualHost>\n')

        f.close()


def createComposerCommands():
    configFile = getCurrentConfigFile()
    repositories = configFile["repositories"]

    createFolderIfNotExists(ebextensionsFolder)

    # Check if one repo would like to install composerPackages
    createComposerInstallConfig = False
    for repo in repositories:
        if repo["installComposerPackages"]:
            createComposerInstallConfig = True
            break

    if createComposerInstallConfig:
        with open(ebextensionsFolder + '/99composer-install.config', 'w') as f:
            f.write('container_commands:')
            for repo in repositories:
                if repo["installComposerPackages"]:
                    f.write('\n  install-packages-'+repo['name']+':\n')
                    f.write('    command: "/usr/bin/composer.phar install -d /var/app/ondeck/'+repo['name']+'/"\n')

            f.close()


# Build and Deployment Functions


def getPathToApplicationFolder():
    return 'applications/'


def writeToZipFolder(zipFileToWrite, path, foldersToSkip, filesToSkip):
    # prepend path to all filesToSkipItems
    toPrepend = path + '/' if path != './' else ''
    foldersToSkip = [toPrepend + x for x in foldersToSkip]
    filesToSkip = [toPrepend + x for x in filesToSkip]

    for root, directories, files in os.walk(path, True):
        if toPrepend == '':
            directories[:] = [d for d in directories if d not in foldersToSkip]
            files[:] = [f for f in files if f not in filesToSkip]

        for filename in files:
            path = os.path.join(root, filename)
            if any(fts in path for fts in foldersToSkip):
                continue

            if any(fts == path for fts in filesToSkip):
                continue

            zipFileToWrite.write(os.path.join(root, filename))


def createApplication():
    pathToApplicationFolder = getPathToApplicationFolder()
    configFile = getCurrentConfigFile()
    repositories = configFile["repositories"]

    # create empty .zip file in applications folder
    applicationName = applicationNamePrefix + '_' + datetime.now().strftime("%d_%m_%Y_%H_%M_%S")+'.zip'
    print "Creating application: " + applicationName

    if not os.path.exists(pathToApplicationFolder):
        os.makedirs(pathToApplicationFolder)

    zipFileToWrite = zipfile.ZipFile(pathToApplicationFolder + applicationName, 'w', zipfile.ZIP_DEFLATED)

    # 1. add project root to .zip, We skip the repo's here and walk later over each repo
    foldersToSkipInApplicationZip = []
    foldersToSkipInApplicationZip.extend(configFile["foldersToSkipInApplicationZip"])
    for repo in repositories:
        foldersToSkipInApplicationZip.extend([repo["name"]])

    writeToZipFolder(zipFileToWrite, './', foldersToSkipInApplicationZip, configFile["filesToSkipInApplicationZip"])

    # 2. We add content of each repo
    for repo in repositories:
        writeToZipFolder(zipFileToWrite, repo["name"], repo["foldersToSkipInApplicationZip"], repo["filesToSkipInApplicationZip"])

    zipFileToWrite.close()

    print "\nSuccessfully created application :-)"
    return applicationName


def runCommandsBeforeApplicationCreation():
    configFile = getCurrentConfigFile()
    repositories = configFile["repositories"]

    for repo in repositories:
        os.chdir(repo["name"])
        for command in repo["commandsBeforeApplicationBuild"]:
            call(command, shell=True)
        os.chdir("..")


def updateArtifact(pathToApplication):
    with open('.elasticbeanstalk/config.yml', 'r+') as f:
        fileContent = f.readlines()
        f.seek(0)
        f.truncate()

        for line in fileContent:
            if "artifact:" in line or "deploy:" in line:
                continue
            else:
                f.write(line)

        f.write("deploy:\n")
        f.write("   artifact: " + pathToApplication)

    print '\nUpdated Artifact in ElasticBeanstalk config'


def addRepo(firstRepo):
    checkRepos(firstRepo)
    createVhostConfig()
    createComposerCommands()
