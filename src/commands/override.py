from evennia.commands.default.unloggedin import CmdUnconnectedConnect
from cmdhelp import CmdHelp
from cmdinventory import CmdInventory


class CmdUnconnectedConnect(CmdUnconnectedConnect):
    key = "load"
    aliases = ["connect", "conn", "con", "co"]


