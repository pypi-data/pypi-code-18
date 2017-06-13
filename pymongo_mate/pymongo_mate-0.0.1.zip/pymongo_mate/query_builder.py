#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module helps user to build pymongo query dict.
"""

import re


class Comparison(object):

    @staticmethod
    def less_than_equal(value):
        return {"$lte": value}

    @staticmethod
    def less_than(value):
        return {"$lt": value}

    @staticmethod
    def greater_than_equal(value):
        return {"$gte": value}

    @staticmethod
    def greater_than(value):
        return {"$gt": value}

    @staticmethod
    def euqal_to(value):
        return {"$eq": value}

    @staticmethod
    def not_equal_to(value):
        return {"$ne": value}


class Lang(object):
    English = "en"
    French = "fr"
    German = "de"
    Italian = "it"
    Portuguese = "pt"
    Russian = "ru"
    Spanish = "es"
    SimplifiedChineses = "zhs"
    TraditionalChineses = "zht"


class Text(object):

    @staticmethod
    def startswith(text, ignore_case=True):
        """Test if a string-field start with ``text``.
        """
        if ignore_case:
            compiled = re.compile(
                "^%s" % text.replace("\\", "\\\\"), re.IGNORECASE)
        else:
            compiled = re.compile("^%s" % text.replace("\\", "\\\\"))

        return {"$regex": compiled}

    @staticmethod
    def endswith(text, ignore_case=True):
        """Test if a string-field end with ``text``.
        """
        if ignore_case:
            compiled = re.compile(
                "%s$" % text.replace("\\", "\\\\"), re.IGNORECASE)
        else:
            compiled = re.compile("%s$" % text.replace("\\", "\\\\"))

        return {"$regex": compiled}

    @staticmethod
    def contains(text, ignore_case=True):
        """Test if a string-field has substring of ``text``.
        """
        if ignore_case:
            compiled = re.compile(
                "%s" % text.replace("\\", "\\\\"), re.IGNORECASE)
        else:
            compiled = re.compile("%s" % text.replace("\\", "\\\\"))

        return {"$regex": compiled}

    @staticmethod
    def fulltext(search, lang=Lang.English, ignore_case=True):
        """Full text search.

        .. note::

            This field doesn't need to specify field.
        """
        return {
            "$text": {
                "$search": search,
                "$language": lang,
                "$caseSensitive": not ignore_case,
                "$diacriticSensitive": False,
            }
        }


class Array(object):

    @staticmethod
    def element_match(filters):
        """Test if any of items match the criterion.

        Example::

            data = [
                {"_id": 1, "results": [ 82, 85, 88 ]},
                {"_id": 2, "results": [ 75, 88, 89 ]},
            ]

            filters = {"results": {"$elemMatch": {"$gte": 80, "$lt": 85 }}}
        """
        return {"$elemMatch": filters}

    @staticmethod
    def include_all(items):
        """Test if an array-like field include all these items.

        Example::

            {"tag": ["a", "b", "c"]} include all ["a", "c"]
        """
        return {"$all": items}

    @staticmethod
    def include_any(items):
        """Test if an array-like field include any of these items.

        Example::

            {"tag": ["a", "b", "c"]} include any of ["c", "d"]
        """
        return {"$in": items}

    @staticmethod
    def exclude_all(items):
        """Test if an array-like field doesn't include any of these items.

        Example::

            {"tag": ["a", "b", "c"]} doesn't include any of ["d", "e"]
        """
        return {"$nin": items}

    @staticmethod
    def exclude_any(items):
        """Test if an array-like field doesn't include at lease one of 
        these items.

        Example::

            {"tag": ["a", "b", "c"]} doesn't include "d" from ["c", "d"]
        """
        return {"$not": {"$all": items}}

    @staticmethod
    def item_in(items):
        """Single item is in item sets.

        Example::

            {"item_type": "Fruit"}, "Fruit" in ["Fruit", "Meat"]
        """
        return {"$in": items}

    @staticmethod
    def item_not_in(items):
        """Single item is not in item sets.

        Example::

            {"item_type": "Seafood"}, "Fruit" not in ["Fruit", "Meat"]
        """
        return {"$nin": items}

    @staticmethod
    def size(n):
        """Test if size of an array-like field is n.
        """
        return {"$size": n}


class Geo2DSphere(object):

    @staticmethod
    def near(lat, lng, max_dist=None, unit_miles=False):
        """
        """
        filters = {
            "$nearSphere": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [lng, lat],
                }
            }
        }
        if max_dist:
            if unit_miles:
                max_dist = max_dist / 1609.344
            filters["$nearSphere"]["$maxDistance"] = max_dist
        return filters


if __name__ == "__main__":
    import pymongo
    from pymongo_mate.tests import col

    data = [
        {
            "_id": 1,
            "score": 10,
            "value": 3.14,
            "array": [3, 4, 5],
            "path": r"C:\Users\admin",
            "description": "$text performs a text search on the content of the fields indexed with a text index.",
            "loc": {"type": "Point", "coordinates": [-77.142901, 39.074373]},
        },
    ]
    try:
        col.insert(data)
    except:
        pass

    col.create_index([("loc", pymongo.GEOSPHERE)])
    col.create_index([("description", pymongo.TEXT)])

    def _test(field, filters):
        assert len(list(col.find({field: filters}))) == 1

    def test_operator():
        _test("value", Comparison.euqal_to(3.14))
        _test("value", Comparison.not_equal_to(1.414))
        _test("value", Comparison.greater_than(3))
        _test("value", Comparison.greater_than_equal(3.14))
        _test("value", Comparison.less_than(4))
        _test("value", Comparison.less_than_equal(3.14))

    test_operator()

    def test_text():
        _test("path", Text.startswith("C:\\"))
        _test("path", Text.endswith("admin"))
        _test("path", Text.contains(r":\user"))
        assert len(list(col.find(Text.fulltext("text index")))) == 1

    test_text()

    def test_array():
        _test("score", Array.item_in([10, 11]))
        _test("score", Array.item_not_in([8, 9]))

        _test("array", Array.include_all([3, 5]))
        _test("array", Array.include_any([1, 5, 9]))
        _test("array", Array.exclude_all([1, 2]))
        _test("array", Array.exclude_any([1, 2, 3]))

    test_array()

    def test_geo2dsphere():
        _test("loc",
              Geo2DSphere.near(39.08, -77.14, max_dist=100000, unit_miles=False))

    test_geo2dsphere()
