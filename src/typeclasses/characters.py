"""
Characters

Characters are (by default) Objects setup to be puppeted by Players.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
from evennia import DefaultCharacter


class Character(DefaultCharacter):
    """
    The Character defaults to reimplementing some of base Object's hook methods with the
    following functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead).
    at_after_move(source_location) - Launches the "look" command after every move.
    at_post_unpuppet(player) -  when Player disconnects from the Character, we
                    store the current location in the pre_logout_location Attribute and
                    move it to a None-location so the "unpuppeted" character
                    object does not need to stay on grid. Echoes "Player has disconnected" 
                    to the room.
    at_pre_puppet - Just before Player re-connects, retrieves the character's
                    pre_logout_location Attribute and move it back on the grid.
    at_post_puppet - Echoes "PlayerName has entered the game" to the room.

    """
    def at_object_creation(self):
        self.db.prompt = "\n> \n\n"
        self.db.race = 'human'
        self.db.gender = ''
        self.db.attrs = {}
        self.db.attrs['str'] = {"current": 7, "base": 7}
        self.db.attrs['dex'] = {"current": 7, "base": 7}
        self.db.attrs['end'] = {"current": 7, "base": 7}
        self.db.attrs['int'] = {"current": 7, "base": 7}
        self.db.attrs['edu'] = {"current": 7, "base": 7}
        self.db.attrs['soc'] = {"current": 7, "base": 7}

        self.db.skills = {}
        self.db.boon_dice = 0
        self.db.bane_dice = 0
        self.db.config = {}
        self.db.gm = False
        self.db.equipment = {
            'torso': '',
            }


    def calculate(self):
        pass
