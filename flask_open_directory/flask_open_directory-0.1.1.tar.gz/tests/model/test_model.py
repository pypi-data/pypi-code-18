from flask_open_directory.model import BaseModel, User, Group, Attribute, \
    ModelABC


def test_BaseModel():
    assert issubclass(BaseModel, ModelABC)


def test_Attribute_repr():

    a = Attribute('a')
    assert repr(a) == "Attribute('a', allow_multiple=False)"

    b = Attribute('b', allow_multiple=True)
    assert repr(b) == "Attribute('b', allow_multiple=True)"


def test_Attribute_str():
    a = Attribute('a')
    assert str(a) == 'a'


def test_User():

    data = {
        'id': '123',
        'username': 'test',
        'email': ['test@example.com'],
        'full_name': "Test User"
    }

    u = User(**data)
    u_repr = repr(u)
    assert "id='123'" in u_repr
    assert "username='test'" in u_repr
    assert "mail=['test@example.com']" in u_repr
    assert "full_name='Test User'" in u_repr

    for k, v in data.items():
        assert getattr(u, k) == v

    u2 = User()
    for k in data:
        assert getattr(u2, k) is None

    # set attributes from ldap entry keys.
    data2 = {
        'apple-generateduid': '123',
        'uid': 'test',
        'mail': ['test@example.com'],
        'cn': 'Test User'
    }
    u = User(**data2)
    assert u.id == '123'
    assert u.username == 'test'
    assert u.email == ['test@example.com']
    assert u.full_name == 'Test User'

    # getattr works with ldap entry keys too.
    assert getattr(u, 'apple-generateduid') == u.id


def test_User_attributes():
    assert len(list(User._attributes())) == 4
    for a in User._attributes():
        assert isinstance(a, Attribute)

    assert User.query_cn() == 'users'


def test_User_attribute_for_key():
    assert User.attribute_for_key('id') == User.id
    assert User.attribute_for_key('uid') == User.username


def test_User_get_ldap_value():
    u = User(id=['123', '456'])
    assert u.ldap_values['id'] == ['123', '456']
    assert u._get_ldap_value('id') == '123'


def test_Group():
    data = {
        'id': '123',
        'group_name': 'test',
        'full_name': 'Test Group',
        'users': ['test1', 'test2'],
        'member_ids': ['123', '456']
    }
    g = Group(**data)

    for k, v in data.items():
        assert getattr(g, k) == v

    assert Group.query_cn() == 'groups'


def test_Group_has_user(username, user_id):

    group = Group(
        users=[username],
        member_ids=[user_id]
    )

    assert group.has_user(username)
    assert group.has_user(user_id)
