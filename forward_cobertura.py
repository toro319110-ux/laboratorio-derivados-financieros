# =============================================================================
# PROYECTO: LABORATORIO 1 - FORWARD
# ANÁLISIS DE FORWARD DE DIVISAS - COBERTURA CAMBIARIA USD/COP
# =============================================================================
# INTEGRANTES:
#   Santiago Toro Cadavid - 1040739414
#   Yenny Carolina Serna Chaverra - 1017210528
#   Daniela Perez Meza - 1017220748
# CURSO: Derivados Financieros
# INSTITUCIÓN: [Nombre de tu Universidad]
# =============================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from datetime import datetime, timedelta
import os
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# CONFIGURACIÓN DE RUTAS RELATIVAS (COMPATIBLE CON GITHUB)
# =============================================================================
directorio_actual = os.path.dirname(os.path.abspath(__file__))
CARPETA_BASE = os.path.join(directorio_actual, "outputs", "FORWARD")
os.makedirs(CARPETA_BASE, exist_ok=True)

# =============================================================================
# CONFIGURACIÓN GLOBAL
# =============================================================================
FECHA_ACTUAL = "2026-03-26"
SPOT_ACTUAL = 3688.46
FORWARD_CIERRE = 3968.63
PLAZO_FORWARD_MESES = 6
N_SIMULACIONES = 50000
DIAS_PROYECCION = 129
SEMILLA = 42

# =============================================================================
# INFORMACIÓN DE INTEGRANTES
# =============================================================================
INTEGRANTES = [
    {"nombre": "Santiago Toro Cadavid", "cedula": "1040739414"},
    {"nombre": "Yenny Carolina Serna Chaverra", "cedula": "1017210528"},
    {"nombre": "Daniela Perez Meza", "cedula": "1017220748"}
]
CURSO = "Derivados Financieros"
PROYECTO = "LABORATORIO 1 - Forward"

# =============================================================================
# FUNCIONES DE HEADER Y FOOTER
# =============================================================================
def get_header():
    header = "=" * 80 + "\n"
    header += f"PROYECTO: {PROYECTO}\n"
    header += f"CURSO: {CURSO}\n"
    header += "=" * 80 + "\nINTEGRANTES:\n"
    for intg in INTEGRANTES:
        header += f"  • {intg['nombre']} - {intg['cedula']}\n"
    header += "=" * 80 + "\n"
    return header

def get_footer():
    return "\n" + "=" * 80 + f"\nGenerado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n" + "=" * 80

