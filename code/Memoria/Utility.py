from os.path import dirname, abspath, join
import pygame

main_dir = dirname(abspath(__file__))  # Program's directory


def load_image(file, transparent):
    """loads an image, prepares it for play"""
    file = join(main_dir, 'Data', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s' %
                         (file, pygame.get_error()))
    if transparent:
        return surface.convert_alpha()
    return surface.convert()


def overrides(interface_class):
    """Verify that class is overriding another"""
    def overrider(method):
        assert (method.__name__ in dir(interface_class))
        return method

    return overrider
