import os
import pandas as pd
import vcfpy

def annotate_vcf(vcf_file, dbsnp_file, population_file, output_file):
    # Caminhos absolutos
    vcf_file = os.path.abspath(vcf_file)
    dbsnp_file = os.path.abspath(dbsnp_file)
    population_file = os.path.abspath(population_file)
    output_file = os.path.abspath(output_file)

    # Imprimir o diretório atual e os caminhos absolutos
    print(f"Diretório atual: {os.getcwd()}")
    print(f"Arquivo VCF: {vcf_file}")
    print(f"Arquivo dbSNP: {dbsnp_file}")
    print(f"Arquivo de frequências populacionais: {population_file}")
    print(f"Arquivo de saída: {output_file}")

    # Lê o arquivo VCF
    try:
        vcf_reader = vcfpy.Reader.from_path(vcf_file)
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {vcf_file}")
        return

    # Lê o arquivo dbSNP
    try:
        dbsnp_reader = vcfpy.Reader.from_path(dbsnp_file)
        dbsnp_dict = {}
        for record in dbsnp_reader:
            ids = record.ID if isinstance(record.ID, list) else [record.ID]
            for dbsnp_id in ids:
                dbsnp_dict[dbsnp_id] = dbsnp_id
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {dbsnp_file}")
        return

    # Lê o arquivo de frequências populacionais
    try:
        population_data = pd.read_csv(population_file, sep='\t', comment='#')
        print("Colunas encontradas no arquivo de frequências populacionais:")
        print(population_data.columns)

        if 'variant_id' not in population_data.columns or 'frequency' not in population_data.columns:
            raise ValueError("As colunas 'variant_id' e 'frequency' não foram encontradas no arquivo de frequências populacionais.")

        population_dict = population_data.set_index('variant_id').to_dict()['frequency']
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {population_file}")
        return
    except Exception as e:
        print(f"Erro ao ler o arquivo de frequências populacionais: {e}")
        return

    # Inicialize uma lista para armazenar as linhas de dados
    annotated_data = []

    # Processar cada variante no VCF
    for record in vcf_reader:
        chrom = record.CHROM
        pos = record.POS
        ref = record.REF
        # Converter ALT para string se não for já uma string
        alt = ','.join(str(alt) for alt in record.ALT)
        ids = record.ID if isinstance(record.ID, list) else [record.ID]
        
        for id in ids:
            # Obter dbSNP ID e frequência
            dbsnp_id = dbsnp_dict.get(id, '.')
            frequency = population_dict.get(id, '.')

            # Adicionar os dados à lista
            annotated_data.append({
                'CHROM': chrom,
                'POS': pos,
                'ID': id,
                'REF': ref,
                'ALT': alt,
                'DBSNP_ID': dbsnp_id,
                'FREQUENCY': frequency
            })

    # Converter a lista para um DataFrame
    annotated_df = pd.DataFrame(annotated_data)

    # Verificar o DataFrame antes de salvar
    print("Dados anotados:")
    print(annotated_df.head())

    # Salvar o resultado em um arquivo CSV
    if not os.path.exists(os.path.dirname(output_file)):
        os.makedirs(os.path.dirname(output_file))
    annotated_df.to_csv(output_file, index=False)
    print(f"Arquivo de saída salvo em: {output_file}")

if __name__ == "__main__":
    # Caminhos relativos a partir do diretório scripts
    annotate_vcf('../data/NIST.vcf', '../data/dbsnp.vcf', '../data/population_frequencies.tsv', '../results/annotated_variants.csv')
