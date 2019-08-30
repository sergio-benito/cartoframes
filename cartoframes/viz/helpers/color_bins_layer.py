from __future__ import absolute_import

from .utils import serialize_palette

from ..layer import Layer
from .. import defaults

def color_bins_layer(
        source, value, title='', method='quantiles', bins=5,
        breaks=None, palette=None, size=None, opacity=None,
        strokecolor=None, strokewidth=None, description='',
        footer='', legend=True, popup=True, widget=False, animate=None):
    """Helper function for quickly creating a classed color map.

    Args:
        source (:py:class:`Dataset <cartoframes.data.Dataset>` or str): Dataset
          or text representing a table or query associated with user account.
        value (str): Column to symbolize by.
        title (str, optional): Title of legend.
        method (str, optional): Classification method of data: "quantiles", "equal", "stdev".
          Default is "quantiles".
        bins (int, optional): Number of size classes (bins) for map. Default is 5.
        breaks (int[], optional): Assign manual class break values.
        palette (str, optional): Palette that can be a named cartocolor palette
          or other valid CARTO VL palette expression. Default is `purpor`.
        size (int, optional): Size of point or line features.
        opacity (int, optional): Opacity value for point color and line features.
          Default is '0.8'.
        strokewidth (int, optional): Size of the stroke on point features.
        strokecolor (str, optional): Color of the stroke on point features.
          Default is '#222'.
        description (str, optional): Description text legend placed under legend title.
        footer (str, optional): Footer text placed under legend items.
        legend (bool, optional): Display map legend: "True" or "False".
          Set to "True" by default.
        popup (bool, optional): Display popups on hover and click: "True" or "False".
          Set to "True" by default.
        widget (bool, optional): Display a widget for mapped data: "True" or "False".
          Set to "False" by default.
        animate (str, optional): Animate features by date/time or other numeric field.

    Returns:
        cartoframes.viz.Layer: Layer styled by `value`.
        Includes a legend, popup and widget on `value`.
    """
    if method not in ('quantiles', 'equal', 'stdev'):
        raise ValueError('Available methods are: "quantiles", "equal", "stdev".')

    func = 'buckets' if breaks else {
        'quantiles': 'globalQuantiles',
        'equal': 'globalEqIntervals',
        'stdev': 'globalStandardDev'
    }.get(method)

    default_palette = 'purpor' if breaks else {
        'quantiles': 'purpor',
        'equal': 'purpor',
        'stdev': 'temps'
    }.get(method)

    animation_filter = 'animation(linear(${}), 20, fade(1,1))'.format(animate) if animate else '1'

    return Layer(
        source,
        style={
            'point': {
                'color': 'opacity(ramp({0}(${1}, {2}), {3}),{4})'.format(
                    func, value, breaks or bins, serialize_palette(palette) or default_palette,
                    opacity or '1'),
                'width': '{0}'.format(
                    size or defaults.STYLE['point']['width']),
                'strokeColor': '{0}'.format(
                    strokecolor or defaults.STYLE['point']['strokeColor']),
                'strokeWidth': '{0}'.format(
                    strokewidth or defaults.STYLE['point']['strokeWidth']),
                'filter': animation_filter
            },
            'line': {
                'color': 'opacity(ramp({0}(${1}, {2}), {3}),{4})'.format(
                    func, value, breaks or bins, serialize_palette(palette) or default_palette,
                    opacity or '1'),
                'width': '{0}'.format(
                    size or defaults.STYLE['line']['width']),
                'filter': animation_filter
            },
            'polygon': {
                'color': 'opacity(ramp({0}(${1}, {2}), {3}), {4})'.format(
                    func, value, breaks or bins, serialize_palette(palette) or default_palette, 
                    opacity or '0.9'),
                'strokeColor': '{0}'.format(
                    strokecolor or defaults.STYLE['polygon']['strokeColor']),
                'strokeWidth': '{0}'.format(
                    strokewidth or defaults.STYLE['polygon']['strokeWidth']),
                'filter': animation_filter
            }
        },
        popup=popup and not animate and {
            'hover': {
                'title': title or value,
                'value': '$' + value
            }
        },
        legend=legend and {
            'type': {
                'point': 'color-bins-point',
                'line': 'color-bins-line',
                'polygon': 'color-bins-polygon'
            },
            'title': title or value,
            'description': description,
            'footer': footer
        },
        widgets=[
            animate and {
                'type': 'time-series',
                'value': animate,
                'title': 'Animation'
            },
            widget and {
                'type': 'histogram',
                'value': value,
                'title': 'Distribution'
            }
        ]
    )
