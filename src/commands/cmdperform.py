import re
from command import Command
from random import randint as die
from world.tables import *


class CmdPerform(Command):
    """Syntax: perform <skill> + <attribute>
                perform <attribute>

        Rolls a skill + attribute, or just rolls an attribute.
        2D6 plus your specified skill rank + an attribute dm.

        Examples:
            perform str
            perform broker + int
            perform pilot(spacecraft) + dex
        """
    key = "perform"
    aliases = ["perf", "per"]
    locks = "cmd:all()"
    help_category = "Gaming"


    def func(self):
        args = self.args.strip().lower()
        attrdm = 0
        skillrank = 0
        dice = []
        pm = ""
        pm1 = ""
        pm2 = ""
        string = ""

        regexp1 = r"^(\w+)$"
        regexp2 = r"^(.+) +?\+ +?(\w+)$"


        if re.match(regexp1, args):  # checking for something like 'perform str'
            m = re.match(regexp1, args)
            string = "You rolled a |c{result}|n: dice rolled[|c{die1}|n, |c{die2}|n] {pm}{attr}[|c{attrdm}|n]"

            if args not in ['str', 'dex', 'end', 'int', 'edu', 'soc']:
                self.caller.msg("Attribute is invalid. Select from: str, dex, end, int, edu, soc.")
                return

            dice = [die(1, 6), die(1, 6)]

            attr = args
            attrdm = dm_attr(self.caller.db.attrs[args]['current'])


            if attrdm >= 0:
                pm = "+ "
            elif attrdm < 0:
                pm = "- "


            string = string.format(result=dice[0] + dice[1] + attrdm, die1=dice[0], die2=dice[1], pm=pm, attr=attr, attrdm=attrdm)
            self.caller.msg(string)
            return


        elif re.match(regexp2, args):  # checking for something like 'perform broker + int', or 'perform pilot(spacecraft) + dex'
            m = re.match(regexp2, args)
            string = "You rolled a |c{result}|n: dice rolled[|c{die1}|n, |c{die2}|n] {pm1}{skillname}[|c{skilldm}|n] {pm2}{attr}[|c{attrdm}|n]"
            skillname, attr = m.groups()

            if attr not in ['str', 'dex', 'end', 'int', 'edu', 'soc']:
                self.caller.msg("Attribute is invalid. Select from: str, dex, end, int, edu, soc.")
                return

            dice = [die(1, 6), die(1, 6)]

            skills = []

            for skill in self.caller.db.skills.keys():
                if skillname == skill[:len(skillname)]:
                    skills.append(skill)

            if len(skills) == 0:
                skillrank = -3
                skill = skillname + "[|runskilled|n]"

            elif len(skills) > 1:
                string = "There were multiple matches for '%s': %s." % (skillname, ', '.join(skills))
                self.caller.msg(string)
                return

            elif len(skills) == 1:
                skill = skills.pop()
                skillrank = self.caller.db.skills[skill]


            attrdm = dm_attr(self.caller.db.attrs[attr]['current'])


            if attrdm >= 0:
                pm2 = "+ "
            elif attrdm < 0:
                pm2 = "- "

            if skillrank >= 0:
                pm1 = "+ "
            elif skillrank < 0:
                pm1 = "- "


            string = string.format(
                result=dice[0] + dice[1] + attrdm + skillrank,
                die1=dice[0],
                die2=dice[1],
                pm1=pm1,
                pm2=pm2,
                attr=attr,
                attrdm=attrdm,
                skillname=skill,
                skilldm=skillrank,
                )

            self.caller.msg(string)
            return

        else:  # no matches, abort
            string += "Syntax: perform <skill> + <attribute>\n"
            string += "        perform <attribute>\n"
            string += "        perform <skill> + <attribute> <+/-><dm>\n"

            self.caller.msg(string)
            return


