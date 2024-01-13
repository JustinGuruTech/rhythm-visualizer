import pygame
import math
from dataclasses import dataclass

# Constants and Configuration
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, CENTER_X, CENTER_Y, FPS, BEAT_COLOR_ACTIVE, BEAT_COLOR_INACTIVE,
    BUTTON_TEXT_COLOR, BUTTON_BG_COLOR, FONT_SIZE_LARGE, CIRCLE_DISTANCE, CIRCLE_RADIUS,
    SMALL_CIRCLE_RADIUS, CIRCLE_BORDER_WIDTH, SMOOTH_TRANSITION_FACTOR, BEAT_STRENGTH_MAP
)

@dataclass
class BeatPatternConfig:
    beats_per_minute: int
    beats_per_measure: int
    beat_strengths: dict[int, float]


class CircleBeat:
    """
    A circle that can be drawn on the screen and updated to change its color and size.
    """

    def __init__(self, position, base_radius, color, text=''):
        self.position = position
        self.base_radius = base_radius
        self.radius = base_radius
        self.color = color
        self.text = text
        
    @staticmethod
    def create_circles(bpm_config: BeatPatternConfig) -> list['CircleBeat']:
        num_circles = bpm_config.beats_per_measure
        return [
            CircleBeat(
                position=(
                    CENTER_X + CIRCLE_DISTANCE * math.cos(2 * math.pi * i / (num_circles * 2)),
                    CENTER_Y + CIRCLE_DISTANCE * math.sin(2 * math.pi * i / (num_circles * 2))
                ),
                base_radius=SMALL_CIRCLE_RADIUS if i % 2 else CIRCLE_RADIUS,
                color=BUTTON_TEXT_COLOR
            ) for i in range(num_circles * 2)
        ]

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius)
        pygame.draw.circle(screen, BUTTON_BG_COLOR, self.position,
                           self.radius, CIRCLE_BORDER_WIDTH)  # Add border
        if self.text:
            font = pygame.font.Font(None, FONT_SIZE_LARGE)
            text_surf = font.render(self.text, True, BUTTON_BG_COLOR)
            text_rect = text_surf.get_rect(center=self.position)
            screen.blit(text_surf, text_rect)

    def update(self, is_active, text, size_factor=1.0):
        self.color = BEAT_COLOR_ACTIVE if is_active else BEAT_COLOR_INACTIVE
        self.text = text
        self.radius = int(self.base_radius * size_factor)


class Metronome:
    """
    A rectangle that can be drawn on the screen and updated to change its color.
    """

    def __init__(self, color_start, color_end):
        self.color_start = color_start
        self.color_end = color_end
        self.current_color = color_start

    def update_color(self, beat_counter, total_beats):
        # Adjust to oscillate between color_start and color_end over the full cycle
        t = abs(2 * (beat_counter % total_beats) / total_beats - 1)
        self.current_color = self.lerp_color(
            self.color_start, self.color_end, t)

    def lerp_color(self, color1, color2, t):
        return tuple(int(a + (b - a) * t) for a, b in zip(color1, color2))

    def draw(self, screen):
        screen.fill(self.current_color)


