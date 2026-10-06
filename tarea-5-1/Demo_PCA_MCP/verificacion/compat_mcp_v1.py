"""SOLO para el entorno de verificación de Claude (mcp 1.27 instalado, sin acceso a PyPI).
En mcp >= 2.0 (requirements.txt) NO se necesita: alli existe mcp.server.mcpserver.
Registra un alias del API 2.0 sobre FastMCP (1.x, mismos decoradores) y ejecuta el servidor sin modificarlo."""
import runpy, sys, types
try:
    import mcp.server.mcpserver  # noqa: F401  (mcp >= 2.0: no hace falta nada)
except ModuleNotFoundError:
    from mcp.server.fastmcp import FastMCP
    from mcp.server.fastmcp.prompts.base import UserMessage
    alias = types.ModuleType("mcp.server.mcpserver")
    alias.MCPServer, alias.UserMessage = FastMCP, UserMessage
    sys.modules["mcp.server.mcpserver"] = alias
sys.argv = sys.argv[1:]
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(sys.argv[0])))
runpy.run_path(sys.argv[0], run_name="__main__")
