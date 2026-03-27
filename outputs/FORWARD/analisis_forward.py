# ============================================================================
# LABORATORIO DERIVADOS FINANCIEROS - FORWARD Y COBERTURA CAMBIARIA
# ANÁLISIS DE INVERSIÓN CON COBERTURA FORWARD
# ============================================================================
# CURSO: Derivados Financieros
# INTEGRANTES:
# 1. Santiago Toro Cadavid - Cédula: 1040739414
# 2. Yenny Carolina Serna Chaverra - Cédula: 1017210528
# 3. Daniela Perez Meza - Cédula: 1017220748
# FECHA: 2026
# ============================================================================

import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import norm
from datetime import datetime, timedelta
import os
import warnings
from dateutil.relativedelta import relativedelta

# Configuración
warnings.filterwarnings('ignore')
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

print("="*100)
print(" "*20 + "LABORATORIO DE DERIVADOS FINANCIEROS")
print(" "*25 + "PUNTO 5: PROCESO DE FORWARD")
print("="*100)
print(f"\nFecha de ejecución: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Integrantes: Santiago Toro, Yenny Serna, Daniela Perez")
print()

# ============================================================================
# 1. CONFIGURACIÓN DE RUTA Y CARPETAS
# ============================================================================

ruta_base = r"C:\Users\santi\OneDrive\Pictures\Derivados\Laboratorio\FORWARD"

try:
    if not os.path.exists(ruta_base):
        os.makedirs(ruta_base)
        print(f"✅ Carpeta CREADA exitosamente: {ruta_base}")
    else:
        print(f"✅ Carpeta EXISTE: {ruta_base}")
except Exception as e:
    print(f"⚠️  Error con OneDrive: {e}")
    ruta_base = os.path.join(os.path.expanduser("~"), "Desktop", "FORWARD_LAB")
    os.makedirs(ruta_base, exist_ok=True)
    print(f"📁 Usando ruta alternativa: {ruta_base}")

print(f"\n📂 Todos los archivos se guardarán en: {ruta_base}")
print()

# ============================================================================
# 2. DATOS DEL FORWARD SET-FX (INFORMACIÓN PROPORCIONADA)
# ============================================================================

print("="*100)
print("SECCIÓN 1: INFORMACIÓN FORWARD SET-FX - PLAZO SUPERIOR A 6 MESES")
print("="*100)

# Datos completos de la SET-FX proporcionados
forward_set_fx = {
    'mercado': 'FORWARD',
    'moneda': 'USD/COP',
    'plazo': 'mayores a 6 meses',
    'monto_acumulado': 76002361.44,
    'apertura': 3870.82,
    'cierre': 3968.63,
    'no_transacciones': 42,
    'promedio': 3933.98,
    'precio_min': 3813.51,
    'precio_max': 4226.05,
    'monto_promedio': 1809580.03,
    'monto_min': 7057.92,
    'monto_max': 20000000.00,
    'monto_ultimo': 40307.20,
    'fecha_reporte': '26/03/2026'
}

# Tasa forward seleccionada (usamos el cierre como referencia principal)
FORWARD_RATE = forward_set_fx['cierre']
FORWARD_RATE_PROM = forward_set_fx['promedio']
SPOT_REFERENCE = 3900  # Spot de referencia aproximado

print("\n📋 DOCUMENTACIÓN DE LA ELECCIÓN DEL FORWARD:")
print("-"*100)
print(f"✓ Mercado: {forward_set_fx['mercado']}")
print(f"✓ Par cambiario: {forward_set_fx['moneda']}")
print(f"✓ Plazo seleccionado: {forward_set_fx['plazo']}")
print(f"✓ Fecha de reporte SET-FX: {forward_set_fx['fecha_reporte']}")
print()
print("📊 TASAS FORWARD DISPONIBLES:")
print(f"  • Apertura:           ${forward_set_fx['apertura']:>12,.2f} COP/USD")
print(f"  • Cierre (SELECCIONADA): ${forward_set_fx['cierre']:>12,.2f} COP/USD ←")
print(f"  • Promedio:           ${forward_set_fx['promedio']:>12,.2f} COP/USD")
print(f"  • Mínimo:             ${forward_set_fx['precio_min']:>12,.2f} COP/USD")
print(f"  • Máximo:             ${forward_set_fx['precio_max']:>12,.2f} COP/USD")
print()
print("📈 ESTADÍSTICAS DE TRANSACCIONES:")
print(f"  • Número total de transacciones: {forward_set_fx['no_transacciones']}")
print(f"  • Monto acumulado negociado: ${forward_set_fx['monto_acumulado']:,.2f} USD")
print(f"  • Monto promedio por transacción: ${forward_set_fx['monto_promedio']:,.2f} USD")
print()
print("💡 JUSTIFICACIÓN DE LA ELECCIÓN:")
print(f"  Se selecciona la tasa de CIERRE (${FORWARD_RATE:,.2f}) por ser:")
print(f"  - El precio de mercado al cierre de la jornada")
print(f"  • Representativo de las condiciones actuales del mercado")
print(f"  - Utilizado como referencia para valoración de contratos")
print(f"  • Consistente con prácticas de valoración financiera")
print()

# Guardar datos forward en CSV
df_forward = pd.DataFrame([forward_set_fx])
df_forward.to_csv(os.path.join(ruta_base, "forward_setfx_datos.csv"), index=False, encoding='utf-8')
print("✅ Datos forward guardados: forward_setfx_datos.csv")
print()

# ============================================================================
# 3. DESCARGA Y ANÁLISIS DE DATOS SPOT USDCOP=X
# ============================================================================

print("="*100)
print("SECCIÓN 2: DESCARGA Y ANÁLISIS DE DATOS SPOT USDCOP=X")
print("="*100)

try:
    print("\n⏳ Descargando datos históricos de Yahoo Finance (USDCOP=X)...")
    
    # Descargar 2 años de datos históricos
    spot_data = yf.download('USDCOP=X', period='2y', interval='1d', progress=False)
    
    if len(spot_data) > 0:
        spot_data = spot_data.reset_index()
        
        # Manejar diferentes nombres de columnas
        if 'Date' in spot_data.columns:
            spot_data = spot_data.rename(columns={'Date': 'Fecha'})
        if 'Close' in spot_data.columns:
            spot_data['Spot'] = spot_data['Close']
        
        spot_data['Fecha'] = pd.to_datetime(spot_data['Fecha'])
        spot_data = spot_data[['Fecha', 'Spot', 'Open', 'High', 'Low', 'Volume']].dropna()
        
        # Calcular estadísticas
        spot_actual = spot_data['Spot'].iloc[-1]
        spot_min = spot_data['Spot'].min()
        spot_max = spot_data['Spot'].max()
        spot_prom = spot_data['Spot'].mean()
        spot_std = spot_data['Spot'].std()
        
        # Calcular retornos
        spot_data['Retorno_Diario'] = spot_data['Spot'].pct_change()
        spot_data['Retorno_Log'] = np.log(spot_data['Spot'] / spot_data['Spot'].shift(1))
        
        print(f"\n✅ Datos descargados exitosamente")
        print(f"\n📊 RESUMEN DE DATOS SPOT:")
        print(f"  • Período: {spot_data['Fecha'].min().strftime('%Y-%m-%d')} a {spot_data['Fecha'].max().strftime('%Y-%m-%d')}")
        print(f"  • Total de observaciones: {len(spot_data):,} días hábiles")
        print(f"  • Spot actual (último): ${spot_actual:,.2f} COP/USD")
        print(f"  • Spot mínimo (período): ${spot_min:,.2f}")
        print(f"  • Spot máximo (período): ${spot_max:,.2f}")
        print(f"  • Spot promedio: ${spot_prom:,.2f}")
        print(f"  • Desviación estándar: ${spot_std:,.2f}")
        print(f"  • Volatilidad histórica: {(spot_std/spot_prom)*100:.2f}%")
        
        # Guardar datos spot
        spot_data.to_csv(os.path.join(ruta_base, "spot_usdcop_historico.csv"), index=False, encoding='utf-8')
        print(f"\n✅ Datos spot guardados: spot_usdcop_historico.csv")
        
    else:
        raise Exception("No se pudieron descargar datos")
        
except Exception as e:
    print(f"\n⚠️  Error al descargar: {e}")
    print("Generando datos simulados basados en el forward...")
    
    # Datos simulados como backup
    np.random.seed(42)
    fechas = pd.date_range(end=datetime.now(), periods=504, freq='B')  # 2 años
    spot_sim = np.zeros(len(fechas))
    spot_sim[0] = 3800
    
    for i in range(1, len(fechas)):
        retorno = np.random.normal(0.0001, 0.008)
        spot_sim[i] = spot_sim[i-1] * (1 + retorno)
    
    # Ajustar para que termine cerca del forward
    spot_sim = spot_sim * (FORWARD_RATE / spot_sim[-1])
    
    spot_data = pd.DataFrame({
        'Fecha': fechas,
        'Spot': spot_sim,
        'Open': spot_sim * (1 + np.random.normal(0, 0.001, len(fechas))),
        'High': spot_sim * (1 + np.abs(np.random.normal(0, 0.002, len(fechas)))),
        'Low': spot_sim * (1 - np.abs(np.random.normal(0, 0.002, len(fechas)))),
        'Volume': np.random.randint(1000000, 10000000, len(fechas))
    })
    
    spot_data['Retorno_Diario'] = spot_data['Spot'].pct_change()
    spot_data['Retorno_Log'] = np.log(spot_data['Spot'] / spot_data['Spot'].shift(1))
    
    spot_actual = spot_data['Spot'].iloc[-1]
    spot_min = spot_data['Spot'].min()
    spot_max = spot_data['Spot'].max()
    spot_prom = spot_data['Spot'].mean()
    spot_std = spot_data['Spot'].std()
    
    print(f"✅ Datos simulados generados (usar con precaución)")
    print(f"   Spot actual: ${spot_actual:,.2f}")

print()

# ============================================================================
# 4. PARÁMETROS DE LA INVERSIÓN
# ============================================================================

print("="*100)
print("SECCIÓN 3: PARÁMETROS DE LA INVERSIÓN CON FORWARD")
print("="*100)

