#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

* File Name : getPlugins.py

* Purpose : get all plugins.

* Creation Date : 20-06-2016

* Copyright (c) 2016 Mandeep Singh <mandeeps708@gmail.com>

"""

from __future__ import print_function
import main
# import ipdb

obj = main.getAllPlugins()
plugins = obj.allPlugins()
# ipdb.set_trace()
obj.info(plugins[2])

# obj.install(plugins[0])
# obj.info("animation")
# obj.info("workfeature")
# obj.info("Macro Rectellipse")

"""
for index, plugin in enumerate(plugins):
    print(index, plugin.name)
    print(plugin.baseurl)
"""

# plugins[0]
# ipdb.set_trace()
