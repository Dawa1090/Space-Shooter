import pygame 
import time
import random

from models.models import CONN, CURSOR, Player, Score
from helpers import delete_player

pygame.font.init()

WIDTH, HEIGHT = 600, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

BG = pygame.transform.scale(pygame.image.load("lib/images/bg.jpg"), (WIDTH, HEIGHT))

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 40

PLAYER_VEL = 5
STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 3

FONT = pygame.font.SysFont("comicsans", 45)

def draw(player, elapsed_time, stars, username):
     WIN.blit(BG, (0, 0))

     username_text = FONT.render(f"Player: {username}", 1, "white")
     WIN.blit(username_text, (10, 10))

     time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
     WIN.blit(time_text, (10, 100))
    
     pygame.draw.rect(WIN, "orange", player)

     for star in stars:
          pygame.draw.rect(WIN, "white", star)

     pygame.display.update()



def main():
    print("Enter your username:")
    username = input(" > ")

    player_from_database = Player.load(username)
    if not player_from_database:
        player_from_database = Player.create(username)
        print(f"Hello {player_from_database.username}!")
    else:
        print(f"Welcome back {player_from_database.username}!")
        delete_player(player_from_database)

    run = True
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0

    stars = []
    hit = False

    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time


        if star_count > star_add_increment:
             for _ in range(3):
                   star_x = random.randint(0, WIDTH - STAR_WIDTH)
                   star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                   stars.append(star)

             star_add_increment = max(200, star_add_increment - 50)
             star_count = 0
             

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
             player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
             player.x += PLAYER_VEL

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        if hit:
            lost_text = FONT.render("You Lost!", 1, "white")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        draw(player, elapsed_time, stars, player_from_database.username)

    print(elapsed_time)
    Score.create(player_from_database.id, int(elapsed_time * 100))
    pygame.quit()

if __name__ == "__main__":
        Player.create_table()
        Player.get_all()
        Score.create_table()
        Score.get_all()
        main()