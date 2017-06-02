from app import Gargantua

gargantua = Gargantua()

host = "127.0.0.1"
user = "root"
password = "gargantua"
db = "SSDB"

gargantua.set_db(host=host,
                 user=user,
                 password=password,
                 db=db)

gargantua.set_type("SELECT")
gargantua.set_table('Categories')
gargantua.set_select_values(['CategoryName', 'CategoryId'])
gargantua.set_select_where_values("CategoryId != 0")

query = gargantua.query_builder()
print(query)  # SELECT  CategoryName, CategoryId FROM Categories WHERE CategoryId != 0

gargantua.reset()

gargantua.set_type("INSERT")
gargantua.set_table("Categories")
gargantua.set_insert_values(["CategoryName", "CreatedAt"])
gargantua.set_insert_params(["C#", "17.07.2017"])

query = gargantua.query_builder()
print(query)  # INSERT INTO Categories( 'CategoryName', 'CategorySurname') VALUES ( 'C#', 'C# Surname')

gargantua.reset()

gargantua.set_type("UPDATE")
gargantua.set_table("Categories")
gargantua.set_update_values(["CategoryName", "CreatedAt"])
gargantua.set_update_params(["Java", "17.07.2017"])
gargantua.set_update_where_values("CategoryId != 0")

query = gargantua.query_builder()

print(query)  # UPDATE Categories SET CategoryName =Java , CategorySurname=Java Surname WHERE CategoryId != 0

gargantua.reset()

gargantua.set_type("DELETE")
gargantua.set_table("Categories")
gargantua.set_delete_where_values("CategoryId = 2")

query = gargantua.query_builder()

print(query)  # DELETE FROM Categories WHERE CategoryId = 2
