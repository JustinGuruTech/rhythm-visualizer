import pygame
import math
from dataclasses import dataclass
import pygame.mixer

# Constants and Configuration
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, CENTER_X, CENTER_Y, FPS, BEAT_COLOR_ACTIVE, BEAT_COLOR_INACTIVE,
    BUTTON_TEXT_COLOR, BUTTON_BG_COLOR, FONT_SIZE_LARGE, CIRCLE_DISTANCE, CIRCLE_RADIUS,
    SMALL_CIRCLE_RADIUS, CIRCLE_BORDER_WIDTH, SMOOTH_TRANSITION_FACTOR, BEAT_STRENGTH_MAP, SOUND_FILE, BEAT_PATTERNS, BeatPatternConfig
)


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
        total_circles = bpm_config.beats_per_measure * bpm_config.subdivisions
        return [
            CircleBeat(
                position=(
                    CENTER_X + CIRCLE_DISTANCE *
                    math.cos(2 * math.pi * i / total_circles),
                    CENTER_Y + CIRCLE_DISTANCE *
                    math.sin(2 * math.pi * i / total_circles)
                ),
                base_radius=SMALL_CIRCLE_RADIUS if i % bpm_config.subdivisions else CIRCLE_RADIUS,
                color=BUTTON_TEXT_COLOR
            ) for i in range(total_circles)
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


def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        # Other event handling...
    return True


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

    # Initialize the mixer and load the sound
    pygame.mixer.init()
    hat_sound = pygame.mixer.Sound(SOUND_FILE)  # Ensure SOUND_FILE is defined and points to your audio file

    # Create beat circles
    circles = CircleBeat.create_circles(bpm_config)
    num_circles = bpm_config.beats_per_measure

    running = True
    beat_counter = 0
    interpolation_steps = FPS / (bpm_config.beats_per_minute / 60)
    last_played_index = -1

    while running:
        total_beats = num_circles * bpm_config.subdivisions * 2
        metronome.update_color(beat_counter / interpolation_steps % total_beats, total_beats)
        metronome.draw(screen)

        total_circles = num_circles * bpm_config.subdivisions
        current_index = int(beat_counter / interpolation_steps) % total_circles
        active_beat_number = (current_index // bpm_config.subdivisions) + 1

        if current_index != last_played_index:
            # Adjusted logic to handle beat strengths correctly
            beat_strength_index = current_index if current_index < len(bpm_config.beat_strengths) else 0
            weight = bpm_config.beat_strengths[beat_strength_index]
            volume = BEAT_STRENGTH_MAP.get(weight, 0.25)

            hat_sound.set_volume(volume)
            hat_sound.play()
            last_played_index = current_index

        for i, circle in enumerate(circles):
            is_active = i == current_index
            
            if i % bpm_config.subdivisions == 0:
                text = str((i // bpm_config.subdivisions) + 1)
            else:
                text = ''

            # Adjusted logic for updating circle size
            beat_strength_index = i if i < len(bpm_config.beat_strengths) else 0
            weight = bpm_config.beat_strengths[beat_strength_index]
            target_size = BEAT_STRENGTH_MAP.get(weight, 1.0) if is_active else 1.0
            size_factor = (circle.radius / circle.base_radius + (target_size - circle.radius / circle.base_radius) / SMOOTH_TRANSITION_FACTOR)
            circle.update(is_active, text, size_factor)
            circle.draw(screen)

        # Handle events and update display
        handle_events()
        pygame.display.flip()
        clock.tick(FPS)
        beat_counter += 1

    pygame.quit()


# Example of using a pattern from the dictionary
# chosen_pattern = BEAT_PATTERNS["simple_duple_pattern"]
# chosen_pattern = BEAT_PATTERNS["polyrhythm_pattern"]
# chosen_pattern = BEAT_PATTERNS["waltz_pattern"]
# chosen_pattern = BEAT_PATTERNS["quintuple_pattern_3_2"]
# chosen_pattern = BEAT_PATTERNS["quintuple_pattern_2_3"]
# chosen_pattern = BEAT_PATTERNS["compound_duple_pattern"]
# chosen_pattern = BEAT_PATTERNS["compound_triple_pattern"]
# chosen_pattern = BEAT_PATTERNS["seven_eight_pattern"]
# chosen_pattern = BEAT_PATTERNS["nine_eight_pattern"]
# chosen_pattern = BEAT_PATTERNS["eleven_eight_pattern"]
# chosen_pattern = BEAT_PATTERNS["thirteen_eight_pattern"]
# chosen_pattern = BEAT_PATTERNS["fifteen_eight_pattern"]
# chosen_pattern = BEAT_PATTERNS["song_verse_pattern"]
# chosen_pattern = BEAT_PATTERNS["new_nine_eight"]
# chosen_pattern = BEAT_PATTERNS["new_eleven_eight"]
# chosen_pattern = BEAT_PATTERNS["nine_eight_pattern"]
chosen_pattern = BEAT_PATTERNS["complex_rhythm_5_7"]

simulateBeat(bpm_initial_config=chosen_pattern)
