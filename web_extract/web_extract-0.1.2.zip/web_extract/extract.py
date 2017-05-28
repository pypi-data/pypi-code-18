# coding: utf-8
from urlparse import urljoin
from functools import partial
from scrapy.selector import SelectorList, Selector
from dangerous_eval import DangerousEval
import parser
import json


functions = {
    'html': lambda payload: Selector(text=payload.data),
    'xpath': lambda payload, path: payload.data.xpath(path),
    'css': lambda payload, expr:  payload.data.css(expr),
    'text': lambda payload, el: el.extract(),
    'first': lambda payload, data: data[0] if data else None,
    'last': lambda payload, data: data[-1] if data else None,
    'url': lambda payload, url: urljoin(payload.url, url),
    'str': lambda payload, data: data.extract(),
    'extract': lambda payload, data: data.extract(),
    'extract_first': lambda payload, data: data.extract_first(),
    'upper': lambda payload, data: functions['extract_first'](payload, data).upper(),
    'lower': lambda payload, data: functions['extract_first'](payload, data).lower(),
    'json': lambda payload: json.loads(payload.data),
}


class Payload(object):
    __slots__ = ('url', 'data')
    def __init__(self, url, data):
        self.url = url
        self.data = data


class WebExtract(object):
    def __init__(self, script):
        self._script = parser.parse(script)

    def extract(self, source, url=None):
        payload = Payload(url, source)
        cut_data = dict()
        _ = WebExtract._extract_nodes(self._script, payload, cut_data)
        return cut_data

    @staticmethod
    def _extract_node(node, payload, yield_store):
        s_eval = DangerousEval(env=WebExtract._make_env(payload)).eval

        if node.children:
            eval_result = s_eval(node.expr)
            if isinstance(eval_result, list):
                result = [WebExtract._extract_nodes(node.children, Payload(payload.url, item), yield_store) for item in eval_result]
            else:
                result = WebExtract._extract_nodes(node.children, Payload(payload.url, eval_result), yield_store)
        else:
            result = s_eval(node.expr)
            if not node.children and isinstance(result, (Selector, SelectorList)):
                result = result.extract()

        o_group = node.output
        o_name = node.name
        if o_group:
            if o_group not in yield_store:
                yield_store[o_group] = dict()

            if o_name not in yield_store[o_group]:
                yield_store[o_group][o_name] = result
            else:
                if isinstance(result, list):
                    yield_store[o_group][o_name].extend(result)
                else:
                    yield_store[o_group][o_name] = [yield_store[o_group][o_name], result]

        return result

    @staticmethod
    def _extract_nodes(nodes, payload, yield_store):
        return {c.name: WebExtract._extract_node(c, payload, yield_store) for c in nodes}

    @staticmethod
    def _make_env(payload):
        result = dict()
        for key, method in functions.items():
            result[key] = partial(method, payload)
        return result