# PARÁMETROS DE LA INVERSIÓN (AJUSTABLES)
MONTO_INVERSION_USD = 500000        # Monto de la inversión en USD
PLAZO_FORWARD_MESES = 6             # Plazo del forward en meses
TASA_CREDITO_EA = 0.1131            # Tasa de interés del crédito (11.31% E.A. - DTF + margen)
TASA_LIBOR_ANUAL = 0.045            # Tasa LIBOR/SOFR anual (4.5%)
SPREAD_CREDITO = 0.03               # Spread sobre LIBOR (3%)
MONTO_CREDITO_PCT = 0.80            # Porcentaje financiado con crédito (80%)
PLAZO_CREDITO_MESES = 6             # Plazo del crédito en meses

print(f"\n💰 CARACTERÍSTICAS DE LA INVERSIÓN:")
print(f"  • Monto total de inversión: ${MONTO_INVERSION_USD:,.0f} USD")
print(f"  • Plazo de la cobertura forward: {PLAZO_FORWARD_MESES} meses")
print(f"  • Fecha de vencimiento: {(datetime.now() + relativedelta(months=PLAZO_FORWARD_MESES)).strftime('%Y-%m-%d')}")
print()

print(f"🏦 CONDICIONES DEL CRÉDITO:")
print(f"  • Tasa de interés: {TASA_CREDITO_EA*100:.2f}% E.A.")
print(f"  • Tasa LIBOR de referencia: {TASA_LIBOR_ANUAL*100:.2f}%")
print(f"  • Spread aplicado: {SPREAD_CREDITO*100:.2f}%")
print(f"  • Porcentaje financiado: {MONTO_CREDITO_PCT*100:.0f}%")
print(f"  • Plazo del crédito: {PLAZO_CREDITO_MESES} meses")
print()

# Cálculos preliminares
monto_financiado_usd = MONTO_INVERSION_USD * MONTO_CREDITO_PCT
pago_inicial_usd = MONTO_INVERSION_USD * (1 - MONTO_CREDITO_PCT)

valor_cop_spot_actual = MONTO_INVERSION_USD * spot_actual
valor_cop_forward = MONTO_INVERSION_USD * FORWARD_RATE

tasa_mensual_credito = (1 + TASA_CREDITO_EA)**(1/12) - 1
intereses_6_meses = monto_financiado_usd * spot_actual * ((1 + tasa_mensual_credito)**PLAZO_CREDITO_MESES - 1)

print(f"💵 ESTRUCTURA DE FINANCIAMIENTO:")
print(f"  • Monto financiado: ${monto_financiado_usd:,.0f} USD ({MONTO_CREDITO_PCT*100:.0f}%)")
print(f"  • Pago inicial: ${pago_inicial_usd:,.0f} USD ({(1-MONTO_CREDITO_PCT)*100:.0f}%)")
print(f"  • Valor al spot actual (${spot_actual:,.2f}): ${valor_cop_spot_actual:,.0f} COP")
print(f"  • Valor con forward (${FORWARD_RATE:,.2f}): ${valor_cop_forward:,.0f} COP")
print(f"  • Diferencia: ${valor_cop_forward - valor_cop_spot_actual:,.0f} COP ({((FORWARD_RATE/spot_actual)-1)*100:+.2f}%)")
print(f"  • Intereses crédito ({PLAZO_CREDITO_MESES} meses): ${intereses_6_meses:,.0f} COP")
print()

# ============================================================================
# 5. SIMULACIÓN MONTE CARLO DEL SPOT FUTURO
# ============================================================================

print("="*100)
print("SECCIÓN 4: SIMULACIÓN MONTE CARLO - PROYECCIÓN SPOT FUTURO")
print("="*100)

# Calcular parámetros para la simulación
retornos = spot_data['Retorno_Log'].dropna()
mu_diario = retornos.mean()
sigma_diario = retornos.std()

# Annualizar
mu_anual = mu_diario * 252
sigma_anual = sigma_diario * np.sqrt(252)

print(f"\n📊 PARÁMETROS ESTADÍSTICOS PARA SIMULACIÓN:")
print(f"  • Retorno diario promedio: {mu_diario:.8f} ({mu_diario*100:.6f}%)")
print(f"  • Volatilidad diaria: {sigma_diario:.8f} ({sigma_diario*100:.6f}%)")
print(f"  • Retorno anualizado: {mu_anual:.6f} ({mu_anual*100:.4f}%)")
print(f"  • Volatilidad anualizada: {sigma_anual:.6f} ({sigma_anual*100:.4f}%)")
print()

# Parámetros de simulación
n_simulaciones = 50000  # 50,000 simulaciones para mayor precisión
dias_proyeccion = int(PLAZO_FORWARD_MESES * 21.5)  # Días hábiles aproximados
T = PLAZO_FORWARD_MESES / 12  # en años

print(f"⚙️  CONFIGURACIÓN DE LA SIMULACIÓN:")
print(f"  • Número de simulaciones: {n_simulaciones:,}")
print(f"  • Días de proyección: {dias_proyeccion}")
print(f"  • Horizonte temporal: {PLAZO_FORWARD_MESES} meses ({T:.4f} años)")
print(f"  • Tasa forward de referencia: ${FORWARD_RATE:,.2f}")
print()

# Simulación Monte Carlo usando Geometric Brownian Motion
print("⏳ Ejecutando simulación Monte Carlo...")
np.random.seed(42)

dt = 1/252  # paso de tiempo diario

# Generar caminos aleatorios
Z = np.random.standard_normal((n_simulaciones, dias_proyeccion))
paths = np.zeros((n_simulaciones, dias_proyeccion + 1))
paths[:, 0] = spot_actual

for t in range(1, dias_proyeccion + 1):
    paths[:, t] = paths[:, t-1] * np.exp(
        (mu_diario - 0.5 * sigma_diario**2) + sigma_diario * Z[:, t-1]
    )

# Valores finales de las simulaciones (al cabo de 6 meses)
spot_futuro_simulado = paths[:, -1]

print(f"✅ Simulación completada exitosamente")
print()

print(f"📈 RESULTADOS DE LA SIMULACIÓN:")
print(f"  • Spot inicial: ${spot_actual:,.2f}")
print(f"  • Spot simulado (media): ${spot_futuro_simulado.mean():,.2f}")
print(f"  • Spot simulado (mediana): ${np.median(spot_futuro_simulado):,.2f}")
print(f"  • Spot simulado (desviación): ${spot_futuro_simulado.std():,.2f}")
print(f"  • Spot simulado (mínimo): ${spot_futuro_simulado.min():,.2f}")
print(f"  • Spot simulado (máximo): ${spot_futuro_simulado.max():,.2f}")
print(f"  • Forward contratado: ${FORWARD_RATE:,.2f}")
print(f"  • Diferencia media vs forward: ${spot_futuro_simulado.mean() - FORWARD_RATE:+,.2f}")
print()

# Calcular percentiles importantes
percentiles = {
    '5%': np.percentile(spot_futuro_simulado, 5),
    '10%': np.percentile(spot_futuro_simulado, 10),
    '25%': np.percentile(spot_futuro_simulado, 25),
    '50% (Mediana)': np.percentile(spot_futuro_simulado, 50),
    '75%': np.percentile(spot_futuro_simulado, 75),
    '90%': np.percentile(spot_futuro_simulado, 90),
    '95%': np.percentile(spot_futuro_simulado, 95)
}

print(f"📊 PERCENTILES DE LA DISTRIBUCIÓN:")
for p, v in percentiles.items():
    diff_vs_forward = v - FORWARD_RATE
    simbolo = "↑" if diff_vs_forward > 0 else "↓"
    print(f"  • {p:15s}: ${v:>12,.2f}  (vs Forward: {diff_vs_forward:+,.2f} {simbolo})")
print()

# ============================================================================
# 6. ANÁLISIS DE PROTECCIÓN - EVENTOS PROTEGIDOS VS NO PROTEGIDOS
# ============================================================================

print("="*100)
print("SECCIÓN 5: ANÁLISIS DE PROTECCIÓN - EVALUACIÓN DE ESCENARIOS")
print("="*100)

# Clasificación de escenarios
escenarios_protegidos = spot_futuro_simulado > FORWARD_RATE
escenarios_no_protegidos = spot_futuro_simulado <= FORWARD_RATE

n_protegidos = escenarios_protegidos.sum()
n_no_protegidos = escenarios_no_protegidos.sum()
pct_protegidos = (n_protegidos / n_simulaciones) * 100
pct_no_protegidos = 100 - pct_protegidos

print(f"\n🛡️  CLASIFICACIÓN DE ESCENARIOS DE PROTECCIÓN:")
print(f"\n✅ ESCENARIOS PROTEGIDOS (Spot Futuro > Forward):")
print(f"  • Cantidad: {n_protegidos:,} escenarios")
print(f"  • Porcentaje: {pct_protegidos:.2f}%")
print(f"  • Interpretación: El forward ES BENEFICIOSO - se paga menos que el spot de mercado")
print()

print(f"❌ ESCENARIOS NO PROTEGIDOS (Spot Futuro ≤ Forward):")
print(f"  • Cantidad: {n_no_protegidos:,} escenarios")
print(f"  • Porcentaje: {pct_no_protegidos:.2f}%")
print(f"  • Interpretación: El forward NO ES BENEFICIOSO - se paga más o igual que el spot")
print()

# Análisis detallado de ganancias y pérdidas
print(f"💰 ANÁLISIS DE GANANCIAS Y PÉRDIDAS POR ESCENARIO:")
print("-"*100)

# Cuando está protegido (gana con el forward)
ahorro_por_escenario = (spot_futuro_simulado[escenarios_protegidos] - FORWARD_RATE) * MONTO_INVERSION_USD
print(f"\n✅ ESCENARIOS PROTEGIDOS - AHORROS:")
print(f"  • Ahorro mínimo: ${ahorro_por_escenario.min():,.0f} COP")
print(f"  • Ahorro máximo: ${ahorro_por_escenario.max():,.0f} COP")
print(f"  • Ahorro promedio: ${ahorro_por_escenario.mean():,.0f} COP")
print(f"  • Ahorro mediano: ${np.median(ahorro_por_escenario):,.0f} COP")
print(f"  • Desviación del ahorro: ${ahorro_por_escenario.std():,.0f} COP")
print(f"  • Ahorro total esperado: ${ahorro_por_escenario.sum():,.0f} COP")
print()

