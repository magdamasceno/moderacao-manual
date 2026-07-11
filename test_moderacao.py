import streamlit as st
from google import genai
import json

# Configuração visual
st.set_page_config(page_title="Simulador de Moderação RA", layout="wide")

st.title("🛡️ Simulador de Moderação Reversa - Reclame AQUI")
st.caption("Analise o risco de negativa com base no manual oficial.")

# Coloque sua chave direto aqui entre as aspas para testar sem precisar digitar na tela
MINHA_CHAVE_FIXA = "" 

client = None

if MINHA_CHAVE_FIXA:
    client = genai.Client(api_key=MINHA_CHAVE_FIXA)
else:
    api_key = st.sidebar.text_input("Insira sua Gemini API Key:", type="password")
    if api_key:
        client = genai.Client(api_key=api_key)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Entradas do Caso")
    descricao = st.text_area("Descrição/Relato do Cliente:", height=200)
    resposta = st.text_area("Resposta Pública da Empresa:", height=150)
    replica = st.text_area("Réplica do Consumidor (Opcional):", height=100)
    
    botao_analisar = st.button("🚀 Analisar Risco de Moderação")

with col2:
    st.subheader("Análise e Veredito da IA")
    
    if botao_analisar:
        if client is None:
            st.error("⚠️ Por favor, insira sua API Key na barra lateral esquerda para rodar a análise.")
        else:
            with st.spinner("Analisando critérios do Reclame AQUI..."):
                prompt_sistema = f"""
                Você é um Auditor de Moderação do Reclame AQUI[cite: 1]. Sua tarefa é prever se um pedido de moderação na categoria "A empresa não violou o direito do cliente" será ACEITO ou NEGADO[cite: 1].

                [REGRAS DO MANUAL DO RA]
                - NEGADO (CO06 - Divergência) se houver bate-boca de fatos, datas ou valores conflitantes que o cliente rebateu na réplica/avaliação[cite: 1]. O RA não julga mérito nem analisa documentos[cite: 1].
                - NEGADO se o cliente mencionar qualquer Falha no Atendimento (atendentes, chat fora do ar, demora)[cite: 1].
                - ACEITO se o cliente causou o problema sozinho, perdeu prazos legais explicitamente ou se a resposta da empresa trouxe regras e cálculos matemáticos incontestáveis e o cliente fez réplica puramente de descontentamento subjetivo[cite: 1].

                DADOS DO CASO ATUAL:
                - DESCRIÇÃO: {descricao}
                - RESPOSTA DA EMPRESA: {resposta}
                - RÉPLICA DO CONSUMIDOR: {replica}

                Escreva sua resposta de forma direta e estruturada:
                1. VEREDITO PREVISTO: (Escreva ACEITO ou NEGADO em letras maiúsculas)
                2. MOTIVO / CARIMBO PROVÁVEL: (Diga qual regra ou carimbo como CO06 ou CO01 se aplica)[cite: 1]
                3. EXPLICAÇÃO: (Explique de forma curta e prática o porquê com base no texto inserido)
                """
                
                try:
                    # Nova sintaxe oficial da biblioteca google-genai usando o modelo flash (mais rápido)
                    response = client.models.generate_content(
                        model='gemini-2.0-flash',
                        contents=prompt_sistema,
                    )
                    
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"Erro na comunicação com a API do Gemini: {e}")
