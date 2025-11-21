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
        margin = block_size * 0.2
        rect = pygame.Rect(
            self.position[0] * block_size + margin,
            self.position[1] * block_size + margin,
            block_size - 2 * margin,
            block_size - 2 * margin,
        )
        pygame.draw.ellipse(surface, self.color, rect)


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

    def draw(
        self,
        surface: pygame.Surface,
        block_size: int,
        progress: float,
        grow: bool,
    ) -> None:
        if not self.body:
            return

        progress = max(0.0, min(progress, 1.0))
        margin = block_size * 0.15
        corner_radius = int(block_size * 0.3)

        for start, target, is_head in self._animation_segments(grow):
            interp_x = start[0] + (target[0] - start[0]) * progress
            interp_y = start[1] + (target[1] - start[1]) * progress
            pixel_x = interp_x * block_size + margin
            pixel_y = interp_y * block_size + margin
            size = block_size - 2 * margin
            rect = pygame.Rect(pixel_x, pixel_y, size, size)

            if is_head:
                self._draw_head(surface, rect)
            else:
                pygame.draw.rect(surface, self.color, rect, border_radius=corner_radius)

    def _draw_head(self, surface: pygame.Surface, rect: pygame.Rect) -> None:
        pygame.draw.ellipse(surface, self.color, rect)

        center = rect.center
        radius = rect.width / 2
        dir_x, dir_y = self.direction
        if dir_x == dir_y == 0:
            return

        nose_offset = radius * 0.9
        perp_offset = radius * 0.5

        # Calculate triangle points for the head's direction indicator.
        tip = (center[0] + dir_x * nose_offset, center[1] + dir_y * nose_offset)
        if dir_x != 0:
            perp = (0, 1)
        else:
            perp = (1, 0)
        left = (
            center[0] - perp[0] * perp_offset + dir_x * radius * 0.4,
            center[1] - perp[1] * perp_offset + dir_y * radius * 0.4,
        )
        right = (
            center[0] + perp[0] * perp_offset + dir_x * radius * 0.4,
            center[1] + perp[1] * perp_offset + dir_y * radius * 0.4,
        )
        pygame.draw.polygon(surface, (20, 20, 20), [tip, left, right])

    def _animation_segments(self, grow: bool) -> Tuple[Tuple[Vector2D, Vector2D, bool], ...]:
        segments = list(self.body)
        if not segments:
            return tuple()

        animation: list[Tuple[Vector2D, Vector2D, bool]] = []

        if not grow:
            last_index = len(segments) - 1
            for i, start in enumerate(segments):
                if i < last_index:
                    target = segments[i + 1]
                    is_head = False
                else:
                    target = self.next_head_position()
                    is_head = True
                animation.append((start, target, is_head))
            return tuple(animation)

        # When growing, existing segments stay in place while a new head emerges.
        for i, start in enumerate(segments):
            animation.append((start, start, False))

        animation.append((segments[-1], self.next_head_position(), True))
        return tuple(animation)
