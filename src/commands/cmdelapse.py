from command import Command
from typeclasses.characters import Character


class CmdElapse(Command):
    """Syntax: @elapse <days>
                @elapse reset
        This command will make time pass. Days must be an integer, and between 36000 and 1
        "@elapse reset" will reset the date to "001-1105"."""
    key = "@elapse"
    aliases = ["elapse"]
    locks = "cmd:perm(Wizards) or attr(gm, True)"
    help_category = "Gaming"


    def func(self):
        obj = self.caller.search("#2", global_search=True)
        chars = [char for char in Character.objects.all() if char.player]
        days = 0

        try:
            days = int(self.args.strip())
            if days not in xrange(1, 36000 + 1):
                raise ValueError

        except ValueError:
            if self.args.strip().lower() == "reset":
                obj.db.date_day = 1
                obj.db.date_year = 1105
                self.caller.msg("Okay, time has been reset to |w001-1105 IC|n.")

                for char in chars:
                    # if char.key != self.caller.key:
                        char.msg("{name} reset the date to |w001-1105 IC|n.".format(name=self.caller.key))
                return

            self.caller.msg("Days must be an integer and between 36000 and 1.")
            return


        obj = self.caller.search("#2", global_search=True)

        obj.db.date_day += days

        if obj.db.date_day >= 360:
            while obj.db.date_day >= 360:
                obj.db.date_day -= 360
                obj.db.date_year += 1

        date = ""
        year = ""

        date += str(obj.db.date_day)

        if len(date) < 3:
            while len(date) < 3:
                date = "0" + date


        year = str(obj.db.date_year)

        if len(year) < 4:
            while len(year) < 4:
                year = "0" + year

        date = date + "-" + year + " IC"

        for char in chars:
            char.msg("Time passes. It is now |w" + str(date) + "|n.")

        return
