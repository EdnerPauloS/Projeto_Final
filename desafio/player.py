import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

# Carrega os dados
df = pd.read_csv('players.csv')
df['height'].fillna(df['height'].median(), inplace=True)
df['weight'].fillna(df['weight'].median(), inplace=True)

# Cria janela principal
root = tk.Tk()
root.geometry('1200x900')
root.title('Análise de Jogadores')

# Frames principais
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
    for w in frame_grafico.winfo_children():
        w.destroy()

# Gráfico de barras: Altura média por universidade
def mostrar_barras():
    limpar_frame()
    medias = df.groupby('collage')['height'].mean().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(8, 5))
    medias.plot(kind='bar', ax=ax, color='skyblue')
    ax.set_title('Altura média por universidade')
    ax.set_ylabel('Altura (cm)')
    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack(side='top', fill=tk.BOTH, expand=True)
    label_resultado.config(text='Insight: Universidades com jogadores mais altos em média.')

# Gráfico de dispersão: Altura x Peso
def mostrar_dispersao():
    limpar_frame()
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(df['height'], df['weight'], alpha=0.5, color='purple')
    ax.set_xlabel('Altura (cm)')
    ax.set_ylabel('Peso (kg)')
    ax.set_title('Relação entre altura e peso')
    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack(side='top', fill=tk.BOTH, expand=True)
    label_resultado.config(text='Insight: Jogadores mais altos tendem a ser mais pesados.')

# Gráfico de pizza: Distribuição por estado de nascimento
def mostrar_pizza():
    limpar_frame()
    estados = df['birth_state'].value_counts().dropna().head(20)
    fig, ax = plt.subplots(figsize=(6, 6))
    estados.plot(kind='pie', autopct='%1.1f%%', ax=ax)
    ax.set_ylabel('')
    ax.set_title('Distribuição dos jogadores por estado (top 20)')
    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack(side='top', fill=tk.BOTH, expand=True)
    label_resultado.config(text='Insight: Estados com maior número de jogadores.')

# Medidas de tendência central
def mostrar_tendencia():
    limpar_frame()
    media_altura = df['height'].mean()
    mediana_altura = df['height'].median()
    moda_altura = df['height'].mode()[0]

    media_peso = df['weight'].mean()
    mediana_peso = df['weight'].median()
    moda_peso = df['weight'].mode()[0]

    texto = (
        f'Altura - Média: {media_altura:.2f} cm | Mediana: {mediana_altura:.2f} cm | Moda: {moda_altura} cm\n'
        f'Peso   - Média: {media_peso:.2f} kg | Mediana: {mediana_peso:.2f} kg | Moda: {moda_peso} kg'
    )

    label_resultado.config(text=texto)

# Descrição estatística geral
def mostrar_descricao():
    limpar_frame()
    descricao = df[['height', 'weight']].describe().to_string()
    label_resultado.config(text=f"Descrição estatística:\n{descricao}")

# Previsão usando ML (peso leve/pesado com base em altura e idade)
def previsao():
    limpar_frame()
    df_model = df[['height', 'weight', 'born']].dropna()
    df_model['idade'] = 2024 - df_model['born']
    df_model['categoria'] = ['pesado'
                              if x > df_model['weight'].median()
                              else 'leve' for x in df_model['weight']]
    X = df_model[['height', 'idade']]
    y = LabelEncoder().fit_transform(df_model['categoria'])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)
    acuracia = accuracy_score(y_test, y_pred)

    importancia = pd.Series(modelo.feature_importances_, index=X.columns).sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5))
    importancia.plot(kind='bar', ax=ax, color='green')
    ax.set_title('Importância das características')
    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack(side='top', fill=tk.BOTH, expand=True)
    label_resultado.config(text=f"Acurácia da previsão: {acuracia:.2%}\nInsight: Altura influencia mais que idade no peso.")

# Botões de controle
btn_barras = ttk.Button(frame_controle, text='Gráfico de Barras', command=mostrar_barras)
btn_barras.grid(row=0, column=0, padx=5, pady=5)

btn_disp = ttk.Button(frame_controle, text='Gráfico de Dispersão', command=mostrar_dispersao)
btn_disp.grid(row=0, column=1, padx=5, pady=5)

btn_pizza = ttk.Button(frame_controle, text='Gráfico de Pizza', command=mostrar_pizza)
btn_pizza.grid(row=0, column=2, padx=5, pady=5)

btn_tendencia = ttk.Button(frame_controle, text='Tendência Central', command=mostrar_tendencia)
btn_tendencia.grid(row=0, column=3, padx=5, pady=5)

btn_desc = ttk.Button(frame_controle, text='Descrição', command=mostrar_descricao)
btn_desc.grid(row=0, column=4, padx=5, pady=5)

btn_prev = ttk.Button(frame_controle, text='Previsão ML', command=previsao)
btn_prev.grid(row=0, column=5, padx=5, pady=5)

# Iniciar aplicação
root.mainloop()
