import json
import os
from shutil import copyfile, copytree, rmtree

from core.base.corebaseclass import CoreBaseClass


class CoreFileSystem(CoreBaseClass):
    instance = None

    PATH = 'core.filesystem.path'
    FROM = 'core.filesystem.from'
    TO = 'core.filesystem.to'
    CONTENT = 'core.filesystem.content'
    FILE = 'core.filesystem.file'

    GET_SUB_FOLDERS = 'core.filesystem.get.sub.folders'
    GET_FILES = 'core.filesystem.get.files'
    FILE_EXISTS = 'core.filesystem.file.exists'
    FOLDER_EXISTS = 'core.filesystem.folder.exists'
    CREATE_FOLDER = 'core.filesystem.create.folder'
    COPY_FILE = 'core.filesystem.copy.file'
    COPY_FOLDER = 'core.filesystem.copy.folder'
    CREATE_FILE = 'core.filesystem.create.file'
    CREATE_JSON_FILE = 'core.filesystem.create.json.file'
    APPEND_TEXT_FILE = 'core.filesystem.append.text.file'
    APPEND_BINARY_FILE = 'core.filesystem.append.binary.file'
    READ_TEXT = 'core.filesystem.read.text'
    READ_BYTES = 'core.filesystem.read.bytes'
    READ_FILE = 'core.filesystem.read.file'
    READ_JSON_FILE = 'core.filesystem.read.json.file'
    DELETE_FILE = 'core.filesystem.delete.file'
    DELETE_FOLDER = 'core.filesystem.delete.folder'

    def __init__(self):
        super(CoreFileSystem, self).__init__()
        self.sc.registerService(CoreFileSystem.GET_SUB_FOLDERS, self.serviceGetSubFolders)
        self.sc.registerService(CoreFileSystem.GET_FILES, self.serviceGetFiles)
        self.sc.registerService(CoreFileSystem.FILE_EXISTS, self.serviceFileExists)
        self.sc.registerService(CoreFileSystem.FOLDER_EXISTS, self.serviceFolderExists)
        self.sc.registerService(CoreFileSystem.CREATE_FOLDER, self.serviceCreateFolder)
        self.sc.registerService(CoreFileSystem.COPY_FILE, self.serviceCopyFile)
        self.sc.registerService(CoreFileSystem.COPY_FOLDER, self.serviceCopyFolder)
        self.sc.registerService(CoreFileSystem.CREATE_FILE, self.serviceCreateFile)
        self.sc.registerService(CoreFileSystem.CREATE_JSON_FILE, self.serviceCreateJSONFile)
        self.sc.registerService(CoreFileSystem.APPEND_TEXT_FILE, self.serviceAppendTextFile)
        self.sc.registerService(CoreFileSystem.APPEND_BINARY_FILE, self.serviceAppendBinaryFile)
        self.sc.registerService(CoreFileSystem.READ_TEXT, self.serviceReadText)
        self.sc.registerService(CoreFileSystem.READ_BYTES, self.serviceReadBytes)
        self.sc.registerService(CoreFileSystem.READ_FILE, self.serviceReadFile)
        self.sc.registerService(CoreFileSystem.READ_JSON_FILE, self.serviceReadJSONFile)
        self.sc.registerService(CoreFileSystem.DELETE_FILE, self.serviceDeleteFile)
        self.sc.registerService(CoreFileSystem.DELETE_FOLDER, self.serviceDeleteFolder)

    @staticmethod
    def getInstance():
        if CoreFileSystem.instance == None:
            CoreFileSystem.instance = CoreFileSystem()
        return CoreFileSystem.instance

    def serviceGetSubFolders(self, params):
        pass

    def serviceGetFiles(self, params):
        return os.listdir(params[CoreFileSystem.PATH])

    def serviceFileExists(self, params):
        return os.path.exists(params[CoreFileSystem.PATH])

    def serviceFolderExists(self, params):
        return os.path.exists(params[CoreFileSystem.PATH])

    def serviceCreateFolder(self, params):
        try:
            os.mkdir(params[CoreFileSystem.PATH])
        except Exception as error:
            print error

    def serviceCopyFile(self, params):
        copyfile(params[CoreFileSystem.FROM],params[CoreFileSystem.TO])

    def serviceCopyFolder(self, params):
        copytree(params[CoreFileSystem.FROM],params[CoreFileSystem.TO])

    def serviceCreateFile(self, params):
        self.getFile(params[CoreFileSystem.PATH],'w').write(params[CoreFileSystem.CONTENT])

    def serviceCreateJSONFile(self, params):
        params[CoreFileSystem.CONTENT] = json.dumps(params[CoreFileSystem.CONTENT])
        self.serviceCreateFile(params)

    def serviceAppendTextFile(self, params):
        self.getFile(params[CoreFileSystem.PATH], 'a').write(params[CoreFileSystem.CONTENT])

    def serviceAppendBinaryFile(self, params):
        self.getFile(params[CoreFileSystem.PATH], 'a').write(params[CoreFileSystem.CONTENT])

    def serviceReadText(self, params):
        return self.getFile(params[CoreFileSystem.PATH], 'r').read()

    def serviceReadBytes(self, params):
        return self.getFile(params[CoreFileSystem.PATH], 'rb').read()

    def serviceReadFile(self, params):
        return self.getFile(params[CoreFileSystem.PATH]).read()

    def serviceReadJSONFile(self, params):
        jsonStr = self.getFile(params[CoreFileSystem.PATH]).read()
        return json.loads(jsonStr)

    def serviceDeleteFile(self, params):
        os.remove(params[CoreFileSystem.PATH])

    def serviceDeleteFolder(self, params):
        try:
            rmtree(params[CoreFileSystem.PATH])
        except Exception as error:
            print "can't delete directory ", params[CoreFileSystem.PATH]
            print error

    def getFile(self, path, mode='r'):
        return open(path, mode)
