import uuid
import pandas as pd
from .constraints import Constraint
from .helpers import colorize


class DataProbe(object):
    """Handle specification of constraints for a data test.

    :obj:`DataProbe` provides methods for gathering constraints which, when
    applied to data, yield a :obj:`DataTest` instance holding the details of
    the test.
    """
    def __init__(self, **kwargs):
        self.__uuid = uuid.uuid4()
        self.__constraints = []
        self.status = 'INIT'

    def __repr__(self):
        return '%s #%s [%i constraints]' % \
            (self.__class__.__name__,
             str(self.__uuid)[:5],
             len(self.constraints))

    def __str__(self):
        return f'[{self.status}] DataProbe.'

    @property
    def constraints(self):
        return self.__constraints

    def constrain(self, const: Constraint) -> None:
        self.__constraints.append(const)

    @property
    def summary(self) -> pd.DataFrame:
        """Return a summary of constraints assigned to the probe.

        Returns:
          Pandas dataframe describing constaints applied to data fields.
        """
        return pd.DataFrame([c.to_dict()
                            for c in self.constraints])[
                                    ['Field', 'Constraint', 'Args']]

    def run(self, data: pd.DataFrame):
        """Apply a probe to `data` by running a DataTest.

        Args:
          data (pd.DataFrame): data to be tested.

        Returns:
          datatest (DataTest): test resulting of applying probe to `data`.

        Raises:
          (It should raise an error in case probe does not match data)
        """
        datatest = DataTest(data, self)
        return datatest


class DataTest(object):
    """Verify and log if and how `data` violates a set of constraints.

    Args:
      data (pd.DataFrame): data to be tested
      probe (pd.DataProbe): probe containing  constraints to be applied.
    """
    def __init__(self, data: pd.DataFrame, probe: DataProbe):
        self.data = data
        self.probe = probe
        self.process()

    def process(self):
        results = [c.is_violated(self.data)
                   for c in self.probe.constraints]
        summary = self.probe.summary
        summary.loc[:, 'Result'] = ['Violated' if x[0] else 'OK'
                                    for x in results]
        summary = summary.style.applymap(colorize,
                                         subset=pd.IndexSlice[:, 'Result'])
        self.__details = [x[1] for x in results]
        self.__summary = summary
        self.results = results

    @property
    def summary(self):
        return self.__summary

    @summary.setter
    def summary(self, s: pd.DataFrame):
        self.__summary = s

    @property
    def details(self):
        return self.__details

    @details.setter
    def details(self, test_details):
        self.__details = test_details
