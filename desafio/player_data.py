import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

# Carrega e trata os dados
df = pd.read_csv('player_data.csv')

# Remove linhas com valores ausentes em colunas essenciais
df = df.dropna(subset=['height', 'weight', 'birth_date'])

# Converte altura para centímetros (ex: "6-10" → 208 cm)
def altura_para_cm(valor):
    try:
        feet, inches = valor.split('-')
        return round((int(feet) * 12 + int(inches)) * 2.54, 1)
    except:
        return None

df['height_cm'] = df['height'].apply(altura_para_cm)

# Converte peso para kg
df['weight_kg'] = df['weight'] * 0.453592

# Extrai ano de nascimento
df['birth_year'] = pd.to_datetime(df['birth_date'], errors='coerce').dt.year
df['idade'] = 2024 - df['birth_year']

# Remove valores nulos nas novas colunas
df = df.dropna(subset=['height_cm', 'weight_kg', 'idade'])

# Mapa de tradução para posições
posicoes_traduzidas = {
    'Point Guard': 'Armador',
    'Shooting Guard': 'Ala-Armador',
    'Small Forward': 'Ala-Pivô',
    'Power Forward': 'Ala-Pivô',
    'Center': 'Pivô'
}

# Traduz as posições
df['position'] = df['position'].map(posicoes_traduzidas)

# Cria janela principal
root = tk.Tk()
root.geometry('1200x900')
root.title('Análise de Jogadores')

# Frames
frame_grafico = tk.Frame(root)
frame_grafico.pack(pady=10, fill=tk.BOTH, expand=True)

frame_controle = tk.Frame(root)
frame_controle.pack(pady=10)

frame_resultado = tk.Frame(root)
frame_resultado.pack(pady=10)

label_resultado = tk.Label(frame_resultado, text='', justify=tk.LEFT)
label_resultado.pack()

# Funções auxiliares
def limpar_frame():
    for widget in frame_grafico.winfo_children():
        widget.destroy()

# Gráfico de barras: altura média por posição
def mostrar_barras():
    limpar_frame()
    medias = df.groupby('position')['height_cm'].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5))
    medias.plot(kind='bar', ax=ax, color='skyblue')
    ax.set_title('Altura média por posição')
    ax.set_ylabel('Altura (cm)')
    ax.set_xlabel('Posição')
    ax.set_xticklabels(ax.get_xticklabels())
    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    label_resultado.config(text='Insight: Posições com jogadores mais altos em média.')

# Gráfico de dispersão: altura x peso
def mostrar_dispersao():
    limpar_frame()
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(df['height_cm'], df['weight_kg'], alpha=0.5, color='purple')
    ax.set_xlabel('Altura (cm)')
    ax.set_ylabel('Peso (kg)')
    ax.set_title('Relação entre altura e peso')
    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    label_resultado.config(text='Insight: Jogadores mais altos tendem a pesar mais.')

# Gráfico de pizza: posições mais comuns
def mostrar_pizza():
    limpar_frame()
    posicoes = df['position'].value_counts().head(5)
    fig, ax = plt.subplots(figsize=(6, 6))
    posicoes.plot(kind='pie', autopct='%1.1f%%', ax=ax, startangle=140)
    ax.set_title('Distribuição por posição (Top 5)')
    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    label_resultado.config(text='Insight: Posições mais comuns entre jogadores.')

# Medidas de tendência central
def mostrar_tendencia():
    limpar_frame()
    media_altura = df['height_cm'].mean()
    mediana_altura = df['height_cm'].median()
    moda_altura = df['height_cm'].mode()[0]

    media_peso = df['weight_kg'].mean()
    mediana_peso = df['weight_kg'].median()
    moda_peso = df['weight_kg'].mode()[0]

    texto = (
        f'Altura - Média: {media_altura:.2f} cm | Mediana: {mediana_altura:.2f} cm | Moda: {moda_altura:.2f} cm\n'
        f'Peso   - Média: {media_peso:.2f} kg | Mediana: {mediana_peso:.2f} kg | Moda: {moda_peso:.2f} kg'
    )
    label_resultado.config(text=texto)

# Descrição estatística
def mostrar_descricao():
    limpar_frame()
    descricao = df[['height_cm', 'weight_kg', 'idade']].describe().to_string()
    label_resultado.config(text=f"Descrição estatística:\n{descricao}")

# Previsão de categoria de peso
def previsao():
    limpar_frame()
    df['categoria'] = ['pesado' if x > df['weight_kg'].median() else 'leve' for x in df['weight_kg']]
    X = df[['height_cm', 'idade']]
    y = LabelEncoder().fit_transform(df['categoria'])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)
    acuracia = accuracy_score(y_test, y_pred)

    importancia = pd.Series(modelo.feature_importances_, index=X.columns).sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5))
    importancia.plot(kind='bar', ax=ax, color='green')
    ax.set_title('Importância das características na previsão')
    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    label_resultado.config(text=f"Acurácia da previsão: {acuracia:.2%}\nInsight: Altura e idade influenciam no peso.")

# Botões
ttk.Button(frame_controle, text='Gráfico de Barras', command=mostrar_barras).grid(row=0, column=0, padx=5, pady=5)
ttk.Button(frame_controle, text='Gráfico de Dispersão', command=mostrar_dispersao).grid(row=0, column=1, padx=5, pady=5)
ttk.Button(frame_controle, text='Gráfico de Pizza', command=mostrar_pizza).grid(row=0, column=2, padx=5, pady=5)
ttk.Button(frame_controle, text='Tendência Central', command=mostrar_tendencia).grid(row=0, column=3, padx=5, pady=5)
ttk.Button(frame_controle, text='Descrição Estatística', command=mostrar_descricao).grid(row=0, column=4, padx=5, pady=5)
ttk.Button(frame_controle, text='Previsão (ML)', command=previsao).grid(row=0, column=5, padx=5, pady=5)

# Executa
root.mainloop()
