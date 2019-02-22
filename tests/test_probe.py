import pandas as pd
from dataprobe.probe import DataProbe
from dataprobe.values import Bounded


class TestDataProbe(object):
    def test_uuid(self):
        assert DataProbe().uuid != DataProbe().uuid

    def test_hash_equal(self):
        pi = DataProbe()
        pi.constrain(Bounded('x', upper=24))
        pj = DataProbe()
        pj.constrain(Bounded('x', upper=24))
        assert hash(pi) == hash(pj)

    def test_hash_different(self):
        pi = DataProbe()
        pi.constrain(Bounded('x', upper=12))
        pj = DataProbe()
        pj.constrain(Bounded('x', upper=24))
        assert hash(pi) != hash(pj)


class TestDataTest(object):
    def test_coverage_full(self):
        df = pd.DataFrame({'x': [0 for _ in range(10)]})
        p = DataProbe()
        p.constrain(Bounded('x', lower=0))
        t = p.run(df)
        assert t.coverage == 100

    def test_coverage_half(self):
        df = pd.DataFrame({'y': [0 for _ in range(10)],
                           'x': [0 for _ in range(10)]})
        p = DataProbe()
        p.constrain(Bounded('x', lower=0))
        t = p.run(df)
        assert t.coverage == 50

    def test_n_violations(self):
        df = pd.DataFrame({'y': [i for i in range(10)],
                           'x': [0 for _ in range(10)]})
        p = DataProbe()
        p.constrain(Bounded('y', lower=3))
        p.constrain(Bounded('x', lower=0))
        t = p.run(df)
        assert t.nviolations == [3, 0]

    def test_n_violations_empty(self):
        df = pd.DataFrame({'y': [i for i in range(10)],
                           'x': [0 for _ in range(10)]})
        p = DataProbe()
        p.constrain(Bounded('y', lower=0))
        t = p.run(df)
        assert t.nviolations == [0]
