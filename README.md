# PokéRAG: Asistente de Consulta de Evoluciones y Builds

## 📌 Descripción del Proyecto
PokéRAG es un sistema RAG (*Retrieval-Augmented Generation*) diseñado para responder consultas sencillas sobre evoluciones y builds de Pokémon sin necesidad de navegar por wikis extensas.

El sistema combina:
- **Recuperación semántica:** Transformación de fichas de Pokémon a embeddings (`sentence-transformers/all-MiniLM-L6-v2`) y cálculo de similitud del coseno mediante `scikit-learn`.
- **Generación:** Redacción de respuestas concisas utilizando el modelo `google/flan-t5-small` condicionado al contexto recuperado.

---

## 🛠️ Instalación y Requisitos
Asegúrate de instalar los requisitos necesarios:

```bash
pip install -r requirements.txt