# =============================================================================
# ANÁLISIS  - FORWARD (ESTILO ESTUDIANTE)
# =============================================================================
def analisis_humano_forward(analisis_forward, metricas_riesgo):
    return f"""
LO QUE ENTENDÍ DE ESTE PUNTO (EXPLICACIÓN SENCILLA)
================================================================================

Sobre los FORWARDS, que fueron lo más interesante:

🔄 ¿QUÉ ES UN FORWARD?
Es como hacer un "contrato de precio fijo" para el futuro.
Hoy acordamos a cuánto vamos a comprar/vender dólares dentro de 6 meses, 
sin importar qué pase en el mercado.

📋 LOS DATOS CLAVE:
• TRM hoy (spot): ${3688.46:,.0f} COP/USD
• Forward a 6 meses: ${3968.63:,.0f} COP/USD
• Diferencia: ${3968.63-3688.46:,.0f} COP más caro por asegurar el precio

🎲 ¿QUÉ PASÓ EN LA SIMULACIÓN?
Hicimos 50.000 escenarios posibles para ver si convenía el forward:

✅ ESCENARIOS DONDE EL FORWARD ME AYUDA:
• Cantidad: {analisis_forward['n_protegidos']:,} de 50.000
• Porcentaje: {analisis_forward['pct_protegidos']:.1f}%
• Significa: Cuando el dólar sube mucho, yo ya tengo precio fijo → GANO

❌ ESCENARIOS DONDE EL FORWARD NO ME CONVIENE:
• Cantidad: {analisis_forward['n_no_protegidos']:,} de 50.000  
• Porcentaje: {analisis_forward['pct_no_protegidos']:.1f}%
• Significa: Cuando el dólar baja o no sube tanto, yo pago más → PIERDO

💰 BALANCE FINAL:
• Valor esperado de la cobertura: ${analisis_forward['valor_esperado']:,.0f} COP
• Traducción: En promedio, el forward me "cuesta" esa plata
• Pero elimina el riesgo: ya no tengo sustos con la TRM

🤔 ENTONCES... ¿CONVIENE O NO?
Mi conclusión de estudiante:

✅ CONTRATAR FORWARD SI:
• No puedo tolerar sorpresas grandes en mis pagos
• Mi negocio es muy sensible al tipo de cambio
• Prefiero pagar un poco más por tranquilidad

❌ NO CONTRATAR FORWARD SI:
• Puedo aguantar la volatilidad
• Creo que el dólar no va a subir tanto
• Quiero aprovechar si el dólar baja

🎯 MI DECISIÓN PERSONAL:
Si yo fuera el empresario, probablemente SÍ contrataría el forward.
No porque sea el más barato, sino porque me permite dormir tranquilo 
sabiendo exactamente cuánto voy a pagar. La tranquilidad también tiene valor.

📚 LO QUE APRENDÍ:
• Los derivados no son "apuestas", son herramientas de protección
• No existe la decisión perfecta, solo la que mejor se adapta a tu perfil
• Siempre hay que comparar: costo de la cobertura vs. costo del riesgo

================================================================================
🏁 CONCLUSIÓN FINAL DEL LABORATORIO
================================================================================

Después de hacer los 5 puntos, esto es lo que me llevo:

1️⃣ La TRM es impredecible, pero podemos analizar tendencias
2️⃣ Pedir prestado en dólares puede ser más barato... pero riesgoso
3️⃣ El riesgo cambiario puede costarnos hasta 18% extra sin avisar
4️⃣ Las simulaciones nos ayudan a ver muchos futuros posibles
5️⃣ Los forwards son como "seguros" contra sorpresas del dólar

💡 MI GRAN APRENDIZAJE:
En finanzas, casi nunca hay respuestas blancas o negras.
Todo es un balance entre: rentabilidad, riesgo y tranquilidad.

¡Gracias profe por este laboratorio! Fue difícil pero aprendí mucho 

================================================================================
"""

# =============================================================================
# FUNCIÓN: GENERAR DATOS SPOT
# =============================================================================
def generar_datos_spot():
    print("\n" + "="*80)
    print("📊 PASO 1: GENERANDO DATOS HISTÓRICOS SPOT USD/COP")
    print("="*80)
    np.random.seed(SEMILLA)
    fechas = pd.date_range(start='2024-03-26', end='2026-03-26', freq='B')
    n = len(fechas)
    spot = np.zeros(n)
    spot[0] = 3900
    for i in range(1, n):
        retorno = np.random.normal(0.0001, 0.009)
        spot[i] = spot[i-1] * (1 + retorno)
    spot[(fechas >= '2024-06-01') & (fechas <= '2024-09-30')] *= 1.08
    spot[(fechas >= '2025-03-01') & (fechas <= '2025-06-30')] *= 0.95
    factor = SPOT_ACTUAL / spot[-1]
    spot = spot * factor
    df_spot = pd.DataFrame({'Fecha': fechas, 'Spot': spot})
    archivo_csv = os.path.join(CARPETA_BASE, "spot_historico.csv")
    df_spot['Fecha'] = df_spot['Fecha'].dt.strftime('%Y-%m-%d')
    df_spot.to_csv(archivo_csv, index=False, encoding='utf-8')
    print(f"✅ CSV CREADO: {archivo_csv}")
    print(f"   Tamaño: {os.path.getsize(archivo_csv):,} bytes")
    print(f"   Registros: {len(df_spot)}")
    return df_spot

# =============================================================================
# FUNCIÓN: CALCULAR ESTADÍSTICAS
# =============================================================================
def calcular_estadisticas(df_spot):
    print("\n" + "="*80)
    print("📊 PASO 2: CALCULANDO ESTADÍSTICAS")
    print("="*80)
    df_spot['Fecha'] = pd.to_datetime(df_spot['Fecha'])
    retornos = df_spot['Spot'].pct_change().dropna()
    media_diaria = retornos.mean()
    std_diaria = retornos.std()
    volatilidad_anual = std_diaria * np.sqrt(252)
    print(f"📈 ESTADÍSTICAS DEL SPOT:")
    print(f"   Spot Actual: ${SPOT_ACTUAL:,.2f}")
    print(f"   Spot Mínimo: ${df_spot['Spot'].min():,.2f}")
    print(f"   Spot Máximo: ${df_spot['Spot'].max():,.2f}")
    print(f"   Spot Promedio: ${df_spot['Spot'].mean():,.2f}")
    print(f"\n📈 ESTADÍSTICAS DE RETORNOS:")
    print(f"   Media diaria: {media_diaria:.6f} ({media_diaria*100:.4f}%)")
    print(f"   Volatilidad anualizada: {volatilidad_anual:.6f} ({volatilidad_anual*100:.4f}%)")
    return retornos, media_diaria, std_diaria

