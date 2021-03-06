from .constraints import Constraint


class CorrespondenceConstraint(Constraint):
    pass


class ManyToOne(CorrespondenceConstraint):
    def is_violated(self, data) -> tuple:
        otm = OneToMany(self.field[::-1])
        result, violations = otm.is_violated(data)
        return (result, violations)


class OneToMany(CorrespondenceConstraint):
    '''Implement one-to-many constraint.

    An element of A may be linked to many elements of B, but a member
    of B is linked to only one element of A.
    '''
    def is_violated(self, data) -> tuple:
        '''Check if there is at least one element of B corresponds to multiple
        elements of A.'''
        counts = data[self.field].drop_duplicates().groupby(
            self.field[1])[self.field[0]].count()
        vflag = (counts > 1)

        result = vflag.any()
        if result:
            violations = counts[vflag]
        else:
            violations = []

        return (result, violations)


class OneToOne(CorrespondenceConstraint):
    '''Implement a one-to-one constraint.'''
    def is_violated(self, data) -> tuple:
        '''Check if there is at least one entry mapping to multiple entries.'''
        # [TODO] implement gathering of violations
        import warnings
        warnings.warn('Inspection of violations for OneToOne constraints ' +
                      'is not implemented. Tests will run but no violations ' +
                      'will be available via .inspect() call.')
        if OneToMany(self.field).is_violated(data):
            return True
        if ManyToOne(self.field).is_violated(data):
            return True
        return False
