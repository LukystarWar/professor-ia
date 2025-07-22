import json
import os
from openai import OpenAI
from config import (
    LLM_PROVIDER, GROQ_API_KEY, MODEL_NAME,
    PROVA_PROMPT_TEMPLATE, DATA_ATUAL
)

class LLMService:
    def __init__(self):
        if os.getenv('GROQ_API_KEY'):
            self.client = OpenAI(
                api_key=os.getenv('GROQ_API_KEY'),
                api_base="https://api.groq.com/openai/v1"
            )
        else:
            raise ValueError(f"API key não encontrada no ambiente")
    
    def _validar_json(self, json_str: str) -> str:
        """Limpa e valida a string JSON"""
        # Remove possíveis caracteres especiais ou whitespace no início/fim
        json_str = json_str.strip()
        
        # Remove marcadores de código se presentes
        if json_str.startswith('```'):
            json_str = json_str.split('\n', 1)[1]
        if json_str.endswith('```'):
            json_str = json_str.rsplit('\n', 1)[0]
        
        # Remove qualquer texto antes ou depois do JSON
        json_str = json_str.strip()
        if json_str.startswith('{'):
            json_str = json_str[json_str.find('{'):json_str.rfind('}')+1]
            
        return json_str

    def gerar_prova(self, disciplina: str, serie: str, temas: str) -> dict:
        """Gera uma prova usando o LLM configurado"""
        prompt = PROVA_PROMPT_TEMPLATE.format(
            disciplina=disciplina,
            serie=serie,
            temas=temas,
            data_atual=DATA_ATUAL
        )
        
        try:
            if LLM_PROVIDER == 'groq':
                completion = self.client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {
                            "role": "system", 
                            "content": "Você é um assistente especializado em gerar provas escolares. "
                                     "Suas respostas devem ser SEMPRE em formato JSON válido, sem texto adicional."
                        },
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    response_format={ "type": "json_object" }
                )
                response = completion.choices[0].message.content
                
                # Limpa e valida o JSON
                json_str = self._validar_json(response)
                
                try:
                    prova = json.loads(json_str)
                except json.JSONDecodeError as e:
                    print(f"JSON inválido recebido: {json_str}")
                    print(f"Erro de parse: {str(e)}")
                    raise Exception("O modelo retornou um JSON inválido. Por favor, tente novamente.")
                
                # Valida a estrutura do JSON
                campos_obrigatorios = ['titulo', 'disciplina', 'serie', 'professor', 'data', 'questoes']
                for campo in campos_obrigatorios:
                    if campo not in prova:
                        raise Exception(f"Campo obrigatório '{campo}' não encontrado na resposta")
                
                # Valida cada questão
                for questao in prova['questoes']:
                    campos_questao = ['numero', 'enunciado', 'alternativas', 'resposta_correta']
                    for campo in campos_questao:
                        if campo not in questao:
                            raise Exception(f"Campo '{campo}' não encontrado na questão {questao.get('numero', '?')}")
                    
                    # Valida alternativas
                    if not all(letra in questao['alternativas'] for letra in ['a', 'b', 'c', 'd']):
                        raise Exception(f"Questão {questao['numero']} não tem todas as alternativas (a, b, c, d)")
                    
                    # Valida resposta correta
                    if questao['resposta_correta'] not in ['a', 'b', 'c', 'd']:
                        raise Exception(f"Resposta correta inválida na questão {questao['numero']}")
                
                return prova
                
        except Exception as e:
            raise Exception(f"Erro ao gerar prova: {str(e)}")