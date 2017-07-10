from evennia.utils import evtable, utils
from command import Command


class CmdCashrem(Command):
    """Syntax: cashrem <ID>
        This removes an entry from your financial logs."""
    key = "cashrem"
    aliases = ["cr"]
    locks = "cmd:all()"
    help_category = "Gaming"


    def func(self):
        data = []

        if self.caller.db.cashlog:
            data = self.caller.db.cashlog

        try:
            id = self.args.strip()
            id = int(id)
            if id <= 0:
                raise ValueError
        except ValueError:
            self.caller.msg("Syntax: cashrem <ID>")
            return

        table = evtable.EvTable(
            "|wID|n",
            "|wDate|n",
            "|wAmount|n",
            "|wBalance|n",
            "|wWhat|n",
        )
        found = False

        for entry in data:
            if entry[0] == str(id):
                data.remove(entry)
                self.caller.db.credit -= int(entry[2])
                found = True
                break

        if not found:
            self.caller.msg("Cashlog entry with ID |w" + str(id) + "|n was not found.")

        # for entry in data:
            # table.add_row(
                # utils.crop(entry[0], 3),
                # utils.crop(entry[1], 12),
                # utils.crop(entry[2], 20),
                # utils.crop(entry[3], 20),
                # utils.crop(entry[4], 50),
                # )

        self.caller.db.cashlog = data
        self.caller.msg("Okay, removed cashlog entry with ID |w" + str(id) + "|n.")
        self.caller.execute_cmd("cashlog", self.caller.player.sessions.get()[0])
        # self.caller.msg(table)
