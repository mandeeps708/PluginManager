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

        # Start PluginManager
        self.starter()

        # QtCore.QObject.connect(self.myWidget.calculateButton,
        #                        QtCore.SIGNAL("clicked()"), self.accept)

        # Load plugin list after clicking on "Start". To be automated later.
        # QtCore.QObject.connect(self.myWidget.start_bt,
        #                        QtCore.SIGNAL("clicked()"), self.starter)
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
        self.accept(self.plugins)

    def print_current(self):
        """Print info about currently selected plugin."""
        current_plugin = self.myWidget.pluginlist.currentRow()
        # print(current_plugin, self.myWidget.pluginlist.currentItem.text())
        self.pm.info(self.plugins[current_plugin])

    def installPlugin(self):
        """Install the currently selected plugin."""
        current_plugin = self.myWidget.pluginlist.currentRow()
        # print(current_plugin, self.myWidget.pluginlist.currentItem.text())
        self.pm.install(self.plugins[current_plugin])

    def uninstallPlugin(self):
        """Uninstalls the currently uninstalled plugin."""
        current_plugin = self.myWidget.pluginlist.currentRow()
        self.pm.uninstall(self.plugins[current_plugin])

    def accept(self, plugins):
        """Add plugins to the list widget."""
        # data1 = ['a1', 'a2', 'a3', 'a4']
        # data2 = ['b1', 'b2', 'b3', 'b4']
        # Converting to a list of strings.
        data1 = [str(i) for i in plugins]
        """
        # Using QTableWidget
        self.myWidget.tablu.insertRow(i)
        item = QtGui.QTableWidgetItem(data1[i])
        self.myWidget.tablu.setItem(i, 0, item)
        # item2 = QtGui.QTableWidgetItem(data2[i])
        # self.myWidget.tablu.setItem(i, 1, item2)
        """
        # Using QListWidget
        # Add plugins one by one into the QListWidget "pluginlist".
        # for i in range(len(data1)):
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
