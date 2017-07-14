from command import Command


class CmdSheet(Command):
    """Syntax: sheet <skills/score>
        Shows you sections of your sheet.
        Default with no arguments is score."""
    key = "sheet"
    aliases = []
    locks = "cmd:all()"
    help_category = "Gaming"


    def func(self):
        arg = self.args.strip().lower()
        if not arg:
            arg = "score"

        arg = arg.split()[0]

        string = ""

        if arg == "score":
            # string 
            for attr in self.caller.db.attrs.keys():
                string += "{attr}: |c{current}|n/|c{max}|n\n".format(attr=attr, current=self.caller.db.attrs[attr]['current'], max=self.caller.db.attrs[attr]['base'])
 
            self.caller.msg(string)


        elif arg == "skills":
            for skill in self.caller.db.skills.keys():
                string += "{skill}: |c{rank}|n\n".format(skill=skill, rank=self.caller.db.skills[skill])

            if string:
                self.caller.msg(string)
            elif not string:
                self.caller.msg("No skills currently set.")

        else:
            self.caller.msg("Unknown field '%s'." % arg)