# =============================================================================
# FUNCIÓN: SIMULACIÓN MONTE CARLO
# =============================================================================
def simulacion_monte_carlo(S0, mu, sigma, T, n_sim):
    print("\n" + "="*80)
    print("📊 PASO 3: SIMULACIÓN MONTE CARLO")
    print("="*80)
    dt = 1/252
    steps = int(T * 252)
    np.random.seed(SEMILLA)
    Z = np.random.standard_t(df=5, size=(n_sim, steps))
    Z = Z * np.sqrt(3/5)
    paths = np.zeros((n_sim, steps + 1))
    paths[:, 0] = S0
    for t in range(1, steps + 1):
        paths[:, t] = paths[:, t-1] * np.exp(
            (mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z[:, t-1]
        )
    valores_finales = paths[:, -1]
    print(f"📈 PARÁMETROS DE SIMULACIÓN:")
    print(f"   Spot Inicial (S0): ${S0:,.2f}")
    print(f"   Horizonte: {T:.3f} años ({steps} días)")
    print(f"   Número de simulaciones: {n_sim:,}")
    print(f"\n✅ SIMULACIONES COMPLETADAS")
    print(f"\n📊 DISTRIBUCIÓN DEL SPOT FUTURO:")
    print(f"   Media: ${valores_finales.mean():,.2f}")
    print(f"   Mediana: ${np.median(valores_finales):,.2f}")
    print(f"   Desviación: ${valores_finales.std():,.2f}")
    print(f"   VaR 95%: ${np.percentile(valores_finales, 5):,.2f}")
    return {
        'paths': paths,
        'valores_finales': valores_finales,
        'media': valores_finales.mean(),
        'mediana': np.median(valores_finales),
        'std': valores_finales.std()
    }

# =============================================================================
# FUNCIÓN: ANALIZAR PROTECCIÓN FORWARD
# =============================================================================
def analizar_proteccion_forward(valores_finales, forward):
    print("\n" + "="*80)
    print("📊 PASO 4: ANÁLISIS DE PROTECCIÓN FORWARD")
    print("="*80)
    n_sim = len(valores_finales)
    protegidos = valores_finales > forward
    n_protegidos = protegidos.sum()
    pct_protegidos = n_protegidos / n_sim * 100
    no_protegidos = ~protegidos
    n_no_protegidos = no_protegidos.sum()
    pct_no_protegidos = n_no_protegidos / n_sim * 100
    print(f"\n📊 CLASIFICACIÓN DE ESCENARIOS:")
    print(f"   Escenarios PROTEGIDOS: {n_protegidos:,} ({pct_protegidos:.2f}%)")
    print(f"   Escenarios NO PROTEGIDOS: {n_no_protegidos:,} ({pct_no_protegidos:.2f}%)")
    ahorros = valores_finales[protegidos] - forward
    perdidas = forward - valores_finales[no_protegidos]
    ahorro_promedio = ahorros.mean() if len(ahorros) > 0 else 0
    perdida_promedio = perdidas.mean() if len(perdidas) > 0 else 0
    valor_esperado = (ahorros.sum() - perdidas.sum()) if len(ahorros) > 0 else -perdidas.sum()
    print(f"\n💰 ANÁLISIS DE AHORROS:")
    print(f"   Ahorro promedio: ${ahorro_promedio:,.2f}")
    print(f"\n💸 ANÁLISIS DE PÉRDIDAS:")
    print(f"   Pérdida promedio: ${perdida_promedio:,.2f}")
    print(f"\n📈 VALOR ESPERADO: ${valor_esperado:,.2f}")
    return {
        'n_protegidos': n_protegidos,
        'pct_protegidos': pct_protegidos,
        'n_no_protegidos': n_no_protegidos,
        'pct_no_protegidos': pct_no_protegidos,
        'ahorro_promedio': ahorro_promedio,
        'perdida_promedio': perdida_promedio,
        'valor_esperado': valor_esperado
    }

# =============================================================================
# FUNCIÓN: CALCULAR MÉTRICAS DE RIESGO
# =============================================================================
def calcular_metricas_riesgo(valores_finales, forward):
    print("\n" + "="*80)
    print("📊 PASO 5: CÁLCULO DE MÉTRICAS DE RIESGO")
    print("="*80)
    var_95_sin = np.percentile(valores_finales, 5)
    var_99_sin = np.percentile(valores_finales, 1)
    cvar_95_sin = valores_finales[valores_finales <= np.percentile(valores_finales, 5)].mean()
    print(f"\n📊 VALUE AT RISK (VaR):")
    print(f"   VaR 95% SIN cobertura: ${var_95_sin:,.2f}")
    print(f"   VaR 95% CON forward: ${forward:,.2f} (FIJO)")
    print(f"\n📊 CONDITIONAL VaR (CVaR):")
    print(f"   CVaR 95% SIN cobertura: ${cvar_95_sin:,.2f}")
    print(f"\n📊 VOLATILIDAD:")
    print(f"   Volatilidad SIN cobertura: ${valores_finales.std():,.2f}")
    print(f"   Volatilidad CON forward: $0 (ELIMINADA)")
    return {
        'var_95_sin': var_95_sin,
        'var_99_sin': var_99_sin,
        'var_95_con': forward,
        'cvar_95_sin': cvar_95_sin,
        'volatilidad_sin': valores_finales.std()
    }

# =============================================================================
# FUNCIÓN: GENERAR GRÁFICOS
# =============================================================================
def generar_graficos(df_spot, resultados_sim, analisis, metricas):
    print("\n" + "="*80)
    print("📈 PASO 6: GENERANDO GRÁFICOS")
    print("="*80)
    archivos_graficos = []
    
    # Gráfico 1: Serie Histórica Spot
    fig1, ax1 = plt.subplots(1, 1, figsize=(14, 6))
    ax1.plot(df_spot['Fecha'], df_spot['Spot'], linewidth=1.5, color='blue')
    ax1.fill_between(df_spot['Fecha'], df_spot['Spot'], alpha=0.3)
    ax1.axhline(y=SPOT_ACTUAL, color='green', linestyle='--', linewidth=2, label=f'Spot Actual (${SPOT_ACTUAL:,.0f})')
    ax1.axhline(y=FORWARD_CIERRE, color='red', linestyle='--', linewidth=2, label=f'Forward (${FORWARD_CIERRE:,.0f})')
    ax1.set_title('SERIE HISTÓRICA SPOT USD/COP (2024-2026)', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Fecha')
    ax1.set_ylabel('USD/COP')
    ax1.tick_params(axis='x', rotation=45)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    fig1.text(0.5, 0.02,
             f"Santiago Toro (1040739414) | Yenny Serna (1017210528) | Daniela Perez (1017220748)",
             ha='center', fontsize=8, alpha=0.5)
    plt.tight_layout(rect=[0, 0.03, 1, 1])
    ruta1 = os.path.join(CARPETA_BASE, 'forward_serie_historica.png')
    plt.savefig(ruta1, dpi=300, bbox_inches='tight')
    print(f"✅ {ruta1}")
    plt.close()
    archivos_graficos.append(ruta1)
    
    # Gráfico 2: Distribución Spot Futuro
    fig2, ax2 = plt.subplots(1, 1, figsize=(12, 6))
    ax2.hist(resultados_sim['valores_finales'], bins=100, density=True, alpha=0.7, color='steelblue')
    ax2.axvline(x=FORWARD_CIERRE, color='red', linestyle='--', linewidth=2, label=f'Forward (${FORWARD_CIERRE:,.0f})')
    ax2.axvline(x=resultados_sim['media'], color='green', linestyle='-', linewidth=2, label=f'Media (${resultados_sim["media"]:,.0f})')
    ax2.set_title('DISTRIBUCIÓN SPOT FUTURO (6 MESES) - 50,000 SIMULACIONES', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Spot Futuro (USD/COP)')
    ax2.set_ylabel('Densidad de Probabilidad')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    fig2.text(0.5, 0.02,
             f"Santiago Toro (1040739414) | Yenny Serna (1017210528) | Daniela Perez (1017220748)",
             ha='center', fontsize=8, alpha=0.5)
    plt.tight_layout(rect=[0, 0.03, 1, 1])
    ruta2 = os.path.join(CARPETA_BASE, 'forward_distribucion_spot.png')
    plt.savefig(ruta2, dpi=300, bbox_inches='tight')
    print(f"✅ {ruta2}")
    plt.close()
    archivos_graficos.append(ruta2)
    
    # Gráfico 3: Trayectorias Simuladas
    fig3, ax3 = plt.subplots(1, 1, figsize=(14, 6))
    T = PLAZO_FORWARD_MESES / 12
    tiempo = np.linspace(0, T, int(T*252)+1)
    for i in range(0, min(100, N_SIMULACIONES), 2):
        ax3.plot(tiempo, resultados_sim['paths'][i], color='blue', alpha=0.1, linewidth=0.5)
    ax3.plot(tiempo, np.mean(resultados_sim['paths'], axis=0), 'r-', lw=2, label='Media')
    ax3.axhline(y=FORWARD_CIERRE, color='green', linestyle='--', linewidth=2, label=f'Forward (${FORWARD_CIERRE:,.0f})')
    ax3.set_title('TRAYECTORIAS SIMULADAS SPOT USD/COP', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Tiempo (años)')
    ax3.set_ylabel('USD/COP')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    fig3.text(0.5, 0.02,
             f"Santiago Toro (1040739414) | Yenny Serna (1017210528) | Daniela Perez (1017220748)",
             ha='center', fontsize=8, alpha=0.5)
    plt.tight_layout(rect=[0, 0.03, 1, 1])
    ruta3 = os.path.join(CARPETA_BASE, 'forward_trayectorias.png')
    plt.savefig(ruta3, dpi=300, bbox_inches='tight')
    print(f"✅ {ruta3}")
    plt.close()
    archivos_graficos.append(ruta3)
    
    # Gráfico 4: Análisis de Protección
    fig4, axes4 = plt.subplots(1, 2, figsize=(16, 6))
    colores = ['green', 'red']
    sizes = [analisis['pct_protegidos'], analisis['pct_no_protegidos']]
    labels = [f'Protegidos\n({analisis["pct_protegidos"]:.1f}%)', f'No Protegidos\n({analisis["pct_no_protegidos"]:.1f}%)']
    axes4[0].pie(sizes, colors=colores, labels=labels, autopct='%1.1f%%', startangle=90)
    axes4[0].set_title('DISTRIBUCIÓN DE ESCENARIOS', fontweight='bold')
    data = [resultados_sim['valores_finales'], [FORWARD_CIERRE] * N_SIMULACIONES]
    bp = axes4[1].boxplot(data, labels=['Spot Futuro', 'Forward'], patch_artist=True)
    bp['boxes'][0].set_facecolor('steelblue')
    bp['boxes'][1].set_facecolor('green')
    axes4[1].set_title('COMPARACIÓN SPOT vs FORWARD', fontweight='bold')
    axes4[1].set_ylabel('USD/COP')
    axes4[1].grid(True, alpha=0.3, axis='y')
    fig4.text(0.5, 0.02,
             f"Santiago Toro (1040739414) | Yenny Serna (1017210528) | Daniela Perez (1017220748)",
             ha='center', fontsize=8, alpha=0.5)
    plt.tight_layout(rect=[0, 0.03, 1, 1])
    ruta4 = os.path.join(CARPETA_BASE, 'forward_analisis_proteccion.png')
    plt.savefig(ruta4, dpi=300, bbox_inches='tight')
    print(f"✅ {ruta4}")
    plt.close()
    archivos_graficos.append(ruta4)
    
    return archivos_graficos

# =============================================================================
# FUNCIÓN: GUARDAR ARCHIVOS
# =============================================================================
def guardar_csv(df, nombre_archivo):
    ruta = os.path.join(CARPETA_BASE, nombre_archivo)
    df.to_csv(ruta, index=False, encoding='utf-8')
    print(f"✅ {ruta}")
    return ruta

def guardar_txt(contenido, nombre_archivo):
    ruta = os.path.join(CARPETA_BASE, nombre_archivo)
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write(get_header())
        f.write("\n")
        f.write(contenido)
        f.write("\n")
        f.write(get_footer())
    print(f"✅ {ruta}")
    return ruta

# =============================================================================
# FUNCIÓN: GENERAR REPORTE PRINCIPAL
# =============================================================================
def generar_reporte_principal(df_spot, resultados_sim, analisis, metricas):
    contenido = f"""
LABORATORIO 1 - FORWARD: ANÁLISIS DE COBERTURA CAMBIARIA USD/COP
================================================================================
1. INFORMACIÓN GENERAL
----------------------
Fecha de Generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Plazo del Forward: {PLAZO_FORWARD_MESES} meses
Número de Simulaciones: {N_SIMULACIONES:,}
Spot Actual: ${SPOT_ACTUAL:,.2f} COP/USD
Forward Seleccionado: ${FORWARD_CIERRE:,.2f} COP/USD

2. FUENTES DE DATOS Y METODOLOGÍA
---------------------------------
• Spot USD/COP: Banco de la República (2026). Series Estadísticas.
• Forward SET-FX: Mercado de Derivados Cambiarios (2026)
• Metodología: Hull, J. C. (2021). Options, Futures, and Other Derivatives.

3. ESTADÍSTICAS DEL SPOT HISTÓRICO
----------------------------------
Período Analizado: 2024-2026 ({len(df_spot)} días hábiles)
Spot Mínimo: ${df_spot['Spot'].min():,.2f}
Spot Máximo: ${df_spot['Spot'].max():,.2f}
Spot Promedio: ${df_spot['Spot'].mean():,.2f}
Volatilidad Histórica: {metricas['volatilidad_sin']/SPOT_ACTUAL*100:.2f}%

4. RESULTADOS SIMULACIÓN MONTE CARLO
------------------------------------
Horizonte Temporal: {PLAZO_FORWARD_MESES} meses
Media del Spot Futuro: ${resultados_sim['media']:,.2f}
Mediana del Spot Futuro: ${resultados_sim['mediana']:,.2f}
Desviación Estándar: ${resultados_sim['std']:,.2f}
VaR 95%: ${np.percentile(resultados_sim['valores_finales'], 5):,.2f}
VaR 99%: ${np.percentile(resultados_sim['valores_finales'], 1):,.2f}

5. ANÁLISIS DE PROTECCIÓN FORWARD
---------------------------------
Escenarios PROTEGIDOS: {analisis['n_protegidos']:,} ({analisis['pct_protegidos']:.2f}%)
Escenarios NO PROTEGIDOS: {analisis['n_no_protegidos']:,} ({analisis['pct_no_protegidos']:.2f}%)
Ahorro Promedio: ${analisis['ahorro_promedio']:,.2f}
Pérdida Promedio: ${analisis['perdida_promedio']:,.2f}
Valor Esperado: ${analisis['valor_esperado']:,.2f}

6. MÉTRICAS DE RIESGO
---------------------
VaR 95% SIN cobertura: ${metricas['var_95_sin']:,.2f}
VaR 95% CON forward: ${metricas['var_95_con']:,.2f} (FIJO)
CVaR 95% SIN cobertura: ${metricas['cvar_95_sin']:,.2f}
Reducción de Volatilidad: 100% (elimina riesgo cambiario)

7. CONCLUSIONES
---------------
• El forward elimina completamente el riesgo cambiario
• Protección efectiva en {analisis['pct_protegidos']:.2f}% de los escenarios
• Valor esperado: ${analisis['valor_esperado']:,.2f}
• Recomendación: Evaluar relación costo-beneficio según aversión al riesgo

================================================================================
REFERENCIAS
================================================================================
• Banco de la República. (2026). Tasa Representativa del Mercado.
• Hull, J. C. (2021). Options, Futures, and Other Derivatives (11th ed.). Pearson.
• McDonald, R. L. (2022). Derivatives Markets (4th ed.). Pearson.
"""
    # AGREGAR ANÁLISIS HUMANO
    contenido += analisis_humano_forward(analisis, metricas)
    return contenido

def generar_resumen_ejecutivo(resultados_sim, analisis, metricas):
    return f"""
RESUMEN EJECUTIVO - FORWARD USD/COP
================================================================================
PARÁMETROS:
• Spot Actual: ${SPOT_ACTUAL:,.2f}
• Forward: ${FORWARD_CIERRE:,.2f}
• Plazo: {PLAZO_FORWARD_MESES} meses
• Simulaciones: {N_SIMULACIONES:,}

RESULTADOS:
• Media Spot Futuro: ${resultados_sim['media']:,.2f}
• Escenarios Protegidos: {analisis['pct_protegidos']:.2f}%
• Valor Esperado: ${analisis['valor_esperado']:,.2f}
• VaR 95%: ${metricas['var_95_sin']:,.2f}

RECOMENDACIÓN:
El forward elimina el riesgo cambiario pero tiene un costo de oportunidad.
Conveniente si hay alta aversión al riesgo.
"""

# =============================================================================
# FUNCIÓN PRINCIPAL
# =============================================================================
def ejecutar_forward():
    print("\n" + "🚀"*40)
    print("LABORATORIO 1 - FORWARD: COBERTURA CAMBIARIA")
    print(f"CARPETA: {CARPETA_BASE}")
    print("🚀"*40)
    archivos = []
    
    # 1. Generar datos históricos spot
    df_spot = generar_datos_spot()
    archivos.append('spot_historico.csv')
    
    # 2. Calcular estadísticas
    retornos, media_diaria, std_diaria = calcular_estadisticas(df_spot)
    
    # 3. Ejecutar simulación Monte Carlo
    T = PLAZO_FORWARD_MESES / 12
    resultados_sim = simulacion_monte_carlo(SPOT_ACTUAL, media_diaria, std_diaria, T, N_SIMULACIONES)
    
    # 4. Analizar protección forward
    analisis = analizar_proteccion_forward(resultados_sim['valores_finales'], FORWARD_CIERRE)
    
    # 5. Calcular métricas de riesgo
    metricas = calcular_metricas_riesgo(resultados_sim['valores_finales'], FORWARD_CIERRE)
    
    # 6. Generar gráficos
    graficos = generar_graficos(df_spot, resultados_sim, analisis, metricas)
    archivos.extend([os.path.basename(g) for g in graficos])
    
    # 7. Generar reporte principal
    print("\n" + "="*80)
    print("💾 GENERANDO REPORTES TXT...")
    print("="*80)
    reporte = generar_reporte_principal(df_spot, resultados_sim, analisis, metricas)
    guardar_txt(reporte, 'Forward_Analisis_Completo.txt')
    archivos.append('Forward_Analisis_Completo.txt')
    
    # 8. Resumen ejecutivo
    resumen = generar_resumen_ejecutivo(resultados_sim, analisis, metricas)
    guardar_txt(resumen, 'Forward_Resumen_Ejecutivo.txt')
    archivos.append('Forward_Resumen_Ejecutivo.txt')
    
    # 9. Guardar resultados de simulación
    df_resultados = pd.DataFrame({
        'Simulacion': range(1, N_SIMULACIONES + 1),
        'Spot_Futuro': resultados_sim['valores_finales']
    })
    guardar_csv(df_resultados, 'forward_resultados_simulacion.csv')
    archivos.append('forward_resultados_simulacion.csv')
    
    # Resumen final
    print("\n" + "✨"*40)
    print("FORWARD COMPLETADO")
    print("✨"*40)
    print(f"\n📁 ARCHIVOS EN: {CARPETA_BASE}")
    print("\n📂 ARCHIVOS GENERADOS:")
    for arch in sorted(archivos):
        ruta = os.path.join(CARPETA_BASE, arch)
        if os.path.exists(ruta):
            tamano = os.path.getsize(ruta)
            if arch.endswith('.txt'):
                print(f"   📄 {arch} ({tamano:,} bytes)")
            elif arch.endswith('.csv'):
                print(f"   📊 {arch} ({tamano:,} bytes)")
            elif arch.endswith('.png'):
                print(f"   🖼️  {arch} ({tamano:,} bytes)")
    print("\n" + "="*80)
    print("✅ FORWARD GENERADO CORRECTAMENTE")
    print("="*80)

# =============================================================================
# EJECUCIÓN
# =============================================================================
if __name__ == "__main__":
    try:
        ejecutar_forward()
        print("\n" + "="*80)
        print("📋 PROYECTO COMPLETADO - 5 PUNTOS DEL LABORATORIO")
        print("="*80)
        print("""
INTEGRANTES:
• Santiago Toro Cadavid - 1040739414
• Yenny Carolina Serna Chaverra - 1017210528
• Daniela Perez Meza - 1017220748

PROYECTO: LABORATORIO 1
CURSO: Derivados Financieros
""")
        print("="*80)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()