from flask import Flask, render_template_string, request, jsonify
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

# --- Carrega e prepara os dados ---
data = pd.read_csv('2nd_vinicius/Integrantes/imovel_limpo.csv')
dados = pd.DataFrame({
    'quartos': list(data.get('Quartos')),
    'suites': list(data.get('Suítes')),
    'area': list(data.get('Área do imóvel')),
    'tipo': list(data.get('Tipo do imóvel')),
    'bairro': list(data.get('Bairro')),
    'preco': list(data.get('Preço'))
})
dados = dados.dropna()

# --- Limpeza dos dados numéricos ---
dados['area'] = (
    dados['area']
    .astype(str)
    .str.replace('m²', '', regex=False)
    .str.replace(' ', '', regex=False)
    .str.replace(',', '.', regex=False)
    .astype(float)
)
dados['preco'] = (
    dados['preco']
    .astype(str)
    .str.replace('R$', '', regex=False)
    .str.replace(' ', '', regex=False)
    .str.replace(',00', '', regex=False)
    .str.replace('.', '', regex=False)
    .astype(float)
)

X = dados[['quartos', 'suites', 'area', 'tipo', 'bairro']]
y = dados['preco']

colunas_categoricas = ['bairro', 'tipo']
preprocessador = ColumnTransformer([
    ('cat', OneHotEncoder(drop='first', handle_unknown='ignore'), colunas_categoricas)
], remainder='passthrough')

# --- Treina o modelo com todos os dados primeiro para conhecer todas as categorias ---
preprocessador.fit(X)

# --- Divide treino/teste ---
X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.2, random_state=42)
modelo = LinearRegression()
modelo.fit(preprocessador.transform(X_treino), y_treino)

score_r2 = modelo.score(preprocessador.transform(X_teste), y_teste)

# --- Obtém valores únicos para os selects ---
tipos_imovel = sorted(data['Tipo do imóvel'].dropna().unique())
bairros = sorted(data['Bairro'].dropna().unique())

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculadora de Preço de Imóveis</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Courier New', monospace;
            background: #000;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: #fff;
            border: 3px solid #000;
            padding: 40px;
            max-width: 500px;
            width: 100%;
        }
        
        h1 {
            color: #000;
            margin-bottom: 5px;
            font-size: 32px;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: -2px;
        }
        
        .subtitle {
            color: #000;
            margin-bottom: 30px;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 5px;
            color: #000;
            font-weight: 700;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        input, select {
            width: 100%;
            padding: 12px;
            border: 2px solid #000;
            background: #fff;
            font-size: 16px;
            font-family: 'Courier New', monospace;
        }
        
        input:focus, select:focus {
            outline: none;
            background: #f0f0f0;
        }
        
        button {
            width: 100%;
            padding: 15px;
            background: #000;
            color: #fff;
            border: 3px solid #000;
            font-size: 14px;
            font-weight: 700;
            cursor: pointer;
            text-transform: uppercase;
            letter-spacing: 2px;
            font-family: 'Courier New', monospace;
            transition: all 0.2s;
        }
        
        button:hover {
            background: #fff;
            color: #000;
        }
        
        button:active {
            transform: translate(2px, 2px);
        }
        
        .result {
            margin-top: 30px;
            padding: 20px;
            background: #000;
            color: #fff;
            border: 3px solid #000;
            display: none;
        }
        
        .result h2 {
            font-size: 12px;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        
        .result .price {
            font-size: 36px;
            font-weight: 900;
            letter-spacing: -2px;
        }
        
        .stats {
            margin-top: 20px;
            padding: 15px;
            background: #f0f0f0;
            border: 2px solid #000;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .loading {
            display: none;
            margin-top: 20px;
            color: #000;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>CALCULADORA DE IMÓVEIS</h1>
        <p class="subtitle">Preço estimado com machine learning</p>
        
        <form id="imovelForm">
            <div class="form-group">
                <label for="quartos">Número de Quartos</label>
                <input type="number" id="quartos" name="quartos" min="0" required>
            </div>
            
            <div class="form-group">
                <label for="suites">Número de Suítes</label>
                <input type="number" id="suites" name="suites" min="0" required>
            </div>
            
            <div class="form-group">
                <label for="area">Área (m²)</label>
                <input type="number" id="area" name="area" min="1" required>
            </div>
            
            <div class="form-group">
                <label for="tipo">Tipo do Imóvel</label>
                <select id="tipo" name="tipo" required>
                    <option value="">Selecione...</option>
                    {% for tipo in tipos %}
                    <option value="{{ tipo }}">{{ tipo }}</option>
                    {% endfor %}
                </select>
            </div>
            
            <div class="form-group">
                <label for="bairro">Bairro</label>
                <select id="bairro" name="bairro" required>
                    <option value="">Selecione...</option>
                    {% for bairro in bairros %}
                    <option value="{{ bairro }}">{{ bairro }}</option>
                    {% endfor %}
                </select>
            </div>
            
            <button type="submit">Calcular Preço</button>
        </form>
        
        <div class="loading" id="loading">Calculando...</div>
        
        <div class="result" id="result">
            <h2>Preço Estimado</h2>
            <div class="price" id="preco"></div>
        </div>
        
        <div class="stats">
            <strong>Precisão do Modelo:</strong> R² = {{ "%.2f"|format(score_r2 * 100) }}%
        </div>
    </div>
    
    <script>
        document.getElementById('imovelForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const loading = document.getElementById('loading');
            const result = document.getElementById('result');
            const preco = document.getElementById('preco');
            
            loading.style.display = 'block';
            result.style.display = 'none';
            
            const formData = {
                quartos: document.getElementById('quartos').value,
                suites: document.getElementById('suites').value,
                area: document.getElementById('area').value,
                tipo: document.getElementById('tipo').value,
                bairro: document.getElementById('bairro').value
            };
            
            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });
                
                const data = await response.json();
                
                loading.style.display = 'none';
                preco.textContent = data.preco;
                result.style.display = 'block';
            } catch (error) {
                loading.style.display = 'none';
                alert('Erro ao calcular o preço. Tente novamente.');
            }
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, tipos=tipos_imovel, bairros=bairros, score_r2=score_r2)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    
    novo = pd.DataFrame({
        'quartos': [int(data['quartos'])],
        'suites': [int(data['suites'])],
        'area': [float(data['area'])],
        'tipo': [data['tipo']],
        'bairro': [data['bairro']]
    })
    
    preco_previsto = modelo.predict(preprocessador.transform(novo))
    
    return jsonify({
        'preco': f"R$ {preco_previsto[0]:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    })

if __name__ == '__main__':
    print(f"\n{'='*50}")
    print(f"🏠 Servidor de Predição de Imóveis")
    print(f"{'='*50}")
    print(f"📊 Score R² do modelo: {score_r2:.4f}")
    print(f"🌐 Acesse: http://localhost:5000")
    print(f"{'='*50}\n")
    app.run(debug=True, use_reloader=False)