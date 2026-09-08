# SELVA: SOBREVIVÊNCIA 🦜

Jogo de aventura web com 15 níveis, escolhas, inventário, vida, imagens por fase e finais.

## Publicar no GitHub Pages

1. Crie um repositório no GitHub.
2. Envie **todo o conteúdo desta pasta para a raiz do repositório**.
3. Vá em **Settings → Pages**.
4. Em *Build and deployment*, selecione **Deploy from a branch**.
5. Escolha a branch `main` e a pasta `/ (root)`.
6. Salve e aguarde a publicação.

O arquivo `.nojekyll` já está incluído.

## Estrutura obrigatória

- `index.html`
- `main.py`
- `style.css`
- `assets/imagens/nivel_01.png` até `nivel_15.png`
- `assets/audios/The_Dawn_of_Aethelgard.mp3`

## Controles

- Clique/toque nos botões.
- Também é possível usar as teclas `1`, `2` e `3`.

## Fluxo do jogo

O jogo começa no nível 1 e avança automaticamente conforme a escolha feita pelo jogador.

Itens obtidos em fases anteriores podem alterar escolhas posteriores:
- Galho forte → tocha no nível 3.
- Cipó → tirolesa no nível 8.
- Mapa → ajuda no labirinto do nível 11.
- Resposta correta do enigma → sinalizador para o resgate.

O nível 15 encerra a aventura com resgate ou Game Over.