# Cuando NO está protegido (pierde con el forward)
perdida_por_escenario = (FORWARD_RATE - spot_futuro_simulado[escenarios_no_protegidos]) * MONTO_INVERSION_USD
print(f"❌ ESCENARIOS NO PROTEGIDOS - PÉRDIDAS (COSTO DE OPORTUNIDAD):")
print(f"  • Pérdida mínima: ${perdida_por_escenario.min():,.0f} COP")
print(f"  • Pérdida máxima: ${perdida_por_escenario.max():,.0f} COP")
print(f"  • Pérdida promedio: ${perdida_por_escenario.mean():,.0f} COP")
print(f"  • Pérdida mediana: ${np.median(perdida_por_escenario):,.0f} COP")
print(f"  • Desviación de la pérdida: ${perdida_por_escenario.std():,.0f} COP")
print()

# Valor esperado de la cobertura
valor_esperado_cobertura = (spot_futuro_simulado - FORWARD_RATE) * MONTO_INVERSION_USD
print(f"📊 VALOR ESPERADO DE LA COBERTURA FORWARD:")
print(f"  • Valor esperado: ${valor_esperado_cobertura.mean():,.0f} COP")
print(f"  • Desviación estándar: ${valor_esperado_cobertura.std():,.0f} COP")
print(f"  • Coeficiente de variación: {valor_esperado_cobertura.std()/abs(valor_esperado_cobertura.mean()):.2f}")
print()

# Umbrales de protección
print(f"🎯 UMBRALES DE PROTECCIÓN BAJO VOLATILIDAD:")
umbrales = {
    'Spot = Forward': FORWARD_RATE,
    'Spot = Forward + 1%': FORWARD_RATE * 1.01,
    'Spot = Forward + 2%': FORWARD_RATE * 1.02,
    'Spot = Forward + 5%': FORWARD_RATE * 1.05,
    'Spot = Forward - 1%': FORWARD_RATE * 0.99,
    'Spot = Forward - 2%': FORWARD_RATE * 0.98,
    'Spot = Forward - 5%': FORWARD_RATE * 0.95
}

for nombre, umbral in umbrales.items():
    prob = (spot_futuro_simulado > umbral).sum() / n_simulaciones * 100
    diff = ((umbral / FORWARD_RATE) - 1) * 100
    print(f"  • {nombre:30s}: ${umbral:>10,.2f} ({diff:+.2f}%) → Probabilidad: {prob:.2f}%")
print()

# ============================================================================
# 7. ANÁLISIS DE FLUJO TOTAL - CRÉDITO VS FORWARD
# ============================================================================

print("="*100)
print("SECCIÓN 6: ANÁLISIS DE FLUJO TOTAL - CRÉDITO VS FORWARD")
print("="*100)

print(f"\n🏦 CÁLCULO DEL FLUJO DE CAJA COMPLETO:")
print("-"*100)

# Tasa mensual del crédito
tasa_mensual = (1 + TASA_CREDITO_EA)**(1/12) - 1

# Monto del crédito en COP (al spot actual)
monto_credito_cop = monto_financiado_usd * spot_actual

# Cálculo de intereses y cuota
cuota_mensual = monto_credito_cop * (tasa_mensual * (1 + tasa_mensual)**PLAZO_CREDITO_MESES) / \
                ((1 + tasa_mensual)**PLAZO_CREDITO_MESES - 1)
total_intereses = (cuota_mensual * PLAZO_CREDITO_MESES) - monto_credito_cop
total_pagar_credito = monto_credito_cop + total_intereses

print(f"\n📋 ESTRUCTURA DEL CRÉDITO:")
print(f"  • Monto financiado en USD: ${monto_financiado_usd:,.0f}")
print(f"  • Tasa de cambio spot: ${spot_actual:,.2f}")
print(f"  • Monto del crédito en COP: ${monto_credito_cop:,.0f}")
print(f"  • Tasa mensual: {tasa_mensual*100:.4f}%")
print(f"  • Plazo: {PLAZO_CREDITO_MESES} meses")
print(f"  • Cuota mensual: ${cuota_mensual:,.0f} COP")
print(f"  • Total intereses: ${total_intereses:,.0f} COP")
print(f"  • Total a pagar (crédito): ${total_pagar_credito:,.0f} COP")
print()

# ESCENARIO 1: SIN COBERTURA FORWARD
print(f"\n📊 ESCENARIO 1 - SIN COBERTURA FORWARD:")
print("-"*100)

# Pago de la inversión al spot futuro (esperado)
pago_inversion_spot_promedio = spot_futuro_simulado.mean() * MONTO_INVERSION_USD
pago_inversion_spot_mediana = np.median(spot_futuro_simulado) * MONTO_INVERSION_USD

# Costo total sin cobertura
costo_total_sin_cobertura_promedio = pago_inversion_spot_promedio + total_intereses
costo_total_sin_cobertura_mediana = pago_inversion_spot_mediana + total_intereses

print(f"  • Pago inversión (spot futuro esperado - media): ${pago_inversion_spot_promedio:,.0f} COP")
print(f"  • Pago inversión (spot futuro esperado - mediana): ${pago_inversion_spot_mediana:,.0f} COP")
print(f"  • Intereses del crédito: ${total_intereses:,.0f} COP")
print(f"  • COSTO TOTAL ESPERADO (media): ${costo_total_sin_cobertura_promedio:,.0f} COP")
print(f"  • COSTO TOTAL ESPERADO (mediana): ${costo_total_sin_cobertura_mediana:,.0f} COP")
print()

# ESCENARIO 2: CON COBERTURA FORWARD
print(f"\n📊 ESCENARIO 2 - CON COBERTURA FORWARD:")
print("-"*100)

# Pago de la inversión al forward (fijo)
pago_inversion_forward = FORWARD_RATE * MONTO_INVERSION_USD

# Costo total con forward
costo_total_con_forward = pago_inversion_forward + total_intereses

print(f"  • Pago inversión (forward fijo): ${pago_inversion_forward:,.0f} COP")
print(f"  • Intereses del crédito: ${total_intereses:,.0f} COP")
print(f"  • COSTO TOTAL CON FORWARD: ${costo_total_con_forward:,.0f} COP")
print(f"  • Característica: SIN RIESGO CAMBIARIO (tasa fija conocida)")
print()

# COMPARACIÓN
print(f"\n🔍 COMPARACIÓN DE ESCENARIOS:")
print("="*100)

diferencia_vs_media = costo_total_sin_cobertura_promedio - costo_total_con_forward
diferencia_vs_mediana = costo_total_sin_cobertura_mediana - costo_total_con_forward

pct_diferencia_media = (diferencia_vs_media / costo_total_sin_cobertura_promedio) * 100
pct_diferencia_mediana = (diferencia_vs_mediana / costo_total_sin_cobertura_mediana) * 100

print(f"  Comparación vs SIN cobertura (usando MEDIA):")
print(f"    • Diferencia: ${diferencia_vs_media:+,.0f} COP ({pct_diferencia_media:+.2f}%)")
if diferencia_vs_media > 0:
    print(f"    • ✅ El forward es MÁS CONVENIENTE por ${diferencia_vs_media:,.0f} COP")
else:
    print(f"    • ❌ El forward es MENOS conveniente por ${abs(diferencia_vs_media):,.0f} COP")
print()

print(f"  Comparación vs SIN cobertura (usando MEDIANA):")
print(f"    • Diferencia: ${diferencia_vs_mediana:+,.0f} COP ({pct_diferencia_mediana:+.2f}%)")
if diferencia_vs_mediana > 0:
    print(f"    • ✅ El forward es MÁS CONVENIENTE por ${diferencia_vs_mediana:,.0f} COP")
else:
    print(f"    • ❌ El forward es MENOS conveniente por ${abs(diferencia_vs_mediana):,.0f} COP")
print()

# Análisis de sensibilidad del flujo total
print(f"\n📈 ANÁLISIS DE SENSIBILIDAD DEL FLUJO TOTAL:")
print("-"*100)

for p_name, p_value in percentiles.items():
    pago_spot_percentil = p_value * MONTO_INVERSION_USD
    costo_total_percentil = pago_spot_percentil + total_intereses
    diff_vs_forward = costo_total_percentil - costo_total_con_forward
    mejor = "FORWARD" if diff_vs_forward > 0 else "SPOT"
    
    print(f"  • {p_name:15s}: Costo Total=${costo_total_percentil:>15,.0f} → Dif vs Forward=${diff_vs_forward:>+14,.0f} → Mejor: {mejor}")
print()

# ============================================================================
# 8. ANÁLISIS DE RIESGO - VaR, CVaR Y MÉTRICAS
# ============================================================================

print("="*100)
print("SECCIÓN 7: ANÁLISIS DE RIESGO - VaR, CVaR Y MÉTRICAS DE VOLATILIDAD")
print("="*100)

# Value at Risk (VaR)
var_95_sin_cobertura = np.percentile(spot_futuro_simulado * MONTO_INVERSION_USD, 5)
var_99_sin_cobertura = np.percentile(spot_futuro_simulado * MONTO_INVERSION_USD, 1)

var_95_con_forward = FORWARD_RATE * MONTO_INVERSION_USD  # Sin riesgo
var_99_con_forward = FORWARD_RATE * MONTO_INVERSION_USD

print(f"\n📊 VALUE AT RISK (VaR) - NIVEL DE CONFIANZA:")
print(f"  • VaR 95% SIN cobertura: ${var_95_sin_cobertura:,.0f} COP")
print(f"    Interpretación: 95% de probabilidad de que la pérdida no exceda este valor")
print(f"  • VaR 99% SIN cobertura: ${var_99_sin_cobertura:,.0f} COP")
print(f"    Interpretación: 99% de probabilidad de que la pérdida no exceda este valor")
print()
print(f"  • VaR 95% CON forward: ${var_95_con_forward:,.0f} COP (FIJO - sin riesgo)")
print(f"  • VaR 99% CON forward: ${var_99_con_forward:,.0f} COP (FIJO - sin riesgo)")
print()

reduccion_var_95 = var_95_con_forward - var_95_sin_cobertura
reduccion_var_99 = var_99_con_forward - var_99_sin_cobertura

print(f"  🛡️  REDUCCIÓN DE RIESGO CON FORWARD:")
print(f"    • Reducción VaR 95%: ${reduccion_var_95:+,.0f} COP ({(reduccion_var_95/var_95_sin_cobertura)*100:+.2f}%)")
print(f"    • Reducción VaR 99%: ${reduccion_var_99:+,.0f} COP ({(reduccion_var_99/var_99_sin_cobertura)*100:+.2f}%)")
print()

