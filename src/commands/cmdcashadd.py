from evennia.utils import evtable, utils
from command import Command


class CmdCashadd(Command):
    """Syntax: cashadd <amount> <item>
        This allows you to keep financial logs."""
    key = "cashadd"
    aliases = ["ca"]
    locks = "cmd:all()"
    help_category = "Gaming"


    def func(self):
        try:
            args = self.args.strip().split()
            amount = args.pop(0)
            amount = int(amount.split(".")[0])
            item = ' '.join(args)

        except (ValueError, IndexError):
            self.caller.msg("Syntax: cashadd <amount> <item>")
            return

        data = []

        if self.caller.db.cashlog:
            data = self.caller.db.cashlog

        table = evtable.EvTable(
            "|wID|n",
            "|wDate|n",
            "|wAmount|n",
            "|wBalance|n",
            "|wWhat|n",
        )

        obj = self.caller.search("#2", global_search=True)
        day = str(obj.db.date_day)
        year = str(obj.db.date_year)

        if len(day) < 3:
            while len(day) < 3:
                day = "0" + day

        if len(year) < 4:
            while len(year) < 4:
                year = "0" + year

        date = day + "-" + year + " IC"

        balance = self.caller.db.credit + amount
        self.caller.db.credit = balance

        data.append([str(self.caller.db.cashlog_id), date, str(amount), str(balance), item])
        self.caller.db.cashlog_id += 1


        # for entry in data:
            # table.add_row(
                # utils.crop(entry[0], 3),
                # utils.crop(entry[1], 12),
                # utils.crop(entry[2], 20),
                # utils.crop(entry[3], 20),
                # utils.crop(entry[4], 50),
                # )

        self.caller.db.cashlog = data
        self.caller.execute_cmd("cashlog", self.caller.player.sessions.get()[0])
        # self.caller.msg(table)
