import uuid
import pandas as pd
from .constraints import Constraint
from .helpers import colorize, flatten_list


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

    def __hash__(self):
        return hash(tuple(self.__constraints))

    @property
    def uuid(self):
        """Return unique probe identifier."""
        return self.__uuid

    @property
    def constraints(self):
        """Return constraints appended to the probe."""
        return self.__constraints

    def constrain(self, const: Constraint) -> None:
        """Append constraint to probe's list of constraints."""
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
          datatest (:obj:`DataTest`): generated test.

        Raises:
          (It should raise an error in case probe does not match data).
        """
        datatest = DataTest(data, self)
        return datatest


class DataTest(object):
    """Verify and log if and how `data` violates a set of constraints.

    Args:
      data (pd.DataFrame): data to be tested.
      probe (:obj:`DataProbe`): probe containing  constraints to be applied.
    """
    def __init__(self, data: pd.DataFrame, probe: DataProbe):
        self.data = data
        self.probe = probe
        self.__tested = []
        self.process()

    def __hash__(self):
        return hash(frozenset(self.data)) ^ hash(self.probe)

    def process(self):
        """Apply constraints defined in instance of :obj:DataProbe to data."""
        results = [c.is_violated(self.data)
                   for c in self.probe.constraints]

        summary = self.probe.summary
        self.__tested = flatten_list(list(summary.Field))
        self.__nviolations = [x[1].shape[0] if x[0] else 0
                              for x in results]
        self.__verdict = ['Violated' if x[0] else 'OK'
                          for x in results]

        # append violation flag
        summary.loc[:, 'Result'] = self.__verdict

        # append number of violations
        summary.loc[:, 'NrViolations'] = self.__nviolations

        self.__details = [x[1] for x in results]
        self.__summary = summary
        self.results = results

    @property
    def summary(self):
        """Generate a styled summary of test results."""
        summary = self.__summary.style.applymap(
            colorize,
            subset=pd.IndexSlice[:, 'Result'])
        return summary

    @property
    def coverage(self):
        """Return percentage of columns covered by the test."""
        data_cols = set(self.data.columns)
        n_data_cols = len(data_cols)
        tested_cols = set(self.__tested)
        n_tested_cols = len(data_cols.intersection(tested_cols))
        return n_tested_cols/n_data_cols * 100

    @property
    def nviolations(self):
        """Return number of violations verified in the test."""
        return self.__nviolations

    @property
    def details(self):
        """Return violations that led to failed tests."""
        return self.__details
