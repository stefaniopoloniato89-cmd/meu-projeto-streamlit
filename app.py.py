import pandas as pd
import numpy as np

def get_basic_stats(df):
    """Calcula estatísticas descritivas básicas."""
    if df.empty: return None
    # Calculando a moda e pegando o primeiro valor se houver múltiplos
    mode_series = df['multiplier'].mode()
    mode_val = mode_series.iloc[0] if not mode_series.empty else np.nan
    
    return {
        'Média': df['multiplier'].mean(),
        'Mediana': df['multiplier'].median(),
        'Moda': mode_val,
        'Desvio Padrão': df['multiplier'].std()
    }

def get_frequencies(df):
    """Calcula a distribuição de probabilidade empírica por faixas."""
    if df.empty: return None
    bins = [0, 1.499, 1.999, 4.999, float('inf')]
    labels = ['< 1.5x', '1.5x - 2.0x', '2.0x - 5.0x', '> 5.0x']
    
    # Criando faixas
    faixas = pd.cut(df['multiplier'], bins=bins, labels=labels)
    
    # Calculando porcentagem
    freq = faixas.value_counts(normalize=True) * 100
    return freq.to_dict()

def check_alerts(df):
    """Gera alertas baseados em comportamento recente de risco."""
    alerts = []
    if df.empty or len(df) < 5: 
        return alerts
        
    recent_5 = df.tail(5)['multiplier'].values
    recent_10 = df.tail(10)['multiplier'].values
    
    # Alerta de Sequência de Perdas (Red Streak)
    if all(x < 2.0 for x in recent_5):
        alerts.append(("⚠️ ALERTA", "Sequência de 5+ rodadas abaixo de 2.0x. Alto risco de viés da falácia do apostador."))
        
    # Alerta de Volatilidade (Desvio padrão alto no curto prazo)
    if len(recent_10) == 10 and np.std(recent_10) > 3.0:
         alerts.append(("📈 VOLATILIDADE", "Alta oscilação detectada nas últimas 10 rodadas. Sugestão: Pausa na sessão."))
         
    return alerts