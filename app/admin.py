import asyncio

from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.config import settings
from app.crud import get_user_by_username
from app.database import engine
from app.models import Log, Notification, Student, User
from app.security import verify_password
from app.tasks import process_notification


class LogAdmin(ModelView, model=Log):
    column_list = [Log.id, Log.notification_id, Log.student_id, Log.status]
    column_sortable_list = [Log.id, Log.notification_id, Log.student_id, Log.status]
    page_size_options = [100, 250, 500]
    page_size = 500


class NotificationAdmin(ModelView, model=Notification):
    column_list = [Notification.id, Notification.message]
    form_columns = [Notification.message]
    page_size_options = [100, 250, 500]
    page_size = 100
    form_widget_args = {
        'message': {
            'style': 'height: 30em;',
        },
    }

    async def after_model_change(self, data, model, is_created, request):
        await super().on_model_change(data, model, is_created, request)
        asyncio.create_task(process_notification(model))


class StudentAdmin(ModelView, model=Student):
    column_list = [Student.id, Student.phone_number, Student.username, Student.full_name, Student.birth_date]
    form_columns = [Student.phone_number, Student.username, Student.full_name, Student.birth_date]
    column_searchable_list = [Student.phone_number]
    page_size_options = [100, 250, 500]
    page_size = 100


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.email, User.full_name]
    form_columns = [User.username, User.email, User.full_name]


class MyAuthBackend(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get('username')
        password = form.get('password')
        user = await get_user_by_username(username)
        if user and verify_password(password, user.password):
            request.session.update({'user_id': user.id})
            RedirectResponse(url='/admin', status_code=302)
            return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        return 'user_id' in request.session


def create_admin(app):
    admin = Admin(app, engine, authentication_backend=MyAuthBackend(secret_key=settings.SECRET_KEY))
    admin.add_view(LogAdmin)
    admin.add_view(NotificationAdmin)
    admin.add_view(StudentAdmin)
    admin.add_view(UserAdmin)
    return admin
