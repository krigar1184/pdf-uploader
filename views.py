from tornado import web
from service import login, upload


class BaseHandler(web.RequestHandler):
    def get_current_user(self):
        return 'nils'


class MainHandler(BaseHandler):
    @web.authenticated
    def get(self):
        self.render('home.html')


class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')

        try:
            login(username, password)
        except Exception:
            pass

        self.redirect('/')


class LogoutHandler(BaseHandler):
    def get(self):
        self.redirect('/')


class UploadHandler(BaseHandler):
    def get(self):
        self.render('upload_form.html')

    def post(self):
        if not self.request.files:
            self.set_status(400)
            self.write('No files.')
            return

        file_info = self.request.files['file'][0]  # TODO handle multiple upload
        file_name = file_info['filename']
        file_body = file_info['body']
        content_type = file_info['content_type']

        try:
            upload(file_body)
        except Exception:
            raise

        self.write('TODO: handle upload')


class FileHandler(BaseHandler):
    def get(self):
        self.render('file_list.html')


class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.write('TODO: logout')
