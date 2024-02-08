import websockets
import asyncio
import json

import game
from game import Game


games:list[Game] = []
connections = set()




async def handler(conn:websockets.WebSocketServerProtocol):
    print(f"Connected with: {conn.id}")
    connections.add(conn)

    #Receive the first piece of data from client
    try:
        raw_data = await conn.recv()
    except:
        return
    
    data:dict = json.loads(raw_data)

    #First- Login action data validation
    if not isinstance(data, dict):
        await conn.close(reason="data format wrong")
        return
    if data.get("action") != "login":
        await conn.close(reason="Data format wrong or first action not login")
        return
    if not data.get("username"):
        await conn.close(reason="No username provided")
        return
    
    username = str(data["username"])

    if games and games[-1] and games[-1].state == game.WAITING:
        #Join an existing game
        player_num = games[-1].join(username)
    else:
        #Creates a new game
        games.append(Game())
        player_num = games[-1].join(username)
    
    #Makes sure the player successfully joins the game
    if player_num == 0:
        await conn.close(reason="Game joining error.")
        print("Game joining error, please check issue")
        return
    
    joined_game = games[-1]
    await conn.send(json.dumps({"player_num":player_num, "game":joined_game.get(player_num)}))

    try:
        async for raw_data in conn:
            if joined_game not in games:
                await conn.close()
                break
            data = json.loads(raw_data)
            action = data.get("action")
            if action:
                if action == "get":
                    game_info = joined_game.get(player_num)
                    await conn.send(json.dumps(game_info))
                
                elif action == "setup":
                    try:
                        joined_game.setup(player_num, data["space_ids"], data["piece_values"])
                    except Exception as e:
                        print(e)
                
                

                else:
                    await conn.send(json.dumps({}))
    
    except websockets.ConnectionClosedError as e:
        print(e)
        
    
    try:
        games.remove(joined_game)
    except:
        pass














async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("server started, waiting for connections")
        await asyncio.Future()

asyncio.run(main())