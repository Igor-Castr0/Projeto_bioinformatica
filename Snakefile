rule all:
    input:
        "results/annotated_variants.csv"

rule annotate_variants:
    input:
        vcf="data/NIST.vcf",
        dbsnp="data/dbsnp.vcf",
        population_frequencies="data/population_frequencies.tsv"
    output:
        "results/annotated_variants.csv"
    script:
        "scripts/annotate_variants.py"
