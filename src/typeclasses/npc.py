from typeclasses.objects import Object
from typeclasses.characters import Character


class NPC(Character):
    def at_object_creation(self):
        super(NPC, self).at_object_creation()
        self.locks.add("puppet:pperm(puppet_%s)" % self.key.lower())
        self.permissions.add("Players")

        self.home = "#2"
