import pygame
import time
import math

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 1200
CENTER_X, CENTER_Y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
FPS = 60  # Frame rate for smooth transitions
BEAT_COLOR_ACTIVE = (96, 224, 130)
BEAT_COLOR_INACTIVE = (200, 220, 200)
BUTTON_TEXT_COLOR = (255, 255, 255)
BUTTON_BG_COLOR = (0, 0, 0)
FONT_SIZE_LARGE = 36
CIRCLE_DISTANCE = 300
CIRCLE_RADIUS = 65
SMALL_CIRCLE_RADIUS = 50
CIRCLE_BORDER_WIDTH = 2
SMOOTH_TRANSITION_FACTOR = 10
# Mapping beat strengths to size factors
BEAT_STRENGTH_MAP = {
    1: 0.5,
    2: 0.75,
    3: 1.0,  # Baseline beat strength
    4: 1.25,
    5: 1.5,
}


class BeatPatternConfig:
    """
    Holds configuration for the beat pattern.
    """

    def __init__(self, beats_per_minute, beats_per_measure, beat_strengths):
        self.beats_per_minute = beats_per_minute
        self.beats_per_measure = beats_per_measure
        self.beat_strengths = beat_strengths


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


class Button:
    def __init__(self, x, y, width, height, text=''):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0),
                         (self.x, self.y, self.width, self.height), 0)
        if self.text != '':
            font = pygame.font.Font(None, 30)
            text = font.render(self.text, 1, (255, 255, 255))
            screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2),
                        self.y + (self.height / 2 - text.get_height() / 2)))

    def is_over(self, pos):
        if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
            return True
        return False


def simulateBeat(bpm_initial_config):
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    clock = pygame.time.Clock()

    bpm_config = bpm_initial_config
    metronome = Metronome((130, 130, 130), (190, 190, 190))

    # Creating beat circles
    num_circles = bpm_config.beats_per_measure
    circles = [CircleBeat(
        position=(
            CENTER_X + CIRCLE_DISTANCE * math.cos(2 * math.pi * i / (num_circles * 2)),
            CENTER_Y + CIRCLE_DISTANCE * math.sin(2 * math.pi * i / (num_circles * 2))
        ),
        base_radius=SMALL_CIRCLE_RADIUS if i % 2 else CIRCLE_RADIUS,
        color=BUTTON_TEXT_COLOR
    ) for i in range(num_circles * 2)]

    # UI Buttons for rhythm selection
    btn_subdivision1 = Button(50, 1050, 200, 50, '4/4 Beat')
    btn_subdivision2 = Button(300, 1050, 200, 50, '7/4 Beat')

    running = True
    beat_counter = 0
    interpolation_steps = FPS / (bpm_config.beats_per_minute / 60)
    update_configuration_required = False

    while running:
        metronome.update_color(
            beat_counter / interpolation_steps % (num_circles * 2),
            num_circles * 2 * 2
        )
        metronome.draw(screen)
        btn_subdivision1.draw(screen)
        btn_subdivision2.draw(screen)

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
                if btn_subdivision1.is_over(pos):
                    bpm_config = BeatPatternConfig(
                        beats_per_minute=bpm_config.beats_per_minute,
                        beats_per_measure=8,
                        beat_strengths=[3, 2, 1, 1, 3, 2,
                                        1, 1, 3, 2, 1, 1, 3, 2, 1, 1],
                    )
                    update_configuration_required = True
                if btn_subdivision2.is_over(pos):
                    bpm_config = BeatPatternConfig(
                        beats_per_minute=bpm_config.beats_per_minute,
                        beats_per_measure=7,
                        beat_strengths=[5, 2, 2, 2, 5,
                                        2, 2, 2, 5, 2, 2, 2, 5, 2],
                    )
                    update_configuration_required = True

        if update_configuration_required:
            num_circles = bpm_config.beats_per_measure
            circles = []
            for i in range(num_circles * 2):
                angle = 2 * math.pi * i / (num_circles * 2)
                position = (CENTER_X + CIRCLE_DISTANCE * math.cos(angle),
                            CENTER_Y + CIRCLE_DISTANCE * math.sin(angle))
                radius = SMALL_CIRCLE_RADIUS if i % 2 else CIRCLE_RADIUS
                circle = CircleBeat(position, radius, BUTTON_TEXT_COLOR)
                circles.append(circle)

                beat_delay = 60 / bpm_config.beats_per_minute / 2
                interpolation_steps = FPS / (bpm_config.beats_per_minute / 60)
                beat_counter = 0  # Reset the beat counter
                update_configuration_required = False

        pygame.display.flip()
        clock.tick(FPS)
        beat_counter += 1

    pygame.quit()


