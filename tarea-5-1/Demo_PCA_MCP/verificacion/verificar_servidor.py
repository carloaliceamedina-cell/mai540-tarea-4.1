"""Verificación de las 5 piezas de mcp_server.py a través del protocolo MCP real (stdio),
usando el mismo mcp_client.py del proyecto. Equivale a probar cada pieza a mano en el
MCP Inspector, pero deja un log reproducible.

Uso (desde la carpeta del proyecto):
    python verificacion/verificar_servidor.py            # mcp >= 2.0
    python verificacion/verificar_servidor.py --compat   # solo si tienes mcp 1.x
"""
import asyncio, json, sys
from datetime import datetime
from pathlib import Path

PROYECTO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROYECTO))
from mcp_client import MCPClient  # noqa: E402


async def leer_recurso(s, uri):
    """Lee un resource por el protocolo. (mcp_client.read_resource usa el atributo `mime_type`
    del SDK 2.0; aquí se acepta también `mimeType` del SDK 1.x para que el script sirva en ambos.)"""
    r = (await s.read_resource(uri)).contents[0]
    mime = getattr(r, "mime_type", None) or getattr(r, "mimeType", None)
    return {"uri": uri, "mimeType": mime, "contenido": json.loads(r.text) if mime == "application/json" else r.text}


def bloque(titulo, contenido):
    print(f"\n=== {titulo} ===")
    print(contenido if isinstance(contenido, str) else json.dumps(contenido, ensure_ascii=False, indent=2))


async def main():
    args = ["verificacion/compat_mcp_v1.py", "mcp_server.py"] if "--compat" in sys.argv else ["mcp_server.py"]
    print(f"Verificación del servidor MCP 'analisis-datos' — {datetime.now():%Y-%m-%d %H:%M}")
    async with MCPClient(command=sys.executable, args=args, cwd=str(PROYECTO)) as c:
        s = c.session()
        tools = await c.list_tools()
        bloque("Descubrimiento: tools", [{"name": t.name, "inputSchema": t.inputSchema} for t in tools])
        recursos = await c.list_resources()
        plantillas = (await s.list_resource_templates()).resourceTemplates
        bloque("Descubrimiento: resources", [str(r.uri) for r in recursos] + [t.uriTemplate for t in plantillas])
        prompts = await c.list_prompts()
        bloque("Descubrimiento: prompts", [{"name": p.name, "arguments": [a.name for a in (p.arguments or [])]} for p in prompts])

        r = await c.call_tool("cargar_dataset", {"nombre": "iris"})
        bloque("PIEZA 1 — tool cargar_dataset(nombre='iris')", json.loads(r.content[0].text))
        r = await c.call_tool("ejecutar_pca", {"nombre": "iris", "n_componentes": 2})
        bloque("PIEZA 2 — tool ejecutar_pca(nombre='iris', n_componentes=2)", json.loads(r.content[0].text))
        bloque("PIEZA 3 — resource data://datasets", await leer_recurso(s, "data://datasets"))
        bloque("PIEZA 4 — resource data://datasets/{nombre} con nombre='wine'", await leer_recurso(s, "data://datasets/wine"))
        msgs = await c.get_prompt("interpretar_componentes", {"nombre": "iris", "n_componentes": "2"})
        bloque("PIEZA 5 — prompt interpretar_componentes(nombre='iris', n_componentes=2)",
               f"role={msgs[0].role}\n{msgs[0].content.text}")

        r = await c.call_tool("segmentar_kmeans", {"nombre": "wine", "k": 3})
        res = json.loads(r.content[0].text)
        res["etiquetas"] = f"{len(res['etiquetas'])} etiquetas; primeras 15: {res['etiquetas'][:15]}"
        bloque("TAREA 5.2 — tool segmentar_kmeans(nombre='wine', k=3)", res)

        print("\n=== CASOS LÍMITE (permisos y errores) ===")
        casos = [("ejecutar_pca", {"nombre": "iris", "n_componentes": 9}),
                 ("cargar_dataset", {"nombre": "no_existe"}),
                 ("cargar_dataset", {"nombre": "../verificacion/secreto_fuera"}),
                 ("cargar_dataset", {"nombre": "C:/Windows/secreto"}),
                 ("segmentar_kmeans", {"nombre": "wine", "k": 1}),
                 ("segmentar_kmeans", {"nombre": "../verificacion/secreto_fuera", "k": 2})]
        for tool, a in casos:
            r = await c.call_tool(tool, a)
            texto = r.content[0].text if r.content else ""
            print(f"- {tool}({a}) -> isError={r.isError}: {texto[:160]}")


if __name__ == "__main__":
    asyncio.run(main())
