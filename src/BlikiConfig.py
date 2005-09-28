import ConfigParser
import os

# XXX: This module has serious problem. The problem lies in testRoot.
# It means that instead of os.walk recursive function must be used

class BlikiConfigException(Exception):
    pass


class BlikiConfig:
    """Bliki config class allows to browse config information in hierarchical
    manner.

    """

    def __init__(self):
        self.config = []
        self.current_path = ''

    def testRoot(self, root, files):
        """ This function must be used inside of os.walk cycle.
        It founds parent of 'root' directory and reads new config files
        if such exists.
        """

        self.current_path = root

        if len(self.config) > 0:
            found = False
            while not found and len(self.config) > 0:
                try:
                    root.index(self.config[-1]['path'])
                    found = True
                except ValueError:
                    self.config.pop()

        try:
            files.index('pybliki.cfg')
            cfg = ConfigParser.ConfigParser()
            cfg.read([os.path.join(root, 'pybliki.cfg')])
            self.config.append({'path': root, 'config': cfg})
        except ValueError:
            pass

    def get(self, section, option):
        """Returns path and required option from section."""
        try:
            idx = -1
            while True:
                try:
                    res = self.config[idx]['config'].get(section, option)

                    return (self.config[idx]['path'], res)
                except (ConfigParser.NoSectionError,
                        ConfigParser.NoOptionError):
                    idx -= 1
        except IndexError:
            raise BlikiConfigException('Section "%s", Option "%s" not found' %
                                       (section, option))
