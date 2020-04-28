""""
Utility Functions for GUI
"""
import time

import pygame
from code.pyIgnitionAlpha import PyIgnition
from code.Memoria.Utility import load_image

SHADOW_COLOR = pygame.color.THECOLORS['gray']
pygame.font.init()


class TabShow(object):
    pass


class GameResultPopUp(object):
    def __init__(self, win, x, y, width, height, color, winner,
                 font=pygame.font.SysFont('impact', 40)):
        """Initializes Game Result PopUp"""
        self.win = win
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.font = font
        self.winner = winner  # INT
        self.bg_surf = pygame.surface.Surface((700, 700), pygame.SRCALPHA)
        self.bg_surf.fill((*color, 128))
        self.play_button = Button(win, "Play Again!", x + 100, y + 250, width * 2 / 3, height / 5, (55, 219, 137), font)
        self.quit_button = Button(win, "Quit", x + 100, y + 350, width * 2 / 3, height / 5, (232, 71, 87), font)

    def draw(self, player):
        """Draw to screen the object"""
        self.win.blit(self.bg_surf, (0, 0))

        pygame.draw.rect(self.win, self.color, (self.x, self.y, self.width, self.height))

        # DRAWS WINNER TODO: CHECK

        if self.winner == 2:

            shadowed_text(self.win, self.font, "Tie!.", (0, 0, 0), self.width + 200,
                          self.height * 2 / 3)

        elif player != self.winner:

            shadowed_text(self.win, self.font, "Congratulations you won!.", (0, 0, 0), self.width + 200,
                          self.height * 2 / 3)

        else:
            shadowed_text(self.win, self.font, "Congratulations you Lose!.", (0, 0, 0), self.width + 200,
                          self.height * 2 / 3)

        # DRAW BUTTON

        self.play_button.draw_shadowed()
        self.play_button.hover()
        self.quit_button.draw_shadowed()
        self.quit_button.hover()

    def click(self):
        """
        Returns 1 for Play Again, and Return 2 for quit
        """
        if self.play_button.click():
            return 1
        if self.quit_button.click():
            return 2
        return -1


class PlayerBanner(object):
    """
    Will show the players and who's turn is
    """

    def __init__(self, win, name, image_file, x, y, width, height, side='r'):
        """
        Initializes PlayerBanner object
        """
        self.win = win
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont('impact', 60)
        self.small_font = pygame.font.SysFont('impact', 40)
        self.name = name
        self.image = load_image(image_file, 1)
        self.image.fill((255, 255, 255, 120), None, pygame.BLEND_RGBA_MULT)
        self.sub = self.win.subsurface((self.x, self.y - self.height / 1.5, self.width, self.height * 1.5))
        self.side = side

    def draw(self):
        """Draws the object to screen"""
        self.sub.blit(self.image, (self.x, self.y - self.height / 1.5, self.width, self.height * 1.5))

        if self.side == "l":
            shadowed_text(self.win, self.font, self.name, (255, 255, 255), self.width * 2.2, self.height * 2.5)
        else:
            shadowed_text(self.win, self.font, self.name, (255, 255, 255), self.width, self.height * 2.5)

    def set_name(self, name):
        """Sets the name variable"""
        self.name = name

    def draw_turn(self, turn='self'):
        """Draws a circle on players who's turn is"""
        if turn != 'self':
            pygame.draw.circle(self.win, (0, 255, 0), (round(self.width - 95), round(self.height)), 10)
        else:
            pygame.draw.circle(self.win, (0, 255, 0), (round(self.width - 7), round(self.height)), 10)

    # TODO: FIX FUNCTION

    def draw_name_points(self, points):
        """
        Draws the score to the board
        """
        self.sub.blit(self.image, (self.x, self.y, self.width, self.height))
        # self.draw_turn()

        if self.side == "r":  # TODO:CHECK
            # Name
            shadowed_text(self.win, self.small_font, self.name, (0, 255, 255), self.width * 2.4, self.height * 2.5)
            shadowed_text(self.win, self.font, f'{points}', (0, 255, 255), self.width * 1.8, self.height * 2.5)

        else:
            # Name
            shadowed_text(self.win, self.small_font, self.name, (255, 0, 255), self.width / 1.6, self.height * 2.5)
            shadowed_text(self.win, self.font, f'{points}', (255, 0, 255), self.width * 1.6, self.height * 2.5)

    def draw_same_side(self):
        pass

    def draw_points(self, turn='self'):
        """
        Draws the score to the board
        """
        if turn != 'self':
            pygame.draw.rect(self.win, (0, 255, 0),
                             (self.x, self.y + self.height, round(self.width - 95), round(self.height)), 10)
        else:
            pygame.draw.rect(self.win, (0, 0, 255),
                             (self.x, self.y + self.height, round(self.width - 95), round(self.height)), 10)


