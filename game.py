WAITING = 0
SETTING_UP = 1
PLAYING = 2

#Player only states
READY = 3

from board import PlayerBoard, EmptyPlayerBoard, Board


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



    def play(self):
        ...

    def get(self, player_num:int) -> dict:
        state = self.players_info[player_num]["state"]
        if state == WAITING:
            return self.info_dict() | {"your_state":state}
        if state == SETTING_UP:
            return self.info_dict() | {"board":self.players_info[player_num]["board"].send_board(), "player_states":[player_info["state"] for player_num, player_info in sorted(self.players_info.items(), key=lambda x:x[0])], "your_state":state}
        if state == READY:
            return self.info_dict() | {"player_states":[player_info["state"] for player_num, player_info in sorted(self.players_info.items(), key=lambda x:x[0])], "your_state":state}
        return {}
    
    def info_dict(self) -> dict:
        return {
            "state":self.state, 
            "players":[player_info["username"] for player_num, player_info in sorted(self.players_info.items(), key=lambda x:x[0])], 
            "turn":self.turn
        }