from command import Command


class CmdEq(Command):
    """Syntax: eq
        This command shows you the items you are currently wearing/equipped with.
    """
    key = "eq"
    aliases = ["equipment", "gear"]
    lock = "cmd:all()"
    help_category = "Gaming"


    def func(self):
        string = ""
        armor = None
        weapon = None

        if self.caller.db.armor is not None:
            armor = self.caller.search(self.caller.db.armor, quiet=True, global_search=True)
            if not armor:  # major error occured
                self.caller.msg("|rERROR: NONEXISTENT ARMOR!!|n Please notify an administrator immediately to rectify this.")
            else:
                armor = armor.pop()
                string += "Armor worn: %s\n" % str("|c" + armor.key + "|n")

                if armor:
                    string += "    rating: |c%s|n\n" % str(armor.db.rating)
                    string += "    mass: |c%s|n\n" % str(armor.db.mass)

        elif self.caller.db.armor is None:
            string += "Armor worn: |cNone|n\n"

        if self.caller.db.weapon is  not None:
            weapon = self.caller.search(self.caller.db.weapon, quiet=True, global_search=True)
            if not weapon:  # major error occured
                self.caller.msg("|rERROR: NONEXISTENT WEAPON!!|n Please notify an administrator immediately to rectify this.")
            else:
                weapon = weapon.pop()
                string += "Weapon equipped: %s\n" % str("|c" + weapon.key + "|n")

                if weapon:
                    string += "    ap: |c%s|n\n" % str(weapon.db.ap)
                    string += "    damage: |c%s|n\n" % str(weapon.db.damage)
                    string += "    skill: |c%s|n\n" % str(weapon.db.skill)
                    string += "    ammo: |c%s|n/|c%s|n\n" % (str(weapon.db.ammo), str(weapon.db.ammo_max))
                    string += "    mass: |c%s|n\n" % str(weapon.db.mass)

        elif self.caller.db.weapon is None:
            string += "Weapon equipped: |cNone|n\n"


        self.msg(string)

