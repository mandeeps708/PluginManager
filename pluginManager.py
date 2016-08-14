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
import shutil
# import ipdb


class Plugin():
    "Information about plugin."
    # def __init__(self, name, author, plugin_type, description, baseurl,
    #              infourl):
    # def __init__(self, name, author, baseurl, description):
    def __init__(self, name, baseurl, plugin_type, author=None,
                 description=None, version=None, directory=None):
        "returns plugin info"
        self.name = name
        self.author = author
        self.baseurl = baseurl
        self.description = description
        self.plugin_type = plugin_type
        self.fetch = self
        self.plugin_dir = directory
        self.version = version
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

    def isInstalled(self, plugin):
        print("If installed or not")

    def install(self, plugin):
        print("Installing")

    def isUpToDate(self, plugin):
        print("Check for latest version")

    def uninstall(self, plugin):
        print("Un-installation")

    def update(self, plugin):
        print("Update the plugin")


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
        self.workbench_path = os.path.join(FreeCAD.ConfigGet("UserAppData"), "Mod")

        # If any of the paths do not exist, then create one.
        if not os.path.exists(self.workbench_path):
            os.makedirs(self.workbench_path)

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

        # Checks if the additional information has already been fetched.
        if targetPlugin.author is not None and targetPlugin.description \
                is not None:
            print("Already in the list...")
            return targetPlugin

        # If information isn't there, then fetch it and store it to the dict.
        else:
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

                    # Modifying the Plugin class instance.
                    print(instance.name, "\n", instance.baseurl, "\n",
                          self.plugin_type, "\n",  submodule_author, "\n",
                          submodule_description)
                    targetPlugin.description = submodule_description
                    targetPlugin.author = submodule_author
                    # targetPlugin.version = submodule_version
                    self.gitPlugins.append(targetPlugin)
                    break

                    # ipdb.set_trace()
            return targetPlugin

    def isInstalled(self, plugin):
        """Checks and returns True if the plugin is already installed,
           else returns false.
        """

        self.install_dir = os.path.join(self.workbench_path, plugin.name)
        print(self.install_dir)
        # Associate the plugin directory with the plugin instance.
        plugin.plugin_dir = self.install_dir

        # Checks if the plugin installation path already exists.
        if os.path.exists(self.install_dir):
            return True
        else:
            return False

    def install(self, plugin):
        "Installs a GitHub plugin"

        print("Installing...", plugin.name)
        import git

        # Clone the GitHub repository via the URL.
        # git.Git().clone(str(plugin.baseurl), install_dir)

        # Checks if the plugin installation path already exists.
        if not self.isInstalled(plugin):
            """Clone the GitHub repository via Plugin URL to install_dir and
            with depth=1 (shallow clone).
            """
            git.Repo.clone_from(plugin.baseurl, self.install_dir, depth=1)
            print("Done!")

        else:
            print("Plugin already installed!")

    def isUpToDate(self, targetPlugin):
        "Checks if the plugin is up to date or not"

        # First checks if the plugin is installed!
        if self.isInstalled(targetPlugin) is True:
            # Gets the version of installed plugin.
            from git import Repo
            print(targetPlugin.plugin_dir)
            self.repository = Repo(targetPlugin.plugin_dir)
            print("It is installed!")
            # Fetch information from the remote repository.
            self.repository.git.fetch()
            # Gets the `git status` of the repository.
            git_status = self.repository.git.status()
            # Checks if the repository is up-to-date with remote.
            if re.findall("clean", git_status) or re.findall("up-to-date", git_status):
                print("Latest version already installed!")
                return True

            elif re.findall("behind", git_status) or re.findall("git pull", git_status):
                # New version available!
                print("New version available!")
                return False

        else:
            # If the plugin isn't installed.
            print("Plugin not installed!")
            return None

    def uninstall(self, plugin):
        "Uninstall a GitHub workbench"
        if self.isInstalled(plugin):
            print("Un-installing....", self.install_dir)
            shutil.rmtree(self.install_dir)

        else:
            print("Invalid plugin!")

    def update(self, plugin):
        "Update a GitHub workbench"
        if self.isUpToDate(plugin) is False:
            print("Updating...")
            # git pull the changes to update the plugin.
            self.repository.git.pull()
            print("Plugin successfully updated!")

        else:
            print("Plugin already up-to-date.")


