from api import ArazimBattlesBot, EcoBloons, Exceptions, Monkeys, Maps
import math



class MyBot(ArazimBattlesBot):
    monkey_count = 0
    monkey_levels = []
    attempted_position =  5
    attempted_position_y = 5

    koz = False
    
    bank = []
    bank_points_prioritues = {}
    
    def create_bank(self):
        for p1, p2 in self.context.get_bloon_route():
            self.bank.append((math.floor((p1[0] + 3 * p2[0])/4), math.floor((p1[1] + 3 * p2[1])/4)))
    
    def update_bank(self):
        pass
    
    def setup(self) -> None:
        self.create_bank()
    
    def place_near_point(self, type: Monkeys, point: tuple(float, float)) -> Exception:
        ops = [point]
        p = ops.pop(0)
        res = self.context.place_monkey(type, p)
        count = 0
        while (res != Exceptions.OK and count < 100):
            count += 1
            if res in [Exceptions.OUT_OF_MAP, Exceptions.TOO_CLOSE_TO_BLOON_ROUTE, Exceptions.TOO_CLOSE_TO_OTHER_MONKEY]:
                ops.append((p[0] + 3, p[1]), (p[0] - 3, p[1]), (p[0], p[1] + 3), (p[0], p[1] - 3))
                p = ops.pop(0)
            else:
                break

        if res == Exceptions.OK:
            self.monkey_count += 1
            self.monkey_levels.append(0)
        return res
    
    def run(self) -> None:
        
        # kozim:
        if not koz:
            pre_last_point = self.context.get_bloon_route()[-1][0]
            if self.context.get_map() == Maps.DUNGEON:
                point = (240, 630)
                res = self.context.place_monkey(Monkeys.TACK_SHOOTER, point)
                if res == Exceptions.OK:
                    koz = True
            else:
                point = pre_last_point[0] + 15, pre_last_point[1]
                res = self.context.place_monkey(Monkeys.TACK_SHOOTER, point)
                if res == Exceptions.OK:
                    koz = True
        
        if self.context.get_current_time() % 10 == 0:
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

        for monkey_index in range(self.monkey_count):
            # Upgrade Monkeys
            if self.context.get_current_time() > 20:
                if self.monkey_levels[monkey_index] == 0:
                    if self.context.upgrade_monkey(monkey_index, True):
                        self.monkey_levels[monkey_index] += 1
                elif self.monkey_levels[monkey_index] < 5:
                    if self.context.upgrade_monkey(monkey_index, False):
                        self.monkey_levels[monkey_index] += 1

            # Target Bloons
            targets = self.context.get_monkey_targets(monkey_index)
            if len(targets) > 0:
                self.context.target_bloon(monkey_index, targets[0].index)
        
        self.update_bank()