from api import ArazimBattlesBot, EcoBloons, Exceptions, Monkeys


class MyBot(ArazimBattlesBot):
    monkey_count = 0
    monkey_levels = []
    attempted_position = 0

    def run(self) -> None:
        if self.context.get_current_time() % 5 == 0:
            # Place Monkeys
            result = self.context.place_monkey(
                Monkeys.DART_MONKEY, (24 * self.attempted_position + 24, 400)
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

        for monkey_index in range(self.monkey_count):
            # Upgrade Monkeys
            if self.context.get_current_time() > 20:
                if self.monkey_levels[monkey_index] < 4:
                    if self.context.upgrade_monkey(monkey_index, True):
                        self.monkey_levels[monkey_index] += 1

            # Target Bloons
            targets = self.context.get_monkey_targets(monkey_index)
            if len(targets) > 0:
                self.context.target_bloon(monkey_index, targets[0].index)