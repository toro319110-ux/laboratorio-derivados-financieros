# 🏦 Laboratorio 1 - Derivados Financieros

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-orange.svg)](https://pandas.pydata.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7+-green.svg)](https://matplotlib.org/)
[![Estado](https://img.shields.io/badge/Estado-✅_Completado-green.svg)]()

**Análisis de Riesgo Cambiario y Cobertura con Derivados Financieros**

---

## 👥 Equipo de Trabajo

| Integrante | Cédula |
|------------|--------|
| Santiago Toro Cadavid | 1040739414 |
| Yenny Carolina Serna Chaverra | 1017210528 |
| Daniela Perez Meza | 1017220748 |

**Curso:** Derivados Financieros  
**Fecha:** Marzo 2026  
**Institución:** Universidad

---

## 📋 Tabla de Contenidos

- [📊 Resumen Ejecutivo](#-resumen-ejecutivo)
- [📈 Punto 1: Análisis TRM](#-punto-1-análisis-fundamental-de-la-trm)
- [💰 Punto 2: Crédito en USD](#-punto-2-crédito-en-dólares)
- [💱 Punto 3: Riesgo Cambiario](#-punto-3-recreación-en-pesos)
- [🎲 Punto 4: Simulación Monte Carlo](#-punto-4-simulación-monte-carlo)
- [🛡️ Punto 5: Forward](#-punto-5-forward-de-cobertura)
- [🎯 Conclusiones Generales](#-conclusiones-generales)
- [📚 Referencias](#-referencias)
- [📁 Estructura del Repositorio](#-estructura-del-repositorio)
- [🚀 Cómo Ejecutar los Códigos](#-cómo-ejecutar-los-códigos)

---

## 📊 Resumen Ejecutivo

Este laboratorio analiza el **riesgo cambiario** del peso colombiano frente al dólar y evalúa diferentes estrategias de cobertura utilizando **derivados financieros**.

### 🔍 ¿Qué hicimos?

1. ✅ Analizamos la evolución histórica de la TRM y proyectamos su comportamiento
2. ✅ Simulamos un crédito en dólares para importar maquinaria
3. ✅ Evaluamos el impacto del riesgo cambiario en pesos colombianos
4. ✅ Usamos simulación Monte Carlo para proyectar escenarios futuros
5. ✅ Analizamos la conveniencia de usar forwards como cobertura

### 💡 Hallazgos Principales

| Indicador | Valor |
|-----------|-------|
| **TRM Actual** | $3,688 COP/USD |
| **Expectativa 12 meses** | $3,900 COP/USD (+5.7%) |
| **Impacto cambiario** | Hasta 18% adicional en créditos en USD |
| **Protección con Forward** | 17.55% de escenarios protegidos |
| **Recomendación Forward** | ❌ NO CONTRATAR (con tasa actual) |

---

## 📈 Punto 1: Análisis Fundamental de la TRM

### Objetivos
- Analizar factores que afectan la TRM
- Proyectar la expectativa del dólar a 12 meses
- Evaluar escenarios probabilísticos

### Resultados Principales

| Escenario | Probabilidad | TRM Proyectada | Variación |
|-----------|-------------|----------------|-----------|
| **Base** | 55% | $3,900 | +5.7% |
| Alcista | 25% | $4,325 | +17.2% |
| Bajista | 15% | $3,550 | -3.7% |
| Crisis | 5% | $4,900 | +32.9% |

### 💬 Lo que entendimos

> "La TRM hoy está en $3,688 pesos por dólar y esperamos que en un año suba a $3,900 pesos. Eso sería un aumento del 5.7%. Si tuviéramos que comprar dólares el próximo año, nos costaría más pesos. El peso colombiano se estaría 'debilitando' frente al dólar."

**Factores clave identificados:**
- 📊 Diferencial de tasas: BanRep 9.25% vs Fed 5.25%
- 🛢️ Precio del petróleo: $60-65 USD/barril
- 📉 Riesgo fiscal: Déficit ~7% del PIB
- 🗳️ Incertidumbre electoral 2026

📄 **Ver análisis completo:** [Laboratorio1_Punto1_Analisis_TRM.txt](outputs/PUNTO_1/Laboratorio1_Punto1_Analisis_TRM.txt)

---

## 💰 Punto 2: Crédito en Dólares

### Características del Financiamiento

| Concepto | Valor |
|----------|-------|
| Valor Maquinaria | $95,292.89 USD |
| Inicial (10%) | $9,529.29 USD |
| Monto Crédito | $85,763.60 USD |
| Tasa Interés | 8.25% E.A. |
| Plazo | 10 años (40 trimestres) |
| Cuota Trimestral | $3,186.45 USD |

### Comparativo USD vs COP

**En Pesos Colombianos (TRM $3,688.46):**
- Total a Pagar: $432,847,234 COP
- Total Intereses: $86,284,156 COP
- Costo Financiero: 50.2% del monto financiado

### 💬 Lo que entendimos

> "Los primeros años de la cuota, casi todo es INTERÉS y muy poco es pagar el préstamo. Es como cuando pagas la cuota de una tarjeta de crédito... al principio casi no baja la deuda. El problema grande es que este crédito es en DÓLARES. Si la TRM sube, mi cuota en pesos también sube."

### Tasas de Mercado Americano

| Entidad | Tasa Promedio | Plazo Máx |
|---------|--------------|-----------|
| SBA 7(a) Loan | 10.50% | 10 años |
| Equipment Loan | 8.25% | 10 años |
| Commercial Bank | 8.75% | 15 años |
| Wells Fargo | 8.12% | 10 años |
| JPMorgan Chase | 7.87% | 10 años |
| Bank of America | 8.37% | 10 años |

📄 **Ver análisis completo:** [Laboratorio1_Punto2_Credito_USD.txt](outputs/PUNTO_2/Laboratorio1_Punto2_Credito_USD.txt)

---

## 💱 Punto 3: Recreación en Pesos

### Análisis de Impacto Cambiario

| Concepto | USD | COP (Proyectado) |
|----------|-----|------------------|
| Total a Pagar | $127,627.82 | $523,412,000 |
| Total Intereses | $41,864.22 | $78,512,000 |

### Proyección TRM 10 Años

**Resultados:**
- TRM Inicial: $3,688 COP/USD
- TRM Promedio: $5,234 COP/USD
- TRM Final: $6,145 COP/USD
- **Variación: +66.62%**
- **Impacto Cambiario: $245,678,901 COP (+18.45%)**

### 💬 Lo que entendimos

> "Imaginen que planean gastar $100.000 en algo, pero al final terminan gastando $118.000 solo porque el dólar subió. Eso es lo que pasa aquí: el riesgo cambiario nos puede 'cobrar' un 18% extra sin que nosotros hayamos hecho nada malo. No podemos controlar la TRM."

📄 **Ver análisis completo:** [Laboratorio1_Punto3_Credito_COP.txt](outputs/PUNTO_3/Laboratorio1_Punto3_Credito_COP.txt)

---

## 🎲 Punto 4: Simulación Monte Carlo

### Metodología BMG (Movimiento Browniano Geométrico)

**Parámetros:**
- Período histórico: 2019-2024 (5 años)
- Simulaciones: 1,000 trayectorias
- Horizonte: 5 años
- Distribuciones: Normal y T-Student

### Resultados

| Estadístico | Valor |
|-------------|-------|
| Media retorno mensual | +0.45% |
| Volatilidad mensual | 2.85% |
| TRM proyectada (media) | $4,850 COP/USD |
| VaR 95% | $3,420 COP/USD |

### 💬 Lo que entendimos

> "Es como lanzar un dado 50.000 veces para ver qué pasa en promedio. En vez de adivinar el futuro, simulamos MUCHOS futuros posibles. Hay MUCHA incertidumbre: la TRM podría terminar entre $2,890 y $7,650. Al principio me asustó tanta fórmula, pero después entendí que es como hacer muchas apuestas virtuales."

📄 **Ver análisis completo:** [resultados.txt](outputs/PUNTO_4/resultados.txt)

---

## 🛡️ Punto 5: Forward de Cobertura

### Parámetros del Forward SET-FX

| Concepto | Valor |
|----------|-------|
| Spot Actual | $3,688.46 COP/USD |
| Forward 6 meses | $3,968.63 COP/USD |
| Diferencia | +$280.17 (+7.60%) |
| Monto Cobertura | $500,000 USD |

### Análisis de Protección

**Resultados Simulación (50,000 escenarios):**

| Escenario | Cantidad | Porcentaje |
|-----------|----------|------------|
| **Protegidos** ✅ | 8,776 | 17.55% |
| No Protegidos ❌ | 41,224 | 82.45% |

### Métricas de Riesgo

| Métrica | Sin Cobertura | Con Forward |
|---------|--------------|-------------|
| VaR 95% | $1,512,635,541 | $1,984,315,000 (FIJO) |
| CVaR 95% | $1,450,894,653 | $1,984,315,000 |
| Volatilidad | $189,779,442 | $0 (ELIMINADA) |

### 💬 Lo que entendimos

> "El forward es como hacer un 'contrato de precio fijo' para el futuro. Solo protege en 17.55% de los casos, pero elimina completamente el riesgo. Si yo fuera el empresario, probablemente SÍ contrataría el forward. No porque sea el más barato, sino porque me permite dormir tranquilo sabiendo exactamente cuánto voy a pagar. La tranquilidad también tiene valor."

### Recomendación Final

**❌ NO CONTRATAR FORWARD** (con tasa actual)

**Justificación:**
- Valor esperado negativo: -$176,342,713 COP
- Solo conveniente en 17.55% de escenarios
- Relación Beneficio/Costo: 0.10
- **Alternativa:** Negociar forward más competitivo o usar opciones

📄 **Ver análisis completo:** [Forward_Analisis_Completo.txt](outputs/FORWARD/Forward_Analisis_Completo.txt)

---

## 🎯 Conclusiones Generales

### Lecciones Aprendidas

1. **📊 La TRM es impredecible**  
   Aunque podemos analizar tendencias y proyecciones, el tipo de cambio tiene alta volatilidad e incertidumbre.

2. **💰 Créditos en moneda extranjera**  
   Pueden ser más baratos en tasas de interés, pero exponen a riesgo cambiario significativo.

3. **⚡ Impacto del riesgo cambiario**  
   Puede representar hasta 18% adicional en el costo total sin previo aviso.

4. **🎲 Simulaciones Monte Carlo**  
   Herramienta poderosa para visualizar múltiples escenarios futuros y tomar decisiones informadas.

5. **🛡️ Forwards como cobertura**  
   Eliminan el riesgo cambiario pero tienen costo de oportunidad. La decisión depende del perfil de riesgo.

### Reflexión Final

> "En finanzas, casi nunca hay respuestas blancas o negras. Todo es un balance entre: **rentabilidad**, **riesgo** y **tranquilidad**. No existe la decisión perfecta, solo la que mejor se adapta a tu perfil y necesidades."

---

## 📚 Referencias

### Fuentes de Datos

- **Banco de la República.** (2026). Tasa Representativa del Mercado (TRM). https://www.banrep.gov.co/es/trm
- **Federal Reserve.** (2026). Federal Funds Rate. https://www.federalreserve.gov
- **SBA.gov.** (2026). 7(a) Loan Program. https://www.sba.gov/funding-programs/loans/7a-loans
- **BankRate.** (2026). Commercial Equipment Loan Rates. https://www.bankrate.com
- **SET-FX.** (2026). Mercado de Derivados Cambiarios. https://www.set-fx.com

### Bibliografía

- **Hull, J. C.** (2021). *Options, Futures, and Other Derivatives* (11th ed.). Pearson.
- **McDonald, R. L.** (2022). *Derivatives Markets* (4th ed.). Pearson.
- **Glasserman, P.** (2020). *Monte Carlo Methods in Financial Engineering*. Springer.

---

## 📁 Estructura del Repositorio
