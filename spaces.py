import pieces
from pieces import Piece

POST = 1
CAMPSITE = 2
HEADQUARTER = 3
NORMAL_LINKAGE = 1
RAIL_LINKAGE = 2


class Space:
    '''Represents a space on the board

    Attributes
    ----------
    id: `int`
        The id of the space, details below
    type: `int`
        The type of the space, POST | CAMPSITE | HEADQUARTER (1,2,3)
    piece: `Piece`|None
        The piece that is currently on the space, None if there is not a piece
    linkages: `list`[`tuple`[`Space`, Linkage `int`]]
        A list of adjecent spaces and their respective linkage to the current space. Linkage: NORMAL_LINKAGE | RAIL_LINKAGE (1,2)

    Methods
    --------
    set_linkages
    '''

    def __init__(self, id: int, type: int, piece: Piece | None) -> None:
        self.id = id
        self.type = type
        self.piece = piece
        self.linkages = []

    def set_linkages(self, linkages: list[tuple]):
        '''Used to set linkages between this space and other spaces

        Parameters
        ----------
        linkages: `list`[`tuple`[`Space`, Linkage `int`]]'''
        for space, linkage in linkages:
            if not isinstance(space, Space):
                raise TypeError("Invalid space argument type")
            if not isinstance(linkage, int) or linkage == NORMAL_LINKAGE or linkage == RAIL_LINKAGE:
                raise TypeError(f"Invalid linkage '{linkage}'")
        self.linkages = linkages

    def add_linkage(self, space, linkage: int):
        '''Used to add linkages between this space and other spaces

        Parameters
        ----------
        linkages: `list`[`tuple`[`Space`, Linkage `int`]]'''
        if not isinstance(space, Space):
            raise TypeError("Invalid space argument type")
        if not isinstance(linkage, int) and linkage != NORMAL_LINKAGE and linkage != RAIL_LINKAGE:
            raise TypeError(f"Invalid linkage '{linkage}'")

        self.linkages.append((space, linkage))

    def send_space(self, player_num: int) -> tuple[int, int, int|None]:
        if self.piece and self.piece.owner != player_num:
            return (self.id, self.type, pieces.ENEMY)
        elif self.piece:
            return (self.id, self.type, self.piece.value)
        else:
            return (self.id, self.type, None)
