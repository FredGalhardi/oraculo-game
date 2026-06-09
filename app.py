import streamlit as st
import random
import time

# --- DADOS DO JOGO (CONTEÚDO CRIATIVO & ANIMADO) ---
GAME_DATA = {
    "Mansão Noir": {
        "desc": "🕵️‍♂️ Um mistério clássico de assassinato cheio de drama, segredos e acusações dramáticas na alta sociedade!",
        "roles": {"bad": "Assassino(a) VIP", "special": "Detetive Astuto(a)", "normal": "Inocente da Festa"},
        "hints": {
            "Assassino(a) VIP": "🤫 Você envenenou o drink do Lorde! Minta descaradamente, invente risadas falsas e jogue a culpa em quem estiver mais nervoso na mesa!",
            "Detetive Astuto(a)": "🔍 Você achou uma pista crucial! A porta estava trancada por dentro. O culpado está 100% nesta mesa fingindo demência!",
            "Inocente da Festa": "😇 Você estava apenas curtindo a pista de dança. Seu objetivo é sobreviver aos olhares tortos e desmascarar o traidor!"
        },
        "rounds": [
            {"fact": "📢 FATO PÚBLICO: O relógio cuco da biblioteca parou exatamente à meia-noite... a hora exata do crime!", "secret": "O corpo exalava um leve perfume de amêndoas e champanhe caro. Veneno puro!"},
            {"fact": "📢 FATO PÚBLICO: Uma taça de cristal caríssima foi encontrada estraçalhada bem perto do tapete principal.", "secret": "Havia uma marca gritante de batom ou óleo de charuto na borda de uma taça intacta ao lado."},
            {"fact": "📢 FATO PÚBLICO: O testamento da vítima foi alterado misteriosamente na tarde de ontem!", "secret": "Alguém aqui na mesa gastou até o que não tinha essa semana e precisava dessa herança urgente!"}
        ]
    },
    "Sabotagem na Firma": {
        "desc": "🚀 Caos corporativo cômico! Alguém simplesmente deletou o banco de dados de produção em plena sexta-feira 17h!",
        "roles": {"bad": "Sabotador(a) do Café", "special": "Diretor(a) de T.I.", "normal": "Colaborador(a) Dedicado(a)"},
        "hints": {
            "Sabotador(a) do Café": "😈 Você rodou o comando proibido e tentou culpar o estagiário! Finja indignação e fale termos técnicos difíceis para confundir a mesa!",
            "Diretor(a) de T.I.": "💻 Você manja dos logs! Alguém usou um acesso remoto suspeito bem na hora da queda. Investigue quem estava no celular nesse horário!",
            "Colaborador(a) Dedicado(a)": "☕ Você só queria bater o ponto e ir tomar uma cerveja! Ajude a achar quem estragou o fim de semana do time!"
        },
        "rounds": [
            {"fact": "📢 FATO PÚBLICO: O servidor caiu exatamente às 16h45, logo após o e-mail de 'bom fim de semana'.", "secret": "Curiosamente, apenas a tabela com as notas de avaliação da chefia foi apagada!"},
            {"fact": "📢 FATO PÚBLICO: A cafeteira expressa explodiu na mesma hora, criando uma fumaça na cozinha.", "secret": "Alguém passou correndo pelo corredor segurando um notebook e suando frio de nervoso!"},
            {"fact": "📢 FATO PÚBLICO: O crachá do RH foi encontrado jogado perto da lixeira.", "secret": "O comando de exclusão foi disparado de um sistema operacional que quase ninguém usa na firma."}
        ]
    },
    "A Ressaca": {
        "desc": "🍻 Baseado em fatos reais! Vocês acordaram após a melhor festa do ano, mas a chave da casa SUMIU. Ninguém sai até descobrir quem fez a arte!",
        "roles": {"bad": "Inimigo(a) do Fim", "special": "Amigo(a) Paranoico(a)", "normal": "Mente em Branco"},
        "hints": {
            "Inimigo(a) do Fim": "🤪 Você jogou a chave pela janela achando que era um frisbee mágico! Agora disfarce, segure o riso e finja que também está procurando!",
            "Amigo(a) Paranoico(a)": "👀 Você não bebeu quase nada e tem certeza absoluta de que alguém escondeu a chave de propósito para a festa não acabar!",
            "Mente em Branco": "🧠 Sua cabeça está explodindo, você só lembra de cantar no karaokê e quer muito a sua cama. Descubra quem sumiu com a chave!"
        },
        "rounds": [
            {"fact": "📢 FATO PÚBLICO: A porta principal tá trancada, mas a janela da cozinha amanheceu escancarada.", "secret": "Pistas na grama! Há marcas de passos na terra logo abaixo da janela da cozinha... pegadas suspeitas!"},
            {"fact": "📢 FATO PÚBLICO: O cachorro do vizinho não parou de latir para o telhado desde as 3 da manhã.", "secret": "Há um boné ou acessório de alguém da mesa jogado bem embaixo do sofá da sala."},
            {"fact": "📢 FATO PÚBLICO: Alguém atacou a geladeira de madrugada e comeu o bolo de aniversário inteiro.", "secret": "O(A) grande culpado(a) foi visto(a) cochilando em pé perto do corredor antes de todo mundo apagar!"}
        ]
    }
}

