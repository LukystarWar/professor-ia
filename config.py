from dotenv import load_dotenv
import os
from datetime import datetime

# Carrega variáveis de ambiente
load_dotenv()

# Data atual formatada
DATA_ATUAL = datetime.now().strftime("%d/%m/%Y")

# Configurações do LLM
LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'groq')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
MODEL_NAME = os.getenv('MODEL_NAME', 'llama2-70b-4096')

# Configurações da aplicação
DISCIPLINAS = [
    "Português",
    "Matemática",
    "História",
    "Ciências",
    "Geografia",
    "Ed. Física",
    "Religião",
    "Artes"
]

SERIES = [f"{i}º ano" for i in range(1, 10)]

# Template do prompt para geração de provas
PROVA_PROMPT_TEMPLATE = """IMPORTANTE: Sua resposta deve ser APENAS um objeto JSON válido, sem texto adicional antes ou depois.

Como professor especialista em {disciplina} para o {serie} do ensino fundamental, crie uma prova sobre os seguintes temas:
{temas}

Requisitos da prova:
1. 10 questões objetivas (A, B, C, D)
2. Questões contextualizadas com situações do cotidiano
3. Linguagem apropriada para {serie}
4. Cada questão deve ter texto-base ou contextualização
5. Questões devem estimular interpretação e raciocínio
6. Alternativas claras e inequívocas

Use EXATAMENTE este formato JSON (mantenha as chaves exatamente como mostradas):
{{
    "titulo": "Avaliação de {disciplina} - {serie}",
    "disciplina": "{disciplina}",
    "serie": "{serie}",
    "professor": "Prof. Especialista",
    "data": "{data_atual}",
    "questoes": [
        {{
            "numero": 1,
            "enunciado": "Texto da questão com contextualização",
            "alternativas": {{
                "a": "Texto da alternativa A",
                "b": "Texto da alternativa B",
                "c": "Texto da alternativa C",
                "d": "Texto da alternativa D"
            }},
            "resposta_correta": "a"
        }}
    ]
}}

LEMBRE-SE:
- Não adicione comentários ou texto fora do JSON
- Use aspas duplas para strings
- A resposta_correta deve ser apenas a letra (a, b, c ou d)
- Mantenha a estrutura exata do JSON"""