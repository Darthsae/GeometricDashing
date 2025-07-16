from dataclasses import dataclass
import pygame
from pygame import Sound

@dataclass
class AudioData:
    sound: Sound

    @classmethod
    def load(cls, filepath):
        sound: Sound = pygame.Sound(filepath)
        return cls(sound)