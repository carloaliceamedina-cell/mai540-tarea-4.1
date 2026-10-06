"""
Servidor MCP: dos tools, dos resources, un prompt.

Este es el archivo que el profesor completa en vivo durante la Clase 5.1,
siguiendo el mismo patrón del curso de Anthropic "Introduction to Model
Context Protocol" (M02), adaptado de un chatbot de documentos a un
servidor de análisis de datos.

Tools    -> operaciones que Claude puede decidir ejecutar (cargar un dataset,
            correr PCA).
Resources -> datos que el cliente puede pedir directamente, sin pasar por
            una decisión de Claude (la lista de datasets, la ficha de uno).
Prompt   -> una plantilla ya evaluada para una tarea recurrente: interpretar
            componentes principales en términos del dominio, no solo en
            términos de varianza.

ESTADO: COMPLETO (Tarea 5.1). Las 5 piezas están implementadas debajo de su TODO.
Cada bloque "# TODO" de abajo es una pieza que se escribe en vivo durante la
clase, siguiendo el patrón de @mcp.tool / @mcp.resource / @mcp.prompt que ya
viste en las diapositivas 10, 11 y 12. La lógica de negocio (pca_utils.py) ya
está completa — aquí solo falta envolverla con el decorador correcto.

Para probar este archivo una vez completado, sin cliente ni CLI:
    mcp dev mcp_server.py
Abre el Inspector en el navegador, conecta, y prueba cada tool/resource/prompt
a mano antes de conectarlo a nada más.
"""

from mcp.server.mcpserver import MCPServer, UserMessage
from pydantic import Field

import pca_utils

mcp = MCPServer("analisis-datos")


# ---------------------------------------------------------------------------
# Tools — algo que Claude DECIDE ejecutar, con los argumentos que el modelo
# elige según lo que pida quien está conversando.
# ---------------------------------------------------------------------------

# TODO 1 — tool "cargar_dataset"
#   Decorador:   @mcp.tool(name="cargar_dataset", description="...")
#   Función:     cargar_dataset(nombre: str = Field(...)) -> dict
#   Cuerpo:      return pca_utils.describir_dataset(nombre)
#   La descripción debe explicar que esta tool se usa ANTES de ejecutar_pca,
#   para que Claude sepa qué columnas numéricas tiene el dataset.
@mcp.tool(
    name="cargar_dataset",
    description=(
        "Carga un dataset de la carpeta datasets/ y devuelve su ficha: número de "
        "filas, columnas numéricas y columnas categóricas. Úsala ANTES de "
        "ejecutar_pca para saber qué columnas numéricas tiene el dataset y cuántos "
        "componentes como máximo se pueden pedir."
    ),
)
def cargar_dataset(
    nombre: str = Field(description="Nombre del dataset sin extensión .csv, por ejemplo 'iris' o 'wine'."),
) -> dict:
    return pca_utils.describir_dataset(nombre)


# TODO 2 — tool "ejecutar_pca"
#   Decorador:   @mcp.tool(name="ejecutar_pca", description="...")
#   Función:     ejecutar_pca(nombre: str = Field(...),
#                              n_componentes: int = Field(...)) -> dict
#   Cuerpo:      return pca_utils.ejecutar_pca(nombre, n_componentes)
#   La descripción debe mencionar que devuelve varianza explicada, varianza
#   acumulada y las cargas (loadings) de cada variable original.
@mcp.tool(
    name="ejecutar_pca",
    description=(
        "Ejecuta PCA (con estandarización previa) sobre las columnas numéricas de un "
        "dataset. Devuelve la varianza explicada por cada componente, la varianza "
        "acumulada y las cargas (loadings) de cada variable original en cada "
        "componente. n_componentes debe estar entre 1 y el número de columnas "
        "numéricas (consúltalo antes con cargar_dataset)."
    ),
)
def ejecutar_pca(
    nombre: str = Field(description="Nombre del dataset sin extensión .csv."),
    n_componentes: int = Field(description="Número de componentes principales a calcular (entero >= 1)."),
) -> dict:
    return pca_utils.ejecutar_pca(nombre, n_componentes)


# ---------------------------------------------------------------------------
# Resources — datos que el CLIENTE pide directamente, sin que Claude decida
# nada. Estático (siempre lo mismo) o con plantilla (un parámetro en la URI).
# ---------------------------------------------------------------------------

# TODO 3 — resource estático "data://datasets"
#   Decorador:   @mcp.resource("data://datasets", mime_type="application/json")
#   Función:     listar_datasets() -> list[str]
#   Cuerpo:      return pca_utils.listar_datasets()
@mcp.resource("data://datasets", mime_type="application/json")
def listar_datasets() -> list[str]:
    return pca_utils.listar_datasets()


# TODO 4 — resource con plantilla "data://datasets/{nombre}"
#   Decorador:   @mcp.resource("data://datasets/{nombre}", mime_type="application/json")
#   Función:     ficha_dataset(nombre: str) -> dict
#   Cuerpo:      return pca_utils.describir_dataset(nombre)
#   El framework extrae automáticamente lo que haya entre {llaves} en la URI
#   que pida el cliente y lo pasa como argumento "nombre".
@mcp.resource("data://datasets/{nombre}", mime_type="application/json")
def ficha_dataset(nombre: str) -> dict:
    return pca_utils.describir_dataset(nombre)


# ---------------------------------------------------------------------------
# Prompt — una plantilla YA EVALUADA para una tarea que se repite, en vez de
# dejar que cada usuario improvise su propia pregunta de interpretación.
# ---------------------------------------------------------------------------

# TODO 5 — prompt "interpretar_componentes"
#   Decorador:   @mcp.prompt(name="interpretar_componentes", description="...")
#   Función:     interpretar_componentes(nombre: str = Field(...),
#                                         n_componentes: int = Field(...)
#                                         ) -> list[UserMessage]
#   Cuerpo:      construir un f-string "prompt" que le pida a Claude, sobre el
#                resultado de ejecutar_pca:
#                  1. identificar las 2-3 variables con mayor carga por componente
#                  2. explicar qué patrón de dominio podría representar cada una
#                  3. indicar si el signo de la carga tiene una lectura razonable
#                y terminar preguntando si n_componentes alcanza según la
#                varianza acumulada.
#   Devolver:    return [UserMessage(prompt)]
#   Ver el texto exacto sugerido en la diapositiva 12.
@mcp.prompt(
    name="interpretar_componentes",
    description=(
        "Plantilla evaluada para interpretar los componentes principales de un "
        "dataset en términos del dominio, no solo de la varianza."
    ),
)
def interpretar_componentes(
    nombre: str = Field(description="Nombre del dataset sobre el que se ejecutó (o se ejecutará) PCA."),
    n_componentes: int = Field(description="Número de componentes a interpretar."),
) -> list[UserMessage]:
    prompt = f"""Usa la tool ejecutar_pca sobre el dataset "{nombre}" con {n_componentes} componentes y, con ese resultado:

1. Para cada componente, identifica las 2-3 variables originales con mayor carga en valor absoluto.
2. Explica qué patrón del dominio de "{nombre}" podría representar cada componente según esas variables (no te limites a decir cuánta varianza captura).
3. Indica si el signo de las cargas tiene una lectura razonable: qué significa que una variable cargue en positivo y otra en negativo dentro del mismo componente.

Termina respondiendo: según la varianza acumulada, ¿alcanzan {n_componentes} componentes para resumir el dataset, o harían falta más?"""
    return [UserMessage(prompt)]


if __name__ == "__main__":
    mcp.run(transport="stdio")
