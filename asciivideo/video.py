from typing import List, Tuple

from cv2 import (
    COLOR_BGR2GRAY,
    INTER_AREA,
    VideoCapture,
    cvtColor,
    imshow,
    resize,
    transpose,
)
from numba import njit
from moviepy.editor import AudioFileClip
import pygame

from .configuration import *


pygame.mixer.pre_init(44100, 32, 2, 4096)
pygame.mixer.init()


@njit(fastmath=True)
def accelerate_conversion(
    frame, width: int, height: int, coefficient: int, step: int
) -> List[Tuple[int, Tuple[int, int]]]:

    values = []

    for x in range(0, width, step):
        for y in range(0, height, step):
            index = frame[x, y] // coefficient

            if index:
                values.append((index, (x, y)))

    return values


def audio_capture(path_to_file: str) -> None:
    audio = AudioFileClip(path_to_file)
    audio.write_audiofile(f"{path_to_file.split('.')[0]}.mp3")


class AsciiVideo:
    def __init__(self, path_to_file: str) -> None:
        pygame.init()

        self.capture = VideoCapture(path_to_file)
        self.frame = self.get_frame()
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE, bold=True)

        self.ASCII_COEFFICIENT = COEFFICIENT
        self.CHAR_STEP = int(FONT_SIZE * STEP_VALUE)
        self.WIDTH, self.HEIGHT = self.frame.shape[0], self.frame.shape[1]

        self.surface = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        audio_capture(path_to_file)
        self.sound = pygame.mixer.Sound(f"{path_to_file.split('.')[0]}.mp3")
        self.clock = pygame.time.Clock()

        self.RENDERED_SYMBOLS = [
            self.font.render(char, False, "white") for char in SYMBOLS
        ]

    def draw_converted_frame(self) -> None:
        self.frame = self.get_frame()
        array_of_values = accelerate_conversion(
            self.frame,
            self.WIDTH,
            self.HEIGHT,
            self.ASCII_COEFFICIENT,
            self.CHAR_STEP,
        )

        for char_index, position in array_of_values:
            self.surface.blit(self.RENDERED_SYMBOLS[char_index], position)

    def get_frame(self) -> cvtColor:
        self.frame = self.capture.read()[1]
        transposed_frame = transpose(self.frame)

        gray_frame = cvtColor(transposed_frame, COLOR_BGR2GRAY)
        return gray_frame

    def draw_frame(self) -> None:
        resized_frame = resize(self.frame, interpolation=INTER_AREA)
        imshow("img", resized_frame)

    def draw(self) -> None:
        self.surface.fill("black")
        self.draw_converted_frame()

    def run(self) -> None:
        pygame.display.set_caption("AsciiVideo")
        self.sound.play()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit()

            self.clock.tick(FPS)
            self.draw()
            pygame.display.update()
