


class Contract:

    def __init__(self, address, username, password, form_data, session) -> None:
        self.address = address
        self.username = username
        self.password = password
        self.session = session
        self.login_url = f'https://{address}/ws/v1.0/auth/process'
        self.simlist_url = 'https://{address}/ws/v1.0/subscriber/mobile/list?from={start}&size={size}'
        self.form_data = form_data
        # self.payload = {'captchaTime': 'undefined', 'username': self.username, 'password': self.password}
        form_list = [['captchaTime', 'undefined'], ['username', self.username], ['password', self.password]]
        for value in form_list:
            self.form_data.add_fields(value)


    