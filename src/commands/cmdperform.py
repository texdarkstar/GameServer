import re
from command import Command
from random import randint as die
from world.tables import *
from typeclasses.characters import Character


class CmdPerform(Command):
    """Syntax: perform <skill> + <attribute> [<boon>]
                perform <attribute> [<boon>]

        Rolls a skill + attribute, or just rolls an attribute.
        2D6 plus your specified skill rank + an attribute dm.

        Examples:
            perform str
            perform broker + int
            perform pilot(spacecraft) + dex
            perform int boon
            perform gun combat(rifle) + dex boon
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
        use_boon = False
        use_bane = self.caller.db.bane_dice > 0
        boonbane_string = ""
        string = ""

        regexp1 = r"^(\w+)\s*?(\w+)?$"
        regexp2 = r"^(.+)\s*?\+\s+?(\w+)\s?(\w+)?$"



        _chars = [char for char in Character.objects.all() if char.player]  # getting a list of all connected characters
        chars = []
        privy_chars = []

        for char in _chars:
            if (char.player.check_permstring("Wizards") or char.db.gm):  # removing those that are not allowed to hear priviledged data, also removing self.caller
                privy_chars.append(char)
            else:
                chars.append(char)


        # removing duplicates of self.caller
        for char in chars:
            if char.id == self.caller.id:
                chars.remove(char)

        for char in privy_chars:
            if char.id == self.caller.id:
                privy_chars.remove(char)


        if re.match(regexp1, args):  # checking for something like 'perform str', or 'perform int boon'
            m = re.match(regexp1, args).groups()
            string = "You rolled a |c{result}|n: dice_rolled[|c{die1}|n, |c{die2}|n] {pm}{attr}[|c{attrdm}|n]{crit}{boonbane}"

            attr = m[0]
            if attr not in ['str', 'dex', 'end', 'int', 'edu', 'soc']:
                self.caller.msg("Attribute is invalid. Select from: str, dex, end, int, edu, soc.")
                return


            dice = [die(1, 6), die(1, 6)]

            use_boon = self.caller.db.boon_dice > 0 and (str(m[1]).lower() == "boon" or self.caller.player.db.config["autospend"])

            if use_boon:
                self.caller.db.boon_dice -= 1
                if self.caller.db.bane_dice > 0:
                    self.caller.db.bane_dice -= 1
                    use_boon = False
                    use_bane = False

            if use_boon:
                boon = die(1, 6)
                toss = "nothing"
                for d in dice:
                    if boon > d:
                        toss = d

                if toss != "nothing":
                    strdie = str(dice.pop(dice.index(toss)))
                else:
                    strdie = toss

                boonbane_string = "\n|gboon_rolled|n[|c{boon}|n], tossed |c{die}|n.".format(
                    boon=str(boon),
                    die=strdie
                    )
                dice.append(boon)

            if use_bane:
                self.caller.db.bane_dice -= 1
                bane = die(1, 6)
                toss = "nothing"
                for d in dice:
                    if bane < d:
                        toss = d

                if toss != "nothing":
                    strdie = str(dice.pop(dice.index(toss)))
                else:
                    strdie = toss

                boonbane_string = "\n|rbane_rolled|n[|c{bane}|n], tossed |c{die}|n.".format(
                    bane=str(bane),
                    die=strdie
                    )
                dice.append(bane)

            crit = ""
            if dice[0] == dice[1] == 1:
                crit = " (|rsnake eyes!|n)"

            elif dice[0] == dice[1] == 6:
                crit = " (|gbox cars!|n)"

            attrdm = dm_attr(self.caller.db.attrs[attr]['current'])


            if attrdm >= 0:
                pm = "+ "
            elif attrdm < 0:
                pm = "- "


            string = string.format(
                result=dice[0] + dice[1] + attrdm,
                die1=dice[0],
                die2=dice[1],
                pm=pm,
                attr=attr,
                attrdm=attrdm,
                crit=crit,
                boonbane=boonbane_string,
                )

            self.caller.msg(string)
            for char in privy_chars:
                char.msg(string.replace("You", self.caller.key))

            for char in chars:
                char.msg("{who} rolled {attr}: |c{result}{crit}|n".format(who=self.caller.key, attr=attr, result=dice[0] + dice[1] + attrdm, crit=crit))

            return


        elif re.match(regexp2, args):  # checking for something like 'perform broker + int', or 'perform pilot(spacecraft) + dex', or 'perform computers + int boon'
            string = "You rolled a |c{result}|n: dice_rolled[|c{die1}|n, |c{die2}|n] {pm1}{skillname}[|c{skilldm}|n] {pm2}{attr}[|c{attrdm}|n]{crit}{boonbane}"
            m = re.match(regexp2, args).groups()
            skillname = m[0]
            attr = m[1]

            if skillname.strip() == "jack of all trades":
                self.caller.msg("You can't roll jack of all trades.")
                return

            if attr not in ['str', 'dex', 'end', 'int', 'edu', 'soc']:
                self.caller.msg("Attribute is invalid. Select from: str, dex, end, int, edu, soc.")
                return

            dice = [die(1, 6), die(1, 6)]

            use_boon = self.caller.db.boon_dice > 0 and (str(m[2]).lower() == "boon" or self.caller.player.db.config["autospend"])

            if use_boon:
                self.caller.db.boon_dice -= 1
                if self.caller.db.bane_dice > 0:
                    self.caller.db.bane_dice -= 1
                    use_boon = False
                    use_bane = False

            if use_boon:
                boon = die(1, 6)
                toss = "nothing"
                for d in dice:
                    if boon > d:
                        toss = d

                if toss != "nothing":
                    strdie = str(dice.pop(dice.index(toss)))
                else:
                    strdie = toss

                boonbane_string = "\n|gboon_rolled|n[|c{boon}|n], tossed |c{die}|n.".format(
                    boon=str(boon),
                    die=strdie
                    )
                dice.append(boon)

            if use_bane:
                self.caller.db.bane_dice -= 1
                bane = die(1, 6)
                toss = "nothing"
                for d in dice:
                    if bane < d:
                        toss = d

                if toss != "nothing":
                    strdie = str(dice.pop(dice.index(toss)))
                else:
                    strdie = toss

                boonbane_string = "\n|rbane_rolled|n[|c{bane}|n], tossed |c{die}|n.".format(
                    bane=str(bane),
                    die=strdie
                    )
                dice.append(bane)


            crit = ""
            if dice[0] == dice[1] == 1:
                crit = " (|rsnake eyes!|n)"

            elif dice[0] == dice[1] == 6:
                crit = "(|gbox cars!|n)"

            skills = []

            for skill in self.caller.db.skills.keys():
                if skillname == skill[:len(skillname)]:
                    skills.append(skill)

            if len(skills) == 0:
                skillrank = -3
                skill = skillname + "[|runskilled|n]"

                if "jack of all trades" in self.caller.db.skills.keys():
                    rank = self.caller.db.skills["jack of all trades"]
                    skillrank = -3 + rank

                    if skillrank == 0:
                        skillrank = 0

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
                crit=crit,
                boonbane=boonbane_string,
                )

            self.caller.msg(string)

            for char in privy_chars:
                char.msg(string.replace("You", self.caller.key))

            for char in chars:
                char.msg("{who} rolled {skillname} + {attr}: |c{result}{crit}|n".format(who=self.caller.key, skillname=skillname, attr=attr, result=dice[0] + dice[1] + attrdm + skillrank, crit=crit))

            if "jack of all trades" in self.caller.db.skills.keys():
                rank = self.caller.db.skills["jack of all trades"]
                self.caller.msg("(Deducted |c%s|n for having jack of trades at rank |c%s|n)" % (rank, rank))

                for char in privy_chars:
                    char.msg("(Deducted |c%s|n for having jack of trades at rank |c%s|n)" % (rank, rank))

            return

        else:  # no matches, abort
            string += "Syntax: perform <skill> + <attribute> [<boon>]\n"
            string += "        perform <attribute> [<boon>]\n"

            self.caller.msg(string)
            return


