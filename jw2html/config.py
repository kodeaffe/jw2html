import os, logging
from configparser import ConfigParser


LOGGER = logging.getLogger(__name__)
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
config = ConfigParser()
parsed = config.read(CONFIG_FILENAMES)
if not parsed:
    raise ConfigNotFoundError(
        'Please make sure at least one of these ini files exist:\n%s' %\
        '\n'.join(CONFIG_FILENAMES)
    )
else:
    LOGGER.info('Read from config files: %s' % ', '.join(parsed))

# Set up settings dict to be imported
settings = config['SETTINGS']
__all__ = ['settings']
