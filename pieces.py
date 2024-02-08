FIELD_MARSHAL = 9
GENERAL = 8
MAJOR_GENERAL = 7
BRIGADIER_GENERAL = 6
COLONEL = 5
MAJOR = 4
CAPTAIN = 3
LIEUTENANT = 2
ENGINEER = 1
BOMB = 10
LANDMINE = 11
FLAG = 12
ENEMY = 13


class Piece:
    '''Represents a playing piece

    Attributes
    -----------
    owner `int`:
        The player number of the owner of the piece
    name `str`:
        Name of the piece
    value `int`:
        From 1-12, represents the type of the piece'''

    def __init__(self, owner: int, value: int) -> None:
        self.owner = owner
        self.value = value
