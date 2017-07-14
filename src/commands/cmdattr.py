from command import Command


class CmdAttr(Command):
    """Syntax: @attr <target> <attr> <value>
    This command is used for setting a characters attribute scores.

    With just target as an argument, this will show you the targets scores.

    Available attributes:
        (str)ength
        (dex)terity
        (end)urance
        (int)elligence
        (edu)cation
        (soc)ial Standing

    Note, an attribute score has a min cap of 1, and a max cap of 15.
    """
    key = "@attr"
    aliases = ["attr", "@setattr", "setattr"]
    locks = "cmd:perm(Wizards) or attr(gm, True)"
    category = "Gaming"


    def func(self):
        args = self.args.strip().split()
        who = attr = value = None

        if len(args) == 1:
            who = str(args[0])

        elif len(args) == 3:
            who, attr, value = args
            attr = attr.lower()

            try:
                value = int(value)
                if value <= 0:
                    raise ValueError()
            except ValueError:
                self.caller.msg("Value must be a positive integer greater than zero.")
                return

            if attr not in ["str", "dex", "end", "int", "edu", "soc"]:
                self.caller.msg("Invalid attribute '{attr}'.".format(attr=attr))
                return
                # self.caller.msg("Syntax: @attr <target> <attr> <value>\n        @attr <target>")

        else:
            self.caller.msg("Syntax: @attr <target> <attr> <value>\n        @attr <target>")
            return


        target = self.caller.search(who, global_search=True)

        if target and (attr != None) and (value != None):
            target.db.attrs[attr]["base"] = value
            target.db.attrs[attr]["current"] = target.db.attrs[attr]["base"]

            self.caller.msg("Okay, set |c{target}|n's |c{attr}|n to |c{value}|n.".format(target=target.key, attr=attr, value=value))
            target.msg("|c{caller}|n set your |c{attr}|n to |c{value}|n.".format(caller=self.caller.key, attr=attr, value=value))
            return

        elif target:
            string = "{target}'s attribute score:\n".format(target=target.key)

            for attr in target.db.attrs.keys():
                string += "{attr}: {current}/{max}\n".format(attr=attr, current=target.db.attrs[attr]['current'], max=target.db.attrs[attr]['base'])

            self.caller.msg(string)


