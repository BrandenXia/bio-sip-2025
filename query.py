import re

from utils import GAF_DIR, GFF_DIR, GTF_DIR, rg_search

LOC_REGEX = re.compile(r"\bLOC\d+\b")
REGION_NAME_REGEX = re.compile(r";Name=(\w+);")
GENE_ID_REGEX = re.compile(r"gene_id \"(\w+)\";")


def go2locs(go_id: str) -> set[str]:
    locs = [
        matched.group(0)
        for loc in rg_search(GAF_DIR, go_id)
        if (matched := LOC_REGEX.search(loc))
    ]
    locs = set(locs)

    return locs


region_cache: dict[str, str] = {}


def loc2region(loc: str) -> tuple[str, int, int]:
    global region_cache

    gene = [
        (split[0].split(":")[1], int(split[3]), int(split[4]))
        for gene in rg_search(GFF_DIR, f"ID=gene-{loc}")
        if (split := gene.split("\t"))
    ][0]

    if gene[0] in region_cache:
        region = region_cache[gene[0]]
    else:
        region = rg_search(GFF_DIR, f"ID={gene[0]}")[0]
        if matched := REGION_NAME_REGEX.search(region):
            region = matched.group(1)
            region_cache[gene[0]] = region
        else:
            raise ValueError(f"Region name not found for {gene[0]}")

    return region, gene[1], gene[2]


def geneid2loc(geneid: str) -> str:
    line = rg_search(GTF_DIR, geneid)[0]
    if matched := re.search(GENE_ID_REGEX, line):
        return matched.group(1)
    else:
        raise ValueError(f"Gene ID not found for {geneid}")
