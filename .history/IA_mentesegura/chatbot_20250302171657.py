import ollama
import torch
import random
from embeddings import generate_embeddings

# Definição das estratégias fixas com múltiplas variações
estrategias = {
    "acolhimento": [
        "Sei que momentos difíceis podem ser desafiadores. O que você está passando é importante e merece atenção.",
        "Entendo que essa situação pode estar sendo difícil para você. Falar sobre isso pode ajudar. Me conte mais, se quiser.",
        "Estou aqui para ouvir e apoiar você. Se quiser compartilhar mais detalhes, ficarei feliz em ajudar."
    ],
    "separacao_vida_trabalho": [
        "Manter um equilíbrio entre trabalho e vida pessoal pode ser difícil. Criar um ritual ao chegar em casa pode ajudar.",
        "Muitas pessoas enfrentam essa dificuldade. Já tentou reservar um momento do dia só para você, sem distrações do trabalho?",
        "Desconectar-se do trabalho pode ser um desafio. Pequenos hábitos, como evitar checar mensagens fora do expediente, podem ajudar."
    ],
    "estresse_trabalho": [
        "Passar por situações estressantes no trabalho pode ser exaustivo. É importante reconhecer o impacto dessas experiências e buscar formas saudáveis de lidar com elas.",
        "Situações de pressão no trabalho fazem parte da rotina, mas encontrar formas de equilibrar esse estresse pode fazer a diferença.",
        "Cada pessoa lida com o estresse de uma forma diferente. Você já experimentou técnicas como respiração profunda ou pequenas pausas para clarear a mente?"
    ],
    "autocuidado": [
        "Cuidar de si mesmo é tão importante quanto cuidar dos outros. O que você faz para se sentir bem?",
        "Dormir bem e se alimentar de forma equilibrada podem ter um grande impacto no seu bem-estar. Como está sua rotina nesses aspectos?",
        "Praticar atividades que trazem prazer pode ser uma forma eficaz de aliviar o estresse. O que você gosta de fazer no seu tempo livre?"
    ],
    "rede_apoio": [
        "Conversar com alguém de confiança pode trazer alívio. Você tem alguém com quem possa compartilhar suas preocupações?",
        "Construir uma rede de apoio é fundamental. Como você se sente ao compartilhar suas experiências com outras pessoas?",
        "Às vezes, falar com colegas que passam por situações semelhantes pode ser reconfortante. Já pensou nisso?"
    ],
    "reflexao_autoconhecimento": [
        "Refletir sobre suas experiências pode ajudar a entender melhor suas emoções. O que você aprendeu sobre si mesmo recentemente?",
        "Autoconhecimento é um processo contínuo. Como você tem se sentido em relação às suas escolhas e ações?",
        "Às vezes, olhar para dentro pode trazer clareza. O que você acha que poderia te ajudar a se sentir melhor?"
    ],
    "motivacao_proposito": [
        "Encontrar um sentido no que você faz pode trazer mais satisfação. O que te motiva no seu trabalho?",
        "Ter metas claras pode ajudar a manter o foco e a motivação. O que você gostaria de alcançar nos próximos meses?",
        "Ressignificar desafios pode trazer uma nova perspectiva. Como você vê as dificuldades que enfrenta atualmente?"
    ],
    "sinais_alerta": [
        "É importante prestar atenção em como você está se sentindo. Você notou alguma mudança recente no seu humor ou comportamento?",
        "Reconhecer sinais de que algo não está bem é o primeiro passo para buscar ajuda. Como você tem lidado com isso?",
        "Às vezes, pequenas mudanças no dia a dia podem indicar que precisamos de mais cuidado. O que você tem observado em si mesmo?"
    ],
    "busca_ajuda_profissional": [
        "Buscar ajuda profissional pode ser um passo importante para cuidar da sua saúde mental. Já considerou essa possibilidade?",
        "Conversar com um psicólogo pode oferecer ferramentas para lidar melhor com as situações que você enfrenta. O que você acha disso?",
        "Cuidar da saúde mental é tão importante quanto cuidar da saúde física. Você já pensou em buscar apoio especializado?"
    ]
}

