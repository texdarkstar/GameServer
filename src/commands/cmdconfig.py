from command import Command
from evennia.utils import utils, evtable


class CmdConfig(Command):
    """Syntax: @config
        @config <option>

        This command, without args, will show you a table of your current configuration.
        These are stored on your Player, so it is global across your account.
    """
    key = "@config"
    aliases = ["config", "conf"]
    locks = "cmd:all()"
    help_category = "General"


    def func(self):
        args = self.args.strip().lower()
        table = None
        string = ""
        player = self.caller.player

        if not args:  # display our current configuration with EvTable
            table = evtable.EvTable(
                "|woption|n",
                "|wvalue|n",
                )

            for key in player.db.config:
                value = str(self.player.db.config[key])
                table.add_row("|w" + key + "|n", "|w" + value + "|n")

            string += str(table)
            string += "\nUse config <option> to toggle."

            self.caller.msg(string)
            return

        elif args:  # the user wants to toggle something
            try:
                player.db.config[args] = not player.db.config[args]
                self.caller.msg("Okay, toggled |c" + args + "|n to |c" + str(player.db.config[args]) + "|n.")

            except KeyError:  # the option to toggle doesn't exist
                self.caller.msg("Config option '%s' doesn't exist!" % args)
                return
