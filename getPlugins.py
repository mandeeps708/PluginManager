#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

* File Name : getPlugins.py

* Purpose : get all plugins.

* Creation Date : 20-06-2016

* Copyright (c) 2016 Mandeep Singh <mandeeps708@gmail.com>

"""

from __future__ import print_function
import pluginManager
# import ipdb

obj = pluginManager.PluginManager()
plugins = obj.allPlugins()

# Getting a list of all Plugins.
for index, plugin in enumerate(plugins):
    print("\n===========")
    print(index, plugin.name)
    # obj.info(plugin)
    if plugin.plugin_type == "Macro":
        obj.install(plugin)
"""
# ipdb.set_trace()
obj.info(plugins[2])
obj.info(plugins[7])
obj.info(plugins[0])
obj.info(plugins[24])
obj.install(plugins[21])
obj.install(plugins[2])
"""
# obj.install(plugins[0])
