# from models.models import Player

def delete_player(player_from_database):
    print("Would you like to delete your account? (yes / no)")
    user_input = input(" > ")
    while not (user_input.upper() in ['yes'.upper(), 'no'.upper()]):
        print("You must answer 'Yes' or 'No'! Please try again!")
        user_input = input(" > ")
    if user_input.upper() == 'yes'.upper():
        player_from_database.delete()
        print('Player deleted.')
        keyboard = input("* return to continue */n")