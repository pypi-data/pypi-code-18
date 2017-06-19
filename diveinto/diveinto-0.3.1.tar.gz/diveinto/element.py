# -*- coding: utf-8 -*-
import uuid
import xml.etree.ElementTree as etree

class Task(etree.Element):
    def __init__(self, taskName):
        uid = uuid.uuid4().hex
        super().__init__('task',{'name':taskName, 'status':'incomplete', 'priority':'0', 'uid':uid})

    def incomplete(self):
        self.set('status','incomplete')

    def Completed(self):
        self.set('status','complete')

    def IsCompleate(self):
        if(self.get('status') == 'complete'):
            return True
        else:
            return False

    def SetPriority(self, value):
        self.set('priority', value)

    def IncrementPriority(self):
        self.set('priority', self.get('priority')+1)

    def DecrementPriority(self):
        if (self.get('priority')==0): return
        self.set('priority',self.get('priority')-1)

    def __str__(self):
        return self.get('title')
