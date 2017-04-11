from evennia.commands.default.unloggedin import CmdUnconnectedConnect


class CmdUnconnectedConnect(CmdUnconnectedConnect):
    key = "load"
    aliases = ["connect", "conn", "con", "co"]

