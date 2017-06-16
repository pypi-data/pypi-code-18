'''
Declares additional EXML schemas
'''
from pytree.exml import make_syntax_doc, \
    EnumAttribute, TextAttribute, RefAttribute, \
    Topic, EduRange, Edu, \
    Document, GenericMarkable, MarkableSchema

__all__ = ['DiscRel', 'DiscRelEdges',
           'make_konn_doc', 'make_implicit_doc']

rel_map = {
    'evaluative': 'antithesis',
    'epistemic_cause': 'evidence'
}


def get_rel(info, which):
    k = getattr(info, which, None)
    if k in rel_map:
        k = rel_map[k]
    if k == 'NULL':
        k = None
    return k


class DiscRel(GenericMarkable):

    def __init__(self, label, target, marking=None):
        self.label = label
        self.marking = marking
        self.target = target


class DiscRelEdges(object):

    def __init__(self, name):
        self.name = name
        self.attributes = [EnumAttribute('relation'),
                           EnumAttribute('marking'),
                           RefAttribute('arg2')]
        self.suffix = "Edge"

    def get_edges(self, obj, doc):
        edges = []
        if hasattr(obj, 'rels') and obj.rels is not None:
            for rel in obj.rels:
                edges.append((rel.label, rel.marking, rel.target))
        return edges

    def set_edges(self, obj, vals, doc):
        rels = []
        for lbl, mark, tgt in vals:
            rels.append(DiscRel(lbl, tgt, mark))
        obj.rels = rels

    def get_updown(self, obj, doc, result):
        pass


def make_konn_doc(want_implicit=True):
doc = make_syntax_doc(want_dc=True, want_deps=True,
                        want_wsd=True)
discrel_edge = DiscRelEdges('discRel')
topic_schema = MarkableSchema('topic', Topic)
topic_schema.attributes = [TextAttribute('description')]
topic_schema.locality = 'text'
topic_schema.edges = [discrel_edge]
edu_range_schema = MarkableSchema('edu-range', EduRange)
edu_range_schema.locality = 'text'
edu_range_schema.edges = [discrel_edge]
edu_schema = MarkableSchema('edu', Edu)
edu_schema.locality = 'sentence'
edu_schema.edges = [discrel_edge]
doc.add_schemas([edu_schema, topic_schema, edu_range_schema])
return doc


def make_implicit_doc():
    text_schema = MarkableSchema('text', Text)
    text_schema.attributes = [TextAttribute('origin')]
    s_schema = MarkableSchema('sentence', tree.Tree)
    s_schema.locality = 'text'
    discrel_edge = DiscRelEdges('discRel')
    topic_schema = MarkableSchema('topic', Topic)
    topic_schema.attributes = [TextAttribute('description')]
    topic_schema.locality = 'text'
    topic_schema.edges = [discrel_edge]
    edu_range_schema = MarkableSchema('edu-range', EduRange)
    edu_range_schema.locality = 'text'
    edu_range_schema.edges = [discrel_edge]
    edu_schema = MarkableSchema('edu', Edu)
    edu_schema.locality = 'sentence'
    edu_schema.edges = [discrel_edge]
    t_schema = TerminalSchema('word', tree.TerminalNode)
    t_schema.attributes = [TextAttribute('form', prop_name='word'),
                           EnumAttribute('pos', prop_name='cat'),
                           EnumAttribute('morph', prop_name='morph'),
                           EnumAttribute('lemma', prop_name='lemma'),
                           RefAttribute('dephead', prop_name='syn_parent'),
                           EnumAttribute('deprel', prop_name='syn_label')]
    return Document(t_schema, [text_schema, s_schema,
                               edu_schema, topic_schema, edu_range_schema])
