from typeclasses.objects import Object
from random import randint
import re


class Weapon(Object):
    def at_object_creation(self):
        self.db.ap = 0
        self.db.damage = ""
        self.db.skill = ""
        self.db.ammo = 0
        self.db.ammo_max = self.db.ammo

