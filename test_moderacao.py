import streamlit as st
import google.generativeai as genai
import json

# Configuração visual da página
st.set_page_config(page_title="Simulador de Moderação RA", layout="wide")

st.title("🛡️ Simulador de Moderação Reversa - Reclame AQUI")
st.caption("Analise o risco de negativa e gere respostas blindadas com base no manual oficial.")

# Área para colar a chave de API (Você pode deixar uma fixa no código se preferir)
api_key = st.sidebar.text_input("Insira sua Gemini API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.warning("⚠️ Insira sua Gemini API Key na barra lateral para ativar o sistema.")

# Criando o formulário na tela
col1, col2 = st.columns(2)

with col1:
    st.subheader("Entradas do Caso")
    descricao = st.text_area("Descrição/Relato do Cliente:", height=200)
    resposta = st.text_area("Resposta Pública da Empresa:", height=150)
    replica = st.text_area("Réplica do Consumidor (Opcional):", height=100)
    
    botao_analisar = st.button("🚀 Analisar Risco de Moderação")

with col2:
    st.subheader("Análise e Veredito da IA")
    
    if botao_analisar and api_key:
        with st.spinner("Analisando o manual do Reclame AQUI..."):
            
            prompt_sistema = f"""
            Você é um Auditor de Moderação do Reclame AQUI. Sua tarefa é prever se um pedido de moderação na categoria "A empresa não violou o direito do cliente" ou "Este é um caso de fraude" será ACEITO ou NEGADO.

            [DIRETRIZES DE SUCESSO]
            - ACEITO se a empresa provar matematicamente/via regulamento que seguiu o padrão e o cliente apenas demonstrar insatisfação subjetiva.
            - ACEITO se o cliente admitir que perdeu prazos (ex: testar após 7 dias) ou causou o próprio problema (ex: trânsito).
            - ACEITO se a resposta citar cláusulas exatas que desmentem a premissa do cliente sem margem para dupla interpretação.

            [DIRETRIZES DE REJEIÇÃO]
            - NEGADO (CO06 - Divergência) se houver bate-boca de fatos não comprováveis publicamente (datas ou valores conflitantes).
            - NEGADO se o cliente mencionar "Falha no Atendimento" (demora, chat que caiu).

            DADOS DO CASO ATUAL:
            - TÍTULO: {titulo}
            - DESCRIÇÃO: {descricao}
            - RESPOSTA DA EMPRESA: {resposta}
            - RÉPLICA DO CONSUMIDOR: {replica}

            Retorne estritamente um formato JSON válido (sem markdown ou texto extra):
            {{
                "veredito_previso": "ACEITO" ou "NEGADO",
                "carimbo_provavel": "CO01" ou "CO06" ou "Nenhum",
                "chance_sucesso_percentual": 85,
                "justificativa": "Sua explicação detalhada aqui."
            }}
            """
            
            try:
                model = genai.GenerativeModel('gemini-1.5-pro')
                response = model.generate_content(prompt_sistema)
                
                # Limpa marcações de código markdown se o modelo colocar
                texto_limpo = response.text.replace("```json", "").replace("```", "").strip()
                dados = json.loads(texto_limpo)
                
                # Exibindo os resultados visualmente
                if dados["veredito_previso"] == "ACEITO":
                    st.success(f"🎉 Veredito: {dados['veredito_previso']} ({dados['chance_sucesso_percentual']}% de chance)")
                else:
                    st.error(f"❌ Veredito: {dados['veredito_previso']} ({dados['chance_sucesso_percentual']}% de risco de rejeição)")
                    
                st.metric(label="Carimbo Provável do RA", value=dados["carimbo_provavel"])
                st.info(f"**Justificativa Analítica:** {dados['justificativa']}")
                
            except Exception as e:
                st.error(f"Erro ao processar análise: {e}")
