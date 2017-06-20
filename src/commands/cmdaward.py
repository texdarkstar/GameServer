from command import Command


class CmdAward(Command):
    """Syntax: @award <player> <boon/bane>
        Awards a player either a bane die or a boon die."""
    key = "@award"
    aliases = ["award"]

    locks = "cmd:perm(Wizards) or attr(GM, True)"
    help_category = "Gaming"


    def func(self):
        target, _type = self.args.strip().split()

        if target.lower() in ["me", "self"]:
            target = self.caller.name

        char = self.caller.search(target, global_search=True)
        error = False
        
        if _type.lower() == "boon" and char:
            char.db.boon_dice += 1
        elif _type.lower() == "bane" and char:
            char.db.bane_dice += 1
        else:
            error = True

        if not error:
            self.caller.msg("Okay, awarded |c{who}|n a |g{type}|n die.".format(who=self.caller.name, type=_type.lower()))
            char.msg("|c{who}|n awarded you a |g{type}|n die.".format(who=self.caller.name, type=_type.lower()))

        elif error:
            self.caller.msg("Syntax: {key} <player> <boon/bane>".format(key=self.key))


        return
