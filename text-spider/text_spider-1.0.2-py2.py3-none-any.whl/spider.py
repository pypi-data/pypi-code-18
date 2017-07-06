#!/usr/bin/python

#   Copyright (c) 2017, Pan Labs (panorbit.in).  
#   This file is licensed under the MIT License.
#   See the LICENSE file.

import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import requests
from text_spider.parse import MyParser
from text_spider.PrintIt import PrintIt
import urlparse



class Spider():

    #init constructor function
    #takes input URL and allowed_domain as input
    def __init__(self,url,allowed_domain):
        self.url=url
        self.allowed_domain=allowed_domain

        self.ProjectName=''#ProjectName variable which is used to get o/p file name
        # self.add_tags=[]

        #Myparser object is created and an instance is assigned to self.parser
        self.parser=MyParser()
        #the output_data which is recursed from My parser function is assigned to output_data varibale
        self.output_data_s=self.parser.output_data

        #this varibales are switches to check how output_data flows
        self.json_output=False
        self.txt_output=False
        self.is_recursive=True


    def spider(self):
        # parser = MyParser()
        links=self.parser.PagesToVisit

        #datas which is stored in spider varibale is assigned to Myparser objects
        self.parser.ProjectName=self.ProjectName
        self.parser.PresentURL=''
        self.parser.json_output=self.json_output
        self.parser.txt_output=self.txt_output
        self.parser.get_first_page=self.is_recursive
        
        if not self.url.startswith('http'):
            self.url=''.join(['http://',self.url])
        if not self.allowed_domain.startswith('http'):
            self.allowed_domain=''.join(['http://',self.allowed_domain])

        #add requested url to links
        links+=[self.url]

        visitedLinks=[]#this varibale checks links visited

        print('spider is crawling for you')

        #recursion links to parse html content starts here
        for link in links:
            try:
                #checks if url link is in domain range
                if link.startswith(self.allowed_domain):
                    #checks if url is not visited before
                    if link not in visitedLinks:
                        #gets html content using request module
                        r=requests.get(link)
                        self.parser.PresentURL=str(link)

                        if self.txt_output==True:
                            PrintIt('-----------------------------------------------------------------------------\n',self.ProjectName)
                            PrintIt('URL : %s \n'%(link),self.ProjectName)
                        self.parser.feed(r.content)
                        visitedLinks+=[link]
                        links=self.parser.PagesToVisit
                elif not link.startswith('http'):
                    if link not in visitedLinks:
                        if not link.startswith('#'):
                            if len(link) >1:
                                joinedLink=urlparse.urljoin(self.allowed_domain,link)
                                r=requests.get(joinedLink)
                                self.parser.PresentURL=str(link)
                                # print('from spider2')
                                if self.txt_output==True:
                                    PrintIt('-----------------------------------------------------------------------------\n',self.ProjectName)
                                    PrintIt('URL : %s \n'%(joinedLink),self.ProjectName)
                                self.parser.feed(r.content)
                                visitedLinks+=[link]
                                links=self.parser.PagesToVisit
            except:
                pass
                #print('.')
        print('crawling completed successfully')
        return self.output_data_s,links #returns output_data and links


#this function add tags to lists
#takes tags as input in list []
    def add_tags(self,tags):
        for tag in tags:
            if tag not in self.parser.textTags:
                self.parser.textTags+=[tag]


#this function remove tags from lists
#takes tags as input in list []
    def remove_tags(self,tags):
        for tag in tags:
            if tag in self.parser.headTags:
                self.parser.headTags.remove(tag)
            elif tag in self.parser.textTags:
                self.parser.textTags.remove(tag)

#this function gets all takes present in lists
    def get_tags_list(self):
        if self.parser.checktags:
            return(self.parser.textTags+self.parser.headTags)
