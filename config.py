import os
from configparser import ConfigParser


CONFIG_FILENAMES = [
    os.path.join(os.sep, 'etc', 'jw2html.ini'),
    os.path.join(os.getenv('HOME'), '.jw2html.ini'),
]


class ConfigNotFoundError(Exception):
    """
    Exception to raise if none of the config files could be found.
    """
    pass


# Read-in the config file(s)
config_parser = ConfigParser()
if not config_parser.read(CONFIG_FILENAMES):
    raise ConfigNotFoundError(
        'Please make sure at least one of these ini files exist:\n%s' %\
        '\n'.join(CONFIG_FILENAMES)
    )

# Set up settings dict to be imported
settings = dict(config_parser.items('SETTINGS'))
__all__ = ['settings']
