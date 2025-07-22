import streamlit as st
import os
from datetime import datetime
from llm_service import LLMService
from word_generator import WordGenerator
from config import DISCIPLINAS, SERIES

def criar_nome_arquivo(disciplina: str, serie: str) -> str:
    """Cria um nome de arquivo único para a prova"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_base = f"Prova_{disciplina}_{serie}_{timestamp}"
    return nome_base.replace(" ", "_").replace("º", "") + ".docx"

def main():
    st.set_page_config(
        page_title="Gerador de Provas",
        page_icon="📚",
        layout="centered"
    )
    
    st.title("📚 Gerador Automático de Provas")
    st.write("Sistema para geração automática de provas escolares usando IA")
    
    # Inicialização dos serviços
    llm_service = LLMService()
    word_generator = WordGenerator()
    
    # Interface
    with st.form("prova_form"):
        # Seleção de disciplina
        disciplina = st.selectbox(
            "Selecione a disciplina:",
            options=DISCIPLINAS
        )
        
        # Seleção de série
        serie = st.selectbox(
            "Selecione a série:",
            options=SERIES
        )
        
        # Campo de temas
        temas = st.text_area(
            "Digite os temas da prova (um por linha):",
            height=150,
            placeholder="Ex:\nFrações\nOperações básicas\nProblemas com números decimais"
        )
        
        # Botão de geração
        submitted = st.form_submit_button("Gerar Prova")
    
    if submitted and temas.strip():
        try:
            with st.spinner("Gerando sua prova... Aguarde um momento..."):
                # Gera a prova usando o LLM
                prova_data = llm_service.gerar_prova(
                    disciplina=disciplina,
                    serie=serie,
                    temas=temas
                )
                
                # Gera o documento Word
                doc = word_generator.generate_prova(prova_data)
                
                # Salva o arquivo
                output_file = criar_nome_arquivo(disciplina, serie)
                doc.save(output_file)
                
                # Exibe prévia da prova
                st.success("✅ Prova gerada com sucesso!")
                
                # Mostra prévia das questões
                st.subheader("Prévia da Prova")
                for questao in prova_data['questoes']:
                    with st.expander(f"Questão {questao['numero']}"):
                        st.write(questao['enunciado'])
                        for letra, texto in questao['alternativas'].items():
                            st.write(f"{letra.upper()}) {texto}")
                        st.write(f"**Resposta**: {questao['resposta_correta'].upper()}")
                
                # Botão de download
                with open(output_file, "rb") as file:
                    st.download_button(
                        label="📥 Baixar Prova (.docx)",
                        data=file,
                        file_name=output_file,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                
                # Remove o arquivo temporário
                os.remove(output_file)
                
        except Exception as e:
            st.error(f"Erro ao gerar a prova: {str(e)}")
    
    # Rodapé
    st.markdown("---")
    st.markdown(
        "Desenvolvido com ❤️ usando Streamlit e IA | "
        "Versão 1.0.0"
    )

if __name__ == "__main__":
    main()