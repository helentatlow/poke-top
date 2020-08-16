import random as rd
import requests
import inflect
import time

p = inflect.engine()


# defining function to generate decks from API
def generate_two_pokemon_decks(cards):
    pokemon_ids = list(rd.sample(range(1, 152), k=cards))
    two_pokemon_decks = []
    for pokemon_id in pokemon_ids:
        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}/'
        response = requests.get(url)
        pokemon = response.json()
        pokemon_dict = {
            'name': pokemon['name'],
            'hp': pokemon['stats'][0]['base_stat'],
            'attack': pokemon['stats'][1]['base_stat'],
            'defence': pokemon['stats'][2]['base_stat'],
            'special attack': pokemon['stats'][3]['base_stat'],
            'special defence': pokemon['stats'][4]['base_stat']
        }
        two_pokemon_decks.append(pokemon_dict)
    return two_pokemon_decks


# greet player
print("Welcome to Top Trumps, Pokemon Edition!")
time.sleep(2)

# determine deck size via input, with exception handling
while True:
    try:
        number_of_cards_per_deck = int(input('How many cards should be in each deck? (max 10): '))
        if number_of_cards_per_deck in range(1, 11):
            break
        else:
            print("Sorry, the number of cards should be between 1 and 10. Let's try again.")
            time.sleep(1)
    except ValueError:
        print("Sorry, the number of cards should be between 1 and 10. Let's try again.")
        time.sleep(1)

total_number_of_cards = 2 * number_of_cards_per_deck

# use function to create the decks
pokemon_decks = generate_two_pokemon_decks(total_number_of_cards)

# separate into two decks using slicing
my_pokemon_deck = list(pokemon_decks[:len(pokemon_decks)//2]) # first half
opponent_pokemon_deck = list(pokemon_decks[len(pokemon_decks)//2:]) # second half

# initialise round counting and card counting
my_number_of_cards = number_of_cards_per_deck
round_number = 1

# play game - while loop runs until player has all cards or no cards
while my_number_of_cards in range(1, total_number_of_cards):

    # listing the pokemon in the deck
    print(f'Round {round_number}! Your pokemon deck:')

    for i, pokemon_in_deck in enumerate(my_pokemon_deck):
        time.sleep(0.5)
        print("{}. {}".format(i + 1, my_pokemon_deck[i]['name']))

    time.sleep(1)

    # using a random integer to select opponent pokemon
    opponent_choice = rd.randint(1, total_number_of_cards - my_number_of_cards)
    opponent_pokemon = opponent_pokemon_deck[int(opponent_choice) - 1]

    # player selects pokemon via input, with exception handling
    if my_number_of_cards == 1:
        while True:
            try:
                pokemon_choice = input(f"You only have 1 card left. Enter '1' to play: ")
                my_pokemon = my_pokemon_deck[int(pokemon_choice) - 1]
                break
            except IndexError:
                print("Sorry, I didn't understand that. Let's try again.")
                time.sleep(1)
            except ValueError:
                print("Sorry, I didn't understand that. Let's try again.")
                time.sleep(1)

    else:
        while True:
            try:
                pokemon_choice = input(f"Which pokemon will you choose? (Enter a number from 1 to {my_number_of_cards}): ")
                my_pokemon = my_pokemon_deck[int(pokemon_choice) - 1]
                break
            except IndexError:
                print("Sorry, I didn't understand that. Let's try again.")
                time.sleep(1)
            except ValueError:
                print("Sorry, I didn't understand that. Let's try again.")
                time.sleep(1)

    print(f"Your pokemon is {my_pokemon['name']}.")

    # player selects stat via input, with exception handling
    # Bonus stat categories once player has >75% of total cards
    keys = my_pokemon.keys()

    if my_number_of_cards < 0.75 * total_number_of_cards:
        while True:
            try:
                stat_choice = input('Which stat will you choose? (hp/attack/defence): ').lower()
                if stat_choice in keys and stat_choice not in ['special attack', 'special defence']:
                    break
                else:
                    print("Please choose from the stats listed.")
                    time.sleep(1)
            except ValueError:
                print("Please choose from the stats listed.")
                time.sleep(1)

    else:
        while True:
            try:
                stat_choice = input('Which stat will you choose? (hp/attack/defence/special attack/special defence): ').lower()
                if stat_choice in keys:
                    break
                else:
                    print("Please choose from the stats listed.")
                    time.sleep(1)
            except ValueError:
                print("Please choose from the stats listed.")
                time.sleep(1)

    # programme compares the stats and determines winner
    my_stat = my_pokemon[stat_choice]
    opponent_stat = opponent_pokemon[stat_choice]

    print(f"Your {stat_choice} is {my_stat}.")
    time.sleep(1)
    print(f"Your opponent has {opponent_pokemon['name']}. Your opponent's {stat_choice} is {opponent_stat}.")
    time.sleep(1)

    if my_stat > opponent_stat:
        print("You win this round!")
        my_number_of_cards += 1
        opponent_pokemon_deck.remove(opponent_pokemon)
        my_pokemon_deck.append(opponent_pokemon)

    elif my_stat < opponent_stat:
        print('You lose this round.')
        my_number_of_cards -= 1
        my_pokemon_deck.remove(my_pokemon)
        opponent_pokemon_deck.append(my_pokemon)

    else:
        print("It's a draw for this round.")
        my_number_of_cards = my_number_of_cards

    round_number += 1

    print("You've got " + p.no("card", my_number_of_cards) + ".\n")
    time.sleep(2)


# exit the while loop when player has 0 cards (player has lost) or all the cards (player has won)
if my_number_of_cards == 0:
    print("Bad luck! Your opponent has won the game.")

else:
    print("Congratulations! You've won the game!")
