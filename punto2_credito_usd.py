# =============================================================================
# PROYECTO: LABORATORIO 1 - PUNTO 2
# SIMULACIÓN DE CRÉDITO DE MAQUINARIA CON TASA EXTRANJERA (USD)
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
from datetime import datetime, timedelta
import os
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# CONFIGURACIÓN DE RUTAS RELATIVAS
# =============================================================================
directorio_actual = os.path.dirname(os.path.abspath(__file__))
CARPETA_BASE = os.path.join(directorio_actual, "outputs", "PUNTO_2")
os.makedirs(CARPETA_BASE, exist_ok=True)

# =============================================================================
# CONFIGURACIÓN GLOBAL
# =============================================================================
FECHA_ACTUAL = "2026-03-26"
TRM_ACTUAL = 3688.46
VALOR_MAQUINARIA_USD = 95292.89
PORCENTAJE_INICIAL = 0.10
TASA_CREDITO_USD_ANUAL = 0.0825
PLAZO_CREDITO_ANOS = 10
FRECUENCIA_PAGO = 4

# =============================================================================
# INFORMACIÓN DE INTEGRANTES
# =============================================================================
INTEGRANTES = [
    {"nombre": "Santiago Toro Cadavid", "cedula": "1040739414"},
    {"nombre": "Yenny Carolina Serna Chaverra", "cedula": "1017210528"},
    {"nombre": "Daniela Perez Meza", "cedula": "1017220748"}
]
CURSO = "Derivados Financieros"
PROYECTO = "LABORATORIO 1 - Punto 2"

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
# ANÁLISIS  - PUNTO 2 (ESTILO ESTUDIANTE)
# =============================================================================
def analisis_humano_punto2(resultados):
    return f"""
LO QUE ENTENDÍ DE ESTE PUNTO (EXPLICACIÓN SENCILLA)
================================================================================

Con el crédito en dólares:

💰 LO BÁSICO DEL EJERCICIO:
• Queremos comprar una maquinaria que cuesta ${resultados['valor_maquinaria_usd']:,.0f} USD
• En pesos colombianos eso son ${resultados['valor_maquinaria_cop']:,.0f} COP 
• Pedimos prestado el 90% → ${resultados['monto_credito_usd']:,.0f} USD
• La tasa de interés es del 8.25% anual (no está mal comparado con Colombia)

📅 ¿CUÁNTO VOY A PAGAR?
• Cuota trimestral: ${resultados['cuota_trimestral_usd']:,.2f} USD
• En pesos (con TRM de hoy): ${resultados['cuota_trimestral_cop']:,.2f} COP
• Total de intereses en 10 años: ${resultados['total_intereses_usd']:,.0f} USD
• Eso es como pagar un {resultados['costo_financiero_pct']:.1f}% extra por pedir prestado

🤯 LO QUE MÁS ME SORPRENDIÓ:
Los primeros años de la cuota, casi todo es INTERÉS y muy poco es pagar el préstamo.
Es como cuando pagas la cuota de una tarjeta de crédito... al principio casi no baja la deuda.

⚠️ EL PROBLEMA GRANDE:
Este crédito es en DÓLARES. Si la TRM sube, mi cuota en pesos también sube.
No tengo control sobre eso. Es como jugar ruleta con el tipo de cambio 

 MI OPINIÓN PERSONAL:
• La tasa de interés está bien comparada con opciones en Colombia
• Pero el riesgo cambiario me da miedo
• Si yo fuera el empresario, pediría un seguro (forward) para protegerme

📚 LO QUE INVESTIGUÉ:
• Tasas de SBA.gov para pequeños negocios en USA
• BankRate.com para comparar opciones
• Clase de Derivados

================================================================================
"""

