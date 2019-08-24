from schemas import ma
from models.user import UserModel


class UserSchema(ma.ModelSchema):
    # blog = ma.Nested(BlogSchema, many=True)

    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id", "created_at", "modified_at")
        include_fk = True
