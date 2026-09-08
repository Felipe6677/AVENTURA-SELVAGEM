// SELVA: SOBREVIVÊNCIA — versão web estável para GitHub Pages.
// A lógica abaixo roda diretamente no navegador, sem depender de PyScript.

const CONFIG = {
  vidaInicial: 3,
  vidaMaxima: 5,
  pontosIniciais: 0,
  cenaInicial: 'nivel_01',
  trilha: 'assets/audios/The_Dawn_of_Aethelgard.mp3'
};

const SCENES = {
  nivel_01:{level:1,title:'O BURACO NA SELVA',video:'assets/videos/nivel_01.mp4',text:'Você acorda na selva e há um enorme buraco cobrindo a trilha.',options:[['Tentar pular o buraco','jump_hole'],['Passar por uma árvore caída','fallen_tree']]},
  nivel_02:{level:2,title:'OS ESPINHOS',image:'assets/imagens/nivel_02.png',text:'Arbustos cheios de espinhos bloqueiam a passagem.',options:[['Forçar passagem','force_thorns'],['Usar pedra para cortar caminho','sharp_stone']]},
  nivel_03:{level:3,title:'A CAVERNA ESCURA',image:'assets/imagens/nivel_03.png',text:'Começa a chover forte e você encontra uma caverna com morcegos.',options:[['Entrar no escuro','dark_cave'],['Fazer uma tocha improvisada','make_torch']]},
  nivel_04:{level:4,title:'O RIO DAS PIRANHAS',image:'assets/imagens/nivel_04.png',text:'Você chega a um rio agitado e cheio de piranhas.',options:[['Nadar rápido','swim'],['Montar uma pequena jangada','raft']]},
  nivel_05:{level:5,title:'ACAMPAMENTO ABANDONADO',image:'assets/imagens/nivel_05.png',text:'Você acha uma barraca velha com suprimentos.',options:[['Pegar o kit médico','medkit'],['Pegar o mapa antigo','map']]},
  nivel_06:{level:6,title:'PÂNTANO MOVEDIÇO',image:'assets/imagens/nivel_06.png',text:'Você começa a afundar na lama movediça.',options:[['Debater-se para sair','struggle'],['Manter a calma e usar cipó ou raiz','vine']]},
  nivel_07:{level:7,title:'FRUTAS MISTERIOSAS',image:'assets/imagens/nivel_07.png',text:'Você encontra frutas brilhantes em uma árvore.',options:[['Comer as frutas','eat_fruit'],['Ignorar e continuar','ignore_fruit']]},
  nivel_08:{level:8,title:'A PONTE DE CORDA',image:'assets/imagens/nivel_08.png',text:'Há um abismo com uma ponte velha caindo aos pedaços.',options:[['Correr pela ponte','old_bridge'],['Usar cipó como tirolesa','zipline']]},
  nivel_09:{level:9,title:'ATAQUE DA ONÇA',image:'assets/imagens/nivel_09.png',text:'Uma onça-pintada surge na trilha.',options:[['Tentar afastá-la','fight_jaguar'],['Usar o fogo da tocha','torch_jaguar']]},
  nivel_10:{level:10,title:'O ENIGMA DAS RUÍNAS',image:'assets/imagens/nivel_10.png',text:'Enigma da porta: “O que corre sem ter pernas?”',options:[['O vento','wind_riddle'],['O rio','river_riddle']]},
  nivel_11:{level:11,title:'O LABIRINTO',image:'assets/imagens/nivel_11.png',text:'Você entra em um corredor com vários caminhos.',options:[['Caminho da esquerda','left_maze'],['Caminho da direita','right_maze']]},
  nivel_12:{level:12,title:'NINHO DE COBRAS',image:'assets/imagens/nivel_12.png',text:'O chão está repleto de animais perigosos.',options:[['Andar devagar sem fazer barulho','slow_snakes'],['Correr e pular','run_snakes']]},
  nivel_13:{level:13,title:'O PAREDÃO DE ROCHA',image:'assets/imagens/nivel_13.png',text:'Você precisa encontrar uma passagem segura pelo paredão.',options:[['Subir pelas pedras soltas','loose_rocks'],['Usar raízes firmes','firm_roots']]},
  nivel_14:{level:14,title:'TEMPESTADE NO TOPO',image:'assets/imagens/nivel_14.png',text:'Raios e ventos fortes atingem o alto da montanha.',options:[['Buscar abrigo nas rochas','rock_shelter'],['Continuar andando no aberto','open_storm']]},
  nivel_15:{level:15,title:'O RESGATE FINAL',image:'assets/imagens/nivel_15.png',text:'Você ouve um helicóptero de resgate sobrevoando.',options:[['Disparar o sinalizador','flare'],['Fazer fumaça com a tocha','smoke'],['Apenas chamar atenção','shout']]}
};

