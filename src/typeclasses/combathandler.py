from typeclasses.scripts import Script
from evennia.utils import inherits_from, evtable
from random import randint, choice
from world.tables import dm_attr


class CombatHandler(Script):
    def at_script_creation(self):
        self.desc = "Combat handler/inititive tracker"
        self.key = "combathandler"
        self.persistent = False
        self.interval = .01
        self.repeats = 0
        self.start_delay = False

        self.db.characters = {}  # {"Texdarkstar":, "#1"}
        self.db.inititive_board = {}  # {"Texdarkstar": 7}
        self.db.went = []
        self.db.turn_player = ""
        self.db.running = False
        self.db.going = []
        self.db.rounds = 1

    def at_start(self):
        if not self.db.running:
            self.obj.msg_contents("Combat has begun!  Roll inititive!")

            for name in self.db.characters.keys():
                rolls = []
                char = self.obj.search(self.db.characters[name], global_search=True)
                if not char:
                    pass
                else:
                    dex = char.db.attrs["dex"]["current"]
                    self.db.inititive_board[name] += dm_attr(dex)
                    for i in xrange(2):
                        roll = randint(1, 6)
                        rolls.append(roll)
                        self.db.inititive_board[name] += roll

                char.msg("Your inititive roll is a |c" + str(self.db.inititive_board[name]) + "|n: dice_rolled[|c%d|n, |c%d|n] %s dex[|c%d|n]" % (rolls[0], rolls[1], "+" if dm_attr(dex) >= 0 else "-", dm_attr(dex)))

            self.db.running = True

    def at_server_reload(self):
        self.stop()

    def add_character(self, character):
        if character.key in self.db.characters.keys():
            raise KeyError()

        self.db.characters[character.key] = character.dbref
        self.db.inititive_board[character.key] = 0

    def rem_character(self, character):
        del self.db.characters[character.key]
        del self.db.inititive_board[character.key]

    def at_repeat(self):
        if self.db.going == []:
            self.db.went = []

            if self.db.rounds > 1:
                self.obj.msg_contents("A new round begins. This is round |c%d|n." % self.db.rounds)

            self.db.rounds += 1

        if self.db.going == []:
            highest = []
            board = {}
            for key in self.db.inititive_board.keys():
                board[key] = self.db.inititive_board[key]

            while len(self.db.going) < len(self.db.characters.keys()):
                highest = []

                for name in board.keys():
                    i = self.db.inititive_board[name]
                    if highest == []:
                        highest = [name, i]
                    else:

                        if i > highest[1] and name != highest[0]:
                            highest = [name, i]
                        elif i < highest[1] and name != highest[0]:
                            continue

                        elif i == highest[1] and name != highest[0]:
                            obj1 = self.obj.search(self.db.characters[name], global_search=True)
                            obj2 = self.obj.search(self.db.characters[highest[0]], global_search=True)

                            if obj1.db.attrs["dex"]["current"] > obj2.db.attrs["dex"]["current"]:
                                highest = [name, i]
                            elif obj1.db.attrs["dex"]["current"] < obj2.db.attrs["dex"]["current"]:
                                continue
                            elif obj1.db.attrs["dex"]["current"] == obj2.db.attrs["dex"]["current"]:
                                highest = choice([[name, i], highest])

                self.db.going.append(highest)
                del board[highest[0]]

        self.func()


    def func(self):
        character = self.obj.search(self.db.characters[self.db.going.pop(0)[0]], global_search=True)
        self.obj.msg_contents("It is %s's turn." % character.key)
        self.db.turn_player = character.key
        self.pause()
