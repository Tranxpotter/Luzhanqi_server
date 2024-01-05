WAITING = 0
SETTING_UP = 1
PLAYING = 2


class Game:
    def __init__(self) -> None:
        self.state = WAITING
        self.players = []
    
    def join(self, player) -> int:
        '''Lets a player join and return the player number, returns 0 if failed to join'''
        if self.state != WAITING:
            return 0
        self.players.append(player)
        if len(self.players) == 2:
            self.state = SETTING_UP
        
        return len(self.players)
    
    def play(self):
        ...

    def get(self):
        ...