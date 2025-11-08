"""Core objects used by the snake game."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Deque, Iterable, Tuple

import pygame

# Type alias for readability
Vector2D = Tuple[int, int]


@dataclass
class Food:
    """Represents a food pellet on the grid."""

    position: Vector2D
    color: Tuple[int, int, int] = (200, 30, 30)

    def draw(self, surface: pygame.Surface, block_size: int) -> None:
        rect = pygame.Rect(
            self.position[0] * block_size,
            self.position[1] * block_size,
            block_size,
            block_size,
        )
        pygame.draw.rect(surface, self.color, rect)


class Snake:
    """Simple snake implementation using a deque for the body."""

    def __init__(
        self,
        start: Iterable[Vector2D],
        color: Tuple[int, int, int] = (40, 200, 40),
    ) -> None:
        self.body: Deque[Vector2D]
        self.direction: Vector2D
        self.color = color

        body_list = list(start)
        if not body_list:
            raise ValueError("Snake must start with at least one segment")
        self.body = deque(body_list)
        self.direction = (1, 0)

    def head(self) -> Vector2D:
        return self.body[-1]

    def set_direction(self, direction: Vector2D) -> None:
        """Prevent the snake from reversing into itself."""

        if not self.body:
            return
        current = self.direction
        # Avoid reversing direction.
        if (direction[0] == -current[0] and direction[1] == -current[1]) or direction == current:
            return
        self.direction = direction

    def next_head_position(self) -> Vector2D:
        head_x, head_y = self.head()
        return head_x + self.direction[0], head_y + self.direction[1]

    def move(self, grow: bool = False) -> None:
        self.body.append(self.next_head_position())
        if not grow:
            self.body.popleft()

    def hits_self(self) -> bool:
        head = self.head()
        return head in list(self.body)[:-1]

    def draw(self, surface: pygame.Surface, block_size: int) -> None:
        for x, y in self.body:
            rect = pygame.Rect(x * block_size, y * block_size, block_size, block_size)
            pygame.draw.rect(surface, self.color, rect)