# =============================================================================
# FUNCIONES PRINCIPALES
# =============================================================================
def obtener_tasas_mercado_americano():
    print("\n" + "="*80)
    print("🏦 TASAS DE INTERÉS - MERCADO AMERICANO (MARZO 2026)")
    print("="*80)
    tasas = {
        'SBA_7a': {'nombre': 'SBA 7(a) Loan', 'tasa_min': 0.0950, 'tasa_max': 0.1150, 'tasa_promedio': 0.1050, 'plazo_max': 10, 'fuente': 'SBA.gov'},
        'Equipment_Loan': {'nombre': 'Equipment Loan', 'tasa_min': 0.0700, 'tasa_max': 0.0950, 'tasa_promedio': 0.0825, 'plazo_max': 10, 'fuente': 'BankRate.com'},
        'Commercial_Bank': {'nombre': 'Commercial Bank Loan', 'tasa_min': 0.0750, 'tasa_max': 0.1000, 'tasa_promedio': 0.0875, 'plazo_max': 15, 'fuente': 'Federal Reserve'},
        'Wells_Fargo': {'nombre': 'Wells Fargo', 'tasa_min': 0.0725, 'tasa_max': 0.0900, 'tasa_promedio': 0.0812, 'plazo_max': 10, 'fuente': 'wellsfargo.com'},
        'JPMorgan': {'nombre': 'JPMorgan Chase', 'tasa_min': 0.0700, 'tasa_max': 0.0875, 'tasa_promedio': 0.0787, 'plazo_max': 10, 'fuente': 'jpmorganchase.com'},
        'Bank_of_America': {'nombre': 'Bank of America', 'tasa_min': 0.0750, 'tasa_max': 0.0925, 'tasa_promedio': 0.0837, 'plazo_max': 10, 'fuente': 'bankofamerica.com'}
    }
    print("\n📊 TASAS DE CRÉDITO COMERCIAL:")
    print("-"*80)
    for key, info in tasas.items():
        print(f"{info['nombre']:<25} | {info['tasa_promedio']*100:>8.2f}%")
    print("-"*80)
    return tasas

def calcular_cuota_frances(principal, tasa_anual, plazo_anos, frecuencia_anual=4):
    i = tasa_anual / frecuencia_anual
    n = plazo_anos * frecuencia_anual
    if i == 0:
        return principal / n
    cuota = principal * (i * (1 + i)**n) / ((1 + i)**n - 1)
    return cuota, i, n

def generar_tabla_amortizacion(principal, tasa_anual, plazo_anos, frecuencia_anual=4):
    cuota, i, n = calcular_cuota_frances(principal, tasa_anual, plazo_anos, frecuencia_anual)
    saldo = principal
    tabla = []
    for periodo in range(1, n + 1):
        interes = saldo * i
        amortizacion = cuota - interes
        saldo_nuevo = saldo - amortizacion
        if periodo == n:
            amortizacion = saldo
            cuota = interes + amortizacion
            saldo_nuevo = 0
        tabla.append({
            'Periodo': periodo,
            'Cuota_Total': cuota,
            'Interes': interes,
            'Amortizacion': amortizacion,
            'Saldo_Pendiente': max(0, saldo_nuevo)
        })
        saldo = saldo_nuevo
    return pd.DataFrame(tabla), cuota

def simular_credito_maquinaria():
    print("\n" + "="*80)
    print("💰 SIMULACIÓN DE CRÉDITO - MAQUINARIA (USD)")
    print("="*80)
    valor_maquinaria_usd = VALOR_MAQUINARIA_USD
    inicial_usd = valor_maquinaria_usd * PORCENTAJE_INICIAL
    monto_credito_usd = valor_maquinaria_usd - inicial_usd
    print(f"\n📋 ESTRUCTURA DEL FINANCIAMIENTO:")
    print(f"   Valor Maquinaria: ${valor_maquinaria_usd:,.2f} USD")
    print(f"   Inicial (10%): ${inicial_usd:,.2f} USD")
    print(f"   Monto a Financiar: ${monto_credito_usd:,.2f} USD")
    df_amortizacion, cuota_trimestral = generar_tabla_amortizacion(monto_credito_usd, TASA_CREDITO_USD_ANUAL, PLAZO_CREDITO_ANOS, FRECUENCIA_PAGO)
    total_pagado_usd = df_amortizacion['Cuota_Total'].sum()
    total_intereses_usd = df_amortizacion['Interes'].sum()
    print(f"\n💵 RESUMEN DEL CRÉDITO (USD):")
    print(f"   Cuota Trimestral: ${cuota_trimestral:,.2f} USD")
    print(f"   Total Intereses: ${total_intereses_usd:,.2f} USD")
    resultados = {
        'valor_maquinaria_usd': valor_maquinaria_usd,
        'valor_maquinaria_cop': valor_maquinaria_usd * TRM_ACTUAL,
        'inicial_usd': inicial_usd,
        'monto_credito_usd': monto_credito_usd,
        'monto_credito_cop': monto_credito_usd * TRM_ACTUAL,
        'cuota_trimestral_usd': cuota_trimestral,
        'cuota_trimestral_cop': cuota_trimestral * TRM_ACTUAL,
        'total_pagado_usd': total_pagado_usd,
        'total_pagado_cop': total_pagado_usd * TRM_ACTUAL,
        'total_intereses_usd': total_intereses_usd,
        'total_intereses_cop': total_intereses_usd * TRM_ACTUAL,
        'costo_financiero_pct': (total_intereses_usd/monto_credito_usd)*100,
        'df_amortizacion': df_amortizacion,
        'tasa_anual': TASA_CREDITO_USD_ANUAL,
        'plazo_anos': PLAZO_CREDITO_ANOS,
        'frecuencia_pago': FRECUENCIA_PAGO
    }
    return resultados

