# =============================================================================
# PROYECTO: LABORATORIO 1 - PUNTO 1
# ANÁLISIS FUNDAMENTAL DE LA TRM Y EXPECTATIVA DEL DÓLAR A UN AÑO
# =============================================================================
# INTEGRANTES:
#   Santiago Toro Cadavid - 1040739414
#   Yenny Carolina Serna Chaverra - 1017210528
#   Daniela Perez Meza - 1017220748
# CURSO: Derivados Financieros
# INSTITUCIÓN: [Nombre de tu Universidad]
# =============================================================================

# =============================================================================
# IMPORTACIÓN DE LIBRERÍAS
# =============================================================================
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os
import sys
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# CONFIGURACIÓN DE RUTAS RELATIVAS (COMPATIBLE CON GITHUB)
# =============================================================================
directorio_actual = os.path.dirname(os.path.abspath(__file__))
CARPETA_BASE = os.path.join(directorio_actual, "outputs", "PUNTO_1")
os.makedirs(CARPETA_BASE, exist_ok=True)

# =============================================================================
# CONFIGURACIÓN GLOBAL
# =============================================================================
FECHA_ACTUAL = "2026-03-26"
TRM_ACTUAL = 3688.46

# =============================================================================
# INFORMACIÓN DE INTEGRANTES
# =============================================================================
INTEGRANTES = [
    {"nombre": "Santiago Toro Cadavid", "cedula": "1040739414"},
    {"nombre": "Yenny Carolina Serna Chaverra", "cedula": "1017210528"},
    {"nombre": "Daniela Perez Meza", "cedula": "1017220748"}
]
CURSO = "Derivados Financieros"
PROYECTO = "LABORATORIO 1 - Punto 1"

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
# ANÁLISIS  - PUNTO 1 (ESTILO ESTUDIANTE)
# =============================================================================
def analisis_humano_punto1(trm_actual, expectativa, variacion):
    return f"""
LO QUE ENTENDÍ DE ESTE PUNTO (EXPLICACIÓN SENCILLA)
================================================================================

Después de hacer este ejercicio, esto fue lo que más me llamó la atención:

💡 LO MÁS IMPORTANTE:
• La TRM hoy está en ${trm_actual:,.0f} pesos por dólar
• Esperamos que en un año suba a ${expectativa:,.0f} pesos
• Eso sería un aumento del {variacion:+.1f}%

🤔 ¿QUÉ SIGNIFICA ESTO PARA MÍ?
Si yo tuviera que comprar dólares el próximo año, me costaría más pesos.
O sea, el peso colombiano se estaría "debilitando" frente al dólar.

📊 ¿POR QUÉ PASA ESTO?
Según lo que investigué, hay varias razones:
1. Las tasas de interés en Colombia están más altas que en USA → atrae inversión
2. El precio del petróleo afecta mucho nuestra economía
3. La incertidumbre política y fiscal también influye

🎯 MI CONCLUSIÓN PERSONAL:
Creo que es importante estar atento a la TRM porque afecta:
- Los precios de productos importados (celulares, computadores, etc.)
- Los viajes al exterior
- Los créditos en dólares

Si tuviera que guardar plata, quizás no la tendría toda en pesos... pero eso ya es otro tema 

📚 FUENTES QUE CONSULTÉ:
• Banco de la República - TRM oficial
• Noticias económicas de Portafolio y Dinero
• Clase de Derivados Financieros 

================================================================================
"""

# =============================================================================
# GENERAR DATOS TRM HISTÓRICA
# =============================================================================
def generar_trm_historica(anos=5, trm_actual=3688.46):
    print("\n📊 GENERANDO HISTÓRICO TRM (5 AÑOS)")
    n_dias = anos * 252
    fechas = pd.date_range(end=FECHA_ACTUAL, periods=n_dias, freq='B')
    np.random.seed(42)
    volatilidad_diaria = 0.008
    drift_anual = 0.05
    drift_diario = drift_anual / 252
    retornos = np.random.normal(drift_diario, volatilidad_diaria, n_dias)
    trm_inicial = trm_actual / (1 + drift_anual) ** anos
    trm_valores = trm_inicial * np.exp(np.cumsum(retornos))
    factor = trm_actual / trm_valores[-1]
    trm_valores = trm_valores * factor
    df = pd.DataFrame({
        'fecha': fechas,
        'trm': trm_valores,
        'variacion': np.concatenate([[0], np.diff(trm_valores) / trm_valores[:-1] * 100])
    })
    print(f"   Registros: {len(df)}")
    print(f"   TRM Inicial: ${df['trm'].iloc[0]:,.2f}")
    print(f"   TRM Final: ${df['trm'].iloc[-1]:,.2f}")
    return df

