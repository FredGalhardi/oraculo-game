import streamlit as st
import random
import time

# --- DADOS DO JOGO (CONTEÚDO CRIATIVO) ---
GAME_DATA = {
    "Mansão Noir": {
        "desc": "Mistério clássico de assassinato na alta sociedade.",
        "roles": {"bad": "Assassino", "special": "Detetive", "normal": "Inocente"},
        "hints": {
            "Assassino": "Você envenenou o Lorde Cornwell. Minta, crie álibis falsos e tente culpar os outros.",
            "Detetive": "Você encontrou a porta trancada por dentro. O culpado definitivamente está nesta mesa.",
            "Inocente": "Você estava no salão de festas na hora do crime. Tente sobreviver e descobrir o culpado."
        },
        "rounds": [
            {"fact": "O relógio da biblioteca parou exatamente à meia-noite, hora da morte.", "secret": "O corpo exalava um leve cheiro de amêndoas (típico de cianeto)."},
            {"fact": "Uma taça de cristal foi encontrada quebrada no tapete.", "secret": "Havia uma marca de batom/óleo de charuto na borda da taça intacta ao lado."},
            {"fact": "O testamento do Lorde foi alterado ontem.", "secret": "Alguém da mesa está secretamente falido e precisava de dinheiro."}
        ]
    },
    "Sabotagem na Firma": {
        "desc": "Caos corporativo. Alguém deletou o banco de dados de produção na sexta-feira.",
        "roles": {"bad": "Sabotador", "special": "Gerente de T.I.", "normal": "Funcionário"},
        "hints": {
            "Sabotador": "Você rodou um 'DROP TABLE' sem querer e tentou apagar os logs. Culpe o estagiário.",
            "Gerente de T.I.": "Você tem acesso aos logs do servidor. Alguém usou a VPN de casa para fazer a cagada.",
            "Funcionário": "Você só queria tomar seu café e bater o ponto. Ajude a achar o culpado para poder ir embora."
        },
        "rounds": [
            {"fact": "O sistema caiu exatamente às 16h45 de sexta-feira.", "secret": "Apenas as tabelas de folha de pagamento foram deletadas."},
            {"fact": "A cafeteira quebrou na mesma hora, gerando uma distração.", "secret": "Alguém foi visto saindo correndo da sala dos servidores suando frio."},
            {"fact": "O crachá do estagiário foi clonado.", "secret": "O acesso remoto foi feito a partir de um Mac, e poucos usam Mac na empresa."}
        ]
    },
    "A Ressaca": {
        "desc": "Amigos acordam após uma festa épica e a chave da casa sumiu. Ninguém sai até acharem.",
        "roles": {"bad": "Culpado", "special": "Paranoico", "normal": "Desmemoriado"},
        "hints": {
            "Culpado": "Você jogou a chave pela janela achando que era um morcego. Finja que não lembra de nada.",
            "Paranoico": "Você não bebeu, mas está convencido de que alienígenas roubaram a chave. Dissemine o caos.",
            "Desmemoriado": "Sua cabeça dói muito. Você acordou no chão da cozinha e quer sua cama."
        },
        "rounds": [
            {"fact": "A porta está trancada por dentro e as janelas da sala estão abertas.", "secret": "Alguém encontrou arranhões misteriosos perto da janela do banheiro."},
            {"fact": "O cachorro do vizinho está latindo para o telhado desde as 3h da manhã.", "secret": "Há uma marca de sapato sujo de barro no sofá encostado na janela."},
            {"fact": "A geladeira amanheceu aberta e sem a gaveta de legumes.", "secret": "O Culpado foi a última pessoa vista indo ao banheiro antes de todos apagarem."}
        ]
    }
}

# --- CONFIGURAÇÃO DA PÁGINA E CSS ---
st.set_page_config(page_title="Oráculo: O Jogo", page_icon="👁️", layout="centered")

