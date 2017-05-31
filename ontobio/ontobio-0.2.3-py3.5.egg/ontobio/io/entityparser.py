from ontobio.io.gafparser import AssocParser, ENTITY

# TODO - use abstract parent for both entity and assoc
class EntityParser(AssocParser):
    pass
    
class GpiParser(EntityParser):
    def parse_line(self, line):            
        """Parses a single line of a GPI.

        Return a tuple `(processed_line, associations)`. Typically
        there will be a single association, but in some cases there
        may be none (invalid line) or multiple (disjunctive clause in
        annotation extensions)

        Note: most applications will only need to call this directly if they require fine-grained control of parsing. For most purposes,
        :method:`parse_file` can be used over the whole file

        Arguments
        ---------
        line : str
            A single tab-seperated line from a GPAD file

        """
        vals = line.split("\t")
        [db,
         db_object_id,
         db_object_symbol,
         db_object_name,
         db_object_synonym,
         db_object_type,
         taxon,
         parent_object_id,
         xrefs,
         properties] = vals

        ## --
        ## db + db_object_id. CARD=1
        ## --
        id = self._pair_to_id(db, db_object_id)
        if not self._validate_id(id, line, ENTITY):
            return line, []

        ## --
        ## db_object_synonym CARD=0..*
        ## --
        synonyms = db_object_synonym.split("|")
        if db_object_synonym == "":
            synonyms = []

        # TODO: DRY
        parents = parent_object_id.split("|")
        if parent_object_id == "":
            parents = []
            
        xref_ids = xrefs.split("|")
        if xrefs == "":
            xref_ids = []
        
        obj = {
            'id': id,
            'label': db_object_symbol,
            'fullname': db_object_name,
            'synonyms': synonyms,
            'type': db_object_type,
            'parents': parents,
            'xrefs': xref_ids,
            'taxon': {
                'id': self._taxon_id(taxon)
            }
        }
        return line, [obj]

class BgiParser(EntityParser):
    """
    TODO
    """
    def parse(self):
        pass
    
