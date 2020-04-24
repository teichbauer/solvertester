
class Klause:
    def __init__(self, cname, clause):
        '''  clause example: {7:1, 5:0, 2:1}  '''
        self.name = cname
        self.clause = clause
        self.set_filter_and_mask()

    def set_filter_and_mask(self):
        # For the example klause {7:1, 5:0, 2:1}
        '''               BITS:   7  6  5  4  3  2  1  0
        the relevant bits:        *     *        *
        {7:1, 5:0, 2:1}'s filter: 1  0  1  0  0  1  0  0
        surppose v = 135 bin(v):  1  0  0  0  0  1  1  1
        x = v AND filter =        1  0  0  0  0  1  0  0
        bits of v left(rest->0):  ^     ^        ^
        {7:1, 5:0, 2:1}' mask  :  1  0  0  0  0  1  0  0
        This methos set self.filter
        '''
        filter = 0
        mask = 0
        for k, v in self.clause.items():
            filter = filter | (1 << k)
            if v == 1:
                mask = mask | (1 << k)
        self.mask = mask
        self.filter = filter

    def hit(self, v):
        '''
        first only let the relevant 3 bits from v remain -> fv
        mask ^ fv : (False: unsat, or hit by the mask, True: not hit, or SAT)
        return the reverse of this
        '''
        fv = self.filter & v
        return not bool(self.mask ^ fv)
