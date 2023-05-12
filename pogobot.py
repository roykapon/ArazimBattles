from api import ArazimBattlesBot, EcoBloons, Exceptions, Monkeys


class MyBot(ArazimBattlesBot):
    monkey_count = 0
    monkey_levels = []
    attempted_position =  5
    attempted_position_y = 5

    def run(self) -> None:
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