from command import Command


class CmdSign(Command):
    """Syntax: sign <thing> <message>
        This lets you affix a simple message to a thing, likely the table in the Game Room.

        Sign away!
    """
    key = "sign"
    lock_string = "cmd:all()"
    help_category = "Gaming"


    def func(self):
        args = self.args.strip().split()

        try:
            thing = args.pop(0)
            message = ' '.join(args)
        except IndexError:
            self.caller.msg("Syntax: sign <thing> <message>")
            return

        if not message:
            self.caller.msg("What do you want to sign with?")
            return

        obj = self.caller.search(thing)

        if not obj:
            self.caller.msg("You can't find anything like that.")
            return

        if not obj.db.signable:
            self.caller.msg("You can't sign that!")
            return


        self.caller.msg("You sign |C{thing}|n with '{message}'.".format(thing=obj.name, message=message))
        obj.db.desc += '\n    ' + message
