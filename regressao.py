import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mdates
import matplotlib
import time
import os
import getpass
from tkinter import messagebox

matplotlib.use("TkAgg")  

#  Usuários( nome do computador ) e senhas
users = {
    "Casa": "1928",
    "Micro": "1234",
    "juliana": "1234", 
    "widep": "1234",
    "Lucas": "1234",

      
}

def verificar_usuario():
    user = usuario_entry.get()
    password = senha_entry.get()
    if user in users and password == users[user]:
        pc_user = getpass.getuser()
        if pc_user == user:  
            return True
    return False


def autenticar():
    if verificar_usuario():
        autenticacao_janela.destroy()
        criar_grafico()
    else:
        messagebox.showerror("Acesso Negado", "Usuário ou senha incorretos.")

def criar_grafico():
    # Conecta-se ao MetaTrader 5
    if not obter_dados_acao():
        messagebox.showerror("Erro", "Falha na inicialização do MetaTrader 5")
        return


autenticacao_janela = tk.Tk()
autenticacao_janela.title("Autenticação")
autenticacao_janela.geometry("300x200")
autenticacao_janela.configure(bg='black')

usuario_label = tk.Label(autenticacao_janela, text='Usuário:', fg='#FF3399', font=("Arial", 12), bg='black')
usuario_label.pack(pady=10)
usuario_entry = tk.Entry(autenticacao_janela)
usuario_entry.pack(pady=5)

senha_label = tk.Label(autenticacao_janela, text='Senha:', fg='#FF3399',font=("Arial", 12), bg='black')
senha_label.pack(pady=10)
senha_entry = tk.Entry(autenticacao_janela, show="*")
senha_entry.pack(pady=5)

autenticar_button = tk.Button(autenticacao_janela, text='Autenticar', command=autenticar)
autenticar_button.pack(pady=15)

autenticacao_janela.mainloop()



def obter_dados_acao(simbolo_acao, data_inicio, data_fim):
    try:
        # Obtendo os dados da ação do Yahoo Finance
        dados_acao = yf.download(simbolo_acao, start=data_inicio, end=data_fim)
        return dados_acao

    except Exception as e:
        print(f"Ocorreu um erro ao obter os dados: {e}")
        return None


def calcular_dias_corridos(dados_acao):
    primeira_data = dados_acao.index[0]
    dados_acao['Dias'] = (dados_acao.index - primeira_data).days
    return dados_acao


def plotar_regressao_linear(dados_acao, simbolo_acao):
    
    X = dados_acao['Dias'].values.reshape(-1, 1)  # Dias corridos como valor numérico
    y = dados_acao['Close'].values  # Preço de fechamento como variável alvo

    e
    alpha = 0.1  # Parâmetro de regularização (ajuste conforme necessário)
    model = Ridge(alpha=alpha)
    model.fit(X, y)

    
    y_pred = model.predict(X)

    
    plt.figure(figsize=(12, 6))
    plt.scatter(dados_acao.index, dados_acao['Close'], label='Preço de Fechamento Real', color='b', marker='o')
    plt.plot(dados_acao.index, y_pred, label='Regressão Linear (Ridge)', color='r', linewidth=2)
    plt.xlabel('Data')
    plt.ylabel('Preço de Fechamento (R$)')
    plt.title(f'Regressão Linear (Ridge) do Preço de Fechamento da Ação {simbolo_acao}')
    plt.legend()

    
    plt.text(0.05, 0.95, f'Coeficiente Linear (Intercept): {model.intercept_:.2f}\nCoeficiente Angular: {model.coef_[0]:.2f}', 
             transform=plt.gca().transAxes, fontsize=12, verticalalignment='top')
    
    plt.grid()

    
    return plt.gcf()

def plotar_candlestick(dados_acao, simbolo_acao):
    
    dados_acao['DataNum'] = mdates.date2num(dados_acao.index.to_pydatetime())

    
    plt.figure(figsize=(12, 6))
    candlestick_ohlc(plt.gca(), dados_acao[['DataNum', 'Open', 'High', 'Low', 'Close']].values, width=0.6, colorup='g', colordown='r')
    plt.xlabel('Data')
    plt.ylabel('Preço (R$)')
    plt.title(f'Gráfico de Candlestick da Ação {simbolo_acao}')
    plt.grid()

    
    return plt.gcf()


