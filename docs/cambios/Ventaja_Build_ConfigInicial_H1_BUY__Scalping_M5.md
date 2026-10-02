# Ventaja_Build_ConfigInicial_H1_BUY__Scalping_M5

*Original:* `Ventaja_Build_ConfigInicial_H1_BUY.cfx` · *Estilo:* Scalping (micro-ruptura en sesión líquida) · *Timeframe:* M5 · *Rol:* Builder de test de ventaja (entrada)

Tabla generada automáticamente a partir de los cambios aplicados al XML (cada fila es un valor que difiere del original). Estado: **no validado en SQX** (ver docs/04).

| Sección | Parámetro | Valor original | Valor nuevo | Justificación |
|---|---|---|---|---|
| Task | `Task@templateFile` | C:\Users\<usuario>\Desktop\Ventaja_Build_ConfigInicial_H1_BUY.cfx | Ventaja_Build_ConfigInicial_H1_BUY__Scalping_M5.cfx | Ruta local del autor (C:\Users\<usuario>\Desktop\...) sustituida por el nombre del nuevo archivo: no aporta nada y expone el nombre de usuario de Windows. |
| Trading options | `Param key="SignalTimeRangeFrom"` | 5400 | 32400 | 09:00 servidor ≈ apertura de Londres (UTC+2). |
| Trading options | `Param key="SignalTimeRangeTo"` | 84600 | 66600 | 18:30 servidor ≈ final del solape Londres-NY. |
| Trading options | `Param key="ExitAtEndOfRange"` | false | true | Un scalper no arrastra posiciones fuera de su ventana. |
| Trading options | `Param key="ExitAtEndOfDay"` | false | true | Red de seguridad: nada abierto al cierre del día. |
| Trading options | `Param key="EODExitTime"` | 83040 | 75600 | Antes del rollover (spreads anchos). |
| Trading options | `Param key="ExitOnFriday"` | false | true | Sin riesgo de gap de fin de semana. |
| Trading options | `Param key="FridayExitTime"` | 74400 | 72000 | Viernes tarde: liquidez decreciente. |
| Trading options | `Param key="MaxTradesPerDay"` | 0 | 4 | Limita sobre-operar en días de ruido. |
| Trading options | `Param key="MaxDistanceFromMarket"` | false | true | Evita órdenes stop lejos del precio. |
| Trading options | `Param key="MaxDistancePct"` | 6 | 0.3 | 0,3 % ≈ 45 pips en GBPJPY; tope razonable para M5. |
| Trading options | `Param key="ReservedBars"` | 50 | 120 | ≥ periodo máximo (100) para que los indicadores estén calculados. |
| What to build · complejidad | `Chart@maxExitTypes` | 5 | 1 | Test de ventaja: sólo salida temporal, para medir la entrada aislada. |
| What to build · complejidad | `Chart@minPeriod` | 4 | 5 | Periodos 5-100 velas de M5 (25 min a 8 h): horizonte de micro-estructura; ≥100 no aporta nada a un scalper y sobreajusta. |
| What to build · complejidad | `Chart@maxPeriod` | 200 | 100 | Periodos 5-100 velas de M5 (25 min a 8 h): horizonte de micro-estructura; ≥100 no aporta nada a un scalper y sobreajusta. |
| Genetic options | `PopulationSize` | 15 | 30 | 5-15 individuos por isla es demasiado poco para que el cruce explore; 30-50 es un mínimo práctico. |
| Genetic options | `MaxGenerations` | 10 | 30 | Con 10 generaciones la evolución apenas actúa (y el reinicio por estancamiento a 30 nunca saltaba). |
| Genetic options | `Islands` | 5 | 4 | 4 islas: diversidad suficiente con menos coste. |
| Genetic options | `CrossoverProbability` | 46 | 80 | 46 % es bajo para un AG; 70-90 % es lo habitual (supuesto de práctica general, no de SQX). |
| Genetic options | `MutationProbability` | 35 | 30 | Algo menor para no destruir buenas soluciones. |
| Genetic options | `MigrationModulo` | 5 | 10 | Migrar cada 10 generaciones (con 30-40 generaciones). |
| Genetic options | `MigrationRate` | 6 | 10 | 6 % de 5 individuos = 0,3: la migración original era nula en la práctica. |
| Genetic options | `EvoRestartOnStagnation@generations` | 30 | 15 | Debe ser menor que MaxGenerations para poder actuar. |
| Genetic options | `BuildMode/Conditions (población inicial)` | ReturnDDRatio(IS) >= 2; AvgBarsInTrade(IS) >= 2; NumberOfTrades(IS) >= 250; WinningPct(IS) >= 35 | ReturnDDRatio(IS) >= 1.5; AvgBarsInTrade(IS) >= 3; NumberOfTrades(IS) >= 830; WinningPct(IS) >= 35 | Misma lógica del autor (≈60 % del Ret/DD final, ≈83 % de las operaciones, -5 puntos de acierto) con los umbrales del estilo. |
| Ranking | `Rankings/Conditions (filtros)` | AvgBarsInTrade(IS) >= 2; ReturnDDRatio(IS) >= 4; NumberOfTrades(IS) >= 300; WinningPct(IS) >= 40 | NumberOfTrades(IS) >= 1000; ReturnDDRatio(IS) >= 3; WinningPct(IS) >= 40; ProfitFactor(IS) >= 1.15; AvgBarsInTrade(IS) >= 3; NetProfit(OOS) > 0 | Umbrales del estilo (frecuencia, acierto típico, Ret/DD) + exigencia en el tramo de validación OOS, que el original no tenía. Test de ventaja: Ret/DD a la mitad, PF mínimo 1,15. |
| Ranking | `FitnessCriteria/Settings/Ranking` | Weighted: Stagnation (peso 1, min) | Weighted: SQN (peso 2, max), StagnationPct (peso 1, min) | SQN mide la calidad estadística de la entrada (expectativa/desviación·√N); el original optimizaba sólo 'Stagnation', que ignora el beneficio. |
| Data | `Setup/Chart@timeframe` | H1 | M5 | Timeframe del estilo Scalping. |
| Data | `Setup@slippage` | 0 | 0.5 | El original usa 0; en M5 un deslizamiento de 0,5 pips por orden stop/mercado es conservador-realista y cambia el signo de muchas estrategias. |
| Data | `Setup@dateFrom` | 2013.09.30 | 2016.01.04 | M5/M15: 5 años bastan en operaciones y reducen el cómputo. |
| Data | `OutOfSample/Range` | (sin OOS) | 2019.07.01–2020.12.31 | Nuevo tramo de validación dentro del Builder (el original no tenía OOS y filtraba sólo sobre IS). |
| Cross checks | `RetestOnAdditionalMarkets/Setup@timeframe` | H1 | M5 | Coherencia si se activa (sigue desactivado). |
| Building blocks | `Bloques activos · signals` | 146 activos | 12 activos: ADXRising(w1), ATRChangesUp(w1), ATRRising(w1), BBBarClosesAboveUp(w1), BBBarOpensAboveUpAfterOpenBelow(w2), BarOpensAboveHighestAfterOpenBelow(w3), KCBarClosesAboveUpper(w1), KCBarOpensAboveUpperAfterOpenBelow(w2), LaguerreRSICrossUP(w1), MARising(w1), RSICrossUp(w1), StdDevRising(w1) | Bloques de ruptura de rango corto (Donchian, Bollinger, Keltner, máximo de sesión asiática) + confirmación de expansión de volatilidad sin niveles absolutos (dependientes de precio). |
| Building blocks | `Bloques activos · indicators` | 29 activos | 17 activos: CrossesAbove(w1), CrossesBelow(w1), Indicators.ATR(w1), Indicators.BollingerBands(w1), Indicators.EMA(w1), Indicators.Highest(w2), Indicators.KeltnerChannel(w1), Indicators.Lowest(w1), IsGreater(w1), IsGreaterCount(w1), IsLower(w1), Prices.Close(w1), Prices.High(w1), Prices.Low(w1), Prices.Open(w1), Prices.SessionHigh(w2), Prices.SessionLow(w1) | Bloques de ruptura de rango corto (Donchian, Bollinger, Keltner, máximo de sesión asiática) + confirmación de expansión de volatilidad sin niveles absolutos (dependientes de precio). |
| Building blocks | `Bloques activos · stopLimitBlocks` | 29 activos | 8 activos: Stop/Limit Price Levels.BollingerBands(w1), Stop/Limit Price Levels.High(w2), Stop/Limit Price Levels.Highest(w3), Stop/Limit Price Levels.KeltnerChannel(w1), Stop/Limit Price Levels.SessionHigh(w2), Stop/Limit Price Ranges.ATR(w2), Stop/Limit Price Ranges.BarRange(w1), Stop/Limit Price Ranges.SmallestRange(w1) | Bloques de ruptura de rango corto (Donchian, Bollinger, Keltner, máximo de sesión asiática) + confirmación de expansión de volatilidad sin niveles absolutos (dependientes de precio). |
| Building blocks | `Prices.SessionHigh · Start Hours` | 0..23/1 | 1..3/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Prices.SessionHigh · Start Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Prices.SessionHigh · End Hours` | 0..23/1 | 8..10/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Prices.SessionHigh · End Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Prices.SessionLow · Start Hours` | 0..23/1 | 1..3/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Prices.SessionLow · Start Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Prices.SessionLow · End Hours` | 0..23/1 | 8..10/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Prices.SessionLow · End Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Stop/Limit Price Levels.SessionHigh · Start Hours` | 0..23/1 | 1..3/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Stop/Limit Price Levels.SessionHigh · Start Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Stop/Limit Price Levels.SessionHigh · End Hours` | 0..23/1 | 8..10/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `Stop/Limit Price Levels.SessionHigh · End Minutes` | 0..59/1 | 0..0/1 | Rango acotado al estilo (ver ficha). |
| Building blocks | `LaguerreRSICrossUP · Gamma` | 0..0.95/0.01 | 0.3..0.8/0.05 | Rango acotado al estilo (ver ficha). |
| Building blocks | `LaguerreRSICrossUP · Level` | 0.05..0.95/0.05 | 0.4..0.85/0.05 | Rango acotado al estilo (ver ficha). |
| Building blocks | `RSICrossUp · Level` | 0..100/5 | 50..70/5 | Rango acotado al estilo (ver ficha). |
| Order types | `EnterAtStop@use` | false | true | Orden stop por encima del máximo: entra sólo si la ruptura ocurre; validez 1-3 velas (5-15 min) para no comprar rupturas viejas. |
| Order types | `EnterAtStop@weight` | 1 | 2 | Peso relativo entre tipos de orden. |
| Order types | `EnterAtStop · BarsValid min` | 2 | 1 | Orden stop por encima del máximo: entra sólo si la ruptura ocurre; validez 1-3 velas (5-15 min) para no comprar rupturas viejas. |
| Order types | `EnterAtStop · BarsValid max` | 10 | 3 | Orden stop por encima del máximo: entra sólo si la ruptura ocurre; validez 1-3 velas (5-15 min) para no comprar rupturas viejas. |
| Order types | `EnterAtStop · ExitAfterBars min` | 5 | 3 | Alineado con el rango de ExitTypes para eliminar la ambigüedad del original (5-20 vs 2-15). |
| Order types | `EnterAtStop · ExitAfterBars max` | 20 | 24 | Alineado con el rango de ExitTypes. |
| Order types | `EnterAtMarket · ExitAfterBars min` | 5 | 3 | Alineado con el rango de ExitTypes para eliminar la ambigüedad del original (5-20 vs 2-15). |
| Order types | `EnterAtMarket · ExitAfterBars max` | 20 | 24 | Alineado con el rango de ExitTypes. |
| Exit types | `ExitAfterBars@probability` | 50 | 100 | Explícito: es la única salida (el original ponía 50 y dependía de minExitTypes=1). |
| Exit types | `ExitAfterBars min` | 2 | 3 | Test de ventaja: salida pura por tiempo 15 min-2 h, sin SL/PT. |
| Exit types | `ExitAfterBars max` | 15 | 24 | Test de ventaja: salida pura por tiempo 15 min-2 h, sin SL/PT. |
| Notes | `Notes` | <b>Breakout strategies setup</b><div><br></div><div><br></div><div><br></div><div><br></div> | <b>Scalping (micro-ruptura en sesión líquida) – Builder de test de ventaja (entrada)</b><div>Derivado de Ventaja_Build_ConfigInicial_H1_BUY (build 140.2099). Timeframe M5. Ver docs/03 (ficha Scalping) y docs/04 (checklist).</div><div>NO VALIDADO EN SQX: revisar símbolo, costes, horario del servidor e importación.</div> | Descripción del estilo y advertencias. |
