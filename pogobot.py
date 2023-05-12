from api import ArazimBattlesBot, EcoBloons, Exceptions, Monkeys, Maps
import math


BALOON_INTERVAL = 20
MONKEY_INTERVAL = 15
SEARCH_STEP = 8
RATIO = 5/3

def get_ballon_type(time):
    if 29 <= time and time <= 68:
        return {'packed': EcoBloons.GROUPED_RED, 'spaced': EcoBloons.SPACED_BLUE}
    if time <= 122:
        return {'packed': EcoBloons.GROUPED_BLUE, 'spaced': EcoBloons.SPACED_PINK}
    if time <= 161:
        return {'packed': EcoBloons.GROUPED_GREEN, 'spaced': EcoBloons.SPACED_BLACK}
    if time <= 196:
        return {'packed': EcoBloons.GROUPED_YELLOW, 'spaced': EcoBloons.SPACED_WHITE}
    if time <= 237:
        return {'packed': EcoBloons.GROUPED_PINK, 'spaced': EcoBloons.SPACED_LEAD}
    if time <= 275:
        return {'packed': EcoBloons.GROUPED_WHITE, 'spaced': EcoBloons.SPACED_ZEBRA} 
    return {'packed': EcoBloons.GROUPED_BLACK, 'spaced': EcoBloons.SPACED_RAINBOW}

class MyBot(ArazimBattlesBot):
    monkey_count = 0
    monkey_levels = []
    attempted_position =  5
    attempted_position_y = 5
    our_monkeys = []

    koz = False
    
    banks = {Monkeys.NINJA_MONKEY: [], Monkeys.DART_MONKEY: []}
    
    def dist(self, p1, p2):
        return math.sqrt((p2[0]-p1[0]) ** 2 + (p2[1]-p1[1]) ** 2)
    
    def create_banks(self):
        for p in self.context.get_bloon_route():
            p1, p2 = p.start, p.end
            self.banks[Monkeys.NINJA_MONKEY].append((math.floor((p1[0] + 3 * p2[0])/4), math.floor((p1[1] + 3 * p2[1])/4)))
            # p2 + 24 * (p2-p1)/|p2 - p1|
            distance = self.dist(p1, p2)
            self.banks[Monkeys.DART_MONKEY].append((math.floor(p2[0] + SEARCH_STEP * (p2[0] - p1[0]) / distance), math.floor(p2[1] + SEARCH_STEP * (p2[1] - p1[1]) / distance)))
    
    def setup(self) -> None:
        self.create_banks()
    
    def place_near_point(self, type: Monkeys, point) -> Exception:
        ops = [point]
        p = ops.pop(0)
        res = self.context.place_monkey(type, p)
        count = 0
        good_exceptions =[Exceptions.OUT_OF_MAP, Exceptions.TOO_CLOSE_TO_BLOON_ROUTE, Exceptions.TOO_CLOSE_TO_OTHER_MONKEY] 
        while (res in good_exceptions and count < 200):
            count += 1
            ops += [(p[0] + SEARCH_STEP, p[1]), (p[0] - SEARCH_STEP, p[1]), (p[0], p[1] + SEARCH_STEP), (p[0], p[1] - SEARCH_STEP)]
            p = ops.pop(0)
            res = self.context.place_monkey(type, p)
        if res == Exceptions.OK:
            self.our_monkeys.append({'monkey_type': type, 'position': p, 'index': self.monkey_count})

        if res == Exceptions.OK:
            self.monkey_count += 1
            self.monkey_levels.append(0)
        return res
    
    def run(self) -> None:
        time = self.context.get_current_time()
        if time < 60:
            #build only ninja
            self.place_monkeys(Monkeys.NINJA_MONKEY)
        elif time < 196:
            self.place_monkeys(self.get_monkey_type())
            self.upgrade_monkeys()
        elif time < 230:
            self.upgrade_monkeys()
        else:
            self.send_baloons()
            self.upgrade_monkeys()
        
        self.target_baloons()
    
    def get_monkey_type(self):
        print(f'index {self.context.get_current_player_index()}')
        monkeys = self.our_monkeys
        darts = [monkey for monkey in monkeys if monkey['monkey_type'] == Monkeys.DART_MONKEY]
        ninjas = [monkey for monkey in monkeys if monkey['monkey_type'] == Monkeys.NINJA_MONKEY]
        if len(darts) == 0:
            return Monkeys.NINJA_MONKEY
        curr_ratio = len(ninjas) / len(darts)
        if curr_ratio > RATIO:
            return Monkeys.DART_MONKEY
        return Monkeys.NINJA_MONKEY


    def place_monkeys(self, type):
        result = Exceptions.OUT_OF_MAP
        index = 0
        while result != Exceptions.OK and result != Exceptions.NOT_ENOUGH_MONEY:
            if index > 100:
                break
            index += 1

            print(f'in loop {index}')
            # Place Monkeys
            position = self.banks[type].pop(0)
            print(f'position: {position}')
            result = self.place_near_point(type, position) 
            self.banks[type].append(position)
        if 24 * self.attempted_position + 24 > 200:
            self.attempted_position_y += 1
            self.attempted_position = 5
    
    def upgrade_monkeys(self):
        for monkey_index in range(self.monkey_count):
            if self.our_monkeys[monkey_index]["monkey_type"] == Monkeys.NINJA_MONKEY:
                if self.monkey_levels[monkey_index] < 0:
                    if self.context.upgrade_monkey(monkey_index, True):
                        self.monkey_levels[monkey_index] += 1
            else:
                if self.monkey_levels[monkey_index] < 4:
                    if self.context.upgrade_monkey(monkey_index, True):
                        self.monkey_levels[monkey_index] += 1
    
    def target_baloons(self):
        for monkey_index in range(self.monkey_count):
            targets = self.context.get_monkey_targets(monkey_index)
            if len(targets) > 0:
                self.context.target_bloon(monkey_index, targets[0].index)
        self.update_banks()
    
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