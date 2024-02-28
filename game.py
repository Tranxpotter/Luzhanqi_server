WAITING = 0
SETTING_UP = 1
PLAYING = 2
END = 4

#Player only states
READY = 3

from board import PlayerBoard, EmptyPlayerBoard, Board
import pieces as pieces_mod
from pieces import Piece
import spaces as spaces_mod
from spaces import Space



class Game:
    def __init__(self, max_players:int = 2) -> None:
        self.max_players = max_players
        self.state = WAITING
        self.players_info:dict[int, dict] = {}
        self.board:Board|None = None
        self.turn = 1
    
    def join(self, username:str) -> int:
        '''Lets a player join and return the player number, returns 0 if failed to join'''
        if self.state != WAITING:
            return 0
        player_num = len(self.players_info) + 1
        self.players_info[player_num] = {"username":username, "state":WAITING, "board":EmptyPlayerBoard(player_num)}
        
        if player_num == self.max_players:
            self.state = SETTING_UP
            self.on_start_setup()
        
        return player_num
    
    def on_start_setup(self):
        for player_num in self.players_info:
            self.players_info[player_num]["state"] = SETTING_UP

    def setup(self, player_num:int, space_ids, piece_values):
        for space_id, piece_value in zip(space_ids, piece_values):
            piece:Piece|None = Piece(player_num, piece_value) if piece_value else None
            self.players_info[player_num]["board"].find_space(space_id).piece = piece
    
    def ready(self, player_num:int):
        self.players_info[player_num]["state"] = READY
        if all(map(lambda x:x["state"] == READY, self.players_info.values())):  #Check if all players are ready
            for player_info in self.players_info.values():
                player_info["state"] = PLAYING
            self.board = Board([player_board for player_board in map(lambda x:x["board"], self.players_info.values())])
            self.state = PLAYING

    def play(self, player_num:int, origin:list[int], destination:list[int]):
        if self.state == END:
            return
        
        if player_num != self.turn:
            return
        origin_board, origin_space_id = origin
        dest_board, dest_space_id = destination
        print(f"{player_num=}, {origin_board=}, {origin_space_id=}, {dest_board=}, {dest_space_id=}")
        
        if origin == destination:
            return
        if origin_board == 4 or dest_board == 4:
            return
        if self.board is None:
            return
        
        origin_space = self.board.find_space(origin_board, origin_space_id)
        if not origin_space:
            return
        import pprint
        print("origin space:")
        pprint.pp(origin_space.__dict__)
        print()

        dest_space = self.board.find_space(dest_board, dest_space_id)
        if not dest_space:
            return
        print("Dest space:")
        pprint.pp(dest_space.__dict__)
        print()
        
        piece = origin_space.piece
        if not piece:
            return
        if piece.value == pieces_mod.LANDMINE or piece.value == pieces_mod.FLAG:
            return
        elif piece.value != pieces_mod.ENGINEER:
            print("Single space search")
            if not origin_space.space_is_linked(dest_space):
                print("Single space search failed.")
                return
        else:
            print("Single space search")
            if not origin_space.space_is_linked(dest_space):
                print("Single space search failed.")
            def search_linkages(space:Space, dest:Space, visited:list = [], bypass:bool = False):
                print("Searching space:")
                pprint.pp(space.__dict__)
                if space in visited:
                    return False
                visited.append(space)
                if space == dest:
                    return True
                if not bypass and space.piece:
                    return False
                return any([search_linkages(new_space, dest, visited=visited) for new_space in map(lambda x:x[0], filter(lambda x:x[1] == spaces_mod.RAIL_LINKAGE, space.linkages))])
            print("multi space search")
            if not search_linkages(origin_space, dest_space, bypass=True):
                print("multi space search failed.")
                return
            
        
        
        
        dest_piece = dest_space.piece
        if dest_piece:
            if dest_piece.owner == piece.owner:
                return
            elif dest_space.type == spaces_mod.CAMPSITE:
                return
        
        origin_space.piece = None
        if dest_piece is None:
            dest_space.piece = piece
            origin_space.piece = None
            
        elif dest_piece.value == pieces_mod.FLAG:
            #WIN/LOSE SEQUENCE
            self.state = END
            return
        
        elif piece.value == pieces_mod.BOMB:
            dest_space.piece = None
        
        elif piece.value < 10 and dest_piece.value < 10:
            if piece.value == dest_piece.value:
                dest_space.piece = None
            elif dest_piece.value < piece.value:
                dest_space.piece = piece
        
        elif dest_piece.value == pieces_mod.LANDMINE:
            if piece.value == pieces_mod.ENGINEER:
                dest_space.piece = piece
            else:
                dest_space.piece = None
        
        elif dest_piece.value == pieces_mod.BOMB:
            dest_space.piece = None
        
        else:
            print("PIECE NOT RECOGNIZED????")
            return
        
        self.turn = 3 - self.turn
        
        
            
        

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

    def get(self, player_num:int) -> dict:
        state = self.players_info[player_num]["state"]
        if state == WAITING:
            return self.info_dict() | {"your_state":state}
        if state == SETTING_UP:
            return self.info_dict() | {"board":self.players_info[player_num]["board"].send_board(player_num)[1], "player_states":[player_info["state"] for player_num, player_info in sorted(self.players_info.items(), key=lambda x:x[0])], "your_state":state}
        if state == READY:
            return self.info_dict() | {"player_states":[player_info["state"] for player_num, player_info in sorted(self.players_info.items(), key=lambda x:x[0])], "your_state":state}
        if state == PLAYING:
            if not self.board:
                print("Board not set up!!!")
                return self.info_dict()
            return self.info_dict() | {"turn":self.turn, "board":self.board.send_board(player_num)}
        return {}
    
    def info_dict(self) -> dict:
        return {
            "state":self.state, 
            "players":[player_info["username"] for player_num, player_info in sorted(self.players_info.items(), key=lambda x:x[0])], 
            "turn":self.turn
        }