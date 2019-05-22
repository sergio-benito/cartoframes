from __future__ import absolute_import

from ..layer import Layer


def color_category_layer(source, category, top=11, palette='bold'):
    return Layer(
        source,
        style={
            'point': {
                'color': 'ramp(top(${0}, {1}), {2})'.format(category, top, palette)
            },
            'line': {
                'color': 'ramp(top(${0}, {1}), {2})'.format(category, top, palette)
            },
            'polygon': {
                'color': 'opacity(ramp(top(${0}, {1}), {2}),0.9)'.format(category, top, palette)
            }
        },
        popup={},
        legend={}
    )
