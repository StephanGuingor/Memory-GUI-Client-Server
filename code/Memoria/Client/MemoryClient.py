"""
Will handle the logic for the GUI
"""

import sys

from code.Memoria.Client.NetworkAssistant import Network
from code.Memoria.UI.GUIAssistant import *
from code.Memoria.UI.Board import Board

# LOADING IMAGES
bg_image = 'nbg.jpg'

# Initializes font module
pygame.init()
pygame.font.init()

# Initial Set Up
WIDTH = 700
HEIGHT = 700

win = pygame.display.set_mode((WIDTH, HEIGHT))  # Sets dimension of the screen
pygame.display.set_caption("Client")

effect = set_wind_particles_effect(win, WIDTH, HEIGHT) # creates particles


def quit_button():
    """
    A quit button
    """
    pass


def timer():
    """
    Displays time passed since the game started
    """
    pass


def game_logic(game, n, p1_banner, p2_banner, board):
    """
    Core logic for the game
    """
    p2_banner.set_name(other(n.p, game))  # Change Name?

    if game.get_player_move() == n.p:
        p1_banner.draw_turn('self')  # Shows whose turn is
        # p1_banner.draw_points('self')
    else:
        p2_banner.draw_turn('other')
        # p1_banner.draw_points('other')

    board.draw()  # draws cards to screen

    board.paint_card(game.selected, (255, 120, 30))

    # print(game.block)

    if pygame.mouse.get_pressed()[0]:
        print("Click")
        pos = pygame.mouse.get_pos()
        card_val = board.click(pos)

        if card_val is not None and n.p == game.get_player_move() and not game.block:
            print("send value")
            n.send(str(card_val))


def game_online_loop(name):
    """
    Runs the main game (online)
    """
    run = True
    clock = pygame.time.Clock()
    bg = Background(bg_image, (0, 0))

    p1_banner = PlayerBanner(win, name, 'cat.jpg', 0, HEIGHT / 10, WIDTH / 2.3, HEIGHT / 8, (255, 0, 0))
    p2_banner = PlayerBanner(win, "Waiting...", 'abs.jpg', WIDTH - (WIDTH / 1.4), HEIGHT / 10, WIDTH / 1.4, HEIGHT / 8,
                             side='r')

    n = Network()
    game = n.send('name ' + name)
    # print(len(game.back))
    board = Board(win, game.back, 5, HEIGHT // 8, WIDTH, HEIGHT, image='file.jpg',
                  dim=4)  # TODO:IMPROVE
    ready = False
    while run:
        clock.tick(60)
        win.fill(pygame.color.THECOLORS['aliceblue'])

        win.blit(bg.image, bg.rect)

        # draw_effect(effect)  # Draws Effect

        # Banners
        p1_banner.draw_name_points(game.p1_pairs if n.p == 1 else game.p2_pairs)
        p2_banner.draw_name_points(game.p2_pairs if n.p == 1 else game.p1_pairs)
        game = n.send('get')
        board.back = game.back

        if game.ready or game.end:

            if not game.end:  # TODO:
                ready = False
                game_logic(game, n, p1_banner, p2_banner, board)
            else:
                if not ready:
                    # print("GAME RESULT")
                    gp = GameResultPopUp(win, 100, 100, 500, 500, (62, 178, 191), game.last)
                    gp.draw(n.p)

                    # HANDLE CLICK LOGIC

                    if pygame.mouse.get_pressed()[0]:
                        click = gp.click()
                        if click == 1:
                            game = n.send("again")
                            ready = True

                        elif click == 2:
                            pygame.quit()
                            sys.exit()
                            return

                # WIN or Lose
                # Maybe activate a variable if ready and send message to server.

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                return


def game_offline_loop():
    """
    Runs the main game (offline)
    """
    pass


def pop_up_name():
    run = True
    clock = pygame.time.Clock()
    bg = Background(bg_image, (0, 0))

    pop = PopUpName(win, x=700 / 2 - 200, y=700 / 2 - 200, color=(48, 138, 234), width=400, height=400)

    while run:
        clock.tick(60)
        win.fill(pygame.color.THECOLORS['aliceblue'])

        win.blit(bg.image, bg.rect)

        draw_effect(effect)  # Draws Effect

        pop.draw_shadow()

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                res = pop.focused()
                if not res:
                    pop.unfocused()

            if event.type == pygame.KEYDOWN:
                if pop.valid_text() and event.key == pygame.K_RETURN:
                    run = False

                if pop.focus:
                    if event.key == 8:  # delete
                        pop.del_char_field()
                    else:
                        pop.update_field_text(event.key)
    game_online_loop(pop.get_player_name())


def offline_online():
    """
    Menu to choose between online and offline
    """
    run = True
    clock = pygame.time.Clock()
    bg = Background(bg_image, (0, 0))

    # Buttons
    offline = Button(win, "Offline", x=700 / 2 - 200, y=700 / 2 - 50 - 75, color=(84, 249, 219), width=400, height=100)
    online = Button(win, "Online", x=700 / 2 - 200, y=700 / 2 - 50 + 75, color=(84, 134, 249), width=400, height=100)

    off = True

    while run:
        clock.tick(60)
        win.fill(pygame.color.THECOLORS['aliceblue'])

        win.blit(bg.image, bg.rect)

        draw_effect(effect)  # Draws Effect

        offline.draw_shadowed()
        online.draw_shadowed()

        offline.hover()
        online.hover()

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if offline.click():
                    off = True
                    run = False
                elif online.click():
                    off = False
                    run = False
    if off:
        game_offline_loop()
    else:
        pop_up_name()


def main_menu():
    """
    Shows a menu before connecting to the game
    """
    run = True
    clock = pygame.time.Clock()
    bg = Background(bg_image, (0, 0))
    while run:
        clock.tick(60)
        win.fill(pygame.color.THECOLORS['aliceblue'])
        font = pygame.font.SysFont("comicsans", 100)

        win.blit(bg.image, bg.rect)

        draw_effect(effect)  # Draws Effect

        shadowed_text(win, font, "Card Frenzy", (220, 140, 220), WIDTH, HEIGHT, x_offset=1, pos='c')

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    offline_online()


if __name__ == "__main__":

    while True:
        try:
            main_menu()
        except EOFError as e:
            print("[CONNECTION ERROR] -> Other player disconnected")
