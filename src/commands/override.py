from evennia.commands.default.unloggedin import CmdUnconnectedConnect
from evennia.commands.default.general import CmdInventory
from evennia.utils import evtable
from evennia import utils


class CmdUnconnectedConnect(CmdUnconnectedConnect):
    key = "load"
    aliases = ["connect", "conn", "con", "co"]


class CmdInventory(CmdInventory):
    def func(self):
        """check inventory"""
        items = self.caller.contents
        if not items:
            string = "You are not carrying anything."
        else:
            table = evtable.EvTable(border="header")
            for item in items:
                if utils.inherits_from(item, "typeclasses.armor.Armor"):
                    table.add_row("|C%s|n" % item.name, "(|gequipped|n)" if (item.dbref == self.caller.db.armor) else "")
                elif utils.inherits_from(item, "typeclasses.weapon.Weapon"):
                    table.add_row("|C%s|n" % item.name, "(|gequipped|n)" if (item.dbref == self.caller.db.weapon)  else "")
            string = "|wYou are carrying:\n%s" % table
        self.caller.msg(string)
