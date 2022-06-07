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
from pygame import display, init
from pygame.font import SysFont

from configuration import COEFFICIENT, FONT_NAME, STEP_VALUE, SYMBOLS


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


class AsciiVideo:
    def __init__(
        self,
        capture: VideoCapture,
        font_size: int,
        ascii_coefficient: int,
    ) -> None:
        init()

        self.capture = capture
        self.frame = self.get_frame()
        self.font = SysFont(FONT_NAME, font_size, bold=True)

        self.ASCII_COEFFICIENT = ascii_coefficient
        self.CHAR_STEP = int(font_size * STEP_VALUE)
        self.WIDTH, self.HEIGHT = self.frame.shape[0], self.frame.shape[1]

        self.surface = display.set_mode((self.WIDTH, self.HEIGHT))

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

    def get_frame(self) -> "GrayImage":
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
        self.draw()
        display.flip()


def main() -> None:
    video_file: str = "video.mp4"
    font_size: int = 12

    capture = VideoCapture(video_file)
    app: AsciiVideo = AsciiVideo(capture, font_size, COEFFICIENT)

    while True:
        app.run()


if __name__ == "__main__":
    main()
