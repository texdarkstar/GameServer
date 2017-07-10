import re
from command import Command
from random import randint
from typeclasses.characters import Character


class CmdRoll(Command):
    """Syntax: roll <number>d<sides> <+\-> <dm>

        This command generates a random number, by rolling <number> of dice each
        with <sides> number of sides, plus or minus <dm>, depending on the third arg.
        Can also just roll <number>D<sides> with no dms.
    """
    key = "roll"
    aliases = []
    locks = "cmd:all()"
    help_category = "Gaming"


    def func(self):
        chars = [char for char in Character.objects.all() if char.player]  # getting a list of all connected characters
        privy_chars = []

        for char in chars:
            if (char.player.check_permstring("Wizards") or char.db.gm):  # removing those that are not allowed to hear priviledged data
                privy_chars.append(char)


        # removing self.caller from both lists, he already gets the privy data when he rolls, regardless of perms
        for char in chars:
            if char.id == self.caller.id:
                chars.remove(char)

        for char in privy_chars:
            if char.id == self.caller.id:
                privy_chars.remove(char)


        args = self.args.strip().lower()

        args = args.replace(' ', '')

        m = re.match(r"^(\d+)d(\d+)(.*)", args)

        try:
            number, sides, args = m.groups()
        except AttributeError:
            self.caller.msg("Syntax: roll <number>d<sides> <+\-> <dm>")
            return

        dm = 0

        try:
            number = int(number)
        except ValueError:
            self.caller.msg("Number must be a integer.")
            return

        try:
            sides = int(sides)
        except ValueError:
            self.caller.msg("Sides must be a integer.")
            return

        if args:
            try:
                dm = int(args)
            except ValueError:
                self.caller.msg("Can't use a non integer as a dm.")
                return

        result = 0
        rolls = []

        for i in xrange(number):
            roll = randint(1, sides)
            rolls.append(str(roll))
            result += roll

        result += dm

        dice = '|c%s|n' % ' + '.join(rolls)
        strdm = ''

        if dm > 0:
            strdm = ' + dm[|c%d|n]' % dm

        if dm == 0:
            strdm = ''

        if dm < 0:
            strdm = ' - dm[|c%d|n]' % abs(dm)

        unprivy = "{who} rolled |c{number}d{sides}|n{dm}|n for a total of |c{result}|n".format(who=self.caller.key, number=str(number), sides=str(sides), dm=strdm, result=result)
        privy = "{who} rolled |c{number}d{sides}|n{dm}|n for a total of |c{result}|n: dice[{dice}] {dm}".format(who=self.caller.key, number=str(number), sides=str(sides), dm=strdm, result=result, dice=dice)

        for char in chars:
            char.msg(unprivy)

        for char in privy_chars:
            char.msg(privy)

        self.caller.msg(privy)
