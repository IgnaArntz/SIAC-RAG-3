# SIAC - Sistema Inteligente de Asistencia Clínica

SIAC es un asistente clínico virtual académico desarrollado con **FastAPI** y una arquitectura híbrida basada en **RAG (Retrieval-Augmented Generation)**, **memoria conversacional** y **observabilidad**.

El sistema permite responder preguntas relacionadas con documentos clínicos almacenados en una base vectorial **ChromaDB**, mantener contexto básico de la conversación mediante memoria temporal y monitorear su comportamiento mediante métricas, logs y un dashboard visual.

---

# Tecnologías utilizadas

- FastAPI
- Python
- GitHub Models
- OpenAI SDK
- LangChain
- ChromaDB
- Sentence Transformers
- Pydantic
- Uvicorn
- Python Dotenv
- Streamlit
- Logging estándar de Python

---

# Arquitectura general

```text
Usuario
   │
   ▼
FastAPI (/ask, /metrics)
   │
   ▼
Agent Service
   │
   ├──────────────► search_memory()
   │                     │
   │                     ▼
   │               Memory Service
   │
   └──────────────► search_documents()
                         │
                         ▼
                     RAG Service
                         │
                         ▼
                     ChromaDB
                         │
                         ▼
                   Documentos PDF
```

---

# Arquitectura del agente

El sistema incorpora un agente simple basado en reglas.

El agente analiza la intención de la consulta y selecciona automáticamente la herramienta más adecuada.

## Herramientas disponibles

### `search_documents()`
Permite recuperar información semánticamente relevante desde ChromaDB mediante embeddings y búsqueda vectorial.

### `search_memory()`
Permite recuperar mensajes almacenados en memoria temporal para mantener continuidad conversacional.

---

# Flujo de funcionamiento

1. El usuario envía una pregunta.
2. FastAPI recibe la solicitud.
3. El agente analiza la consulta.
4. Dependiendo de la intención:
   - consulta memoria;
   - consulta documentos.
5. Se recupera información desde la base vectorial.
6. Se registran métricas y logs.
7. Se genera la respuesta.
8. La interacción se almacena en memoria.

---

# Memoria conversacional

El sistema incorpora una memoria temporal implementada en:

```text
app/services/memory_service.py
```

La memoria almacena los últimos mensajes intercambiados entre usuario y asistente.

## Objetivos

- Mantener contexto entre interacciones.
- Recuperar información previa.
- Demostrar continuidad conversacional.
- Apoyar la toma de decisiones del agente.

## Ejemplo

### Pregunta
```text
Mi nombre es Ignacio
```

### Posteriormente
```text
¿Qué dije antes?
```

### Respuesta
```text
Antes dijiste: Mi nombre es Ignacio
```

---

# Recuperación semántica (RAG)

SIAC utiliza una arquitectura RAG para responder preguntas basadas en documentos clínicos.

## Proceso

```text
Pregunta
   │
   ▼
Embeddings
   │
   ▼
Retriever
   │
   ▼
ChromaDB
   │
   ▼
Documentos relevantes
   │
   ▼
Respuesta
```

## Beneficios

- Reducción de alucinaciones.
- Respuestas basadas en evidencia documental.
- Reutilización de documentos clínicos existentes.
- Mayor precisión y trazabilidad de la información.

---

# Observabilidad y monitoreo

Durante la implementación se incorporó un módulo de observabilidad para medir el comportamiento del sistema.

## Métricas implementadas

El sistema expone métricas a través del endpoint:

```text
GET /metrics
```

Las métricas registradas son:

- total de consultas;
- consultas exitosas;
- cantidad de errores;
- latencia promedio.

## Ejemplo de respuesta

```json
{
  "total_requests": 1,
  "successful_requests": 1,
  "errors": 0,
  "average_latency": 10.17,
  "timestamp": "2026-07-05 10:33:32"
}
```

## Logs de ejecución

Los eventos del sistema se almacenan automáticamente en:

```text
logs/siac.log
```

Ejemplos registrados:

- pregunta recibida;
- respuesta generada correctamente;
- latencia de respuesta;
- errores detectados.

## Dashboard de observabilidad

Se implementó un dashboard en **Streamlit** para visualizar el estado general del sistema.

Archivo principal:

```text
dashboard.py
```

El dashboard permite observar:

- cantidad de consultas;
- consultas exitosas;
- errores;
- latencia promedio.

---

# Instalación

## 1. Clonar repositorio

```bash
git clone URL_DEL_REPOSITORIO
cd SIAC-RAG-2-main
```

## 2. Crear entorno virtual

```bash
python -m venv venv311
```

## 3. Activar entorno virtual

