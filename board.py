from spaces import Space, POST, CAMPSITE, HEADQUARTER, NORMAL_LINKAGE, RAIL_LINKAGE


class PlayerBoard:
    def __init__(self, player: int, spaces: list[Space]) -> None:
        self.player = player
        self.spaces = spaces

    def find_space(self, id: int):
        '''Returns the first occurence of the space with the given id'''
        for space in self.spaces:
            if space.id == id:
                return space

    def send_board(self) -> list[tuple[int, int]]:
        return [space.send_space(self.player) for space in self.spaces]


class EmptyPlayerBoard(PlayerBoard):
    def __init__(self, player: int) -> None:
        empty_board_spaces: list[Space] = [Space(1, POST, None), Space(2, POST, None), Space(3, POST, None), Space(4, POST, None), Space(5, POST, None),      # nopep8
                            Space(6, POST, None), Space(7, CAMPSITE, None), Space(8, POST, None), Space(9, CAMPSITE, None), Space(10, POST, None),           # nopep8
                            Space(11, POST, None), Space(12, POST, None), Space(13, CAMPSITE, None), Space(14, POST, None), Space(15, POST, None),           # nopep8
                            Space(16, POST, None), Space(17, CAMPSITE, None), Space(18, POST, None), Space(19, CAMPSITE, None), Space(20, POST, None),        # nopep8
                            Space(21, POST, None), Space(22, POST, None), Space(23, POST, None), Space(24, POST, None), Space(25, POST, None),               # nopep8
                            Space(26, POST, None), Space(27, HEADQUARTER, None), Space(28, POST, None), Space(29, HEADQUARTER, None), Space(30, POST, None)]  # nopep8

        for index, space in enumerate(empty_board_spaces):
            # Add linkage above
            if index - 5 >= 0:
                if index < 25 and (index % 5 == 0 or (index + 1) % 5 == 0):
                    space.add_linkage(
                        empty_board_spaces[index - 5], RAIL_LINKAGE)
                else:
                    space.add_linkage(
                        empty_board_spaces[index - 5], NORMAL_LINKAGE)

            # Add linkage below
            if index + 5 < len(empty_board_spaces):
                if index < 25 and (index % 5 == 0 or (index + 1) % 5 == 0):
                    space.add_linkage(
                        empty_board_spaces[index + 5], RAIL_LINKAGE)
                else:
                    space.add_linkage(
                        empty_board_spaces[index + 5], NORMAL_LINKAGE)

            # Add linkage to the right
            if index + 1 < len(empty_board_spaces):
                if index < 5 or (index >= 20 and index < 25):
                    space.add_linkage(
                        empty_board_spaces[index + 1], RAIL_LINKAGE)
                else:
                    space.add_linkage(
                        empty_board_spaces[index + 1], NORMAL_LINKAGE)

            # Add linkage to the left
            if index - 1 >= 0:
                if index < 5 or (index >= 20 and index < 25):
                    space.add_linkage(
                        empty_board_spaces[index - 1], RAIL_LINKAGE)
                else:
                    space.add_linkage(
                        empty_board_spaces[index - 1], NORMAL_LINKAGE)

            # Add diagonal linkages to all campsites and in reverse
            if space.type == CAMPSITE:
                # top left
                space.add_linkage(
                    empty_board_spaces[index - 6], NORMAL_LINKAGE)
                empty_board_spaces[index -
                                   6].add_linkage(space, NORMAL_LINKAGE)

                # top right
                space.add_linkage(
                    empty_board_spaces[index - 4], NORMAL_LINKAGE)
                empty_board_spaces[index -
                                   4].add_linkage(space, NORMAL_LINKAGE)

                # bottom left
                space.add_linkage(
                    empty_board_spaces[index + 4], NORMAL_LINKAGE)
                empty_board_spaces[index +
                                   4].add_linkage(space, NORMAL_LINKAGE)

                # bottom right
                space.add_linkage(
                    empty_board_spaces[index + 6], NORMAL_LINKAGE)
                empty_board_spaces[index +
                                   6].add_linkage(space, NORMAL_LINKAGE)

        self.player = player
        self.spaces = empty_board_spaces


class Board:
    def __init__(self, boards: list[PlayerBoard]) -> None:
        self.boards = boards
        self.boards.sort(key=lambda board: board.player)
        # 2 player board joining
        if len(boards) == 2:
            between_board_links = [(1, 5), (3, 3), (5, 1)]
            for link in between_board_links:
                joining = boards[0].find_space(
                    link[0]), boards[1].find_space(link[1])
                if joining[0] and joining[1]:
                    joining[0].add_linkage(joining[1], RAIL_LINKAGE)
                    joining[1].add_linkage(joining[0], RAIL_LINKAGE)

        else:
            raise NotImplementedError(
                "More than 2 players not yet implemented")

    def send_board(self, player_num: int) -> list[tuple[int, int]]:
        return_board = []
        if len(self.boards) == 2:
            return_board += [space.send_space(player_num) for space in reversed(
                self.boards[1 if player_num == 2 else 2].spaces)]
            return_board += [space.send_space(player_num)
                             for space in self.boards[player_num].spaces]
        else:
            raise NotImplementedError(
                "More than 2 players not yet implemented")

        return return_board
