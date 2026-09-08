# ============================================================
# SELVA: SOBREVIVÊNCIA — EDIÇÃO FLIPERAMA
# Jogo completo em 15 níveis com escolhas, itens, vida e finais.
# A lógica roda no navegador através do PyScript.
# ============================================================

from pyscript import web, when, window

CONFIG = {
    "titulo": "SELVA: SOBREVIVÊNCIA",
    "subtitulo": "15 níveis • escolhas • itens • vida • finais",
    "autor": "Projeto baseado no código original",
    "vida_inicial": 3,
    "vida_maxima": 5,
    "pontos_iniciais": 0,
    "cena_inicial": "nivel_01",
    "trilha": "assets/audios/The_Dawn_of_Aethelgard.mp3",
}

state = {
    "vida": CONFIG["vida_inicial"],
    "inventario": [],
    "pontos": CONFIG["pontos_iniciais"],
    "cena": CONFIG["cena_inicial"],
    "niveis_visitados": 0,
}

def el(id_):
    return web.page[id_]

def reset_state():
    state["vida"] = CONFIG["vida_inicial"]
    state["inventario"] = []
    state["pontos"] = CONFIG["pontos_iniciais"]
    state["cena"] = CONFIG["cena_inicial"]
    state["niveis_visitados"] = 0

def possui(item):
    return item in state["inventario"]

def pegar(item, pontos=0):
    if item not in state["inventario"]:
        state["inventario"].append(item)
        state["pontos"] += pontos
        mostrar_toast(f"🎒 ITEM OBTIDO: [{item.upper()}]", "good")

def curar(pts):
    antes = state["vida"]
    state["vida"] = min(CONFIG["vida_maxima"], state["vida"] + pts)
    recuperado = state["vida"] - antes
    if recuperado:
        mostrar_toast(f"❤️ +{recuperado} VIDA", "good")

def dano(pts):
    state["vida"] = max(0, state["vida"] - pts)
    mostrar_toast(f"💥 -{pts} VIDA", "bad")

# ============================================================
# 15 CENAS — a próxima fase é definida pelas ações abaixo.
# As imagens são trocadas automaticamente junto com a cena.
# ============================================================

