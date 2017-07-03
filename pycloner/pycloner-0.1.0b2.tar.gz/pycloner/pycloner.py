#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
################################################################################
#
#    Copyright 2017 Félix Brezo and Yaiza Rubio (i3visio, contacto@i3visio.com)
#
#    This file is part of Pycloner. You can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero  General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################

import argparse
import hashlib
import os
import requests
import shutil
import sys

from  bs4 import BeautifulSoup

from utils import error, warning, success, info, safelyCreateDirectories

__version__ = "0.1.0"


class CrawlerInitializationException(Exception):
    def __init__(self, message="Crawler instance could not be done."):
        self.message = error(message)


class CrawlingException(Exception):
    def __init__(self, message="Something happened when cloning the website."):
        self.message = error(message)


class Crawler():
    # Defining static variables
    visited_links = []
    error_links = []
    max_deep_level = 1


    def __init__(self, url, project_name="website_crawled", data_folder="./tmp", deep_level=None):
        # Verifying if the instance is correct
        if not self._isUrl(url):
            print url
            raise CrawlerInitializationException("The URL provided ('"  + url + "') is not a valid URL.")

        # Initializing the variables
        self.original_url = url                             # http://example.com/index.html
        self.site_name = self.original_url.split("/")[2]    # example.com
        self.base_url = self._getBaseUrl(self.original_url) # http://example.com/
        self.project_name = project_name
        self.data_folder = data_folder
        self.project_path = os.path.join(self.data_folder, self.project_name)
        try:
            safelyCreateDirectories(self.project_path, type="DIRECTORY")
        except:
            raise CrawlerInitializationException("The project path ('"  + self.project_path + "') could not be created.")
        # Setting the deep level
        if deep_level != None:
            Crawler.max_deep_level = deep_level


    def _isUrl(self, url):
        """Private method that verifies whether an URL is an URL.
        """
        if "http://" not in url and "https://" not in url:
            return False
        return True


    def _getBaseUrl(self, url):
        """Private method that gets the base for an URL.
        """
        parts = url.split("/")
        return parts[0] + "//" + parts[2] + "/"


    def _getUrlHash(self, url):
        return hashlib.sha256(url).hexdigest()


    def _save(self, bs, element, folder_path, check=None):
        """Method that iterates over HTML so as to find a given element and collect them.
        """
        links = bs.find_all(element)

        for l in links:
            # Catching the href for most elements which is in <script href="…"
            if element != "img":
                href = l.get("href")
            # Catching the href for images which is in <img src="…"
            else:
                href = l.get("src")

            if href is not None and href not in Crawler.visited_links:
                if check == None or check != None and check in href :
                    print(info("Working with: {}".format(href)))
                    if "//" in href:
                        path_s = href.split("/", 3)
                        file_name = path_s[3]
                    elif href[0] == "/":
                        file_name = href[1:]

                    l = os.path.join(self.base_url, file_name)
                    try:
                        if element != "img":
                            r = requests.get(l)
                        # Saving images
                        else:
                            r = requests.get(l, stream=True)
                    except requests.exceptions.ConnectionError:
                        Crawler.error_links.append(l)
                        continue

                    if r.status_code != 200:
                        Crawler.error_links.append(l)
                        print(error(l))
                        continue

                    try:
                        file_path = os.path.join(folder_path, file_name.split("?")[0].split("#")[0])
                        # Check the existence of the folder structure
                        safelyCreateDirectories(file_path)
                    except:
                        print(error("We could not create the directory tree for: " + file_path))

                    print(info("Saving asset at {}".format(file_path)))
                    if element != "img":
                        with open(file_path, "wb") as f:
                            f.write(r.text.encode('utf-8'))
                            f.close()
                    # Saving images
                    else:
                        with open(file_path, "wb") as f:
                            shutil.copyfileobj(r.raw, f)

                    Crawler.visited_links.append(l)


    def _save_assets(self, html_text, folder_path):
        """Saving the assets from an HTML text.
        """
        bs = BeautifulSoup(html_text, "html.parser")

        # Saving CSS
        self._save(bs=bs, element="link", check=".css", folder_path=folder_path)

        # Saving Javascript
        self._save(bs=bs, element="script", check=".js", folder_path=folder_path)

        # Saving the rest of the images
        self._save(bs=bs, element="img", folder_path=folder_path)


    def crawl(self, link=None, full_website=True, current_level=0):
        """Main crawling function. It receives a link to be crawled and is recursive. If none is provided the original_url of the class will be used.
        """
        if not link:
            link = self.original_url

        # Method needed to create relative URL when called recursively
        if "http://" not in link and "https://" not in link:
            link = self.base_url + link

        if self.site_name in link and link not in Crawler.visited_links:
            print(info("Crawling level: " + str(current_level) + ". Working with: {}".format(link)))

            # Recovering the resource
            try:
                r = requests.get(link)
            except requests.exceptions.ConnectionError:
                raise CrawlingException("Connection error when requesting " + link)

            if r.status_code != 200:
                raise CrawlingException("Invalid response when requesting " + link)

            # Building the current URL folder
            current_url_folder = os.path.join(self.project_path, self.site_name + "_" + self._getUrlHash(link))
            try:
                safelyCreateDirectories(current_url_folder, type="DIRECTORY")
            except:
                raise CrawlerInitializationException("The path for the current website ('"  + current_url_folder + "') could not be created.")

            # Get the file name after https?://
            if link.count("/") <= 2:
                file_name = "index.html"
            elif link.count("/") == 3 and link[-1] == "/":
                file_name = "index.html"
            else:
                file_name = link.split("/", 3)[3]
                if file_name[-1] == "/":
                    file_name += "index.html"

            file_path = os.path.join(current_url_folder, file_name)

            print("Crawled file:\t" + file_path)

            # Saving the crawled file
            with open(file_path, "wb") as f:
                # Replacing any reference  to the website to a local instance of the crawled data
                text = r.text.replace(self.site_name, self.project_path)
                f.write(text.encode('utf-8'))
                f.close()

            # Adding the link to the visited links
            Crawler.visited_links.append(link)

            if full_website:
                # Saving the assets found in the text recovered
                self._save_assets(r.text, current_url_folder)

            # Collecting more resources in deep
            if current_level < self.max_deep_level:
                soup = BeautifulSoup(r.text, "html.parser")

                # Iterating again through all the elements in the HTML website to get new links
                tags = soup.find_all('a')
                for i, link in enumerate(tags):
                    print(info("Starting a new crawling process " + str(i+1) + "/" + str(len(tags)) + " for " + link.get("href")))
                    try:
                        # Instatiating the crwaler
                        new_crawler = Crawler(link.get("href"), self.project_name, self.data_folder)
                        # Starting the crawling process
                        new_crawler.crawl(current_level=current_level+1)
                    except CrawlerInitializationException as e:
                        print(e.message)
                    print(success("Finished crawling for " + link.get("href")))


