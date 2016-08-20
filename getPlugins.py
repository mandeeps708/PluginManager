#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

* File Name : getPlugins.py

* Purpose : Example usage of the pluginManager.

* Creation Date : 20-06-2016

* Copyright (c) 2016 Mandeep Singh <mandeeps708@gmail.com>

"""

from __future__ import print_function
from pluginManager import PluginManager
# import ipdb

# May also do:
# import pluginManager
# pm = pluginManager.PluginManager()

""" This is an example file to use the pluginManager.py. It have some lines
as comments and their respective description. Uncomment a line to see it in
action. For example, uncomment the line 50 i.e. "# pm.install(plugin)" to
install the plugin.
"""

# Creating instance of PluginManager class.
pm = PluginManager()
# Get all Plugins in form of a list.
# Access individual all_plugins as all_plugins[1]
all_plugins = pm.allPlugins()

# Print a list and the respecive indices of all Plugins by iterating over it.
for index, plugin in enumerate(all_plugins):
    print("\n===========")
    print(index, plugin.name)

# Select a particular plugin. Let's say a Macro.
plugin = all_plugins[23]

# Get additional information about this plugin.
pm.info(plugin)

# Check if the plugin is installed or not.
print("\nChecking if the plugin is installed: ")
pm.isInstalled(plugin)

# Install a plugin.
# pm.install(plugin)

# Check if the plugin is up-to-date (latest version available).
# pm.isUpToDate(plugin)

# Update a plugin.
# pm.update(plugin)

# Uninstall a plugin.
# pm.uninstall(plugin)
