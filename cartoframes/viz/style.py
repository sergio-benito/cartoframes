from ..utils.utils import merge_dicts, text_match
from . import defaults


class Style:
    """Style

    Args:
        data (str, dict): The style for the layer.
    """

    def __init__(self, data=None, value=None, default_legends=None,
                 default_widgets=None, default_popups=None):
        self._style = self._init_style(data=data)
        self._value = value
        self._default_legends = default_legends
        self._default_widgets = default_widgets
        self._default_popups = default_popups

    def _init_style(self, data):
        if data is None:
            return defaults.STYLE
        elif isinstance(data, (str, dict)):
            return data
        else:
            raise ValueError('`style` must be a dictionary')

    @property
    def value(self):
        return self._value

    @property
    def default_legends(self):
        return self._default_legends

    @property
    def default_widgets(self):
        return self._default_widgets

    @property
    def default_popups(self):
        return self._default_popups

    def compute_viz(self, geom_type, variables={}):
        style = self._style
        default_style = defaults.STYLE[geom_type]

        if isinstance(style, str):
            # Only for testing purposes
            return self._parse_style_str(style, default_style, variables)
        elif isinstance(style, dict):
            if geom_type in style:
                style = style.get(geom_type)
            return self._parse_style_dict(style, default_style, variables)
        else:
            raise ValueError('`style` must be a dictionary')

    def _parse_style_dict(self, style, default_style, ext_vars):
        variables = merge_dicts(style.get('vars', {}), ext_vars)
        properties = merge_dicts(default_style, style)

        serialized_variables = self._serialize_variables(variables)
        serialized_properties = self._serialize_properties(properties)

        return serialized_variables + serialized_properties

    def _parse_style_str(self, style, default_style, ext_vars):
        variables = ext_vars
        default_properties = self._prune_defaults(default_style, style)

        serialized_variables = self._serialize_variables(variables)
        serialized_default_properties = self._serialize_properties(default_properties)

        return serialized_variables + serialized_default_properties + style

    def _serialize_variables(self, variables={}):
        output = ''
        for var in variables:
            output += '@{name}: {value}\n'.format(
                name=var,
                value=variables.get(var)
            )
        return output

    def _serialize_properties(self, properties={}):
        output = ''
        for prop in properties:
            if prop == 'vars':
                continue
            output += '{name}: {value}\n'.format(
                name=prop,
                value=properties.get(prop)
            )
        return output

    def _prune_defaults(self, default_style, style):
        output = default_style.copy()
        if 'color' in output and text_match(r'color\s*:', style):
            del output['color']
        if 'width' in output and text_match(r'width\s*:', style):
            del output['width']
        if 'strokeColor' in output and text_match(r'strokeColor\s*:', style):
            del output['strokeColor']
        if 'strokeWidth' in output and text_match(r'strokeWidth\s*:', style):
            del output['strokeWidth']
        return output
