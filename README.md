# SpaceScape

SpaceScape é um jogo 2D desenvolvido em **Python** utilizando a biblioteca **Pygame**, projetado para demonstrar conceitos de criação de jogos, organização modular e implementação de mecânicas clássicas de ação espacial. O projeto inclui sistema de menu, seleção de dificuldade, múltiplas fases, movimentação do jogador, disparos, detecção de colisão e gerenciamento de estado do jogo.

---

## 📌 Visão Geral do Projeto
O jogo foi criado com foco em apresentar uma estrutura sólida e reutilizável para jogos simples em Pygame. A mecânica consiste em controlar uma nave espacial, eliminar inimigos e avançar por três fases distintas, mantendo um nível de dificuldade consistente com o valor selecionado no menu inicial.

O projeto também implementa regras claras de progressão, feedback ao jogador e telas finais de vitória e derrota.

---

## ⚙️ Funcionalidades Principais
- Sistema completo de **menu inicial**.
- **Seleção de dificuldade** aplicável a todas as fases.
- **Seleção de jogador** (skin da nave).
- **Três fases temáticas**, cada uma com fundo e atmosfera próprios.
- Mecânica de tiro sincronizada com detecção de colisão.
- Pontuação contabilizada **apenas quando o disparo acerta o inimigo**.
- Gerenciamento de vidas do jogador.
- Telas de **Game Over** e **Victory**, que avançam apenas com interação do usuário.
- Lógica modular, facilitando manutenção e expansão.

---

## 🧬 Estrutura do Funcionamento
### Movimento
- O jogador se movimenta horizontalmente utilizando as setas **←** e **→**.
- Os disparos são acionados pela tecla **ESPAÇO**.

### Inimigos
- Surgem no topo da tela e descem verticalmente.
- A velocidade e a frequência de spawn variam conforme a dificuldade escolhida.

### Dificuldade
Os níveis podem ser pré-definidos ou personalizados e afetam:
- Velocidade dos inimigos
- Quantidade de inimigos em tela
- Frequência de aparecimento

A dificuldade escolhida é **replicada nas três fases**, garantindo uniformidade do desafio.

---

## 🗺️ Fases do Jogo
### **Fase 1 – Nebulosa Inicial**
- Introdução das mecânicas básicas.
- Baixa complexidade visual.

### **Fase 2 – Campo de Meteoros**
- Ambiente mais denso.
- Inimigos podem surgir com maior frequência.

### **Fase 3 – Galáxia Sombria**
- Atmosfera mais intensa.
- Maior volume de inimigos.

Apesar das diferenças visuais, todas seguem o nível de dificuldade selecionado pelo jogador.

---

## 🎮 Instruções
### Controles
- **← / →**: mover a nave.
- **ESPAÇO**: atirar.

###Objetivo
- Acumular pontos eliminando inimigos.
- Avançar pelas três fases.
- Evitar que inimigos colidam com o jogador.
- Atingir a pontuação-alvo definida.

### Fim do Jogo
- Em caso de derrota ou vitória, a tela correspondente é exibida.
- O jogo **somente avança após o usuário clicar**, evitando encerramento automático.

---

## 🛠️ Tecnologias Utilizadas
- **Python 3.x**
- **Pygame**
- Manipulação de sprites, eventos e colisões
- Estrutura de loop principal otimizada

---

## 📂 Possível Estrutura de Pastas
```
SpaceScape/
│
├── assets/
│   ├── images/
│   ├── sounds/
│   └── fonts/
│
├── spaceScape.py
├── README.md
└── requirements.txt
```

---

## 🚧 Melhorias Futuras
- Implementação de chefes (bosses) por fase.
- Sistema de upgrades da nave.
- Animações de explosão e efeitos visuais adicionais.
- Multiplayer local.

---

## 📜 Licença
Este projeto pode ser utilizado para estudo, modificação e expansão livremente.

---

## 👩‍💻 Autoria
Projeto desenvolvido em colaboração com a usuária, com ajustes progressivos baseados nas necessidades e nas mecânicas desejadas para o jogo SpaceScape.
