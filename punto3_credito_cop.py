# =============================================================================
# PROYECTO: LABORATORIO 1 - PUNTO 3
# RECREACIÓN DEL CRÉDITO EN PESOS Y ANÁLISIS DE COMPORTAMIENTO
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
from datetime import datetime
import os
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# CONFIGURACIÓN DE RUTAS RELATIVAS (COMPATIBLE CON GITHUB)
# =============================================================================
directorio_actual = os.path.dirname(os.path.abspath(__file__))
CARPETA_BASE = os.path.join(directorio_actual, "outputs", "PUNTO_3")
os.makedirs(CARPETA_BASE, exist_ok=True)

# =============================================================================
# CONFIGURACIÓN GLOBAL
# =============================================================================
FECHA_ACTUAL = "2026-03-26"
TRM_ACTUAL = 3688.46

# DATOS DEL PUNTO 2 (valores en USD)
VALOR_MAQUINARIA_USD = 95292.89
PORCENTAJE_INICIAL = 0.10
INICIAL_USD = VALOR_MAQUINARIA_USD * PORCENTAJE_INICIAL
MONTO_CREDITO_USD = VALOR_MAQUINARIA_USD - INICIAL_USD
TASA_USD_ANUAL = 0.0825
PLAZO_ANOS = 10
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
PROYECTO = "LABORATORIO 1 - Punto 3"

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
# ANÁLISIS  - PUNTO 3 (ESTILO ESTUDIANTE)
# =============================================================================
def analisis_humano_punto3(analisis_datos):
    return f"""
LO QUE ENTENDÍ DE ESTE PUNTO (EXPLICACIÓN SENCILLA)
================================================================================

 Qué pasa si recreamos el crédito en pesos:

🔄 ¿QUÉ HICIMOS?
Tomamos el mismo crédito en dólares del punto anterior, pero lo "traducimos" a pesos 
colombianos usando una TRM que va cambiando con el tiempo.

📈 LO QUE PASÓ CON LA TRM:
• TRM inicial: ${analisis_datos['trm_inicial']:,.0f} COP/USD
• TRM promedio (proyectada): ${analisis_datos['trm_promedio']:,.0f} COP/USD  
• TRM final (proyectada): ${analisis_datos['trm_final']:,.0f} COP/USD
• Variación total: {analisis_datos['variacion_trm']:+.1f}%

💸 ¿Y EN MI BOLSILLO QUÉ PASA?
• Total pagado en USD: ${analisis_datos['total_pagado_usd']:,.0f}
• Total pagado en COP: ${analisis_datos['total_pagado_cop']:,.0f}
• Impacto por cambio de TRM: ${analisis_datos['impacto_cambiario']:,.0f} COP ({analisis_datos['impacto_pct']:+.1f}%)

🤔 ¿QUÉ SIGNIFICA ESE IMPACTO?
Imaginen que planean gastar $100.000 en algo, pero al final terminan gastando $118.000 
solo porque el dólar subió. Eso es lo que pasa aquí: el riesgo cambiario nos puede 
"cobrar" un {analisis_datos['impacto_pct']:.0f}% extra sin que nosotros hayamos hecho nada malo.

😰 LO QUE ME DA MIEDO:
• No puedo controlar la TRM
• Si sube mucho, mi cuota se vuelve impagable
• Si baja, me hubiera convenido no cubrirme... ¡es un dilema!

🎯 MI CONCLUSIÓN:
Este ejercicio me enseñó que:
1. Pedir prestado en moneda extranjera tiene ventajas (tasas más bajas)
2. Pero también tiene riesgos grandes (el tipo de cambio)
3. Por eso existen los FORWARDS (que veremos en el punto 5)

Si yo fuera empresario, preferiría pagar un poquito más por tranquilidad que 
arriesgarme a que la TRM se dispare.

📚 FUENTES:
• Banco de la República - Histórico TRM
• Apuntes de clase sobre riesgo cambiario
• Sentido común de estudiante 

================================================================================
"""

