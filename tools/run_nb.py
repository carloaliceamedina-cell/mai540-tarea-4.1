"""Ejecutor mínimo de notebooks (sin Jupyter): ejecuta las celdas de código en
un namespace compartido y guarda stdout / errores / figuras como outputs.
Uso: python tools/run_nb.py entrada.ipynb [salida.ipynb]
"""
import sys, json, io, base64, traceback, contextlib, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

src = sys.argv[1]
dst = os.path.abspath(sys.argv[2] if len(sys.argv) > 2 else src)
nb = json.load(open(src, encoding="utf-8"))
os.chdir(os.path.dirname(os.path.abspath(src)) or ".")
ns = {"__name__": "__main__", "display": print}
count = 0
for cell in nb["cells"]:
    if cell["cell_type"] != "code":
        continue
    count += 1
    code = "".join(cell["source"]) if isinstance(cell["source"], list) else cell["source"]
    code = "\n".join(l for l in code.splitlines() if not l.strip().startswith(("!", "%")))
    buf = io.StringIO(); outputs = []; outputs_val = None
    try:
        import ast
        tree = ast.parse(code)
        last = tree.body.pop() if tree.body and isinstance(tree.body[-1], ast.Expr) else None
        with contextlib.redirect_stdout(buf):
            exec(compile(tree, f"<celda {count}>", "exec"), ns)
            val = eval(compile(ast.Expression(last.value), f"<celda {count}>", "eval"), ns) if last else None
        if val is not None and not hasattr(val, "figure") and not isinstance(val, list):
            outputs_val = {"output_type": "execute_result", "execution_count": count, "metadata": {},
                           "data": {"text/plain": repr(val)}}
        else:
            outputs_val = None
        err = None
    except Exception as e:
        err = e
    if buf.getvalue():
        outputs.append({"output_type": "stream", "name": "stdout", "text": buf.getvalue()})
    for num in plt.get_fignums():
        b = io.BytesIO(); plt.figure(num).savefig(b, format="png", bbox_inches="tight", dpi=90)
        outputs.append({"output_type": "display_data", "metadata": {},
                        "data": {"image/png": base64.b64encode(b.getvalue()).decode()}})
    plt.close("all")
    if err is None and outputs_val:
        outputs.append(outputs_val)
    if err is not None:
        tb = traceback.format_exception(type(err), err, err.__traceback__)
        outputs.append({"output_type": "error", "ename": type(err).__name__,
                        "evalue": str(err), "traceback": tb[-3:]})
        print(f"[celda {count}] ERROR {type(err).__name__}: {err}")
    cell["outputs"] = outputs; cell["execution_count"] = count
json.dump(nb, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"OK: {count} celdas de código ejecutadas -> {dst}")
