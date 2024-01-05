from spaces import Space, POST, CAMPSITE, HEADQUARTER, NORMAL_LINKAGE, RAIL_LINKAGE

class Board:
    def __init__(self, spaces:list[Space]) -> None:
        self.spaces = spaces

class EmptyBoard(Board):
    def __init__(self) -> None:
        empty_board_spaces:list[Space] = [Space(1, POST, None), Space(2, POST, None), Space(3, POST, None), Space(4, POST, None), Space(5, POST, None),
                            Space(6, POST, None), Space(7, CAMPSITE, None), Space(8, POST, None), Space(9, CAMPSITE, None), Space(10, POST, None),
                            Space(11, POST, None), Space(12, POST, None), Space(13, CAMPSITE, None), Space(14, POST, None), Space(15, POST, None),
                            Space(16, POST, None), Space(17, CAMPSITE, None), Space(1, POST, None), Space(19, CAMPSITE, None), Space(20, POST, None),
                            Space(21, POST, None), Space(22, POST, None), Space(23, POST, None), Space(24, POST, None), Space(25, POST, None),
                            Space(26, POST, None), Space(27, HEADQUARTER, None), Space(28, POST, None), Space(29, HEADQUARTER, None), Space(30, POST, None)]

        for index, space in enumerate(empty_board_spaces):
            #Add linkage above
            if index - 5 >= 0:
                if index < 25 and (index % 5 == 0 or (index + 1) % 5 == 0):
                    space.add_linkage((empty_board_spaces[index - 5], RAIL_LINKAGE))
                else:
                    space.add_linkage((empty_board_spaces[index - 5], NORMAL_LINKAGE))

            #Add linkage below
            if index + 5 < len(empty_board_spaces):
                if index < 25 and (index % 5 == 0 or (index + 1) % 5 == 0):
                    space.add_linkage((empty_board_spaces[index + 5], RAIL_LINKAGE))
                else:
                    space.add_linkage((empty_board_spaces[index + 5], NORMAL_LINKAGE))

            #Add linkage to the right
            if index + 1 < len(empty_board_spaces):
                if index < 5 or (index >= 20 and index < 25):
                    space.add_linkage((empty_board_spaces[index + 1], RAIL_LINKAGE))
                else:
                    space.add_linkage((empty_board_spaces[index + 1], NORMAL_LINKAGE))

            #Add linkage to the left
            if index - 1 >= 0:
                if index < 5 or (index >= 20 and index < 25):
                    space.add_linkage((empty_board_spaces[index - 1], RAIL_LINKAGE))
                else:
                    space.add_linkage((empty_board_spaces[index - 1], NORMAL_LINKAGE))

            #Add diagonal linkages to all campsites and in reverse
            if space.type == CAMPSITE:
                #top left
                space.add_linkage((empty_board_spaces[index - 6], NORMAL_LINKAGE))
                empty_board_spaces[index - 6].add_linkage((space, NORMAL_LINKAGE))

                #top right
                space.add_linkage((empty_board_spaces[index - 4], NORMAL_LINKAGE))
                empty_board_spaces[index - 4].add_linkage((space, NORMAL_LINKAGE))

                #bottom left
                space.add_linkage((empty_board_spaces[index + 4], NORMAL_LINKAGE))
                empty_board_spaces[index + 4].add_linkage((space, NORMAL_LINKAGE))

                #bottom right
                space.add_linkage((empty_board_spaces[index + 6], NORMAL_LINKAGE))
                empty_board_spaces[index + 6].add_linkage((space, NORMAL_LINKAGE))

        self.spaces = empty_board_spaces