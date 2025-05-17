
# Escuta IA - Presente quando ninguém mais está

**Escuta IA** é um protótipo de assistente emocional baseado em Inteligência Artificial, inspirado nos princípios do CVV. O projeto busca oferecer escuta empática em momentos de crise emocional, especialmente quando não há disponibilidade de atendimento humano imediato.

---

## Objetivo

Oferecer uma arquitetura leve, reutilizável, ética e acessível para acolhimento emocional baseado em IA. A proposta é facilitar o desenvolvimento de outros projetos similares com foco em privacidade, empatia e apoio.

---

## Arquitetura Técnica

- **Linguagem:** Python 3.10.13
- **Backend:** FastAPI (Railway)  
- **NLU:** Rasa NLU  
- **LLM atual:** Claude (via Together.ai)  
- **LLM futura (ideal):** GPT-4o (OpenAI)  
- **Frontend:** Webchat do Botpress embutido em GitHub Pages  
- **Integração:** Custom Action envia mensagem + contexto ao FastAPI  
- **IA reutilizável:** Integra com Telegram, WhatsApp, etc.

---

## Arquitetura do Escuta IA (Fluxo de Comunicação)

```
[Usuário] 
   │
   ▼
[Webchat Botpress (GitHub Pages)]
   │
   ▼
[Custom Action Botpress]
   │
   ▼ (payload: mensagem + contexto salvo no navegador)
[FastAPI no Railway]
   ├──> [Rasa NLU] → Detecta intenção da mensagem
   └──> [Claude via Together.ai] → Gera resposta empática com contexto
   │
   ▼
[Botpress] → Entrega resposta ao usuário
```

---

## Funcionalidades Críticas

- Detecção de risco emocional  
- Rota de resposta crítica empática  
- Controle de contexto  
- Armazenamento local anônimo conforme a LGPD

---

## Armazenamento no Navegador

- Última intenção detectada  
- Sinal de crise  
- Falas recentes  
- Prevenção de repetições

---

## Prompt do Claude

```
Você é um atendente emocional do Escuta IA, baseado nas práticas do CVV.
Sua função é escutar com empatia, sem julgamentos, conselhos ou análises. 
Acolha com presença, silêncio e frases abertas, quando necessário.
```

---

## Como Usar / Clonar Este Projeto

```bash
git clone https://github.com/fabianofranca/escuta-ia.git
cd escuta-ia
python3 -m venv venv
source venv/bin/activate   # ou venv\Scripts\activate no Windows
pip install fastapi uvicorn rasa
rasa train
rasa shell nlu
uvicorn app:app --reload
```

---

## Recursos e Ferramentas

- [Botpress](https://botpress.com/)  
- [Claude (Together.ai)](https://platform.together.ai/)  
- [Rasa](https://rasa.com/)  
- [Railway](https://railway.app/)  
- [Tinybird](https://www.tinybird.co/)  
- [GitHub Pages](https://pages.github.com/)

---

## Painéis Analíticos

O Escuta IA usará a plataforma Tinybird para armazenar e analisar dados anonimizados de uso com segurança e em conformidade com a LGPD. Esses dados permitirão a criação de painéis de visualização para:

- Entender padrões emocionais
- Melhorar a escuta empática
- Avaliar o impacto social do projeto
- Corrigir falhas técnicas ou éticas

### 📊 Painel 1 – Volume de Uso
Monitora a atividade geral da plataforma:
- Quantidade de sessões por dia
- Sessões simultâneas
- Duração média das conversas
- Número médio de mensagens por sessão

**Objetivo:** acompanhar o crescimento do uso e o nível de engajamento.

---

### 📊 Painel 2 – Intenções Detectadas
Mostra a distribuição das intenções entendidas pelo NLU:
- Quais são as intenções mais comuns (ex: desabafo, crise, agradecimento)
- Variação de intenção por horário do dia ou dia da semana
- Evolução histórica de emoções mais frequentes

**Objetivo:** entender o estado emocional predominante e tendências ao longo do tempo.

---

### 📊 Painel 3 – Crises Emocionais
Foca nas sessões com `crise_detectada = true`:
- Percentual de sessões críticas
- Duração média das conversas com crise
- Horários com maior incidência de crises

**Objetivo:** identificar padrões de risco emocional e antecipar horários sensíveis.

---

### 📊 Painel 4 – Indicadores Éticos
Analisa a qualidade da escuta e a conduta do assistente:
- Sessões muito curtas (usuário abandonou cedo)
- Sessões muito longas (risco de dependência)
- Usuários que recusaram ajuda humana

**Objetivo:** garantir limites éticos da escuta e ajustar intervenções automáticas.

---

### 📊 Painel 5 – Métricas Técnicas
Avalia o desempenho do sistema:
- Latência média da resposta da LLM
- Falhas na comunicação com a LLM ou NLU
- Detecção de intenção incorreta (caso for avaliado)

**Objetivo:** manter a plataforma estável, responsiva e com boa interpretação.

---

### 📦 Exemplo de Log Armazenado

```json
{
  "session_id": "uuid",
  "data": "2025-05-11T12:30:00",
  "intencao_final": "crise_emocional",
  "mensagens": 17,
  "duracao_segundos": 340,
  "crise_detectada": true,
  "rejeicao_ajuda": false,
  "agradecimento_ocorreu": true,
  "latencia_ms": 843,
  "erro_nlu": false,
  "erro_llm": false
}
```

## Contribuições

Este projeto está em desenvolvimento e aberto para contribuições acadêmicas e sociais.  
Respeite os princípios éticos da escuta emocional ao contribuir.

---

## Aviso

Este projeto não substitui apoio humano. Em caso de crise, procure o CVV pelo número **188**.

---

## Licença

Este projeto é distribuído com fins educacionais e sociais, inspirado nas práticas de escuta empática do CVV (Centro de Valorização da Vida).

Você tem permissão para:

- Usar o código e estrutura para fins não comerciais
- Adaptar e reutilizar o conteúdo para fins educacionais ou comunitários
- Distribuir versões modificadas com os devidos créditos

Você não pode:

- Comercializar direta ou indiretamente serviços derivados deste projeto
- Utilizar o projeto para fins que envolvam coleta de dados sensíveis sem consentimento claro
- Associar este projeto a instituições de apoio emocional sem autorização expressa delas

Recomenda-se que todo uso siga os princípios éticos da escuta:
- Acolhimento sem julgamento
- Respeito ao tempo e silêncio do outro
- Preservação do anonimato