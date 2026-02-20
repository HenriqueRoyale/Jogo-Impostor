import streamlit as st
import random

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Impostor Elite", page_icon="🕵️", layout="centered")

# --- CSS CUSTOMIZADO PARA DESIGN MODERNO ---
st.markdown("""
    <style>
    /* Fundo e Fonte */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }

    /* Estilo dos Botões */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3em;
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%);
        color: white;
        font-weight: bold;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(168, 85, 247, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(168, 85, 247, 0.6);
        color: white;
    }

    /* Cards de Informação (Glassmorphism) */
    .custom-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        margin-bottom: 20px;
        text-align: center;
    }

    /* Esconder o menu do Streamlit para parecer App nativo */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- BANCO DE DADOS ATUALIZADO ---
if 'temas' not in st.session_state:
    st.session_state.temas = {
        "🌍 Geografia": {"Japão": "Ásia", "Brasil": "América Latina", "Egito": "Pirâmides", "Islândia": "Gelo e Fogo", "Dubai": "Luxo"},
        "🍕 Gastronomia": {"Sushi": "Peixe Cru", "Fondue": "Queijo/Chocolate", "Taco": "Tortilha", "Strogonoff": "Champignon", "Croissant": "França"},
        "🦸 Super-Heróis": {"Batman": "Morcego", "Thor": "Martelo", "Coringa": "Riso", "Homem-Aranha": "Teia", "Pantera Negra": "Wakanda"},
        "🎥 Cinema": {"Inception": "Sonhos", "Interestelar": "Buraco Negro", "Tropa de Elite": "Operações", "Coringa": "Vilão", "Parasita": "Coreia"},
        "💻 Tecnologia": {"ChatGPT": "IA", "Bitcoin": "Moeda", "Metaverso": "Realidade Virtual", "Steve Jobs": "Apple", "Linux": "Pinguim"},
        "🧠 Mitologia": {"Zeus": "Raios", "Medusa": "Cobras", "Anúbis": "Chacal", "Thor": "Nórdico", "Afrodite": "Amor"},
        "🎸 Música": {"Beatles": "Quarteto", "Freddie Mercury": "Queen", "Beyoncé": "Diva", "Daft Punk": "Capacete", "Nirvana": "Grunge"}
    }

# --- LÓGICA DO JOGO ---
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

# TÍTULO PRINCIPAL
st.markdown("<h1 style='text-align: center; color: #6366f1;'>🕵️ IMPOSTOR <span style='color: #a855f7;'>ELITE</span></h1>", unsafe_allow_html=True)

if st.session_state.etapa == "config":
    st.markdown("<div class='custom-card'><h3>Configurações da Partida</h3></div>", unsafe_allow_html=True)
    
    temas_selecionados = st.multiselect("Selecione os Temas:", list(st.session_state.temas.keys()), default=list(st.session_state.temas.keys()))
    
    col1, col2 = st.columns(2)
    num_jogadores = col1.number_input("Jogadores:", 3, 20, 6)
    num_impostores = col2.number_input("Impostores:", 1, num_jogadores-1, 1)
    
    st.markdown("---")
    nomes = []
    cols = st.columns(2)
    for i in range(num_jogadores):
        nome = cols[i % 2].text_input(f"Nome Jogador {i+1}", f"Jogador {i+1}", key=f"n_{i}")
        nomes.append(nome)
    
    if st.button("INICIAR MISSÃO"):
        if not temas_selecionados: st.error("Selecione ao menos um tema!")
        else:
            iniciar_jogo(nomes, num_impostores, temas_selecionados)
            st.rerun()

elif st.session_state.etapa == "revelacao":
    progresso = (st.session_state.jogador_atual) / len(st.session_state.jogo["nomes"])
    st.progress(progresso)
    
    idx = st.session_state.jogador_atual
    nome = st.session_state.jogo["nomes"][idx]
    
    st.markdown(f"""
        <div class='custom-card'>
            <h2 style='margin:0;'>Vez de {nome}</h2>
            <p style='color: #888;'>Passe o aparelho para esta pessoa.</p>
        </div>
    """, unsafe_allow_html=True)

    if not st.session_