# --- CONFIGURAÇÃO DA PÁGINA (OTIMIZADO PARA MOBILE) ---
st.set_page_config(
    page_title="Oráculo Festivo", 
    page_icon="🥳", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS CUSTOMIZADO: MODO ESCURO VIBRANTE + ALTA LEGIBILIDADE ---
st.markdown("""
<style>
    /* Forçar fundo super escuro e moderno estilo balada */
    .stApp {
        background: linear-gradient(180deg, #0D0A1C 0%, #160F29 100%) !important;
    }
    
    /* Garantir que TODO texto padrão seja branco puro, sem letras pretas */
    h1, h2, h3, h4, h5, h6, p, span, label, li, div {
        color: #FFFFFF !important;
        font-family: 'Helvetica Neue', Arial, sans-serif;
    }
    
    /* Inputs, Textareas e Selectboxes com alta visibilidade e texto claro */
    .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        background-color: #241B45 !important;
        color: #FFFFFF !important;
        border: 2px solid #7B2CBF !important;
        font-size: 16px !important;
    }
    
    /* Títulos Estilizados e Alegres */
    .main-title {
        font-size: 32px !important; 
        font-weight: 900 !important; 
        text-align: center; 
        color: #00F5D4 !important; /* Neon Mint */
        text-shadow: 0px 0px 12px rgba(0, 245, 212, 0.6);
        margin-bottom: 5px;
    }
    .subtitle {
        font-size: 16px !important;
        text-align: center;
        color: #FF007F !important; /* Neon Pink */
        font-weight: bold;
        margin-bottom: 25px;
    }
    
    /* Caixas de Informação Estilo 'Card de Jogo' */
    .secret-card { 
        background: linear-gradient(135deg, #4F0026 0%, #2A0013 100%); 
        padding: 22px; 
        border-radius: 16px; 
        border: 3px solid #FF007F; 
        text-align: center;
        box-shadow: 0px 0px 20px rgba(255, 0, 127, 0.4);
        margin: 15px 0;
    }
    .public-card { 
        background: linear-gradient(135deg, #0A2647 0%, #144272 100%); 
        padding: 22px; 
        border-radius: 16px; 
        border: 3px solid #00F5D4; 
        text-align: center;
        box-shadow: 0px 0px 20px rgba(0, 245, 212, 0.3);
        margin: 15px 0;
    }
    
    /* BOTÕES GIGANTES: Perfeitos para o dedão no celular durante a resenha */
    div.stButton > button { 
        height: 65px !important; 
        font-size: 18px !important; 
        font-weight: bold !important;
        border-radius: 15px !important; 
        background: linear-gradient(90deg, #7B2CBF 0%, #9D4EDD 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        box-shadow: 0px 6px 15px rgba(157, 78, 221, 0.4) !important;
        transition: transform 0.1s ease-in-out;
    }
    div.stButton > button:active {
        transform: scale(0.96);
    }
    /* Botões Primários com Destaque Neon Rosa */
    div.stButton > button[data-testid="stBaseButton-primary"] {
        background: linear-gradient(90deg, #FF007F 0%, #FF5E00 100%) !important;
        box-shadow: 0px 6px 20px rgba(255, 0, 127, 0.5) !important;
    }
</style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO ROBUSTA DO ESTADO DO JOGO ---
def init_game_state():
    state_keys = {
        'phase': 'setup',
        'players': [],
        'context': '',
        'roles': {},
        'current_player_idx': 0,
        'show_secret': False,
        'round_num': 0,
        'readers': [],
        'show_round_secret': False
    }
    for key, val in state_keys.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_game_state()

# --- SORTEIO DINÂMICO E ASSETRIA ---
def shuffle_and_assign(players, context):
    random.shuffle(players)
    roles_config = GAME_DATA[context]['roles']
    assigned = {}
    
    # 1 Vilão, 1 Especial, resto Inocente/Normal
    assigned[players[0]] = roles_config['bad']
    assigned[players[1]] = roles_config['special']
    for p in players[2:]:
        assigned[p] = roles_config['normal']
        
    return assigned

# --- TELA 1: CONFIGURAÇÃO ENÉRGICA ---
def render_setup():
    st.markdown("<p class='main-title'>🔮 ORÁCULO NEON 🔮</p>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>O Party Game Definitivo para sua Roda de Amigos!</p>", unsafe_allow_html=True)
    
    st.markdown("### 👥 1. Quem vai jogar?")
    players_raw = st.text_area(
        "Digite os nomes (um por linha):", 
        height=140, 
        placeholder="Ex:\nLucas\nBeatriz\nThiago\nAmanda"
    )
    players = [p.strip() for p in players_raw.split('\n') if p.strip()]
    
    if len(players) > 0:
        st.markdown(f"🎉 **{len(players)} jogadores prontos para a diversão!** (Mínimo 3, Máximo 8)")
    
    st.markdown("### 🌆 2. Escolha o Cenário da Rodada")
    context = st.selectbox("", list(GAME_DATA.keys()))
    
    # Caixa informativa estilizada e clara
    st.markdown(f"""
    <div style='background-color: #1A1235; padding: 15px; border-radius: 12px; border-left: 5px solid #00F5D4; margin-bottom: 20px;'>
        <p style='margin:0; font-size:15px; line-height:1.4;'>{GAME_DATA[context]['desc']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔥 INICIAR JOGO DETONANTE!", use_container_width=True, type="primary"):
        if len(players) < 3:
            st.error("🚨 Opa! Chame pelo menos 3 amigos para a brincadeira começar!")
        elif len(players) > 8:
            st.error("🚨 Limite máximo de 8 jogadores para não virar bagunça na mesa!")
        elif len(set(players)) != len(players):
            st.error("🚨 Tem nomes repetidos aí! Coloque um sobrenome ou apelido para diferenciar.")
        else:
            st.session_state.players = players
            st.session_state.context = context
            st.session_state.roles = shuffle_and_assign(players, context)
            st.session_state.phase = 'distribution'
            st.rerun()

# --- TELA 2: DISTRIBUIÇÃO - PASSA-PASSA (ANTI-SPOILER) ---
def render_distribution():
    idx = st.session_state.current_player_idx
    players = st.session_state.players
    
    if idx >= len(players):
        st.markdown("<p class='main-title'>🎉 TUDO PRONTO! 🎉</p>", unsafe_allow_html=True)
        st.markdown("<p class='center-text' style='text-align:center; font-size:18px;'>Todos já sabem seus papéis secretos. Coloque o celular no centro da mesa!</p>", unsafe_allow_html=True)
        st.write("")
        if st.button("🚀 COMEÇAR RODADA 1", use_container_width=True, type="primary"):
            st.session_state.phase = 'rounds'
            st.rerun()
        return

    current_player = players[idx]
    
    st.markdown("<p class='main-title'>🎭 IDENTIDADES SECRETAS</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; font-size: 20px;'>📱 Passe o celular para: <br><b style='color:#00F5D4; font-size:28px;'>{current_player}</b></p>", unsafe_allow_html=True)
    st.write("")
    
    if not st.session_state.show_secret:
        if st.button(f"👀 Ver Meu Papel Secreto", use_container_width=True):
            st.session_state.show_secret = True
            st.rerun()
    else:
        role = st.session_state.roles[current_player]
        hint = GAME_DATA[st.session_state.context]['hints'][role]
        
        st.markdown(f"""
        <div class='secret-card'>
            <h3 style='color: #FF007F !important; margin-top:0;'>✨ Seu Papel é: {role}</h3>
            <p style='font-size: 16px; font-style: italic; margin-bottom:0;'>{hint}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<p style='text-align:center; color:#FF5E00 !important; font-weight:bold;'>⚠️ Memorize e não deixe ninguém ver a tela!</p>", unsafe_allow_html=True)
        
        if st.button("🙈 Esconder e Passar Próximo", use_container_width=True, type="primary"):
            st.session_state.show_secret = False
            st.session_state.current_player_idx += 1
            st.rerun()

# --- TELA 3: AS RODADAS DE DEBATE E CAOS ---
def render_rounds():
    round_idx = st.session_state.round_num
    context_data = GAME_DATA[st.session_state.context]
    
    if round_idx >= 3:
        st.session_state.phase = 'voting'
        st.rerun()
        return
        
    st.markdown(f"<p class='main-title'>🔥 RODADA {round_idx + 1} DE 3 🔥</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#9D4EDD !important; font-weight:bold;'>📱 CELULAR NO CENTRO DA MESA PARA TODOS VEREM!</p>", unsafe_allow_html=True)
    
    # Card do Fato Público (Texto super visível)
    st.markdown(f"""
    <div class='public-card'>
        <h4 style='color: #00F5D4 !important; margin-top:0; font-size:18px;'>📢 REVELAÇÃO DO ORÁCULO</h4>
        <p style='font-size:16px; margin-bottom:0; font-weight:500;'>{context_data['rounds'][round_idx]['fact']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Definir os dois sortudos que lerão a pista
    if not st.session_state.readers:
        st.session_state.readers = random.sample(st.session_state.players, 2)
    
    p1, p2 = st.session_state.readers[0], st.session_state.readers[1]
    
    st.write("")
    
    if not st.session_state.show_round_secret:
        st.markdown("<p style='text-align:center; font-size:15px;'>Uma pista assimétrica exclusiva apareceu!</p>", unsafe_allow_html=True)
        if st.button(f"🤫 Apenas {p1} e {p2}: Cliquem Aqui", use_container_width=True):
            st.session_state.show_round_secret = True
            st.rerun()
    else:
        st.markdown(f"""
        <div class='secret-card'>
            <h4 style='color: #FF007F !important; margin-top:0;'>🤫 Pista Exclusiva para {p1} e {p2}</h4>
            <p style='font-size:15px; margin-bottom:0;'>{context_data['rounds'][round_idx]['secret']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Ok, Lemos! Esconder e Debater 🗣️", use_container_width=True):
            st.session_state.show_round_secret = False
            st.rerun()
            
    st.divider()
    
    # Cronômetro visual animado para pressionar a mesa
    st.markdown("<h3 style='text-align:center;'>⏱️ 3 Minutos de Debate Intenso!</h3>", unsafe_allow_html=True)
    
    timer_placeholder = st.empty()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ Iniciar Timer", use_container_width=True):
            with timer_placeholder:
                bar = st.progress(0)
                # Escalonado rápido de 10s para testes fluidos no MVP. Para 3min reais, use sleep mais longo ou lógica de datetime.
                for i in range(100):
                    time.sleep(0.06) 
                    bar.progress(i + 1)
                st.markdown("<p style='color:#FF007F !important; font-weight:bold; font-size:20px; text-align:center;'>🚨 O TEMPO ACABOU! ACUSEM!</p>", unsafe_allow_html=True)
    with col2:
        if st.button("Próxima Rodada ⏭️", use_container_width=True, type="primary"):
            st.session_state.round_num += 1
            st.session_state.readers = [] 
            st.session_state.show_round_secret = False
            st.rerun()

# --- TELA 4: VEREDITO FINAL E FESTA DO RESULTADO ---
def render_voting():
    st.markdown("<p class='main-title'>⚖️ HORA DO VEREDITO ⚖️</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:16px;'>Discutam, debatam e cheguem a um consenso na mesa:</p>", unsafe_allow_html=True)
    
    # Selectbox estilizado
    suspect = st.selectbox("Quem a mesa vai apontar como o grande culpado?", ["(Escolha um jogador da mesa)"] + st.session_state.players)
    
    if suspect != "(Escolha um jogador da mesa)":
        st.write("")
        if st.button("🚨 REVELAR A VERDADE ABSOLUTA!", use_container_width=True, type="primary"):
            st.divider()
            
            bad_role_name = GAME_DATA[st.session_state.context]['roles']['bad']
            real_culprit = [p for p, role in st.session_state.roles.items() if role == bad_role_name][0]
            
            if suspect == real_culprit:
                st.markdown(f"""
                <div style='background-color: #004D40; padding: 25px; border-radius: 16px; border: 3px solid #00F5D4; text-align:center; box-shadow: 0 0 25px rgba(0,245,212,0.5);'>
                    <h2 style='color:#00F5D4 !important; margin-top:0;'>🎉 VITÓRIA DA MESA! 🎉</h2>
                    <p style='font-size:18px; margin-bottom:0;'>Vocês desmascararam <b>{real_culprit}</b>, que realmente era o(a) <b>{bad_role_name}</b>!</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style='background-color: #4A0E17; padding: 25px; border-radius: 16px; border: 3px solid #FF007F; text-align:center; box-shadow: 0 0 25px rgba(255,0,127,0.5);'>
                    <h2 style='color:#FF007F !important; margin-top:0;'>💀 FIM DE JOGO! O MAL VENCEU! 💀</h2>
                    <p style='font-size:18px;'>Vocês condenaram o inocente <b>{suspect}</b>!</p>
                    <p style='font-size:18px; margin-bottom:0; font-weight:bold; color:#00F5D4 !important;'>O verdadeiro {bad_role_name} era: {real_culprit}!</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Tabela final de Revelação
            st.markdown("<h3 style='margin-top:30px; text-align:center;'>📋 Papéis de Todo Mundo:</h3>", unsafe_allow_html=True)
            for p, role in st.session_state.roles.items():
                st.markdown(f"• **{p}**: {role}")
                
            st.write("")
            if st.button("🔄 Jogar Outra Partida!", use_container_width=True):
                st.session_state.clear()
                st.rerun()

# --- ROTEADOR PRINCIPAL ---
def main():
    if st.session_state.phase == 'setup':
        render_setup()
    elif st.session_state.phase == 'distribution':
        render_distribution()
    elif st.session_state.phase == 'rounds':
        render_rounds()
    elif st.session_state.phase == 'voting':
        render_voting()

if __name__ == "__main__":
    main()
