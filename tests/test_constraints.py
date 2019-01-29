import pytest
import pandas as pd
import dataprobe as dp
from dataprobe.correspondence import OneToOne, OneToMany, ManyToOne
from dataprobe.cov import Monotonic
from dataprobe.values import Bounded, Positive, Negative
from dataprobe.values import ElementOf, Contains, Match
from dataprobe.types import Type


def generate_df(data_dict):
    return pd.DataFrame(data=data_dict)


class TestBounded(object):

    def test_lower_bound(self):
        c = Bounded('age', lower=0)

        bdf = generate_df({'name': [0, 1, 23, 21, 20, 19],
                           'age': [20, 1, 31, 32, 2, -1]})
        gdf = generate_df({'name': [0, 1, 23, 21, 20, 19],
                           'age': [20, 1, 31, 32, 2, 1]})

        assert (c.is_violated(bdf)[0] & ~c.is_violated(gdf)[0])

    def test_upper_bound(self):
        c = Bounded('hours_per_day', upper=24)

        bdf = generate_df({'hours_per_day': [0, 1, 25, 21, 20, 19],
                           'x': [1, 2, 3, 4, 5, 6]})
        gdf = generate_df({'hours_per_day': [0, 1, 23, 21, 20, 19],
                           'x': [1, 2, 3, 4, 5, 6]})

        assert (c.is_violated(bdf)[0] & ~c.is_violated(gdf)[0])

    def test_both_bounds(self):
        c = Bounded('hours_per_day', upper=24, lower=0)

        bdf = generate_df({'hours_per_day': [-2, 1, 26, 21, 20, 19],
                           'x': [1, 2, 3, 4, 5, 6]})
        gdf = generate_df({'hours_per_day': [0, 1, 23, 21, 20, 19],
                           'x': [1, 2, 3, 4, 5, 6]})

        assert (c.is_violated(bdf)[0] & ~c.is_violated(gdf)[0])

    def test_negative(self):
        c = Negative('x')

        bdf = generate_df({'x': [-1, -1, 23, -21, -20, 19],
                           'age': [20, 1, 31, 32, 2, 10]})
        gdf = generate_df({'x': [-1, -2, -2, -4, -2, -19],
                           'age': [20, 1, 31, 32, 2, 1]})

        assert (c.is_violated(bdf)[0] & ~c.is_violated(gdf)[0])

    def test_positive(self):
        c = Positive('age')

        bdf = generate_df({'x': [1, 1, 23, 21, 20, 19],
                           'age': [20, 1, 31, 32, -2, 10]})
        gdf = generate_df({'x': [1, 2, 2, 4, 2, 19],
                           'age': [20, 1, 31, 32, 2, 1]})

        assert (c.is_violated(bdf)[0] & ~c.is_violated(gdf)[0])


class TestMatch(object):

    def test_regex_match(self):
        c = Match('test_names', pattern='test_.')
        bdf = generate_df({'test_names': ['afatest',
                                          '--testaff asf',
                                          '!!test dafas',
                                          'test___',
                                          '___test',
                                          '-__test'],
                           'x': [20, 1, 31, 32, 2, 10]})
        gdf = generate_df({'test_names': ['test_1',
                                          'test_probe',
                                          'test_12314',
                                          'test_another',
                                          'test_full',
                                          'test_da'],
                           'x': [20, 1, 31, 32, 2, 10]})
    
        assert (c.is_violated(bdf)[0] & ~c.is_violated(gdf)[0])

        
class TestContains(object):
    def test_contains(self):
        c = Contains('test_names', pattern='test')
        bdf = generate_df({'test_names': ['afatst',
                                          '--testaff asf',
                                          '!!test dafas',
                                          'test___',
                                          '___test',
                                          '-__test'],
                           'x': [20, 1, 31, 32, 2, 10]})
        gdf = generate_df({'test_names': ['ad test_1',
                                          'fadatest_probe',
                                          'da-test_12314',
                                          '111!test_another',
                                          '__1test_full',
                                          '1_test_da'],
                           'x': [20, 1, 31, 32, 2, 10]})
    
        assert (c.is_violated(bdf)[0] & ~c.is_violated(gdf)[0])


class TestElementOf(object):
    def test_element_of(self):
        c = ElementOf('color', collection=['B', 'R'])
        bdf = generate_df({'color': ['B',
                                     'R',
                                     'B',
                                     'R',
                                     'F',
                                     'R'],
                           'x': [20, 1, 31, 32, 2, 10]})
        gdf = generate_df({'color': ['B',
                                     'R',
                                     'B',
                                     'R',
                                     'B',
                                     'R'],
                           'x': [20, 1, 31, 32, 2, 10]})
    
        assert (c.is_violated(bdf)[0] & ~c.is_violated(gdf)[0])


# probe.constrain(OneToMany(['author', 'book']))
# probe.constrain(ManyToOne(['author', 'gender']))
# probe.constrain(OneToOne(['age', 'years_to_retire']))
# probe.constrain(Type('years_to_retire', dtype=int))
# probe.constrain(Monotonic('n_pages'))
# probe.summary()
# r = probe.run(df)[0]
# print(r)