class FetchFromWiki(Fetch):
    "Fetching macros listed on the FreeCAD Wiki"

    def __init__(self):
        print("Fetching Macros from FC Wiki")
        self.macro_instances = []
        self.plugin_type = "Macro"
        # ipdb.set_trace()

        # Get the user-preferred Macro directory.
        self.macro_path = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Macro").GetString("MacroPath")

        # If not specified by user, then set a default one.
        if not self.macro_path:
            self.macro_path = os.path.join(FreeCAD.ConfigGet("UserAppData"),
                                           "Macro")

        # If any of the paths do not exist, then create one.
        if not os.path.exists(self.macro_path):
            os.makedirs(self.macro_path)

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
           by another functions.
        """

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

        # Checks if the additional information has already been fetched.""
        if targetPlugin.author is not None and targetPlugin.version \
                is not None:
            print("Already in the list...")
            return targetPlugin

        # If information isn't there, then fetch it and store it to the dict.
        else:
            try:
                # ipdb.set_trace()
                # import IPython; IPython.embed()

                # Use the same URL to fetch macro desciption and macro author
                macro = self.macroWeb(targetPlugin)
                macro_description = macro.select(".macro-description")[0].getText()
                macro_author = macro.select(".macro-author")[0].getText()
                macro_version = macro.select(".macro-version")[0].getText().replace("\n", "")

            except IndexError:
                print("Macro Information not found! Skipping Macro...")

            else:
                """macro_instance = Plugin(macro_name, macro_author, macro_url,
                                        macro_description)
                """
                # Modifying the plugin information.
                targetPlugin.description = macro_description
                targetPlugin.author = macro_author
                targetPlugin.version = macro_version

                print(targetPlugin.name, "\n", targetPlugin.baseurl, "\n",
                      self.plugin_type, "\n",  macro_author, "\n",
                      macro_description, macro_version)
            return targetPlugin

    def isInstalled(self, targetPlugin):
        """Checks and returns True if the plugin is already installed,
           else returns false.
        """

        # Get plugin information.
        info = self.getInfo(targetPlugin)
        # Store version information after removing new line from it.
        version = info.version
        # The macro installation path.
        self.install_dir = os.path.join(self.macro_path, targetPlugin.name +
                                        "_" + version + ".FCMacro")
        targetPlugin.plugin_dir = self.install_dir
        print(targetPlugin.plugin_dir)

        # Checks if the plugin installation path already exists.
        if os.path.exists(self.install_dir):
            return True
        else:
            return False

    def install(self, targetPlugin):
        "Installs the Macro"

        print("Installing...", targetPlugin.name)

        # Lambda function to check the path existence.
        # self.isThere = lambda path: os.path.exists(path)

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
            if not self.isInstalled(targetPlugin):
                macro_file = open(self.install_dir, 'w+')
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

    def isUpToDate(self, targetPlugin):
        "Checks if the plugin is up to date or not"

        # First checks if the plugin is installed!
        if self.isInstalled(targetPlugin) is True:
            # Gets the version of installed plugin.
            try:
                current_version = re.search('_(\d.+?).FCMacro', targetPlugin.plugin_dir).group(1)
                # current_version = re.findall('_(\d.+?).FCMacro', targetPlugin.plugin_dir)
            except TypeError:
                print("Unexpectedly, couldn't get the plugin dir!")
            # Compares local version with the remote version.
            if current_version == targetPlugin.version:
                print("Latest version already installed!")
                return True

            else:
                # New version available!
                return False

        else:
            # If the plugin isn't installed.
            print("Plugin not installed!")
            return None

    def uninstall(self, targetPlugin):
        "Uninstalls a Macro plugin"
        if self.isInstalled(targetPlugin):
            print("Un-installing....", self.install_dir)
            os.remove(self.install_dir)

        else:
            print("Invalid plugin")

    def update(self, targetPlugin):
        "Update a Macro plugin"
        if self.isUpToDate(targetPlugin) is False:
            print("Updating...")
            backup_file = targetPlugin.plugin_dir + "bak"
            os.rename(targetPlugin.plugin_dir, backup_file)
            # Downloading the Macro again to update the plugin.
            self.install(targetPlugin)
            os.remove(backup_file)
            print("Plugin successfully updated!")

        else:
            print("Plugin already up-to-date.")


class PluginManager():
    "An interface to manage all plugins"

    def __init__(self):
        # ipdb.set_trace()
        gObj = FetchFromGitHub()
        mac = FetchFromWiki()
        try:
            self.totalPlugins = gObj.getPluginsList() + mac.getPluginsList()

            """The blacklisted plugins are those that can not be installed.
                And that do not contain code.
            """
            self.blacklisted_plugins_list = ["Macro BOLTS",
                                             "Macro PartsLibrary",
                                             "Macro FCGear",
                                             "Macro WorkFeatures"]

        except:
            print("Please check the connection!")
            exit()

    def allPlugins(self):
        "Returns all of the available plugins"
        # ipdb.set_trace()

        # Removes the blacklisted Plugins.
        for index, plugin in enumerate(self.totalPlugins):
            if plugin.name in self.blacklisted_plugins_list:
                del self.totalPlugins[index]

        # ipdb.set_trace()
        return self.totalPlugins

    def info(self, targetPlugin):
        "Get additional information about a plugin"
        # ipdb.set_trace()
        # import IPython; IPython.embed()

        if targetPlugin in self.totalPlugins:
            print("\nGetting information about", targetPlugin, "...")
            # ipdb.set_trace()
            pluginInfo = targetPlugin.fetch.getInfo(targetPlugin)
            return pluginInfo

    def isInstalled(self, targetPlugin):
        "Checks if the plugin is installed or not"
        if targetPlugin in self.totalPlugins:
            return targetPlugin.fetch.isInstalled(targetPlugin)

    def install(self, targetPlugin):
        "Install a plugin"
        if targetPlugin in self.totalPlugins:
            targetPlugin.fetch.install(targetPlugin)

    def isUpToDate(self, targetPlugin):
        "Checks if the plugin is up to date"
        if targetPlugin in self.totalPlugins:
            return targetPlugin.fetch.isUpToDate(targetPlugin)

    def uninstall(self, targetPlugin):
        "Uninstall a plugin"
        if targetPlugin in self.totalPlugins:
            targetPlugin.fetch.uninstall(targetPlugin)

    def update(self, targetPlugin):
        "Update a plugin"
        if targetPlugin in self.totalPlugins:
            targetPlugin.fetch.update(targetPlugin)
