import pygame
import time
import math

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 1200
CIRCLE_RADIUS = 65
SMALL_CIRCLE_RADIUS = 35
CENTER_X, CENTER_Y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
FPS = 60  # Higher frame rate for smoother transitions
BEAT_COLOR_ACTIVE = (96, 224, 130)
BEAT_COLOR_INACTIVE = (200, 220, 200)
BUTTON_TEXT_COLOR = (255, 255, 255)
BUTTON_BG_COLOR = (0, 0, 0)
FONT_SIZE_LARGE = 36
FONT_SIZE_MEDIUM = 30
CIRCLE_DISTANCE = 300
CIRCLE_BORDER_WIDTH = 2
SMOOTH_TRANSITION_FACTOR = 10
# New constant for mapping weights to size factors
BEAT_STRENGTH_MAP = {
    1: 0.5,
    2: 0.75,
    3: 1.0,  # Assuming 3 is the baseline
    4: 1.25,
    5: 1.5,
}

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
        pygame.draw.circle(screen, BUTTON_BG_COLOR, self.position, self.radius, CIRCLE_BORDER_WIDTH)  # Add border
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
        self.current_color = self.lerp_color(self.color_start, self.color_end, t)

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
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.width, self.height), 0)
        if self.text != '':
            font = pygame.font.Font(None, 30)
            text = font.render(self.text, 1, (255, 255, 255))
            screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def is_over(self, pos):
        if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
            return True
        return False
    

def simulateBeat(per_minute, per_measure, beat_strengths, background_start=(120, 120, 120), background_end=(150, 150, 150)):
    pygame.init()

    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

    bpm = per_minute
    beat_delay = 60 / bpm / 2

    metronome = Metronome(background_start, background_end)

    num_circles = per_measure

    clock = pygame.time.Clock()

    circles = []
    for i in range(num_circles * 2):
        angle = 2 * math.pi * i / (num_circles * 2)
        position = (CENTER_X + CIRCLE_DISTANCE * math.cos(angle), CENTER_Y + CIRCLE_DISTANCE * math.sin(angle))
        radius = SMALL_CIRCLE_RADIUS if i % 2 else CIRCLE_RADIUS
        circle = CircleBeat(position, radius, BUTTON_TEXT_COLOR)
        circles.append(circle)

    running = True
    beat_counter = 0
    interpolation_steps = FPS / (bpm / 60)  # Number of frames per beat

    # UI Buttons for rhythm selection
    btn_subdivision1 = Button(50, 1050, 200, 50, '4/4 Beat')
    btn_subdivision2 = Button(300, 1050, 200, 50, '7/4 Beat')

    while running:
        # Interpolate metronome color
        t = abs(2 * (beat_counter / interpolation_steps % (num_circles * 2)) / (num_circles * 2) - 1)
        metronome.update_color(t, num_circles * 2 * 2)
        metronome.draw(screen)

        # Draw buttons
        btn_subdivision1.draw(screen)
        btn_subdivision2.draw(screen)

        # Interpolate circle sizes with updated weights
        for i, circle in enumerate(circles):
            is_active = i == int(beat_counter / interpolation_steps) % (num_circles * 2)
            text = str((i // 2) + 1) if i % 2 == 0 else ''
            
            # Use the weight to get the target size from the mapping
            weight = beat_strengths[i]
            target_size = BEAT_STRENGTH_MAP.get(weight, 1.0) if is_active else 1.0
            
            current_size = circle.radius / circle.base_radius
            size_factor = current_size + (target_size - current_size) / SMOOTH_TRANSITION_FACTOR  # Smooth transition
            circle.update(is_active, text, size_factor)
            circle.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if btn_subdivision1.is_over(pos):
                    beat_pattern = [1, 0.75, 0.5, 0.25, 1, 0.75, 0.5, 0.25, 1, 0.75, 0.5, 0.25, 1, 0.75, 0.5, 0.25]
                    per_measure = 4
                    simulateBeat(per_minute=per_minute, per_measure=8, beat_strengths=beat_pattern)
                if btn_subdivision2.is_over(pos):
                    beat_pattern = [1, 0.5, 0.5, 0.5, 1, 0.5, 0.5, 0.5, 1, 0.5, 0.5, 0.5, 1, 0.5]  # Original pattern for 7/4
                    per_measure = 7
                    simulateBeat(per_minute=per_minute, per_measure=7, beat_strengths=beat_pattern)

        pygame.display.flip()
        clock.tick(FPS)
        beat_counter += 1

    pygame.quit()

# Example usage
beat_strengths = [5, 2, 2, 2, 5, 2, 2, 2, 5, 2, 2, 2, 5, 2]
# beat_strengths= [1.5, 1, 1.5, 1, .5, 1.5, 1, 1.5, 1, .5, 1, 1]
simulateBeat(per_minute=280, per_measure=7, beat_strengths=beat_strengths)