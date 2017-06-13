#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
pymongo query convenence method.
"""


def select_all(col):
    """Select all document from collection.
    """
    return list(col.find())


def select_field(col, *fields, filters=None):
    """Select single or multiple fields.

    :params fields: list of str
    :returns headers: headers
    :return data: list of row

    **中文文档**

    - 在选择单列时, 返回的是 str, list
    - 在选择多列时, 返回的是 str list, list of list

    返回单列或多列的数据。
    """
    if filters is None:
        filters = dict()

    wanted = {field: True for field in fields}

    if len(fields) == 1:
        header = fields[0]
        data = [doc.get(header) for doc in col.find(filters, wanted)]
        return header, data
    else:
        headers = list(fields)
        data = [[doc.get(header) for header in headers]
                for doc in col.find(filters, wanted)]
        return headers, data


def select_distinct_field(col, *fields, filters=None):
    """Select distinct value or combination of values of 
    single or multiple fields.

    :params fields: list of str
    :return data: list of list

    **中文文档**

    选择多列中出现过的所有可能的排列组合。
    """
    if filters is None:
        filters = dict()

    if len(fields) == 1:
        key = fields[0]
        data = list(col.find(filters).distinct(key))
        return data
    else:
        pipeline = [
            {
                "$match": filters
            },
            {
                "$group": {
                    "_id": {key: "$" + key for key in fields},
                },
            },
        ]
        data = list()
        for doc in col.aggregate(pipeline):
            # doc = {"_id": {"a": 0, "b": 0}} ...
            data.append([doc["_id"][key] for key in fields])
        return data


def random_sample(col, n=5, filters=None):
    """Randomly select n document from query result set. If no query specified,
    then from entire collection.

    **中文文档**

    从collection中随机选择 ``n`` 个样本。
    """
    pipeline = list()
    if filters is not None:
        pipeline.append({"$match": filters})
    pipeline.append({"$sample": {"size": n}})
    return list(col.aggregate(pipeline))


if __name__ == "__main__":
    import random
    from pymongo_mate.tests import col

    def insert_4_data():
        col.remove({})
        data = [
            {"_id": 0, "v": 0},
            {"_id": 1, "v": 1},
            {"_id": 2, "v": 2},
            {"_id": 3, "v": 3},
        ]
        col.insert(data)

    def insert_1000_a_b_c_data():
        col.remove({})

        data = list()
        _id = 0
        for a in range(10):
            for b in range(10):
                for c in range(10):
                    _id += 1
                    data.append({"_id": _id, "a": a, "b": b, "c": c})
        col.insert(data)

    def test_selelct_field():
        insert_4_data()

        header, data = select_field(col, "_id")
        assert header == "_id"
        assert data == [0, 1, 2, 3]

        headers, data = select_field(
            col, "_id", "v", filters={"_id": {"$gte": 2}})
        assert headers == ["_id", "v"]
        assert data == [[2, 2], [3, 3]]

    test_selelct_field()

    def test_select_distinct():
        insert_1000_a_b_c_data()

        assert select_distinct_field(col, "a") == list(range(10))
        assert len((select_distinct_field(col, "a", "b"))) == 100
        assert len((select_distinct_field(col, "a", "b", "c"))) == 1000

        assert select_distinct_field(
            col, "a", filters={"a": {"$gte": 5}}) == list(range(5, 10))
        assert len(
            (select_distinct_field(col, "a", "b", filters={"a": {"$gte": 5}}))) == 50
        assert len(
            (select_distinct_field(col, "a", "b", "c", filters={"a": {"$gte": 5}}))) == 500

    test_select_distinct()

    def test_random_sample():
        insert_1000_a_b_c_data()

        assert len(random_sample(col, n=5)) == 5

        result = random_sample(col, n=5, filters={"_id": {"$gte": 500}})
        assert len(result) == 5
        for doc in result:
            assert doc["_id"] >= 500

    test_random_sample()
