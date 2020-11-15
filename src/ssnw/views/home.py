from flask.views import View


class HomeView(View):

    def dispatch_request(self):
        return 'hello world (home)'
