from Robinhood import Robinhood

class User:
    def __init__(self, username=''):
        self.logged_in = None
        self.username = username
        self.trader = Robinhood()

    def log_in(self):
        self.logged_in = self.trader.login(username=username_input,password=password_input,mfa_code=auth_code)


    def __str__(self):
        return 'Username: ' + self.username
