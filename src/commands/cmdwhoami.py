from command import Command


class CmdWhoami(Command):
    """Syntax: @whoami
        This command shows you your player name, and the name of the character you are playing.

        Note: Your prompt can be configured to display this information automatically.
    """
    key = "@whoami"
    aliases = ["whoami"]
    locks = "cmd:all()"
    help_category = "General"


    def func(self):
        character = ""
        if self.player.character:
            character = self.caller.key

        string = "You are Player |c{player}|n, and you are playing : |c{character}|n.".format(player=self.player.key, character=character or "No one")
        self.msg(string)

