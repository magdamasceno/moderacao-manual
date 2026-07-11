import google.generativeai as genai

genai.configure(api_key="SUA_CHAVE_API_AQUI")

def simular_moderacao_com_exemplos(titulo, descricao, resposta_empresa, replica_consumidor=""):
    
    prompt_sistema = f"""
    Você é um Auditor de Moderação do Reclame AQUI. Sua tarefa é prever se um pedido de moderação na categoria "A empresa não violou o direito do cliente" será ACEITO ou NEGADO.

    [DIRETRIZES DE SUCESSO (BASEADO EM CASOS REAIS ACEITOS)]
    - O pedido será ACEITO se a empresa provar matematicamente ou via regulamento que seguiu o padrão, e o cliente apenas demonstrar insatisfação subjetiva (ex: formato de pontuação qualificável).
    - O pedido será ACEITO se o cliente admitir que perdeu prazos (ex: testar produto após o 7º dia) ou causou o próprio problema (ex: perdeu o voo por causa do trânsito).
    - O pedido será ACEITO se a resposta da empresa for cirúrgica, citando cláusulas exatas (ex: Item 7.8 do Regulamento) que desmentem a premissa do cliente sem margem para dupla interpretação.

    [DIRETRIZES DE REJEIÇÃO (BASEADO EM CASOS REAIS NEGADOS)]
    - O pedido será NEGADO (CO06 - Divergência) se houver bate-boca de fatos não comprováveis publicamente (ex: cliente diz que contratou em 2026 e empresa diz que foi em 2023, ou cliente diz que foi cobrado e empresa diz que estornou).
    - O pedido será NEGADO se o cliente colocar no texto qualquer menção a "Falha no Atendimento" (demora no chat, telefone que caiu, promessa errada de atendente).

    DADOS DO CASO ATUAL:
    - TÍTULO: {titulo}
    - DESCRIÇÃO: {descricao}
    - RESPOSTA DA EMPRESA: {resposta_empresa}
    - RÉPLICA DO CONSUMIDOR: {replica_consumidor}

    Retorne uma análise estruturada em formato JSON:
    {{
        "veredito_previso": "ACEITO" ou "NEGADO",
        "carimbo_provavel": "Nenhum", "CO01" ou "CO06",
        "chance_sucesso_percentual": 85,
        "justificativa_com_base_no_manual": "Sua explicação detalhada aqui."
    }}
    """

    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content(prompt_sistema)
    return response.text
