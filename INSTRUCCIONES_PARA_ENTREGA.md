# Estado de entrega y acciones finales

**Fecha límite: 24 de noviembre de 2026, 23:59**. Son cinco integrantes y hay una exposición presencial de diez minutos.

## Ya generado en este workspace por @workspace-mcp

1. `final_visualizations.ipynb`: **ejecutado** sobre el CSV verdadero (9,994 filas), sin celdas de error. Incluye limpieza, histogramas, KDE, boxplot, intervalos bootstrap de confianza, heatmap de correlaciones, scatter/bubble Plotly, series temporales y mapa geográfico.
2. `outputs/figures/`: 12 archivos exportados, incluidos PNG/SVG/HTML. `outputs/tables/`: ocho CSV.
3. `dashboard/app.py`: dashboard interactivo Streamlit, con filtros de fecha/año, estado, región, categoría y segmento, cruce por selección de barras, métricas KPI, mapas y descarga CSV. Se comprobó que **inicia con HTTP 200**. Falta una revisión visual en navegador.
4. `presentation/Superstore_Executive_Story.pptx`: PowerPoint **editable**, 10 diapositivas, generado en el workspace.
5. `presentation/Superstore_Executive_Story.pdf`: presentación PDF.
6. `presentation/TEAM_SCRIPT.md`: guion en inglés para cinco participantes.
7. `data/raw/Sample_Superstore.csv`, `data/processed/superstore_clean.csv`, `data/verified_summary.json`: datasets y métricas verificadas.

## Pendientes de entrega (importantes)

- **Dashboard nativo**: ahora existe `dashboard/Superstore_Executive_Dashboard.twbx`, con CSV, 4 hojas, dashboard y un filtro cruzado de categorías. Se validó el archivo XML y su empaquetado, pero **no se pudo abrir visualmente en Tableau Desktop/Public**, porque no está instalado en Linux. Es importante abrirlo en Windows/macOS y verificar su funcionamiento antes de entregar. Streamlit se conserva como alternativa funcional.
- **GitHub**: el repositorio ya está publicado como público en https://github.com/MarcoCaamal/database-knowledge-extraction. Solo resta comprobar que el enlace abra sin iniciar sesión y actualizar los nombres de integrantes cuando se conozcan.
- **Nombres**: la presentación y el guion ya contienen a Juan Manuel Sánchez Hernández (2302084), Seir Mendoza Vidal (2302072), José Rodrigo de la Cruz Chim (2302089) y Marco Antonio Caamal Chi (2302075). Falta el quinto integrante exigido por el profesor.
- **Revisión visual y exposición**: abrir dashboard, ensayar el tiempo, compartir presentación y mirar el último video de la clase (no fue adjuntado).

## Comandos de comprobación

```bash
cd ~/projects/database-knowledge-extraction
.venv/bin/python scripts/qa.py
.venv/bin/streamlit run dashboard/app.py
```

Eviten atribuir causalidad a la relación entre descuentos y pérdidas. Mencionen que los datos son una muestra didáctica histórica y que las recomendaciones requieren pilotos controlados.
