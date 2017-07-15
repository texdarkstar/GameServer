from typeclasses.scripts import Script
from evennia.utils import inherits_from


class CombatHandler(Script):
    desc = "Combat handler/inititive tracker"
    key = "combathandler"


    def at_script_creation(self):
        self.db.characters = {}  # {"Texdarkstar":, "#1"}
        self.db.inititive_board = {}  # {"Texdarkstar": 7}


    def add_character(self, character):
        if character.key in self.db.characters.keys():
            raise KeyError()

        self.db.characters[character.key] = character.dbref


    def rem_character(self, character):
        del self.db.characters[character.key]


    def at_start(self):
        self.obj.msg_contents("Combat has begun!")

