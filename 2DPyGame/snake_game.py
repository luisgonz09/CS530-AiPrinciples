"""Simple Snake arcade game prototype using Pygame.

Controls:
- Arrow keys to move the snake
- ESC to open the pause/options menu
- R to restart after game over or while paused
- Q to quit the game

Game rules:
- Collect green food dots to increase score.
- Avoid red mine dots. Collision with a mine ends the game.
- Avoid colliding with your own tail.
- Food appears every 3 seconds, mines appear every 5-10 seconds.
"""

import io
import math
import random
import struct
import sys
import wave

import pygame

# Screen and grid settings
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 30
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT
FPS = 10

# Colors
COLOR_BACKGROUND = pygame.Color("black")
COLOR_SNAKE = pygame.Color("lime")
COLOR_FOOD = pygame.Color("green")
COLOR_MINE = pygame.Color("red")
COLOR_TEXT = pygame.Color("white")
COLOR_MENU = pygame.Color("dodgerblue")
COLOR_OVERLAY = pygame.Color(0, 0, 0, 180)

# Timers (milliseconds)
FOOD_SPAWN_INTERVAL = 3000
MINE_SPAWN_MIN = 5000
MINE_SPAWN_MAX = 10000


class SnakeGame:
    """Encapsulates game state and logic for the Snake prototype."""

    @staticmethod
    def _make_wav_bytes(frequencies, duration=0.16, volume=0.5, sample_rate=44100):
        """Create WAV audio bytes for one or more sine-wave frequencies."""
        if isinstance(frequencies, (int, float)):
            frequencies = (frequencies,)

        num_samples = int(duration * sample_rate)
        audio_data = bytearray()
        for sample_index in range(num_samples):
            sample_value = 0.0
            for frequency in frequencies:
                sample_value += math.sin(2.0 * math.pi * frequency * sample_index / sample_rate)
            sample_value /= len(frequencies)
            packed_value = int(sample_value * volume * 32767)
            audio_data += struct.pack('<h', packed_value)

        with io.BytesIO() as wav_file:
            with wave.open(wav_file, 'wb') as wave_writer:
                wave_writer.setnchannels(1)
                wave_writer.setsampwidth(2)
                wave_writer.setframerate(sample_rate)
                wave_writer.writeframes(bytes(audio_data))
            return wav_file.getvalue()

    def _create_sound(self, frequencies, duration=0.16, volume=0.5):
        """Create a Pygame Sound object from generated WAV bytes."""
        wav_bytes = self._make_wav_bytes(frequencies, duration, volume)
        return pygame.mixer.Sound(buffer=wav_bytes)

    def __init__(self):
        pygame.init()
        try:
            pygame.mixer.init()
        except pygame.error:
            pass

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake Arcade Prototype")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Consolas", 20)
        self.large_font = pygame.font.SysFont("Consolas", 36, bold=True)
        self.sfx_collect = self._create_sound((880, 1320), duration=0.12, volume=0.5)
        self.sfx_mine = self._create_sound(220, duration=0.22, volume=0.6)
        self.sfx_crash = self._create_sound((130, 260), duration=0.28, volume=0.7)
        self.reset_game()

    def reset_game(self):
        """Reset game state to start or restart the game."""
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.pending_direction = self.direction
        self.score = 0
        self.food_positions = []
        self.mine_positions = []
        self.next_food_spawn = pygame.time.get_ticks() + FOOD_SPAWN_INTERVAL
        self.next_mine_spawn = pygame.time.get_ticks() + random.randint(MINE_SPAWN_MIN, MINE_SPAWN_MAX)
        self.game_over = False
        self.menu_open = False
        self.last_move_time = 0
        self.move_delay = 1000 // FPS

    def spawn_dot(self, avoid_positions):
        """Spawn a dot at a random position not occupied by the snake, food, or mines."""
        while True:
            position = (random.randrange(GRID_WIDTH), random.randrange(GRID_HEIGHT))
            if position not in avoid_positions:
                return position

    def update(self):
        """Update game state for the current frame."""
        if self.game_over or self.menu_open:
            return

        current_time = pygame.time.get_ticks()
        if current_time >= self.next_food_spawn:
            self.food_positions.append(self.spawn_dot(self.snake + self.food_positions + self.mine_positions))
            self.next_food_spawn = current_time + FOOD_SPAWN_INTERVAL

        if current_time >= self.next_mine_spawn:
            self.mine_positions.append(self.spawn_dot(self.snake + self.food_positions + self.mine_positions))
            self.next_mine_spawn = current_time + random.randint(MINE_SPAWN_MIN, MINE_SPAWN_MAX)

        if current_time - self.last_move_time >= self.move_delay:
            self.direction = self.pending_direction
            new_head = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])
            self.last_move_time = current_time

            # Wrap around screen edges for a classic arcade feel
            new_head = (new_head[0] % GRID_WIDTH, new_head[1] % GRID_HEIGHT)

            if new_head in self.snake:
                self.sfx_crash.play()
                self.game_over = True
                return

            self.snake.insert(0, new_head)

            if new_head in self.food_positions:
                self.food_positions.remove(new_head)
                self.score += 1
                self.sfx_collect.play()
            elif new_head in self.mine_positions:
                self.sfx_mine.play()
                self.game_over = True
            else:
                self.snake.pop()

    def handle_input(self):
        """Handle player input events for movement and menu controls."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.menu_open = not self.menu_open
                elif event.key == pygame.K_r:
                    self.reset_game()
                elif event.key == pygame.K_q:
                    self.quit_game()
                elif not self.game_over and not self.menu_open:
                    self.handle_direction_keys(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN and self.menu_open:
                self.check_menu_click(event.pos)

    def handle_direction_keys(self, key):
        """Update the snake direction based on arrow key presses."""
        if key == pygame.K_UP and self.direction != (0, 1):
            self.pending_direction = (0, -1)
        elif key == pygame.K_DOWN and self.direction != (0, -1):
            self.pending_direction = (0, 1)
        elif key == pygame.K_LEFT and self.direction != (1, 0):
            self.pending_direction = (-1, 0)
        elif key == pygame.K_RIGHT and self.direction != (-1, 0):
            self.pending_direction = (1, 0)

    def check_menu_click(self, mouse_pos):
        """Handle mouse clicks inside the pause/options menu."""
        restart_rect = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3, SCREEN_WIDTH // 2, 50)
        quit_rect = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3 + 80, SCREEN_WIDTH // 2, 50)
        if restart_rect.collidepoint(mouse_pos):
            self.reset_game()
            self.menu_open = False
        elif quit_rect.collidepoint(mouse_pos):
            self.quit_game()

    def draw(self):
        """Draw the current game state on the screen."""
        self.screen.fill(COLOR_BACKGROUND)
        self.draw_grid()
        self.draw_snake()
        self.draw_dots()
        self.draw_hud()

        if self.menu_open:
            self.draw_menu()
        elif self.game_over:
            self.draw_game_over()

        pygame.display.flip()

    def draw_grid(self):
        """Draw the background grid lines."""
        for x in range(0, SCREEN_WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, pygame.Color("gray15"), (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, pygame.Color("gray15"), (0, y), (SCREEN_WIDTH, y))

    def draw_snake(self):
        """Draw the snake body segments as circles."""
        radius = CELL_SIZE // 2 - 2
        for segment in self.snake:
            center = (segment[0] * CELL_SIZE + CELL_SIZE // 2, segment[1] * CELL_SIZE + CELL_SIZE // 2)
            pygame.draw.circle(self.screen, COLOR_SNAKE, center, radius)

    def draw_dots(self):
        """Draw food and mine dots."""
        for food in self.food_positions:
            center = (food[0] * CELL_SIZE + CELL_SIZE // 2, food[1] * CELL_SIZE + CELL_SIZE // 2)
            pygame.draw.circle(self.screen, COLOR_FOOD, center, CELL_SIZE // 2 - 2)

        for mine in self.mine_positions:
            center = (mine[0] * CELL_SIZE + CELL_SIZE // 2, mine[1] * CELL_SIZE + CELL_SIZE // 2)
            pygame.draw.circle(self.screen, COLOR_MINE, center, CELL_SIZE // 2 - 2)

    def draw_hud(self):
        """Draw the score, instructions, and timing info."""
        score_text = self.font.render(f"Score: {self.score}", True, COLOR_TEXT)
        instructions = self.font.render("Arrows: Move | ESC: Menu | R: Restart | Q: Quit", True, COLOR_TEXT)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(instructions, (10, SCREEN_HEIGHT - 30))

        remaining_food = max(0, self.next_food_spawn - pygame.time.get_ticks()) // 1000
        remaining_mine = max(0, self.next_mine_spawn - pygame.time.get_ticks()) // 1000
        timer_text = self.font.render(f"Next food: {remaining_food}s | Next mine: {remaining_mine}s", True, COLOR_TEXT)
        self.screen.blit(timer_text, (10, 35))

    def draw_game_over(self):
        """Draw the game over screen overlay."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill(COLOR_OVERLAY)
        self.screen.blit(overlay, (0, 0))

        game_over_text = self.large_font.render("Game Over", True, COLOR_TEXT)
        score_text = self.font.render(f"Final score: {self.score}", True, COLOR_TEXT)
        restart_text = self.font.render("Press R to restart or Q to quit", True, COLOR_TEXT)

        self.screen.blit(game_over_text, game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)))
        self.screen.blit(score_text, score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
        self.screen.blit(restart_text, restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)))

    def draw_menu(self):
        """Draw the pause/options menu overlay."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill(COLOR_OVERLAY)
        self.screen.blit(overlay, (0, 0))

        menu_title = self.large_font.render("Paused", True, COLOR_TEXT)
        menu_subtitle = self.font.render("Click a button or press R / Q", True, COLOR_TEXT)

        restart_rect = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3, SCREEN_WIDTH // 2, 50)
        quit_rect = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3 + 80, SCREEN_WIDTH // 2, 50)

        pygame.draw.rect(self.screen, COLOR_MENU, restart_rect)
        pygame.draw.rect(self.screen, COLOR_MENU, quit_rect)

        restart_text = self.font.render("Restart", True, COLOR_TEXT)
        quit_text = self.font.render("Quit", True, COLOR_TEXT)

        self.screen.blit(menu_title, menu_title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 - 70)))
        self.screen.blit(menu_subtitle, menu_subtitle.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 - 30)))
        self.screen.blit(restart_text, restart_text.get_rect(center=restart_rect.center))
        self.screen.blit(quit_text, quit_text.get_rect(center=quit_rect.center))

    def quit_game(self):
        """Quit the game and close the Pygame window."""
        pygame.quit()
        sys.exit()

    def run(self):
        """Main game loop."""
        while True:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)


def main():
    game = SnakeGame()
    game.run()


if __name__ == "__main__":
    main()
