# Demo Clase 5.1 — Servidor MCP para PCA

Adaptado del curso de Anthropic *Introduction to Model Context Protocol* (M01–M03):
mismo patrón (servidor con tools, resources y un prompt; cliente que se conecta a
él; un chatbot de CLI que los usa), pero en vez de un chatbot de documentos, es un
servidor de análisis de datos que expone PCA.

## Qué construye este proyecto

Un CLI que conversa con Claude y, cuando hace falta, usa un servidor MCP propio
(`mcp_server.py`) para cargar datasets y ejecutar PCA. Servidor y cliente corren
en el mismo proceso de desarrollo — en un proyecto real normalmente se hace solo
uno de los dos (ver la nota del video de *Project Setup* del curso original).

| Pieza | Qué hace | Se completa en clase o ya viene lista |
|---|---|---|
| `pca_utils.py` | La lógica de PCA en sí, sin nada de MCP | Ya viene lista |
| `mcp_server.py` | Envuelve `pca_utils.py` con tools, resources y un prompt | **Se completa en vivo en la Clase 5.1** |
| `mcp_client.py` | La conexión hacia el servidor (gestión de sesión) | Ya viene lista |
| `chat.py` | El lazo de conversación con la API de Claude | Ya viene lista |
| `main.py` | El CLI: entrada de usuario, atajos `@dataset` y `/interpretar` | Ya viene lista |

## Instalación

Requiere Python 3.10+. Esto es lo único que hace falta para la Tarea 5.1 — no
necesitas ninguna clave de API para instalar ni para probar el servidor.

```bash
pip install -r requirements.txt
```

## Probar el servidor solo, sin cliente ni CLI

Esto es lo primero que hay que hacer siempre que se toca `mcp_server.py` — antes
de conectar nada, confirmar que el servidor responde bien. **Esta es la evidencia
que pide la Tarea 5.1, y no requiere `ANTHROPIC_API_KEY` ni ningún pago:**

```bash
mcp dev mcp_server.py
```

Abre la URL que imprime en el navegador, conecta, y prueba a mano:
- **Tools** → `cargar_dataset` con `nombre="iris"`, luego `ejecutar_pca` con
  `nombre="iris"` y `n_componentes=2`.
- **Resources** → `data://datasets` (lista completa), y el template
  `data://datasets/{nombre}` con `nombre="wine"`.
- **Prompts** → `interpretar_componentes` con `nombre="iris"`, `n_componentes=2`.

## Conectar con Claude Desktop (gratis)

Si quieres ver a Claude decidiendo usar tus tools en una conversación real —no
solo probándolas a mano en el Inspector— sin pagar nada: Claude Desktop (la
app, no el navegador) se conecta a servidores MCP locales usando tu cuenta
normal de claude.ai, sin clave de API y sin cobro por token. Esto es opcional,
no se evalúa en la tarea.

1. Instala Claude Desktop desde `claude.ai/download` si no la tienes.
2. Abre Claude Desktop → Settings → Developer → Edit Config. Esto abre (o crea)
   `claude_desktop_config.json`.
3. Agrega una entrada con **rutas absolutas** a este proyecto:

```json
{
  "mcpServers": {
    "analisis-datos": {
      "command": "/ruta/completa/a/este/proyecto/.venv/bin/python",
      "args": ["/ruta/completa/a/este/proyecto/mcp_server.py"]
    }
  }
}
```

   En Windows, usa `.venv/Scripts/python.exe` y rutas con `C:/...` (con
   barras `/`, aunque sea Windows, para que el JSON no se rompa). Obtén la
   ruta completa con `pwd` (Mac) o `cd` sin argumentos (Windows) dentro de la
   terminal del proyecto.
4. Guarda el archivo y reinicia Claude Desktop por completo.
5. Debe aparecer un ícono de herramienta en el cuadro de chat — ábrelo para
   confirmar que ve `cargar_dataset` y `ejecutar_pca`.
6. Chatea normal: "ejecuta PCA sobre iris con 2 componentes y dime qué
   representa cada uno" — Claude decide usar la tool por su cuenta.

## Correr el CLI completo (opcional, requiere clave de pago)

Esta sección es una alternativa al Claude Desktop de arriba, usando el
cliente propio del proyecto en vez de la app. Requiere crear una clave en
`console.anthropic.com` (de pago, aparte de una suscripción de claude.ai) y
pegarla en un archivo `.env`:

```bash
cp .env.example .env
# Edita .env y pon tu ANTHROPIC_API_KEY
python main.py
```

Ejemplos de uso una vez conectado:

```
> ¿qué columnas numéricas tiene wine?
> ejecuta PCA sobre iris con 2 componentes y dime qué representa cada uno
> ¿qué columnas tiene @iris?
> /interpretar wine 3
```

## Los tres conceptos, en este proyecto

- **Tool** — algo que *Claude decide* ejecutar. `ejecutar_pca` es una tool porque
  Claude necesita decidir con cuántos componentes correrlo según lo que pida el
  usuario.
- **Resource** — algo que el *cliente pide directamente*, sin pasar por una
  decisión de Claude. `data://datasets` es estático (siempre la misma lista);
  `data://datasets/{nombre}` es con plantilla (un parámetro en la URI).