# Conditional Value at Risk (CVaR / Expected Shortfall)
cvar_95_sin_cobertura = spot_futuro_simulado[spot_futuro_simulado <= np.percentile(spot_futuro_simulado, 5)].mean() * MONTO_INVERSION_USD
cvar_95_con_forward = FORWARD_RATE * MONTO_INVERSION_USD

print(f"📊 CONDITIONAL VaR (CVaR / Expected Shortfall):")
print(f"  • CVaR 95% SIN cobertura: ${cvar_95_sin_cobertura:,.0f} COP")
print(f"    Interpretación: Pérdida esperada en el 5% de los peores casos")
print(f"  • CVaR 95% CON forward: ${cvar_95_con_forward:,.0f} COP")
print()

# Volatilidad
volatilidad_sin_cobertura = spot_futuro_simulado.std() * MONTO_INVERSION_USD
volatilidad_con_forward = 0  # Sin volatilidad con forward

print(f"📊 VOLATILIDAD DEL PAGO:")
print(f"  • Volatilidad SIN cobertura: ${volatilidad_sin_cobertura:,.0f} COP")
print(f"  • Volatilidad CON forward: ${volatilidad_con_forward:,.0f} COP (ELIMINADA)")
print(f"  • Reducción de volatilidad: 100%")
print()

# ============================================================================
# 9. ANÁLISIS COSTO-BENEFICIO Y CONVENIENCIA
# ============================================================================

print("="*100)
print("SECCIÓN 8: ANÁLISIS COSTO-BENEFICIO - ¿FUE CONVENIENTE LA INVERSIÓN?")
print("="*100)

print(f"\n💰 ANÁLISIS DE COSTO-BENEFICIO DE LA COBERTURA:")
print("-"*100)

# Costo de oportunidad del forward
costo_oportunidad_promedio = perdida_por_escenario.mean() * (n_no_protegidos / n_simulaciones)
beneficio_promedio = ahorro_por_escenario.mean() * (n_protegidos / n_simulaciones)
beneficio_neto_esperado = beneficio_promedio - costo_oportunidad_promedio

print(f"  • Beneficio esperado cuando protege: ${beneficio_promedio:,.0f} COP")
print(f"  • Costo de oportunidad cuando NO protege: ${costo_oportunidad_promedio:,.0f} COP")
print(f"  • BENEFICIO NETO ESPERADO: ${beneficio_neto_esperado:,.0f} COP")
print()

# Relación beneficio-costo
if costo_oportunidad_promedio > 0:
    relacion_beneficio_costo = beneficio_promedio / costo_oportunidad_promedio
else:
    relacion_beneficio_costo = float('inf')

print(f"  • Relación Beneficio/Costo: {relacion_beneficio_costo:.2f}")
if relacion_beneficio_costo > 1:
    print(f"    ✅ Por cada $1 de costo de oportunidad, se generan ${relacion_beneficio_costo:.2f} de beneficio")
else:
    print(f"    ⚠️  Por cada $1 de costo de oportunidad, se generan ${relacion_beneficio_costo:.2f} de beneficio")
print()

# Análisis de la inversión
print(f"\n📊 EVALUACIÓN DE LA INVERSIÓN CON FORWARD:")
print("-"*100)

# Supongamos que la inversión genera un retorno
tasa_retorno_inversion_anual = 0.15  # 15% anual esperado
retorno_6_meses = MONTO_INVERSION_USD * spot_actual * (tasa_retorno_inversion_anual * 6/12)

print(f"  • Inversión inicial (al spot): ${valor_cop_spot_actual:,.0f} COP")
print(f"  • Retorno esperado de la inversión (6 meses): ${retorno_6_meses:,.0f} COP")
print(f"  • Tasa de retorno de la inversión: {tasa_retorno_inversion_anual*100:.1f}% anual")
print()

# Flujo neto con y sin cobertura
flujo_neto_sin_cobertura = retorno_6_meses - total_intereses - (pago_inversion_spot_promedio - valor_cop_spot_actual)
flujo_neto_con_forward = retorno_6_meses - total_intereses - (pago_inversion_forward - valor_cop_spot_actual)

print(f"  • Flujo neto SIN cobertura: ${flujo_neto_sin_cobertura:,.0f} COP")
print(f"  • Flujo neto CON forward: ${flujo_neto_con_forward:,.0f} COP")
print()

if flujo_neto_con_forward > flujo_neto_sin_cobertura:
    print(f"  ✅ La inversión CON FORWARD es más rentable por ${flujo_neto_con_forward - flujo_neto_sin_cobertura:,.0f} COP")
else:
    print(f"  ⚠️  La inversión SIN cobertura es más rentable por ${flujo_neto_sin_cobertura - flujo_neto_con_forward:,.0f} COP")
print()

# Justificación final
print(f"\n🎯 JUSTIFICACIÓN DE LA CONVENIENCIA DE LA INVERSIÓN:")
print("="*100)

criterios = {
    'Protección > 50%': pct_protegidos > 50,
    'Beneficio neto positivo': beneficio_neto_esperado > 0,
    'Reducción de riesgo significativa': abs(reduccion_var_95) > valor_cop_spot_actual * 0.05,
    'Forward más conveniente': diferencia_vs_mediana > 0,
    'Relación B/C > 1': relacion_beneficio_costo > 1
}

print(f"\n📋 CRITERIOS DE EVALUACIÓN:")
for criterio, cumple in criterios.items():
    estado = "✅ CUMPLE" if cumple else "❌ NO CUMPLE"
    print(f"  • {criterio:40s}: {estado}")

criterios_cumplidos = sum(criterios.values())
print(f"\n📊 RESUMEN: {criterios_cumplidos} de {len(criterios)} criterios cumplidos")
print()

# Decisión final
print(f"\n💡 CONCLUSIÓN Y RECOMENDACIÓN FINAL:")
print("-"*100)

if criterios_cumplidos >= 4:
    print(f"  ✅✅✅ RECOMENDACIÓN: CONTRATAR EL FORWARD")
    print(f"  ")
    print(f"  Justificación:")
    print(f"  • La cobertura protege en {pct_protegidos:.2f}% de los escenarios")
    print(f"  • Genera un beneficio neto esperado de ${beneficio_neto_esperado:,.0f} COP")
    print(f"  • Reduce el riesgo (VaR 95%) en ${abs(reduccion_var_95):,.0f} COP")
    print(f"  • Elimina la incertidumbre cambiaria, facilitando la planificación financiera")
    print(f"  • Es financieramente conveniente en la mayoría de escenarios")
    
elif criterios_cumplidos >= 3:
    print(f"  ⚠️  RECOMENDACIÓN: EVALUAR RIESGO VS COSTO")
    print(f"  ")
    print(f"  Justificación:")
    print(f"  • La cobertura tiene beneficios pero también costos de oportunidad")
    print(f"  • Protege en {pct_protegidos:.2f}% de los escenarios")
    print(f"  • La decisión depende de la aversión al riesgo de la empresa")
    print(f"  • Si la prioridad es la certeza, conviene el forward")
    print(f"  • Si la prioridad es maximizar retorno, evaluar alternativas")
    
else:
    print(f"  ❌ RECOMENDACIÓN: NO CONTRATAR FORWARD (o negociar mejor tasa)")
    print(f"  ")
    print(f"  Justificación:")
    print(f"  • El forward es más costoso en la mayoría de escenarios")
    print(f"  • Solo protege en {pct_protegidos:.2f}% de los casos")
    print(f"  • El beneficio neto esperado es negativo: ${beneficio_neto_esperado:,.0f} COP")
    print(f"  • Solo conviene si hay extrema aversión al riesgo")
    print(f"  • Considerar negociar una tasa forward más competitiva")

print()

# ============================================================================
# 10. GENERACIÓN DE ARCHIVO TXT COMPLETO
# ============================================================================

print("="*100)
print("SECCIÓN 9: GENERACIÓN DE ARCHIVO TXT CON ANÁLISIS COMPLETO")
print("="*100)

archivo_txt = os.path.join(ruta_base, "ANALISIS_FORWARD_COMPLETO.txt")