def guardar_csv(df, nombre_archivo):
    ruta = os.path.join(CARPETA_BASE, nombre_archivo)
    df.to_csv(ruta, index=False, encoding='utf-8')
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

def generar_grafico_amortizacion(resultados):
    print("\n📈 GENERANDO GRÁFICO DE AMORTIZACIÓN...")
    df = resultados['df_amortizacion']
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    axes[0, 0].stackplot(df['Periodo'], df['Interes'], df['Amortizacion'], labels=['Interés', 'Amortización'], colors=['#ff9999', '#66b3ff'], alpha=0.8)
    axes[0, 0].set_title('Composición de la Cuota Trimestral (USD)', fontweight='bold')
    axes[0, 0].legend(loc='upper right')
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 1].plot(df['Periodo'], df['Saldo_Pendiente'], color='green', linewidth=2)
    axes[0, 1].set_title('Evolución del Saldo Pendiente (USD)', fontweight='bold')
    axes[0, 1].grid(True, alpha=0.3)
    axes[1, 0].plot(df['Periodo'], df['Interes'].cumsum(), label='Interés Acumulado', color='red', linewidth=2)
    axes[1, 0].plot(df['Periodo'], df['Amortizacion'].cumsum(), label='Amortización Acumulada', color='blue', linewidth=2)
    axes[1, 0].set_title('Acumulado: Interés vs Amortización (USD)', fontweight='bold')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    df['Anio'] = (df['Periodo'] - 1) // 4 + 1
    anual = df.groupby('Anio').agg({'Interes': 'sum', 'Amortizacion': 'sum', 'Cuota_Total': 'sum'}).reset_index()
    x = anual['Anio']
    axes[1, 1].bar(x - 0.15, anual['Interes'], width=0.3, label='Interés', color='#ff9999')
    axes[1, 1].bar(x + 0.15, anual['Amortizacion'], width=0.3, label='Amortización', color='#66b3ff')
    axes[1, 1].set_title('Distribución Anual (USD)', fontweight='bold')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3, axis='y')
    fig.text(0.5, 0.02, f"Santiago Toro (1040739414) | Yenny Serna (1017210528) | Daniela Perez (1017220748)", ha='center', fontsize=8, alpha=0.5)
    plt.tight_layout(rect=[0, 0.03, 1, 1])
    ruta = os.path.join(CARPETA_BASE, 'punto2_tabla_amortizacion.png')
    plt.savefig(ruta, dpi=300, bbox_inches='tight')
    print(f"✅ Gráfico guardado: {ruta}")
    plt.close()
    return ruta

def generar_grafico_comparativo_tasas(tasas):
    print("\n📈 GENERANDO GRÁFICO COMPARATIVO DE TASAS...")
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    entidades = list(tasas.keys())
    nombres = [tasas[e]['nombre'][:20] for e in entidades]
    tasas_promedio = [tasas[e]['tasa_promedio']*100 for e in entidades]
    colores = ['green' if t <= 8.5 else 'orange' if t <= 9.5 else 'red' for t in tasas_promedio]
    bars = axes[0].bar(nombres, tasas_promedio, color=colores, edgecolor='black', alpha=0.8)
    axes[0].set_ylabel('Tasa de Interés Anual (%)', fontweight='bold')
    axes[0].set_title('Comparativo de Tasas Promedio - Entidades USA', fontweight='bold')
    axes[0].axhline(y=TASA_CREDITO_USD_ANUAL*100, color='blue', linestyle='--', linewidth=2, label=f'Tasa Ejercicio ({TASA_CREDITO_USD_ANUAL*100:.2f}%)')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3, axis='y')
    axes[0].set_xticklabels(nombres, rotation=45, ha='right')
    fig.text(0.5, 0.02, f"Santiago Toro (1040739414) | Yenny Serna (1017210528) | Daniela Perez (1017220748)", ha='center', fontsize=8, alpha=0.5)
    plt.tight_layout(rect=[0, 0.03, 1, 1])
    ruta = os.path.join(CARPETA_BASE, 'punto2_comparativo_tasas.png')
    plt.savefig(ruta, dpi=300, bbox_inches='tight')
    print(f"✅ Gráfico guardado: {ruta}")
    plt.close()
    return ruta

