from api import ArazimBattlesBot, EcoBloons, Exceptions, Monkeys

BALOON_INTERVAL = 20
MONKEY_INTERVAL = 15

def get_ballon_type(time):
    if 29 <= time and time <= 68:
        return {'spaced': EcoBloons.GROUPED_RED, 'packed': EcoBloons.SPACED_BLUE}
    if time <= 122:
        return {'spaced': EcoBloons.GROUPED_BLUE, 'packed': EcoBloons.SPACED_PINK}
    if time <= 161:
        return {'spaced': EcoBloons.GROUPED_GREEN, 'packed': EcoBloons.SPACED_BLACK}
    if time <= 196:
        return {'spaced': EcoBloons.GROUPED_YELLOW, 'packed': EcoBloons.SPACED_WHITE}
    if time <= 237:
        return {'spaced': EcoBloons.GROUPED_PINK, 'packed': EcoBloons.SPACED_LEAD}
    if time <= 275:
        return {'spaced': EcoBloons.GROUPED_WHITE, 'packed': EcoBloons.SPACED_ZEBRA} 
    return {'spaced': EcoBloons.GROUPED_BLACK, 'packed': EcoBloons.SPACED_RAINBOW}

class MyBot(ArazimBattlesBot):
    monkey_count = 0
    monkey_levels = []
    attempted_position =  5
    attempted_position_y = 5

    def run(self) -> None:
        if self.context.get_current_time() % BALOON_INTERVAL in [1,2,3]:
            result = self.context.send_bloons(0, get_ballon_type(self.context.get_current_time())['spaced'])
            print(result)
        if self.context.get_current_time() % MONKEY_INTERVAL == 0:
            self.place_monkeys()
        
        self.upgrade_monkeys()
        self.target_baloons()


    def place_monkeys(self):
        result = Exceptions.OUT_OF_MAP
        index = 0
        while result != Exceptions.OK and result != Exceptions.NOT_ENOUGH_MONEY:
            if index > 100:
                break
            print(f'in loop {index}')
            # Place Monkeys
            result = self.context.place_monkey(
                Monkeys.DART_MONKEY, (24 * self.attempted_position + 24, 24 * self.attempted_position_y + 24)
            )
            if result == Exceptions.OK:
                self.monkey_count += 1
                self.monkey_levels.append(0)
            elif (
                result == Exceptions.OUT_OF_MAP
                or result == Exceptions.TOO_CLOSE_TO_BLOON_ROUTE
                or result == Exceptions.TOO_CLOSE_TO_OTHER_MONKEY
            ):
                self.attempted_position += 1
            index += 1
        if 24 * self.attempted_position + 24 > 200:
            self.attempted_position_y += 1
            self.attempted_position = 5
    
    def upgrade_monkeys(self):
        for monkey_index in range(self.monkey_count):
            if self.monkey_levels[monkey_index] == 0:
                if self.context.upgrade_monkey(monkey_index, True):
                    self.monkey_levels[monkey_index] += 1
            elif self.monkey_levels[monkey_index] < 5:
                if self.context.upgrade_monkey(monkey_index, False):
                    self.monkey_levels[monkey_index] += 1
    
    def target_baloons(self):
        for monkey_index in range(self.monkey_count):
            targets = self.context.get_monkey_targets(monkey_index)
            if len(targets) > 0:
                self.context.target_bloon(monkey_index, targets[0].index)
