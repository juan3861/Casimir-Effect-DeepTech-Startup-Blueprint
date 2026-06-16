import numpy as np
import matplotlib.pyplot as plt
import os

# Garantir que o diretório assets exista
os.makedirs("../assets", exist_ok=True)

# Parâmetros Físicos (Unidades arbitrárias normalizadas para demonstração visual)
k = 1.0       # Constante da mola de silício (Lei de Hooke)
d0 = 2.0      # Distância de equilíbrio (gap inicial) sem atração
C = 1.2       # Constante da força Casimir (Proporcional à Área e constante de Planck)
rep_C = 0.05  # Repulsão de Pauli (Evita singularidade quando d -> 0)

# ==========================================
# 1. GERANDO O GRÁFICO DO POÇO BIESTÁVEL
# ==========================================
x = np.linspace(0.8, 3.5, 1000)

# Energias Potenciais
U_repulsive = rep_C / x**12
U_spring = 0.5 * k * (x - d0)**2
U_casimir = - C / (x**3)
U_total = U_spring + U_casimir + U_repulsive

plt.figure(figsize=(10, 6), facecolor='#0d1117')
ax = plt.axes()
ax.set_facecolor('#0d1117')

plt.plot(x, U_total, color='#00ff9d', linewidth=3, label='Potencial Total (Mola + Casimir)')
plt.plot(x, U_spring, '--', color='#58a6ff', alpha=0.7, label='Potencial da Mola (Hooke)')
plt.plot(x, U_casimir, '--', color='#ff7b72', alpha=0.7, label='Atração de Casimir')

plt.ylim(-2, 2)
plt.title('POÇO BIESTÁVEL: O "MOTOR" INVISÍVEL DA AETHERIS', color='white', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Distância Gap da Placa (nm)', color='white', fontsize=12)
plt.ylabel('Energia Potencial U(d)', color='white', fontsize=12)
plt.legend(facecolor='#161b22', edgecolor='#30363d', labelcolor='white')
plt.grid(color='#30363d', linestyle='-', linewidth=0.5)
ax.tick_params(colors='white')

plt.tight_layout()
plt.savefig("../assets/bistable_potential.png", dpi=300, bbox_inches='tight')
plt.close()
print("[AETHERIS] Gráfico do Poço Biestável gerado: assets/bistable_potential.png")

# ==========================================
# 2. SIMULAÇÃO DA DINÂMICA DE LANGEVIN (Estocástica)
# ==========================================
dt = 0.01
steps = 8000
time = np.linspace(0, dt*steps, steps)
x_t = np.zeros(steps)
x_t[0] = 1.2  # Inicia na posição de equilíbrio inferior

gamma = 0.8  # Amortecimento viscoso
T = 0.25     # Intensidade do Ruído Ambiental (Vibração térmica/acústica)

def force(x):
    # F = -dU/dx
    # Derivada analítica do potencial
    return -(k*(x-d0) + 3*C/(x**4) - 12*rep_C/(x**13))

# Euler-Maruyama Method para Integração Estocástica
for i in range(1, steps):
    noise = np.random.normal(0, np.sqrt(2 * gamma * T / dt))
    # Aproximação overdamped: dx/dt = (F + ruído) / gamma
    dx = (force(x_t[i-1]) + noise) / gamma * dt
    x_t[i] = x_t[i-1] + dx

# ==========================================
# 3. EXTRAÇÃO DA TENSÃO PIEZOELÉTRICA (HARVESTING)
# ==========================================
# A placa gera voltagem quando há mudanças bruscas de velocidade (os estalos entre os poços)
velocity = np.gradient(x_t)
voltage = np.abs(velocity) * 100  # Fator de conversão piezoelétrico fictício
# Filtramos apenas os picos (colisões)
threshold = np.percentile(voltage, 98)
voltage[voltage < threshold] = 0

# Gráficos de Langevin e Tensão
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True, facecolor='#0d1117')

# Plot Posição
ax1.set_facecolor('#0d1117')
ax1.plot(time, x_t, color='#58a6ff', linewidth=1)
ax1.set_title('RESSONÂNCIA ESTOCÁSTICA DE LANGEVIN (O Ruído Ativando o Efeito Casimir)', color='white', fontsize=14, fontweight='bold')
ax1.set_ylabel('Posição da Placa (nm)', color='white', fontsize=12)
ax1.grid(color='#30363d', linestyle='-', linewidth=0.5)
ax1.tick_params(colors='white')

# Plot Voltagem
ax2.set_facecolor('#0d1117')
ax2.plot(time, voltage, color='#ff7b72', linewidth=1.5)
ax2.fill_between(time, 0, voltage, color='#ff7b72', alpha=0.3)
ax2.set_title('CONVERSÃO PIEZOELÉTRICA (A Bateria Sendo Recarregada Pelo Ruído)', color='white', fontsize=14, fontweight='bold')
ax2.set_ylabel('Voltagem Piezo (mV)', color='white', fontsize=12)
ax2.set_xlabel('Tempo de Operação (ms)', color='white', fontsize=12)
ax2.grid(color='#30363d', linestyle='-', linewidth=0.5)
ax2.tick_params(colors='white')

plt.tight_layout()
plt.savefig("../assets/voltage_generation.png", dpi=300, bbox_inches='tight')
plt.close()
print("[AETHERIS] Gráfico de Conversão Elétrica gerado: assets/voltage_generation.png")
print("[AETHERIS] Simulação Concluída. A termodinâmica está salva.")
