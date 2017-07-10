from evennia.utils import evtable, utils
from command import Command


class CmdCashlog(Command):
    """Syntax: cashlog
        This shows you your financial log."""
    key = "cashlog"
    aliases = ["cl"]
    locks = "cmd:all()"
    help_category = "Gaming"


    def func(self):
        data = []

        if self.caller.db.cashlog is not None:
            data = self.caller.db.cashlog

        table = evtable.EvTable(
            "|wID|n",
            "|wDate|n",
            "|wAmount|n",
            "|wBalance|n",
            "|wWhat|n",
        )

        for entry in data:
            table.add_row(
                utils.crop(entry[0], 3),
                utils.crop(entry[1], 12),
                utils.crop(entry[2], 20),
                utils.crop(entry[3], 20),
                utils.crop(entry[4], 50),
                )

        self.caller.msg(table)
        self.caller.msg("You currently have %d credit%s." % (self.caller.db.credit, "s" if (self.caller.db.credit > 1 or self.caller.db.credit < 0) else ""))
