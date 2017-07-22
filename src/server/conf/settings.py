"""
Evennia settings file.

The available options are found in the default settings file found
here:

c:\mud\evennia\evennia\settings_default.py

Remember:

Don't copy more from the default file than you actually intend to
change; this will make sure that you don't overload upstream updates
unnecessarily.

When changing a setting requiring a file system path (like
path/to/actual/file.py), use GAME_DIR and EVENNIA_DIR to reference
your game folder and the Evennia library folders respectively. Python
paths (path.to.module) should be given relative to the game's root
folder (typeclasses.foo) whereas paths within the Evennia library
needs to be given explicitly (evennia.foo).

"""

# Use the defaults from Evennia unless explicitly overridden
from evennia.settings_default import *
import os

######################################################################
# Evennia base server config
######################################################################

# This is the name of your game. Make it catchy!
SERVERNAME = "GameServer"
TELNET_PORTS = [5331]
WEBSERVER_PORTS = [(80, 5001)]
WEBCLIENT_ENABLED = False  # for now
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# SEARCH_MULTIMATCH_REGEX = r"(?P<number>[0-9]+)-(?P<name>.*)"
# SEARCH_MULTIMATCH_TEMPLATE = " {name}{aliases}{info}-{number}\n"
IN_GAME_ERRORS = False
COMMAND_PARSER = "commands.cmdparser.cmdparser"
COMMAND_DEFAULT_CLASS = "commands.command.MuxCommand"
TELNET_OOB_ENABLED = True

MULTISESSION_MODE = 2
MAX_NR_CHARACTERS = 25

DEFAULT_CHANNELS = [
                  # public channel
                  {"key": "Chat",
                  "aliases": ('.', 'ooc'),
                  "desc": "Public discussion",
                  "locks": "control:perm(Wizards);listen:all();send:all()"},
                  # connection/mud info
                  {"key": "System",
                   "aliases": "",
                   "desc": "Connection log",
                   "locks": "control:perm(Immortals);listen:perm(Wizards);send:false()"}
                  ]


######################################################################
# Django web features
######################################################################
# Web configuration
INSTALLED_APPS += (
        "web.help_system",
)
INSTALLED_APPS += (
        "web.client_index",
)
INSTALLED_APPS += (
        "web.plugin_index",
)

# The secret key is randomly seeded upon creation. It is used to sign
# Django's cookies. Do not share this with anyone. Changing it will
# log out all active web browsing sessions. Game web client sessions
# may survive.
SECRET_KEY = 'ergQzy-t$4U(|vxPh!<DST_ckmZ=G&"Yo+C.FRn/'
DEBUG = False