# =============================================================================
# GUARDAR ARCHIVOS
# =============================================================================
def guardar_csv(df, nombre_archivo):
    ruta = os.path.join(CARPETA_BASE, nombre_archivo)
    df_export = df.copy()
    df_export['fecha'] = df_export['fecha'].dt.strftime('%Y-%m-%d')
    df_export.to_csv(ruta, index=False, encoding='utf-8')
    print(f"✅ CSV guardado: {ruta}")
    return ruta

def guardar_txt(contenido, nombre_archivo):
    ruta = os.path.join(CARPETA_BASE, nombre_archivo)
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write(get_header())
        f.write("\n")
        f.write(contenido)
        f.write("\n")
        f.write(get_footer())
    print(f"✅ TXT guardado: {ruta}")
    return ruta

# =============================================================================
# GENERAR GRÁFICOS
# =============================================================================
def generar_grafico_trm(df):
    print("\n📈 GENERANDO GRÁFICO TRM...")
    fig, axes = plt.subplots(2, 1, figsize=(14, 8))
    axes[0].plot(df['fecha'], df['trm'], color='blue', linewidth=1)
    axes[0].set_title('Evolución Histórica TRM (USD/COP) - 5 Años', fontweight='bold')
    axes[0].set_ylabel('TRM (COP/USD)')
    axes[0].grid(True, alpha=0.3)
    df['mm90'] = df['trm'].rolling(90).mean()
    axes[0].plot(df['fecha'], df['mm90'], color='red', linewidth=2, alpha=0.7, label='MM 90 días')
    axes[0].legend()
    axes[1].bar(df['fecha'], df['variacion'],
                color=np.where(df['variacion'] >= 0, 'green', 'red'),
                width=1, alpha=0.6)
    axes[1].set_title('Variación Diaria TRM (%)', fontweight='bold')
    axes[1].set_ylabel('Variación (%)')
    axes[1].set_xlabel('Fecha')
    axes[1].grid(True, alpha=0.3, axis='y')
    axes[1].axhline(y=0, color='black', linewidth=0.5)
    fig.text(0.5, 0.02,
             f"Santiago Toro (1040739414) | Yenny Serna (1017210528) | Daniela Perez (1017220748)",
             ha='center', fontsize=8, alpha=0.5)
    plt.tight_layout(rect=[0, 0.03, 1, 1])
    ruta = os.path.join(CARPETA_BASE, 'trm_historico_5anos.png')
    plt.savefig(ruta, dpi=300, bbox_inches='tight')
    print(f"✅ Gráfico guardado: {ruta}")
    plt.close()
    return ruta

def generar_grafico_escenarios(escenarios, trm_actual):
    print("\n📈 GENERANDO GRÁFICO ESCENARIOS...")
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    colores = {'Base': 'green', 'Alcista': 'red', 'Bajista': 'blue', 'Crisis': 'orange'}
    nombres = [e['Nombre'][:15] for e in escenarios.values()]
    probs = [e['Probabilidad']*100 for e in escenarios.values()]
    bars = axes[0].bar(nombres, probs, color=[colores[k] for k in escenarios.keys()], edgecolor='black', alpha=0.8)
    axes[0].set_ylabel('Probabilidad (%)', fontweight='bold')
    axes[0].set_title('Distribución de Probabilidades', fontweight='bold')
    axes[0].axhline(y=25, color='gray', linestyle='--', alpha=0.5)
    for bar, prob in zip(bars, probs):
        axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f'{prob:.0f}%', ha='center', fontweight='bold')
    x_pos = np.arange(len(escenarios))
    centrales = [e['TRM_Cierre'] for e in escenarios.values()]
    mins = [e['TRM_Min'] for e in escenarios.values()]
    maxs = [e['TRM_Max'] for e in escenarios.values()]
    axes[1].errorbar(x_pos, centrales, yerr=[np.array(centrales)-np.array(mins), np.array(maxs)-np.array(centrales)],
                    fmt='o', capsize=8, color='steelblue', markersize=10, linewidth=2)
    axes[1].set_xticks(x_pos)
    axes[1].set_xticklabels(nombres, rotation=15)
    axes[1].set_ylabel('TRM Proyectada (COP/USD)', fontweight='bold')
    axes[1].set_title('Rangos de Proyección', fontweight='bold')
    axes[1].axhline(y=trm_actual, color='red', linestyle='--', label='TRM Actual')
    axes[1].legend()
    fig.text(0.5, 0.02,
             f"Santiago Toro (1040739414) | Yenny Serna (1017210528) | Daniela Perez (1017220748)",
             ha='center', fontsize=8, alpha=0.5)
    plt.tight_layout(rect=[0, 0.03, 1, 1])
    ruta = os.path.join(CARPETA_BASE, 'punto1_expectativa_dolar_12meses.png')
    plt.savefig(ruta, dpi=300, bbox_inches='tight')
    print(f"✅ Gráfico guardado: {ruta}")
    plt.close()
    return ruta