with open(archivo_txt, 'w', encoding='utf-8') as f:
    # Encabezado
    f.write("="*100 + "\n")
    f.write(" "*20 + "LABORATORIO DE DERIVADOS FINANCIEROS\n")
    f.write(" "*25 + "ANÁLISIS DE FORWARD - COBERTURA CAMBIARIA\n")
    f.write(" "*20 + "INVERSIÓN CON FORWARD SET-FX\n")
    f.write("="*100 + "\n\n")
    
    f.write("INTEGRANTES:\n")
    f.write("1. Santiago Toro Cadavid - Cédula: 1040739414\n")
    f.write("2. Yenny Carolina Serna Chaverra - Cédula: 1017210528\n")
    f.write("3. Daniela Perez Meza - Cédula: 1017220748\n\n")
    
    f.write(f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"Curso: Derivados Financieros\n\n")
    
    # Sección 1: Forward SET-FX
    f.write("="*100 + "\n")
    f.write("SECCIÓN 1: INFORMACIÓN FORWARD SET-FX - PLAZO SUPERIOR A 6 MESES\n")
    f.write("="*100 + "\n\n")
    
    f.write("DOCUMENTACIÓN DE LA ELECCIÓN DEL FORWARD:\n")
    f.write("-"*100 + "\n")
    f.write(f"Mercado: {forward_set_fx['mercado']}\n")
    f.write(f"Par cambiario: {forward_set_fx['moneda']}\n")
    f.write(f"Plazo seleccionado: {forward_set_fx['plazo']}\n")
    f.write(f"Fecha de reporte SET-FX: {forward_set_fx['fecha_reporte']}\n\n")
    
    f.write("TASAS FORWARD DISPONIBLES:\n")
    f.write(f"  • Apertura:           ${forward_set_fx['apertura']:>12,.2f} COP/USD\n")
    f.write(f"  • Cierre (SELECCIONADA): ${forward_set_fx['cierre']:>12,.2f} COP/USD ←\n")
    f.write(f"  • Promedio:           ${forward_set_fx['promedio']:>12,.2f} COP/USD\n")
    f.write(f"  • Mínimo:             ${forward_set_fx['precio_min']:>12,.2f} COP/USD\n")
    f.write(f"  • Máximo:             ${forward_set_fx['precio_max']:>12,.2f} COP/USD\n\n")
    
    f.write("ESTADÍSTICAS DE TRANSACCIONES:\n")
    f.write(f"  • Número total de transacciones: {forward_set_fx['no_transacciones']}\n")
    f.write(f"  • Monto acumulado negociado: ${forward_set_fx['monto_acumulado']:,.2f} USD\n")
    f.write(f"  • Monto promedio por transacción: ${forward_set_fx['monto_promedio']:,.2f} USD\n\n")
    
    f.write("JUSTIFICACIÓN DE LA ELECCIÓN:\n")
    f.write(f"  Se selecciona la tasa de CIERRE (${FORWARD_RATE:,.2f}) por ser:\n")
    f.write(f"  - El precio de mercado al cierre de la jornada\n")
    f.write(f"  - Representativo de las condiciones actuales del mercado\n")
    f.write(f"  - Utilizado como referencia para valoración de contratos\n")
    f.write(f"  - Consistente con prácticas de valoración financiera\n\n")
    
    # Sección 2: Datos Spot
    f.write("="*100 + "\n")
    f.write("SECCIÓN 2: DATOS SPOT USDCOP=X - ANÁLISIS HISTÓRICO\n")
    f.write("="*100 + "\n\n")
    
    f.write(f"Período analizado: {spot_data['Fecha'].min().strftime('%Y-%m-%d')} a {spot_data['Fecha'].max().strftime('%Y-%m-%d')}\n")
    f.write(f"Total de observaciones: {len(spot_data):,} días hábiles\n\n")
    
    f.write("ESTADÍSTICAS DESCRIPTIVAS DEL SPOT:\n")
    f.write(f"  • Spot actual (último): ${spot_actual:,.2f} COP/USD\n")
    f.write(f"  • Spot mínimo (período): ${spot_min:,.2f}\n")
    f.write(f"  • Spot máximo (período): ${spot_max:,.2f}\n")
    f.write(f"  • Spot promedio: ${spot_prom:,.2f}\n")
    f.write(f"  • Desviación estándar: ${spot_std:,.2f}\n")
    f.write(f"  • Volatilidad histórica: {(spot_std/spot_prom)*100:.2f}%\n\n")
    
    # Sección 3: Parámetros de inversión
    f.write("="*100 + "\n")
    f.write("SECCIÓN 3: PARÁMETROS DE LA INVERSIÓN CON FORWARD\n")
    f.write("="*100 + "\n\n")
    
    f.write("CARACTERÍSTICAS DE LA INVERSIÓN:\n")
    f.write(f"  • Monto total de inversión: ${MONTO_INVERSION_USD:,.0f} USD\n")
    f.write(f"  • Plazo de la cobertura forward: {PLAZO_FORWARD_MESES} meses\n")
    f.write(f"  • Fecha de vencimiento: {(datetime.now() + relativedelta(months=PLAZO_FORWARD_MESES)).strftime('%Y-%m-%d')}\n\n")
    
    f.write("CONDICIONES DEL CRÉDITO:\n")
    f.write(f"  • Tasa de interés: {TASA_CREDITO_EA*100:.2f}% E.A.\n")
    f.write(f"  • Tasa LIBOR de referencia: {TASA_LIBOR_ANUAL*100:.2f}%\n")
    f.write(f"  • Spread aplicado: {SPREAD_CREDITO*100:.2f}%\n")
    f.write(f"  • Porcentaje financiado: {MONTO_CREDITO_PCT*100:.0f}%\n")
    f.write(f"  • Plazo del crédito: {PLAZO_CREDITO_MESES} meses\n\n")
    
    f.write("ESTRUCTURA DE FINANCIAMIENTO:\n")
    f.write(f"  • Monto financiado: ${monto_financiado_usd:,.0f} USD ({MONTO_CREDITO_PCT*100:.0f}%)\n")
    f.write(f"  • Pago inicial: ${pago_inicial_usd:,.0f} USD ({(1-MONTO_CREDITO_PCT)*100:.0f}%)\n")
    f.write(f"  • Valor al spot actual (${spot_actual:,.2f}): ${valor_cop_spot_actual:,.0f} COP\n")
    f.write(f"  • Valor con forward (${FORWARD_RATE:,.2f}): ${valor_cop_forward:,.0f} COP\n")
    f.write(f"  • Diferencia: ${valor_cop_forward - valor_cop_spot_actual:,.0f} COP ({((FORWARD_RATE/spot_actual)-1)*100:+.2f}%)\n")
    f.write(f"  • Intereses crédito ({PLAZO_CREDITO_MESES} meses): ${intereses_6_meses:,.0f} COP\n\n")
    
    # Sección 4: Simulación Monte Carlo
    f.write("="*100 + "\n")
    f.write("SECCIÓN 4: SIMULACIÓN MONTE CARLO - PROYECCIÓN SPOT FUTURO\n")
    f.write("="*100 + "\n\n")
    
    f.write("PARÁMETROS ESTADÍSTICOS PARA SIMULACIÓN:\n")
    f.write(f"  • Retorno diario promedio: {mu_diario:.8f} ({mu_diario*100:.6f}%)\n")
    f.write(f"  • Volatilidad diaria: {sigma_diario:.8f} ({sigma_diario*100:.6f}%)\n")
    f.write(f"  • Retorno anualizado: {mu_anual:.6f} ({mu_anual*100:.4f}%)\n")
    f.write(f"  • Volatilidad anualizada: {sigma_anual:.6f} ({sigma_anual*100:.4f}%)\n\n")
    
    f.write("CONFIGURACIÓN DE LA SIMULACIÓN:\n")
    f.write(f"  • Número de simulaciones: {n_simulaciones:,}\n")
    f.write(f"  • Días de proyección: {dias_proyeccion}\n")
    f.write(f"  • Horizonte temporal: {PLAZO_FORWARD_MESES} meses ({T:.4f} años)\n")
    f.write(f"  • Tasa forward de referencia: ${FORWARD_RATE:,.2f}\n\n")
    
    f.write("RESULTADOS DE LA SIMULACIÓN:\n")
    f.write(f"  • Spot inicial: ${spot_actual:,.2f}\n")
    f.write(f"  • Spot simulado (media): ${spot_futuro_simulado.mean():,.2f}\n")
    f.write(f"  • Spot simulado (mediana): ${np.median(spot_futuro_simulado):,.2f}\n")
    f.write(f"  • Spot simulado (desviación): ${spot_futuro_simulado.std():,.2f}\n")
    f.write(f"  • Spot simulado (mínimo): ${spot_futuro_simulado.min():,.2f}\n")
    f.write(f"  • Spot simulado (máximo): ${spot_futuro_simulado.max():,.2f}\n")
    f.write(f"  • Forward contratado: ${FORWARD_RATE:,.2f}\n")
    f.write(f"  • Diferencia media vs forward: ${spot_futuro_simulado.mean() - FORWARD_RATE:+,.2f}\n\n")
    
    f.write("PERCENTILES DE LA DISTRIBUCIÓN:\n")
    for p, v in percentiles.items():
        diff_vs_forward = v - FORWARD_RATE
        f.write(f"  • {p:15s}: ${v:>12,.2f}  (vs Forward: {diff_vs_forward:+,.2f})\n")
    f.write("\n")
    
    # Sección 5: Análisis de protección
    f.write("="*100 + "\n")
    f.write("SECCIÓN 5: ANÁLISIS DE PROTECCIÓN - EVALUACIÓN SISTEMÁTICA DE ESCENARIOS\n")
    f.write("="*100 + "\n\n")
    
    f.write("CLASIFICACIÓN DE ESCENARIOS DE PROTECCIÓN:\n\n")
    f.write("ESCENARIOS PROTEGIDOS (Spot Futuro > Forward):\n")
    f.write(f"  • Cantidad: {n_protegidos:,} escenarios\n")
    f.write(f"  • Porcentaje: {pct_protegidos:.2f}%\n")
    f.write(f"  • Interpretación: El forward ES BENEFICIOSO - se paga menos que el spot de mercado\n\n")
    
    f.write("ESCENARIOS NO PROTEGIDOS (Spot Futuro ≤ Forward):\n")
    f.write(f"  • Cantidad: {n_no_protegidos:,} escenarios\n")
    f.write(f"  • Porcentaje: {pct_no_protegidos:.2f}%\n")
    f.write(f"  • Interpretación: El forward NO ES BENEFICIOSO - se paga más o igual que el spot\n\n")
    
    f.write("ANÁLISIS DE GANANCIAS Y PÉRDIDAS POR ESCENARIO:\n\n")
    f.write("ESCENARIOS PROTEGIDOS - AHORROS:\n")
    f.write(f"  • Ahorro mínimo: ${ahorro_por_escenario.min():,.0f} COP\n")
    f.write(f"  • Ahorro máximo: ${ahorro_por_escenario.max():,.0f} COP\n")
    f.write(f"  • Ahorro promedio: ${ahorro_por_escenario.mean():,.0f} COP\n")
    f.write(f"  • Ahorro mediano: ${np.median(ahorro_por_escenario):,.0f} COP\n")
    f.write(f"  • Desviación del ahorro: ${ahorro_por_escenario.std():,.0f} COP\n")
    f.write(f"  • Ahorro total esperado: ${ahorro_por_escenario.sum():,.0f} COP\n\n")
    
    f.write("ESCENARIOS NO PROTEGIDOS - PÉRDIDAS (COSTO DE OPORTUNIDAD):\n")
    f.write(f"  • Pérdida mínima: ${perdida_por_escenario.min():,.0f} COP\n")
    f.write(f"  • Pérdida máxima: ${perdida_por_escenario.max():,.0f} COP\n")
    f.write(f"  • Pérdida promedio: ${perdida_por_escenario.mean():,.0f} COP\n")
    f.write(f"  • Pérdida mediana: ${np.median(perdida_por_escenario):,.0f} COP\n")
    f.write(f"  • Desviación de la pérdida: ${perdida_por_escenario.std():,.0f} COP\n\n")
    
    f.write("VALOR ESPERADO DE LA COBERTURA FORWARD:\n")
    f.write(f"  • Valor esperado: ${valor_esperado_cobertura.mean():,.0f} COP\n")
    f.write(f"  • Desviación estándar: ${valor_esperado_cobertura.std():,.0f} COP\n")
    f.write(f"  • Coeficiente de variación: {valor_esperado_cobertura.std()/abs(valor_esperado_cobertura.mean()):.2f}\n\n")
    
    f.write("UMBRALES DE PROTECCIÓN BAJO VOLATILIDAD CAMBIARIA:\n")
    for nombre, umbral in umbrales.items():
        prob = (spot_futuro_simulado > umbral).sum() / n_simulaciones * 100
        diff = ((umbral / FORWARD_RATE) - 1) * 100
        f.write(f"  • {nombre:30s}: ${umbral:>10,.2f} ({diff:+.2f}%) → Probabilidad: {prob:.2f}%\n")
    f.write("\n")
    
    # Sección 6: Flujo total
    f.write("="*100 + "\n")
    f.write("SECCIÓN 6: ANÁLISIS DE FLUJO TOTAL - CRÉDITO VS FORWARD\n")
    f.write("="*100 + "\n\n")
    
    f.write("CÁLCULO DEL FLUJO DE CAJA COMPLETO:\n\n")
    f.write("ESTRUCTURA DEL CRÉDITO:\n")
    f.write(f"  • Monto financiado en USD: ${monto_financiado_usd:,.0f}\n")
    f.write(f"  • Tasa de cambio spot: ${spot_actual:,.2f}\n")
    f.write(f"  • Monto del crédito en COP: ${monto_credito_cop:,.0f}\n")
    f.write(f"  • Tasa mensual: {tasa_mensual*100:.4f}%\n")
    f.write(f"  • Plazo: {PLAZO_CREDITO_MESES} meses\n")
    f.write(f"  • Cuota mensual: ${cuota_mensual:,.0f} COP\n")
    f.write(f"  • Total intereses: ${total_intereses:,.0f} COP\n")
    f.write(f"  • Total a pagar (crédito): ${total_pagar_credito:,.0f} COP\n\n")
    
    f.write("ESCENARIO 1 - SIN COBERTURA FORWARD:\n")
    f.write("-"*100 + "\n")
    f.write(f"  • Pago inversión (spot futuro esperado - media): ${pago_inversion_spot_promedio:,.0f} COP\n")
    f.write(f"  • Pago inversión (spot futuro esperado - mediana): ${pago_inversion_spot_mediana:,.0f} COP\n")
    f.write(f"  • Intereses del crédito: ${total_intereses:,.0f} COP\n")
    f.write(f"  • COSTO TOTAL ESPERADO (media): ${costo_total_sin_cobertura_promedio:,.0f} COP\n")
    f.write(f"  • COSTO TOTAL ESPERADO (mediana): ${costo_total_sin_cobertura_mediana:,.0f} COP\n\n")
    
    f.write("ESCENARIO 2 - CON COBERTURA FORWARD:\n")
    f.write("-"*100 + "\n")
    f.write(f"  • Pago inversión (forward fijo): ${pago_inversion_forward:,.0f} COP\n")
    f.write(f"  • Intereses del crédito: ${total_intereses:,.0f} COP\n")
    f.write(f"  • COSTO TOTAL CON FORWARD: ${costo_total_con_forward:,.0f} COP\n")
    f.write(f"  • Característica: SIN RIESGO CAMBIARIO (tasa fija conocida)\n\n")
    
    f.write("COMPARACIÓN DE ESCENARIOS:\n")
    f.write("="*100 + "\n")
    f.write(f"  Comparación vs SIN cobertura (usando MEDIA):\n")
    f.write(f"    • Diferencia: ${diferencia_vs_media:+,.0f} COP ({pct_diferencia_media:+.2f}%)\n")
    if diferencia_vs_media > 0:
        f.write(f"    • ✅ El forward es MÁS CONVENIENTE por ${diferencia_vs_media:,.0f} COP\n")
    else:
        f.write(f"    • ❌ El forward es MENOS conveniente por ${abs(diferencia_vs_media):,.0f} COP\n")
    f.write("\n")
    
    f.write(f"  Comparación vs SIN cobertura (usando MEDIANA):\n")
    f.write(f"    • Diferencia: ${diferencia_vs_mediana:+,.0f} COP ({pct_diferencia_mediana:+.2f}%)\n")
    if diferencia_vs_mediana > 0:
        f.write(f"    • ✅ El forward es MÁS CONVENIENTE por ${diferencia_vs_mediana:,.0f} COP\n")
    else:
        f.write(f"    • ❌ El forward es MENOS conveniente por ${abs(diferencia_vs_mediana):,.0f} COP\n")
    f.write("\n")
    
    f.write("ANÁLISIS DE SENSIBILIDAD DEL FLUJO TOTAL:\n")
    f.write("-"*100 + "\n")
    for p_name, p_value in percentiles.items():
        pago_spot_percentil = p_value * MONTO_INVERSION_USD
        costo_total_percentil = pago_spot_percentil + total_intereses
        diff_vs_forward = costo_total_percentil - costo_total_con_forward
        mejor = "FORWARD" if diff_vs_forward > 0 else "SPOT"
        f.write(f"  • {p_name:15s}: Costo Total=${costo_total_percentil:>15,.0f} → Dif vs Forward=${diff_vs_forward:>+14,.0f} → Mejor: {mejor}\n")
    f.write("\n")
    
    # Sección 7: Análisis de riesgo
    f.write("="*100 + "\n")
    f.write("SECCIÓN 7: ANÁLISIS DE RIESGO - VaR, CVaR Y MÉTRICAS\n")
    f.write("="*100 + "\n\n")
    
    f.write("VALUE AT RISK (VaR) - NIVEL DE CONFIANZA:\n")
    f.write(f"  • VaR 95% SIN cobertura: ${var_95_sin_cobertura:,.0f} COP\n")
    f.write(f"    Interpretación: 95% de probabilidad de que la pérdida no exceda este valor\n")
    f.write(f"  • VaR 99% SIN cobertura: ${var_99_sin_cobertura:,.0f} COP\n")
    f.write(f"    Interpretación: 99% de probabilidad de que la pérdida no exceda este valor\n\n")
    f.write(f"  • VaR 95% CON forward: ${var_95_con_forward:,.0f} COP (FIJO - sin riesgo)\n")
    f.write(f"  • VaR 99% CON forward: ${var_99_con_forward:,.0f} COP (FIJO - sin riesgo)\n\n")
    
    f.write("REDUCCIÓN DE RIESGO CON FORWARD:\n")
    f.write(f"    • Reducción VaR 95%: ${reduccion_var_95:+,.0f} COP ({(reduccion_var_95/var_95_sin_cobertura)*100:+.2f}%)\n")
    f.write(f"    • Reducción VaR 99%: ${reduccion_var_99:+,.0f} COP ({(reduccion_var_99/var_99_sin_cobertura)*100:+.2f}%)\n\n")
    
    f.write("CONDITIONAL VaR (CVaR / Expected Shortfall):\n")
    f.write(f"  • CVaR 95% SIN cobertura: ${cvar_95_sin_cobertura:,.0f} COP\n")
    f.write(f"    Interpretación: Pérdida esperada en el 5% de los peores casos\n")
    f.write(f"  • CVaR 95% CON forward: ${cvar_95_con_forward:,.0f} COP\n\n")
    
    f.write("VOLATILIDAD DEL PAGO:\n")
    f.write(f"  • Volatilidad SIN cobertura: ${volatilidad_sin_cobertura:,.0f} COP\n")
    f.write(f"  • Volatilidad CON forward: ${volatilidad_con_forward:,.0f} COP (ELIMINADA)\n")
    f.write(f"  • Reducción de volatilidad: 100%\n\n")
    
    # Sección 8: Costo-beneficio
    f.write("="*100 + "\n")
    f.write("SECCIÓN 8: ANÁLISIS COSTO-BENEFICIO - CONVENIENCIA DE LA INVERSIÓN\n")
    f.write("="*100 + "\n\n")
    
    f.write("ANÁLISIS DE COSTO-BENEFICIO DE LA COBERTURA:\n")
    f.write("-"*100 + "\n")
    f.write(f"  • Beneficio esperado cuando protege: ${beneficio_promedio:,.0f} COP\n")
    f.write(f"  • Costo de oportunidad cuando NO protege: ${costo_oportunidad_promedio:,.0f} COP\n")
    f.write(f"  • BENEFICIO NETO ESPERADO: ${beneficio_neto_esperado:,.0f} COP\n\n")
    
    f.write(f"  • Relación Beneficio/Costo: {relacion_beneficio_costo:.2f}\n")
    if relacion_beneficio_costo > 1:
        f.write(f"    ✅ Por cada $1 de costo de oportunidad, se generan ${relacion_beneficio_costo:.2f} de beneficio\n")
    else:
        f.write(f"    ⚠️  Por cada $1 de costo de oportunidad, se generan ${relacion_beneficio_costo:.2f} de beneficio\n")
    f.write("\n")
    
    f.write("EVALUACIÓN DE LA INVERSIÓN CON FORWARD:\n")
    f.write("-"*100 + "\n")
    f.write(f"  • Inversión inicial (al spot): ${valor_cop_spot_actual:,.0f} COP\n")
    f.write(f"  • Retorno esperado de la inversión (6 meses): ${retorno_6_meses:,.0f} COP\n")
    f.write(f"  • Tasa de retorno de la inversión: {tasa_retorno_inversion_anual*100:.1f}% anual\n\n")
    
    f.write(f"  • Flujo neto SIN cobertura: ${flujo_neto_sin_cobertura:,.0f} COP\n")
    f.write(f"  • Flujo neto CON forward: ${flujo_neto_con_forward:,.0f} COP\n\n")
    
    if flujo_neto_con_forward > flujo_neto_sin_cobertura:
        f.write(f"  ✅ La inversión CON FORWARD es más rentable por ${flujo_neto_con_forward - flujo_neto_sin_cobertura:,.0f} COP\n")
    else:
        f.write(f"  ⚠️  La inversión SIN cobertura es más rentable por ${flujo_neto_sin_cobertura - flujo_neto_con_forward:,.0f} COP\n")
    f.write("\n")
    
    f.write("JUSTIFICACIÓN DE LA CONVENIENCIA DE LA INVERSIÓN:\n")
    f.write("="*100 + "\n\n")
    
    f.write("CRITERIOS DE EVALUACIÓN:\n")
    for criterio, cumple in criterios.items():
        estado = "✅ CUMPLE" if cumple else "❌ NO CUMPLE"
        f.write(f"  • {criterio:40s}: {estado}\n")
    
    f.write(f"\n📊 RESUMEN: {criterios_cumplidos} de {len(criterios)} criterios cumplidos\n\n")
    
    f.write("CONCLUSIÓN Y RECOMENDACIÓN FINAL:\n")
    f.write("-"*100 + "\n")
    
    if criterios_cumplidos >= 4:
        f.write("  ✅✅✅ RECOMENDACIÓN: CONTRATAR EL FORWARD\n\n")
        f.write("  Justificación:\n")
        f.write(f"  • La cobertura protege en {pct_protegidos:.2f}% de los escenarios\n")
        f.write(f"  • Genera un beneficio neto esperado de ${beneficio_neto_esperado:,.0f} COP\n")
        f.write(f"  • Reduce el riesgo (VaR 95%) en ${abs(reduccion_var_95):,.0f} COP\n")
        f.write(f"  • Elimina la incertidumbre cambiaria, facilitando la planificación financiera\n")
        f.write(f"  • Es financieramente conveniente en la mayoría de escenarios\n")
        
    elif criterios_cumplidos >= 3:
        f.write("  ⚠️  RECOMENDACIÓN: EVALUAR RIESGO VS COSTO\n\n")
        f.write("  Justificación:\n")
        f.write(f"  • La cobertura tiene beneficios pero también costos de oportunidad\n")
        f.write(f"  • Protege en {pct_protegidos:.2f}% de los escenarios\n")
        f.write(f"  • La decisión depende de la aversión al riesgo de la empresa\n")
        f.write(f"  • Si la prioridad es la certeza, conviene el forward\n")
        f.write(f"  • Si la prioridad es maximizar retorno, evaluar alternativas\n")
        
    else:
        f.write("  ❌ RECOMENDACIÓN: NO CONTRATAR FORWARD (o negociar mejor tasa)\n\n")
        f.write("  Justificación:\n")
        f.write(f"  • El forward es más costoso en la mayoría de escenarios\n")
        f.write(f"  • Solo protege en {pct_protegidos:.2f}% de los casos\n")
        f.write(f"  • El beneficio neto esperado es negativo: ${beneficio_neto_esperado:,.0f} COP\n")
        f.write(f"  • Solo conviene si hay extrema aversión al riesgo\n")
        f.write(f"  • Considerar negociar una tasa forward más competitiva\n")
    
    f.write("\n")
    f.write("="*100 + "\n")
    f.write("FIN DEL ANÁLISIS\n")
    f.write("="*100 + "\n")

