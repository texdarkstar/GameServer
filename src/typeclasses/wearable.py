from objects import Object


class Wearable(Object):
    """Object class that can be worn, inherit your wearable items from this.
    """

    def at_object_creation(self):
        self.db.wearable = True