SCENES = {
    "nivel_01": {
        "level": 1,
        "title": "O BURACO NA SELVA",
        "image": "assets/imagens/nivel_01.png",
        "text": "Você acorda na selva e há um enorme buraco cobrindo a trilha.",
        "options": [
            ("🦘 Tentar pular o buraco", "jump_hole", "Perigo • -1 vida"),
            ("🌳 Passar por uma árvore caída", "fallen_tree", "Seguro • item"),
        ],
    },
    "nivel_02": {
        "level": 2,
        "title": "OS ESPINHOS",
        "image": "assets/imagens/nivel_02.png",
        "text": "Arbustos cheios de espinhos bloqueiam a passagem.",
        "options": [
            ("💪 Forçar passagem", "force_thorns", "Perigo • -1 vida"),
            ("🪨 Usar pedra para cortar caminho", "sharp_stone", "Seguro • item"),
        ],
    },
    "nivel_03": {
        "level": 3,
        "title": "A CAVERNA ESCURA",
        "image": "assets/imagens/nivel_03.png",
        "text": "Começa a chover forte e você encontra uma caverna com morcegos.",
        "options": [
            ("🌑 Entrar no escuro", "dark_cave", "Perigo • -1 vida"),
            ("🔥 Fazer uma tocha improvisada", "make_torch", "Requer galho forte"),
        ],
    },
    "nivel_04": {
        "level": 4,
        "title": "O RIO DAS PIRANHAS",
        "image": "assets/imagens/nivel_04.png",
        "text": "Você chega a um rio agitado e cheio de piranhas.",
        "options": [
            ("🏊 Nadar rápido", "swim", "Muito perigoso • -2 vidas"),
            ("🛶 Montar uma pequena jangada", "raft", "Seguro"),
        ],
    },
    "nivel_05": {
        "level": 5,
        "title": "ACAMPAMENTO ABANDONADO",
        "image": "assets/imagens/nivel_05.png",
        "text": "Você acha uma barraca velha com suprimentos.",
        "options": [
            ("🩹 Pegar o kit médico", "medkit", "Recupera até 2 vidas"),
            ("🗺️ Pegar o mapa antigo", "map", "Item • ajuda no labirinto"),
        ],
    },
    "nivel_06": {
        "level": 6,
        "title": "PÂNTANO MOVEDIÇO",
        "image": "assets/imagens/nivel_06.png",
        "text": "Você começa a afundar na lama movediça!",
        "options": [
            ("😰 Debater-se para sair", "struggle", "Perigo • -1 vida"),
            ("🌿 Manter a calma e usar cipó/raiz", "vine", "Seguro • item"),
        ],
    },
    "nivel_07": {
        "level": 7,
        "title": "FRUTAS MISTERIOSAS",
        "image": "assets/imagens/nivel_07.png",
        "text": "Você encontra frutas brilhantes em uma árvore.",
        "options": [
            ("🍇 Comer as frutas", "eat_fruit", "Perigo • -1 vida"),
            ("🚶 Ignorar e continuar", "ignore_fruit", "Seguro"),
        ],
    },
    "nivel_08": {
        "level": 8,
        "title": "A PONTE DE CORDA",
        "image": "assets/imagens/nivel_08.png",
        "text": "Há um abismo com uma ponte velha caindo aos pedaços.",
        "options": [
            ("🏃 Correr pela ponte", "old_bridge", "Risco • -1 vida"),
            ("🪢 Usar cipó como tirolesa", "zipline", "Requer cipó"),
        ],
    },
    "nivel_09": {
        "level": 9,
        "title": "ATAQUE DA ONÇA",
        "image": "assets/imagens/nivel_09.png",
        "text": "Uma onça-pintada surge rosnando na sua frente!",
        "options": [
            ("👊 Lutar com as mãos", "fight_jaguar", "Muito perigoso • -2 vidas"),
            ("🔥 Espantar com o fogo da tocha", "torch_jaguar", "Requer tocha"),
        ],
    },
    "nivel_10": {
        "level": 10,
        "title": "O ENIGMA DAS RUÍNAS",
        "image": "assets/imagens/nivel_10.png",
        "text": "Enigma da porta: “O que corre sem ter pernas?”",
        "options": [
            ("💨 O vento", "wind_riddle", "Resposta errada • -1 vida"),
            ("🌊 O rio", "river_riddle", "Resposta correta • sinalizador"),
        ],
    },
    "nivel_11": {
        "level": 11,
        "title": "O LABIRINTO",
        "image": "assets/imagens/nivel_11.png",
        "text": "Você entra em um corredor com vários caminhos.",
        "options": [
            ("⬅️ Caminho da esquerda", "left_maze", "Com mapa: seguro"),
            ("➡️ Caminho da direita", "right_maze", "Seguro"),
        ],
    },
    "nivel_12": {
        "level": 12,
        "title": "NINHO DE COBRAS",
        "image": "assets/imagens/nivel_12.png",
        "text": "O chão está repleto de cobras venenosas.",
        "options": [
            ("🐍 Andar devagar sem fazer barulho", "slow_snakes", "Seguro"),
            ("🏃 Correr e pular", "run_snakes", "Risco • -1 vida"),
        ],
    },
    "nivel_13": {
        "level": 13,
        "title": "O PAREDÃO DE ROCHA",
        "image": "assets/imagens/nivel_13.png",
        "text": "Você precisa escalar um paredão íngreme.",
        "options": [
            ("🪨 Subir pelas pedras soltas", "loose_rocks", "Risco • -1 vida"),
            ("🌿 Usar raízes firmes", "firm_roots", "Seguro"),
        ],
    },
    "nivel_14": {
        "level": 14,
        "title": "TEMPESTADE NO TOPO",
        "image": "assets/imagens/nivel_14.png",
        "text": "Raios e ventos fortes atingem o alto da montanha.",
        "options": [
            ("🪨 Buscar abrigo nas rochas", "rock_shelter", "Seguro"),
            ("⚡ Continuar andando no aberto", "open_storm", "Risco • -1 vida"),
        ],
    },
    "nivel_15": {
        "level": 15,
        "title": "O RESGATE FINAL",
        "image": "assets/imagens/nivel_15.png",
        "text": "Você ouve um helicóptero de resgate sobrevoando!",
        "options": [
            ("🚨 Disparar o sinalizador", "flare", "Requer sinalizador"),
            ("🔥 Fazer fumaça com a tocha", "smoke", "Requer tocha"),
            ("📢 Apenas gritar alto", "shout", "Pode falhar"),
        ],
    },
}