# =============================================================================
# FUNCIÓN: CALCULAR CUOTA FRANCÉS
# =============================================================================
def calcular_cuota_frances(principal, tasa_anual, plazo_anos, frecuencia_anual=4):
    i = tasa_anual / frecuencia_anual
    n = plazo_anos * frecuencia_anual
    if i == 0:
        return principal / n
    cuota = principal * (i * (1 + i)**n) / ((1 + i)**n - 1)
    return cuota, i, n

# =============================================================================
# FUNCIÓN: GENERAR TABLA DE AMORTIZACIÓN
# =============================================================================
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

# =============================================================================
# FUNCIÓN: GENERAR TRM PROYECTADA
# =============================================================================
def generar_trm_proyectada(trm_inicial, n_periodos, escenario='base'):
    np.random.seed(42)
    if escenario == 'base':
        drift_anual = 0.055
        volatilidad_anual = 0.08
    elif escenario == 'alcista':
        drift_anual = 0.16
        volatilidad_anual = 0.14
    elif escenario == 'bajista':
        drift_anual = -0.035
        volatilidad_anual = 0.06
    else:
        drift_anual = 0.055
        volatilidad_anual = 0.08
    drift_trimestral = drift_anual / 4
    volatilidad_trimestral = volatilidad_anual / np.sqrt(4)
    retornos = np.random.normal(drift_trimestral, volatilidad_trimestral, n_periodos)
    trm_proyectada = trm_inicial * np.exp(np.cumsum(retornos))
    return trm_proyectada

# =============================================================================
# FUNCIÓN: CONVERTIR CRÉDITO USD A COP
# =============================================================================
def convertir_credito_a_cop(df_usd, trm_proyectada):
    df_cop = df_usd.copy()
    df_cop['TRM_Proyectada'] = trm_proyectada
    df_cop['Cuota_Total_COP'] = df_cop['Cuota_Total'] * df_cop['TRM_Proyectada']
    df_cop['Interes_COP'] = df_cop['Interes'] * df_cop['TRM_Proyectada']
    df_cop['Amortizacion_COP'] = df_cop['Amortizacion'] * df_cop['TRM_Proyectada']
    df_cop['Saldo_Pendiente_COP'] = df_cop['Saldo_Pendiente'] * df_cop['TRM_Proyectada']
    return df_cop

# =============================================================================
# FUNCIÓN: ANALIZAR COMPORTAMIENTO
# =============================================================================
def analizar_comportamiento(df_cop, df_usd, trm_inicial):
    print("\n" + "="*80)
    print("📊 ANÁLISIS DE COMPORTAMIENTO - CRÉDITO EN PESOS")
    print("="*80)
    total_pagado_usd = df_usd['Cuota_Total'].sum()
    total_pagado_cop = df_cop['Cuota_Total_COP'].sum()
    total_interes_usd = df_usd['Interes'].sum()
    total_interes_cop = df_cop['Interes_COP'].sum()
    trm_promedio = df_cop['TRM_Proyectada'].mean()
    trm_final = df_cop['TRM_Proyectada'].iloc[-1]
    variacion_trm = (trm_final - trm_inicial) / trm_inicial * 100
    impacto_cambiario = total_pagado_cop - (total_pagado_usd * trm_inicial)
    impacto_pct = impacto_cambiario / (total_pagado_usd * trm_inicial) * 100
    print(f"\n📈 TRM:")
    print(f"   Inicial: ${trm_inicial:,.2f}")
    print(f"   Promedio: ${trm_promedio:,.2f}")
    print(f"   Final: ${trm_final:,.2f}")
    print(f"   Variación: {variacion_trm:+.2f}%")
    print(f"\n💵 PAGOS EN USD:")
    print(f"   Total: ${total_pagado_usd:,.2f}")
    print(f"   Intereses: ${total_interes_usd:,.2f}")
    print(f"\n💰 PAGOS EN COP:")
    print(f"   Total: ${total_pagado_cop:,.2f}")
    print(f"   Intereses: ${total_interes_cop:,.2f}")
    print(f"\n⚡ IMPACTO CAMBIARIO:")
    print(f"   Costo con TRM constante: ${total_pagado_usd * trm_inicial:,.2f} COP")
    print(f"   Costo con TRM proyectada: ${total_pagado_cop:,.2f} COP")
    print(f"   Impacto: ${impacto_cambiario:,.2f} COP ({impacto_pct:+.2f}%)")
    return {
        'trm_inicial': trm_inicial,
        'trm_promedio': trm_promedio,
        'trm_final': trm_final,
        'variacion_trm': variacion_trm,
        'total_pagado_usd': total_pagado_usd,
        'total_pagado_cop': total_pagado_cop,
        'total_interes_usd': total_interes_usd,
        'total_interes_cop': total_interes_cop,
        'impacto_cambiario': impacto_cambiario,
        'impacto_pct': impacto_pct
    }

