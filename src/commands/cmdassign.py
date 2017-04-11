from command import Command
from world.xmlparser import XMLParser


class CmdAssign(Command):
    """Syntax: @assign <player> <path\\to\\sheet>
        Assigns an XML character sheet to a player.
    """
    key = "@assign"
    aliases = ["assign", "ass"]
    locks = "cmd:perm(Wizard) or attr(GM, True)"
    help_category = "Gaming"


    def func(self):
        try:
            player, sheet = self.args.strip().lower().split()
        except ValueError:
            self.caller.msg("Syntax: @assign <player> <path\\to\\sheet>")
            return

        # file = open("world\\sheets\\")
