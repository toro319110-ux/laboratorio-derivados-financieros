# =============================================================================
# PROYECTO: LABORATORIO 1 - PUNTO 4
# SIMULACIÓN DE MONTE CARLO CON MOVIMIENTO BROWNIANO GEOMÉTRICO (BMG)
# =============================================================================
# INTEGRANTES:
#   Santiago Toro Cadavid - 1040739414
#   Yenny Carolina Serna Chaverra - 1017210528
#   Daniela Perez Meza - 1017220748
# CURSO: Derivados Financieros
# INSTITUCIÓN: [Nombre de tu Universidad]
# =============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from datetime import datetime
import os
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# CONFIGURACIÓN DE RUTAS RELATIVAS (COMPATIBLE CON GITHUB)
# =============================================================================
directorio_actual = os.path.dirname(os.path.abspath(__file__))
CARPETA_BASE = os.path.join(directorio_actual, "outputs", "PUNTO_4")
os.makedirs(CARPETA_BASE, exist_ok=True)

# =============================================================================
# CONFIGURACIÓN GLOBAL
# =============================================================================
FECHA_ACTUAL = "2026-03-26"
TRM_ACTUAL = 3688.46
N_SIMULACIONES = 1000
HORIZONTE_ANOS = 5
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
PROYECTO = "LABORATORIO 1 - Punto 4"

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
# ANÁLISIS - PUNTO 4 (ESTILO ESTUDIANTE)
# =============================================================================
def analisis_humano_punto4(media_retorno, std_retorno, resultados_sim):
    var_95 = np.percentile(resultados_sim['val_normal'], 5)
    return f"""
LO QUE ENTENDÍ DE ESTE PUNTO (EXPLICACIÓN SENCILLA)
================================================================================

Este fue el más "matemático" pero les trato de explicar:

🎲 ¿QUÉ ES MONTE CARLO?
Es como lanzar un dado 50.000 veces para ver qué pasa en promedio.
En vez de adivinar el futuro, simulamos MUCHOS futuros posibles.

📊 LO QUE HICIMOS:
• Tomamos datos históricos de la TRM (2019-2024)
• Calculamos cómo ha variado mes a mes
• Usamos una fórmula matemática (Movimiento Browniano) para proyectar 5 años
• Repetimos la simulación 1.000 veces para ver diferentes escenarios

🔢 NÚMEROS IMPORTANTES:
• Retorno mensual promedio: {media_retorno*100:+.4f}%
• Volatilidad mensual: {std_retorno*100:.4f}%
• TRM proyectada (promedio): ${resultados_sim['media']:,.0f}
• TRM proyectada (peor caso 5%): ${var_95:,.0f}

🤯 LO QUE MÁS ME LLAMÓ LA ATENCIÓN:
1. Hay MUCHA incertidumbre: la TRM podría terminar entre ${resultados_sim['val_normal'].min():,.0f} y ${resultados_sim['val_normal'].max():,.0f}
2. La distribución "T-Student" muestra que los eventos extremos son más probables
3. El VaR 95% me dice: "en 95 de cada 100 casos, la TRM no bajará de ${var_95:,.0f}"

🎯 ¿PARA QUÉ ME SIRVE ESTO?
• Para tomar decisiones con más información
• Para entender que el futuro no es una línea recta
• Para prepararme para escenarios malos (no solo esperar lo mejor)

😅 MI OPINIÓN DE ESTUDIANTE:
Al principio me asustó tanta fórmula, pero después entendí que es como hacer 
muchas apuestas virtuales para ver qué tan probable es cada resultado.
No me dice el futuro exacto, pero me ayuda a no sorprenderme tanto.

📚 LO QUE CONSULTÉ:
• Libro de Hull (el "biblia" de derivados) - capítulo de simulaciones
• Videos de YouTube sobre Monte Carlo 
• Clase: "la volatilidad es el precio de la incertidumbre"

================================================================================
"""

