class SegmentTree:
    """Iterative segment tree over an associative op with an identity element."""

    def __init__(self, values, op, identity):
        self.op = op
        self.identity = identity
        self.size = 1 << (len(values) - 1).bit_length()
        self.tree = [identity] * (2 * self.size)
        self.tree[self.size:self.size + len(values)] = values
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = op(self.tree[2 * i], self.tree[2 * i + 1])

    def update(self, i, x):
        """Set position i to x."""
        i += self.size
        self.tree[i] = x
        i >>= 1
        while i:
            self.tree[i] = self.op(self.tree[2 * i], self.tree[2 * i + 1])
            i >>= 1

    def get(self, i):
        """Value at position i."""
        return self.tree[i + self.size]

    def query(self, lo, hi):
        """Combine values over the half-open range [lo, hi)."""
        lo += self.size
        hi += self.size
        res = self.identity
        while lo < hi:
            if lo & 1:
                res = self.op(res, self.tree[lo])
                lo += 1
            if hi & 1:
                hi -= 1
                res = self.op(res, self.tree[hi])
            lo >>= 1
            hi >>= 1
        return res
