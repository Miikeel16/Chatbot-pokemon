# PokéRAG: Asistente de Consulta de Evoluciones y Builds

## Descripción
PokéRAG es un asistente basado en **RAG (Retrieval-Augmented Generation)** diseñado para responder consultas rápidas sobre niveles de evolución, estadísticas clave y movimientos recomendados de los 151 Pokémon de Kanto.

## Arquitectura
1. **Base Documental (`download_data.py`):** Extrae los datos estructurados desde PokéAPI y los guarda en `data/pokemon_data.json`.
2. **Recuperación (`all-MiniLM-L6-v2`):** Convierte las fichas y la pregunta en embeddings y calcula la similitud del coseno mediante `scikit-learn`. Incluye un umbral de similitud (`0.45`) para evitar alucinaciones cuando se pregunta por Pokémon fuera de la base de datos.
3. **Generación (`Qwen/Qwen2.5-0.5B-Instruct`):** Redacta la respuesta final basándose únicamente en las fichas recuperadas.

## Ejecución
1. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
