from wearable import Wearable


class Armor(Wearable):
    """Worn armor, provides armor protection to the slots it takes up."""

    def at_object_creation(self):
        self.db.slots = []
        self.db.rating = 0
        self.db.mass = 0
