
/* Interface definition for the ControllerService service */

namespace csharp ControllerService
namespace py ControllerService


enum Direction {
    UP    = 0x0,
    RIGHT = 0x1,
    DOWN  = 0x2,
    LEFT  = 0x3,
}


struct GameInfo {
    1: string name,
    2: string description,
    3: i8 maxPlayers,
}


exception GameError {
    1: string errorMessage,
}


service ControllerService {
    void Ping(),
    i16 ConnectRenderer(1: string host, 2: i32 port),
    void DisconnectRenderer(1: i16 rendererId),
    void MovePlayer(1: i8 number, 2: Direction direction) throws (1:GameError gameError),
    void JumpPlayer(1: i8 number, 2: Direction direction) throws (1:GameError gameError),
    list<string> GetGames(),
    GameInfo GetGameInfo(1: string name) throws (1:GameError gameError),
    void LoadGame(1: string name) throws (1:GameError gameError),
    void ReloadGame(),
    void ResetLevel(),
}
