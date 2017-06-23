from __future__ import print_function
from PySide import QtGui
from PySide import QtCore
from PySide import QtUiTools
from pluginManager import PluginManager


class MyWidget(QtGui.QMainWindow):
    """PluginManager User Interface."""
    def __init__(self):
        apply(QtGui.QMainWindow.__init__, (self,))

        # Loading Qt Designer UI file.
        loader = QtUiTools.QUiLoader()
        qt_file = QtCore.QFile("interface.ui")
        qt_file.open(QtCore.QFile.ReadOnly)
        self.myWidget = loader.load(qt_file, self)
        qt_file.close()

        self.setCentralWidget(self.myWidget)
        # QtCore.QObject.connect(self.myWidget.calculateButton,
        #                        QtCore.SIGNAL("clicked()"), self.accept)

        # Load plugin list after clicking on "Start". To be automated later.
        QtCore.QObject.connect(self.myWidget.start_bt,
                               QtCore.SIGNAL("clicked()"), self.starter)

    def starter(self):
        """To be initialized after basic UI has loaded."""
        # Load plugin manager & fetch plugins.
        instance = PluginManager()
        plugins = instance.allPlugins()
        self.accept(plugins)

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
