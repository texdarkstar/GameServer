from command import Command
from evennia.utils import inherits_from


class CmdDone(Command):
    """Syntax: @done
        This command will end your turn with the current combat handler, and proceed to the next."""
    key = "@done"
    aliases = ["done"]
    locks = "cmd:all()"
    help_category = "Gaming"


    def func(self):
        room = self.caller.location
        scripts = room.scripts.all()
        for script in scripts:
            if inherits_from(script, "typeclasses.combathandler.CombatHandler"):
                break

        try:
            if (script.db.turn_player == self.caller.key) and script.db.running:
                script.unpause()
                self.caller.msg("Okay, you are done with your turn.")
                for name in [key for key in script.db.characters.keys() if key != self.caller.key]:
                    char = self.caller.search(name, global_search=True)
                    char.msg("%s's turn is over." % self.caller.key)

                return
            elif (script.db.turn_player != self.caller.key) and (script.db.running):
                self.caller.msg("It isn't your turn!")
                return
            elif not script.db.running:
                self.caller.msg("The combat has yet to begin.")
                return
        except UnboundLocalError:
            self.caller.msg("You aren't in a combat.")
            return