const ACTIONS = {
  jump_hole:[-1,0,null,'Você pula o buraco, mas se machuca e continua.','nivel_02'], fallen_tree:[0,10,'galho_forte','A árvore caída serve de passagem. Você pega um galho forte.','nivel_02'],
  force_thorns:[-1,0,null,'Você força a passagem e se machuca nos espinhos.','nivel_03'], sharp_stone:[0,10,'pedra_afiada','Você usa uma pedra afiada e abre caminho.','nivel_03'],
  dark_cave:[-1,0,null,'Você entra no escuro e consegue seguir em frente.','nivel_04'],
  swim:[-2,0,null,'Você nada rápido e consegue atravessar o rio.','nivel_05'], raft:[0,15,null,'Você monta uma pequena jangada e atravessa em segurança.','nivel_05'],
  medkit:[0,0,'kit_medico','Você encontra um kit médico.','nivel_06'], map:[0,15,'mapa','Você encontra um mapa antigo que poderá ajudar no labirinto.','nivel_06'],
  struggle:[-1,0,null,'Você se debate na lama e consegue sair.','nivel_07'], vine:[0,15,'cipo','Você usa um cipó resistente e consegue sair do pântano.','nivel_07'],
  eat_fruit:[-1,0,null,'As frutas não eram uma boa escolha. Você perde vida, mas continua.','nivel_08'], ignore_fruit:[0,5,null,'Você ignora as frutas e continua pela trilha.','nivel_08'],
  old_bridge:[-1,0,null,'A ponte balança, você se machuca, mas alcança o outro lado.','nivel_09'],
  fight_jaguar:[-2,0,null,'Você consegue se afastar da situação, mas perde vida.','nivel_10'],
  wind_riddle:[-1,0,null,'A resposta está errada. Você força a passagem e se machuca.','nivel_11'], river_riddle:[0,25,'sinalizador','Correto! O rio corre sem pernas. A porta se abre e você encontra um sinalizador.','nivel_11'],
  left_maze:[-1,0,null,'Sem o mapa, você pega o caminho errado e perde vida antes de achar a saída.','nivel_12'], right_maze:[0,10,null,'Você escolhe a direita e encontra a saída do labirinto.','nivel_12'],
  slow_snakes:[0,15,null,'Você atravessa o trecho com cuidado e encontra a saída.','nivel_13'], run_snakes:[-1,0,null,'Você corre e consegue escapar, mas perde vida.','nivel_13'],
  loose_rocks:[-1,0,null,'Uma pedra se solta. Você escorrega e perde vida.','nivel_14'], firm_roots:[0,15,null,'As raízes firmes ajudam você a chegar ao topo.','nivel_14'],
  rock_shelter:[0,15,null,'Você encontra abrigo e espera a tempestade passar.','nivel_15'], open_storm:[-1,0,null,'Você atravessa a tempestade no aberto e perde vida.','nivel_15']
};

const SAVE_KEY = 'selva_sobrevivencia_save_v2';

const state = {
  vida: CONFIG.vidaInicial,
  inventario: [],
  pontos: CONFIG.pontosIniciais,
  cena: CONFIG.cenaInicial,
  niveisVisitados: 0,
  somAtivo: true
};

let inputBloqueado = false;
let toastTimer = null;
const $ = id => document.getElementById(id);
const possui = item => state.inventario.includes(item);

const ITEM_NAMES = {
  galho_forte:'Galho forte',
  pedra_afiada:'Pedra afiada',
  tocha:'Tocha',
  kit_medico:'Kit médico',
  mapa:'Mapa',
  cipo:'Cipó',
  sinalizador:'Sinalizador'
};

