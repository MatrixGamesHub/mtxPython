
/* Interface definition for the RendererService service */

namespace csharp RendererService
namespace py RendererService


enum Direction {
    UP    = 0x0,
    RIGHT = 0x1,
    DOWN  = 0x2,
    LEFT  = 0x3,
}


enum GroundTexture {
    NONE     = 0x00,
    RANDOM   = 0x01,
    GRAS     = 0x02,
    WOOD     = 0x03,
    ROCK     = 0x04,
    SAND     = 0x05,
    LAVA     = 0x06,
    SNOW     = 0x07
    ICE      = 0x08,
    EARTH    = 0x09
    METAL    = 0x0A,
    MARBLE   = 0x0B,
    PAVEMENT = 0x0C,
    CONCRETE = 0x0D,
}


enum WallTexture {
    RED_BRICKS   = 0x00,
    WHITE_BRICKS = 0x01,
}


struct LevelInfo {
    1: string name,
    2: GroundTexture groundTexture,
    3: WallTexture wallTexture,
}


union Value {
    1: string strValue,
    2: i32 intValue,
    3: bool boolValue,
    4: double doubleValue,
}


service RendererService {
    void Ping(),
    void Shutdown(),
    void Freeze(),
    void Thaw(),
    void Pause(),
    void Resume(),
    void Clear(),
    list<i8> GetPreferedFieldSize(),
    void LoadLevel(1: list<list<list<list<i16>>>> field, 2: LevelInfo levelInfo),
    void ResetLevel(1: list<list<list<list<i16>>>> field),
    void UpdateObject(1: i16 objectId, 2: string key, 3: Value value),
    void Spawn(1: i16 objId, 2: i8 symbol, 3: i16 positionX, 4: i16 positionY),
    void Remove(1: i16 objectId, 2: i16 sourceId),
    void Collect(1: i16 objectId, 2: i16 sourceId),
    void TriggerEnter(1: i16 objectId, 2: i16 sourceId),
    void TriggerLeave(1: i16 objectId, 2: i16 sourceId),
    void Move(1: i16 objectId, 2: Direction direction, 3: i16 fromX, 4: i16 fromY, 5: i16 toX, 6: i16 toY),
    void Jump(1: i16 objectId, 2: Direction direction, 3: i16 fromX, 4: i16 fromY, 5: i16 toX, 6: i16 toY),
}
