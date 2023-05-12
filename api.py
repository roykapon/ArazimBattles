"""
Welcome to the API Documentation!

You probably want to get started with `Context` methods, and have a look at `Exceptions`.
"""

from enum import Enum
from typing import Optional


class Bloons(Enum):
    """
    An enum representing all bloon types.

    **Note:** `CAMO` and `LEAD` are currently not protected like normal game rules.
    """

    RED = 0
    BLUE = 1
    GREEN = 2
    YELLOW = 3
    PINK = 4
    BLACK = 5
    WHITE = 6
    CAMO = 7
    """Currently not protected like normal game rules."""
    LEAD = 8
    """Currently not protected like normal game rules."""
    ZEBRA = 9
    RAINBOW = 10
    CERAMIC = 11
    MOAB = 12
    BFB = 13
    ZOMG = 14


class Maps(Enum):
    CARDS = 1
    DREADBLOON = 2
    DUNGEON = 3
    MOUNTAIN_PASS = 4


class Monkeys(Enum):
    """
    An enum representing all available monkeys.

    Keep in mind that not all BTD Battles monkeys are available.
    """

    DART_MONKEY = 0
    TACK_SHOOTER = 1
    NINJA_MONKEY = 2
    SUPER_MONKEY = 3


class EcoBloons(Enum):
    """
    An enum representing available eco bloons, i.e. bloons to send to opponents. See `Context.send_bloons`.

    Keep in mind that not all BTD Battles monkeys are available.
    """

    GROUPED_RED = (0,)
    SPACED_BLUE = (1,)
    GROUPED_BLUE = (2,)
    SPACED_PINK = (3,)
    GROUPED_GREEN = (4,)
    SPACED_BLACK = (5,)
    GROUPED_YELLOW = (6,)
    SPACED_WHITE = (7,)
    GROUPED_PINK = (8,)
    SPACED_LEAD = (9,)
    GROUPED_WHITE = (10,)
    SPACED_ZEBRA = (11,)
    GROUPED_BLACK = (12,)
    SPACED_RAINBOW = (13,)
    GROUPED_ZEBRA = (14,)
    GROUPED_RAINBOW = (15,)
    GROUPED_LEAD = (16,)
    SPACED_CERAMIC = (17,)
    FAST_COOLDOWN_CERAMIC = (18,)
    MOAB = (19,)
    FAST_COOLDOWN_MOAB = (20,)
    BFB = (21,)
    FAST_COOLDOWN_BFB = (22,)
    ZOMG = (23,)
    FAST_COOLDOWN_ZOMG = (24,)


class Exceptions(Enum):
    """
    An enum representing result of API methods.
    See each method for a list of possible exceptions.
    If a method was successful, it always returns `OK`.
    """

    OK = 0
    NOT_ENOUGH_MONEY = 1
    OUT_OF_MAP = 2
    """The specified position is outside of the map borders."""
    TOO_CLOSE_TO_BLOON_ROUTE = 3
    TOO_CLOSE_TO_OTHER_MONKEY = 4
    INVALID_MONKEY_INDEX = 5
    """The specified monkey index argument is not a valid index of the player's monkeys."""
    INVALID_BLOON_INDEX = 6
    """The specified bloon index argument is not a valid index of the player's bloons."""
    MONKEY_CANT_SEE = 7
    """The monkey cannot target the specified bloon because it is outside of its range."""
    OTHER_ROW_CHOSEN = 8
    """The upgrade cannot be completed because the monkey was already upgraded on the other row beyond Level 2."""
    INVALID_PLAYER = 9
    """The specified player is either yourself, an inactive player or an invalid player index."""
    ECO_QUEUE_FULL = 10
    """You sent too many eco bloons which have yet been sent. Your queue of size 5 is filled."""
    TOO_EARLY = 11
    """The specified eco bloons are only available in the future."""
    ALREADY_MAXED_OUT = 12
    """The monkey is already upgraded to level 4 in the selected path."""

    def __bool__(self):
        return self == Exceptions.OK


