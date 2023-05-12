from api import ArazimBattlesBot, EcoBloons, Exceptions, Monkeys, Maps
import math


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

    koz = False
    
    bank = []
    bank_points_prioritues = {}
    
    def create_bank(self):
        for p in self.context.get_bloon_route():
            p1, p2 = p.start, p.end
            self.bank.append((math.floor((p1[0] + 3 * p2[0])/4), math.floor((p1[1] + 3 * p2[1])/4)))
    
    def update_bank(self):
        pass
    
    def setup(self) -> None:
        self.create_bank()
    
    def place_near_point(self, type: Monkeys, point) -> Exception:
        ops = [point]
        p = ops.pop(0)
        res = self.context.place_monkey(type, p)
        count = 0
        while (res != Exceptions.OK and count < 100):
            count += 1
            res = self.context.place_monkey(type, p)
            if res in [Exceptions.OUT_OF_MAP, Exceptions.TOO_CLOSE_TO_BLOON_ROUTE, Exceptions.TOO_CLOSE_TO_OTHER_MONKEY]:
                ops += [(p[0] + 3, p[1]), (p[0] - 3, p[1]), (p[0], p[1] + 3), (p[0], p[1] - 3)]
                p = ops.pop(0)
            else:
                break

        if res == Exceptions.OK:
            self.monkey_count += 1
            self.monkey_levels.append(0)
        return res
    
    def run(self) -> None:
        
        # kozim:

        if self.context.get_current_time() % BALOON_INTERVAL in [1,2,3]:
            self.send_baloons()
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
            index += 1

            print(f'in loop {index}')
            # Place Monkeys
            position = self.bank.pop(0)
            print(f'position: {position}')
            result = self.place_near_point(Monkeys.NINJA_MONKEY, position) 
            self.bank.append(position)
        if 24 * self.attempted_position + 24 > 200:
            self.attempted_position_y += 1
            self.attempted_position = 5
    
    def upgrade_monkeys(self):
        for monkey_index in range(self.monkey_count):
            if self.monkey_levels[monkey_index] < 4:
                if self.context.upgrade_monkey(monkey_index, True):
                    self.monkey_levels[monkey_index] += 1
    
    def target_baloons(self):
        for monkey_index in range(self.monkey_count):
            targets = self.context.get_monkey_targets(monkey_index)
            if len(targets) > 0:
                self.context.target_bloon(monkey_index, targets[0].index)
        self.update_bank()
    
    def get_player_index(self):
        my_index = self.context.get_current_player_index()
        num_players = self.context.get_player_count()
        for i in list(range(num_players)):
            if i != my_index:
                return i
        return -1

    def send_baloons(self):
        result = self.context.send_bloons(self.get_player_index(), get_ballon_type(self.context.get_current_time())['packed'])
        print(result)