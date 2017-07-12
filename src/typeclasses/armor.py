from objects import Object


class Armor(Object):
    def at_object_creation(self):
        self.db.rating = 0
        self.db.mass = 0