class BloonInfo:
    type: Bloons
    """The type (usually color) of the bloon."""
    position: tuple[float, float]
    """The position of the bloon, as a tuple of (x, y)."""
    index: int
    """
    The index of the bloon.
    
    **Important:** This may change between repeated calls to `ArazimBattlesBot.run`!
    """
    uid: int
    """
    The unique id of the bloon.
    This is guaranteed to be unique and persistent, but it is for your usage only.
    When targeting a bloon, you must use it's **current** index.
    """

    def __init__(
        self, type: Bloons, position: tuple[float, float], index: int, uid: int
    ) -> None:
        self.type = type
        self.position = position
        self.index = index
        self.uid = uid


class MonkeyInfo:
    type: Monkeys
    position: tuple[float, float]
    """The position of the monkey, as a tuple of (x, y)."""
    top_level: int
    bottom_level: int
    direction: float
    """The direction the monkey is facing: 0 for up, `math.pi / 2` for right etc."""

    def __init__(
        self,
        type: Monkeys,
        position: tuple[float, float],
        top_level: int,
        bottom_level: int,
        direction: float,
    ) -> None:
        self.type = type
        self.position = position
        self.top_level = top_level
        self.bottom_level = bottom_level
        self.direction = direction


class LineInfo:
    start: tuple[float, float]
    """The start position (x,y) of the line, in pixels."""
    end: tuple[float, float]
    """The end position (x,y) of the line, in pixels."""

    def __init__(self, start: tuple[float, float], end: tuple[float, float]) -> None:
        self.start = start
        self.end = end


