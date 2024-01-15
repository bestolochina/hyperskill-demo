class CoffeeMachine:
    def __init__(self):
        self.storage = {'water': 400, 'milk': 540, 'coffee beans': 120, 'disposable cups': 9, 'money': 550}
        self.recipies = {
            '1': {'water': 250, 'milk': 0, 'coffee beans': 16, 'disposable cups': 1, 'money': -4},
            '2': {'water': 350, 'milk': 75, 'coffee beans': 20, 'disposable cups': 1, 'money': -7},
            '3': {'water': 200, 'milk': 100, 'coffee beans': 12, 'disposable cups': 1, 'money': -6}}
        self.refill_messages = {'water': 'Write how many ml of water you want to add: ',
                                'milk': 'Write how many ml of milk you want to add: ',
                                'coffee beans': 'Write how many grams of coffee beans you want to add: ',
                                'disposable cups': 'Write how many disposable cups you want to add: '}

    def action(self):
        while True:
            action = input('Write action (buy, fill, take, remaining, exit): ')
            if action == 'exit':
                break
            elif action == 'remaining':
                self.display_content()
            elif action == 'buy':
                self.sell()
            elif action == 'fill':
                self.fill_machine()
            elif action == 'take':
                self.give_money()

    def display_content(self):
        print(f'''The coffee machine has:
{self.storage['water']} ml of water
{self.storage['milk']} ml of milk
{self.storage['coffee beans']} g of coffee beans
{self.storage['disposable cups']} disposable cups
${self.storage['money']} of money''')

    def give_money(self):
        print(f'I gave you ${self.storage['money']}')
        self.storage['money'] = 0

    def fill_machine(self):
        for item in list(self.storage.keys())[:-1]:
            amount = int(input(self.refill_messages[item]))
            self.storage[item] += amount

    def sell(self):
        coffee = input('What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu: ')
        if coffee == 'back':
            return
        missing = []
        for item in list(self.storage.keys())[:-1]:
            if self.storage[item] < self.recipies[coffee][item]:
                missing.append(item)
        if missing:
            missing_list = ', '.join(x for x in missing)
            print(f'Sorry, not enough {missing_list}!')
            return
        print('I have enough resources, making you a coffee!')
        for item in self.storage.keys():
            self.storage[item] -= self.recipies[coffee][item]


def main():
    machine = CoffeeMachine()
    machine.action()


if __name__ == '__main__':
    main()
