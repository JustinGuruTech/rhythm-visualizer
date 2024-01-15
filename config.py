from dataclasses import dataclass


@dataclass
class BeatPatternConfig:
    beats_per_minute: int
    beats_per_measure: int
    beat_strengths: dict[int, float]
    # Default to 2, can be changed to 3 for triplets, etc.
    subdivisions: int = 2


# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 900
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
SMOOTH_TRANSITION_FACTOR = 5
# Mapping beat strengths to size factors
BEAT_STRENGTH_MAP = {
    0: 0.0,
    1: 0.25,
    2: 0.5,
    3: 1.0,  # Baseline beat strength
    4: 1.5,
    5: 2.0,
}
SOUND_FILE = 'sounds/hat2.wav'

BEAT_PATTERNS = {
    "simple_duple_pattern": BeatPatternConfig(
        beats_per_minute=240,
        beats_per_measure=4,
        beat_strengths=[5, 1, 1, 1, 5, 1, 1, 1]
    ),
    "polyrhythm_pattern": BeatPatternConfig(
        beats_per_minute=240,
        beats_per_measure=4,
        beat_strengths=[5, 1, 1, 1, 5, 1, 1, 1, 5, 1, 1, 1],
        subdivisions=3
    ),
    "waltz_pattern": BeatPatternConfig(
        beats_per_minute=340,
        beats_per_measure=3,
        beat_strengths=[5, 1, 1, 5, 1, 1]
    ),
    "quintuple_pattern_3_2": BeatPatternConfig(
        beats_per_minute=420,
        beats_per_measure=5,
        beat_strengths=[5, 2, 1, 5, 1, 5, 2, 1, 5, 1]
    ),
    "quintuple_pattern_2_3": BeatPatternConfig(
        beats_per_minute=420,
        beats_per_measure=5,
        beat_strengths=[5, 1, 5, 2, 2, 5, 1, 5, 2, 2]
    ),
    "compound_duple_pattern": BeatPatternConfig(
        beats_per_minute=320,
        beats_per_measure=6,
        beat_strengths=[5, 2, 1, 5, 2, 1, 5, 2, 1, 5, 2, 1],
    ),
    "compound_triple_pattern": BeatPatternConfig(
        beats_per_minute=420,
        beats_per_measure=9,
        beat_strengths=[5, 2, 1, 5, 2, 1, 5, 2, 1, 5, 2, 1, 5, 2, 1, 5, 2, 1]
    ),
    "seven_eight_pattern": BeatPatternConfig(
        beats_per_minute=360,
        beats_per_measure=7,
        beat_strengths=[5, 2, 1, 2, 5, 2, 1, 2, 5, 2, 1, 2, 5, 2]
    ),
    "nine_eight_pattern": BeatPatternConfig(
        beats_per_minute=360,
        beats_per_measure=9,
        beat_strengths=[5, 1, 4, 1, 4, 1, 5, 1, 1, 5, 1, 4, 1, 4, 1, 5, 1, 1]
    ),
    "eleven_eight_pattern": BeatPatternConfig(
        beats_per_minute=360,
        beats_per_measure=11,
        beat_strengths=[5, 1, 4, 1, 5, 1, 1, 4, 1,
                        4, 1, 5, 1, 4, 1, 5, 1, 1, 4, 1, 4, 1]
    ),
    "thirteen_eight_pattern": BeatPatternConfig(
        beats_per_minute=360,
        beats_per_measure=13,
        beat_strengths=[5, 1, 4, 1, 4, 1, 5, 2, 1, 5, 1,
                        4, 1, 5, 1, 1, 5, 1, 4, 1, 4, 1, 5, 1, 1, 5]
    ),
    "fifteen_eight_pattern": BeatPatternConfig(
        beats_per_minute=360,
        beats_per_measure=15,
        beat_strengths=[5, 1, 4, 1, 4, 1, 4, 1, 5, 2, 1, 4, 1,
                        4, 1, 5, 1, 4, 1, 4, 1, 4, 1, 5, 1, 1, 4, 1, 4, 1]
    ),
    "song_verse_pattern": BeatPatternConfig(
        beats_per_minute=340,
        beats_per_measure=7,
        beat_strengths=[5, 2, 5, 2, 3, 5, 2, 2, 5, 2, 5, 3, 2, 5, 2, 2, 5, 3, 2, 5, 5, 3,
                        2, 2, 5, 3, 2, 5, 2, 5, 2, 2, 5, 3, 2, 5, 3, 5, 3, 5, 5, 2, 5, 2, 3, 5, 2, 5] * 2
    ),
    "new_nine_eight": BeatPatternConfig(
        beats_per_minute=340,
        beats_per_measure=9,
        beat_strengths=[5, 3, 1, 5, 3, 1, 5, 3, 1, 5, 4, 3, 5, 3, 1, 5,
                        3, 1, 5, 3, 1, 5, 3, 1, 5, 3, 1, 5, 4, 3, 5, 3, 1, 5, 3, 1],
        subdivisions=3
    ),
    "new_eleven_eight": BeatPatternConfig(
        beats_per_minute=340,
        beats_per_measure=11,
        beat_strengths=[5, 3, 1, 5, 3, 1, 5, 3, 1, 5, 4, 3, 5, 3, 1, 5, 3, 1, 5,
                        3, 1, 5, 4, 3, 5, 3, 1, 5, 3, 1, 5, 3, 1, 5, 4, 3, 5, 3, 1, 5, 3, 1]
    ),
    "triplet_pattern": BeatPatternConfig(
        beats_per_minute=340,
        beats_per_measure=3,
        beat_strengths=[5, 0, 1, 0, 1, 0, 1, 0, 1],
        subdivisions=3
    ),
    "progressive_pattern": BeatPatternConfig(
        beats_per_minute=340,
        beats_per_measure=4,
        beat_strengths=[5, 0, 1, 0, 1, 0, 1, 0, 1],
        subdivisions=3
    ),
    # This one is awesome
    "long_pattern_in_seven": BeatPatternConfig(
        beats_per_minute=340,
        beats_per_measure=7,
        # 28 beats with a pattern syncopated over the 28 beats and a pattern syncopated over 7 beats
        beat_strengths=[5, 0, 1, 0, 1, 0, 1, 0, 1] * 4 + [5, 0, 1, 0, 1, 0, 1],
        subdivisions=3
    ),
    # This is sick too!
    "long_pattern_in_eleven": BeatPatternConfig(
        beats_per_minute=340,
        beats_per_measure=11,
        # 44 beats with a pattern syncopated over the 44 beats and a pattern syncopated over 11 beats
        beat_strengths=[5, 0, 1, 0, 1, 0, 1, 0, 1] * 4 + [5, 0, 1, 0, 1, 0, 1] * 4 + [5, 0, 1, 0, 1, 0, 1],
        subdivisions=3
    ),
    "long_pattern_in_five_syncopated": BeatPatternConfig(
        beats_per_minute=340,
        beats_per_measure=5,
        # 20 beats with a pattern syncopated over the 20 beats and a pattern syncopated over 5 beats
        beat_strengths=[5, 0, 1, 0, 1, 0, 1, 0, 1] * 4 + [5, 0, 1, 0, 1],
        subdivisions=3
    ),
    "bouncy_seven_pattern": BeatPatternConfig(
        beats_per_minute=340,
        beats_per_measure=7,
        beat_strengths=[5, 0, 1, 0, 1, 0, 1, 0, 1] * 2 + [5, 0, 1],
        subdivisions=3
    ),
    "bouncy_eleven_pattern": BeatPatternConfig(
        beats_per_minute=340,
        beats_per_measure=11,
        beat_strengths=[5, 0, 1, 0, 1, 0, 1, 0, 1] * 4 + [5, 0, 1],
        subdivisions=3
    ),
    "massive_chorus_pattern_in_six": BeatPatternConfig(
        beats_per_minute=340,
        beats_per_measure=6,
        beat_strengths=[5, 0, 1, 0, 1, 0, 1, 0, 1] * 4 + [5, 0, 1],
        subdivisions=3
    ),
    # Complex rhythm that uses full range of beat strengths, odd time, and subdivisions
    "complex_rhythm": BeatPatternConfig(
        beats_per_minute=340,
        beats_per_measure=9,
        # 36 beats with a pattern syncopated in group sizes of 9x4 and 6x6, using weights 1, 2, 3, 4, 5
        beat_strengths=[5, 1, 2, 3, 4, 5, 1, 2, 3] * 4 + [5, 1, 2, 3, 4, 5] * 6,
        subdivisions=3
    ),
    # Subdivisions of 5
    "complex_rhythm_5": BeatPatternConfig(
        beats_per_minute=340,
        beats_per_measure=6,
        beat_strengths=[5, 1, 2, 3, 4, 5, 1, 2, 3] * 4 + [5, 1, 2, 3, 4, 5] * 6,
        subdivisions=5
    ),
    # Subdivisions of 5 and in 7
    "complex_rhythm_5_7": BeatPatternConfig(
        beats_per_minute=340,
        beats_per_measure=7,
        beat_strengths=[5, 1, 2, 3, 4, 5, 1, 2, 3] * 4 + [5, 1, 2, 3, 4, 5] * 6,
        subdivisions=5
    ),
}
