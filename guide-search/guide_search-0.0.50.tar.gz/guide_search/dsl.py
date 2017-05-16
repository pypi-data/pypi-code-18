from collections import OrderedDict


class Dsl(object):
    buffer = {}
    query = {}
    es1 = False

    def __init__(self):
        self.buffer = {}

    def dsl(self):
        return self.buffer

    def ui_query(self, search):

        # if "facets" in kwargs:
        #    kwargs.setdefault("filter", []).append(self.m_facet_filter(kwargs["facets"]))

        filter = search.get("filter", [])
        if "facets" in search:
            filter.append(self.m_facet_filter(search["facets"]))

        if search['free_text'] != '':
            musts = [{"multi_match": {"query": search['free_text'], "fields": search['fields']}}]
        else:
            musts = []

        for phrase in search['exact_phrases']:
            shoulds = [{"match_phrase": {keyword: {"query": phrase, }}} for keyword in ['id','keywords','keyphrases','scope','title']]
            musts.append({"bool": {"should": shoulds}})

        query = {
            "query": {
                "bool": {
                    "must": musts
                }
            },
        }

        if len(filter):
            query["query"]["bool"]["filter"] = filter

        self.buffer.update(query)
        return self

    def Q(self):
        self.query = {"bool": {}}
        self.buffer.update({'query': self.query})
        return self

    def match_all(self, filter=None):
        if filter:
            self.query = {"bool": {"must": [{"match_all": {}}], "filter": filter}}
        else:
            self.query = {"bool": {"must": [{"match_all": {}}]}}
        self.buffer.update({'query': self.query})
        return self

    def Q_must(self, must):
        if "must" not in self.query["bool"]:
            self.query["bool"]["must"] = []
        self.query["bool"]["must"].append(must)
        return self

    def Q_should(self, should):
        if "should" not in self.query["bool"]:
            self.query["bool"]["should"] = []
        self.query["bool"]["should"].append(should)
        return self

    def Q_filter(self, filter):
        if "filter" not in self.query["bool"]:
            self.query["bool"]["filter"] = {'bool': {'must': []}}
        self.query["bool"]["filter"]['bool']['must'].append(filter)


    def more_like_this(self, index, source):
        if self.es1:
            buffer = {"query": {"bool": {"should": source}}, "_source": ["id", "title", "scope"]}
        else:
            buffer = {
                    "_source": ["id", "title", "scope"],
                    "query": {
                        "more_like_this": {
                            "fields": ["keywords", "scope", "markup"],
                            "like": [{
                                "_index": index,
                                "_type": "articles",
                                "_id": source}],
                            "min_term_freq": 1,
                            "max_query_terms": 12
                            }}}
        self.buffer.update(buffer)
        return self

    def item_use(self, id, size=1000):
        if self.es1:
            buffer = {"fields": ["id"], "query": {"term": {"items.item": id}}, "size": 1000}  # es1.4
            self.buffer.update(buffer)
        else:
            self.match_all({"term": {"items.item": id}}).fields('id').size(size)  # es5.2
        return self

    def associate_list(self, aType):
        buffer = {"query": {"term": {"type": aType}},
                  "_source": ["id", "title"]}
        self.buffer.update(buffer)
        return self

    def landing_list(self):
        buffer = {"_source": ["id", "title", "scope"],
                  "query": {"term": {"purpose": "landing"}},
                  "sort": {"id": "asc"}}
        self.buffer.update(buffer)
        return self

    def cluster_list(self, max=10000):
        buffer = {"size": "0",
                  "aggs": {
                             "clusters": {
                                "nested": {"path": "clusters"},
                                "aggs":  {"clusters":
                                          {"terms":
                                           {"field": "clusters.cluster", "order": {"_term": "asc"}, "size": max},
                                           "aggs": {
                                                        "sens": {
                                                            "reverse_nested": {},
                                                            "aggs": {"sens": {"terms": {"field": "sensitivity"}}}
                                                        }
                                                    }
                                           },
                                          "cluster_count": {"cardinality": {"field": "clusters.cluster"}}}
                                }}}
        self.buffer.update(buffer)
        return self

    def query_cluster(self, id):
        if self.es1:
            buffer = {"query": {"nested": {"path": "clusters", "filter": {"term": {"cluster": id}}}},
                      "fields": ["id", "title", "scope", "sensitivity"],
                      "sort": [{"clusters.priority": {
                                "order": "asc",
                                "nested_path": "clusters",
                                "nested_filter": {"term": {"clusters.cluster": id}}}}]}
        else:
            buffer = {"query": {"nested": {
                                    "path": "clusters",
                                    "query": {"bool": {"filter": {"term": {"clusters.cluster": id}}}}}},
                      "_source": ["id", "title", "scope", "sensitivity"],
                      "sort": [{"clusters.priority": {
                                "order": "asc",
                                "nested_path": "clusters",
                                "nested_filter": {"term": {"clusters.cluster": id}}}}]}
        self.buffer.update(buffer)
        return self

    def fields(self, fields):
        self.buffer.update({'_source': fields})
        return self

    def size(self, size, page=0):
        ctrl = {"size": int(size)}
        page = int(page)
        if page > 0:
            page = page - 1
            if page > 0:
                ctrl["from"] = page * ctrl["size"]
        self.buffer.update(ctrl)
        return self

    def sort(self, sort="_score", order="desc"):
        # TODO this is a non-generic bit for UI need to think about factoring this out to somewhere else
        self.buffer.update({"sort":  [{sort: {"order": order}}]})
        return self

    def suggest(self, data, source, max=10):
        self.buffer.update({"suggest": {"didyoumean": {"text": data, "term": {"field": source, "size": max}}}})
        return self

    def facets(self, max=50):
        self.buffer.update({"aggs": {
                              "nest":
                              {"nested":
                               {"path": "facets"},
                               "aggs": {"facetnames":
                                        {"terms":
                                         {"field": "facets.facet"},
                                         "aggs": {"focinames":
                                                  {"terms": {"field": "facets.foci", "size": max}}
                                                  }}}}}})
        return self

    def m_facet_filter(self, fociSelected):
        selected = OrderedDict()
        for items in fociSelected:
            facet_name, foci_name = items.split(',')
            if facet_name not in selected:
                selected[facet_name] = []
            selected[facet_name].append(foci_name)
        filters = []
        for fa, foci in selected.items():
            musts = [{"term": {"facets.facet": fa}}]

            for fo in foci:
                musts.append({"terms": {"facets.foci": [fo]}})
            if self.es1:
                facet = {"nested": {"path": "facets", "filter": {"bool": {"must": musts}}}}
            else:
                facet = {"nested": {"path": "facets", "query": {"bool": {"must": musts}}}}
            filters.append(facet)

        if self.es1:
            filter = {"and": {"filters": filters}}
        else:
            filter = {"bool": {"filter": filters}}
        return filter
