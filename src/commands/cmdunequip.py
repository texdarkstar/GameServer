from command import Command
from evennia import utils


class CmdUnequip(Command):
    """Syntax: unequip <weapon/armor>
        This command unequips your character with an item.
        If it is armor, it will remove it from your character and decrease your armor rating accordingly.
        If it is a weapon, it will remove it, leaving you with your fists.

        This command will also update your encumberance rating.
        """
    key = "unequip"
    aliases = ["remove", "rem"]
    locks = "cmd:all()"
    help_category = "Gaming"


    def func(self):
        arg = self.args.strip().lower()

        if arg:
            item = self.caller.search(arg, candidates=self.caller.contents, nofound_string="You can't remove |c%s|n, you aren't wearing it." % arg)

            if item:
                # item = item.pop()
                if utils.inherits_from(item, "typeclasses.armor.Armor"):  # it is armor
                    if not self.caller.db.armor:  # checking slot
                        self.caller.msg("You can't unequip |c" + item.key + "|n, you aren't equiped with anything!")
                        return
                    else:  # good to go!
                        self.caller.db.armor_rating -= item.db.rating
                        del self.caller.db.armor

                elif utils.inherits_from(item, "typeclasses.weapon.Weapon"): # it is a weapon
                    if not self.caller.db.weapon:  # checking slot
                        self.caller.msg("You can't unequip |c" + item.key + "|n, you aren't equiped with anything!")
                        return
                    else:  # good to go!
                        del self.caller.db.weapon
                else:
                    self.caller.msg("You can't unequip |c" + item.key + "|n.")
                    return

                item.locaton = self.caller  # moving the item back to the callers inventory
                self.caller.db.worn_mass -= item.db.mass
                self.caller.msg("You unequip |c" + item.key + "|n.")
                return

        elif not arg:
            self.caller.msg("Unequip what?")
            return

