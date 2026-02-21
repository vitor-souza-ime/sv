# 🌡 Sensor Virtual (SV)

Sistema Web de **Sensor Virtual baseado em Regressão Linear**, utilizando dados meteorológicos em tempo real da OpenWeatherMap para estimar e prever temperatura e umidade.

O projeto combina:

- ✅ Coleta automática de dados meteorológicos
- ✅ Armazenamento em janela deslizante
- ✅ Treinamento de modelo de Regressão Linear
- ✅ Previsão de passos futuros
- ✅ Dashboard interativo em tempo real
- ✅ API REST para consumo dos dados

---

## 📌 Conceito

Um **Sensor Virtual** é um modelo matemático que estima valores futuros com base em dados históricos.  
Neste projeto, utilizamos:

- Regressão Linear (`scikit-learn`)
- Janela deslizante de dados
- Previsão de múltiplos passos à frente
- Atualização contínua via thread

A cada coleta:

1. Dados reais são obtidos da OpenWeatherMap
2. O histórico é atualizado
3. O modelo é treinado (quando há ≥ 3 pontos)
4. São geradas previsões futuras
5. O dashboard é atualizado automaticamente

---

## 🏗 Arquitetura do Projeto

```

sv/
│
├── app.py                # Backend Flask + modelo ML
├── templates/
│   └── index.html        # Dashboard interativo
└── README.md

```

---

## ⚙️ Tecnologias Utilizadas

### Backend
- Python 3
- Flask
- NumPy
- Scikit-learn
- Requests

### Frontend
- Chart.js
- Moment.js
- HTML5 + CSS3
- Fetch API

### API Externa
- OpenWeatherMap

---

## 📊 Funcionalidades

### 🔹 Coleta Contínua
- Intervalo configurável (padrão: 30s)
- Thread dedicada para coleta
- Janela deslizante de até 30 pontos

### 🔹 Modelo de Machine Learning
- Regressão Linear
- Treinado dinamicamente
- Mínimo de 3 pontos para ativação
- Previsão de 6 passos à frente

### 🔹 Dashboard
- KPIs:
  - Temperatura
  - Umidade
  - Pressão
  - Velocidade do vento
- Gráficos:
  - Temperatura real vs previsão
  - Umidade real vs previsão
- Indicador de status do modelo
- Atualização automática

### 🔹 API Interna

Endpoint:

```

GET /api/data

````

Retorna:

```json
{
  "history": {...},
  "forecast": {...},
  "last": {...},
  "model": {...}
}
````

---

## 🚀 Como Executar

### 1️⃣ Clonar o repositório

```bash
git clone https://github.com/vitor-souza-ime/sv.git
cd sv
```

### 2️⃣ Criar ambiente virtual (opcional)

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3️⃣ Instalar dependências

```bash
pip install flask requests numpy scikit-learn
```

### 4️⃣ Configurar variáveis de ambiente (recomendado)

Linux/Mac:

```bash
export OWM_API_KEY="sua_chave"
export OWM_CITY="Rio de Janeiro"
```

Windows:

```bash
set OWM_API_KEY=sua_chave
set OWM_CITY=Rio de Janeiro
```

### 5️⃣ Executar o servidor

```bash
python app.py
```

Acesse:

```
http://localhost:5000
```

---

## 🔧 Configurações Principais

No `app.py`:

```python
INTERVAL = 30        # segundos entre coletas
MAX_HISTORY = 30     # tamanho da janela deslizante
FORECAST_STEPS = 6   # passos futuros previstos
```

---

## 📐 Funcionamento Matemático

O modelo utiliza:

[
y = \beta_0 + \beta_1 x
]

Onde:

* ( x ) = índice temporal
* ( y ) = temperatura ou umidade
* ( \beta_0, \beta_1 ) = coeficientes estimados

A previsão é feita extrapolando os próximos índices temporais.

---

## 🧠 Possíveis Extensões

* Regressão Polinomial
* ARIMA
* LSTM
* Persistência em banco de dados
* Deploy em Docker
* Deploy em nuvem (Render, Railway, AWS)

---

## 🎓 Aplicações Acadêmicas

Este projeto pode ser utilizado em disciplinas como:

* Sistemas Embarcados
* Sistemas Inteligentes
* Aprendizado de Máquina
* Engenharia de Controle
* Sistemas Distribuídos
* Engenharia de Software

---

## 📜 Licença

Uso acadêmico e educacional.

---

## 👨‍🏫 Autor

**Vitor Amadeu Souza**
Engenharia de Computação
Projeto educacional de Sensor Virtual com Machine Learning

