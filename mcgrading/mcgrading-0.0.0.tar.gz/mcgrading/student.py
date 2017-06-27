from .functions import *

class Student():
    def __init__(self, zipfile):
        self.zipfile = zipfile
        self.split = self.zipfile.split('_')
        self.name = self.split[-2]
        self.user = self.split[1]
        self.folder = ""
        self.comments = []
        self.comments_text = ""
        self.tasks = []

        with ZipFile(self.zipfile) as zipfile:
            self.files_in_zip = zipfile.namelist()

    def run(self, task):
        self.dir()
        try:
            task.run()
        except Exception as e:
            print("EXCEPTION", e)
            self.comments.append(str(e))
        self.backdir()

    def addTasks(self, tasks):
        self.tasks += tasks

    def unzip(self):
        if self.hasDirectory():
            self.folder = self.files_in_zip[0]
            with ZipFile(self.zipfile) as zipfile:
                zipfile.extractall()
        else:
            self.folder = "%s_%s/"%(self.name, self.split[-1].split('.')[0])
            self.comments.append("Directory does not exist.")
            try:
                os.mkdir(self.folder)
            except FileExistsError:
                pass
            with ZipFile(self.zipfile) as zipfile:
                zipfile.extractall(self.folder)

    def runAll(self):
        for task in self.tasks:
            self.run(task)

        self.makeTextLine()

    def hasDirectory(self):
        if self.files_in_zip[0][-1] == "/":
            return True
        else:
            return False

    def dir(self):
        os.chdir(self.folder[:-1])

    def backdir(self):
        os.chdir(CURRENT_DIRECTORY)

    def undesired(self, desired, remove = True):
        self.dir()
        all_files = glob("*")
        for name in desired:
            if name in all_files:
                all_files.remove(name)
        if len(all_files) != 0:
            text = " ".join(all_files)
            self.comments.append("extrafiles: %s,"%text)
            if remove:
                cleanFiles(all_files)
        self.backdir()
        return all_files

    def makeTextLine(self, delimiter = ','):
        comments = " ".join(self.comments)
        self.comments_text = delimiter.join([self.name, self.user, comments])
