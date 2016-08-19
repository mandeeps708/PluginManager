# PluginManager
A Plugin Manager for FreeCAD. 

## Concept
There are mainly two ways to add functionality to FreeCAD (for user's ease).

1. Workbenches
2. Macros

Let's consider both these as Plugins. The Workbenches are stored at a
GitHub repository as submodules. While the macros are currently being stored
at the FreeCAD Wiki. So, finding and installing can certainly be a non-obvious
thing. That's when this Plugin Manager comes into play!

Read more about what are Workbenches and Macros here [Link to be added].

## Present Scenario
Currently, the PluginManager is command-line only. No GUI; but it's the very
next thing that is to be done.

### What works?
The following is the list of what's currently working in this Plugin Manager.

- **Get Plugins List** : Get list of Plugins that are available to be
installed. Each Plugin within the list will have Plugin name, URL and its type.
- **Get Additional Info** : Get additional information about a Plugin. It will
give additional information like Plugin Author, Description of what it does and
version (in case of Macro).
- **Plugin Installed or not** : Check if a Plugin is currently installed on the
system or not.
- **Install a Plugin** : If not currently installed, then a Plugin can be
easily installed.
- **Plugin up-to-date** : Check if an installed Plugin is up-to-date. Is there
any newer version available of that Plugin?
- **Update a Plugin** : If a Plugin is having a newer version available, then
it can be updated to that newer version.
- **Uninstall a Plugin** : Don't need a Plugin anymore? No problem, one can
very easily uninstall it.
- **API** : There is an API providing to use the above features with ease. Just
import the PluginManager and start calling the methods.

## What's next?
- **No GUI** : Currently, there is no GUI for this PluginManager. It's
one of the tasks with highest priority (bounty).
- **Highly unstable :D** : Needs testing under different situations. Test and
if a bug is found, report it at https://github.com/mandeeps708/PluginManager/issues
with adequate information.


## Installation
###  Pre-requisites
- Beautiful Soup ($ `pip install bs4`)
- Requests ($ `pip install requests`)
- PyGithub ($ `pip install pygithub`)
- GitPython ($ `pip install gitpython`)

###  Some other dependencies
These ones are pre-installed on most of the systems.
- os, re, socket, FreeCAD, shutil, glob

### Guide to import FreeCAD:
https://mandeep7.wordpress.com/2016/07/23/import-freecad-in-python/

## How to use?

### Through Python

Just see the example usage in the file getPlugins.py in this repository
(directory).
- Import the pluginManager.
- Create an instance of the PluginManager() class (API).
- Use that instance to access methods (features) via the API.

#### Execution
After you are done with what you want the PluginManager to do for you, just
fire the following command from the console to execute and see it in action.

$ `python getPlugins.py`
