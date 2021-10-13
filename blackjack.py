from random import choice

def draw_card(deck, hand, value):
    draw = choice(list(deck.items()))
    hand.append(draw[0])
    value.append(draw[1])
    return hand, value

def players_evaluation(players_value, points):
    players_score = sum(players_value)
    while True:
        if players_score == 21:
            game_status(players_hand, players_value, croupiers_hand, croupiers_value)
            points += 10
            print(f'Blackjack! You win {points} points!')
            return points
        elif players_score > 21 and any(v == 11 for v in players_value):
            players_value = [1 if k == 11 else k for k in players_value]
            players_score = sum(players_value)
            continue
        elif players_score > 21:
            game_status(players_hand, players_value, croupiers_hand, croupiers_value)
            points -= 10
            print(f'Busted! You lose {-points} points!')
            return points
        else:
            game_status(players_hand, players_value, croupiers_hand, croupiers_value)
            points = drawpass(points)[4]
            return points

def croupiers_evaluation(players_value, croupiers_value, points):
    croupiers_score = sum(croupiers_value)
    players_score = sum(players_value)
    while True:
        if croupiers_score <= 16:
            draw_card(deck, croupiers_hand, croupiers_value)
            croupiers_score = sum(croupiers_value)
            continue
        elif croupiers_score > 21 and any(v == 11 for v in croupiers_value):
            croupiers_value = [1 if k == 11 else k for k in croupiers_value]
            croupiers_score = sum(croupiers_value)
            continue
        elif croupiers_score > 21:
            game_status(players_hand, players_value, croupiers_hand, croupiers_value)
            points = game_outcome(players_score, croupiers_score, points)
            return points
        elif croupiers_score > 16:
            game_status(players_hand, players_value, croupiers_hand, croupiers_value)
            points = game_outcome(players_score, croupiers_score, points)
            return points

def game_status(players_hand, players_value, croupiers_hand, croupiers_value):
    print('')
    print(f"Card(s) in croupier's hand: [{', '.join(croupiers_hand)}]")
    print('')
    print(f"The value of cards in croupier's hand: {sum(croupiers_value)}")
    print('')
    print(f"Cards in your hand: [{', '.join(players_hand)}]")
    print('')
    print(f"The value of cards in your hand: {(str(players_value)).replace(',', ' +')} = {sum(players_value)}")
    print('')
    return

def drawpass(points):
    while True:
        decision = input('What is your decision? (draw/pass) ')
        if decision.lower() == 'draw':
            draw_card(deck, players_hand, players_value)
            points = players_evaluation(players_value, points)
            return players_hand, players_value, croupiers_hand, croupiers_value, points
        elif decision.lower() == 'pass':
            print("\nCroupier's turn.")
            draw_card(deck, croupiers_hand, croupiers_value)
            points = croupiers_evaluation(players_value, croupiers_value, points)
            return players_hand, players_value, croupiers_hand, croupiers_value, points
        else:
            print('\nWrong decision.\n')
            continue
    return

def game_outcome(players_score, croupiers_score, points):
    if croupiers_score > 21:
        points += 10
        print(f'Croupier busted. You win {points} points!')
    elif croupiers_score > players_score:
        points -= 10
        print(f"Croupier hand's value ({croupiers_score}) is higher than yours ({players_score}). You lose {-points} points!")
    elif croupiers_score == players_score:
        print("It's a draw!")
    elif croupiers_score < players_score:
        points += 10
        print(f"Croupier hand's value ({croupiers_score}) is lower than yours ({players_score}). You win {points} points!")
    return points

def game(deck, players_hand, players_value, croupiers_hand, croupiers_value, points):
    draw_card(deck, players_hand, players_value)
    draw_card(deck, players_hand, players_value)
    draw_card(deck, croupiers_hand, croupiers_value)
    points = players_evaluation(players_value, points)
    return points

deck = {
    "Ace": 11,
    "King": 10,
    "Queen": 10,
    "Jack": 10,
    "10": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2
}

total = 0

play_again = 'yes'
while play_again == 'yes':
    points = 0
    players_hand = []
    players_value = []
    croupiers_hand = []
    croupiers_value = []
    points = game(deck, players_hand, players_value, croupiers_hand, croupiers_value, points)
    total += points
    while True:
        play_again = input('\nDo you want to play again? (yes/no) ')
        if play_again.lower() == 'yes':
            break
        elif play_again.lower() == 'no':
            print(f'\nYour total score is {total} points.')
            break
        else:
            print('\nWrong answer.')
            continue