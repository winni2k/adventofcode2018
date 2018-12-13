from collections import defaultdict

import attr


@attr.s(slots=True)
class Claim:
    cid = attr.ib()
    x = attr.ib()
    y = attr.ib()
    w = attr.ib()
    h = attr.ib()

    @classmethod
    def from_line(cls, line):
        fields = line.rstrip().split()
        cid = fields[0]
        x, y = fields[2].rstrip(':').split(',')
        w, h = fields[3].split('x')
        return cls(cid=cid, x=int(x), y=int(y), w=int(w), h=int(h))

    def contained_coordinates(self):
        for x in range(self.x, self.x + self.w):
            for y in range(self.y, self.y + self.h):
                yield (x, y)


def main(lines):
    claims = []
    for line in lines:
        claims.append(Claim.from_line(line))
    all_claim_ids = {claim.cid for claim in claims}
    print(all_claim_ids)

    seen_coordinates = defaultdict(set)
    for idx, claim in enumerate(claims):
        for coord in claim.contained_coordinates():
            seen_coordinates[coord].add(claim.cid)

    assert len(seen_coordinates.keys()) <= 1000 * 1000

    for claim_ids in seen_coordinates.values():
        if len(claim_ids) > 1:
            for claim_id in claim_ids:
                all_claim_ids.discard(claim_id)

    return sum(1 for count in seen_coordinates.values() if len(count) > 1), all_claim_ids


test = """#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
"""
print(main(test.splitlines(keepends=True)))
print(main(open('input.txt').readlines()))

