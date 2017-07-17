from command import Command
from evennia.utils import inherits_from, evtable


class CmdCombat(Command):
    """Syntax: @combat <start/stop/join/leave/begin>
        This will start the combat handler in the current room (if start),
        end the combat handler script in the current room (if stop),
        join the combat in the room (if join),
        or leave the combat in the room (if leave).

        If no args, then this will show you who all is in the current combat.

        Only Wizards+ and gms and use 'start', 'stop', and 'begin',
        Anyone can use 'join' and 'leave', however.
    """
    key = "@combat"
    aliases = ["combat"]
    locks = "cmd:all()"
    help_category = "Gaming"


    def func(self):
        arg = self.args.strip().lower()
        room = self.caller.location

        if not arg:
            # self.caller.msg("Syntax: @combat <start/stop/join/leave")
            scripts = room.scripts.all()
            for script in scripts:
                if inherits_from(script, "typeclasses.combathandler.CombatHandler"):
                    break

            try:
                if not script.is_active and not script.db.running:
                    characters = [char for char in script.db.characters.keys()]
                    string = "Currently in combat:\n"
                    if len(characters) > 0:
                        for char in characters:
                            string += "|_|_|_|_" + char + "\n"

                    elif len(characters) == 0:
                        string += "|_|_|_|_No one."

                    self.caller.msg(string)
                    return

                elif script.db.running:
                    table = evtable.EvTable("Who", "Inititive", "Turn Player")
                    characters = [char for char in script.db.characters.keys()]
                    for char in characters:
                        obj = self.caller.search(char, global_search=True)
                        table.add_row(
                            "|c" + char + "|n",
                            "|c" + str(script.db.inititive_board[char]) if not obj.db.hide_init else "|rXX"+ "|n",
                            "|rYes|n" if (obj.key == script.db.turn_player) else "|gNo|n",
                            )

                    self.caller.msg(table)
                    return

            except UnboundLocalError:
                self.caller.msg("There isn't a combat running!")
                return


        elif arg == "start" and (self.caller.check_permstring("Wizards") or self.caller.db.gm):
            scripts = room.scripts.all()
            for script in scripts:
                if inherits_from(script, "typeclasses.combathandler.CombatHandler"):
                    self.caller.msg("Combat is already started!")
                    return

            room.msg_contents("{who} starts a combat.".format(who=self.caller.key))
            room.scripts.add("typeclasses.combathandler.CombatHandler", autostart=False)
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

            room.msg_contents("{who} joined the combat.".format(who=self.caller.key))


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

            room.msg_contents("{who} left the combat.".format(who=self.caller.key))


        elif arg == "begin" and (self.caller.check_permstring("Wizards") or self.caller.db.gm):
            scripts = room.scripts.all()
            for script in scripts:
                if inherits_from(script, "typeclasses.combathandler.CombatHandler"):
                    break

            try:
                if script.is_active:
                    self.caller.msg("Combat is already running!")
                    return
                elif len(script.db.characters.keys()) < 2:
                    self.caller.msg("Need at least two characters to begin!")
                    return
            except UnboundLocalError:
                self.caller.msg("There isn't a combat to begin!")
                return

            room.msg_contents("{who} begins the combat.".format(who=self.caller.key))
            script.start()

        else:
            self.caller.msg("Unknown argument '{arg}'.".format(arg=arg))
            return