# Ações normais:
# dano, pontos, item, mensagem, próxima cena
ACTIONS = {
    "jump_hole": (-1, 0, None, "Você pula o buraco, mas se machuca e continua.", "nivel_02"),
    "fallen_tree": (0, 10, "galho_forte", "A árvore caída serve de passagem. Você pega um galho forte.", "nivel_02"),

    "force_thorns": (-1, 0, None, "Você força a passagem e se machuca nos espinhos.", "nivel_03"),
    "sharp_stone": (0, 10, "pedra_afiada", "Você usa uma pedra afiada e abre caminho.", "nivel_03"),

    "dark_cave": (-1, 0, None, "Você entra no escuro e se machuca com a movimentação dos morcegos.", "nivel_04"),

    "swim": (-2, 0, None, "Você nada rápido e consegue atravessar o rio.", "nivel_05"),
    "raft": (0, 15, None, "Você monta uma pequena jangada e atravessa em segurança.", "nivel_05"),

    "medkit": (0, 0, "kit_medico", "Você encontra um kit médico.", "nivel_06"),
    "map": (0, 15, "mapa", "Você encontra um mapa antigo que poderá ajudar no labirinto.", "nivel_06"),

    "struggle": (-1, 0, None, "Você se debate na lama e se machuca, mas consegue sair.", "nivel_07"),
    "vine": (0, 15, "cipo", "Você usa um cipó resistente e consegue sair do pântano.", "nivel_07"),

    "eat_fruit": (-1, 0, None, "As frutas eram venenosas! Você perde vida, mas consegue continuar.", "nivel_08"),
    "ignore_fruit": (0, 5, None, "Você ignora as frutas e continua pela trilha.", "nivel_08"),

    "old_bridge": (-1, 0, None, "A ponte quebra e você se machuca, mas alcança o outro lado.", "nivel_09"),

    "fight_jaguar": (-2, 0, None, "Você enfrenta a onça e consegue fazê-la recuar, mas se machuca.", "nivel_10"),

    "wind_riddle": (-1, 0, None, "A resposta está errada. Você força a passagem e se machuca.", "nivel_11"),
    "river_riddle": (0, 25, "sinalizador", "Correto! O rio corre sem pernas. A porta se abre e você encontra um sinalizador.", "nivel_11"),

    "left_maze": (-1, 0, None, "Sem o mapa, você pega o caminho errado e perde vida antes de achar a saída.", "nivel_12"),
    "right_maze": (0, 10, None, "Você escolhe a direita e encontra a saída do labirinto.", "nivel_12"),

    "slow_snakes": (0, 15, None, "Você anda devagar e atravessa o ninho sem acordar as cobras.", "nivel_13"),
    "run_snakes": (-1, 0, None, "Você corre e consegue escapar, mas perde vida.", "nivel_13"),

    "loose_rocks": (-1, 0, None, "Uma pedra se solta. Você escorrega e se machuca.", "nivel_14"),
    "firm_roots": (0, 15, None, "As raízes firmes sustentam seu peso e você chega ao topo.", "nivel_14"),

    "rock_shelter": (0, 15, None, "Você encontra abrigo e espera a tempestade passar.", "nivel_15"),
    "open_storm": (-1, 0, None, "Você atravessa a tempestade no aberto e perde vida.", "nivel_15"),
}

# ============================================================
# Interface
# ============================================================

def mostrar_toast(texto, tipo="normal"):
    el("toast").innerText = texto
    el("toast").className = f"toast show {tipo}"
    window.setTimeout(lambda: el("toast").classList.remove("show"), 1600)

