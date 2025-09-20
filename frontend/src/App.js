import React, { useState } from 'react';
import './App.css';

const traducoes = {
  pt: {
    titulo: "Calculator Aquae Sumptionis",
    peso: "Peso (kg):",
    idade: "Idade:",
    atividade: "Atividade:",
    sedentario: "Sedentário",
    ativo: "Ativo",
    clima: "Clima:",
    normal: "Normal",
    quente: "Quente",
    frio: "Frio",
    calcular: "Calcular",
    metaDiaria: "Meta diária:",
    mais250ml: "+250ml",
    mais350ml: "+350ml",
    mais500ml: "+500ml",
    mais1l: "+1 L"
  },
  en: {
    titulo: "Water Intake Calculator",
    peso: "Weight (kg):",
    idade: "Age:",
    atividade: "Activity:",
    sedentario: "Sedentary",
    ativo: "Active",
    clima: "Climate:",
    normal: "Normal",
    quente: "Hot",
    frio: "Cold",
    calcular: "Calculate",
    metaDiaria: "Daily goal:",
    mais250ml: "+250ml",
    mais350ml: "+350ml",
    mais500ml: "+500ml",
    mais1l: "+1 L"
  },
  es: {
    titulo: "Calculadora de Consumo de Agua",
    peso: "Peso (kg):",
    idade: "Edad:",
    atividade: "Actividad:",
    sedentario: "Sedentario",
    ativo: "Activo",
    clima: "Clima:",
    normal: "Normal",
    quente: "Caliente",
    frio: "Frío",
    calcular: "Calcular",
    metaDiaria: "Meta diaria:",
    mais250ml: "+250ml",
    mais350ml: "+350ml",
    mais500ml: "+500ml",
    mais1l: "+1 L"
  }
};

function App() {
  // Detecta idioma do navegador
  const idiomaBrowser = navigator.language.slice(0, 2);
  const idiomasSuportados = ['pt', 'en', 'es'];

  const [idioma] = useState(
    idiomasSuportados.includes(idiomaBrowser) ? idiomaBrowser : 'pt'
  );

  const [peso, setPeso] = useState('');
  const [idade, setIdade] = useState('');
  const [atividade, setAtividade] = useState('sedentario');
  const [clima, setClima] = useState('normal');
  const [resultado, setResultado] = useState(null);
  const [consumido, setConsumido] = useState(0);

  const calcularAgua = async () => {
    try {
      const response = await fetch('https://cas-hygy.onrender.com/calcular', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ peso, idade, atividade, clima })
      });

      if (!response.ok) {
        const errorData = await response.json();
        alert(errorData.erro || 'Erro na API');
        return;
      }

      const data = await response.json();
      setResultado(data.agua_recomendada.toFixed(2));
      setConsumido(0);
    } catch (error) {
      alert('Erro ao conectar com o servidor');
      console.error(error);
    }
  }

  return (
    <div className="App">
      <h1>{traducoes[idioma].titulo}</h1>

      <div>
        <label>{traducoes[idioma].peso} </label>
        <input type="number" value={peso} onChange={(e) => setPeso(e.target.value)} />
      </div>

      <div>
        <label>{traducoes[idioma].idade} </label>
        <input type="number" value={idade} onChange={(e) => setIdade(e.target.value)} />
      </div>

      <div>
        <label>{traducoes[idioma].atividade} </label>
        <select value={atividade} onChange={(e) => setAtividade(e.target.value)}>
          <option value="sedentario">{traducoes[idioma].sedentario}</option>
          <option value="ativo">{traducoes[idioma].ativo}</option>
        </select>
      </div>

      <div>
        <label>{traducoes[idioma].clima} </label>
        <select value={clima} onChange={(e) => setClima(e.target.value)}>
          <option value="normal">{traducoes[idioma].normal}</option>
          <option value="quente">{traducoes[idioma].quente}</option>
          <option value="frio">{traducoes[idioma].frio}</option>
        </select>
      </div>

      <button onClick={calcularAgua}>{traducoes[idioma].calcular}</button>

      {resultado && (
        <div style={{ marginTop: '20px' }}>
          <h2>{traducoes[idioma].metaDiaria} {resultado} L</h2>

          <div className="progress-container">
            <div
              className="progress-bar"
              style={{ width: `${Math.min((consumido / resultado) * 100, 100)}%` }}
            />
            <div className="progress-text">{consumido.toFixed(2)} L</div>
          </div>

          <div style={{ marginTop: '15px' }}>
            <button onClick={() => setConsumido(consumido + 0.25)} style={{ marginRight: '10px' }}>
              {traducoes[idioma].mais250ml}
            </button>
            <button onClick={() => setConsumido(consumido + 0.35)} style={{ marginRight: '10px' }}>
              {traducoes[idioma].mais350ml}
            </button>
            <button onClick={() => setConsumido(consumido + 0.5)} style={{ marginRight: '10px' }}>
              {traducoes[idioma].mais500ml}
            </button>
            <button onClick={() => setConsumido(consumido + 1)}>
              {traducoes[idioma].mais1l}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