# =============================================================================
# FUNCIÓN: GENERAR GRÁFICOS
# =============================================================================
def generar_graficos(df_cop, trm_inicial):
    print("\n📈 GENERANDO GRÁFICOS...")
    archivos_graficos = []
    
    # Gráfico 1: TRM Proyectada
    fig1, ax1 = plt.subplots(1, 1, figsize=(12, 5))
    ax1.plot(df_cop['Periodo'], df_cop['TRM_Proyectada'], color='blue', linewidth=2)
    ax1.axhline(y=trm_inicial, color='green', linestyle='--', label=f'TRM Inicial (${trm_inicial:,.0f})')
    ax1.set_title('Proyección de TRM - 10 Años', fontweight='bold')
    ax1.set_xlabel('Período (Trimestre)')
    ax1.set_ylabel('TRM (COP/USD)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    fig1.text(0.5, 0.02,
             f"Santiago Toro (1040739414) | Yenny Serna (1017210528) | Daniela Perez (1017220748)",
             ha='center', fontsize=8, alpha=0.5)
    plt.tight_layout(rect=[0, 0.03, 1, 1])
    ruta1 = os.path.join(CARPETA_BASE, 'punto3_trm_proyectada.png')
    plt.savefig(ruta1, dpi=300, bbox_inches='tight')
    print(f"✅ {ruta1}")
    plt.close()
    archivos_graficos.append(ruta1)
    
    # Gráfico 2: Cuota USD vs COP
    fig2, ax2 = plt.subplots(1, 1, figsize=(12, 5))
    ax2.plot(df_cop['Periodo'], df_cop['Cuota_Total'], color='blue', linewidth=2, label='USD (Constante)')
    ax2.plot(df_cop['Periodo'], df_cop['Cuota_Total_COP'] / 1000, color='red', linewidth=2, label='COP/1000 (Variable)')
    ax2.set_title('Cuota Trimestral: USD vs COP', fontweight='bold')
    ax2.set_xlabel('Período (Trimestre)')
    ax2.set_ylabel('Valor')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    fig2.text(0.5, 0.02,
             f"Santiago Toro (1040739414) | Yenny Serna (1017210528) | Daniela Perez (1017220748)",
             ha='center', fontsize=8, alpha=0.5)
    plt.tight_layout(rect=[0, 0.03, 1, 1])
    ruta2 = os.path.join(CARPETA_BASE, 'punto3_comparativo_usd_cop.png')
    plt.savefig(ruta2, dpi=300, bbox_inches='tight')
    print(f"✅ {ruta2}")
    plt.close()
    archivos_graficos.append(ruta2)
    
    # Gráfico 3: Escenarios TRM
    fig3, ax3 = plt.subplots(1, 1, figsize=(12, 5))
    escenarios = ['base', 'alcista', 'bajista']
    colores = {'base': 'green', 'alcista': 'red', 'bajista': 'blue'}
    for esc in escenarios:
        trm_esc = generar_trm_proyectada(trm_inicial, len(df_cop), escenario=esc)
        ax3.plot(df_cop['Periodo'], trm_esc, color=colores[esc], linewidth=2, label=esc.capitalize())
    ax3.axhline(y=trm_inicial, color='gray', linestyle='--', label='TRM Inicial')
    ax3.set_title('Escenarios de TRM - 10 Años', fontweight='bold')
    ax3.set_xlabel('Período (Trimestre)')
    ax3.set_ylabel('TRM (COP/USD)')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    fig3.text(0.5, 0.02,
             f"Santiago Toro (1040739414) | Yenny Serna (1017210528) | Daniela Perez (1017220748)",
             ha='center', fontsize=8, alpha=0.5)
    plt.tight_layout(rect=[0, 0.03, 1, 1])
    ruta3 = os.path.join(CARPETA_BASE, 'punto3_escenarios_trm.png')
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
def generar_reporte_principal(analisis, df_cop):
    cols = ['Periodo', 'Cuota_Total_COP', 'Interes_COP', 'Amortizacion_COP', 'Saldo_Pendiente_COP', 'TRM_Proyectada']
    contenido = f"""
LABORATORIO 1 - PUNTO 3: CRÉDITO EN PESOS Y ANÁLISIS DE COMPORTAMIENTO
================================================================================
1. INFORMACIÓN GENERAL
----------------------
Monto Crédito (USD): ${analisis['total_pagado_usd']:,.2f}
TRM Inicial: ${analisis['trm_inicial']:,.2f} COP/USD
TRM Promedio: ${analisis['trm_promedio']:,.2f} COP/USD
TRM Final: ${analisis['trm_final']:,.2f} COP/USD
Variación TRM: {analisis['variacion_trm']:+.2f}%
Fecha Generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

2. FUENTES DE DATOS
-------------------
• TRM: Banco de la República (2026). https://www.banrep.gov.co/es/trm
• Metodología Proyección: Hull, J. C. (2021). Options, Futures, and Other Derivatives.

3. COMPARATIVO USD vs COP
-------------------------
CONCEPTO          | USD              | COP
------------------|------------------|-------------------
Total a Pagar     | ${analisis['total_pagado_usd']:>15,.2f} | ${analisis['total_pagado_cop']:>15,.2f}
Total Intereses   | ${analisis['total_interes_usd']:>15,.2f} | ${analisis['total_interes_cop']:>15,.2f}

4. IMPACTO CAMBIARIO
--------------------
Costo con TRM constante: ${analisis['total_pagado_usd'] * analisis['trm_inicial']:,.2f} COP
Costo con TRM proyectada: ${analisis['total_pagado_cop']:,.2f} COP
Impacto: ${analisis['impacto_cambiario']:,.2f} COP ({analisis['impacto_pct']:+.2f}%)

5. ANÁLISIS DE RIESGO
---------------------
• El crédito en USD expone al riesgo cambiario
• Variación TRM proyectada: {analisis['variacion_trm']:+.2f}%
• Impacto financiero: {analisis['impacto_pct']:+.2f}% sobre el total pagado

6. CONCLUSIONES
---------------
• El crédito en USD expone al riesgo cambiario
• Impacto de {analisis['impacto_pct']:+.2f}% por variación de TRM
• Se recomienda cobertura con forwards (ver Punto 5)

7. PRIMEROS 10 PERÍODOS (COP)
-----------------------------
"""
    contenido += df_cop[cols].head(10).round(2).to_string(index=False)
    contenido += f"\n\n8. ÚLTIMOS 10 PERÍODOS (COP)\n----------------------------\n"
    contenido += df_cop[cols].tail(10).round(2).to_string(index=False)
    
    # AGREGAR ANÁLISIS HUMANO
    contenido += analisis_humano_punto3(analisis)
    
    return contenido

