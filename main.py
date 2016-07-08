#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

* File Name : main.py

* Purpose : Plugin Manager that fetches plugins from GitHub and FC Wiki

* Creation Date : 06-06-2016

* Copyright (c) 2016 Mandeep Singh <mandeeps708@gmail.com>

"""

from __future__ import print_function
import re
from socket import gaierror
# import ipdb

class Plugin():
    "Information about plugin."
    # def __init__(self, name, author, plugin_type, description, baseurl, infourl):
    # def __init__(self, name, author, baseurl, description):
    def __init__(self, name, baseurl, author = None, description = None):
        "returns plugin info"
        self.name = name
        self.author = author
        self.baseurl = baseurl
        self.description = description
        # self.plugin_type = plugin_type
        # self.infourl = infourl

    def __repr__(self):
        return 'Plugin(%s)' % (self.name)

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
        print("Fetching GitHub Workbenches")
        # For storing instances of Plugin() class.
        # self.instances = []
        self.instances = {}
        self.allPlugins = []

    def githubAuth(self):
        "common function for github authentication"

        from github import Github
        # Github API token. Create one at https://github.com/settings/tokens/new
        # and replace it by "None" below.
        token = None
        git = Github(token)

        return git

    def getPluginsList(self):

        try:
            git = self.githubAuth()

            github_username = "FreeCAD"

            # Name of the repository residing at github_username account.
            repository = "FreeCAD-addons"

            # Repository instance.
            repo = git.get_user(github_username).get_repo(repository)
            print("Fetching repository details...")

            # To store count of number of submodules.
            count = 0

            # Fetching repository contents.
            repo_content = repo.get_dir_contents("")

            # Iterations to fetch submodule entries and their info.
            for item in repo_content:
		url = str(item.html_url)
		try:
		    gitUrl = re.search('(.+?)/tree', url).group(1)
		except:
		    pass
		else:
		    # print(item.name)
		    # print(gitUrl)
                    instance = Plugin(item.name, gitUrl)
                    self.instances[str(item.name)] = instance

            # ipdb.set_trace()
            # print("\nPlugins: ", self.instances)
            return self.instances.values()
            
            """
                ######## Some slow code ########
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
            """
        except gaierror or timeout:
            print("Please check your network connection!")

        except KeyboardInterrupt:
            print("\nInterrupted by Keyboard!")

        except ImportError:
            print("PyGithub isn't installed!")

        #except GithubException:
        #    print("API limit exceeded!")

        #except:
        #    print("Please check your network connection!")


    def getInfo(self, PluginName):

        git = self.githubAuth()

        for x in self.instances.keys():
            if(x == PluginName):
                plugin = self.instances[PluginName]
                print(plugin.name)
                print(plugin.baseurl)

                # Getting the submodule info like author, description.
                submodule_repoInfo = re.search('https://github.com/(.+?)$', plugin.baseurl).group(1)
                submodule_repo = git.get_repo(submodule_repoInfo)
                submodule_author = submodule_repo.owner.name
                submodule_description = submodule_repo.description
                print(submodule_author, submodule_description)
                # ipdb.set_trace()
                # import IPython; IPython.embed()

                # Creating Plugin class instances.
                plugin = Plugin(plugin.name, plugin.baseurl, submodule_author, submodule_description)
                self.allPlugins.append(plugin)
                print(self.allPlugins)

                # ipdb.set_trace()
        return plugin

class FetchFromWiki():
    "fetching macros from wiki"

    def __init__(self):
        print("Fetching Macros from FC Wiki")
        self.macro_instances = []
        self.all_macros = []

    def getPluginsList(self):

        try:
            import requests, bs4

            # FreeCAD Macro page.
            source_link = "http://www.freecadweb.org/wiki/index.php?title=Macros_recipes"
            # source_link = "http://www.freecadweb.org/wiki/index.php?title=Sandbox:Macro_Recipes"

            # Generating parsed HTML tree from the URL.
            req = requests.get(source_link, timeout=15)
            soup = bs4.BeautifulSoup(req.text, 'html.parser')
            # soup = bs4.BeautifulSoup(open("index.html"), 'html.parser')

            # Selects the spans with class MacroLink enclosing the macro links.
            macros = soup.select("span.MacroLink")
            macro_count = 0

            for macro in macros[:5]:
                # Prints macro name
                # ipdb.set_trace()
                macro_name = macro.a.getText()

                # Macro URL.
                macro_url = "http://freecadweb.org" + macro.a.get("href")
                # print(macro_name, macro_url)
                macro_instance = Plugin(macro_name, macro_url)
                self.macro_instances.append(macro_instance)


        except requests.exceptions.ConnectionError:
            print("Please check your network connection!")

        except KeyboardInterrupt:
            print("\nInterrupted by Keyboard!")

        except ImportError:
            print("\nMake sure requests and BeautifulSoup are installed!")

        # print("\nPlugins:", self.macro_instances)
        # ipdb.set_trace()
        return self.macro_instances


    def getInfo(self, PluginName):
        "getting info about macros"

        try:
            import requests, bs4

            for macro in self.macro_instances:
                if(macro.name == PluginName):

                    macro_page = requests.get(macro.baseurl)
                    soup = bs4.BeautifulSoup(macro_page.text, 'html.parser')
                    # ipdb.set_trace()
                    # Use the same URL to fetch macro desciption and macro author

                    macro_description = soup.select(".macro-description")[0].getText()
                    macro_author = soup.select(".macro-author")[0].getText()

        except IndexError:
            print("Macro Information not found! Skipping Macro...")

        else:
            # macro_instance = Plugin(macro_name, macro_author, macro_url, macro_description)
            plugin = Plugin(macro.name, macro.baseurl, macro_author, macro_description)
            self.all_macros.append(plugin)
            # print(plugin.author)

        # ipdb.set_trace()
        return plugin


#obj = Fetch()
#obj.getInfo()

"""
print("\n================ GitHub Workbenches ================\n")
gObj = FetchFromGitHub()
plugins = gObj.getPluginsList()

print("\n================ Macros ================\n")
mac = FetchFromWiki()
mplugins = mac.getPluginsList()

makeCube_info = mac.getInfo("Macro Make Cube")
"""

# animation_info = gObj.getInfo("animation")
# sheetmetal_info = gObj.getInfo("sheetmetal")
# ipdb.set_trace()


class getAllPlugins():
    "Interface to manage all plugins"

    def __init__(self):
        gObj = FetchFromGitHub()
        self.plugins = gObj.getPluginsList()
        mac = FetchFromWiki()
        self.mplugins = mac.getPluginsList()

    def allPlugins(self):
        # ipdb.set_trace()
        allPlugins = self.plugins + self.mplugins
        return allPlugins

# plugin = getAllPlugins()
# plugin.allPlugins()
