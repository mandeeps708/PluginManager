#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

* File Name : pluginManager.py

* Purpose : Plugin Manager that fetches plugins from GitHub and FC Wiki

* Creation Date : 06-06-2016

* Copyright (c) 2016 Mandeep Singh <mandeeps708@gmail.com>

"""

from __future__ import print_function
import re
import os
from socket import gaierror
# Guide to import FreeCAD:
# https://mandeep7.wordpress.com/2016/07/23/import-freecad-in-python/
import FreeCAD
# import ipdb


class Plugin():
    "Information about plugin."
    # def __init__(self, name, author, plugin_type, description, baseurl,
    #              infourl):
    # def __init__(self, name, author, baseurl, description):
    def __init__(self, name, baseurl, plugin_type, author=None,
                 description=None):
        "returns plugin info"
        self.name = name
        self.author = author
        self.baseurl = baseurl
        self.description = description
        self.plugin_type = plugin_type
        self.fetch = self
        self.plugin_dir = None
        # self.infourl = infourl

    def __repr__(self):
        return 'Plugin(%s)' % (self.name)


class Fetch(object):
    "The base fetch class"

    def __init__(self):
        print("Object created")
        self.Plugins = []

    def getPluginsList(self):
        print("Plugins list")

    def getInfo(self, plugin):
        return plugin

    def isInstalled(self):
        print("If installed or not")

    def install(self, plugin):
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
        self.gitPlugins = []
        self.plugin_type = "Workbench"

        # Specify the directory where the Workbenches are to be installed.
        self.plugin_dir = os.path.join(FreeCAD.ConfigGet("UserAppData"), "Mod")

        # If any of the paths do not exist, then create one.
        if not os.path.exists(self.plugin_dir):
            os.makedirs(self.plugin_dir)

    def githubAuth(self):
        "A common function for github authentication"

        from github import Github
        """Github API token. Create one at
        https://github.com/settings/tokens/new and replace it by "None" below.
        """
        token = None
        git = Github(token)

        return git

    def getPluginsList(self):
        "Get a list of GitHub Plugins"

        try:
            git = self.githubAuth()

            github_username = "FreeCAD"

            # Name of the repository residing at github_username account.
            repository = "FreeCAD-addons"

            # Repository instance.
            repo = git.get_user(github_username).get_repo(repository)
            print("Fetching repository details...")

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
                    instance = Plugin(item.name, gitUrl, self.plugin_type)
                    instance.fetch = self
                    self.instances[str(item.name)] = instance

            # ipdb.set_trace()
            # print("\nPlugins: ", self.instances)
            return self.instances.values()

        except gaierror or timeout:
            print("Please check your network connection!")

        except KeyboardInterrupt:
            print("\nInterrupted by Keyboard!")

        except ImportError:
            print("PyGithub isn't installed!")

        """except GithubException:
            print("API limit exceeded!")

        except:
            print("Please check your network connection!")
        """

    def getInfo(self, targetPlugin):
        "Get additional information about a specific plugin (GitHub)."
        git = self.githubAuth()

        # ipdb.set_trace()
        # Check if a plugin is present in the plugin list.
        for instance in self.instances.values():
            if(targetPlugin.name == instance.name):
                # Getting the submodule info like author, description.
                submodule_repoInfo = re.search('https://github.com/(.+?)$',
                                               instance.baseurl).group(1)
                submodule_repo = git.get_repo(submodule_repoInfo)
                # submodule_author = submodule_repo.owner.name
                submodule_author = submodule_repo.owner.login
                submodule_description = submodule_repo.description
                # print(submodule_author, submodule_description)
                # ipdb.set_trace()
                # import IPython; IPython.embed()

                # Creating Plugin class instances.
                print(instance.name, "\n", instance.baseurl, "\n",
                      self.plugin_type, "\n",  submodule_author, "\n",
                      submodule_description)
                workbench = Plugin(instance.name, instance.baseurl,
                                   self.plugin_type, submodule_author,
                                   submodule_description)
                self.gitPlugins.append(workbench)
                break

                # ipdb.set_trace()
        return workbench

    def install(self, plugin):
        "Installs a GitHub plugin"

        print("Installing...", plugin.name)
        import git

        install_dir = os.path.join(self.plugin_dir, plugin.name)

        # Clone the GitHub repository via the URL.
        # git.Git().clone(str(plugin.baseurl), install_dir)

        # Checks if the plugin installation path already exists.
        if not os.path.exists(install_dir):
            """Clone the GitHub repository via Plugin URL to install_dir and
            with depth=1 (shallow clone).
            """
            git.Repo.clone_from(plugin.baseurl, install_dir, depth=1)
            print("Done!")

        else:
            print("Plugin already installed!")


class FetchFromWiki(Fetch):
    "Fetching macros listed on the FreeCAD Wiki"

    def __init__(self):
        print("Fetching Macros from FC Wiki")
        self.macro_instances = []
        self.all_macros = []
        self.plugin_type = "Macro"
        # ipdb.set_trace()

        # Get the user-preferred Macro directory.
        self.plugin_dir = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Macro").GetString("MacroPath")

        # If not specified by user, then set a default one.
        if not self.plugin_dir:
            self.plugin_dir = os.path.join(FreeCAD.ConfigGet("UserAppData"),
                                           "Macro")

        # If any of the paths do not exist, then create one.
        if not os.path.exists(self.plugin_dir):
            os.makedirs(self.plugin_dir)

    def getPluginsList(self):
        "Get a list of plugins available on the FreeCAD Wiki"
        try:
            import requests
            import bs4

            # FreeCAD Macro page.
            source_link = "http://www.freecadweb.org/wiki/index.php?title=Macros_recipes"
            """source_link = "http://www.freecadweb.org/wiki/
                             index.php?title=Sandbox:Macro_Recipes"
            """

            # Generating parsed HTML tree from the URL.
            req = requests.get(source_link, timeout=15)
            soup = bs4.BeautifulSoup(req.text, 'html.parser')
            # soup = bs4.BeautifulSoup(open("index.html"), 'html.parser')

            # Selects the spans with class MacroLink enclosing the macro links.
            macros = soup.select("span.MacroLink")

            # for macro in macros[:5]:
            for macro in macros:
                # Prints macro name
                # ipdb.set_trace()
                macro_name = macro.a.getText()

                # Macro URL.
                macro_url = "http://freecadweb.org" + macro.a.get("href")
                # print(macro_name, macro_url)
                macro_instance = Plugin(macro_name, macro_url,
                                        self.plugin_type)
                macro_instance.fetch = self
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

    def macroWeb(self, targetPlugin):
        """Returns the parsed Macro Web page object. Separated, to be used
           by another functions."""

        try:
            import requests
            import bs4

            if targetPlugin in self.macro_instances:
                macro_page = requests.get(targetPlugin.baseurl)
                soup = bs4.BeautifulSoup(macro_page.text, 'html.parser')
                return soup
            else:
                print("Unknown Plugin!", targetPlugin)

        except requests.exceptions.ConnectionError:
            print("Please check your network connection!")

    def getInfo(self, targetPlugin):
        "Getting additional information about a plugin (macro)"

        try:
            # ipdb.set_trace()
            # import IPython; IPython.embed()

            # Use the same URL to fetch macro desciption and macro author
            macro = self.macroWeb(targetPlugin)
            macro_description = macro.select(".macro-description")[0].getText()
            macro_author = macro.select(".macro-author")[0].getText()

        except IndexError:
            print("Macro Information not found! Skipping Macro...")

        else:
            """macro_instance = Plugin(macro_name, macro_author, macro_url,
                                    macro_description)
            """
            plugin = Plugin(targetPlugin.name, targetPlugin.baseurl,
                            self.plugin_type, macro_author, macro_description)
            print(plugin.name, "\n", plugin.baseurl, "\n", self.plugin_type,
                  "\n",  macro_author, "\n", macro_description)
            self.all_macros.append(plugin)
            # print(plugin.author)

        # ipdb.set_trace()
        return plugin

    def install(self, targetPlugin):
        "Installs the Macro"

        print("Installing...", targetPlugin.name)
        install_dir = os.path.join(self.plugin_dir, targetPlugin.name +
                                   ".FCMacro")

        macro = self.macroWeb(targetPlugin)

        try:
            try:
                macro_code = macro.select(".mw-highlight.mw-content-ltr.macro-code")[0].getText()

            except IndexError:
                macro_code = macro.select(".mw-highlight.mw-content-ltr")[0].getText()

            else:
                print("Nothing there!")

            """except:
                print("No code found!")
            """
            # else:
            # try:
            # Checks if the plugin installation path already exists.

        except:
            print("Macro fetching Error!")

        else:
            if not os.path.exists(install_dir):
                macro_file = open(install_dir, 'w+')
                # ipdb.set_trace()
                macro_file.write(macro_code.encode("utf8"))
                macro_file.close()
                print("Done!")

            else:
                print("Plugin already installed!")
        """
        except:
            print("Couldn't create the file", install_dir)
        """


class PluginManager():
    "An interface to manage all plugins"

    def __init__(self):
        # ipdb.set_trace()
        gObj = FetchFromGitHub()
        mac = FetchFromWiki()
        try:
            self.totalPlugins = gObj.getPluginsList() + mac.getPluginsList()
        except:
            print("Please check the connection!")
            exit()
        self.macro_dir = os.path.join(FreeCAD.ConfigGet("UserAppData"),
                                      "Macro")
        self.workbench_dir = os.path.join(FreeCAD.ConfigGet("UserAppData"),
                                          "Mod")

    def allPlugins(self):
        "Returns all of the available plugins"
        # ipdb.set_trace()
        return self.totalPlugins

    def info(self, targetPlugin):
        "Get additional information about a plugin"
        # ipdb.set_trace()
        # import IPython; IPython.embed()
        if targetPlugin in self.totalPlugins:
            print("\nGetting information about", targetPlugin, "...")
            # ipdb.set_trace()
            targetPlugin.fetch.getInfo(targetPlugin)

    def install(self, targetPlugin):
        "Install a plugin"
        if targetPlugin in self.totalPlugins:
            targetPlugin.fetch.install(targetPlugin)
