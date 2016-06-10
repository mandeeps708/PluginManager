#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

* File Name : main.py

* Purpose : Contain the base class for plugin manager

* Creation Date : 06-06-2016

* Copyright (c) 2016 Mandeep Singh <mandeeps708@gmail.com>

"""

from __future__ import print_function
import requests, bs4

class Plugin():
    "Information about plugin."
    def __init__(self, name, author, plugin_type, description, baseurl, infourl):
        "returns plugin info"
        self.name = name
        self.author = author
        self.plugin_type = plugin_type
        self.description = description
        self.baseurl = baseurl
        self.infourl = infourl

class Fetch():
    "The base fetch class"

    def __init__(self):
        print("Object created")
        self.Plugins = []

    def getPluginsList(self):
        print("Plugins list")

    def getInfo(self):
        print("Plugin Info")

    def isInstalled(self):
        print("If installed or not")

    def install(self):
        print("Installing")
        
    def isUpToDate(self):
        print("Check for latest version")


class FetchFromGitHub(Fetch):
    "class to get workbenches from GitHub"

    def __init__(self):
        print("git workbenches")

    def getpluginsList(self):
        print('hi')
        link = 'https://github.com/FreeCAD/FreeCAD-addons'
        
        req = requests.get(link)

        soup = bs4.BeautifulSoup(req.text, 'html.parser')

        #output = soup.select(".css-truncate.css-truncate-target")[0].getText()
        output = soup.select(".css-truncate.css-truncate-target")

        #for

        print(output)

        
class FetchFromWiki():
    "fetching macros from wiki"

    def __init__(self):
        print("macros")

obj = Fetch()
obj.getInfo()

git = FetchFromGitHub()
git.getpluginsList()
