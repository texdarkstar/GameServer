from command import Command
from evennia import utils


class CmdEquip(Command):
    """Syntax: equip <weapon/armor>
        This command equips your character with an item.
        If it is armor, it will put it on your character and increase armor rating accordingly.
        If it is a weapon, it will make sure that all future attacks are with that weapon.

        This command will also update your encumberance rating.
        """
    key = "equip"
    aliases = ["wear"]
    locks = "cmd:all()"
    help_category = "Gaming"


    def func(self):
        arg = self.args.strip().lower()

        if arg:
            item = self.caller.search(arg, candidates=self.caller.contents, nofound_string="You can't equip |c%s|n, you aren't carrying it." % arg)

            if item:
                # item = item.pop()
                if utils.inherits_from(item, "typeclasses.armor.Armor"):  # it is armor
                    if self.caller.db.armor:  # checking slot
                        self.caller.msg("You can't equip |c" + item.key + "|n, your armor slot is full.")
                        return
                    else:  # good to go!
                        self.caller.db.armor = "#" + str(item.id)
                        self.caller.db.armor_rating = item.db.rating

                elif utils.inherits_from(item, "typeclasses.weapon.Weapon"): # it is a weapon
                    if self.caller.db.weapon:  # checking slot
                        self.caller.msg("You can't equip |c" + item.key + "|n, your weapon slot is full.")
                        return
                    else:  # good to go!
                        self.caller.db.weapon = "#" + str(item.id)
                else:
                    self.caller.msg("You can't equip |c" + item.key + "|n.")
                    return

                self.caller.db.worn_mass += item.db.mass
                self.caller.msg("You equip |c" + item.key + "|n.")
                return

        elif not arg:
            self.caller.msg("Equip what?")
            return

