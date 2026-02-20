import streamlit as st
import random

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Impostor Web", page_icon="🕵️", layout="centered")

# --- BANCO DE DADOS AMPLIADO ---
if 'temas' not in st.session_state:
    st.session_state.temas = {
        "Países": {"Japão": "Ásia", "Brasil": "América Latina", "França": "Europa", "Egito": "África", "Canadá": "América do Norte", "Austrália": "Oceania"},
        "Comidas": {"Pizza": "Massa", "Sushi": "Peixe", "Hambúrguer": "Fast-food", "Lasanha": "Itália", "Churrasco": "Carne", "Taco": "México"},
        "Profissões": {"Médico": "Saúde", "Astronauta": "Espaço", "Bombeiro": "Emergência", "Professor": "Educação", "Advogado": "Justiça", "Cozinheiro": "Restaurante"},
        "Animais": {"Leão": "Felino", "Tubarão": "Oceano", "Elefante": "Savana", "Águia": "Céu", "Cobra": "Rastejante", "Pinguim": "Gelo"},
        "Super-heróis": {"Batman": "Morcego", "Homem de Ferro": "Tecnologia", "Superman": "Capa", "Homem-Aranha": "Teia", "Thor": "Martelo", "Hulk": "Verde"},
        "Séries e Filmes": {"Stranger Things": "Anos 80", "Harry Potter": "Magia", "Vingadores": "Heróis", "The Office": "Escritório", "Titanic": "Navio", "Star Wars": "Galáxia"},
        "Esportes": {"Futebol": "Campo", "Basquete": "Cesta", "Vôlei": "Rede", "Tênis": "Raquete", "Natação": "Piscina", "Golfe": "Buraco"},
        "Cidades": {"Nova York": "EUA", "Paris": "França", "Roma": "Itália", "Tóquio": "Japão", "Rio de Janeiro": "Brasil", "Londres": "Inglaterra"},
        "Objetos": {"Celular": "Eletrônico", "Relógio": "Tempo", "Óculos": "Visão", "Mochila": "Viagem", "Chave": "Porta", "Guarda-chuva": "Chuva"},
        "Disney e Pixar": {"Toy Story": "Brinquedos", "Procurando Nemo": "Peixe", "Shrek": "Ogro", "Frozen": "Gelo", "Carros": "Corrida", "Monstros S.A": "Susto"},
        "Tecnologia": {"Google": "Busca", "Apple": "Iphone", "Netflix": "Streaming", "Tesla": "Carro Elétrico", "WhatsApp": "Mensagem", "Instagram": "Fotos"},
        "Corpo Humano": {"Coração": "Órgão Vital", "Cérebro": "Pensamento", "Pulmão": "Respiração", "Fígado": "Digestão", "Esqueleto": "Ossos", "Pele": "Tato"},
        "Mitologia Grega": {"Zeus": "Olimpo", "Poseidon": "Mares", "Hades": "Submundo", "Hércules": "Força", "Afonso": "Sabedoria", "Medusa": "Serpentes"},
        "Marcas Famosas": {"Nike": "Esporte", "Coca-Cola": "Refrigerante", "McDonalds": "Lanche", "Ferrari": "Carro Luxo", "Amazon": "Entrega", "Lego": "Blocos"},
        "Desenhos Animados": {"Pica-Pau": "Pássaro", "Tom e Jerry": "Gato e Rato", "Simpsons": "Amarelos", "Bob Esponja": "Fundo do Mar", "Scooby-Doo": "Mistério", "Naruto": "Ninja"}
    }

# --- ESTADOS DO JOGO ---
if 'etapa' not in st.session_state:
    st.session_state.etapa = "config"
if 'jogador_atual' not in st.session_state:
    st.session_state.jogador_atual = 0
if 'mostrar_palavra' not in st.session_state:
    st.session_state.mostrar_palavra = False

# --- FUNÇÕES ---
def iniciar_jogo(nomes, num_impostores, temas_escolhidos):
    tema_final = random.choice(temas_escolhidos)
    palavra = random.choice(list(st.session_state.temas[tema_final].keys()))
    dica = st.session_state.temas[tema_final][palavra]
    
    indices_impostores = random.sample(range(len(nomes)), num_impostores)
    
    st.session_state.jogo = {
        "nomes": nomes,
        "tema": tema_final,
        "palavra": palavra,
        "dica_impostor": dica,
        "impostores": indices_impostores
    }
    st.session_state.etapa = "revelacao"
    st.session_state.jogador_atual = 0

# --- INTERFACE ---
st.title("🕵️ Jogo do Impostor")

if st.session_state.etapa == "config":
    st.subheader("Configurações do Grupo")
    
    # Seleção de Temas
    todos_temas = list(st.session_state.temas.keys())
    temas_selecionados = st.multiselect("Quais temas quer no jogo?", todos_temas, default=todos_temas)
    
    num_jogadores = st.number_input("Número de jogadores", min_value=3, max_value=20, value=6)
    num_impostores = st.number_input("Número de impostores", min_value=1, max_value=num_jogadores-1, value=1)
    
    st.divider()
    nomes = []
    cols = st.columns(2) # Divide em duas colunas para ficar melhor no celular
    for i in range(num_jogadores):
        col_idx = 0 if i % 2 == 0 else 1
        nome = cols[col_idx].text_input(f"Jogador {i+1}", value=f"J{i+1}", key=f"p_{i}")
        nomes.append(nome)
    
    if st.button("GERAR PALAVRAS 🚀", use_container_width=True):
        if not temas_selecionados:
            st.error("Escolha pelo menos um tema!")
        else:
            iniciar_jogo(nomes, num_impostores, temas_selecionados)
            st.rerun()

elif st.session_state.etapa == "revelacao":
    idx = st.session_state.jogador_atual
    nome_da_vez = st.session_state.jogo["nomes"][idx]
    
    st.header(f"Vez de: {nome_da_vez}")
    st.info("Passe o celular para esta pessoa.")

    if not st.session_state.mostrar_palavra:
        if st.button(f"REVELAR MINHA PALAVRA", use_container_width=True):
            st.session_state.mostrar_palavra = True
            st.rerun()
    else:
        with st.container(border=True):
            st.write(f"**TEMA:** {st.session_state.jogo['tema']}")
            if idx in st.session_state.jogo["impostores"]:
                st.error("VOCÊ É O IMPOSTOR! 🕵️")
                st.write(f"Sua dica: **{st.session_state.jogo['dica_impostor']}**")
            else:
                st.success("VOCÊ É UM CIDADÃO! ✅")
                st.write(f"Sua palavra: **{st.session_state.jogo['palavra']}**")
        
        if st.button("OK, PRÓXIMO ➡️", use_container_width=True):
            st.session_state.mostrar_palavra = False
            if st.session_state.jogador_atual < len(st.session_state.jogo["nomes"]) - 1:
                st.session_state.jogador_atual += 1
            else:
                st.session_state.etapa = "discussao"
            st.rerun()

elif st.session_state.etapa == "discussao":
    st.balloons()
    st.header("🗣️ Hora de Debater!")
    st.write(f"O tema sorteado foi: **{st.session_state.jogo['tema']}**")
    st.warning("Cada um deve dar uma dica curta sobre a sua palavra. Depois, votem em quem vocês acham que é o impostor!")
    
    if st.button("JOGAR NOVAMENTE 🔄", use_container_width=True):
        st.session_state.etapa = "config"
        st.rerun()