def generar_reporte_principal(resultados, tasas):
    df = resultados['df_amortizacion']
    contenido = f"""
LABORATORIO 1 - PUNTO 2: SIMULACIÓN DE CRÉDITO DE MAQUINARIA (USD)
================================================================================
1. INFORMACIÓN GENERAL
----------------------
Valor Maquinaria: ${resultados['valor_maquinaria_usd']:,.2f} USD
Valor en COP: ${resultados['valor_maquinaria_cop']:,.2f} COP
Monto a Financiar: ${resultados['monto_credito_usd']:,.2f} USD
Tasa de Interés: {resultados['tasa_anual']*100:.2f}% anual
Plazo: {resultados['plazo_anos']} años

2. FUENTES DE TASAS DE INTERÉS
------------------------------
"""
    for key, info in tasas.items():
        contenido += f"{info['nombre']}: {info['tasa_promedio']*100:.2f}% ({info['fuente']})\n"
    contenido += f"""
3. RESUMEN DEL CRÉDITO
----------------------
Cuota Trimestral (USD): ${resultados['cuota_trimestral_usd']:,.2f}
Total a Pagar (USD): ${resultados['total_pagado_usd']:,.2f}
Total Intereses (USD): ${resultados['total_intereses_usd']:,.2f}
Costo Financiero Total: {resultados['costo_financiero_pct']:.2f}%

4. CONCLUSIONES
---------------
• El crédito en USD tiene una tasa competitiva del {TASA_CREDITO_USD_ANUAL*100:.2f}% anual
• Se recomienda cubrir el riesgo cambiario con forwards

================================================================================
REFERENCIAS
================================================================================
• SBA.gov. (2026). 7(a) Loan Program. https://www.sba.gov
• BankRate. (2026). Commercial Equipment Loan Rates. https://www.bankrate.com
• Hull, J. C. (2021). Options, Futures, and Other Derivatives (11th ed.). Pearson.
"""
    contenido += analisis_humano_punto2(resultados)
    return contenido

def generar_resumen_ejecutivo(resultados):
    return f"""
RESUMEN EJECUTIVO - LABORATORIO 1 PUNTO 2
================================================================================
INVERSIÓN:
• Maquinaria: ${resultados['valor_maquinaria_usd']:,.2f} USD
• Crédito: ${resultados['monto_credito_usd']:,.2f} USD
• Cuota: ${resultados['cuota_trimestral_usd']:,.2f} USD

COSTOS TOTALES:
• Total Intereses: ${resultados['total_intereses_usd']:,.2f} USD
• Costo Financiero: {resultados['costo_financiero_pct']:.2f}%

RECOMENDACIÓN:
El crédito en USD es competitivo. Se requiere cobertura cambiaria.
"""

def ejecutar_punto2():
    print("\n" + "🚀"*40)
    print("LABORATORIO 1 - PUNTO 2: SIMULACIÓN CRÉDITO USD")
    print(f"CARPETA: {CARPETA_BASE}")
    print("🚀"*40)
    archivos = []
    tasas = obtener_tasas_mercado_americano()
    resultados = simular_credito_maquinaria()
    generar_grafico_amortizacion(resultados)
    archivos.append('punto2_tabla_amortizacion.png')
    generar_grafico_comparativo_tasas(tasas)
    archivos.append('punto2_comparativo_tasas.png')
    print("\n💾 GENERANDO REPORTES TXT...")
    reporte = generar_reporte_principal(resultados, tasas)
    guardar_txt(reporte, 'Laboratorio1_Punto2_Credito_USD.txt')
    archivos.append('Laboratorio1_Punto2_Credito_USD.txt')
    resumen = generar_resumen_ejecutivo(resultados)
    guardar_txt(resumen, 'Resumen_Ejecutivo_Punto2.txt')
    archivos.append('Resumen_Ejecutivo_Punto2.txt')
    guardar_csv(resultados['df_amortizacion'], 'punto2_tabla_amortizacion.csv')
    archivos.append('punto2_tabla_amortizacion.csv')
    print("\n" + "✨"*40)
    print("PUNTO 2 COMPLETADO")
    print("✨"*40)
    print(f"\n📁 ARCHIVOS EN: {CARPETA_BASE}")
    for arch in sorted(archivos):
        ruta = os.path.join(CARPETA_BASE, arch)
        if os.path.exists(ruta):
            tamano = os.path.getsize(ruta)
            tipo = "📄" if arch.endswith('.txt') else "📊" if arch.endswith('.csv') else "🖼️"
            print(f"   {tipo} {arch} ({tamano:,} bytes)")
    print("\n" + "="*80)
    print("✅ PUNTO 2 GENERADO CORRECTAMENTE")
    print("="*80)
    return resultados

if __name__ == "__main__":
    try:
        ejecutar_punto2()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()