print(f"\n✅ Archivo TXT generado: ANALISIS_FORWARD_COMPLETO.txt")
print(f"   Ubicación: {archivo_txt}")
print(f"   Tamaño: {os.path.getsize(archivo_txt):,} bytes")
print()

# ============================================================================
# 11. GENERACIÓN DE GRÁFICAS PROFESIONALES
# ============================================================================

print("="*100)
print("SECCIÓN 10: GENERACIÓN DE GRÁFICAS PROFESIONALES CON ANÁLISIS")
print("="*100)

# Configurar estilo
plt.rcParams['figure.figsize'] = [16, 9]
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12

print("\n📊 Generando gráficas...")

# Gráfica 1: Distribución del spot futuro vs forward
print("  • Gráfica 1: Distribución spot futuro vs forward...")
fig, ax = plt.subplots(figsize=(14, 7))

n, bins, patches = ax.hist(spot_futuro_simulado, bins=150, density=True, 
                           alpha=0.7, color='steelblue', edgecolor='black', linewidth=0.5)

# Agregar curva de densidad normal
mu, sigma = norm.fit(spot_futuro_simulado)
x = np.linspace(spot_futuro_simulado.min(), spot_futuro_simulado.max(), 1000)
p = norm.pdf(x, mu, sigma)
ax.plot(x, p, 'r-', linewidth=2.5, label=f'Distribución Normal\n(μ=${mu:,.2f}, σ=${sigma:,.2f})')

