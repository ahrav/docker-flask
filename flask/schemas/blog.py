from schemas import ma
from models.blog import BlogModel


class BlogSchema(ma.ModelSchema):
    class Meta:
        model = BlogModel
        load_only = ("owner",)
        dump_only = ("id", "created_at", "modified_at")
        include_fk = True
