from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "aventura-selva-chave-secreta"

MAX_VIDA = 5

CENAS = {
    "inicio": {
        "nivel": 1,
        "titulo": "O BURACO NA SELVA",
        "emoji": "🌴",
        "texto": "Você acorda no meio da selva. À sua frente existe um enorme buraco cobrindo toda a trilha.",
        "opcoes": [
            {"id": "1", "texto": "Tentar pular o buraco", "proxima": "nivel_02_espinhos", "dano": 1},
            {"id": "2", "texto": "Passar por uma árvore caída", "proxima": "nivel_02_espinhos", "item": "galho_forte"}
        ]
    },
    "nivel_02_espinhos": {
        "nivel": 2,
        "titulo": "OS ESPINHOS",
        "emoji": "🌿",
        "texto": "Arbustos enormes e cheios de espinhos bloqueiam completamente a passagem.",
        "opcoes": [
            {"id": "1", "texto": "Forçar passagem", "proxima": "nivel_03_caverna", "dano": 1},
            {"id": "2", "texto": "Usar a pedra para cortar o caminho", "proxima": "nivel_03_caverna", "item": "pedra_afiada"}
        ]
    },
    "nivel_03_caverna": {
        "nivel": 3,
        "titulo": "A CAVERNA ESCURA",
        "emoji": "🦇",
        "texto": "Começa a chover forte. Você encontra uma caverna escura cheia de morcegos.",
        "opcoes": [
            {"id": "1", "texto": "Entrar no escuro", "proxima": "nivel_04_rio", "dano": 1},
            {"id": "2", "texto": "Fazer uma tocha improvisada", "proxima": "nivel_04_rio", "item": "tocha", "requer": "galho_forte"}
        ]
    },
    "nivel_04_rio": {
        "nivel": 4,
        "titulo": "O RIO DAS PIRANHAS",
        "emoji": "🐟",
        "texto": "Você chega a um rio agitado e cheio de piranhas.",
        "opcoes": [
            {"id": "1", "texto": "Nadar rapidamente", "proxima": "nivel_05_acampamento", "dano": 2},
            {"id": "2", "texto": "Montar uma pequena jangada", "proxima": "nivel_05_acampamento"}
        ]
    },
    "nivel_05_acampamento": {
        "nivel": 5,
        "titulo": "ACAMPAMENTO ABANDONADO",
        "emoji": "⛺",
        "texto": "Você encontra uma barraca velha abandonada com alguns suprimentos.",
        "opcoes": [
            {"id": "1", "texto": "Pegar o kit médico", "proxima": "nivel_06_pantano", "cura": 2},
            {"id": "2", "texto": "Pegar o mapa antigo", "proxima": "nivel_06_pantano", "item": "mapa"}
        ]
    },
    "nivel_06_pantano": {
        "nivel": 6,
        "titulo": "PÂNTANO MOVEDIÇO",
        "emoji": "🐊",
        "texto": "De repente, você começa a afundar em uma lama movediça!",
        "opcoes": [
            {"id": "1", "texto": "Debater-se para sair", "proxima": "nivel_07_frutas", "dano": 1},
            {"id": "2", "texto": "Manter a calma e usar um cipó", "proxima": "nivel_07_frutas", "item": "cipo"}
        ]
    },
    "nivel_07_frutas": {
        "nivel": 7,
        "titulo": "FRUTAS MISTERIOSAS",
        "emoji": "🍇",
        "texto": "Você encontra frutas brilhantes em uma árvore. Elas parecem deliciosas...",
        "opcoes": [
            {"id": "1", "texto": "Comer as frutas", "proxima": "nivel_08_ponte", "dano": 1},
            {"id": "2", "texto": "Ignorar e continuar", "proxima": "nivel_08_ponte"}
        ]
    },
    "nivel_08_ponte": {
        "nivel": 8,
        "titulo": "A PONTE DE CORDA",
        "emoji": "🌉",
        "texto": "Um enorme abismo aparece diante de você. Existe uma ponte velha caindo aos pedaços.",
        "opcoes": [
            {"id": "1", "texto": "Correr pela ponte", "proxima": "nivel_09_onca", "dano": 1},
            {"id": "2", "texto": "Usar o cipó como tirolesa", "proxima": "nivel_09_onca", "requer": "cipo"}
        ]
    },
    "nivel_09_onca": {
        "nivel": 9,
        "titulo": "ATAQUE DA ONÇA",
        "emoji": "🐆",
        "texto": "Uma enorme onça-pintada surge rosnando bem na sua frente!",
        "opcoes": [
            {"id": "1", "texto": "Lutar com as mãos", "proxima": "nivel_10_templo", "dano": 2},
            {"id": "2", "texto": "Espantar com o fogo da tocha", "proxima": "nivel_10_templo", "requer": "tocha"}
        ]
    },
    "nivel_10_templo": {
        "nivel": 10,
        "titulo": "O ENIGMA DAS RUÍNAS",
        "emoji": "🏛️",
        "texto": "Você encontra uma porta antiga. Um enigma está escrito nela: “O que corre sem ter pernas?”",
        "opcoes": [
            {"id": "1", "texto": "O vento", "proxima": "nivel_11_labirinto", "dano": 1},
            {"id": "2", "texto": "O rio", "proxima": "nivel_11_labirinto", "item": "sinalizador"}
        ]
    },
    "nivel_11_labirinto": {
        "nivel": 11,
        "titulo": "O LABIRINTO",
        "emoji": "🌀",
        "texto": "Você entra em um corredor com vários caminhos. Esquerda ou direita?",
        "opcoes": [
            {"id": "1", "texto": "Caminho da esquerda", "proxima": "nivel_12_ninho", "dano": 1},
            {"id": "2", "texto": "Caminho da direita", "proxima": "nivel_12_ninho"}
        ]
    },
    "nivel_12_ninho": {
        "nivel": 12,
        "titulo": "NINHO DE COBRAS",
        "emoji": "🐍",
        "texto": "O chão está completamente coberto de cobras venenosas.",
        "opcoes": [
            {"id": "1", "texto": "Andar devagar sem fazer barulho", "proxima": "nivel_13_escalada"},
            {"id": "2", "texto": "Correr e pular", "proxima": "nivel_13_escalada", "dano": 1}
        ]
    },
    "nivel_13_escalada": {
        "nivel": 13,
        "titulo": "O PAREDÃO DE ROCHA",
        "emoji": "🧗",
        "texto": "Você precisa escalar um enorme paredão de rocha para continuar sua aventura.",
        "opcoes": [
            {"id": "1", "texto": "Subir pelas pedras soltas", "proxima": "nivel_14_tempestade", "dano": 1},
            {"id": "2", "texto": "Usar raízes firmes", "proxima": "nivel_14_tempestade"}
        ]
    },
    "nivel_14_tempestade": {
        "nivel": 14,
        "titulo": "TEMPESTADE NO TOPO",
        "emoji": "⛈️",
        "texto": "Raios e ventos muito fortes atingem o alto da montanha.",
        "opcoes": [
            {"id": "1", "texto": "Buscar abrigo nas rochas", "proxima": "nivel_15_resgate"},
            {"id": "2", "texto": "Continuar andando no aberto", "proxima": "nivel_15_resgate", "dano": 1}
        ]
    },
    "nivel_15_resgate": {
        "nivel": 15,
        "titulo": "O RESGATE FINAL",
        "emoji": "🚁",
        "texto": "Você ouve um helicóptero de resgate sobrevoando a montanha!",
        "opcoes": [
            {"id": "1", "texto": "Fazer fumaça com a tocha", "proxima": "fim_bom", "requer": "tocha"},
            {"id": "2", "texto": "Apenas gritar alto", "proxima": "fim_ruim"}
        ]
    }
}


