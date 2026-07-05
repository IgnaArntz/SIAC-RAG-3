# SIAC - Sistema Inteligente de Asistencia Clínica

SIAC es un asistente clínico virtual académico desarrollado con **FastAPI** y una arquitectura híbrida basada en **RAG (Retrieval-Augmented Generation)** y un **agente con memoria conversacional**.

El sistema permite responder preguntas relacionadas con documentos clínicos almacenados en una base vectorial **ChromaDB**, además de mantener contexto básico de la conversación mediante memoria temporal.

---

# Tecnologías utilizadas

* FastAPI
* Python
* GitHub Models
* OpenAI SDK
* LangChain
* ChromaDB
* Sentence Transformers
* Pydantic
* Uvicorn
* Python Dotenv

---

# Arquitectura General

```text
Usuario
   │
   ▼
FastAPI (/ask)
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
                     ChromaDB
                         │
                         ▼
                   Documentos PDF
```

---

# Arquitectura del Agente

El sistema incorpora un agente simple basado en reglas.

El agente analiza la intención de la consulta y selecciona automáticamente la herramienta más adecuada.

Herramientas disponibles:

### search_documents()

Permite recuperar información semánticamente relevante desde ChromaDB mediante embeddings y búsqueda vectorial.

### search_memory()

Permite recuperar mensajes almacenados en memoria temporal para mantener continuidad conversacional.

---

# Flujo de funcionamiento

1. El usuario envía una pregunta.
2. FastAPI recibe la solicitud.
3. El agente analiza la consulta.
4. Dependiendo de la intención:

   * consulta memoria;
   * consulta documentos.
5. Se genera la respuesta.
6. La interacción se almacena en memoria.

---

# Memoria Conversacional

El sistema incorpora una memoria temporal implementada mediante:

```text
app/services/memory_service.py
```

La memoria almacena los últimos mensajes intercambiados entre usuario y asistente.

Objetivos:

* mantener contexto;
* recuperar información previa;
* demostrar continuidad conversacional;
* apoyar la toma de decisiones del agente.

Ejemplo:

Pregunta:

```text
Mi nombre es Ignacio
```

Posteriormente:

```text
¿Qué dije antes?
```

Respuesta:

```text
Antes dijiste: Mi nombre es Ignacio
```

---

# Recuperación Semántica (RAG)

El sistema utiliza una arquitectura RAG para responder preguntas basadas en documentos clínicos.

Proceso:

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

Beneficios:

* reducción de alucinaciones;
* respuestas basadas en evidencia documental;
* reutilización de documentos clínicos existentes.

---

# Instalación

## 1. Clonar repositorio

```bash
git clone URL_DEL_REPOSITORIO
cd SIAC-RAG
```

---

## 2. Crear entorno virtual

```bash
python -m venv venv311
```

---

## 3. Activar entorno virtual

Windows PowerShell:

```powershell
.\venv311\Scripts\Activate.ps1
```

Si PowerShell bloquea la ejecución:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

# Variables de Entorno

Crear un archivo:

```text
.env
```

Ejemplo:

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
```

Nunca subir credenciales al repositorio.

---

# Crear Base Vectorial

Procesar documentos:

```bash
python create_db.py
```

Esto genera la colección vectorial utilizada por ChromaDB.

---

# Ejecutar la API

```bash
python -m uvicorn app.main:app --reload --port 8001
```

Servidor:

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

# Endpoint Principal

## POST /ask

Ejemplo:

```json
{
  "question": "¿Qué información existe sobre atención clínica?"
}
```

Respuesta:

```json
{
  "response": "Respuesta generada por el sistema."
}
```

---

# Ejemplos de Uso

## Consulta documental

Entrada:

```json
{
  "question": "¿Qué información existe sobre atención clínica?"
}
```

Acción ejecutada:

```text
search_documents()
```

Resultado:

```text
Información recuperada desde ChromaDB.
```

---

## Consulta de memoria

Entrada:

```json
{
  "question": "¿Qué dije antes?"
}
```

Acción ejecutada:

```text
search_memory()
```

Resultado:

```text
Antes dijiste: Mi nombre es Ignacio
```

---

# Toma de Decisiones del Agente

El agente utiliza reglas para seleccionar herramientas.

Ejemplo:

```python
if any(word in lower_question for word in memory_keywords):
    response = search_memory()
else:
    response = search_documents(question)
```

Esto permite que el agente opere con autonomía básica y seleccione recursos según el contexto de la consulta.

---

# Estructura del Proyecto

```text
SIAC-RAG/
│
├── app/
│
├── api/
│   └── routes.py
│
├── services/
│   ├── agent_service.py
│   ├── memory_service.py
│   ├── tools_service.py
│   ├── rag_service.py
│   ├── vector_service.py
│   └── loader_service.py
│
├── chroma/
│
├── .env
├── requirements.txt
├── README.md
└── main.py
```

---

# Funcionalidades

* Arquitectura RAG.
* Recuperación semántica.
* ChromaDB.
* Embeddings.
* Memoria conversacional.
* Agente con toma de decisiones.
* Integración con GitHub Models.
* Swagger UI.
* FastAPI.
* Separación modular por servicios.
* Configuración mediante variables de entorno.

---

# Justificación de Componentes

### FastAPI

Permite construir APIs modernas, rápidas y fácilmente documentables mediante Swagger.

### ChromaDB

Facilita el almacenamiento y recuperación eficiente de embeddings para búsqueda semántica.

### Arquitectura RAG

Permite responder utilizando información documental real, reduciendo respuestas inventadas.

### Memoria Conversacional

Permite mantener continuidad entre interacciones y recuperar información previa del usuario.

### Agente

Permite seleccionar dinámicamente la herramienta más adecuada según la intención detectada.

---

# Consideraciones Académicas

Este proyecto fue desarrollado con fines académicos para demostrar:

* agentes inteligentes;
* recuperación semántica;
* memoria conversacional;
* toma de decisiones;
* integración de herramientas;
* arquitecturas RAG.

El sistema no reemplaza criterio clínico profesional ni realiza diagnósticos médicos.

---

# Autor

Proyecto académico SIAC.

# SIAC-RAG-3
