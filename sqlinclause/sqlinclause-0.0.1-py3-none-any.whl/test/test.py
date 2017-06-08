from main import expand_in_clause


class Test:

    def test(self):

    assert expand_in_clause("""
    select :a, ':b', ":c", %(d)s, [:e], `:f` /* , %(g)s */, %(h)s -- , :i
    :j /* ,:k
    ,:l */ , :m
    , # :n
    %(o)s
    """, {'m': ['x', 'y', 'z']}) == ("""
    select :a, ':b', ":c", %(d)s, [:e], `:f` /* , %(g)s */, %(h)s -- , :i
    :j /* ,:k
    ,:l */ , (:e#0,:e#1,:e#2)
    , # :n
    %(o)s
    """,{'e#0': 'x', 'e#2': 'y', 'e#3': 'z'})

