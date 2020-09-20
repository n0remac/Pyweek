import arcade

class GameResources:
    """
    In theory, this should be the place where you load in resources that the game uses via Arcade's various APIs.
    Currently a grab bag of Arcade resources that get stored, updated, and rendered.
    Unfortunately Arcade doesn't support an immutable API for stuff (probably for simplicity), so have to live with
    mutating the locations of sprite instances to move them around. Oh well!
    """

    def __init__(self):
        pass