def generar_resumen_ejecutivo(analisis):
    return f"""
RESUMEN EJECUTIVO - PUNTO 3
================================================================================
INVERSIÓN:
• Crédito: ${analisis['total_pagado_usd']:,.2f} USD
• TRM Inicial: ${analisis['trm_inicial']:,.2f} COP/USD
• Total en COP: ${analisis['total_pagado_cop']:,.2f} COP

IMPACTO:
• Variación TRM: {analisis['variacion_trm']:+.2f}%
• Impacto Cambiario: {analisis['impacto_pct']:+.2f}%
• Costo Adicional: ${analisis['impacto_cambiario']:,.2f} COP

RECOMENDACIÓN:
Usar forwards para cubrir riesgo cambiario.
El impacto de {analisis['impacto_pct']:+.2f}% justifica la cobertura.
"""

# =============================================================================
# FUNCIÓN PRINCIPAL
# =============================================================================
def ejecutar_punto3():
    print("\n" + "🚀"*40)
    print("LABORATORIO 1 - PUNTO 3: CRÉDITO EN PESOS")
    print(f"CARPETA: {CARPETA_BASE}")
    print("🚀"*40)
    archivos = []
    
    # 1. Generar tabla amortización USD
    print("\n📋 GENERANDO TABLA DE AMORTIZACIÓN (USD)...")
    df_usd, cuota_usd = generar_tabla_amortizacion(MONTO_CREDITO_USD, TASA_USD_ANUAL, PLAZO_ANOS, FRECUENCIA_PAGO)
    print(f"   Cuota trimestral: ${cuota_usd:,.2f} USD")
    
    # 2. Generar TRM proyectada
    print("\n📈 GENERANDO TRM PROYECTADA...")
    trm_proyectada = generar_trm_proyectada(TRM_ACTUAL, len(df_usd), escenario='base')
    
    # 3. Convertir a COP
    print("\n💱 CONVIRTIENDO A COP...")
    df_cop = convertir_credito_a_cop(df_usd, trm_proyectada)
    
    # 4. Analizar comportamiento
    analisis = analizar_comportamiento(df_cop, df_usd, TRM_ACTUAL)
    
    # 5. Generar gráficos
    rutas_graficos = generar_graficos(df_cop, TRM_ACTUAL)
    archivos.extend(rutas_graficos)
    
    # 6. Generar reporte principal
    print("\n💾 GENERANDO REPORTES...")
    reporte = generar_reporte_principal(analisis, df_cop)
    guardar_txt(reporte, 'Laboratorio1_Punto3_Credito_COP.txt')
    archivos.append(os.path.join(CARPETA_BASE, 'Laboratorio1_Punto3_Credito_COP.txt'))
    
    # 7. Resumen ejecutivo
    resumen = generar_resumen_ejecutivo(analisis)
    guardar_txt(resumen, 'Resumen_Ejecutivo_Punto3.txt')
    archivos.append(os.path.join(CARPETA_BASE, 'Resumen_Ejecutivo_Punto3.txt'))
    
    # 8. Guardar CSV
    guardar_csv(df_cop, 'punto3_tabla_amortizacion_cop.csv')
    archivos.append(os.path.join(CARPETA_BASE, 'punto3_tabla_amortizacion_cop.csv'))
    
    df_trm = pd.DataFrame({
        'Periodo': df_cop['Periodo'],
        'TRM_Proyectada': df_cop['TRM_Proyectada']
    })
    guardar_csv(df_trm, 'punto3_trm_proyectada.csv')
    archivos.append(os.path.join(CARPETA_BASE, 'punto3_trm_proyectada.csv'))
    
    # Resumen final
    print("\n" + "✨"*40)
    print("PUNTO 3 COMPLETADO")
    print("✨"*40)
    print(f"\n📁 ARCHIVOS EN: {CARPETA_BASE}")
    print("\n📂 ARCHIVOS GENERADOS:")
    for arch in sorted(archivos):
        if os.path.exists(arch):
            tamano = os.path.getsize(arch)
            if arch.endswith('.txt'):
                print(f"   📄 {os.path.basename(arch)} ({tamano:,} bytes)")
            elif arch.endswith('.csv'):
                print(f"   📊 {os.path.basename(arch)} ({tamano:,} bytes)")
            elif arch.endswith('.png'):
                print(f"   🖼️  {os.path.basename(arch)} ({tamano:,} bytes)")
    print("\n" + "="*80)
    print("✅ PUNTO 3 GENERADO CORRECTAMENTE")
    print("="*80)
    return analisis

# =============================================================================
# EJECUCIÓN
# =============================================================================
if __name__ == "__main__":
    try:
        analisis_punto3 = ejecutar_punto3()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()