def atualizar_status():
    vida = state["vida"]
    coracoes = " ".join(["❤️"] * vida)
    vazios = " ".join(["🖤"] * (CONFIG["vida_maxima"] - vida))
    el("vida").innerText = (coracoes + " " + vazios).strip()
    el("vida-num").innerText = f"{vida}/{CONFIG['vida_maxima']}"
    el("pontos").innerText = str(state["pontos"])
    el("inventario").innerText = " • ".join(state["inventario"]) if state["inventario"] else "Vazio"
    nivel = SCENES[state["cena"]]["level"]
    el("fase-atual").innerText = f"{nivel:02d}/15"

def atualizar_progresso():
    nivel = SCENES[state["cena"]]["level"]
    el("barra-progresso").style.width = f"{int(nivel / 15 * 100)}%"
    el("progresso-texto").innerText = f"NÍVEL {nivel:02d} / 15"

def set_buttons(options):
    for i in range(1, 4):
        botao = el(f"opcao{i}")
        if i <= len(options):
            label, action, hint = options[i - 1]
            botao.innerText = f"{i}. {label}\n{hint}"
            botao.style.display = "block"
            botao.disabled = False
            botao.dataset.action = action
        else:
            botao.innerText = ""
            botao.style.display = "none"
            botao.disabled = True
            botao.dataset.action = ""

def atualizar_imagem(path):
    img = el("imagem-cena")
    img.style.opacity = "0.2"
    img.src = path
    def imagem_carregada(event):
        img.style.opacity = "1"
    img.onload = imagem_carregada

def mostrar_cena(nome):
    if nome not in SCENES:
        mostrar_final(False, "Erro interno: a próxima fase não foi encontrada.")
        return

    state["cena"] = nome
    cena = SCENES[nome]

    if cena["level"] > state["niveis_visitados"]:
        state["niveis_visitados"] = cena["level"]

    el("titulo-cena").innerText = f"NÍVEL {cena['level']:02d}  //  {cena['title']}"
    el("texto-cena").innerText = cena["text"]
    atualizar_imagem(cena["image"])
    set_buttons(cena["options"])
    atualizar_status()
    atualizar_progresso()

    el("painel-cena").classList.remove("scene-enter")
    window.setTimeout(lambda: el("painel-cena").classList.add("scene-enter"), 10)

def concluir_nivel(proxima, mensagem):
    if state["vida"] <= 0:
        mostrar_final(False, "Sua vida chegou a 0 antes de concluir a aventura.")
        return
    mostrar_toast(mensagem, "good")
    window.setTimeout(lambda: mostrar_cena(proxima), 550)

def executar_acao(acao):
    # NÍVEL 3 — tocha só pode ser feita com o galho obtido no nível 1.
    if acao == "make_torch":
        if not possui("galho_forte"):
            mostrar_toast("⚠️ Você precisa do GALHO FORTE do nível 1.", "bad")
            return
        if not possui("tocha"):
            pegar("tocha", 20)
        concluir_nivel("nivel_04", "🔥 Tocha pronta! Os morcegos se afastam.")
        return

    # NÍVEL 8 — tirolesa depende do cipó obtido no nível 6.
    if acao == "zipline":
        if not possui("cipo"):
            mostrar_toast("⚠️ Você precisa do CIPÓ do nível 6.", "bad")
            return
        concluir_nivel("nivel_09", "🪢 Tirolesa montada com sucesso!")
        return

    # NÍVEL 9 — fogo da tocha afasta a onça.
    if acao == "torch_jaguar":
        if not possui("tocha"):
            mostrar_toast("⚠️ Você precisa da TOCHA do nível 3.", "bad")
            return
        concluir_nivel("nivel_10", "🔥 A onça se assusta com o fogo e foge!")
        return

    # NÍVEL 11 — o mapa transforma o caminho da esquerda em opção segura.
    if acao == "left_maze" and possui("mapa"):
        state["pontos"] += 20
        concluir_nivel("nivel_12", "🗺️ O mapa mostra o caminho correto!")
        return

    # NÍVEL 15 — final da aventura.
    if state["cena"] == "nivel_15":
        if acao == "flare":
            if possui("sinalizador"):
                mostrar_final(True, "Você dispara o sinalizador e o helicóptero localiza sua posição.")
            else:
                mostrar_toast("⚠️ Você não possui o sinalizador.", "bad")
            return

        if acao == "smoke":
            if possui("tocha"):
                mostrar_final(True, "A fumaça da tocha chama a atenção do piloto.")
            else:
                mostrar_toast("⚠️ Você não possui a tocha.", "bad")
            return

        if acao == "shout":
            # Alternativa jogável: não exige item, mas é menos confiável.
            if possui("mapa") or state["vida"] >= 4:
                mostrar_final(True, "Seu grito é ouvido pelo helicóptero e o resgate acontece.")
            else:
                mostrar_final(False, "O helicóptero não consegue localizar você a tempo.")
            return

    if acao not in ACTIONS:
        mostrar_toast("⚠️ Ação inválida.", "bad")
        return

    dano_pts, pontos, item, mensagem, proxima = ACTIONS[acao]

    if dano_pts < 0:
        dano(-dano_pts)

    if pontos:
        state["pontos"] += pontos

    if item:
        pegar(item)

    if acao == "medkit":
        curar(2)

    concluir_nivel(proxima, mensagem)