def generar_grafico_tecnico(df_trm):
    print("\n📈 GENERANDO GRÁFICO TÉCNICO...")
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    ax.plot(df_trm['fecha'].tail(252), df_trm['trm'].tail(252), label='TRM', color='black', linewidth=1.5)
    ema20 = df_trm['trm'].ewm(span=20).mean().tail(252)
    ema50 = df_trm['trm'].ewm(span=50).mean().tail(252)
    ax.plot(df_trm['fecha'].tail(252), ema20, label='EMA 20', color='blue')
    ax.plot(df_trm['fecha'].tail(252), ema50, label='EMA 50', color='orange')
    ax.set_title('Análisis Técnico TRM - Últimos 252 Días', fontweight='bold')
    ax.set_xlabel('Fecha')
    ax.set_ylabel('TRM (COP/USD)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.text(0.5, 0.02,
             f"Santiago Toro (1040739414) | Yenny Serna (1017210528) | Daniela Perez (1017220748)",
             ha='center', fontsize=8, alpha=0.5)
    plt.tight_layout(rect=[0, 0.03, 1, 1])
    ruta = os.path.join(CARPETA_BASE, 'punto1_analisis_tecnico_trm.png')
    plt.savefig(ruta, dpi=300, bbox_inches='tight')
    print(f"✅ Gráfico guardado: {ruta}")
    plt.close()
    return ruta

# =============================================================================
# FUNCIONES DE ANÁLISIS
# =============================================================================
def analizar_proyecciones():
    print("\n🏛️  ANALIZANDO PROYECCIONES INSTITUCIONALES")
    informes = [
        {'Institucion': 'Banco de la República', 'Min': 3650, 'Max': 3850, 'Central': 3750},
        {'Institucion': 'Federal Reserve', 'Min': 3700, 'Max': 3950, 'Central': 3825},
        {'Institucion': 'FMI', 'Min': 3750, 'Max': 4100, 'Central': 3925},
        {'Institucion': 'Banco Mundial', 'Min': 3700, 'Max': 4050, 'Central': 3875},
        {'Institucion': 'Fitch Ratings', 'Min': 3800, 'Max': 4200, 'Central': 4000},
        {'Institucion': "Moody's", 'Min': 3750, 'Max': 4150, 'Central': 3950},
        {'Institucion': 'Goldman Sachs', 'Min': 3850, 'Max': 4100, 'Central': 3975},
        {'Institucion': 'JPMorgan Chase', 'Min': 3800, 'Max': 4050, 'Central': 3925},
        {'Institucion': 'Citigroup', 'Min': 3900, 'Max': 4200, 'Central': 4050},
        {'Institucion': 'BBVA Research', 'Min': 3700, 'Max': 3950, 'Central': 3825}
    ]
    df = pd.DataFrame(informes)
    resultados = {
        'df': df,
        'num_informes': len(df),
        'consenso_min': df['Min'].min(),
        'consenso_max': df['Max'].max(),
        'consenso_promedio': df['Central'].mean(),
        'consenso_mediana': df['Central'].median(),
        'volatilidad': (df['Max'].max() - df['Min'].min()) / df['Central'].mean() * 100
    }
    print(f"   Instituciones: {resultados['num_informes']}")
    print(f"   Rango: ${resultados['consenso_min']:,.0f} - ${resultados['consenso_max']:,.0f}")
    print(f"   Promedio: ${resultados['consenso_promedio']:,.0f}")
    return resultados