def criar_janela_tkinter():
    def definir_estilo_customizado():
        estilo = ttk.Style()

        
        estilo.configure(".", background="black", foreground="violet")

       
        estilo.configure("TCombobox", fieldbackground="neon blue", foreground="black")

       
        estilo.configure("TEntry", fieldbackground="neon blue", foreground="black")

         
        autenticacao_janela.mainloop()
        
    def atualizar_graficos():
        simbolo_acao = var_simbolo_acao.get()
        data_inicio = var_data_inicio.get()
        data_fim = var_data_fim.get()

        dados_acao = obter_dados_acao(simbolo_acao, data_inicio, data_fim)
        if dados_acao is not None:
            dados_acao = calcular_dias_corridos(dados_acao)

           
            fig_regressao_linear = plotar_regressao_linear(dados_acao, simbolo_acao)
            fig_candlestick = plotar_candlestick(dados_acao, simbolo_acao)

          
            janela_regressao_linear = tk.Toplevel()
            janela_regressao_linear.title("Regressão Linear")
            canvas_regressao_linear = FigureCanvasTkAgg(fig_regressao_linear, master=janela_regressao_linear)
            canvas_regressao_linear.draw()
            canvas_regressao_linear.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

            janela_candlestick = tk.Toplevel()
            janela_candlestick.title("Candlestick")
            canvas_candlestick = FigureCanvasTkAgg(fig_candlestick, master=janela_candlestick)
            canvas_candlestick.draw()
            canvas_candlestick.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    janela = tk.Tk()
    janela.title("Regressão Linear e Candlestick - Escolha o Ativo e as Datas")
    janela.configure(bg="black")  

    
    var_simbolo_acao = tk.StringVar()
    var_data_inicio = tk.StringVar()
    var_data_fim = tk.StringVar()

    lbl_simbolo_acao = ttk.Label(janela, text="Selecione o Ativo:")
    lbl_simbolo_acao.grid(row=0, column=0, padx=5, pady=5)

    cmb_simbolo_acao = ttk.Combobox(janela, textvariable=var_simbolo_acao, values=[
        "^BVSP", "BRL=X", "ALPA4.SA", "ASAI3.SA", "AZUL4.SA", "B3SA3.SA", "BBAS3.SA", "BBDC3.SA", "BBDC4.SA", "BBSE3.SA", "BEEF3.SA", "BPAC11.SA", "BRAP4.SA", "BRFS3.SA", "BRKM5.SA", "CASH3.SA", "CCRO3.SA", "CIEL3.SA", "CMIG4.SA", "CMIN3.SA", "COGN3.SA", "CPFE3.SA", "CPLE6.SA", "CRFB3.SA", "CSAN3.SA", "CSNA3.SA", "CYRE3.SA", "DXCO3.SA", "ELET3.SA", "ELET6.SA", "EMBR3.SA", "ENEV3.SA", "ENBR3.SA", "ENGI11.SA", "EQTL3.SA", "EZTC3.SA", "FLRY3.SA", "GGBR4.SA", "GOLL4.SA", "GOAU4.SA", "HAPV3.SA", "HYPE3.SA", "IGTI11.SA", "IRBR3.SA", "ITSA4.SA", "ITUB4.SA", "JBSS3.SA", "KLBN11.SA", "LREN3.SA", "LWSA3.SA", "MGLU3.SA", "MRFG3.SA", "MRVE3.SA", "NTCO3.SA", "PCAR3.SA", "PETR3.SA", "PETR4.SA", "PETZ3.SA", "PRIO3.SA", "RADL3.SA", "RAIL3.SA", "RAIZ4.SA", "RDOR3.SA", "RENT3.SA", "RRRP3.SA", "SANB11.SA", "SBSP3.SA", "SLCE3.SA", "SMTO3.SA", "SOMA3.SA", "SUZB3.SA", "TAEE11.SA", "TIMS3.SA", "TOTS3.SA", "UGPA3.SA", "USIM5.SA", "VALE3.SA", "VBBR3.SA", "VIIA3.SA", "VIVT3.SA", "WEGE3.SA", "YDUQ3.SA"
    ])
    cmb_simbolo_acao.grid(row=0, column=1, padx=5, pady=5)
    cmb_simbolo_acao.set("^BVSP")  

    lbl_data_inicio = ttk.Label(janela, text="Data de Início:")
    lbl_data_inicio.grid(row=1, column=0, padx=5, pady=5)

    ent_data_inicio = ttk.Entry(janela, textvariable=var_data_inicio)
    ent_data_inicio.grid(row=1, column=1, padx=5, pady=5)
    ent_data_inicio.insert(0, "2021-01-01")  

    lbl_data_fim = ttk.Label(janela, text="Data Final:")
    lbl_data_fim.grid(row=2, column=0, padx=5, pady=5)

    ent_data_fim = ttk.Entry(janela, textvariable=var_data_fim)
    ent_data_fim.grid(row=2, column=1, padx=5, pady=5)
    ent_data_fim.insert(0, "2023-08-01")  

    btn_atualizar = ttk.Button(janela, text="Atualizar Gráficos", command=atualizar_graficos)
    btn_atualizar.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

    
    definir_estilo_customizado()

    janela.mainloop()

if __name__ == "__main__":
    criar_janela_tkinter()


