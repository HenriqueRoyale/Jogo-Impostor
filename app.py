import streamlit as st
import random

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Impostor Ultimate", page_icon="🕵️", layout="centered")

# --- CSS CUSTOMIZADO PARA DESIGN PREMIUM ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #0e1117; }
    
    .stButton>button {
        width: 100%; border-radius: 12px; height: 3.8em;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        color: white; font-weight: 800; border: none; transition: all 0.4s ease;
        text-transform: uppercase; letter-spacing: 1px;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 10px 25px rgba(168, 85, 247, 0.4); color: white; }

    .custom-card {
        background: rgba(255, 255, 255, 0.03); border-radius: 20px;
        padding: 30px; border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(12px); margin-bottom: 25px; text-align: center;
    }
    
    .reveal-box {
        padding: 40px; border-radius: 20px; text-align: center;
        margin-top: 20px; border: 2px solid;
    }

    h1, h2, h3 { color: #ffffff; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- BANCO DE DADOS GIGANTE (MISTURA DE TUDO) ---
if 'temas' not in st.session_state:
    st.session_state.temas = {
        "🏛️ História e Política (Hard)": {
            "Código de Hamurabi": "Jurisprudência Antiga", "Guerra Fria": "Equilíbrio de Poder", 
            "Revolução Industrial": "Mecanização Social", "Apartheid": "Divisão Institucional",
            "Queda de Constantinopla": "Ponto de Inflexão Histórico"
        },
        "🌌 Ciência e Cosmos (Hard)": {
            "Matéria Escura": "Componente Invisível", "Teoria das Cordas": "Vibrações Fundamentais",
            "Entropia": "Degradação de Energia", "Fissão Nuclear": "Ruptura de Núcleo",
            "Paradoxo de Fermi": "Probabilidade de Contato"
        },
        "🧠 Filosofia e Psique (Hard)": {
            "Niilismo": "Negação de Valores", "Efeito Mandela": "Distorção Coletiva",
            "Mito da Caverna": "Percepção da Realidade", "Dilema do Prisioneiro": "Estratégia de Cooperação",
            "Imperativo Categórico": "Ética Universal"
        },
        "🎨 Arte e Cultura": {
            "Surrealismo": "Lógica do Sonho", "Guernica": "Expressão de Conflito",
            "Antropofagia": "Assimilação Cultural", "Bauhaus": "União de Forma e Função",
            "Renascimento": "Valorização Humana"
        },
        "🌍 Lugares do Mundo": {
            "Tóquio": "Metrópole Asiática", "Rio de Janeiro": "Cidade Costeira", "Paris": "Referência Europeia",
            "Egito": "Berço Civilizatório", "Islândia": "Ilha Geológica", "Machu Picchu": "Ruínas de Altitude"
        },
        "🍕 Gastronomia": {
            "Sushi": "Culinária Oriental", "Trufa Negra": "Especiaria Subterrânea", "Foie Gras": "Prato de Luxo",
            "Ceviche": "Preparo Marinado", "Churrasco": "Tradição de Fogo", "Pizza": "Base de Massa"
        },
        "🦸 Super-Heróis": {
            "Batman": "Vigilante Noturno", "Homem de Ferro": "Gênio Tecnológico", "Thor": "Divindade Guerreira",
            "Pantera Negra": "Realeza Africana", "Coringa": "Agente do Caos"
        },
        "🎥 Entretenimento": {
            "Harry Potter": "Universo de Magia", "Interestelar": "Exploração do Tempo", "The Office": "Ambiente Corporativo",
            "Star Wars": "Conflito Galáctico", "Stranger Things": "Nostalgia Sobrenatural"
        },
        "💻 Tecnologia": {
            "Bitcoin": "Ativo Digital", "Inteligência Artificial": "Processamento Cognitivo", "Metaverso": "Ambiente Virtual",
            "Linux": "Sistema Aberto", "Tesla": "Mobilidade Elétrica"
        },
        "⚽ Esportes": {
            "Natação": "Atividade Aquática", "Basquete": "Dinâmica de Salto", "Tênis": "Duelo de Impacto",
            "Golfe": "Precisão em Campo", "Futebol": "Competição de Massa"
        }
    }

# --- ESTADOS DO JOGO ---
if 'etapa' not in st.session_state: st.session_state.etapa = "config"
if 'jogador_atual' not in st.session_state: st.session_state.jogador_atual = 0
if 'mostrar_palavra' not in st.session_state: st.session_state.mostrar_palavra = False

def iniciar_jogo(nomes, num_impostores, temas_escolhidos):
    tema_final = random.choice(temas_escolhidos)
    palavra = random.choice(list(st.session_state.temas[tema_final].keys()))
    dica = st.session_state.temas[tema_final][palavra]
    indices_impostores = random.sample(range(len(nomes)), num_impostores)
    
    st.session_state.jogo = {
        "nomes": nomes, "tema": tema_final, "palavra": palavra,
        "dica_impostor": dica, "impostores": indices_impostores
    }
    st.session_state.etapa = "revelacao"
    st.session_state.jogador_atual = 0

# --- TELAS ---
st.markdown("<h1 style='text-align: center; color: #6366f1;'>🕵️ IMPOSTOR <span style='color: #a855f7;'>ULTIMATE</span></h1>", unsafe_allow_html=True)

# TELA 1: CONFIGURAÇÃO
if st.session_state.etapa == "config":
    st.markdown("<div class='custom-card'><h3>Setup da Partida</h3></div>", unsafe_allow_html=True)
    
    # Opção de selecionar temas
    todos_temas = list(st.session_state.temas.keys())
    temas_selecionados = st.multiselect("Selecione os Temas:", todos_temas, default=todos_temas)
    
    col1, col2 = st.columns(2)
    num_jogadores = col1.number_input("Jogadores:", 3, 20, 6)
    num_impostores = col2.number_input("Impostores:", 1, num_jogadores-1, 1)
    
    st.markdown("---")
    nomes = []
    cols = st.columns(2)
    for i in range(num_jogadores):
        nome = cols[i % 2].text_input(f"Nome do Player {i+1}", f"Jogador {i+1}", key=f"n_{i}")
        nomes.append(nome)
    
    if st.button("GERAR PARTIDA"):
        if not temas_selecionados: st.error("Selecione pelo menos um tema!")
        else:
            iniciar_jogo(nomes, num_impostores, temas_selecionados)
            st.rerun()

# TELA 2: REVELAÇÃO
elif st.session_state.etapa == "revelacao":
    idx = st.session_state.jogador_atual
    nome = st.session_state.jogo["nomes"][idx]
    
    st.markdown(f"<div class='custom-card'><h2>{nome}</h2><p>Receba o dispositivo e mantenha o sigilo.</p></div>", unsafe_allow_html=True)

    if not st.session_state.mostrar_palavra:
        if st.button("VER IDENTIDADE"):
            st.session_state.mostrar_palavra = True
            st.rerun()
    else:
        if idx in st.session_state.jogo["impostores"]:
            st.markdown(f"""
                <div class='reveal-box' style='background: rgba(255, 75, 75, 0.1); border-color: #ff4b4b;'>
                    <h2 style='color: #ff4b4b;'>🕵️ VOCÊ É O IMPOSTOR</h2>
                    <p style='color: #eee;'>Tema: {st.session_state.jogo['tema']}</p>
                    <h1 style='font-size: 2.2em; color: white;'>{st.session_state.jogo['dica_impostor']}</h1>
                    <small style='color: #888;'>Blefe com base neste conceito!</small>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class='reveal-box' style='background: rgba(0, 200, 83, 0.1); border-color: #00c853;'>
                    <h2 style='color: #00c853;'>✅ VOCÊ É CIDADÃO</h2>
                    <p style='color: #eee;'>Tema: {st.session_state.jogo['tema']}</p>
                    <h1 style='font-size: 2.2em; color: white;'>{st.session_state.jogo['palavra']}</h1>
                    <small style='color: #888;'>Dê sua dica sem entregar a palavra!</small>
                </div>
            """, unsafe_allow_html=True)
            
        if st.button("ENTENDI"):
            st.session_state.mostrar_palavra = False
            if st.session_state.jogador_atual < len(st.session_state.jogo["nomes"]) - 1:
                st.session_state.jogador_atual += 1
            else: st.session_state.etapa = "discussao"
            st.rerun()

# TELA 3: DISCUSSÃO
elif st.session_state.etapa == "discussao":
    st.markdown(f"""
        <div class='custom-card'>
            <h1 style='color: #a855f7;'>🗣️ DISCUSSÃO ATIVA</h1>
            <p>O tema sorteado foi:</p>
            <div style='background: #6366f1; color: white; display: inline-block; padding: 12px 35px; border-radius: 50px; font-weight: bold; font-size: 1.2em;'>
                {st.session_state.jogo['tema']}
            </div>
            <p style='margin-top:25px; color: #888;'>Tentem identificar o impostor pelas dicas!</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("FINALIZAR E REINICIAR"):
        st.session_state.etapa = "config"
        st.rerun()
