import abc


class Constraint(abc.ABC):
    def __init__(self, field, **kwargs):
        self.field = field
        self.kwargs = kwargs
        self.__violations = None

    def __str__(self):
        pass

    def __repr__(self):
        kw = ', '.join('%s=%r' % x for x in self.kwargs.items())
        return f'{self.__class__.__name__}({self.field}, {kw})'

    def __hash__(self):
        return hash(tuple(self.to_dict().items()))

    def to_dict(self):
        kw = ', '.join('%s=%r' % x for x in self.kwargs.items())

        d = {'Constraint': self.__class__.__name__,
             'Field': self.field,
             'Args': (kw.replace("'", "").replace("<class ", "")
                      .replace(">", ""))}
        return d

    def is_valid(self):
        """Check if constrained fields are valid."""
        pass

    @abc.abstractmethod
    def is_violated(self, data):
        '''Check if constraint is violated by data.

        Args:
          data (pd.DataFrame)

        Returns:
          Boolean expressing constraint violation.
        '''
        pass

    @property
    def violations(self):
        return self.__violations

    @violations.setter
    def violations(self, df):
        self.__violations = df