class Context:
    """
    The main access point for your bot. Access this using `self.context` inside your `run` method.

    Each action method returns `Exceptions`, which is `Exceptions.OK` if it succeeded, or another value explaining why it failed.
    """

    def __init__(self) -> None:
        pass

    ### GENERAL GAME METHODS ###

    def get_player_count(self) -> int:
        """Returns the amount of players in the player list."""
        raise NotImplementedError("GetPlayerCount")

    def get_current_ticks(self) -> int:
        """
        Returns the elapsed time of the game in ticks.
        There are 20 ticks in every second.
        """
        raise NotImplementedError("GetCurrentTicks")

    def get_current_time(self) -> float:
        """
        Returns the elapsed time of the game in seconds.
        If the time is a precise second, it returns an int instead.
        """
        raise NotImplementedError("GetCurrentTime")

    def get_map(self) -> Maps:
        """Returns the map of the current game."""
        raise NotImplementedError("GetMap")

    def get_bloon_route(self) -> list[LineInfo]:
        """Returns the map's bloon route."""
        raise NotImplementedError("GetBloonRoute")

    def get_eco_bloon_route(self) -> list[LineInfo]:
        """Returns the map's eco bloon route."""
        raise NotImplementedError("GetEcoBloonRoute")

    ### CURRENT PLAYER METHODS ###

    def get_current_player_index(self) -> int:
        """Returns the index of the current player in the player list."""
        raise NotImplementedError("GetCurrentPlayerIndex")

    def get_money(self) -> int:
        """Returns the current amount of money the player possesses."""
        raise NotImplementedError("GetMoney")

    def get_eco(self) -> int:
        """
        Returns the current eco the player has.
        This is added to the players' money pool every 5 seconds.
        """
        raise NotImplementedError("GetEco")

    def get_eco_queue_size(self) -> int:
        """
        Returns the current filled size of the players' eco queue.
        If this is five, it means you cannot send more eco bloons now.
        """
        raise NotImplementedError("GetEco")

    def get_bloons(self) -> list[BloonInfo]:
        """Returns the current bloons in the players' map."""
        raise NotImplementedError("GetBloons")

    def get_monkey_cooldown(self, monkey_index: int) -> float:
        """
        Returns the current cooldown of the given monkey in seconds.
        During this time, the monkey will not be able to attack!
        If the `monkey_index` is invalid, returns -1.
        """
        raise NotImplementedError("GetMonkeyCooldown")

    def get_monkey_targets(self, monkey_index: int) -> list[BloonInfo]:
        """
        Returns the bloons the specified monkey can see.
        If the monkey_index is invalid, returns an empty list.
        """
        raise NotImplementedError("GetMonkeyTargets")

    def place_monkey(self, type: Monkeys, position: tuple[float, float]) -> Exceptions:
        """
        Places a monkey with the given type in the given (x,y) position on the players' board.
        Returns whether the operation was successful.

        Possible exceptions: `Exceptions.NOT_ENOUGH_MONEY`, `Exceptions.OUT_OF_MAP`, `Exceptions.TOO_CLOSE_TO_BLOON_ROUTE`, `Exceptions.TOO_CLOSE_TO_OTHER_MONKEY`.
        """
        raise NotImplementedError("PlaceMonkey")

    def target_bloon(self, monkey_index: int, bloon_index: int) -> Exceptions:
        """
        Sets the specified bloon as the target for the specified monkey.
        Returns whether the operation was successful.

        Possible exceptions: `Exceptions.INVALID_MONKEY_INDEX`, `Exceptions.INVALID_BLOON_INDEX`, `Exceptions.MONKEY_CANT_SEE`.
        """
        raise NotImplementedError("TargetBloon")

    def upgrade_monkey(self, monkey_index: int, top_row: bool) -> Exceptions:
        """
        Upgrades the specified monkey in the specified row.
        For more information, read Monkey Upgrades.
        Returns whether the operation was successful.

        Possible exceptions: `Exceptions.INVALID_MONKEY_INDEX`, `Exceptions.OTHER_ROW_CHOSEN`, `Exceptions.NOT_ENOUGH_MONEY`, `Exceptions.ALREADY_MAXED_OUT`.
        """
        raise NotImplementedError("UpgradeMonkey")

    def send_bloons(self, player_index: int, bloon: EcoBloons) -> Exceptions:
        """
        Sends the given eco bloons to the specified player.
        Keep in mind that you only have a queue of 5 eco bloons to send out.

        Grouped and fast-cooldown bloons take 5 seconds to send out, while spaced and regular zeppelins take 8 seconds to send out.

        Returns whether the operation was successful.

        Possible exceptions: `Exceptions.INVALID_PLAYER`, `Exceptions.NOT_ENOUGH_MONEY`, `Exceptions.TOO_EARLY`.
        """
        raise NotImplementedError("TargetBloon")

    ### OTHER PLAYER INFORMATION ###

    def is_player_active(self, player_index: int) -> bool:
        """
        Returns whether the player is alive (active).
        If the `player_index` is invalid, returns False.
        """
        raise NotImplementedError("IsPlayerActive")

    def get_player_monkeys(self, player_index: int) -> list[MonkeyInfo]:
        """
        Returns the current monkeys in the given players' map.
        If the `player_index` is invalid, returns an empty list.
        """
        raise NotImplementedError("GetPlayerMonkeys")

    def get_player_bloons(self, player_index: int) -> list[BloonInfo]:
        """
        Returns the current bloons in the given players' map.
        If the `player_index` is invalid, returns an empty list.
        """
        raise NotImplementedError("GetPlayerBloons")


class ArazimBattlesBot:
    """
    Base class for writing your bots.

    **Important:** Your bot must subclass this directly, and be called MyBot!

    **Important:** Your bot must not have a custom __init__ method. Use `setup` for any setup code you may have.

    **Example:**

    ```python
    class MyBot(ArazimBattlesBot):
        def setup(self):
            self.message = "Hello!"
        def run(self):
            if self.context.get_time() == 2:
                print(self.message)
    ```
    """

    context: Context

    def __init__(self, context: Context):
        self.context = context
        self.setup()

    def setup(self) -> None:
        """
        This optional method will be called upon construction.

        If you need to define any instance variables like in a constructor, do it here.
        """

    def run(self) -> None:
        """
        This method will be called once every game step.

        Interact with the game using `self.context`.
        """
