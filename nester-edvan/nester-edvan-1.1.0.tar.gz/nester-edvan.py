""" Este é o modulo "nester.py", e fornece uma função chamada print_lol() que imprime listas
que podem ou não incluir listas aninnhadas."""

def print_lol(the_list, level):
    """Esta função requer um argumento posicional chamada "the_list", que é qualquer
lista Python (de possíveis listas aninhadas). Cada item de dados na lista
fornecida é (recursivamente) impresso na telaem sua própria linha."""
    
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, level+1)

        else:
            for tab_stop in range(level):
                print("\t", end="")
            print(each_item)

movies = [
    "The Holy Grail", 1975, "Terry Jones & Terry Gilliam", 91,
        ["Graham Chapman",
             ["Michel Palin", "John Clesse", "Terry Gilliam", "Eric Idle", "Terry Jones"]]]

print_lol(movies,0)