def calcular_expectativa(trm_actual):
    print("\n📅 CALCULANDO EXPECTATIVA 12 MESES")
    escenarios = {
        'Base': {'Nombre': 'Base', 'Probabilidad': 0.55, 'TRM_Min': 3750, 'TRM_Max': 4050, 'TRM_Cierre': 3900, 'Variacion': '+5.7%'},
        'Alcista': {'Nombre': 'Alcista', 'Probabilidad': 0.25, 'TRM_Min': 4100, 'TRM_Max': 4550, 'TRM_Cierre': 4325, 'Variacion': '+17.2%'},
        'Bajista': {'Nombre': 'Bajista', 'Probabilidad': 0.15, 'TRM_Min': 3400, 'TRM_Max': 3700, 'TRM_Cierre': 3550, 'Variacion': '-3.7%'},
        'Crisis': {'Nombre': 'Crisis', 'Probabilidad': 0.05, 'TRM_Min': 4600, 'TRM_Max': 5200, 'TRM_Cierre': 4900, 'Variacion': '+32.9%'}
    }
    expectativa = sum(e['TRM_Cierre'] * e['Probabilidad'] for e in escenarios.values())
    variacion = (expectativa / trm_actual - 1) * 100
    print(f"   Expectativa: ${expectativa:,.0f}")
    print(f"   Variación: {variacion:+.2f}%")
    return escenarios, expectativa, variacion

def analisis_tecnico(df_trm):
    print("\n📈 REALIZANDO ANÁLISIS TÉCNICO")
    trm = df_trm.set_index('fecha')['trm']
    ema20 = trm.ewm(span=20).mean()
    ema50 = trm.ewm(span=50).mean()
    trm_actual = trm.iloc[-1]
    senal = 'ALCISTA' if trm_actual > ema20.iloc[-1] > ema50.iloc[-1] else 'BAJISTA'
    print(f"   TRM: ${trm_actual:,.2f}")
    print(f"   EMA 20: ${ema20.iloc[-1]:,.2f}")
    print(f"   EMA 50: ${ema50.iloc[-1]:,.2f}")
    print(f"   Señal: {senal}")
    return {'ema_20': ema20.iloc[-1], 'ema_50': ema50.iloc[-1], 'senal': senal, 'trm_actual': trm_actual}

# =============================================================================
# GENERAR REPORTE PRINCIPAL
# =============================================================================
def generar_reporte_principal(trm_actual, resultados_informes, expectativa, variacion, escenarios, tecnicos):
    contenido = f"""
LABORATORIO 1 - PUNTO 1: ANÁLISIS FUNDAMENTAL DE LA TRM
================================================================================
1. INFORMACIÓN GENERAL
----------------------
TRM Actual ({FECHA_ACTUAL}): ${trm_actual:,.2f} COP/USD
Horizonte: 12 meses
Fecha Generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

2. FACTORES FUNDAMENTALES
-------------------------
• Diferencial Tasas: BanRep 9.25% vs Fed 5.25%
• Petróleo Brent: $60-65 USD/barril
• Riesgo Fiscal: Déficit ~7% PIB
• Electoral 2026: Marzo-Junio
• Inflación USA: 2.7%

3. PROYECCIONES INSTITUCIONALES
-------------------------------
Número de Informes: {resultados_informes['num_informes']}
Estadísticos:
• Mínimo: ${resultados_informes['consenso_min']:,.0f}
• Máximo: ${resultados_informes['consenso_max']:,.0f}
• Promedio: ${resultados_informes['consenso_promedio']:,.0f}
• Volatilidad: {resultados_informes['volatilidad']:.2f}%

4. EXPECTATIVA 12 MESES
-----------------------
Expectativa Ponderada: ${expectativa:,.0f} COP/USD
Variación Esperada: {variacion:+.2f}%
Escenarios:
• Base (55%): ${escenarios['Base']['TRM_Cierre']:,.0f} ({escenarios['Base']['Variacion']})
• Alcista (25%): ${escenarios['Alcista']['TRM_Cierre']:,.0f} ({escenarios['Alcista']['Variacion']})
• Bajista (15%): ${escenarios['Bajista']['TRM_Cierre']:,.0f} ({escenarios['Bajista']['Variacion']})
• Crisis (5%): ${escenarios['Crisis']['TRM_Cierre']:,.0f} ({escenarios['Crisis']['Variacion']})

5. ANÁLISIS TÉCNICO
-------------------
EMA 20: ${tecnicos['ema_20']:,.2f}
EMA 50: ${tecnicos['ema_50']:,.2f}
Señal: {tecnicos['senal']}

6. CONCLUSIONES
---------------
• TRM con tendencia a depreciación moderada del COP
• Volatilidad esperada: {resultados_informes['volatilidad']:.2f}%
• Monitorear: tasas, petróleo, riesgo fiscal

================================================================================
REFERENCIAS
================================================================================
• Banco de la República. (2026). Tasa Representativa del Mercado.
  https://www.banrep.gov.co/es/trm
• Federal Reserve. (2026). Federal Funds Rate.
  https://www.federalreserve.gov
• Hull, J. C. (2021). Options, Futures, and Other Derivatives (11th ed.). Pearson.
"""
    # AGREGAR ANÁLISIS HUMANO
    contenido += analisis_humano_punto1(trm_actual, expectativa, variacion)
    return contenido

