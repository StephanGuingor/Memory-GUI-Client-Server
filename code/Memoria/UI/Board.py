"""
Represents the Graphical Board
"""
import pygame

from code.Memoria.Utility import load_image, overrides


class Board(object):
    def __init__(self, win, og_cards, x, y, width, height, image, dim=4, ):
        """
        Initializes Board object
        """
        self.win = win
        self.og = og_cards
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.dim = dim
        self.image = load_image(image, 1)
        self.cards = self._create_cards()

    def _create_cards(self):
        """
        Creates dict of card objects
        """

        cards = {}
        width = self.width // self.dim - 50
        height = self.height // self.dim - 80
        off = 10
        x_start = (self.width - (width * self.dim + (off * 2 * (self.dim - 1)))) / 2
        y_start = 200  # Check later
        for idx, val in enumerate(self.og):

            if idx == 0:
                card = ImagedCard(self.win, idx, val, x_start, y_start, width, height, image_file=self.image)

                cards[idx] = card

            elif idx % self.dim == 0:
                x_start = (self.width - (width * self.dim + (off * 2 * (self.dim - 1)))) / 2
                y_start += (off * 2) + height
                card = ImagedCard(self.win, idx, val, x_start, y_start, width, height, image_file=self.image)

                cards[idx] = card
            else:
                x_start += (off * 2) + width
                card = ImagedCard(self.win, idx, val, x_start, y_start, width, height, image_file=self.image)

                cards[idx] = card

        return cards

    # COULD DO BST WITH X AND WIDTH AS KEY

    def draw(self):
        for idx, i in enumerate(self.cards.values()):
            i.value = str(self.back[idx])
            i.draw_shadowed()

    def click(self, pos):
        for i in self.cards.values():
            click = i.click(pos)
            if click:
                return i.idx

    def paint_card(self, idx, color):
        if idx[0] is not None:
            self.cards[idx[0]].draw(color)

        if idx[1] is not None:
            self.cards[idx[1]].draw(color)


class Card(object):
    def __init__(self, win, idx, value, x, y, width, height):
        """
        Initializes Card object
        """
        self.win = win
        self.idx = idx
        self.value = str(value)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont("comicsans", 40)

    # TODO:FIX BACK
    def draw(self, color=(0, 0, 0)):
        """
        draws button into screen
        :return: None
        """
        pygame.draw.rect(self.win, (255, 255, 255), (self.x, self.y, self.width, self.height))
        text = self.font.render(self.value if self.value != '-1' else "???", 1, color)
        self.win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                             self.y + round(self.height / 2) - round(text.get_height() / 2)))

    def draw_shadowed(self, x_offset=2, y_offset=3, color=(48, 49, 50)):
        pygame.draw.rect(self.win, (220, 160, 20), (self.x + x_offset, self.y + y_offset, self.width, self.height))

        self.draw()

    def click(self, pos):
        x = pos[0]
        y = pos[1]

        if self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height:
            return True
        return None


class ImagedCard(Card):
    """
    Card but with an image as background
    """

    def __init__(self, *args, image_file=None):
        super().__init__(*args)
        self.args = args
        # TODO: PROOF THIS
        self.image = image_file
        self.image.fill((255, 255, 255, 255), None, pygame.BLEND_RGBA_MULT)
        # self.sub = self.win.subsurface((self.x, self.y, self.width, self.height))

    @overrides(Card)  # TODO: verification
    def draw(self, color=(0, 0, 0)):
        """create surface and add image to it"""

        if self.value == "-1":
            self.win.blit(self.image, (self.x, self.y, self.width, self.height))
        else:
            pygame.draw.rect(self.win, (255, 255, 255), (self.x, self.y, self.width, self.height))
            text = self.font.render(self.value, 1, color)
            self.win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                                 self.y + round(self.height / 2) - round(text.get_height() / 2)))


if __name__ == "__main__":
    b = Board("win", [i for i in range(16)], 5, 700 // 8, 700, 700)
    for i in b.cards.values():
        print(i.value)
