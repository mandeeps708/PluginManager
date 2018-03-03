#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

* File Name : ui.py

* Purpose : User-Interface for Plugin Installer

* Creation Date : 14-06-2017

* Copyright (c) 2017 Mandeep Singh <mandeeps708@gmail.com>

"""

from __future__ import print_function
from PySide import QtGui
from PySide import QtCore
from PySide import QtUiTools
from pluginManager import PluginManager
# import ipdb
import threading


class MyWidget(QtGui.QMainWindow):
    """PluginManager User Interface."""
    def __init__(self):
        """Signals & slots"""
        apply(QtGui.QMainWindow.__init__, (self,))

        # Loading Qt Designer UI file.
        loader = QtUiTools.QUiLoader()
        qt_file = QtCore.QFile("interface.ui")
        qt_file.open(QtCore.QFile.ReadOnly)
        self.myWidget = loader.load(qt_file, self)
        qt_file.close()
        self.setCentralWidget(self.myWidget)

        self.myWidget.textview.setPlainText("Welcome to the Plugin Manager. \
                                            \n Please wait while it loads Plugins...")
        """
        self.progressBar = self.myWidget.progressBar
        self.progressBar.setValue(0)
        self.progressBar.hide()
        self.statusLabel = self.myWidget.statusLabel
        self.statusLabel.setText("Status:")
        """
        # Start fetching things via new thread.
        t = threading.Thread(target=self.starter, name='starter')
        t.start()
        # Print info on each click on a Plugin.
        QtCore.QObject.connect(self.myWidget.pluginlist,
                               QtCore.SIGNAL("currentRowChanged(int)"),
                               self.print_current)
        # Call install function when Install button is clicked.
        QtCore.QObject.connect(self.myWidget.install_bt,
                               QtCore.SIGNAL("clicked()"), self.installPlugin)
        # Call Uninstall function when Uninstall button is clicked.
        QtCore.QObject.connect(self.myWidget.uninstall_bt,
                               QtCore.SIGNAL("clicked()"), self.uninstallPlugin)
        # Close the program.
        QtCore.QObject.connect(self.myWidget.exit_bt,
                               QtCore.SIGNAL("clicked()"), self.close)

    def starter(self):
        """To be initialized after basic UI has loaded."""
        # Load plugin manager & fetch plugins.
        self.pm = PluginManager()
        self.plugins = self.pm.allPlugins()
        self.display(self.plugins)

    def print_current(self):
        """Print info about currently selected plugin into the GUI."""
        current_plugin = self.myWidget.pluginlist.currentRow()
        # ipdb.set_trace()
        # print(current_plugin, self.myWidget.pluginlist.currentItem.text())
        info = self.pm.info(self.plugins[current_plugin])

        # When the plugin doesn't have a description (especially GitHub ones).
        if not info.description:
            # set default to empty.
            info.description = ''

        text = "Name: " + str(info.name) + "\n" + \
            "Author: " + str(info.author) + "\n" + \
            "Description: " + info.description + "\n" \
            "Plugin Type: " + str(info.plugin_type) + "\n" + \
            "URL: " + str(info.baseurl)
        self.myWidget.textview.setPlainText(text)

    def installPlugin(self):
        """Install the currently selected plugin."""
        current_plugin_no = self.myWidget.pluginlist.currentRow()
        current_plugin = self.plugins[current_plugin_no]
        # print(current_plugin, self.myWidget.pluginlist.currentItem.text())
        # self.pm.install(current_plugin)
        install_thread = threading.Thread(target=self.pm.install,
                                          name='install',
                                          args=(current_plugin,))
        install_thread.start()

    def uninstallPlugin(self):
        """Uninstalls the currently uninstalled plugin."""
        current_plugin_no = self.myWidget.pluginlist.currentRow()
        current_plugin = self.plugins[current_plugin_no]
        # self.pm.uninstall(self.plugins[current_plugin])
        # self.pm.uninstall(current_plugin)
        uninstall_thread = threading.Thread(target=self.pm.uninstall,
                                            name='uninstall',
                                            args=(current_plugin,))
        uninstall_thread.start()

    def display(self, plugins):
        """Add plugins to the list widget."""
        # Converting to a list of strings.
        data1 = [str(i) for i in plugins]
        # Using QListWidget
        # Add plugins one by one into the QListWidget "pluginlist".
        for i, plugin_name in enumerate(data1):
            self.myWidget.pluginlist.addItem(plugin_name)

        print(self.myWidget.pluginlist.currentRow())

if __name__ == '__main__':
    import sys
    import os
    print("Running in " + os.getcwd() + " .\n")
    app = QtGui.QApplication(sys.argv)

    win = MyWidget()
    win.show()

    app.connect(app, QtCore.SIGNAL("lastWindowClosed()"), app,
                QtCore.SLOT("quit()"))
    app.exec_()