function nomeItem(item){ return ITEM_NAMES[item] || item.replaceAll('_',' '); }

function toast(texto,tipo='normal'){
  clearTimeout(toastTimer);
  const el=$('toast');
  el.innerText=texto;
  el.className=`toast show ${tipo}`;
  toastTimer=setTimeout(()=>el.classList.remove('show'),1800);
}

function pegar(item,pontos=0){
  if(!possui(item)){
    state.inventario.push(item);
    state.pontos+=pontos;
    toast(`Item obtido: ${nomeItem(item)}`,'good');
  }
}

function dano(pts){
  state.vida=Math.max(0,state.vida-pts);
  toast(`Vida perdida: ${pts}`,'bad');
}

function curar(pts){
  const antes=state.vida;
  state.vida=Math.min(CONFIG.vidaMaxima,state.vida+pts);
  if(state.vida>antes) toast(`Vida recuperada: +${state.vida-antes}`,'good');
}

function atualizarStatus(){
  const v=state.vida;
  $('vida').innerText=`${'●'.repeat(v)}${'○'.repeat(CONFIG.vidaMaxima-v)}`;
  $('vida-num').innerText=`${v}/${CONFIG.vidaMaxima}`;
  $('vida').setAttribute('aria-label',`Vida: ${v} de ${CONFIG.vidaMaxima}`);
  $('pontos').innerText=state.pontos;
  $('inventario').innerText=state.inventario.length
    ? state.inventario.map(nomeItem).join(' • ')
    : 'Vazio';
  $('fase-atual')?.remove();
}

function atualizarProgresso(){
  const n=SCENES[state.cena].level;
  $('barra-progresso').style.width=`${Math.round(n/15*100)}%`;
  $('progresso-texto').innerText=`NÍVEL ${String(n).padStart(2,'0')} / 15`;
  $('nivel-media').innerText=`NÍVEL ${String(n).padStart(2,'0')}`;
}

function setButtons(options){
  let visible=0;
  for(let i=1;i<=3;i++){
    const b=$(`opcao${i}`);
    if(options[i-1]){
      const [label,action]=options[i-1];
      visible++;
      b.innerText=`${i}. ${label}`;
      b.style.display='block';
      b.disabled=false;
      b.dataset.action=action;
      b.setAttribute('aria-label',`Escolha ${i}: ${label}`);
    }else{
      b.innerText='';
      b.style.display='none';
      b.disabled=true;
      b.dataset.action='';
    }
  }
  $('choice-count').innerText=`${visible} ${visible===1?'opção':'opções'}`;
}

function atualizarImagem(path, videoPath=null){
  const img=$('imagem-cena');
  const video=$('video-cena');
  const loader=$('loading-image');
  loader.style.display='flex';
  img.style.display='none';
  video.style.display='none';
  video.pause();
  video.removeAttribute('src');
  video.load();

  if(videoPath){
    video.style.display='block';
    video.muted=!state.somAtivo;
    video.src=videoPath;
    video.onloadeddata=()=>{
      loader.style.display='none';
      video.style.opacity='1';
      video.play().catch(()=>{});
    };
    video.onerror=()=>{
      video.style.display='none';
      loader.style.display='none';
      toast('Não foi possível carregar o vídeo do nível 1. Verifique se o arquivo assets/videos/nivel_01.mp4 está no projeto.','bad');
    };
    return;
  }

  img.style.display='block';
  img.style.opacity='.15';
  img.onload=()=>{
    img.style.opacity='1';
    loader.style.display='none';
  };
  img.onerror=()=>{
    img.style.opacity='1';
    loader.style.display='none';
    toast('Não foi possível carregar a imagem da cena.','bad');
  };
  img.src=path;
}

