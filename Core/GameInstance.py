from Core.GameResources import GameResources

class GameInstance:
    """
    This is an instance of the game and all of the different components needed to render it.
    """
    def __init__(self):

        # Core game resources
        self.game_resources = GameResources()