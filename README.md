# PluginManager
A Plugin Manager for [FreeCAD](https://github.com/FreeCAD/FreeCAD).

Started as a Google Summer of Code ([GSoC](https://en.wikipedia.org/wiki/Google_Summer_of_Code) 2016) [project](https://summerofcode.withgoogle.com/projects/#5341872155262976) with proposal [here](http://brlcad.org/wiki/User:Mandeeps708/gsoc_proposal) and dev logs [here](http://brlcad.org/wiki/User:Mandeeps708/GSoC16/logs#Coding_Period).

## Concept
There are mainly two ways to add functionality to FreeCAD (for user's ease).

1. [Workbenches](http://www.freecadweb.org/wiki/index.php?title=Workbenches)
2. [Macros](http://www.freecadweb.org/wiki/index.php?title=Macros)

Let's consider both these as Plugins. The Workbenches are stored at a
GitHub repository as submodules. While the macros are currently being stored
at the FreeCAD Wiki. So, finding and installing can certainly be a non-obvious
thing. That's when this Plugin Manager comes into play!

Read more about what are  Workbenches and Macros [here](https://mandeep7.wordpress.com/2016/06/01/freecad-plugins).

## Present Scenario
Currently, the PluginManager is command-line only. No GUI; but it's the very
next thing that is to be done.

### What works?
The following is the list of what's currently working in this Plugin Manager.

- [x] **Get Plugins List** : Get list of Plugins that are available to be
installed. Each Plugin within the list will have Plugin name, URL and its type.
- [x] **Get Additional Info** : Get additional information about a Plugin. It will
give additional information like Plugin Author, Description of what it does and
version (in case of Macro).
- [x] **Plugin Installed or not** : Check if a Plugin is currently installed on the
system or not.
- [x] **Install a Plugin** : If not currently installed, then a Plugin can be
easily installed.
- [x] **Plugin up-to-date** : Check if an installed Plugin is up-to-date. Is there
any newer version available of that Plugin?
- [x] **Update a Plugin** : If a Plugin is having a newer version available, then
it can be updated to that newer version.
- [x] **Uninstall a Plugin** : Don't need a Plugin anymore? No problem, one can
very easily uninstall it.
- [x] **API** : There is an API providing to use the above features with ease. Just
import the PluginManager and start calling the methods.
- [x] **Basic GUI** : Basic GUI to browse, install/uninstall plugins.

## What's next?
- **Improve GUI** : GUI needs many improvements (mainly threading).
- **Highly unstable :D** : Needs testing under different situations. Test and
if a bug is found, report it at https://github.com/mandeeps708/PluginManager/issues
with adequate information.
- **Hybrid Macros** : There are some macros that are more than just one file.
For example: https://github.com/Rentlau/WorkFeature
They are being identified as a Workbench as it's on GitHub WB repo. But it
a macro to work. Hence it needed to be placed in the "Macro" folder instead of
"Mod". See [here](https://github.com/FreeCAD/FreeCAD-addons/blob/master/addons_installer.FCMacro#L313) to get hint on solving.
- **Fallback method** : Add a fallback method for working with GitHub plugins. There are license compatibility issues with distributing the git executable, hence we may consider the simple HTTP method for downloading the plugins or another alternative like dulwich and gittle.


## Installation
###  Pre-requisites
- Beautiful Soup ($ `pip install bs4`)
- Requests ($ `pip install requests`)
- PyGithub ($ `pip install pygithub`)
- GitPython ($ `pip install gitpython`)

**Note**: You must have `pip` installed to use above commands. On GNU/Linux, use
sudo to execute these (if you are not using `virtualenv`). Try to install these
packages using your OS's native package manager.
More on pip [here](https://packaging.python.org/installing).

###  Some other dependencies
These ones are pre-installed on most of the systems.
- os, re, socket, FreeCAD, shutil, glob

### Guide to import FreeCAD:
https://mandeep7.wordpress.com/2016/07/23/import-freecad-in-python/

## How to use?
Following is a quick guide on how to use the Plugin Manager.

### Through Python

Here is a basic example of using the Plugin Manager.

```python
from pluginManager import PluginManager
instance = PluginManager()            # creating instance of api class
all_plugins = instance.allPlugins()   # get all plugins (as a list)
instance.info(all_plugins[23])        # get info about a particular plugin
instance.install(all_plugins[23])     # install it
```
Hence, it's a 3-step process:

- Import the pluginManager.
- Create an instance of the PluginManager() class (API).
- Use that instance to access methods (features) via the API.

For more details and options about what else you can do with it, just see the example 
usage in the file [getPlugins.py](https://github.com/mandeeps708/PluginManager/blob/master/getPlugins.py)
in this repository/directory.

### GUI

As of now, to use GUI you need to run:  
`python ui.py`

#### Execution
After you are done with what you want the PluginManager to do for you, it just needs to
be executed. For example: fire the following command from the console to execute the
[getPlugins.py](https://github.com/mandeeps708/PluginManager/blob/master/getPlugins.py)
example and see it in action.

$ `python getPlugins.py`
