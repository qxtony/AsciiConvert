from typing import Final


SYMBOLS: Final[str] = ' .",:;!~+-xmo*#W&8@'

FONT_NAME: Final[str] = "Сourier"
FONT_SIZE: Final[int] = 12

COEFFICIENT: Final[int] = 255 // (len(SYMBOLS) - 1)
STEP_VALUE: Final[float] = 0.6
FPS: Final[int] = 30
