from qlib.data.sql import SqlObjectEngine, Table


class Doc(Table):
    title = 'title'
    url = str
    content = str
    tag = str

    
class InLink(Table):
    fromid = int
    toid= int
    strength = float


class OutLink(Table):
    fromid = int
    toid = int
    strength = float


class Hidden(Table):
    link_type = 'Doc'
    linkid = int
    desc = 'this is describle for hidden node . the hidden node can target to any obj. default is doc'

    def __init__(self, handler=None, **kargs):
        
        v = kargs['linkid']
        if hasattr(v, '_table'):
            kargs['linkid'] = v.id
            kargs['link_type'] = v.__class__.__name__
            kargs['desc'] = v.__class__.__name__
        super().__init__(handler=handler, **kargs)

    def __call__(self, sqlhandler, Obj ):
        return handler.find_one(Obj, ID=self.linkid)



class Neural:
    layer_map  =[InLink, Hidden, OutLink]
    def __init__(self, database):
        self._db = SqlObjectEngine(database=database)
        self.database_path = database
        if not ('InLink',) in self._db.sql.table_list():
            self._db.create(InLink)

        if not ('OutLink',) in self._db.sql.table_list():
            self._db.create(OutLink)

        if not ('Hidden',) in self._db.sql.table_list():
            self._db.create(Hidden)

    def __del__(self):
        self._db.close()

    def _get_from_db(self, table,**kargs):
        if hasattr(table, '_table'):
            return self._db.find_one(table, **kargs)
        else:
            return self._db.sql.first(table, **kargs)

    def getStrength(self, fromid, toid, layer):
        
        if isinstance(layer, int):
            l = self.__class__.layer_map[layer]
        elif hasattr(layer, '_table'):
            l = layer
        else:
            raise Exception("not such layer : ",layer)

        res = self._get_from_db(l, fromid=fromid, toid=toid)
        if not res:
            if l is InLink:
                return -0.2
            else:
                return 0.0
        return res.strength

    def getAllHiddenIds(self, inids, outids):
        res_ids = set()
        for inid in inids:
            rows = self._db.find(InLink, fromid=inid)
            for r in rows:
                res_ids.add(r.toid)

        for outid in outids:
            rows = self._db.find(OutLink, toid=outids)
            for r in rows:
                res_ids.add(r.fromid)

        return res_ids

    def setUpNetwork(self, inids, outids):
        self.inids = inids
        self.outids = outids
        self.hiddenids = self.getAllHiddenIds(inids, outids)

        # node
        self.ai = [1.0] * len(self.inids)
        self.ah = [1.0] * len(self.hiddenids)
        self.ao = [1.0] * len(self.outids)

        # create weights matrix
        self.wi = [[ self.getStrength(inid, hiddenid, 0) for  hiddenid in self.hiddenids] for inid in self.inids ]
        self.wo = [[ self.getStrength(hiddenid, outid, 2) for hiddenid in self.hiddenids] for outid in self.outids ]

    def feedforward(self, activation_func):
        # the only inputs are the query words
        for i in range(len(self.inids)):
            self.ai[i] = 1.0

        # hidden activations
        
        self.ah = activation_func(self.inids, self.hiddenids, self.ai, self.wi)
        self.ao = activation_func(self.hiddenids, self.outids, self.ah, self.ao)
        return self.ao


    def getresult(self, inids, outids):
        pass

    def setStrength(self, fromid, toid, layer, strength):
        
        res = self.getStrength(fromid,toid, layer)
        if not res:
            if isinstance(layer, int):
                l = self.__class__.layer_map[layer]
            elif hasattr(layer, '_table'):
                l = layer
            else:
                raise Exception("not such layer : ",layer)
            self._db.add(l(fromid=fromid, toid=toid, strength=strength))
        else:
            res['strength'] = strength
            self._db.save(res)

    def __repr__(self):
    	return '%d-layer-nerual| store in %s' % (len(self.layer_map), self.database_path)