"""Entry point for running the simple snake game."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Tuple

import pygame

from game_objects import Food, Snake


@dataclass
class GameConfig:
    grid_width: int = 20
    grid_height: int = 20
    block_size: int = 20
    fps: int = 60
    moves_per_second: float = 8.0

    @property
    def screen_size(self) -> Tuple[int, int]:
        return (self.grid_width * self.block_size, self.grid_height * self.block_size)


class SnakeGame:
    """Encapsulates the main game loop and rendering."""

    def __init__(self, config: GameConfig | None = None) -> None:
        self.config = config or GameConfig()
        self.screen: pygame.Surface | None = None
        self.clock: pygame.time.Clock | None = None
        self.snake: Snake | None = None
        self.food: Food | None = None
        self.score = 0
        self.waiting_for_start = True
        self.move_progress = 0.0
        self.move_interval = 1.0 / self.config.moves_per_second
        self.pending_growth = False

    def reset(self) -> None:
        start_position = [
            (self.config.grid_width // 2 - 1, self.config.grid_height // 2),
            (self.config.grid_width // 2, self.config.grid_height // 2),
        ]
        self.snake = Snake(start=start_position)
        self.food = self._spawn_food()
        self.score = 0
        self.waiting_for_start = True
        self.move_progress = 0.0
        self.move_interval = 1.0 / self.config.moves_per_second
        self.pending_growth = self.snake.next_head_position() == self.food.position

    def _spawn_food(self) -> Food:
        assert self.snake is not None
        while True:
            position = (
                random.randint(0, self.config.grid_width - 1),
                random.randint(0, self.config.grid_height - 1),
            )
            if position not in self.snake.body:
                return Food(position)

    def run(self) -> None:
        pygame.init()
        pygame.display.set_caption("Codex Demo Snake")
        self.screen = pygame.display.set_mode(self.config.screen_size)
        self.clock = pygame.time.Clock()
        self.reset()

        running = True
        while running:
            assert self.clock is not None and self.snake is not None and self.food is not None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self._handle_key(event.key)

            dt = self.clock.tick(self.config.fps) / 1000.0
            self._update_game_state(dt)
            self._draw()

        pygame.quit()

    def _handle_key(self, key: int) -> None:
        assert self.snake is not None
        if self.waiting_for_start:
            if key in (pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT):
                self._apply_direction_from_key(key)
                self.waiting_for_start = False
                self.move_progress = 0.0
            return

        self._apply_direction_from_key(key)

    def _apply_direction_from_key(self, key: int) -> None:
        assert self.snake is not None
        if key == pygame.K_UP:
            self.snake.set_direction((0, -1))
        elif key == pygame.K_DOWN:
            self.snake.set_direction((0, 1))
        elif key == pygame.K_LEFT:
            self.snake.set_direction((-1, 0))
        elif key == pygame.K_RIGHT:
            self.snake.set_direction((1, 0))

    def _update_game_state(self, dt: float) -> None:
        assert self.snake is not None and self.food is not None

        if self.waiting_for_start:
            self.move_progress = 0.0
            self.pending_growth = self.snake.next_head_position() == self.food.position
            return

        self.move_progress += dt / self.move_interval

        while self.move_progress >= 1.0:
            current_grow = self.snake.next_head_position() == self.food.position
            if not self._advance_snake(current_grow):
                return
            self.move_progress -= 1.0

        self.pending_growth = self.snake.next_head_position() == self.food.position

    def _advance_snake(self, grow: bool) -> bool:
        assert self.snake is not None and self.food is not None

        next_position = self.snake.next_head_position()
        if self._is_out_of_bounds(next_position):
            self.reset()
            return False

        self.snake.move(grow=grow)

        if self.snake.hits_self():
            self.reset()
            return False

        if grow:
            self.score += 1
            self.food = self._spawn_food()
            self.pending_growth = self.snake.next_head_position() == self.food.position

        return True

    def _is_out_of_bounds(self, position: Tuple[int, int]) -> bool:
        x, y = position
        return not (0 <= x < self.config.grid_width and 0 <= y < self.config.grid_height)

    def _draw(self) -> None:
        assert self.screen is not None and self.snake is not None and self.food is not None
        self.screen.fill((30, 30, 30))
        self.food.draw(self.screen, self.config.block_size)
        progress = max(0.0, min(self.move_progress, 1.0))
        self.snake.draw(self.screen, self.config.block_size, progress, self.pending_growth)
        self._draw_score()
        if self.waiting_for_start:
            self._draw_start_prompt()
        pygame.display.flip()

    def _draw_score(self) -> None:
        assert self.screen is not None
        font = pygame.font.SysFont("arial", 18)
        text = font.render(f"Score: {self.score}", True, (220, 220, 220))
        self.screen.blit(text, (5, 5))

    def _draw_start_prompt(self) -> None:
        assert self.screen is not None
        font = pygame.font.SysFont("arial", 22)
        message = "Press ↑, ↓, or → to start"
        text = font.render(message, True, (240, 240, 240))
        rect = text.get_rect(center=(self.config.screen_size[0] // 2, self.config.screen_size[1] // 2))
        background = pygame.Surface(rect.size, pygame.SRCALPHA)
        background.fill((10, 10, 10, 180))
        self.screen.blit(background, rect)
        self.screen.blit(text, rect)


def main() -> None:
    SnakeGame().run()


if __name__ == "__main__":
    main()
