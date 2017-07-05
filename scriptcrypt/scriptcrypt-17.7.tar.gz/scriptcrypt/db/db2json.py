import scriptcrypt.db as db
import scriptcrypt.jsonhandlers as setts
import json


def run(path2write):
    mset = setts.Settigns()
    settings = mset.readData()
    mydb = db.dbHandler("sqlite:///" + settings["db"])
    dump = [mydb.entryInfo(name) for name in mydb.entryNames()]
    with open(path2write, "w") as f:
        f.write(json.dumps(dump,
                           sort_keys=True,
                           indent=4,
                           separators=(',', ': ')))
