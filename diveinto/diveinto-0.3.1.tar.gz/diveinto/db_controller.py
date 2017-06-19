import xml.etree.ElementTree as etree
from diveinto.element import Task
import logging

# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create ch handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

class DBcon:
    '''
    データベースを操作する。
    データベースを操作のための関数と
    カレントリストをもつ
    '''

    def InitDbFile(self, db):
        db.write("<DiveInto name='root'>\n</DiveInto>\n")

    def __init__(self):
        self.IsTreeDirty = False

    def MakeTree(self, db):
        self.tree = etree.parse(db)
        self.cursor = self.tree.getroot()

    def IsDbFileBroken(self, db):
        try:
            tree = etree.parse(db)
        except:
            return True
        return False

    def GetCurrentTaskName(self):
        return self.cursor.get('name')

    def GetCurrentTaskId(self):
        return self.cursor.get('uid')

    def AddTask(self, todoName):
        newTask = Task(todoName)
        self.cursor.append(newTask)
        self.IsTreeDirty = True

    def DeleteTasks(self, *taskNums):
        tasks = []
        taskNames = []
        for taskNum in taskNums:
            try:
                tasks.append(self.cursor[taskNum])
            except IndexError:
                continue

        for task in tasks:
            self.cursor.remove(task)
            taskNames.append(task.get('name'))

        self.IsTreeDirty = True
        return taskNames

    def DiveInto(self, taskNum):
        try:
            self.cursor = self.cursor[taskNum]
        except IndexError:
            return

    def _MoveCursor(self, uid, xpath):
        if uid is None: return
        findResult = self.tree.find(xpath.format(uid))
        if findResult is None: return
        self.cursor = findResult

    def Rise(self):
        parentUid = self.cursor.get('uid')
        self._MoveCursor(parentUid, ".//*[@uid='{}']..")

    def Move(self, uid):
        self._MoveCursor(uid, ".//*[@uid='{}']")

    def ChildTaskNames(self):
        for task in self.cursor:
            yield task.get('name')

    def Commit(self, db):
        self.tree.write(db, encoding='UTF-8')
        self.IsTreeDirty = False
