from evennia.commands.default.unloggedin import CmdUnconnectedConnect
from cmdhelp import CmdHelp
from cmdinventory import CmdInventory
from cmdwho import CmdWho
from cmdoption import CmdOption


class CmdUnconnectedConnect(CmdUnconnectedConnect):
    key = "load"
    aliases = ["connect", "conn", "con", "co"]


