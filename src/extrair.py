import re
import sys
from pathlib import Path

from pypdf import PdfReader

MANTER_HIFEN = {"se", "lo", "la", "los", "las", "nos", "lhe", "lhes", "paga", "pago", "di", "me", "te", "o", "a"}


def corrige_hifen(m):
    antes, depois = m.group(1), m.group(2)
    if depois.lower() in MANTER_HIFEN:
        return m.group(0)
    return antes + "ti" + depois


def limpar(texto):
    texto = texto.replace("\ufb01", "fi").replace("\ufb02", "fl").replace("\u202f", " ")
    texto = re.sub(r"\bOFcio\b", "Ofício", texto)
    texto = re.sub(r"\(\s*(\d+)\s*\)", r"(\1)", texto)
    texto = re.sub(r"(\d+)\s*\n\.\s*\n", r"\1. ", texto)
    texto = re.sub(r"\b(\w*[a-záéíóúâêôãõç])-([a-záéíóúâêôãõç]+)\b", corrige_hifen, texto)
    texto = re.sub(r"\(?\d{2}\)?\s?9?\d{4}-\d{4}", "[telefone]", texto)
    texto = re.sub(r"\n\s*\n", "\n\n", texto)
    texto = re.sub(r"(?<![.:;\n])\n(?!\n|\d+\.\s)", " ", texto)
    texto = re.sub(r"[ \t]+", " ", texto)
    return texto.strip()


def extrair(caminho):
    paginas = []
    for i, p in enumerate(PdfReader(caminho).pages, start=1):
        paginas.append((i, limpar(p.extract_text() or "")))
    return paginas


if __name__ == "__main__":
    arquivo = Path(sys.argv[1])
    for numero, texto in extrair(arquivo):
        print(f"--- página {numero} ({len(texto)} caracteres) ---")
        print(texto[:1200])
        print()