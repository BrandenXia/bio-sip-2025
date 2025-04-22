import re
import sys

from typing import Iterator

from utils import GAF_DIR, GFF_DIR, rg_search

LOC_REGEX = re.compile(r"\bLOC\d+\b")
REGION_NAME_REGEX = re.compile(r";Name=(\w+);")


def get_regions(go_id: str) -> Iterator[tuple[str, tuple[str, tuple[int, int]]]]:
    locs = [
        matched.group(0)
        for loc in rg_search(GAF_DIR, go_id)
        if (matched := LOC_REGEX.search(loc))
    ]
    locs = set(locs)

    genes = [
        [
            (split[0].split(":")[1], (int(split[3]), int(split[4])))
            for gene in rg_search(GFF_DIR, f"ID=gene-{loc}")
            if (split := gene.split("\t"))
        ]
        for loc in locs
    ]
    genes = [gene[0] for gene in genes if gene]

    regions = [gene[0] for gene in genes]
    regions = set(regions)
    regions_map: dict[str, str] = {
        region: matched.group(1)
        for region in regions
        if (matched := REGION_NAME_REGEX.search(rg_search(GFF_DIR, f"ID={region}")[0]))
    }

    genes = [(regions_map[region], indices) for region, indices in genes]

    return zip(locs, genes)


go_id = sys.argv[1]
res = get_regions(go_id)
for loc, (region, indices) in res:
    print(loc, region, f"{indices[0]}-{indices[1]}", sep="\t")