def simulateBeat(bpm_initial_config):
    """
    Simulates a beat pattern on the screen.
    """
    # Initialize pygame and create screen
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    clock = pygame.time.Clock()
    bpm_config = bpm_initial_config
    metronome = Metronome((130, 130, 130), (190, 190, 190))

    # Create beat circles
    circles = CircleBeat.create_circles(bpm_config)
    num_circles = bpm_config.beats_per_measure

    running = True
    beat_counter = 0
    interpolation_steps = FPS / (bpm_config.beats_per_minute / 60)

    while running:
        metronome.update_color(
            beat_counter / interpolation_steps % (num_circles * 2),
            num_circles * 2 * 2
        )
        metronome.draw(screen)

        # Update and draw beat circles
        for i, circle in enumerate(circles):
            is_active = i == int(beat_counter / interpolation_steps) % (num_circles * 2)
            text = str((i // 2) + 1) if i % 2 == 0 else ''
            weight = bpm_config.beat_strengths[i]
            target_size = BEAT_STRENGTH_MAP.get(weight, 1.0) if is_active else 1.0
            size_factor = (circle.radius / circle.base_radius + (target_size - circle.radius / circle.base_radius) / SMOOTH_TRANSITION_FACTOR)
            circle.update(is_active, text, size_factor)
            circle.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # Handle additional events here

        pygame.display.flip()
        clock.tick(FPS)
        beat_counter += 1

    pygame.quit()


beat_patterns = {
    "beat_pattern": BeatPatternConfig(
        beats_per_minute=360,
        beats_per_measure=7,
        beat_strengths=[5, 2, 2, 2, 5, 2, 2, 2, 5, 2, 2, 2, 5, 2]
    ),
    "waltz_pattern": BeatPatternConfig(
        beats_per_minute=240,
        beats_per_measure=3,
        beat_strengths=[5, 1, 1, 5, 1, 1]
    ),
    "quintuple_pattern_3_2": BeatPatternConfig(
        beats_per_minute=220,
        beats_per_measure=5,
        beat_strengths=[5, 2, 1, 5, 1, 5, 2, 1, 5, 1]
    ),
    "quintuple_pattern_2_3": BeatPatternConfig(
        beats_per_minute=220,
        beats_per_measure=5,
        beat_strengths=[5, 1, 5, 2, 2, 5, 1, 5, 2, 2]
    ),
    "compound_duple_pattern": BeatPatternConfig(
        beats_per_minute=220,
        beats_per_measure=6,
        beat_strengths=[5, 2, 1, 5, 2, 1, 5, 2, 1, 5, 2, 1]
    ),
    "compound_triple_pattern": BeatPatternConfig(
        beats_per_minute=620,
        beats_per_measure=9,
        beat_strengths=[5, 2, 1, 5, 2, 1, 5, 2, 1, 5, 2, 1, 5, 2, 1, 5, 2, 1]
    ),
    "seven_eight_pattern": BeatPatternConfig(
        beats_per_minute=260,
        beats_per_measure=7,
        beat_strengths=[5, 1, 4, 1, 5, 1, 1, 5, 1, 4, 1, 5, 1, 1]
    ),
    "nine_eight_pattern": BeatPatternConfig(
        beats_per_minute=260,
        beats_per_measure=9,
        beat_strengths=[5, 1, 4, 1, 4, 1, 5, 1, 1, 5, 1, 4, 1, 4, 1, 5, 1, 1]
    ),
    "eleven_eight_pattern": BeatPatternConfig(
        beats_per_minute=260,
        beats_per_measure=11,
        beat_strengths=[5, 1, 4, 1, 5, 1, 1, 4, 1, 4, 1, 5, 1, 4, 1, 5, 1, 1, 4, 1, 4, 1]
    ),
    "thirteen_eight_pattern": BeatPatternConfig(
        beats_per_minute=260,
        beats_per_measure=13,
        beat_strengths=[5, 1, 4, 1, 4, 1, 5, 2, 1, 5, 1, 4, 1, 5, 1, 1, 5, 1, 4, 1, 4, 1, 5, 1, 1, 5]
    ),
    "fifteen_eight_pattern": BeatPatternConfig(
        beats_per_minute=260,
        beats_per_measure=15,
        beat_strengths=[5, 1, 4, 1, 4, 1, 4, 1, 5, 2, 1, 4, 1, 4, 1, 5, 1, 4, 1, 4, 1, 4, 1, 5, 1, 1, 4, 1, 4, 1]
    ),
    "song_verse_pattern": BeatPatternConfig(
        beats_per_minute=240,
        beats_per_measure=7,
        beat_strengths=[5, 2, 5, 2, 3, 5, 2, 2, 5, 2, 5, 3, 2, 5, 2, 2, 5, 3, 2, 5, 5, 3, 2, 2, 5, 3, 2, 5, 2, 5, 2, 2, 5, 3, 2, 5, 3, 5, 3, 5, 5, 2, 5, 2, 3, 5, 2, 5] * 2
    ),
    "new_nine_eight": BeatPatternConfig(
        beats_per_minute=240,
        beats_per_measure=9,
        beat_strengths=[5, 3, 1, 5, 3, 1, 5, 3, 1, 5, 4, 3, 5, 3, 1, 5, 3, 1]
    ),
}

# Example of using a pattern from the dictionary
chosen_pattern = beat_patterns["new_nine_eight"]
simulateBeat(bpm_initial_config=chosen_pattern)