def iniciar_jogo():
    session["vida"] = 3
    session["inventario"] = []
    session["cena"] = "inicio"
    session["mensagem"] = "A aventura começou!"
    session["tipo_mensagem"] = "info"


def adicionar_item(item):
    inventario = session.get("inventario", [])

    if item not in inventario:
        inventario.append(item)
        session["inventario"] = inventario
        return True

    return False


def aplicar_dano(valor):
    vida = session.get("vida", 3)
    vida -= valor
    session["vida"] = max(0, vida)


def aplicar_cura(valor):
    vida = session.get("vida", 3)
    vida = min(MAX_VIDA, vida + valor)
    session["vida"] = vida


def nome_item(item):
    nomes = {
        "galho_forte": "Galho Forte",
        "pedra_afiada": "Pedra Afiada",
        "tocha": "Tocha",
        "mapa": "Mapa Antigo",
        "cipo": "Cipó",
        "sinalizador": "Sinalizador"
    }

    return nomes.get(item, item)


@app.route("/", methods=["GET"])
def index():
    if "vida" not in session:
        iniciar_jogo()

    cena = session.get("cena", "inicio")
    mensagem = session.get("mensagem", "")
    tipo_mensagem = session.get("tipo_mensagem", "info")

    if cena == "fim_bom":
        return render_template(
            "index.html",
            cena=None,
            final="bom",
            vida=session["vida"],
            inventario=session["inventario"],
            mensagem=mensagem,
            tipo_mensagem=tipo_mensagem,
            nome_item=nome_item
        )

    if cena == "fim_ruim":
        return render_template(
            "index.html",
            cena=None,
            final="ruim",
            vida=session["vida"],
            inventario=session["inventario"],
            mensagem=mensagem,
            tipo_mensagem=tipo_mensagem,
            nome_item=nome_item
        )

    cena_atual = CENAS[cena]

    return render_template(
        "index.html",
        cena=cena_atual,
        final=None,
        vida=session["vida"],
        inventario=session["inventario"],
        mensagem=mensagem,
        tipo_mensagem=tipo_mensagem,
        nome_item=nome_item
    )