st.markdown("""
<style>
    .big-font { font-size: 24px !important; font-weight: bold; text-align: center; }
    .center-text { text-align: center; }
    .secret-box { background-color: #2E2E2E; padding: 20px; border-radius: 10px; border: 2px solid #FF4B4B; text-align: center;}
    .public-box { background-color: #1E1E1E; padding: 20px; border-radius: 10px; border: 2px solid #4B9FFF; text-align: center;}
    div.stButton > button { height: 60px; font-size: 18px; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# --- GERENCIAMENTO DE ESTADO ---
def init_state():
    defaults = {
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
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_state()

# --- FUNÇÕES AUXILIARES ---
def assign_roles(players, context):
    random.shuffle(players)
    roles_config = GAME_DATA[context]['roles']
    assigned = {}
    
    assigned[players[0]] = roles_config['bad']
    assigned[players[1]] = roles_config['special']
    for p in players[2:]:
        assigned[p] = roles_config['normal']
        
    return assigned

# --- TELA 1: CONFIGURAÇÃO ---
def render_setup():
    st.markdown("<p class='big-font'>👁️ ORÁCULO 👁️</p>", unsafe_allow_html=True)
    st.markdown("<p class='center-text'>Bem-vindo. O celular a partir de agora é o mestre do jogo.</p>", unsafe_allow_html=True)
    
    st.divider()
    
    # Input de Jogadores
    players_raw = st.text_area("Insira os nomes dos jogadores (um por linha):", height=150, 
                               placeholder="João\nMaria\nCarlos\nAna")
    players = [p.strip() for p in players_raw.split('\n') if p.strip()]
    
    st.write(f"**Total de Jogadores:** {len(players)} (Recomendado: 3 a 8)")
    
    # Seleção de Contexto
    context = st.selectbox("Escolha o Cenário:", list(GAME_DATA.keys()))
    st.info(GAME_DATA[context]['desc'])
    
    if st.button("🎭 INICIAR PARTIDA", use_container_width=True, type="primary"):
        if len(players) < 3:
            st.error("É necessário pelo menos 3 jogadores!")
        elif len(players) > 8:
            st.error("Máximo de 8 jogadores permitidos pelo Oráculo.")
        elif len(set(players)) != len(players):
            st.error("Existem nomes duplicados. Use sobrenomes ou apelidos.")
        else:
            st.session_state.players = players
            st.session_state.context = context
            st.session_state.roles = assign_roles(players, context)
            st.session_state.phase = 'distribution'
            st.rerun()

# --- TELA 2: DISTRIBUIÇÃO DE PAPÉIS ---
def render_distribution():
    idx = st.session_state.current_player_idx
    players = st.session_state.players
    
    if idx >= len(players):
        st.success("Todos os papéis foram distribuídos!")
        if st.button("🔥 Ir para a Rodada 1", use_container_width=True, type="primary"):
            st.session_state.phase = 'rounds'
            st.rerun()
        return

    current_player = players[idx]
    
    st.markdown("<p class='big-font'>Fase de Distribuição</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='center-text'>Passe o celular para <b>{current_player}</b></p>", unsafe_allow_html=True)
    st.divider()
    
    if not st.session_state.show_secret:
        if st.button(f"👀 Sou o(a) {current_player}, revelar meu papel", use_container_width=True):
            st.session_state.show_secret = True
            st.rerun()
    else:
        role = st.session_state.roles[current_player]
        hint = GAME_DATA[st.session_state.context]['hints'][role]
        
        st.markdown(f"""
        <div class='secret-box'>
            <h3>Seu Papel: {role}</h3>
            <p><i>{hint}</i></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.warning("Leia silenciosamente. Não deixe seus vizinhos verem a tela!")
        
        if st.button("🙈 Esconder e Passar o Celular", use_container_width=True, type="primary"):
            st.session_state.show_secret = False
            st.session_state.current_player_idx += 1
            st.rerun()

# --- TELA 3: RODADAS DO ORÁCULO ---
def render_rounds():
    round_idx = st.session_state.round_num
    context_data = GAME_DATA[st.session_state.context]
    
    if round_idx >= 3:
        st.session_state.phase = 'voting'
        st.rerun()
        return
        
    st.markdown(f"<p class='big-font'>🔥 RODADA {round_idx + 1} 🔥</p>", unsafe_allow_html=True)
    st.markdown("<p class='center-text'>Celular no centro da mesa!</p>", unsafe_allow_html=True)
    
    # Fato Público
    st.markdown(f"""
    <div class='public-box'>
        <h4>📢 Fato Público</h4>
        <p>{context_data['rounds'][round_idx]['fact']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    # Selecionar 2 leitores da pista secreta (se não definidos para a rodada atual)
    if not st.session_state.readers:
        st.session_state.readers = random.sample(st.session_state.players, 2)
    
    p1, p2 = st.session_state.readers[0], st.session_state.readers[1]
    
    if not st.session_state.show_round_secret:
        st.info("Uma nova pista foi descoberta, mas apenas dois de vocês podem ler.")
        if st.button(f"🕵️ Apenas {p1} e {p2}: Cliquem para ler a pista secreta", use_container_width=True):
            st.session_state.show_round_secret = True
            st.rerun()
    else:
        st.markdown(f"""
        <div class='secret-box'>
            <h4>🤫 Pista Secreta (Apenas {p1} e {p2})</h4>
            <p>{context_data['rounds'][round_idx]['secret']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Ocultar Pista e Iniciar Debate", use_container_width=True):
            st.session_state.show_round_secret = False
            st.rerun()
            
    st.divider()
    
    # Cronômetro Visual Simples e Debate
    st.markdown("### ⏱️ Tempo de Debate: 3 Minutos")
    
    # Container vazio para o timer
    timer_placeholder = st.empty()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Iniciar Cronômetro Visual"):
            with timer_placeholder:
                bar = st.progress(0)
                # Simulação rápida de timer sem travar por 3 minutos reais (escalado para 10s para o MVP não ficar tedioso testando)
                # Num cenário real, alterar range para 180 (3 min)
                for i in range(100):
                    time.sleep(0.05) # Delay falso para o progress bar preencher suavemente
                    bar.progress(i + 1)
                st.warning("O TEMPO DE DEBATE ACABOU!")
    with col2:
        if st.button("Avançar para Próxima Rodada ⏭️", use_container_width=True, type="primary"):
            st.session_state.round_num += 1
            st.session_state.readers = [] # Reseta os leitores para a próxima rodada
            st.session_state.show_round_secret = False
            st.rerun()

# --- TELA 4: O VEREDITO ---
def render_voting():
    st.markdown("<p class='big-font'>⚖️ O VEREDITO FINAL ⚖️</p>", unsafe_allow_html=True)
    st.markdown("<p class='center-text'>A mesa deve chegar a um consenso. Quem é o culpado?</p>", unsafe_allow_html=True)
    
    suspect = st.selectbox("Acusar formalmente:", ["(Selecione um jogador)"] + st.session_state.players)
    
    if suspect != "(Selecione um jogador)":
        if st.button("Revelar a Verdade 🚨", use_container_width=True, type="primary"):
            st.divider()
            
            # Encontrar quem era o culpado real (role 'bad')
            bad_role_name = GAME_DATA[st.session_state.context]['roles']['bad']
            real_culprit = [p for p, role in st.session_state.roles.items() if role == bad_role_name][0]
            
            if suspect == real_culprit:
                st.success(f"🎉 **A MESA VENCEU!** {real_culprit} era o {bad_role_name}.")
            else:
                st.error(f"💀 **A MESA ERROU!** Vocês acusaram um inocente. O verdadeiro {bad_role_name} era **{real_culprit}**!")
            
            st.markdown("### Identidades Reveladas:")
            for p, role in st.session_state.roles.items():
                st.write(f"- **{p}:** {role}")
                
            st.write("")
            if st.button("Jogar Novamente", use_container_width=True):
                st.session_state.clear()
                st.rerun()

# --- ROTEADOR DE TELAS ---
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
