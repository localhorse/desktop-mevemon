""" wrapper for ini-file-based settings"""
import configobj
import constants

class Settings:
    # this needs changin', no time right now though --danny
    """ Reads and writes settings to a config files based on the INI format.
        
        For example, a typical mEveMon config file (at '~/.mevemon/mevemon.cfg')will look like this:

        [accounts]
            [[account.<uid1>]]
            uid = <uid1>
            apikey = <apikey1>

            [[account.<uid2>]]
            uid = <uid2>
            apikey = <apikey2>

        [general]
        # this is just a fake example, we don't store any general
        # settings yet...
        super_cow_powers = True

        More information on the format/syntax of the config file can be found
        on the ConfigObj site (http://www.voidspace.org.uk/python/configobj.html#the-config-file-format).
    """
    def __init__(self, cfg_file=constants.CONFIG_PATH):
        self.cfg_file = cfg_file
        self.config = configobj.ConfigObj(self.cfg_file)
        # windows chokes here
        ##self._convert_gconf_to_cfgfile()
   
    def get_accounts(self):
        """ Returns a dictionary containing uid:api_key pairs gathered from the config file
        """
        account_dict = {}
        try:
            cfg_accounts = self.config['accounts'].values()
        except KeyError:
            return account_dict
        
        for account in cfg_accounts:
            account_dict[account['kid']] = account['vcode']

        return account_dict

    def get_vcode(self, kid):
        """ Returns the verification code associated with the given kid.
        """
        try:
            vcode = self.get_accounts()[kid]
            return vcode
        except KeyError:
            raise Exception("KID '%s' is not in settings") 

    def add_account(self, kid, vcode):
        """ Adds the provided kid:vcode pair to the config file.
        """
        if 'accounts' not in self.config.sections:
            self.config['accounts'] = {}

        self.config['accounts']['account.%s' % kid] = {}
        self.config['accounts']['account.%s' % kid]['kid'] = kid
        self.config['accounts']['account.%s' % kid]['vcode'] = vcode
        self.write()

    def remove_account(self, kid):
        """ Removes the provided kid key from the config file
        """
        for key in self.config['accounts']:
            if self.config['accounts'][key]['kid'] == kid:
                del self.config['accounts'][key]
                self.write()
        
    def write(self):
        """ write out the settings into the config file """
        if isinstance(self.cfg_file, str):
            self.config.write()
        else: # cfg_file is a file-like object (StringIO, etc..)
            self.config.write(self.cfg_file)

    def _convert_gconf_to_cfgfile(self):
        """ A temporary method to convert from the old 0.4-9 gconf-based
            settings to the new file-based settings.
        """
        import gconf_settings
        gsettings = gconf_settings.Settings()
        for kid, vcode in gsettings.get_accounts().items():
            self.add_account(kid, vcode)
            gsettings.remove_account(kid)