# Líneas de referencia
ax.axvline(FORWARD_RATE, color='red', linestyle='--', linewidth=2.5, 
           label=f'Forward SET-FX (${FORWARD_RATE:,.2f})')
ax.axvline(spot_actual, color='green', linestyle='--', linewidth=2.5, 
           label=f'Spot Actual (${spot_actual:,.2f})')
ax.axvline(spot_futuro_simulado.mean(), color='orange', linestyle='-', linewidth=2, 
           label=f'Media Simulación (${spot_futuro_simulado.mean():,.2f})')

ax.set_title(f'DISTRIBUCIÓN DEL SPOT FUTURO vs FORWARD - PROYECCIÓN A {PLAZO_FORWARD_MESES} MESES\n'
             f'Inversión: ${MONTO_INVERSION_USD:,.0f} USD | {n_simulaciones:,} Simulaciones', 
             fontsize=14, fontweight='bold', pad=20)
ax.set_xlabel('Tasa de Cambio (COP/USD)', fontsize=12)
ax.set_ylabel('Densidad de Probabilidad', fontsize=12)
ax.legend(loc='upper left', fontsize=10)
ax.grid(True, alpha=0.3)

# Agregar texto con estadísticas
texto_stats = (f"Estadísticas:\n"
               f"• Media: ${spot_futuro_simulado.mean():,.2f}\n"
               f"• Mediana: ${np.median(spot_futuro_simulado):,.2f}\n"
               f"• Std: ${spot_futuro_simulado.std():,.2f}\n"
               f"• Escenarios protegidos: {pct_protegidos:.2f}%")
ax.text(0.98, 0.98, texto_stats, transform=ax.transAxes, fontsize=9,
        verticalalignment='top', horizontalalignment='right',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig(os.path.join(ruta_base, "01_distribucion_spot_forward.png"), dpi=300, bbox_inches='tight')
plt.close()

# Gráfica 2: Escenarios protegidos vs no protegidos
print("  • Gráfica 2: Escenarios protegidos vs no protegidos...")
fig, axes = plt.subplots(1, 2, figsize=(18, 7))

# Panel izquierdo - Escenarios protegidos
axes[0].hist(spot_futuro_simulado[escenarios_protegidos], bins=80, 
             alpha=0.8, color='green', label=f'Protegidos\n({n_protegidos:,} - {pct_protegidos:.2f}%)', 
             edgecolor='darkgreen', linewidth=0.5)
axes[0].axvline(FORWARD_RATE, color='red', linestyle='--', linewidth=2.5, label='Forward')
axes[0].axvline(spot_futuro_simulado[escenarios_protegidos].mean(), color='blue', 
                linestyle='-', linewidth=2, label=f'Media: ${spot_futuro_simulado[escenarios_protegidos].mean():,.2f}')
axes[0].set_title(f'ESCENARIOS PROTEGIDOS\n(El forward ES beneficioso)', 
                  fontsize=12, fontweight='bold', color='green')
axes[0].set_xlabel('Spot Futuro (COP/USD)', fontsize=11)
axes[0].set_ylabel('Frecuencia', fontsize=11)
axes[0].legend(fontsize=10)
axes[0].grid(True, alpha=0.3)

# Panel derecho - Escenarios no protegidos
axes[1].hist(spot_futuro_simulado[escenarios_no_protegidos], bins=80, 
             alpha=0.8, color='orange', label=f'No Protegidos\n({n_no_protegidos:,} - {pct_no_protegidos:.2f}%)', 
             edgecolor='darkorange', linewidth=0.5)
axes[1].axvline(FORWARD_RATE, color='red', linestyle='--', linewidth=2.5, label='Forward')
axes[1].axvline(spot_futuro_simulado[escenarios_no_protegidos].mean(), color='blue', 
                linestyle='-', linewidth=2, label=f'Media: ${spot_futuro_simulado[escenarios_no_protegidos].mean():,.2f}')
axes[1].set_title(f'ESCENARIOS NO PROTEGIDOS\n(El forward NO es beneficioso)', 
                  fontsize=12, fontweight='bold', color='darkorange')
axes[1].set_xlabel('Spot Futuro (COP/USD)', fontsize=11)
axes[1].set_ylabel('Frecuencia', fontsize=11)
axes[1].legend(fontsize=10)
axes[1].grid(True, alpha=0.3)

plt.suptitle(f'ANÁLISIS DE PROTECCIÓN CON FORWARD - INVERSIÓN ${MONTO_INVERSION_USD:,.0f} USD', 
             fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(ruta_base, "02_escenarios_proteccion.png"), dpi=300, bbox_inches='tight')
plt.close()

# Gráfica 3: Comparación de flujo total
print("  • Gráfica 3: Comparación de flujo total...")
fig, ax = plt.subplots(figsize=(12, 7))

categorias = ['Sin Cobertura\n(Media)', 'Sin Cobertura\n(Mediana)', 'Con Forward\n(Fijo)']
valores = [costo_total_sin_cobertura_promedio/1e6, costo_total_sin_cobertura_mediana/1e6, costo_total_con_forward/1e6]
colores = ['orange', 'coral', 'steelblue']

bars = ax.bar(categorias, valores, color=colores, edgecolor='black', linewidth=1.5, width=0.6)

# Agregar valores en las barras
for bar, val in zip(bars, valores):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'${val:,.1f}M\n(${val*1e6:,.0f})',
            ha='center', va='bottom', fontsize=10, fontweight='bold')

ax.set_title(f'COMPARACIÓN DE FLUJO TOTAL - INVERSIÓN ${MONTO_INVERSION_USD:,.0f} USD\n'
             f'Plazo: {PLAZO_FORWARD_MESES} meses | Crédito: {TASA_CREDITO_EA*100:.2f}% E.A.', 
             fontsize=14, fontweight='bold', pad=20)
ax.set_ylabel('Millones de COP', fontsize=12)
ax.grid(True, alpha=0.3, axis='y')

# Agregar línea de diferencia
if diferencia_vs_mediana > 0:
    ax.text(1.5, max(valores)*0.5, f'✅ Ahorro: ${diferencia_vs_mediana/1e6:,.2f}M', 
            fontsize=12, fontweight='bold', color='green',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
else:
    ax.text(1.5, max(valores)*0.5, f'❌ Costo adicional: ${abs(diferencia_vs_mediana)/1e6:,.2f}M', 
            fontsize=12, fontweight='bold', color='red',
            bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.7))

plt.tight_layout()
plt.savefig(os.path.join(ruta_base, "03_comparacion_flujo_total.png"), dpi=300, bbox_inches='tight')
plt.close()

# Gráfica 4: Serie histórica del spot
print("  • Gráfica 4: Serie histórica del spot...")
fig, ax = plt.subplots(figsize=(14, 7))

