from .types import TypeConstraint


class ValueConstraint(TypeConstraint):
    # if we have a value constraint, then we have inherently a type
    # constraint What should I do about this class?  My intuition is
    # that it should exist, but what for?  - constraint violation
    # exceptions? e.g.: - ValueOutOfBounds - ValueOutOfSet It should
    # implement a method that is called upon testing to ensure that
    # the type constraint is met. e.g. decorate the violated method
    # such that it checks if TypeConstraint is violated. But then, is
    # extending type constraint the right thing to do?
    def __str__(self):
        pass


class Bounded(ValueConstraint):

    def is_violated(self, data) -> tuple:
        '''Check if lower or upper bound constraint are violated.'''

        # this needs to be reimplemented
        if ('lower' in self.kwargs) & ('upper' in self.kwargs):
            vflag = ((data[self.field] < self.kwargs['lower']) |
                     (data[self.field] > self.kwargs['upper']))
        else:
            if 'lower' in self.kwargs:
                vflag = data[self.field] < self.kwargs['lower']
            if 'upper' in self.kwargs:
                vflag = data[self.field] > self.kwargs['upper']
        result = vflag.any()
        if result:
            violations = data[self.field][vflag]
        else:
            violations = []

        return (result, violations)


class Positive(ValueConstraint):
    def is_violated(self, data) -> tuple:
        '''Check if value is bounded from below by zero.'''
        return Bounded(self.field, lower=0).is_violated(data)


class Negative(ValueConstraint):
    def is_violated(self, data) -> tuple:
        '''Check if value is bounded from below by zero.'''
        return Bounded(self.field, upper=0).is_violated(data)


class ElementOf(ValueConstraint):
    def is_violated(self, data) -> tuple:
        '''Check if all values in data[self.field] belong to a set.'''
        vflag = ~data[self.field].isin(self.kwargs['collection'])
        result = vflag.any()
        if result:
            violations = data[self.field][vflag]
        else:
            violations = []

        return (result, violations)


class Match(ValueConstraint):
    def is_violated(self, data) -> tuple:
        '''Check if text field adheres to a particular format.'''
        kwargs = dict(self.kwargs)
        pat = kwargs.pop('pattern')

        # [REV] I think this is not necessary here!
        if 'regexp' in kwargs:
            regexp = kwargs.pop('regexp')
            if regexp:
                import re
                pat = re.compile(pat)

        vflag = ~data[self.field].str.match(pat, **kwargs)

        result = vflag.any()
        if result:
            violations = data[self.field][vflag]
        else:
            violations = []

        return (result, violations)


class Contains(ValueConstraint):
    def is_violated(self, data) -> tuple:
        kwargs = dict(self.kwargs)
        pat = kwargs.pop('pattern')
        vflag = ~data[self.field].str.contains(pat, **kwargs)

        result = vflag.any()
        if result:
            violations = data[self.field][vflag]
        else:
            violations = []

        return (result, violations)