def get_relevant_context(query, vault_embeddings, vault_content, top_k=3):
    """Recupera os trechos mais relevantes do vault, garantindo que existam embeddings antes de calcular a similaridade."""
    if vault_embeddings.nelement() == 0:
        return []
    
    query_embedding = torch.tensor(ollama.embeddings(model="mxbai-embed-large", prompt=query)["embedding"])
    scores = torch.cosine_similarity(query_embedding.unsqueeze(0), vault_embeddings)
    top_indices = torch.topk(scores, k=min(top_k, len(scores)))[1].tolist()
    return [vault_content[i].strip() for i in top_indices]

def chat_with_llama(query, vault_embeddings, vault_content, conversation_history):
    """Consulta o modelo LLaMA mantendo o histórico e misturando respostas fixas com respostas dinâmicas."""
    
    conversation_history.append({"role": "user", "content": query})

    relevant_context = get_relevant_context(query, vault_embeddings, vault_content)

    # Identifica todas as estratégias mencionadas na pergunta do usuário
    respostas_estrategias = []
    for chave, lista_textos in estrategias.items():
        if chave in query.lower():
            respostas_estrategias.append(random.choice(lista_textos))  # Escolhe aleatoriamente uma variação da resposta fixa

    if respostas_estrategias:
        # Combina todas as estratégias identificadas
        resposta_base = " ".join(respostas_estrategias)

        # Geração de complemento pela IA para tornar a resposta mais personalizada
        full_prompt = f"""
        Você é um assistente empático e acolhedor. O usuário mencionou o seguinte problema:

        "{query}"

        Responda de forma solidária, expandindo a seguinte resposta fixa de forma natural:

        "{resposta_base}"

        Inclua um pequeno complemento motivador ou uma pergunta que incentive o usuário a continuar a conversa.
        """
        
        response = ollama.chat(model="llama3", messages=[{"role": "user", "content": full_prompt}])
        resposta = resposta_base + " " + response["message"]["content"]
    
    else:
        # Geração de resposta padrão com histórico da conversa
        full_prompt = f"""
        Você é um assistente empático e acolhedor, especializado em apoiar pessoas em momentos difíceis.
        Seu objetivo é oferecer sugestões e reflexões que possam ajudar o usuário, sempre de forma acolhedora e sem julgamentos.

        📌 **O que você NÃO deve fazer:**
        - **Não tente diagnosticar ou avaliar o estado emocional do usuário.**
        - **Não mencione escalas psicológicas, transtornos ou termos médicos.**
        - **Não diga "parece que você está passando por X" ou "você pode estar sentindo Y".**

        📌 **O que você DEVE fazer:**
        - **Responda de forma compreensiva e solidária.**
        - **Ofereça sugestões para que o usuário encontre maneiras de melhorar sua situação.**
        - **Mantenha a continuidade da conversa, lembrando o que foi discutido antes.**
        - **Se o usuário mencionar algo da conversa anterior, leve isso em consideração ao responder.**
        - **Se o usuário mencionar uma escolha anterior, responda com base nisso e não inicie um novo tema.**

        **Histórico da conversa até agora**:
        {conversation_history[-4:]}  # Mantém apenas as últimas 4 interações para evitar textos longos.

        **Contexto relevante dos documentos (se aplicável)**:
        {relevant_context}

        **Pergunta do usuário**: {query}
        """
        
        response = ollama.chat(model="llama3", messages=[{"role": "user", "content": full_prompt}])
        resposta = response["message"]["content"]

    # Adiciona a resposta ao histórico para manter a continuidade
    conversation_history.append({"role": "assistant", "content": resposta})
    return resposta
