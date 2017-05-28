from command import Command


class CmdEcho(Command):
    """Syntax: echo <text>
        Echos some text back to you."""
    key = "echo"
    aliases = ["display"]
    locks = "cmd:all()"
    help_category = "General"


    def func(self):
        if text:
            text = self.args.strip()
            self.caller.msg(text)
            return

        elif not text:
            self.caller.msg("Syntax: echo <text>")
            return

        return
