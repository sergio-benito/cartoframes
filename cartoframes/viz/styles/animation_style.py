from .utils import get_value
from ..style import Style


def animation_style(value, duration=20, color=None, size=None, opacity=None,
                    stroke_color=None, stroke_width=None):
    """Helper function for quickly creating an animated layer"""

    fade = '(1, 1)'
    style = {
        'point': {
            'color': 'opacity({0}, {1})'.format(
                get_value(color, 'color', 'point'),
                get_value(opacity, 1)),
            'width': get_value(size, 'width', 'point'),
            'strokeColor': get_value(stroke_color, 'strokeColor', 'point'),
            'strokeWidth': get_value(stroke_width, 'strokeWidth', 'point'),
            'filter': _animation_filter(value, duration, fade)
        },
        'line': {
            'color': 'opacity({0}, {1})'.format(
                get_value(color, 'color', 'line'),
                get_value(opacity, 1)),
            'width': get_value(size, 'width', 'line'),
            'filter': _animation_filter(value, duration, fade)
        },
        'polygon': {
            'color': 'opacity({0}, {1})'.format(
                get_value(color, 'color', 'polygon'),
                get_value(opacity, 0.9)),
            'strokeColor': get_value(stroke_color, 'strokeColor', 'polygon'),
            'strokeWidth': get_value(stroke_width, 'strokeWidth', 'polygon'),
            'filter': _animation_filter(value, duration, fade)
        }
    }

    return Style('animation', value, style)


def _animation_filter(value, duration, fade):
    return 'animation(linear(${0}), {1}, fade{2})'.format(value, duration, fade)