ax.plot(spot_data['Fecha'], spot_data['Spot'], linewidth=1.5, color='steelblue', alpha=0.8)
ax.axhline(FORWARD_RATE, color='red', linestyle='--', linewidth=2.5, label=f'Forward (${FORWARD_RATE:,.2f})')
ax.axhline(spot_actual, color='green', linestyle='--', linewidth=2.5, label=f'Spot Actual (${spot_actual:,.2f})')
ax.axhline(spot_prom, color='orange', linestyle=':', linewidth=2, label=f'Promedio Histórico (${spot_prom:,.2f})')

ax.fill_between(spot_data['Fecha'], spot_data['Spot'], alpha=0.3, color='steelblue')

ax.set_title('SERIE HISTÓRICA USDCOP=X - ÚLTIMOS 2 AÑOS', fontsize=14, fontweight='bold', pad=20)
ax.set_xlabel('Fecha', fontsize=12)
ax.set_ylabel('Tasa de Cambio (COP/USD)', fontsize=12)
ax.legend(loc='upper left', fontsize=10)
ax.grid(True, alpha=0.3)

# Formato de fechas
plt.xticks(rotation=45)
ax.tick_params(axis='x', labelsize=9)

plt.tight_layout()
plt.savefig(os.path.join(ruta_base, "04_serie_historica_spot.png"), dpi=300, bbox_inches='tight')
plt.close()

# Gráfica 5: Análisis de sensibilidad
print("  • Gráfica 5: Análisis de sensibilidad...")
fig, ax = plt.subplots(figsize=(14, 7))

percentiles_plot = [5, 10, 25, 50, 75, 90, 95]
valores_percentiles = [np.percentile(spot_futuro_simulado, p) for p in percentiles_plot]
pagos_percentiles = [v * MONTO_INVERSION_USD for v in valores_percentiles]
mejor_opcion = ['FORWARD' if p > pago_inversion_forward else 'SPOT' for p in pagos_percentiles]
colores_opcion = ['red' if op == 'FORWARD' else 'green' for op in mejor_opcion]

x = np.arange(len(percentiles_plot))
width = 0.35

bars1 = ax.bar(x - width/2, [p/1e9 for p in pagos_percentiles], width, 
               label='Pago con Spot', color='steelblue', alpha=0.7, edgecolor='black')
bars2 = ax.bar(x + width/2, [pago_inversion_forward/1e9]*len(percentiles_plot), width, 
               label='Pago con Forward', color='red', alpha=0.7, edgecolor='black')

ax.set_xlabel('Percentil de la Distribución', fontsize=12)
ax.set_ylabel('Miles de Millones COP', fontsize=12)
ax.set_title(f'ANÁLISIS DE SENSIBILIDAD - SPOT vs FORWARD\n'
             f'Inversión: ${MONTO_INVERSION_USD:,.0f} USD | Forward: ${FORWARD_RATE:,.2f}', 
             fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels([f'P{p}' for p in percentiles_plot], fontsize=10)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3, axis='y')

# Agregar texto de mejor opción
for i, (p, mejor, color) in enumerate(zip(percentiles_plot, mejor_opcion, colores_opcion)):
    ax.text(i, max(pagos_percentiles)/1e9 * 1.05, mejor, ha='center', fontweight='bold', 
            color=color, fontsize=9, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

plt.tight_layout()
plt.savefig(os.path.join(ruta_base, "05_analisis_sensibilidad.png"), dpi=300, bbox_inches='tight')
plt.close()

# Gráfica 6: Evolución de caminos simulados
print("  • Gráfica 6: Evolución de caminos simulados...")
fig, ax = plt.subplots(figsize=(14, 7))

# Plotear algunos caminos aleatorios
num_caminos = 100
indices = np.random.choice(n_simulaciones, num_caminos, replace=False)

tiempo = np.linspace(0, PLAZO_FORWARD_MESES, dias_proyeccion + 1)

for idx in indices:
    ax.plot(tiempo, paths[idx], linewidth=0.5, alpha=0.3, color='steelblue')

# Línea de la media
ax.plot(tiempo, np.mean(paths, axis=0), 'r-', linewidth=2.5, label='Media Simulaciones')

# Líneas de percentiles
ax.plot(tiempo, np.percentile(paths, 5, axis=0), 'g--', linewidth=2, alpha=0.7, label='Percentil 5%')
ax.plot(tiempo, np.percentile(paths, 95, axis=0), 'g--', linewidth=2, alpha=0.7, label='Percentil 95%')

# Línea del forward
ax.axhline(FORWARD_RATE, color='red', linestyle=':', linewidth=2.5, label=f'Forward (${FORWARD_RATE:,.2f})')

ax.set_title(f'EVOLUCIÓN DE CAMINOS SIMULADOS - {num_caminos} TRAYECTORIAS\n'
             f'Proyección a {PLAZO_FORWARD_MESES} meses', fontsize=14, fontweight='bold', pad=20)
ax.set_xlabel('Meses', fontsize=12)
ax.set_ylabel('Tasa de Cambio (COP/USD)', fontsize=12)
ax.legend(loc='upper left', fontsize=10)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(ruta_base, "06_caminos_simulados.png"), dpi=300, bbox_inches='tight')
plt.close()

# Gráfica 7: Análisis de riesgo - VaR
print("  • Gráfica 7: Análisis de riesgo - VaR...")
fig, axes = plt.subplots(1, 2, figsize=(18, 7))

# Panel izquierdo - VaR
categorias_var = ['VaR 95%\nSin Cobertura', 'VaR 95%\nCon Forward', 'VaR 99%\nSin Cobertura', 'VaR 99%\nCon Forward']
valores_var = [var_95_sin_cobertura/1e6, var_95_con_forward/1e6, 
               var_99_sin_cobertura/1e6, var_99_con_forward/1e6]
colores_var = ['orange', 'steelblue', 'red', 'steelblue']

bars_var = axes[0].bar(categorias_var, valores_var, color=colores_var, edgecolor='black', linewidth=1.5)

for bar, val in zip(bars_var, valores_var):
    height = bar.get_height()
    axes[0].text(bar.get_x() + bar.get_width()/2., height,
                f'${val:,.1f}M',
                ha='center', va='bottom', fontsize=10, fontweight='bold')

axes[0].set_title('VALUE AT RISK (VaR) - COMPARACIÓN', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Millones de COP', fontsize=11)
axes[0].grid(True, alpha=0.3, axis='y')

# Panel derecho - CVaR
categorias_cvar = ['CVaR 95%\nSin Cobertura', 'CVaR 95%\nCon Forward']
valores_cvar = [cvar_95_sin_cobertura/1e6, cvar_95_con_forward/1e6]
colores_cvar = ['orange', 'steelblue']

bars_cvar = axes[1].bar(categorias_cvar, valores_cvar, color=colores_cvar, edgecolor='black', linewidth=1.5)

for bar, val in zip(bars_cvar, valores_cvar):
    height = bar.get_height()
    axes[1].text(bar.get_x() + bar.get_width()/2., height,
                f'${val:,.1f}M',
                ha='center', va='bottom', fontsize=10, fontweight='bold')

axes[1].set_title('CONDITIONAL VaR (CVaR) - COMPARACIÓN', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Millones de COP', fontsize=11)
axes[1].grid(True, alpha=0.3, axis='y')

plt.suptitle(f'ANÁLISIS DE RIESGO - INVERSIÓN ${MONTO_INVERSION_USD:,.0f} USD', 
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(ruta_base, "07_analisis_riesgo_var.png"), dpi=300, bbox_inches='tight')
plt.close()

print("\n✅ Todas las gráficas generadas exitosamente")
print()

# ============================================================================
# 12. RESUMEN FINAL Y VERIFICACIÓN DE ARCHIVOS
# ============================================================================

print("="*100)
print("SECCIÓN 11: RESUMEN FINAL Y VERIFICACIÓN DE ARCHIVOS GENERADOS")
print("="*100)

print(f"\n📊 RESUMEN EJECUTIVO DEL ANÁLISIS:")
print("-"*100)
print(f"✓ Tasa forward SET-FX utilizada: ${FORWARD_RATE:,.2f} COP/USD")
print(f"✓ Spot actual: ${spot_actual:,.2f} COP/USD")
print(f"✓ Monto de inversión: ${MONTO_INVERSION_USD:,.0f} USD")
print(f"✓ Plazo de la cobertura: {PLAZO_FORWARD_MESES} meses")
print()
print(f"📈 RESULTADOS PRINCIPALES:")
print(f"  • Escenarios protegidos: {pct_protegidos:.2f}%")
print(f"  • Beneficio neto esperado: ${beneficio_neto_esperado:,.0f} COP")
print(f"  • Diferencia vs sin cobertura: ${diferencia_vs_mediana:+,.0f} COP")
print(f"  • Reducción de riesgo (VaR 95%): ${abs(reduccion_var_95):,.0f} COP")
print()
print(f"🎯 RECOMENDACIÓN: {'CONTRATAR FORWARD' if criterios_cumplidos >= 4 else 'EVALUAR RIESGO VS COSTO' if criterios_cumplidos >= 3 else 'NO CONTRATAR FORWARD'}")
print(f"   Criterios cumplidos: {criterios_cumplidos} de {len(criterios)}")
print()

print(f"📁 ARCHIVOS GENERADOS EN: {ruta_base}")
print("="*100)

archivos_esperados = [
    "forward_setfx_datos.csv",
    "spot_usdcop_historico.csv",
    "ANALISIS_FORWARD_COMPLETO.txt",
    "01_distribucion_spot_forward.png",
    "02_escenarios_proteccion.png",
    "03_comparacion_flujo_total.png",
    "04_serie_historica_spot.png",
    "05_analisis_sensibilidad.png",
    "06_caminos_simulados.png",
    "07_analisis_riesgo_var.png"
]

print()
for archivo in archivos_esperados:
    ruta_completa = os.path.join(ruta_base, archivo)
    if os.path.exists(ruta_completa):
        tamaño = os.path.getsize(ruta_completa)
        print(f"   ✅ {archivo:<40s} {tamaño:>12,} bytes")
    else:
        print(f"   ❌ {archivo:<40s} NO GENERADO")

print()
print("="*100)
print(" "*30 + "FIN DEL PROCESO - PUNTO 5 COMPLETADO")
print("="*100)
print()