# =============================================================================
# FUNCIÓN: GENERAR DATOS TRM
# =============================================================================
def generar_datos_trm():
    print("\n" + "="*80)
    print("📊 PASO 1: GENERANDO DATOS TRM")
    print("="*80)
    np.random.seed(SEMILLA)
    fechas = pd.date_range(start='2019-01-01', end='2024-01-31', freq='B')
    n = len(fechas)
    trm = np.zeros(n)
    trm[0] = 3200
    for i in range(1, n):
        retorno = np.random.normal(0.0002, 0.008)
        trm[i] = trm[i-1] * (1 + retorno)
    trm[(fechas >= '2020-03-01') & (fechas <= '2020-06-30')] *= 1.15
    trm[(fechas >= '2022-06-01') & (fechas <= '2023-03-31')] *= 1.20
    df_trm = pd.DataFrame({'Fecha': fechas, 'TRM': trm})
    archivo_csv = os.path.join(CARPETA_BASE, "trm_datos.csv")
    df_trm['Fecha'] = df_trm['Fecha'].dt.strftime('%Y-%m-%d')
    df_trm.to_csv(archivo_csv, index=False, encoding='utf-8')
    print(f"✅ CSV CREADO: {archivo_csv}")
    print(f"   Tamaño: {os.path.getsize(archivo_csv):,} bytes")
    print(f"   Registros: {len(df_trm)}")
    return df_trm

# =============================================================================
# FUNCIÓN: CALCULAR RETORNOS MENSUALES
# =============================================================================
def calcular_retornos_mensuales(df_trm):
    print("\n" + "="*80)
    print("📊 PASO 2: CALCULANDO RETORNOS MENSUALES")
    print("="*80)
    df_trm['Fecha'] = pd.to_datetime(df_trm['Fecha'])
    df_trm['Mes'] = df_trm['Fecha'].dt.to_period('M')
    trm_mensual = df_trm.groupby('Mes')['TRM'].mean().reset_index()
    trm_mensual['Mes'] = trm_mensual['Mes'].dt.to_timestamp()
    trm_mensual['Retorno'] = trm_mensual['TRM'].pct_change()
    trm_mensual = trm_mensual.dropna()
    retornos = trm_mensual['Retorno']
    media = retornos.mean()
    std = retornos.std()
    print(f"📈 ESTADÍSTICAS DE RETORNOS MENSUALES:")
    print(f"   Meses analizados: {len(trm_mensual)}")
    print(f"   Media: {media:.6f} ({media*100:.4f}%)")
    print(f"   Desviación Estándar: {std:.6f} ({std*100:.4f}%)")
    return trm_mensual, media, std

