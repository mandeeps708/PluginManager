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
from github import Github
import re
import ipdb

# Github API token.
token = ""

class Plugin():
    "Information about plugin."
    # def __init__(self, name, author, plugin_type, description, baseurl, infourl):
    def __init__(self, name, author, baseurl, description):
        "returns plugin info"
        self.name = name
        self.author = author
        self.baseurl = baseurl
        self.description = description
        # self.plugin_type = plugin_type
        # self.infourl = infourl

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
        # For storing instances of Plugin() class.
        instances = []

    def getPluginsList(self):
        g = Github(token)

        github_username = "FreeCAD"

        # Name of the repository residing at github_username account.
        repository = "FreeCAD-addons"

        # Repository instance.
        repo = g.get_user(github_username).get_repo(repository)
        print("Fetching repository details...")

        # To store count of number of submodules.
        count = 0
        
        instances = []

        # Iterations to fetch submodule entries and their info.
        for x in repo.get_dir_contents(""):
            # if(x.type == "submodule"):
                # print(x.url)

            #Checks if the instance is a submodule, then fetches it's details. 
            if(x.raw_data.get("type") == "submodule"):
                count += 1
                submodule_name = x.name
                print(submodule_name)

                # URL of submodule repository.
                submodule_url = x.raw_data.get("submodule_git_url")
               
                # Getting the owner name and repository name.
                submodule_repoInfo = re.search('https://github.com/(.+?).git', submodule_url).group(1)

                git = Github(token)
                
                # Submodule information.
                submodule_repo = git.get_repo(submodule_repoInfo)
                submodule_author = submodule_repo.owner.name
                submodule_description = submodule_repo.description

                # ipdb.set_trace()

                # Creating Plugin class instances.
                instance = Plugin(submodule_name, submodule_author, submodule_url, submodule_description)
                instances.append(instance)
                # print(instances)

                # ipdb.set_trace()
        return instances

class FetchFromWiki():
    "fetching macros from wiki"

    def __init__(self):
        print("macros")


    def getPluginsList(self):
        # FreeCAD Macro page.
        source_link = "http://www.freecadweb.org/wiki/index.php?title=Macros_recipes"

        # Generating parsed HTML tree from the URL.
        req = requests.get(source_link)
        soup = bs4.BeautifulSoup(req.text, 'html.parser')

        # Selects the spans with class MacroLink enclosing the macro links.
        macros = soup.select("span.MacroLink")
        macro_instances = []
        for macro in macros:
            # Prints macro name
            macro_name = macro.a.getText()

            # Macro URL.
            macro_url = "http://freecadweb.org" + macro.a.get("href")
            print(macro_url)

            macro_page = requests.get(macro_url)
            soup = bs4.BeautifulSoup(macro_page.text, 'html.parser')
            ipdb.set_trace()
            # Use the same URL to fetch macro desciption and macro author
            macro_description = soup.select(".macro-description")[0].getText()
            macro_author = soup.select(".macro-author")[0].getText()

            macro_instance = Plugin(macro_name, macro_author, macro_url, macro_description)
            macro_instances.append(macro_instance)

        return macro_instances

#obj = Fetch()
#obj.getInfo()

git = FetchFromGitHub()
plugins = git.getPluginsList()
mac = FetchFromWiki()
mplugins = mac.getPluginsList()
# ipdb.set_trace()