@app.route("/escolher", methods=["POST"])
def escolher():
    cena_id = session.get("cena", "inicio")
    cena = CENAS.get(cena_id)

    if not cena:
        iniciar_jogo()
        return redirect(url_for("index"))

    escolha = request.form.get("opcao")
    opcao = next(
        (opcao for opcao in cena["opcoes"] if opcao["id"] == escolha),
        None
    )

    if not opcao:
        session["mensagem"] = "⚠️ Escolha inválida!"
        session["tipo_mensagem"] = "erro"
        return redirect(url_for("index"))

    session["mensagem"] = ""
    session["tipo_mensagem"] = "info"

    requer = opcao.get("requer")

    if requer and requer not in session.get("inventario", []):
        if requer == "galho_forte":
            session["mensagem"] = "🔥 Você não possui um galho forte para fazer a tocha!"
        elif requer == "cipo":
            session["mensagem"] = "🌿 Você não possui um cipó para atravessar!"
        elif requer == "tocha":
            session["mensagem"] = "🔥 Você não possui uma tocha para espantar a onça!"

        session["tipo_mensagem"] = "erro"
        return redirect(url_for("index"))

    dano = opcao.get("dano", 0)

    if dano:
        aplicar_dano(dano)
        session["mensagem"] = f"💥 Você sofreu {dano} ponto(s) de dano!"
        session["tipo_mensagem"] = "dano"

    cura = opcao.get("cura", 0)

    if cura:
        aplicar_cura(cura)
        session["mensagem"] = f"❤️ Você recuperou {cura} ponto(s) de vida!"
        session["tipo_mensagem"] = "cura"

    item = opcao.get("item")

    if item:
        novo_item = adicionar_item(item)

        if novo_item:
            session["mensagem"] = f"🎒 Você conseguiu: {nome_item(item)}!"
            session["tipo_mensagem"] = "item"

    if session["vida"] <= 0:
        session["cena"] = "fim_ruim"
        session["mensagem"] = "💀 Sua vida chegou a zero!"
        session["tipo_mensagem"] = "dano"
        return redirect(url_for("index"))

    proxima = opcao["proxima"]

    if cena_id == "nivel_03_caverna" and escolha == "2":
        session["mensagem"] = "🔥 Você acende a tocha e espanta os morcegos!"
        session["tipo_mensagem"] = "item"

    if cena_id == "nivel_04_rio" and escolha == "2":
        session["mensagem"] = "🛶 Você atravessa o rio em segurança com a jangada!"
        session["tipo_mensagem"] = "cura"

    if cena_id == "nivel_08_ponte" and escolha == "2":
        session["mensagem"] = "🌿 Você desliza pela tirolesa e atravessa o abismo!"
        session["tipo_mensagem"] = "cura"

    if cena_id == "nivel_09_onca" and escolha == "2":
        session["mensagem"] = "🔥 A onça se assusta com o fogo e foge!"
        session["tipo_mensagem"] = "item"

    if cena_id == "nivel_10_templo" and escolha == "2":
        session["mensagem"] = "🏛️ A resposta estava correta! A porta se abre e você encontra um sinalizador!"
        session["tipo_mensagem"] = "item"

    if cena_id == "nivel_11_labirinto" and "mapa" in session.get("inventario", []):
        session["mensagem"] = "🗺️ Você usa o mapa e encontra a saída facilmente!"
        session["tipo_mensagem"] = "item"

    if cena_id == "nivel_15_resgate":
        if escolha == "1":
            session["mensagem"] = "🚁 A fumaça chama a atenção do piloto!"
            session["tipo_mensagem"] = "item"

    session["cena"] = proxima

    return redirect(url_for("index"))


@app.route("/reiniciar", methods=["POST"])
def reiniciar():
    iniciar_jogo()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)