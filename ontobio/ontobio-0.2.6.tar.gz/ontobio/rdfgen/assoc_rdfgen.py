from prefixcommons.curie_util import contract_uri, expand_uri, get_prefixes
from ontobio.vocabulary.relations import OboRO, Evidence
from ontobio.vocabulary.upper import UpperLevel
from rdflib import Namespace
from rdflib import BNode
from rdflib import Literal
from rdflib import URIRef
from rdflib.namespace import RDF
from rdflib.namespace import RDFS
from rdflib.namespace import OWL
import rdflib
import logging

ro = OboRO()
evt = Evidence()
upt = UpperLevel()

class RdfGenerator():

    def __init__(self):
        self.graph = rdflib.Graph()
        self.include_subject_info = False

    def genid(self):
        return BNode()

    def blanknode(self):
        return BNode()
        
    def uri(self,id):
        # allow either atoms or objects
        if isinstance(id,dict):
            return self.uri(id['id'])
        logging.info("Expand: {}".format(id))
        return URIRef(expand_uri(id))
    
    def emit(self,s,p,o):
        self.graph.add((s,p,o))
        return (s,p,o)
    
    def emit_type(self,s,t):
        return self.emit(s,RDF.type,t)
    def emit_label(self,s,t):
        return self.emit(s,RDFS.label,o)
    
    def translate_evidence(self, association, stmt):
        """

        ``
        _:1 a Axiom
            subject s
            predicate p
            object o
            evidence [ a ECO ; ...]
        ``
        
        """
        ev = association['evidence']
        ev_id = None
        if 'id' in ev:
            ev_id = self.uri(ev['id'])
        else:
            ev_id = self.genid()

        stmt_id = self.blanknode() ## OWL reification: must be blank
        (s,p,o) = stmt
        self.emit_type(stmt_id, OWL.Axiom)
        
        self.emit(stmt_id, OWL.subject, s)        
        self.emit(stmt_id, OWL.predicate, p)        
        self.emit(stmt_id, OWL.object, o)
        
        self.emit(stmt_id, self.uri(evt.axiom_has_evidence), ev_id)
        self.emit_type(ev_id, self.uri(ev['type']))
        if 'with_support_from' in ev:
            pass # TODO
        for ref in ev['has_supporting_reference']:
            self.emit(ev_id, self.uri(evt.has_supporting_reference), self.uri(ref))
        if 'with_support_from' in ev:
            for ref in ev['with_support_from']:
                self.emit(ev_id, self.uri(evt.evidence_with_support_from), self.uri(ref))
        

class CamGenerator(RdfGenerator):
    """
    Granular instance-based representation (GO-CAM)
    """

    def translate(self, association):
        sub = association['subject']
        obj = association['subject']
        rel = association['relation']
        sub_uri = self.uri(sub)
        obj_uri = self.uri(obj)

        enabler_id = self.genid()
        self.emit_type(enabler_id, sub_uri)
        tgt_id = self.genid()
        self.emit_type(tgt_id, obj_uri)
        
        aspect = association['aspect']
        stmt = None
        if aspect == 'F':
            stmt = self.emit(tgt_id, ro.enabled_by, enabler_id)
        elif aspect == 'P':
            mf_id = self.genid()
            self.emit_type(tgt_id, upt.molecular_function)
            stmt = self.emit(tgt_id, ro.enabled_by, mf_id)
            stmt = self.emit(mf_id, ro.part_of, tgt_id)
        elif aspect == 'C':
            mf_id = self.genid()
            self.emit_type(tgt_id, upt.molecular_function)
            stmt = self.emit(tgt_id, ro.enabled_by, mf_id)
            stmt = self.emit(mf_id, ro.occurs_in, tgt_id)

        if self.include_subject_info:
            pass
            # TODO
        # TODO: extensions
        self.translate_evidence(association, stmt)
        
class SimpleAssocGenerator(RdfGenerator):
    """
    Follows simple OBAN-style model
    """

    def translate(self, association):
        sub = association['subject']
        obj = association['subject']
        rel = association['relation']
        sub_uri = self.uri(sub)
        obj_uri = self.uri(obj)
        rel_uri = self.uri(rel)

        # TODO: extensions
        stmt = self.emit(sub_uri,rel_uri,obj_uri)

        # optionally include info about subject (e.g. gene)
        if self.include_subject_info:
            self.emit_label(sub_uri, sub)
            if 'taxon' in sub:
                taxon = sub['taxon']
                self.emit(sub_uri, ro.in_taxon, self.uri(taxon))
            # TODO syns etc

        self.translate_evidence(association, stmt)
        
