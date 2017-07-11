from command import Command


class CmdHide(Command):
    """Syntax: @hide
        This command will hide you from players with commands like |wwho|n or |wlook|n.
    """
    key = "@hide"
    aliases = ["@wizinvis", "hide"]
    locks = "cmd:perm(Immortals)"
    help_category = "Admin"


    def func(self):
        self.caller.db.invisible = not self.caller.db.invisible
        self.caller.msg("Okay, you are |c%s|n." % ("now invisible" if self.caller.db.invisible else "not invisible"))
