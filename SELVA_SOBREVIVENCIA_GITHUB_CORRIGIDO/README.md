# 🦜 SELVA: SOBREVIVÊNCIA — Edição Fliperama

Jogo de aventura com **15 níveis completos**, baseado no código Python original.

## O que foi integrado

- Progressão automática do nível 1 ao 15 conforme a escolha do jogador.
- Uma imagem `nivel_01.png` ... `nivel_15.png` para cada fase.
- Perguntas/escolhas específicas de cada fase.
- Vida inicial 3/5, dano e cura.
- Inventário com itens que afetam fases futuras.
- Dependências reais entre fases:
  - Nível 1 → galho forte → permite fazer a tocha no nível 3.
  - Nível 6 → cipó → permite usar a tirolesa no nível 8.
  - Nível 5 → mapa → ajuda no labirinto do nível 11.
  - Nível 10 → resposta correta “rio” → sinalizador para o resgate.
- Final de resgate no nível 15 e Game Over quando a vida chega a zero.
- Controles por mouse/toque e teclado `1`, `2` e `3`.
- Música de fundo iniciada após o clique em **INICIAR AVENTURA**.
- Layout responsivo para desktop e celular.

## Estrutura

```text
SELVA_SOBREVIVENCIA/
├── index.html
├── main.py
├── style.css
├── README.md
├── .nojekyll
└── assets/
    ├── imagens/
    │   ├── nivel_01.png
    │   ├── nivel_02.png
    │   ├── ...
    │   └── nivel_15.png
    └── audios/
        └── The_Dawn_of_Aethelgard.mp3
```

## GitHub Pages

Envie todos os arquivos mantendo a estrutura acima. Depois, no repositório:

**Settings → Pages → Deploy from a branch → main → /(root)**.

## Teste local

Na pasta do projeto:

```bash
python -m http.server 8000
```

Abra `http://localhost:8000`.

Não é recomendado abrir `index.html` diretamente com duplo clique, porque o PyScript e alguns recursos do navegador podem ser bloqueados no modo `file://`.