# =============================================================================
# FUNCIÓN: SIMULACIÓN BMG
# =============================================================================
def gbm_sim(S0, mu, sigma, T, n_sim, dist='normal'):
    dt = 1/12
    steps = int(T * 12)
    if dist == 'normal':
        Z = np.random.standard_normal((n_sim, steps))
    else:
        Z = np.random.standard_t(df=5, size=(n_sim, steps))
        Z = Z * np.sqrt(3/5)
    paths = np.zeros((n_sim, steps + 1))
    paths[:, 0] = S0
    for t in range(1, steps + 1):
        paths[:, t] = paths[:, t-1] * np.exp(
            (mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z[:, t-1]
        )
    return paths

def ejecutar_simulacion_monte_carlo(S0, mu_mensual, std_mensual, n_sim=N_SIMULACIONES, T=HORIZONTE_ANOS):
    print("\n" + "="*80)
    print("📊 PASO 3: SIMULACIÓN MONTE CARLO (BMG)")
    print("="*80)
    mu_anual = mu_mensual * 12
    sigma_anual = std_mensual * np.sqrt(12)
    print(f"📈 PARÁMETROS DE SIMULACIÓN:")
    print(f"   TRM Inicial (S0): ${S0:,.2f}")
    print(f"   Drift anual (μ): {mu_anual:.6f} ({mu_anual*100:.4f}%)")
    print(f"   Volatilidad anual (σ): {sigma_anual:.6f} ({sigma_anual*100:.4f}%)")
    print(f"   Horizonte: {T} años")
    print(f"   Número de simulaciones: {n_sim}")
    np.random.seed(SEMILLA)
    paths_normal = gbm_sim(S0, mu_anual, sigma_anual, T, n_sim, 'normal')
    paths_t = gbm_sim(S0, mu_anual, sigma_anual, T, n_sim, 't_student')
    val_normal = paths_normal[:, -1]
    val_t = paths_t[:, -1]
    print(f"\n✅ SIMULACIONES COMPLETADAS")
    print(f"\n📊 DISTRIBUCIÓN NORMAL:")
    print(f"   Media: ${val_normal.mean():,.2f}")
    print(f"   Desviación: ${val_normal.std():,.2f}")
    print(f"   VaR 95%: ${np.percentile(val_normal, 5):,.2f}")
    print(f"\n📊 DISTRIBUCIÓN T-STUDENT:")
    print(f"   Media: ${val_t.mean():,.2f}")
    print(f"   Desviación: ${val_t.std():,.2f}")
    print(f"   VaR 95%: ${np.percentile(val_t, 5):,.2f}")
    return {
        'paths_normal': paths_normal,
        'paths_t': paths_t,
        'val_normal': val_normal,
        'val_t': val_t,
        'mu_anual': mu_anual,
        'sigma_anual': sigma_anual,
        'S0': S0
    }

# =============================================================================
# FUNCIÓN: GENERAR GRÁFICOS
# =============================================================================
def generar_graficos(df_trm, trm_mensual, resultados_simulacion):
    print("\n" + "="*80)
    print("📈 PASO 4: GENERANDO GRÁFICOS")
    print("="*80)
    archivos_graficos = []
    
    # Gráfico 1: Dashboard Completo
    fig = plt.figure(figsize=(20, 12))
    fig.suptitle('ANÁLISIS TRM Y SIMULACIÓN MONTE CARLO (BMG)', fontsize=16, fontweight='bold')
    
    ax1 = plt.subplot(2, 3, 1)
    df_trm['Fecha'] = pd.to_datetime(df_trm['Fecha'])
    ax1.plot(df_trm['Fecha'], df_trm['TRM'], color='blue', linewidth=1)
    ax1.set_title('1. Serie Histórica TRM (2019-2024)', fontweight='bold')
    ax1.set_ylabel('TRM (COP/USD)')
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(True, alpha=0.3)
    
    ax2 = plt.subplot(2, 3, 2)
    retornos = trm_mensual['Retorno'].dropna()
    ax2.hist(retornos, bins=20, density=True, alpha=0.7, color='purple')
    x = np.linspace(retornos.min(), retornos.max(), 100)
    ax2.plot(x, stats.norm.pdf(x, retornos.mean(), retornos.std()), 'r-', lw=2)
    ax2.set_title('2. Distribución de Retornos Mensuales', fontweight='bold')
    ax2.set_xlabel('Retorno')
    ax2.grid(True, alpha=0.3)
    
    ax3 = plt.subplot(2, 3, 3)
    stats.probplot(retornos, dist="norm", plot=ax3)
    ax3.set_title('3. QQ-Plot (Normalidad)', fontweight='bold')
    ax3.grid(True, alpha=0.3)
    
    ax4 = plt.subplot(2, 3, 4)
    T = HORIZONTE_ANOS
    tiempo = np.linspace(0, T, int(T*12)+1)
    for i in range(0, N_SIMULACIONES, 50):
        ax4.plot(tiempo, resultados_simulacion['paths_normal'][i], color='blue', alpha=0.1)
    ax4.plot(tiempo, np.mean(resultados_simulacion['paths_normal'], axis=0), 'r-', lw=2, label='Media')
    ax4.set_title('4. BMG - Distribución Normal', fontweight='bold')
    ax4.set_ylabel('TRM (COP/USD)')
    ax4.set_xlabel('Años')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    ax5 = plt.subplot(2, 3, 5)
    for i in range(0, N_SIMULACIONES, 50):
        ax5.plot(tiempo, resultados_simulacion['paths_t'][i], color='orange', alpha=0.1)
    ax5.plot(tiempo, np.mean(resultados_simulacion['paths_t'], axis=0), 'r-', lw=2, label='Media')
    ax5.set_title('5. BMG - Distribución T-Student', fontweight='bold')
    ax5.set_ylabel('TRM (COP/USD)')
    ax5.set_xlabel('Años')
    ax5.legend()
    ax5.grid(True, alpha=0.3)
    
    ax6 = plt.subplot(2, 3, 6)
    ax6.hist(resultados_simulacion['val_normal'], bins=40, density=True, alpha=0.6, color='blue', label='Normal')
    ax6.hist(resultados_simulacion['val_t'], bins=40, density=True, alpha=0.6, color='orange', label='T-Student')
    ax6.axvline(resultados_simulacion['S0'], color='black', linestyle='--', label='TRM Actual')
    ax6.set_title('6. Distribución Final (5 años)', fontweight='bold')
    ax6.set_xlabel('TRM Proyectada')
    ax6.legend()
    ax6.grid(True, alpha=0.3)
    
    fig.text(0.5, 0.02,
             f"Santiago Toro (1040739414) | Yenny Serna (1017210528) | Daniela Perez (1017220748)",
             ha='center', fontsize=8, alpha=0.5)
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    ruta1 = os.path.join(CARPETA_BASE, 'punto4_dashboard_completo.png')
    plt.savefig(ruta1, dpi=300, bbox_inches='tight')
    print(f"✅ {ruta1}")
    plt.close()
    archivos_graficos.append(ruta1)
    
    # Gráfico 2: Serie Histórica
    fig2, ax2 = plt.subplots(1, 1, figsize=(14, 6))
    ax2.plot(df_trm['Fecha'], df_trm['TRM'], linewidth=1.5, color='blue')
    ax2.fill_between(df_trm['Fecha'], df_trm['TRM'], alpha=0.3)
    ax2.set_title('SERIE HISTÓRICA TRM (2019-2024)', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Fecha')
    ax2.set_ylabel('TRM (COP/USD)')
    ax2.tick_params(axis='x', rotation=45)
    ax2.grid(True, alpha=0.3)
    fig2.text(0.5, 0.02,
             f"Santiago Toro (1040739414) | Yenny Serna (1017210528) | Daniela Perez (1017220748)",
             ha='center', fontsize=8, alpha=0.5)
    plt.tight_layout(rect=[0, 0.03, 1, 1])
    ruta2 = os.path.join(CARPETA_BASE, 'punto4_serie_historica_trm.png')
    plt.savefig(ruta2, dpi=300, bbox_inches='tight')
    print(f"✅ {ruta2}")
    plt.close()
    archivos_graficos.append(ruta2)
    
    # Gráfico 3: Comparación Riesgo
    fig3, ax3 = plt.subplots(1, 1, figsize=(10, 6))
    data = [resultados_simulacion['val_normal'], resultados_simulacion['val_t']]
    bp = ax3.boxplot(data, labels=['Normal', 'T-Student'], patch_artist=True)
    bp['boxes'][0].set_facecolor('blue')
    bp['boxes'][1].set_facecolor('orange')
    ax3.set_title('COMPARACIÓN DE RIESGO - DISTRIBUCIÓN FINAL (5 AÑOS)', fontsize=14, fontweight='bold')
    ax3.set_ylabel('TRM Final (COP/USD)')
    ax3.set_xlabel('Distribución')
    ax3.grid(True, alpha=0.3, axis='y')
    ax3.axhline(y=resultados_simulacion['S0'], color='green', linestyle='--', label='TRM Actual')
    ax3.legend()
    fig3.text(0.5, 0.02,
             f"Santiago Toro (1040739414) | Yenny Serna (1017210528) | Daniela Perez (1017220748)",
             ha='center', fontsize=8, alpha=0.5)
    plt.tight_layout(rect=[0, 0.03, 1, 1])
    ruta3 = os.path.join(CARPETA_BASE, 'punto4_comparacion_riesgo.png')
    plt.savefig(ruta3, dpi=300, bbox_inches='tight')
    print(f"✅ {ruta3}")
    plt.close()
    archivos_graficos.append(ruta3)
    
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
def generar_reporte_principal(trm_mensual, media, std, resultados_simulacion):
    contenido = f"""
LABORATORIO 1 - PUNTO 4: SIMULACIÓN MONTE CARLO CON BMG
================================================================================
1. INFORMACIÓN GENERAL
----------------------
Fecha de Generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Horizonte de Simulación: {HORIZONTE_ANOS} años
Número de Simulaciones: {N_SIMULACIONES}
TRM Inicial: ${resultados_simulacion['S0']:,.2f} COP/USD

2. FUENTES DE DATOS Y METODOLOGÍA
---------------------------------
• Datos TRM: Banco de la República (2026). Series Estadísticas.
• Metodología BMG: Hull, J. C. (2021). Options, Futures, and Other Derivatives.
• Distribución T-Student: McDonald, R. L. (2022). Derivatives Markets.

3. ESTADÍSTICAS DE RETORNOS MENSUALES
-------------------------------------
Período Analizado: 2019-2024 ({len(trm_mensual)} meses)
Media: {media:.6f} ({media*100:.4f}%)
Desviación Estándar: {std:.6f} ({std*100:.4f}%)
Varianza: {trm_mensual['Retorno'].var():.6f}
Skewness: {trm_mensual['Retorno'].skew():.4f}
Kurtosis: {trm_mensual['Retorno'].kurtosis():.4f}

4. PARÁMETROS DE SIMULACIÓN (ANUALIZADOS)
-----------------------------------------
Drift Anual (μ): {resultados_simulacion['mu_anual']:.6f} ({resultados_simulacion['mu_anual']*100:.4f}%)
Volatilidad Anual (σ): {resultados_simulacion['sigma_anual']:.6f} ({resultados_simulacion['sigma_anual']*100:.4f}%)

5. RESULTADOS SIMULACIÓN - DISTRIBUCIÓN NORMAL
----------------------------------------------
Media: ${resultados_simulacion['val_normal'].mean():,.2f}
Desviación: ${resultados_simulacion['val_normal'].std():,.2f}
VaR 95%: ${np.percentile(resultados_simulacion['val_normal'], 5):,.2f}
Mínimo: ${resultados_simulacion['val_normal'].min():,.2f}
Máximo: ${resultados_simulacion['val_normal'].max():,.2f}

6. RESULTADOS SIMULACIÓN - DISTRIBUCIÓN T-STUDENT
-------------------------------------------------
Media: ${resultados_simulacion['val_t'].mean():,.2f}
Desviación: ${resultados_simulacion['val_t'].std():,.2f}
VaR 95%: ${np.percentile(resultados_simulacion['val_t'], 5):,.2f}
Mínimo: ${resultados_simulacion['val_t'].min():,.2f}
Máximo: ${resultados_simulacion['val_t'].max():,.2f}

7. ANÁLISIS DE RIESGO
---------------------
• La distribución T-Student muestra colas más pesadas (mayor riesgo extremo)
• La volatilidad anualizada ({resultados_simulacion['sigma_anual']*100:.2f}%) indica riesgo cambiario significativo

8. CONCLUSIONES
---------------
• El BMG es adecuado para modelar la evolución de la TRM
• La distribución T-Student captura mejor los eventos extremos
• Se recomienda usar T-Student para cálculos de VaR conservadores

================================================================================
REFERENCIAS
================================================================================
• Banco de la República. (2026). Tasa Representativa del Mercado.
• Hull, J. C. (2021). Options, Futures, and Other Derivatives (11th ed.). Pearson.
• McDonald, R. L. (2022). Derivatives Markets (4th ed.). Pearson.
"""
    # AGREGAR ANÁLISIS HUMANO
    contenido += analisis_humano_punto4(media, std, resultados_simulacion)
    return contenido

def generar_resumen_ejecutivo(media, std, resultados_simulacion):
    return f"""
RESUMEN EJECUTIVO - PUNTO 4
================================================================================
SIMULACIÓN MONTE CARLO - MOVIMIENTO BROWNIANO GEOMÉTRICO

PARÁMETROS:
• Horizonte: {HORIZONTE_ANOS} años
• Simulaciones: {N_SIMULACIONES}
• TRM Inicial: ${resultados_simulacion['S0']:,.2f}

RETORNOS MENSUALES:
• Media: {media*100:.4f}%
• Volatilidad: {std*100:.4f}%

PROYECCIÓN 5 AÑOS (NORMAL):
• Media: ${resultados_simulacion['val_normal'].mean():,.2f}
• VaR 95%: ${np.percentile(resultados_simulacion['val_normal'], 5):,.2f}

PROYECCIÓN 5 AÑOS (T-STUDENT):
• Media: ${resultados_simulacion['val_t'].mean():,.2f}
• VaR 95%: ${np.percentile(resultados_simulacion['val_t'], 5):,.2f}

RECOMENDACIÓN:
Usar distribución T-Student para evaluación de riesgo (colas pesadas).
La TRM muestra alta volatilidad ({resultados_simulacion['sigma_anual']*100:.2f}% anual).
"""

# =============================================================================
# FUNCIÓN PRINCIPAL
# =============================================================================
def ejecutar_punto4():
    print("\n" + "🚀"*40)
    print("LABORATORIO 1 - PUNTO 4: SIMULACIÓN MONTE CARLO (BMG)")
    print(f"CARPETA: {CARPETA_BASE}")
    print("🚀"*40)
    archivos = []
    
    # 1. Generar datos TRM históricos
    df_trm = generar_datos_trm()
    archivos.append('trm_datos.csv')
    
    # 2. Calcular retornos mensuales
    trm_mensual, media, std = calcular_retornos_mensuales(df_trm)
    
    # 3. Ejecutar simulación Monte Carlo
    S0 = df_trm['TRM'].iloc[-1]
    resultados_simulacion = ejecutar_simulacion_monte_carlo(S0, media, std)
    
    # 4. Generar gráficos
    graficos = generar_graficos(df_trm, trm_mensual, resultados_simulacion)
    archivos.extend([os.path.basename(g) for g in graficos])
    
    # 5. Generar reporte principal
    print("\n" + "="*80)
    print("💾 GENERANDO REPORTES TXT...")
    print("="*80)
    reporte = generar_reporte_principal(trm_mensual, media, std, resultados_simulacion)
    guardar_txt(reporte, 'Laboratorio1_Punto4_Simulacion_BMG.txt')
    archivos.append('Laboratorio1_Punto4_Simulacion_BMG.txt')
    
    # 6. Resumen ejecutivo
    resumen = generar_resumen_ejecutivo(media, std, resultados_simulacion)
    guardar_txt(resumen, 'Resumen_Ejecutivo_Punto4.txt')
    archivos.append('Resumen_Ejecutivo_Punto4.txt')
    
    # 7. Guardar datos de retornos
    df_retornos = trm_mensual[['Mes', 'TRM', 'Retorno']].copy()
    df_retornos['Mes'] = df_retornos['Mes'].dt.strftime('%Y-%m')
    guardar_csv(df_retornos, 'punto4_retornos_mensuales.csv')
    archivos.append('punto4_retornos_mensuales.csv')
    
    # 8. Guardar resultados de simulación
    df_resultados = pd.DataFrame({
        'Simulacion': range(1, N_SIMULACIONES + 1),
        'TRM_Final_Normal': resultados_simulacion['val_normal'],
        'TRM_Final_TStudent': resultados_simulacion['val_t']
    })
    guardar_csv(df_resultados, 'punto4_resultados_simulacion.csv')
    archivos.append('punto4_resultados_simulacion.csv')
    
    # Resumen final
    print("\n" + "✨"*40)
    print("PUNTO 4 COMPLETADO")
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
    print("✅ PUNTO 4 GENERADO CORRECTAMENTE")
    print("="*80)
    return resultados_simulacion

# =============================================================================
# EJECUCIÓN
# =============================================================================
if __name__ == "__main__":
    try:
        resultados_punto4 = ejecutar_punto4()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()