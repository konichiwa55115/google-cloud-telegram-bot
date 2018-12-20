import logging
import ConfigParser

# Read settings from configuration file
def getConfiguredClass(T, configFile):
    c = ConfigParser.ConfigParser()
    c.read(configFile)
    logger = logging.getLogger('TestBot')
    logger.setLevel(logging.DEBUG)
    base_url = 'https://api.telegram.org/bot%s/' % c.get('Settings', 'TOKEN')
    hook_token = c.get('Settings', 'HOOK_TOKEN')
    hook_url = 'https://%s.appspot.com/TG%s' % (c.get('Settings', 'PROJECT_ID'), hook_token)

    class Configured(T):
        def __init__(self, *args, **kwargs):
            super(Configured, self).__init__(*args, **kwargs)
            self.logger = logger
            self.base_url = base_url
            self.hook_url = hook_url
            self.hook_token = hook_token

    return Configured