function mostrarCena(nome){
  if(!SCENES[nome]) return mostrarFinal(false,'A próxima fase não foi encontrada.');
  inputBloqueado=false;
  state.cena=nome;
  const cena=SCENES[nome];
  state.niveisVisitados=Math.max(state.niveisVisitados,cena.level);

  $('titulo-cena').innerText=`NÍVEL ${String(cena.level).padStart(2,'0')} // ${cena.title}`;
  $('texto-cena').innerText=cena.text;
  atualizarImagem(cena.image || null, cena.video || null);
  setButtons(cena.options);
  atualizarStatus();
  atualizarProgresso();

  $('painel-cena').classList.remove('scene-enter');
  void $('painel-cena').offsetWidth;
  $('painel-cena').classList.add('scene-enter');

  salvarJogo(false);
}

function concluirNivel(proxima,mensagem){
  if(state.vida<=0) return mostrarFinal(false,'Sua vida chegou a zero antes de concluir a aventura.');
  inputBloqueado=true;
  toast(mensagem,'good');
  setTimeout(()=>mostrarCena(proxima),650);
}

function executarAcao(acao){
  if(inputBloqueado) return;

  if(acao==='make_torch'){
    if(!possui('galho_forte')) return toast('Você precisa do Galho forte do nível 1.','bad');
    pegar('tocha',20);
    return concluirNivel('nivel_04','Tocha preparada. Você consegue atravessar a caverna.');
  }

  if(acao==='zipline'){
    if(!possui('cipo')) return toast('Você precisa do Cipó do nível 6.','bad');
    return concluirNivel('nivel_09','A tirolesa está pronta. Você atravessa o abismo.');
  }

  if(acao==='torch_jaguar'){
    if(!possui('tocha')) return toast('Você precisa da Tocha do nível 3.','bad');
    return concluirNivel('nivel_10','A luz da tocha permite seguir pela trilha.');
  }

  if(acao==='left_maze' && possui('mapa')){
    state.pontos+=20;
    return concluirNivel('nivel_12','O mapa mostra o caminho correto.');
  }

  if(state.cena==='nivel_15'){
    if(acao==='flare'){
      return possui('sinalizador')
        ? mostrarFinal(true,'Você dispara o sinalizador e o helicóptero localiza sua posição.')
        : toast('Você não possui o Sinalizador.','bad');
    }
    if(acao==='smoke'){
      return possui('tocha')
        ? mostrarFinal(true,'A fumaça da tocha chama a atenção do piloto.')
        : toast('Você não possui a Tocha.','bad');
    }
    if(acao==='shout'){
      return (possui('mapa')||state.vida>=4)
        ? mostrarFinal(true,'Seu chamado é ouvido e o resgate acontece.')
        : mostrarFinal(false,'O helicóptero não consegue localizar você a tempo.');
    }
  }

  const a=ACTIONS[acao];
  if(!a) return toast('Ação inválida.','bad');

  const [dmg,pts,item,msg,next]=a;
  if(dmg<0) dano(-dmg);
  if(pts) state.pontos+=pts;
  if(item) pegar(item);
  if(acao==='medkit') curar(2);

  concluirNivel(next,msg);
}

function mostrarFinal(bom,motivo){
  inputBloqueado=true;
  $('jogo').style.display='none';
  $('final').style.display='flex';
  $('final-icone').innerText=bom?'MISSÃO CONCLUÍDA':'FIM DA AVENTURA';
  $('final-titulo').innerText=bom?'RESGATE CONCLUÍDO':'GAME OVER';
  $('final-titulo').className=`pixel-title final-title ${bom?'good-text':'bad-text'}`;
  $('final-texto').innerText=(bom
    ? 'Você superou os 15 níveis e encontrou uma rota de resgate.'
    : 'A aventura terminou desta vez.')+`\n\n${motivo}`;
  $('final-vida').innerText=`Vida: ${state.vida}/${CONFIG.vidaMaxima}`;
  $('final-pontos').innerText=`Pontos: ${state.pontos}`;
  $('final-itens').innerText=`Itens: ${state.inventario.length?state.inventario.map(nomeItem).join(', '):'Nenhum'}`;
  localStorage.removeItem(SAVE_KEY);
}

function resetar(){
  state.vida=CONFIG.vidaInicial;
  state.inventario=[];
  state.pontos=CONFIG.pontosIniciais;
  state.cena=CONFIG.cenaInicial;
  state.niveisVisitados=0;
  inputBloqueado=false;
}