def getParser():
    """Grabbing the parser for the arguments.
    """
    parser = argparse.ArgumentParser(description='crawler.py - A tool to crawl the content of a website and clone it.', prog='crawler.py', epilog='Check the README.md file for further details on the usage of this program or follow us on Twitter in <http://twitter.com/i3visio>.', add_help=False)
    parser._optionals.title = "Input options (one required)"

    # Defining the mutually exclusive group for the main options
    groupMainOptions = parser.add_mutually_exclusive_group(required=True)
    # Adding the main options
    groupMainOptions.add_argument('--license', required=False, action='store_true', default=False, help='shows the GPLv3+ license and exists.')
    groupMainOptions.add_argument('-u', '--url', metavar='<URL>', action='store', help = 'the URL to be crawled.')

    # Configuring the processing options
    groupProcessing = parser.add_argument_group('Processing arguments', 'Configuring the way in which the application will process the identified profiles.')
    groupProcessing.add_argument('-d', '--depth', metavar='<depth>', required=False, default=1, action='store', type=int, help='depth of the crawling process. By default: 1.')
    groupProcessing.add_argument('-f', '--data_folder', metavar='<name>', required=False, default="./tmp", action='store', help='the name for the crawling project. By default: ./tmp')
    groupProcessing.add_argument('-p', '--project_name', metavar='<name>', required=False, default="website_crawled", action='store', help='the name for the crawling project. By default: website_crawled.')

    # About options
    groupAbout = parser.add_argument_group('About arguments', 'Showing additional information about this program.')
    groupAbout.add_argument('-h', '--help', action='help', help='shows this help and exists.')
    #groupAbout.add_argument('-v', '--verbose', metavar='<verbosity>', choices=[0, 1, 2], required=False, action='store', default=1, help='select the verbosity level: 0 - none; 1 - normal (default); 2 - debug.', type=int)
    groupAbout.add_argument('--version', action='version', version='%(prog)s ' +" " +__version__, help='shows the version of the program and exists.')

    return parser


if __name__ == "__main__":
    # Grabbing the parser
    parser = getParser()

    args = parser.parse_args()

    if args.license:
        print(info("Showing the contents of the license..."))
        with open("COPYING", "r") as iF:
            content = iF.read()
            print(content)
        print(info("Exiting..."))
    else:
        info("Starting the crawling process...")
        # Instatiating the crwaler
        crawler = Crawler(args.url, args.project_name, args.data_folder)
        # Starting the crawling process
        crawler.crawl()
        print(success("Finished crawling for " + link))

        print(info("FINISHED TASK."))
        print(info("--------------"))

        print(success("Links crawled: " + str(len(Crawler.visited_links))))
        for link in Crawler.visited_links:
            print(success(link))

        print(error("Links with errors: " + str(len(Crawler.error_links))))
        for link in Crawler.error_links:
            print(error(link))
