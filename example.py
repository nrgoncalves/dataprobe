import pandas as pd
import dataprobe as dp
from dataprobe.correspondence import OneToOne, OneToMany, ManyToOne
from dataprobe.cov import Monotonic
from dataprobe.values import Bounded, ElementOf, Contains, Match
from dataprobe.types import Type


age = [20, 20, 2, 50, 26, 23]
retirement_age = 65

df = pd.DataFrame(data={'author': ['jmf', 'kl', 'jlr', 'anm', 'mer', 'jmf'],
                        'book': ['01', '02', '06', '03', '04', '01'],
                        'hours_per_day': [0, 1, 23, 21, 20, 19],
                        'age': age,
                        'years_to_retire': [21, 21, 2, 50, 26, 23],
                        # 'years_to_retire': [retirement_age - x for x in age],
                        'n_pages': [1, 2, 3, 4, 5, 6],
                        'gender': ['M', 'F', 'M', 'F', 'F', 'M']})

probe = dp.DataProbe()
probe.constrain(Bounded('hours_per_day', lower=0, upper=24))
probe.constrain(Bounded('age', lower=0))
probe.constrain(ElementOf('gender', collection=['M', 'F']))
probe.constrain(OneToMany(['author', 'book']))
probe.constrain(ManyToOne(['author', 'gender']))
probe.constrain(OneToOne(['age', 'years_to_retire']))
probe.constrain(Contains('book', pattern='0'))
probe.constrain(Match('book', pattern='0.', regexp=True))
probe.constrain(Type('years_to_retire', dtype=int))
probe.constrain(Monotonic('n_pages'))
probe.summary
r = probe.run(df)
print(r)
