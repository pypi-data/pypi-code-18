""" Este é o modulo "nester.py", e fornece uma função chamada print_lol() que imprime listas
que podem ou não incluir listas aninnhadas."""

def print_lol(the_list, indent=False, level=0):
    """Esta função requer um argumento posicional chamada "the_list", que é qualquer
lista Python (de possíveis listas aninhadas). Cada item de dados na lista
fornecida é (recursivamente) impresso na telaem sua própria linha."""
    
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level+1)

        else:
            if indent:
                for tab_stop in range(level):
                    print("\t", end="")
            print(each_item)
