#!/usr/bin/python

#   Copyright (c) 2017, Pan Labs (panorbit.in).  
#   This file is licensed under the MIT License.
#   See the LICENSE file.


import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from HTMLParser import HTMLParser

from text_spider.PrintIt import PrintIt,Json


class MyParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        #this varibales are switches to check how output_data flows
        self.inLink = False
        self.json_output=False
        self.txt_output=False

        self.dataArray = []
        self.lasttag = None
        self.lastname = None
        self.lastvalue = None

        # self.checktags=['a','p','br\\','h1','h2','h3','h4','h5','h6','title']

        #tags lists to check html content
        self.headTags=['h1','h2','h3','h4','h5','h6']
        self.textTags=['p','pre','br\\','li','ul','div','span', 'title']


        self.PagesToVisit=[]
        self.ProjectName=''
        self.PresentURL=''
        self.output_data={}
        self.get_first_page=True


        #Json object is created and an instance is assigned to self.Jsonobj
        self.Jsonobj=Json()


    #handels start tag
    def handle_starttag(self, tag, attrs):
        self.inLink = False
        # print(tag)
        if (tag.lower() in self.headTags or tag.lower() in self.textTags):
        	self.inLink = True
        	self.lasttag = tag
        # elif tag.lower()=='img':
        #     for (key, value) in attrs:
        #         if key == 'src':
        #             print ('images: %s'%(value))

        elif tag.lower()=='iframe':
            for (key, value) in attrs:
                if key == 'src':
                    # print ('videos: %s'%(value))
                    if self.txt_output==True:
                        PrintIt('videos: %s'%(value),self.ProjectName)

        elif tag.lower() == 'a':
            self.inLink = True
            self.lasttag = tag
            if self.get_first_page==True:

                for (key, value) in attrs:
                    if key == 'href':
                        if value not in self.PagesToVisit:

                            self.PagesToVisit+=[value]



    def handle_endtag(self, tag):
        if (tag.lower() in self.headTags or tag.lower() in self.textTags):
            self.inlink = False

    #this function prints data when
    def handle_data(self, data):

        if (self.lasttag in self.headTags or self.lasttag in self.textTags) and self.inLink and data.strip():

            #prints text output_data
            if self.txt_output==True:
                if self.lasttag == 'title' :
                    PrintIt("Title : ", self.ProjectName)
                    PrintIt(data,self.ProjectName)
                PrintIt(data,self.ProjectName)
                PrintIt('\n',self.ProjectName)

            #prints json output_data
            if self.json_output==True:
                self.Jsonobj.PresentURL=self.PresentURL
                self.Jsonobj.data=data
                self.Jsonobj.ProjectName=self.ProjectName
                self.Jsonobj.jsonData()


            #gets dict of url and data key/value pairs and saves in output_data
            if self.PresentURL in self.output_data:
                self.output_data[self.PresentURL]+=' ' + data + '\n'
            else:
                self.output_data[self.PresentURL] = data + '\n'


    def remove_tags(self,tags):
        for tag in tags:
            if tag in self.headTags:
                self.headTags.remove(tag)
            elif tag in self.textTags:
                self.headTags.remove(tag)

    def add_tags(self,tags):
        for tag in tags:
            if tag not in self.textTags:
                self.textTags+=[tag]
