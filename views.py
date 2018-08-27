from tornado import web

from db import execute
from service import register, login, upload


class BaseHandler(web.RequestHandler):
    def get_current_user(self):
        username = self.get_secure_cookie('current_user')

        if not username:
            return None

        return username


class MainHandler(BaseHandler):
    @web.authenticated
    def get(self):
        self.render('home.html')


class RegistrationHandler(BaseHandler):
    def get(self):
        self.render('register.html')

    def post(self):
        username = self.get_argument('username')
        email = self.get_argument('email')
        password = self.get_argument('password')
        confirm_password = self.get_argument('confirm_password')

        try:
            register(username, email, password, confirm_password)
        except Exception:
            raise

        self.redirect('/login')


class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')

        try:
            login(username, password)
        except Exception:
            raise

        self.set_secure_cookie('current_user', username)
        self.redirect('/')


class LogoutHandler(BaseHandler):
    def get(self):
        self.set_secure_cookie('current_user', '')
        self.redirect('/')


class UploadHandler(BaseHandler):
    @web.authenticated
    def get(self):
        self.render('upload_form.html')

    @web.authenticated
    def post(self):
        if not self.request.files:
            self.set_status(400)
            self.write('No files.')
            return

        file_info = self.request.files['file'][0]
        file_name = file_info['filename']
        file_body = file_info['body']

        try:
            upload(file_body, file_name)
        except Exception:
            raise

        self.write('File was successfully uploaded.')


class FileHandler(BaseHandler):
    @web.authenticated
    def get(self):
        files = execute('''SELECT uu.* FROM user_uploads uu
            JOIN users u ON u.id = uu.user_id
            WHERE u.username = :current_user''', current_user=self.current_user)

        self.render('file_list.html', files=files)
