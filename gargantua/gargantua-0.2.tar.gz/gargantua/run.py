from app import Gargantua
from transaction import TransactionType
import datetime

gargantua = Gargantua()

host = "127.0.0.1"
user = "root"
password = "gargantua"
db = "SSDB"

gargantua.set_db(host=host,
                 user=user,
                 password=password,
                 db=db)

gargantua.set_type(TransactionType.Select)
gargantua.set_table("Categories")
gargantua.set_select_values(["*"])