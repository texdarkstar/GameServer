import re
from command import Command
from random import randint


class CmdRoll(Command):
    """Syntax: roll <number>d<sides> <+\-> <dm>
        
        This command generates a random number, by rolling <number> of dice each
        with <sides> number of sides, plus or minus <dm>, depending on the third arg.
        Can also just roll <number>D<sides> with no dms.
    """
    key = "roll"
    aliases = ["rol"]
    locks = "cmd:all()"
    help_category = "Gaming"


    def func(self):
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

        dice = '%s' % ' + '.join(rolls)
        strdm = ''

        if dm > 0:
            strdm = ' + dm[%d]' % dm

        if dm == 0:
            strdm = ''

        if dm < 0:
            strdm = ' - dm[%d]' % abs(dm)

        crit = ''

        if result - dm == number:
            crit = " (snake eyes!)"

        elif result - dm == number * sides:
            crit = " (box cars!)"

        self.caller.msg("Your result is {result}: dice[{dice}]{dm}{crit}".format(result=result, dice=dice, dm=strdm, crit=crit))

