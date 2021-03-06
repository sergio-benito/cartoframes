from ._version import __version__
from .utils.utils import check_package
from .core.cartodataframe import CartoDataFrame
from .core.logger import set_log_level
from .io.carto import read_carto, to_carto, has_table, delete_table, rename_table, \
                      copy_table, create_table_from_query, describe_table, update_privacy_table


# Check installed packages versions
check_package('carto', '>=1.8.3')
check_package('pandas', '>=0.23.0')
check_package('geopandas', '>=0.6.0')


__all__ = [
    '__version__',
    'CartoDataFrame',
    'read_carto',
    'to_carto',
    'has_table',
    'delete_table',
    'rename_table',
    'copy_table',
    'create_table_from_query',
    'describe_table',
    'update_privacy_table',
    'set_log_level'
]
