from sqlinclause.main import expand_sql_in_clause, expand_sql


class Test:

    def test(self):

        statement, args = expand_sql_in_clause("""
        select :a, ':b', ":c", %(d)s, [:e], `:f` /* , %(g)s */, %(h)s -- , :i
        :j /* ,:k, IN :m
        ,:l */ , IN :m
        , IN (:m)
        , IN (1,2,%(n)s)
        %(o)s -- %(n)s
        :e_3
        """, {'m': ['x', 'y', 'z'],  # 括弧なしのIN句変数は括弧付きに展開
              'n': [3, 4],  # 括弧内のIN句変数は単にカンマ区切りで展開
              'b': [1, 2, 3]  # IN句でない変数は展開の対象外
              })
        assert statement, """
        select :a, ':b', ":c", %(d)s, [:e], `:f` /* , %(g)s */, %(h)s -- , :i
        :j /* ,:k, IN :m
        ,:l */ , IN (:e_1,:e_2,:e_4)
        , IN (:e_1,:e_2,:e_4)
        , IN (1,2,%(e_5)s,%(e_6)s)
        %(o)s -- %(n)s
        :e_3
        """
        assert args == {'e_1': 'x',
                        'e_2': 'y',
                        'e_4': 'z',  # 既存の e_3 という名前はスキップされた
                        'e_5': 3,
                        'e_6': 4,
                        'b': [1, 2, 3]}

        m = ['x', 'y', 'z']
        statement, args = expand_sql("""
        select :a, ':b', ":c", %(d)s, [:e], `:f` /* , %(g)s */, %(h)s -- , :i
        :j /* ,:k, IN :m
        ,:l */ , IN :m
        , IN (:m)
        , IN (1,2,%(n)s)
        %(o)s -- %(n)s
        :e_3
        """, {'n': [3, 4],
              'b': [1, 2, 3]
              })
        assert statement, """
        select :a, ':b', ":c", %(d)s, [:e], `:f` /* , %(g)s */, %(h)s -- , :i
        :j /* ,:k, IN :m
        ,:l */ , IN (:e_1,:e_2,:e_4)
        , IN (:e_1,:e_2,:e_4)
        , IN (1,2,%(e_5)s,%(e_6)s)
        %(o)s -- %(n)s
        :e_3
        """
        assert args == {'e_1': 'x',  # プレースホルダmはローカル変数から拾われた
                        'e_2': 'y',
                        'e_4': 'z',
                        'e_5': 3,
                        'e_6': 4,
                        'b': [1, 2, 3]}