# Example usage
beat_pattern_config = BeatPatternConfig(
    beats_per_minute=360,
    beats_per_measure=7,
    beat_strengths=[5, 2, 2, 2, 5, 2, 2, 2, 5, 2, 2, 2, 5, 2],
)
waltz_pattern_config = BeatPatternConfig(
    beats_per_minute=240,
    beats_per_measure=3,
    beat_strengths=[5, 1, 1, 5, 1, 1],
)
quintuple_pattern_config_3_2 = BeatPatternConfig(
    beats_per_minute=220,
    beats_per_measure=5,
    beat_strengths=[5, 2, 1, 5, 1, 5, 2, 1, 5, 1],
)
quintuple_pattern_config_2_3 = BeatPatternConfig(
    beats_per_minute=220,
    beats_per_measure=5,
    beat_strengths=[5, 1, 5, 2, 2, 5, 1, 5, 2, 2],
)
compound_duple_pattern_config = BeatPatternConfig(
    beats_per_minute=220,
    beats_per_measure=6,
    beat_strengths=[5, 2, 1, 5, 2, 1, 5, 2, 1, 5, 2, 1],
)
compound_triple_pattern_config = BeatPatternConfig(
    beats_per_minute=620,
    beats_per_measure=9,
    beat_strengths=[5, 2, 1, 5, 2, 1, 5, 2, 1, 5, 2, 1, 5, 2, 1, 5, 2, 1],
)
seven_eight_pattern_config = BeatPatternConfig(
    beats_per_minute=260,
    beats_per_measure=7,
    beat_strengths=[5, 1, 4, 1, 5, 1, 1, 5, 1, 4, 1, 5, 1, 1],
)
nine_eight_pattern_config = BeatPatternConfig(
    beats_per_minute=260,
    beats_per_measure=9,
    beat_strengths=[5, 1, 4, 1, 4, 1, 5, 1, 1, 5, 1, 4, 1, 4, 1, 5, 1, 1]
)
eleven_eight_pattern_config = BeatPatternConfig(
    beats_per_minute=260,
    beats_per_measure=11,
    beat_strengths=[5, 1, 4, 1, 5, 1, 1, 4, 1,
                    4, 1, 5, 1, 4, 1, 5, 1, 1, 4, 1, 4, 1]
)
thirteen_eight_pattern_config = BeatPatternConfig(
    beats_per_minute=260,
    beats_per_measure=13,
    beat_strengths=[5, 1, 4, 1, 4, 1, 5, 2, 1, 5, 1,
                    4, 1, 5, 1, 1, 5, 1, 4, 1, 4, 1, 5, 1, 1, 5]
)
fifteen_eight_pattern_config = BeatPatternConfig(
    beats_per_minute=260,
    beats_per_measure=15,
    beat_strengths=[5, 1, 4, 1, 4, 1, 4, 1, 5, 2, 1, 4, 1,
                    4, 1, 5, 1, 4, 1, 4, 1, 4, 1, 5, 1, 1, 4, 1, 4, 1],
)

# Beat strength of each beat in the phrase (two bars per pattern)
beat_strengths_phrase = [
    # Pattern 1
    5, 2, 5, 2, 3, 5, 2, 2,  # **1** 2 **3** 4 + **5** 6 7
    5, 2, 5, 3, 2, 5, 2, 2,  # **1** 2 **3** + 4 **5** 6 7
    
    # Pattern 2
    5, 2, 5, 2, 3, 5, 2, 2,  # **1** 2 **3** 4 + **5** 6 7
    5, 2, 5, 3, 2, 5, 5, 2,  # **1** 2 **3** + 4 **5** **6** 7
    
    # Pattern 3
    5, 3, 2, 5, 5, 3, 2, 2,  # **1** + 2 **3** **4** + 5 6 7
    5, 3, 2, 5, 2, 5, 2, 2,  # **1** + 2 **3** **4** 5 **6** 7
    
    # Pattern 4
    5, 3, 2, 5, 3, 5, 3, 5,  # **1** + 2 **3** + 4 **5** + 6 **7**
    5, 2, 5, 2, 3, 5, 2, 5   # **1** 2 **3** 4 + **5** 6 **7**
]

# Since each beat is represented once, for the visualizer, we need to double the length of the pattern
visualizer_beat_strengths = beat_strengths_phrase * 2
song_verse_pattern_config = BeatPatternConfig(beats_per_minute=240, beats_per_measure=7, beat_strengths=visualizer_beat_strengths)

simulateBeat(bpm_initial_config=eleven_eight_pattern_config)
