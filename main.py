#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

* File Name : main.py

* Purpose : Contain the base class for plugin manager

* Creation Date : 06-06-2016

* Copyright (c) 2016 Mandeep Singh <mandeeps708@gmail.com>

"""

from __future__ import print_function

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

    def getPluginsList(self):
        print("Plugins")

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


class FetchFromWiki():
    "fetching macros from wiki"

    def __init__(self):
        print("macros")
