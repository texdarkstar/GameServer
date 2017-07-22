from command import Command
from typeclasses.characters import Character


class CmdMsp(Command):
    """Syntax: msp <sound file>
        This command will send a MSP signal to all connected clients that support it.
        This is used for GM sound effects primarily. This assumes the client also has
        the MSP plugin installed, with the sound files in the '/mushclient/gameserver/sounds' folder."""
    key = "msp"
    aliases = []
    locks = "cmd:pperm(Wizards) or attr(gm, True)"
    help_category = "General"


    def func(self):
        sound = self.args.strip().lower()

        if not sound:
            self.caller.msg("Syntax: msp <sound file>")
            return

        chars = [char for char in Character.objects.all() if char.player]

        self.caller.msg("Okay, played {sound}.".format(sound=sound))

        for char in chars:
            try:
                if char.player.sessions.get()[-1].protocol_flags["MSP"] == True:
                    char.msg("!!SOUND({sound})".format(sound=sound))
            except KeyError:
                pass

