from player import Player
from item import Item
from room import Room

# Declare all the rooms

room = {
    'outside':  Room("Outside Cave Entrance",
                     "North of you, the cave mount beckons"),

    'foyer':    Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east."""),

    'overlook': Room("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm."""),

    'narrow':   Room("Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air."""),

    'treasure': Room("Treasure Chamber", """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south."""),
}


# Link rooms together

room['outside'].n_to = room['foyer']
room['foyer'].s_to = room['outside']
room['foyer'].n_to = room['overlook']
room['foyer'].e_to = room['narrow']
room['overlook'].s_to = room['foyer']
room['narrow'].w_to = room['foyer']
room['narrow'].n_to = room['treasure']
room['treasure'].s_to = room['narrow']

#
# Main
#

items = {
    'key-1': Item("key", "This key could unlock a door!"),
    'potion': Item("potion", "Drinking this could have an unknown effect."),
    'chicken': Item("chicken", "This savory chicken restores 3 hunger.")
}

room['foyer'].items = [items['key-1']]
room['narrow'].items = [items['potion']]
room['overlook'].items = [items['chicken']]

# Make a new player object that is currently in the 'outside' room.
bash = Player("Bash", room['outside'])

# Write a loop that:
#
# * Prints the current room name
# * Prints the current description (the textwrap module might be useful here).
# * Waits for user input and decides what to do.
#
# If the user enters a cardinal direction, attempt to move to the room there.
# Print an error message if the movement isn't allowed.
#
# If the user enters "q", quit the game.

response = ""

directions = """
The path splits ahead. Choose a direction:
    n. North    e. East    s. South    w. West
"""

options = {'n': 'n_to', 's': 's_to', 'e': 'e_to',
           'w': 'w_to', 'take': 'take', 'get': 'take',
           'drop': 'drop', 'i': 'i', 'inventory': 'i'}


def take(player, room, item_name):
    if item_name in [i.name for i in room.items]:
        item = [i for i in room.items if i.name == item_name][0]
        player.inventory.append(item)
        room.items.remove(item)
        item.on_take()
    else:
        print('That item is not here.')


def drop(player, room, item_name):
    if item_name in [i.name for i in player.inventory]:
        item = [i for i in player.inventory if i.name == item_name][0]
        room.items.append(item)
        player.inventory.remove(item)
        item.on_drop()
    else:
        print('You do not have that item.')


action = {
    'take': take,
    'drop': drop
}


def move_player(player, room):
    player.move_to(room)


while response != "q":
    current_room = bash.current_room
    print(current_room)
    response = input(directions).split()
    try:
        selection = options[response[0]]
        if selection in ("take", "drop"):
            action[selection](bash, current_room, response[1])
        elif selection is 'i':
            print('Inventory:')
            for item in bash.inventory:
                print(f'> {item}')
        else:
            try:
                bash.move_to(getattr(current_room, selection))
            except AttributeError:
                print('\nThere is no path in that direction\n')
    except KeyError:
        print('\nThat is not a valid selection\n')
    except IndexError:
        print('\nPlease make a selection.\n')

print("Thanks for playing!")
