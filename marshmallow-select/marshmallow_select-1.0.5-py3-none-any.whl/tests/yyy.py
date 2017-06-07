import pytest


@pytest.fixture()
def all_detail_schemas(schemas):
    class ImageForUserDetailSchema(schemas.ImageSchema):
        class Meta:
            fields = ['id', 'url']

    class LikeForUserDetailSchema(schemas.LikeSchema):
        image = Nested(ImageForUserDetailSchema)

        class Meta:
            fields = ['id', 'image']

    class UserDetailSchema(schemas.UserSchema):
        images = List(Nested(ImageForUserDetailSchema))
        likes = List(Nested(LikeForUserDetailSchema))

        class Meta:
            exclude = ['default_image']

    class _detail_schemas(object):
        def __init__(self):
            self.ImageForUserDetailSchema = ImageForUserDetailSchema
            self.LikeForUserDetailSchema = LikeForUserDetailSchema
            self.UserDetailSchema = UserDetailSchema

    return _detail_schemas()


@pytest.fixture()
def das():
    pass


@pytest.fixture()
def detail_apispec_single():
    user_detail_spec = {
        "properties": {
            "email": {
                "maxLength": 100,
                "type": "string",
                "x-nullable": true
            },
            "first_name": {
                "maxLength": 100,
                "type": "string",
                "x-nullable": true
            },
            "id": {
                "format": "int32",
                "type": "integer"
            },
            "images": {
                "items": {
                    "properties": {
                        "id": {
                            "format": "int32",
                            "type": "integer"
                        },
                        "url": {
                            "maxLength": 100,
                            "type": "string",
                            "x-nullable": true
                        }
                    },
                    "type": "object"
                },
                "type": "array"
            },
            "last_name": {
                "maxLength": 100,
                "type": "string",
                "x-nullable": true
            },
            "likes": {
                "items": {
                    "properties": {
                        "id": {
                            "format": "int32",
                            "type": "integer"
                        },
                        "image": {
                            "properties": {
                                "id": {
                                    "format": "int32",
                                    "type": "integer"
                                },
                                "url": {
                                    "maxLength": 100,
                                    "type": "string",
                                    "x-nullable": true
                                }
                            },
                            "type": "object"
                        }
                    },
                    "type": "object"
                },
                "type": "array"
            }
        },
        "type": "object"
    }
    return user_detail_spec

@pytest.fixture()
def detail_apispec_all():
    pass


@pytest.fixture()
def detail_schema(all_detail_schemas):
    return all_detail_schemas.UserDetailSchema


class FakeTest:
    @pytest.mark.skip()
    def test_apispec(self, detail_schema):
        from apispec import APISpec
        spec = APISpec(
            title='Swagger Petstore',
            version='1.0.0',
            plugins=[
                'apispec.ext.marshmallow',
            ],
        )
        spec.definition('UserDetail', schema=detail_schema)
        swag = spec.to_dict()
        import pdb ; pdb.set_trace()


@pytest.mark.skip()
class TestApispec:
    def test_apispec(self, all_detail_schemas):
        from apispec import APISpec
        spec = APISpec(
            title='detail',
            version='0.0.0',
            plugins=[
                'apispec.ext.marshmallow',
            ],
        )
        spec.definition('UserDetail', schema=all_detail_schemas.UserDetailSchema)
        spec.definition('ImageForUserDetail', schema=all_detail_schemas.ImageForUserDetailSchema)
        spec.definition('LikeForUserDetail', schema=all_detail_schemas.LikeForUserDetailSchema)
        swag = spec.to_dict()
        import pdb ; pdb.set_trace()
