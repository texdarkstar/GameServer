from command import Command


class CmdSheet(Command):
    """Syntax: sheet <skills/score>
        Shows you sections of your sheet."""
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
                string += "{attr}: {current}/{max}\n".format(attr=attr, current=self.caller.db.attrs[attr]['current'], max=self.caller.db.attrs[attr]['base'])
 
            self.caller.msg(string)


        elif arg == "skills":
            pass