def mostrar_final(bom, motivo=""):
    el("jogo").style.display = "none"
    el("final").style.display = "flex"

    if bom:
        el("final-icone").innerText = "🏆"
        el("final-titulo").innerText = "RESGATE CONCLUÍDO!"
        el("final-titulo").className = "pixel-title final-title good-text"
        el("final-texto").innerText = (
            "🎉 PARABÉNS! Você superou todos os 15 níveis e foi resgatado!\n\n"
            + motivo
        )
    else:
        el("final-icone").innerText = "💀"
        el("final-titulo").innerText = "GAME OVER"
        el("final-titulo").className = "pixel-title final-title bad-text"
        el("final-texto").innerText = (
            "A selva foi implacável desta vez.\n\n" + motivo
        )

    el("final-vida").innerText = f"❤️ Vida: {state['vida']}/{CONFIG['vida_maxima']}"
    el("final-pontos").innerText = f"⭐ Pontos: {state['pontos']}"
    el("final-itens").innerText = (
        "🎒 " + (", ".join(state["inventario"]) if state["inventario"] else "Nenhum")
    )

def iniciar_jogo():
    reset_state()
    el("final").style.display = "none"
    el("tela-inicio").style.display = "none"
    el("jogo").style.display = "grid"
    mostrar_cena(CONFIG["cena_inicial"])

    audio = el("audio-fundo")
    audio.src = CONFIG["trilha"]
    audio.volume = 0.32
    audio.loop = True
    try:
        promessa = audio.play()
        if promessa is not None:
            promessa.catch(lambda error: None)
    except Exception:
        pass

@when("click", "#botao-iniciar")
def click_iniciar(event):
    iniciar_jogo()

@when("click", "#opcao1")
def click_1(event):
    executar_acao(el("opcao1").dataset.action)

@when("click", "#opcao2")
def click_2(event):
    executar_acao(el("opcao2").dataset.action)

@when("click", "#opcao3")
def click_3(event):
    executar_acao(el("opcao3").dataset.action)

@when("click", "#reiniciar")
def click_reiniciar(event):
    iniciar_jogo()

@when("click", "#voltar-inicio")
def click_voltar(event):
    el("final").style.display = "none"
    el("tela-inicio").style.display = "flex"

def tecla_arcade(event):
    # Só processa 1/2/3 enquanto a tela de jogo estiver aberta.
    if el("jogo").style.display == "none":
        return
    tecla = event.key
    if tecla in ["1", "2", "3"]:
        botoes = [el("opcao1"), el("opcao2"), el("opcao3")]
        botao = botoes[int(tecla) - 1]
        if not botao.disabled and botao.style.display != "none":
            botao.click()

window.document.addEventListener("keydown", tecla_arcade)

# Inicialização visual.
el("titulo-abertura").innerText = CONFIG["titulo"]
el("subtitulo-abertura").innerText = CONFIG["subtitulo"]
el("autor-abertura").innerText = CONFIG["autor"]
el("botao-iniciar").disabled = False
el("botao-iniciar").innerText = "▶  INICIAR AVENTURA"
atualizar_status()
atualizar_progresso()
