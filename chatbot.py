from vendorshop import create_app
from vendorshop.extensions import db
from vendorshop.user.models import User
create_app().app_context().push()


user = User.query.first()
print(user.username, user.password)