class PopUpName(object):

    def __init__(self, win, x, y, width, height, color, font=pygame.font.SysFont('impact', 60)):
        """
        Initializes a field to write a name
        """
        self.win = win
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.font = font
        self.focus = True
        self.captured_text = ""

    def draw(self):
        """
        Draws popup into the screen
        :return: None
        """

        pygame.draw.rect(self.win, self.color, (self.x, self.y, self.width, self.height))
        text = self.font.render("Enter name: ", 1, (255, 255, 255))
        self.win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                             self.y + round(self.height / 4) - round(text.get_height() / 2)))
        self.draw_text_field()

    def draw_text_field(self):
        """
        Draws text field
        """
        if self.focus:
            c = (255, 255, 255)
        else:
            c = (200, 200, 200)

        w_quarter = self.width - self.width / 4
        height = self.height - self.height * 3 / 4
        x = self.x + round(self.width / 2) - w_quarter / 2
        y = self.y + round(self.height * 2 / 4)
        pygame.draw.rect(self.win, c, (x, y, w_quarter, height))

        text = self.font.render(self.captured_text, 1, (0, 0, 0))
        self.win.blit(text, (x + round(w_quarter / 2) - round(text.get_width() / 2),
                             y + round(height / 2) - round(text.get_height() / 2)))

    def draw_shadow(self, x_offset=2, y_offset=3):
        """
        Draws shadow
        """
        pygame.draw.rect(self.win, (48, 49, 50), (self.x + x_offset, self.y + y_offset, self.width, self.height))

        self.draw()

    def unfocused(self):
        """
        Called when the text field is not being used
        """
        print("UNFOCUSED")
        self.focus = False

    def update_field_text(self, char):
        """
        Updates text field
        """
        if 32 > char or char > 126:
            return
        if len(self.captured_text) < 10:
            self.captured_text += chr(char)

    def del_char_field(self):
        """
        Deletes character from text field
        """
        if len(self.captured_text) > 0:
            self.captured_text = self.captured_text[:-1]

    def valid_text(self):
        """
        Validates text
        """
        return len(self.captured_text) > 0

    def focused(self):
        """
        Checks if a click happened in the button
        :return: bool
        """
        x1, y1 = pygame.mouse.get_pos()

        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            print("FOCUSED")
            self.focus = True
            return True
        else:
            return False

    def get_player_name(self):
        """
        Returns captured text
        """
        return self.captured_text


class Button(object):

    def __init__(self, win, text, x, y, width, height, color, font=pygame.font.SysFont("impact", 40)):
        """
        Initializes a button object
        :param text: str
        :param x: int
        :param y: int
        :param color: (int,int,int)
        """
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height
        self.win = win
        self.font = font

    def draw(self):
        """
        draws button into screen
        :return: None
        """
        pygame.draw.rect(self.win, self.color, (self.x, self.y, self.width, self.height))
        text = self.font.render(self.text, 1, (255, 255, 255))
        self.win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                             self.y + round(self.height / 2) - round(text.get_height() / 2)))

    def draw_shadowed(self, x_offset=2, y_offset=3, color=(48, 49, 50)):
        # Shadow
        pygame.draw.rect(self.win, color, (self.x + x_offset, self.y + y_offset, self.width, self.height))

        self.draw()

    def click(self):
        """
        Checks if a click happened in the button
        :param pos: (int,int)
        :return: bool
        """
        x1, y1 = pygame.mouse.get_pos()

        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False

    def hover(self):
        """
        Button will change color if mouse position is inside the rect
        """
        d = 20
        if self.click():
            pygame.draw.rect(self.win, (self.color[0] - d, self.color[1] - d, self.color[2] - d),
                             (self.x, self.y, self.width, self.height))
            text = self.font.render(self.text, 1, (255, 255, 255))
            self.win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                                 self.y + round(self.height / 2) - round(text.get_height() / 2)))


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # Call Sprite initializer
        self.image = load_image(image_file, 0)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


def shadowed_text(win, font, text, color, width, height, x_offset=3, y_offset=2, pos="c"):
    """
    Draws the text and a shadow

    :params
    :win: pygame.Surface
    :font: pygame.Font
    :color: (int,int,int)
    :width: int
    :height: int
    :x_offset: int
    :y_offset: int
    :return: None
    """

    original = font.render(text, 1, color)
    shadowed = font.render(text, 1, SHADOW_COLOR)

    if pos == "c":
        width = width / 2 - original.get_width() / 2
        height = height / 2 - original.get_height() / 2

        win.blit(shadowed, (width + x_offset, height + y_offset))
        win.blit(original, (width, height))


def set_wind_particles_effect(win, width, height):
    """Creates a particle effect like wind"""
    effect = PyIgnition.ParticleEffect(win, (0, 0), (width, height))
    effect.CreateSource(pos=(width / 2, -150), initspeed=5, initdirection=-3.2, initspeedrandrange=2,
                        initdirectionrandrange=1, particlesperframe=8, particlelife=150,
                        drawtype=PyIgnition.DRAWTYPE_POINT, colour=(100, 100, 255))
    effect.CreateDirectedGravity(strength=0.0, strengthrandrange=0.2, direction=[0, -1])
    return effect


def draw_effect(effect):
    """Updates and redraws to screen"""
    effect.Update()
    effect.Redraw()


def warm(e):
    """Warms the screen with particles"""
    clock = pygame.time.Clock()
    start = time.perf_counter()
    finish = time.perf_counter()
    while (finish - start) < 2:
        clock.tick(60)
        draw_effect(e)
        finish = time.perf_counter()
    print(f"FINISH {finish - start:2f}")


def other(pid, game):
    """Returns other player id"""
    if pid == 1:
        return game.p1_name
    else:
        return game.p2_name
