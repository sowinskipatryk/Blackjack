import random
import time

STAKE = 10
START_POCKET = 1000

cards_values = {
    'A': 11,
    'K': 10,
    'Q': 10,
    'J': 10,
    '10': 10,
    '9': 9,
    '8': 8,
    '7': 7,
    '6': 6,
    '5': 5,
    '4': 4,
    '3': 3,
    '2': 2,
}


class Hand:

    def __init__(self):
        self.cards = []
        self.value = 0

    def draw_cards(self, num):
        while num:
            card_id = random.choice(list(cards_values))
            card_val = cards_values[card_id]

            self.cards.append(card_id)
            self.value += card_val

            num -= 1

    def show(self):
        print(f'Cards: ', end="")
        for card in self.cards:
            print(f'[{card}]', end=" ")
        time.sleep(0.5)
        print(f'\nValue: {self.value}\n')
        time.sleep(2)

    def is_bust(self):
        if self.value > 21:
            return True
        else:
            return False

    def ace_value(self):
        if any(card == 'A' for card in self.cards) and self.value > 21:
            idx = self.cards.index('A')
            self.cards[idx] = 'A*'
            self.value -= 10


class Player(Hand):

    def decision(self, other):
        while True:
            if self.value < 21:
                answer = input('What\'s your decision? (H)it / (S)tand: ')
                print('')
                if answer.upper() == 'H':
                    print('Player draws another card:')
                    self.draw_cards(1)
                    self.ace_value()
                    self.show()
                    continue
                elif answer.upper() == 'S':
                    return False
            else:
                return True
        other.show()

    def is_blackjack(self):
        if self.value == 21 and len(self.cards) == 2:
            return True
        else:
            return False


class Opponent(Hand):
    def decision(self, other):
        while self.value < 17 and self.value < other.value:
            time.sleep(2)
            print('Opponent draws another card:')
            self.draw_cards(1)
            self.ace_value()
            self.show()

def main():

    play = True
    balance = START_POCKET
    rounds = 0

    print('Welcome to Blackjack!\n')
    time.sleep(2)

    while play:
        player_hand = Player()
        opp_hand = Opponent()
        score = -STAKE
        rounds += 1

        print('Drawing player\'s cards:')
        time.sleep(2)
        player_hand.draw_cards(2)
        blackjack = player_hand.is_blackjack()
        player_hand.show()

        if blackjack:
            score += STAKE*2.5
            print('Blackjack!')
        else:
            print('Drawing opponent\'s card:')
            time.sleep(2)
            opp_hand.draw_cards(1)
            opp_hand.show()
            player_hand.decision(opp_hand)
            player_bust = player_hand.is_bust()
            if player_bust:
                print('Player busted!')
            else:
                opp_hand.decision(player_hand)
                opp_busted = opp_hand.is_bust()
                if opp_busted:
                    score += STAKE*2
                    print('Opponent busted!')
                elif player_hand.value == opp_hand.value:
                    score += STAKE
                    print('It\'s a draw.')
                elif player_hand.value > opp_hand.value:
                    score += STAKE*2
                    print('Player wins!')
                else:
                    print('Opponent wins!')

        balance += score

        print('Round score:', int(score))
        print(f'Balance:', int(balance))
        while True:
            answer = input('\nDo you want to play again? (Y)es/(N)o: ')
            print('')
            if answer.upper() == 'Y':
                break
            elif answer.upper() == 'N':
                play = False
                break
            else:
                print('Answer the question.')
    print(f'You played {rounds} round(s) and your total gain/loss is {int(balance-START_POCKET)} points.')


if __name__ == "__main__":
    main()
