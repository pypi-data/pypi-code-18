import json

import jwt
from bson import ObjectId

from quark_utilities import temporal_helpers
from quark_utilities.json_helpers import bson_to_json


class ObjectMother(object):

    WAYNE_ENTERPRISE = {
            "_id": "wayne",
            "name": "Wayne Enterprise",
            "sys": {
                "created_at": temporal_helpers.utc_now(),
                "created_by": "bruce.wayne",
                "cid": 1
            }
        }

    WAYNE_ENTERPRISE_SUBSCRIPTONS = [
        {
            "_id": ObjectId(),
            "product": "CMS",
            "membership_id": "wayne",
            "status": "ACTIVE",
            "api_permission_prefix": "cms",
            "sys": {
                "created_by": "bruce.wayne",
                "created_at": temporal_helpers.utc_now()
            }
        },
        {
            "_id": ObjectId(),
            "product": "QAP",
            "membership_id": "wayne",
            "status": "ACTIVE",
            "api_permission_prefix": "qap",
            "sys": {
                "created_by": "bruce.wayne",
                "created_at": temporal_helpers.utc_now()
            }
        }
    ]

    BRUCE_WAYNE = {
        "_id": "bruce.wayne",
        "password": "$2b$12$S4P.FaEeFcg.a8fFTSHowe0iWo3ZI5NDISdDgb6xTzktsnAfcvY9K",
        "membership_id": "wayne",
        "permissions": [
            "cms.*",
            "qap.*"
        ],
        "sys": {
            "created_by": "bruce.wayne",
            "created_at": temporal_helpers.utc_now(),
            "cid": 1
        }
    }

    ALFRED = {
        "_id": "alfred",
        "password": "$2b$12$S4P.FaEeFcg.a8fFTSHowe0iWo3ZI5NDISdDgb6xTzktsnAfcvY9K",
        "membership_id": "wayne",
        "permissions": [
            "cms.*",
            "qap.*"
        ],
        "sys": {
            "created_by": "bruce.wayne",
            "created_at": temporal_helpers.utc_now(),
            "cid": 2
        }
    }

    CIVIL = {
        "_id": "civil",
        "password": "$2b$12$S4P.FaEeFcg.a8fFTSHowe0iWo3ZI5NDISdDgb6xTzktsnAfcvY9K",
        "membership_id": "wayne",
        "permissions": [
        ],
        "sys": {
            "created_by": "bruce.wayne",
            "created_at": temporal_helpers.utc_now(),
            "cid": 3
        }
    }

    GOTHAM_NEWS = {
        "_id": ObjectId(),
        "name": "Gotham News",
        "membership_id": "wayne",
        "sys": {
            "created_by": "bruce.wayne",
            "created_at": temporal_helpers.utc_now(),
            "cid": 1
        }
    }

    VILLIANS_PERMISSON_GROUP = {
        "_id": ObjectId(),
        "name": "Gotham City Villians",
        "membership_id": "wayne",
        "permissions": [
            "qap.*"
        ],
        "sys": {
            "created_by": "bruce.wayne",
            "created_at": temporal_helpers.utc_now(),
            "cid": 1
        }
    }

    GOTHAM_NEWS_MASTER_TEMPLATE = {
        "_id": ObjectId(),
        "name": "Gotham News Master Page Template",
        "membership_id": "wayne",
        "domain_id": str(GOTHAM_NEWS["_id"]),
        "sys": {
            "created_by": "bruce.wayne",
            "created_at": temporal_helpers.utc_now(),
            "cid": 1
        }
    }

    GOTHAM_NEWS_FORM_COMPONENT = {
        "_id": ObjectId(),
        "name": "Gotham News Article Component",
        "type": "Article",
        "field_id": "test",
        "membership_id": "wayne",
        "domain_id": str(GOTHAM_NEWS["_id"]),
        "sys": {
            "created_by": "bruce.wayne",
            "created_at": temporal_helpers.utc_now(),
            "cid": 1
        }
    }

    GOTHAM_NEWS_CONTENT_TYPE = {
        "_id": ObjectId(),
        "name": "Gotham News Article Component",
        "type": "Article",
        "base_type": "test",
        "membership_id": "wayne",
        "domain_id": str(GOTHAM_NEWS["_id"]),
        "sys": {
            "created_by": "bruce.wayne",
            "created_at": temporal_helpers.utc_now(),
            "cid": 1
        }
    }

    def __init__(self, mongo_client):
        self._mongo_client = mongo_client

    def create_membership(self):
        self._mongo_client.quark_test.memberships.save(self.WAYNE_ENTERPRISE)

        self._mongo_client.quark_test.users.insert(self.BRUCE_WAYNE)

        for sub in self.WAYNE_ENTERPRISE_SUBSCRIPTONS:
            self._mongo_client.quark_test.subscriptions.save(sub)

        return (self.WAYNE_ENTERPRISE, self.BRUCE_WAYNE, self.WAYNE_ENTERPRISE_SUBSCRIPTONS)

    def create_bruce_wayne_token(self, secret):
        payload = {
            "prn": self.BRUCE_WAYNE["_id"],
            "membership_id": self.BRUCE_WAYNE["membership_id"],
            "permissions": self.BRUCE_WAYNE["permissions"],
            "domains":[],
            'exp': 99999999999,
            'jti': str(ObjectId()),
            'iat': temporal_helpers.to_timestamp(temporal_helpers.utc_now())
        }

        payload = json.loads(json.dumps(payload, default=bson_to_json))

        return jwt.encode(payload, secret).decode("utf-8")

    def create_user_civil(self):
        self._mongo_client.quark_test.users.save(self.CIVIL)
        return self.CIVIL

    def create_civil_token(self, secret):
        payload = {
            "prn": self.CIVIL["_id"],
            "membership_id": self.CIVIL["membership_id"],
            "permissions": self.CIVIL["permissions"],
            "domains": [],
            'exp': 99999999999,
            'jti': str(ObjectId()),
            'iat': temporal_helpers.to_timestamp(temporal_helpers.utc_now())
        }

        payload = json.loads(json.dumps(payload, default=bson_to_json))

        return jwt.encode(payload, secret).decode("utf-8")

    def create_user_alfred(self):
        self._mongo_client.quark_test.users.save(self.ALFRED)
        return self.ALFRED

    def create_domain_gotham_news(self):
        self._mongo_client.quark_test.domains.save(self.GOTHAM_NEWS)
        return self.GOTHAM_NEWS

    def create_template_for_gotham_news(self):
        self._mongo_client.quark_test.templates.save(self.GOTHAM_NEWS_MASTER_TEMPLATE)
        return self.GOTHAM_NEWS_MASTER_TEMPLATE

    def create_form_component_for_gotham_news(self):
        self._mongo_client.quark_test.form_components.save(self.GOTHAM_NEWS_FORM_COMPONENT)
        return self.GOTHAM_NEWS_FORM_COMPONENT

    def create_content_type_for_gotham_news(self):
        self._mongo_client.quark_test.content_types.save(self.GOTHAM_NEWS_CONTENT_TYPE)
        return self.GOTHAM_NEWS_CONTENT_TYPE

    def create_permission_group(self):
        self._mongo_client.quark_test.permission_groups.save(
            self.VILLIANS_PERMISSON_GROUP)
        return self.VILLIANS_PERMISSON_GROUP

    def drop(self):
        self._mongo_client.drop_database("quark_test")