### Windows PowerShell

```powershell
.\venv311\Scripts\Activate.ps1
```

Si PowerShell bloquea la ejecución:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

# Variables de entorno

Crear un archivo llamado:

```text
.env
```

Ejemplo de configuración:

```env
GITHUB_TOKEN=TU_TOKEN
GITHUB_BASE_URL=https://models.github.ai/inference
MODEL_NAME=openai/gpt-4.1-mini
```

---

# Seguridad

Agregar al archivo `.gitignore`:

```gitignore
.env
venv/
venv311/
__pycache__/
logs/
chroma/
chroma_db/
```

Nunca subir credenciales al repositorio.

---

# Crear base vectorial

Procesar los documentos:

```bash
python create_db.py
```

Esto genera la colección vectorial utilizada por ChromaDB.

---

# Ejecutar la API

```bash
python -m uvicorn app.main:app --reload --port 8001
```

Servidor disponible en:

```text
http://127.0.0.1:8001
```

---

# Swagger UI

Abrir:

```text
http://127.0.0.1:8001/docs
```

---

# Dashboard de monitoreo

Ejecutar:

```bash
streamlit run dashboard.py
```

---

# Endpoints principales

## POST `/ask`

Ejemplo de solicitud:

```json
{
  "question": "¿Qué información existe sobre atención clínica?"
}
```

Ejemplo de respuesta:

```json
{
  "response": "Respuesta generada por el sistema."
}
```

## GET `/metrics`

Devuelve las métricas actuales del sistema en tiempo real.

---

# Ejemplos de uso

## Consulta documental

### Entrada
```json
{
  "question": "¿Qué información existe sobre atención clínica?"
}
```

### Acción ejecutada
```text
search_documents()
```

### Resultado
```text
Información recuperada desde ChromaDB.
```

---

## Consulta de memoria

### Entrada
```json
{
  "question": "¿Qué dije antes?"
}
```

### Acción ejecutada
```text
search_memory()
```

### Resultado
```text
Antes dijiste: Mi nombre es Ignacio
```

---

# Toma de decisiones del agente

El agente utiliza reglas para seleccionar herramientas según el contenido de la consulta.

```python
if any(word in lower_question for word in memory_keywords):
    response = search_memory()
else:
    response = search_documents(question)
```

Esto permite que el agente opere con autonomía básica y seleccione recursos según el contexto de la consulta.

---

# Estructura del proyecto

```text
SIAC-RAG-2-main/
│
├── app/
│   ├── api/
│   │   └── routes.py
│   ├── core/
│   │   ├── config.py
│   │   └── prompts.py
│   ├── data/
│   │   └── documentos/
│   ├── monitoring/
│   │   ├── metrics.py
│   │   └── logger.py
│   ├── models/
│   │   ├── question_model.py
│   │   └── response_model.py
│   └── services/
│       ├── agent_service.py
│       ├── memory_service.py
│       ├── tools_service.py
│       ├── rag_service.py
│       ├── vector_service.py
│       └── loader_service.py
│
├── chroma/
├── logs/
├── dashboard.py
├── create_db.py
├── .env
├── requirements.txt
├── README.md
└── app/main.py
```

---

# Funcionalidades

- Arquitectura RAG.
- Recuperación semántica.
- ChromaDB.
- Embeddings.
- Memoria conversacional.
- Agente con toma de decisiones.
- Observabilidad mediante métricas.
- Logs persistentes.
- Dashboard de monitoreo.
- Swagger UI.
- FastAPI.
- Separación modular por servicios.
- Configuración mediante variables de entorno.

---

# Justificación de componentes

### FastAPI
Permite construir APIs modernas, rápidas y fácilmente documentables mediante Swagger.

### ChromaDB
Facilita el almacenamiento y recuperación eficiente de embeddings para búsqueda semántica.

### Arquitectura RAG
Permite responder utilizando información documental real, reduciendo respuestas inventadas.

### Memoria conversacional
Permite mantener continuidad entre interacciones y recuperar información previa del usuario.

### Agente
Permite seleccionar dinámicamente la herramienta más adecuada según la intención detectada.

### Observabilidad
Permite medir el rendimiento del sistema, detectar errores y visualizar métricas operativas.

---

# Consideraciones académicas

Este proyecto fue desarrollado con fines académicos para demostrar:

- agentes inteligentes;
- recuperación semántica;
- memoria conversacional;
- toma de decisiones;
- integración de herramientas;
- observabilidad;
- arquitecturas RAG.

El sistema no reemplaza criterio clínico profesional ni realiza diagnósticos médicos.

---

# Autor

Proyecto académico SIAC.