function salvarJogo(showToast=true){
  try{
    localStorage.setItem(SAVE_KEY,JSON.stringify({
      vida:state.vida,
      inventario:state.inventario,
      pontos:state.pontos,
      cena:state.cena,
      niveisVisitados:state.niveisVisitados,
      savedAt:new Date().toISOString()
    }));
    if(showToast) toast('Progresso salvo.','good');
  }catch{
    if(showToast) toast('Não foi possível salvar neste navegador.','bad');
  }
}

function carregarJogo(){
  try{
    const raw=localStorage.getItem(SAVE_KEY);
    if(!raw) return false;
    const saved=JSON.parse(raw);
    if(!SCENES[saved.cena] || !Array.isArray(saved.inventario)) return false;
    state.vida=Math.max(0,Math.min(CONFIG.vidaMaxima,Number(saved.vida)||CONFIG.vidaInicial));
    state.inventario=saved.inventario.filter(Boolean);
    state.pontos=Math.max(0,Number(saved.pontos)||0);
    state.cena=saved.cena;
    state.niveisVisitados=Math.max(1,Number(saved.niveisVisitados)||1);
    return true;
  }catch{
    return false;
  }
}

function iniciarJogo(){
  const temSave=localStorage.getItem(SAVE_KEY);
  if(temSave){
    const continuar=window.confirm('Existe um progresso salvo. Deseja continuar de onde parou?');
    if(continuar && carregarJogo()){
      $('final').style.display='none';
      $('tela-inicio').style.display='none';
      $('jogo').style.display='grid';
      mostrarCena(state.cena);
      tocarMusica();
      return;
    }
  }

  resetar();
  $('final').style.display='none';
  $('tela-inicio').style.display='none';
  $('jogo').style.display='grid';
  mostrarCena(CONFIG.cenaInicial);
  tocarMusica();
}

function tocarMusica(){
  const audio=$('audio-fundo');
  audio.src=CONFIG.trilha;
  audio.volume=.24;
  audio.muted=!state.somAtivo;
  audio.play().catch(()=>{});
}

function alternarSom(){
  state.somAtivo=!state.somAtivo;
  $('audio-fundo').muted=!state.somAtivo;
  $('video-cena').muted=!state.somAtivo;
  $('botao-som').innerText=`SOM: ${state.somAtivo?'ON':'OFF'}`;
}

function confirmarReinicio(){
  if(window.confirm('Reiniciar a aventura? O progresso atual será substituído.')){
    localStorage.removeItem(SAVE_KEY);
    resetar();
    mostrarCena(CONFIG.cenaInicial);
    toast('Aventura reiniciada.','good');
  }
}

function selecionarPorTecla(tecla){
  if(inputBloqueado) return;
  const b=$(`opcao${tecla}`);
  if(b && !b.disabled && b.style.display!=='none'){
    b.focus();
    b.click();
  }
}

$('botao-iniciar').addEventListener('click',iniciarJogo);
$('botao-som').addEventListener('click',alternarSom);
$('botao-salvar').addEventListener('click',()=>salvarJogo(true));
$('opcao1').addEventListener('click',()=>executarAcao($('opcao1').dataset.action));
$('opcao2').addEventListener('click',()=>executarAcao($('opcao2').dataset.action));
$('opcao3').addEventListener('click',()=>executarAcao($('opcao3').dataset.action));
$('reiniciar').addEventListener('click',confirmarReinicio);
$('voltar-inicio').addEventListener('click',()=>{
  $('final').style.display='none';
  $('tela-inicio').style.display='flex';
  $('mensagem-save').innerText=localStorage.getItem(SAVE_KEY)
    ? 'Há um progresso salvo nesta máquina.'
    : '';
});

document.addEventListener('keydown',e=>{
  if($('jogo').style.display==='none') return;
  if(['1','2','3'].includes(e.key)){
    e.preventDefault();
    selecionarPorTecla(e.key);
  }
});

window.addEventListener('beforeunload',()=>salvarJogo(false));

$('jogo').style.display='none';
$('final').style.display='none';
$('mensagem-save').innerText=localStorage.getItem(SAVE_KEY)
  ? 'Há um progresso salvo nesta máquina.'
  : '';