- **Prompt** — una plantilla ya redactada y evaluada para una tarea que se repite.
  `interpretar_componentes` existe porque "interpreta esto" a secas da resultados
  mediocres; un prompt específico que pide identificar variables dominantes,
  explicar el patrón y evaluar si el número de componentes alcanza, da resultados
  consistentemente mejores.

## Para la tarea (K-Means)

El patrón es el mismo. En lugar de completar `mcp_server.py`, en la tarea:

1. Agregas la lógica de K-Means a un archivo tipo `kmeans_utils.py` (equivalente
   a `pca_utils.py`): una función que cargue un dataset y otra que corra K-Means
   con un número de grupos dado y devuelva las etiquetas, el criterio usado para
   elegir *k*, y algún resumen por grupo.
2. Envuelves esas funciones con `@mcp.tool(...)` en tu propio servidor.
3. Reutilizas `mcp_client.py`, `chat.py` y `main.py` tal cual están aquí — no
   hace falta tocarlos.
4. Escribes tu propio prompt, por ejemplo `interpretar_grupos`, que le pida a
   Claude describir cada grupo en términos del dominio del dataset que elijas
   para tu sector profesional, no solo en términos del centroide.

## Datasets incluidos

`datasets/iris.csv` (150 filas, 4 numéricas) y `datasets/wine.csv` (178 filas,
13 numéricas) — ambos de scikit-learn, generados con `sklearn.datasets`. Puedes
agregar cualquier otro CSV a esa carpeta; `pca_utils.py` no tiene nada
hardcodeado sobre estos dos en particular.

---

## Tarea 5.1 — Estado y verificación (Carlo E. Alicea Medina)

**Las 5 piezas de `mcp_server.py` están completas**, cada una en su propio commit: `cargar_dataset`, `ejecutar_pca`, `data://datasets`, `data://datasets/{nombre}` e `interpretar_componentes`.

### Evidencia
- `evidencia/log_verificacion_final.txt` — resultado de cada una de las 5 piezas, llamadas **por el protocolo MCP real (stdio)** con el `mcp_client.py` del proyecto, más casos límite.
- `evidencia/log_verificacion_1_antes_de_corregir_ruta.txt` — la misma verificación antes de la corrección de seguridad: muestra que `cargar_dataset("../verificacion/secreto_fuera")` **leía un CSV fuera de `datasets/`**.
- Para repetirla: `python verificacion/verificar_servidor.py` (con mcp ≥ 2.0). Con mcp 1.x instalado, agrega `--compat`: un alias temporal del API 2.0, solo para verificar, que no modifica el servidor.
- En el Inspector (`mcp dev mcp_server.py`), las mismas 5 pruebas: `cargar_dataset` con `iris`; `ejecutar_pca` con `iris` y `2`; `data://datasets`; `data://datasets/wine`; `interpretar_componentes` con `iris` y `2`.

### Permisos (mínimos necesarios)
| Puede | No puede |
|---|---|
| Listar los `.csv` de `datasets/` | Leer cualquier archivo fuera de `datasets/` (corregido en `pca_utils._ruta_dataset`: solo nombres de la lista blanca `listar_datasets()`) |
| Leer **un** CSV de `datasets/` y devolver su ficha (filas y nombres de columnas) | Devolver filas crudas: `ejecutar_pca` solo devuelve agregados (varianzas y cargas) |
| Ejecutar PCA en memoria | Escribir, borrar o modificar archivos |
| Responder por stdio al proceso cliente que lo lanzó | Acceder a internet o abrir puertos de red (transporte `stdio`, sin HTTP) |
| — | Leer variables de entorno o `.env` (la `ANTHROPIC_API_KEY` la usa `chat.py`, nunca el servidor) |

---

## Tarea 5.2 — Segmentación con K-Means (mismo servidor)

- **`kmeans_utils.py`**: `cargar_y_escalar(nombre)` y `ejecutar_kmeans(nombre, k)`, que devuelve etiquetas, tamaños, inercia, silueta y perfil medio por grupo. También `evaluar_k(nombre)`, que calcula el codo y la silueta de k = 2 a 8. Reutiliza la validación de nombres de `pca_utils`, así que hereda el mismo permiso mínimo.
- **Tool `segmentar_kmeans(nombre, k)`** en `mcp_server.py`. Verificada por el protocolo en `evidencia/log_verificacion_tarea_5_2.txt`: wine con k = 3 da grupos de 65, 51 y 62 y silueta de 0.285. Se probaron además los casos límite k = 1 y una ruta fuera de `datasets/`.
- **Elección de k**: `segmentacion/eleccion_k.png` y `segmentacion/eleccion_k.csv`. Se eligió k = 3: el codo está ahí (−381 de inercia al pasar de 2 a 3, contra −103 de 3 a 4) y la silueta es máxima (0.285).
- **PCA en 2D**: `segmentacion/pca_kmeans_2d.png`, que usa `pca_utils.ejecutar_pca` de la Tarea 5.1. Conserva el **55.4 %** de la varianza (36.2 % + 19.2 %).
- **Reproducir**: `python segmentacion/analisis_segmentacion.py`
- **Documentos**: `docs/Tarea_5_2_Segmentacion_Interpretacion.pdf` (interpretación de cada grupo y acción propuesta) y `docs/Tarea_5_2_Propuesta_Capstone.pdf`.
