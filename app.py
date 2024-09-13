from flask import Flask, jsonify, request
import vcfpy
import json

app = Flask(__name__)

# Função para carregar o arquivo VCF e retornar as variantes
def load_vcf(file_path):
    variants = []
    with vcfpy.Reader.from_path(file_path) as reader:
        for record in reader:
            variant = {
                "chrom": record.CHROM,
                "pos": record.POS,
                "id": record.ID,
                "ref": record.REF,
                "alt": [str(alt) for alt in record.ALT],
                "info": record.INFO
            }
            variants.append(variant)
    return variants

@app.route('/variants', methods=['GET'])
def get_variants():
    vcf_path = 'data/NIST.vcf.gz'  # Caminho para o arquivo VCF
    variants = load_vcf(vcf_path)
    return jsonify(variants)

@app.route('/')
def home():
    return "API de Bioinformática está funcionando!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