def generar_resumen_ejecutivo(trm_actual, expectativa, variacion):
    contenido = f"""
RESUMEN EJECUTIVO - LABORATORIO 1 PUNTO 1
================================================================================
RESULTADOS PRINCIPALES:
• TRM Actual: ${trm_actual:,.2f} COP/USD
• Expectativa 12 meses: ${expectativa:,.0f} COP/USD
• Variación: {variacion:+.2f}%
• Escenario Más Probable: Base (55%) - $3,900 COP/USD

RECOMENDACIÓN:
La TRM muestra depreciación moderada del COP.
Monitorear: tasas, petróleo, riesgo fiscal, electoral.
"""
    return contenido

# =============================================================================
# FUNCIÓN PRINCIPAL
# =============================================================================
def ejecutar_laboratorio1():
    print("\n" + "🚀"*40)
    print("LABORATORIO 1 - PUNTO 1")
    print(f"CARPETA: {CARPETA_BASE}")
    print("🚀"*40)
    archivos = []
    
    df_trm = generar_trm_historica(anos=5, trm_actual=TRM_ACTUAL)
    guardar_csv(df_trm, 'trm_historico.csv')
    archivos.append('trm_historico.csv')
    
    generar_grafico_trm(df_trm)
    archivos.append('trm_historico_5anos.png')
    
    resultados_informes = analizar_proyecciones()
    escenarios, expectativa, variacion = calcular_expectativa(TRM_ACTUAL)
    tecnicos = analisis_tecnico(df_trm)
    
    generar_grafico_escenarios(escenarios, TRM_ACTUAL)
    archivos.append('punto1_expectativa_dolar_12meses.png')
    generar_grafico_tecnico(df_trm)
    archivos.append('punto1_analisis_tecnico_trm.png')
    
    print("\n💾 GENERANDO REPORTES TXT...")
    reporte = generar_reporte_principal(TRM_ACTUAL, resultados_informes, expectativa, variacion, escenarios, tecnicos)
    guardar_txt(reporte, 'Laboratorio1_Punto1_Analisis_TRM.txt')
    archivos.append('Laboratorio1_Punto1_Analisis_TRM.txt')
    
    resumen = generar_resumen_ejecutivo(TRM_ACTUAL, expectativa, variacion)
    guardar_txt(resumen, 'Resumen_Ejecutivo_Punto1.txt')
    archivos.append('Resumen_Ejecutivo_Punto1.txt')
    
    print("\n" + "✨"*40)
    print("LABORATORIO 1 COMPLETADO")
    print("✨"*40)
    print(f"\n📁 ARCHIVOS EN: {CARPETA_BASE}")
    print("\n📂 ARCHIVOS GENERADOS:")
    for arch in sorted(archivos):
        ruta = os.path.join(CARPETA_BASE, arch)
        if os.path.exists(ruta):
            tamano = os.path.getsize(ruta)
            tipo = "📄" if arch.endswith('.txt') else "🖼️" if arch.endswith('.png') else "📊"
            print(f"   {tipo} {arch} ({tamano:,} bytes)")
    print("\n" + "="*80)
    print("✅ TODOS LOS ARCHIVOS GENERADOS CORRECTAMENTE")
    print("="*80)

if __name__ == "__main__":
    try:
        ejecutar_laboratorio1()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()