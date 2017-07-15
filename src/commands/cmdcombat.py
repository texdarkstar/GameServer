from command import Command
from evennia.utils import inherits_from


class CmdCombat(Command):
    """Syntax: @combat <start/stop/join/leave/begin>
        This will start the combat handler in the current room (if start),
        end the combat handler script in the current room (if stop),
        join the combat in the room (if join),
        or leave the combat in the room (if leave).

        Only Wizards+ and gms and use 'start', 'stop', and 'begin',
        Anyone can use 'join', and 'leave', however.
    """
    key = "@combat"
    aliases = ["combat"]
    locks = "cmd:all()"
    help_category = "Gaming"


    def func(self):
        arg = self.args.strip().lower()
        room = self.caller.location

        if not arg:
            self.caller.msg("Syntax: @combat <start/stop/join/leave")
            return

        elif arg == "start" and (self.caller.check_permstring("Wizards") or self.caller.db.gm):
            scripts = room.scripts.all()
            for script in scripts:
                if inherits_from(script, "typeclasses.combathandler.CombatHandler"):
                    self.caller.msg("Combat is already started!")
                    return

            room.msg_contents("{who} starts a combat.".format(who=self.caller.key))
            room.scripts.add("typeclasses.combathandler.CombatHandler")
            return


        elif arg == "stop" and (self.caller.check_permstring("Wizards") or self.caller.db.gm):
            retcode = room.scripts.stop("typeclasses.combathandler.CombatHandler")

            if retcode == 0:
                self.caller.msg("There isn't a combat to stop!")
            else:
                room.msg_contents("{who} stops the combat.".format(who=self.caller.key))

            return


        elif arg == "join":
            scripts = room.scripts.all()
            for script in scripts:
                if inherits_from(script, "typeclasses.combathandler.CombatHandler"):
                    break

            try:
                script.add_character(self.caller)
            except KeyError:
                self.caller.msg("You are already in the comabat!")
                return
            except UnboundLocalError:
                self.caller.msg("There isn't a combat running!")
                return

            self.caller.msg("Okay, joined the combat.")
            room.msg_contents("{who} joined the combat.".format(who=self.caller.key), exclude=self.caller)

        elif arg == "leave":
            scripts = room.scripts.all()
            for script in scripts:
                if inherits_from(script, "typeclasses.combathandler.CombatHandler"):
                    break

            try:
                script.rem_character(self.caller)
            except KeyError:
                self.caller.msg("You aren't in the combat!")
                return
            except UnboundLocalError:
                self.caller.msg("There isn't a combat running!")
                return

            self.caller.msg("Okay, left the combat.")
            room.msg_contents("{who} left the combat.".format(who=self.caller.key), exclude=self.caller)

        elif arg == "begin" and (self.caller.check_permstring("Wizards") or self.caller.db.gm):
            scripts = room.scripts.all()
            for script in scripts:
                if inherits_from(script, "typeclasses.combathandler.CombatHandler"):
                    break

            try:
                if script.is_active:
                    self.caller.msg("Combat is already running!")
                    return
                script.start()
            except UnboundLocalError:
                self.caller.msg("There isn't a combat to begin!")
                return

            self.caller.msg("Okay, began the combat.")
            room.msg_contents("{who} begins the combat.".format(who=self.caller.key))

        else:
            self.caller.msg("Unknown argument '{arg}'.".format(arg=arg))
            return
