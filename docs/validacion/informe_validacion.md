# Informe de validación estática

Generado por `tools/validar_cfx.py`. Una validación estática **no garantiza** que SQX build 144 abra los archivos sin avisos: sólo que son ZIP/XML válidos, con la misma estructura, atributos y catálogo de bloques que los originales build 140.2099 y con valores coherentes.

## Ida y vuelta de los originales

| Original | C14N idéntico tras reescribir |
|---|---|
| Estrategia_Build_ConfigInicial_H1_BUY.cfx | sí |
| Estrategia_Retest_ConfigInicial_H1_BUY.cfx | sí |
| Ventaja_Build_ConfigInicial_H1_BUY.cfx | sí |
| Ventaja_Retest_ConfigInicial_H1_BUY.cfx | sí |

## Archivos generados

| Archivo | Tamaño ZIP | Resultado |
|---|---|---|
| `DayTrading/Estrategia_Build_ConfigInicial_H1_BUY__DayTrading_M15_BUY.cfx` | 39,053 B | OK |
| `DayTrading/Estrategia_Build_ConfigInicial_H1_BUY__DayTrading_M15_SELL.cfx` | 39,022 B | OK |
| `DayTrading/Estrategia_Retest_ConfigInicial_H1_BUY__DayTrading_M15_BUY.cfx` | 6,299 B | OK |
| `DayTrading/Estrategia_Retest_ConfigInicial_H1_BUY__DayTrading_M15_SELL.cfx` | 6,304 B | OK |
| `DayTrading/Ventaja_Build_ConfigInicial_H1_BUY__DayTrading_M15_BUY.cfx` | 38,139 B | OK |
| `DayTrading/Ventaja_Build_ConfigInicial_H1_BUY__DayTrading_M15_SELL.cfx` | 38,109 B | OK |
| `DayTrading/Ventaja_Retest_ConfigInicial_H1_BUY__DayTrading_M15_BUY.cfx` | 6,217 B | OK |
| `DayTrading/Ventaja_Retest_ConfigInicial_H1_BUY__DayTrading_M15_SELL.cfx` | 6,222 B | OK |
| `NewsProxy/Estrategia_Build_ConfigInicial_H1_BUY__NewsProxy_M15_BUY.cfx` | 38,653 B | OK |
| `NewsProxy/Estrategia_Build_ConfigInicial_H1_BUY__NewsProxy_M15_SELL.cfx` | 38,668 B | OK |
| `NewsProxy/Estrategia_Retest_ConfigInicial_H1_BUY__NewsProxy_M15_BUY.cfx` | 6,311 B | OK |
| `NewsProxy/Estrategia_Retest_ConfigInicial_H1_BUY__NewsProxy_M15_SELL.cfx` | 6,317 B | OK |
| `NewsProxy/Ventaja_Build_ConfigInicial_H1_BUY__NewsProxy_M15_BUY.cfx` | 37,727 B | OK |
| `NewsProxy/Ventaja_Build_ConfigInicial_H1_BUY__NewsProxy_M15_SELL.cfx` | 37,741 B | OK |
| `NewsProxy/Ventaja_Retest_ConfigInicial_H1_BUY__NewsProxy_M15_BUY.cfx` | 6,229 B | OK |
| `NewsProxy/Ventaja_Retest_ConfigInicial_H1_BUY__NewsProxy_M15_SELL.cfx` | 6,234 B | OK |
| `Position/Estrategia_Build_ConfigInicial_H1_BUY__Position_D1_BUY.cfx` | 38,862 B | OK |
| `Position/Estrategia_Build_ConfigInicial_H1_BUY__Position_D1_SELL.cfx` | 38,850 B | OK |
| `Position/Estrategia_Retest_ConfigInicial_H1_BUY__Position_D1_BUY.cfx` | 6,265 B | OK |
| `Position/Estrategia_Retest_ConfigInicial_H1_BUY__Position_D1_SELL.cfx` | 6,271 B | OK |
| `Position/Ventaja_Build_ConfigInicial_H1_BUY__Position_D1_BUY.cfx` | 37,974 B | OK |
| `Position/Ventaja_Build_ConfigInicial_H1_BUY__Position_D1_SELL.cfx` | 37,968 B | OK |
| `Position/Ventaja_Retest_ConfigInicial_H1_BUY__Position_D1_BUY.cfx` | 6,207 B | OK |
| `Position/Ventaja_Retest_ConfigInicial_H1_BUY__Position_D1_SELL.cfx` | 6,213 B | OK |
| `PriceAction/Estrategia_Build_ConfigInicial_H1_BUY__PriceAction_H1_BUY.cfx` | 38,377 B | OK |
| `PriceAction/Estrategia_Build_ConfigInicial_H1_BUY__PriceAction_H1_SELL.cfx` | 38,393 B | OK |
| `PriceAction/Estrategia_Retest_ConfigInicial_H1_BUY__PriceAction_H1_BUY.cfx` | 6,284 B | OK |
| `PriceAction/Estrategia_Retest_ConfigInicial_H1_BUY__PriceAction_H1_SELL.cfx` | 6,289 B | OK |
| `PriceAction/Ventaja_Build_ConfigInicial_H1_BUY__PriceAction_H1_BUY.cfx` | 37,454 B | OK |
| `PriceAction/Ventaja_Build_ConfigInicial_H1_BUY__PriceAction_H1_SELL.cfx` | 37,468 B | OK |
| `PriceAction/Ventaja_Retest_ConfigInicial_H1_BUY__PriceAction_H1_BUY.cfx` | 6,213 B | OK |
| `PriceAction/Ventaja_Retest_ConfigInicial_H1_BUY__PriceAction_H1_SELL.cfx` | 6,218 B | OK |
| `Range/Estrategia_Build_ConfigInicial_H1_BUY__Range_H1_BUY.cfx` | 38,933 B | OK |
| `Range/Estrategia_Build_ConfigInicial_H1_BUY__Range_H1_SELL.cfx` | 38,933 B | OK |
| `Range/Estrategia_Retest_ConfigInicial_H1_BUY__Range_H1_BUY.cfx` | 6,296 B | OK |
| `Range/Estrategia_Retest_ConfigInicial_H1_BUY__Range_H1_SELL.cfx` | 6,301 B | OK |
| `Range/Ventaja_Build_ConfigInicial_H1_BUY__Range_H1_BUY.cfx` | 37,968 B | OK |
| `Range/Ventaja_Build_ConfigInicial_H1_BUY__Range_H1_SELL.cfx` | 37,967 B | OK |
| `Range/Ventaja_Retest_ConfigInicial_H1_BUY__Range_H1_BUY.cfx` | 6,218 B | OK |
| `Range/Ventaja_Retest_ConfigInicial_H1_BUY__Range_H1_SELL.cfx` | 6,224 B | OK |
| `Scalping/Estrategia_Build_ConfigInicial_H1_BUY__Scalping_M5_BUY.cfx` | 38,934 B | OK |
| `Scalping/Estrategia_Build_ConfigInicial_H1_BUY__Scalping_M5_SELL.cfx` | 38,930 B | OK |
| `Scalping/Estrategia_Retest_ConfigInicial_H1_BUY__Scalping_M5_BUY.cfx` | 6,291 B | OK |
| `Scalping/Estrategia_Retest_ConfigInicial_H1_BUY__Scalping_M5_SELL.cfx` | 6,296 B | OK |
| `Scalping/Ventaja_Build_ConfigInicial_H1_BUY__Scalping_M5_BUY.cfx` | 38,028 B | OK |
| `Scalping/Ventaja_Build_ConfigInicial_H1_BUY__Scalping_M5_SELL.cfx` | 38,017 B | OK |
| `Scalping/Ventaja_Retest_ConfigInicial_H1_BUY__Scalping_M5_BUY.cfx` | 6,210 B | OK |
| `Scalping/Ventaja_Retest_ConfigInicial_H1_BUY__Scalping_M5_SELL.cfx` | 6,216 B | OK |
| `Swing/Estrategia_Build_ConfigInicial_H1_BUY__Swing_H4_BUY.cfx` | 38,952 B | OK |
| `Swing/Estrategia_Build_ConfigInicial_H1_BUY__Swing_H4_SELL.cfx` | 38,920 B | OK |
| `Swing/Estrategia_Retest_ConfigInicial_H1_BUY__Swing_H4_BUY.cfx` | 6,277 B | OK |
| `Swing/Estrategia_Retest_ConfigInicial_H1_BUY__Swing_H4_SELL.cfx` | 6,283 B | OK |
| `Swing/Ventaja_Build_ConfigInicial_H1_BUY__Swing_H4_BUY.cfx` | 38,037 B | OK |
| `Swing/Ventaja_Build_ConfigInicial_H1_BUY__Swing_H4_SELL.cfx` | 37,994 B | OK |
| `Swing/Ventaja_Retest_ConfigInicial_H1_BUY__Swing_H4_BUY.cfx` | 6,206 B | OK |
| `Swing/Ventaja_Retest_ConfigInicial_H1_BUY__Swing_H4_SELL.cfx` | 6,211 B | OK |
| `TrendFollowing/Estrategia_Build_ConfigInicial_H1_BUY__TrendFollowing_H1_BUY.cfx` | 38,977 B | OK |
| `TrendFollowing/Estrategia_Build_ConfigInicial_H1_BUY__TrendFollowing_H1_SELL.cfx` | 38,948 B | OK |
| `TrendFollowing/Estrategia_Retest_ConfigInicial_H1_BUY__TrendFollowing_H1_BUY.cfx` | 6,308 B | OK |
| `TrendFollowing/Estrategia_Retest_ConfigInicial_H1_BUY__TrendFollowing_H1_SELL.cfx` | 6,313 B | OK |
| `TrendFollowing/Ventaja_Build_ConfigInicial_H1_BUY__TrendFollowing_H1_BUY.cfx` | 38,115 B | OK |
| `TrendFollowing/Ventaja_Build_ConfigInicial_H1_BUY__TrendFollowing_H1_SELL.cfx` | 38,074 B | OK |
| `TrendFollowing/Ventaja_Retest_ConfigInicial_H1_BUY__TrendFollowing_H1_BUY.cfx` | 6,229 B | OK |
| `TrendFollowing/Ventaja_Retest_ConfigInicial_H1_BUY__TrendFollowing_H1_SELL.cfx` | 6,235 B | OK |

**Total: 64 archivos, 0 errores.**
