from pathlib import Path
import ast

path = Path("app.py")
source = path.read_text(encoding="utf-8-sig")
tree = ast.parse(source)

cards_node = None

for node in tree.body:
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "cards":
                cards_node = node
                break

if cards_node is None:
    raise RuntimeError("No se encontró la lista cards.")

obso_nodes = []

for element in cards_node.value.elts:
    if isinstance(element, ast.Dict):
        titulo = None

        for k, v in zip(element.keys, element.values):
            if (
                isinstance(k, ast.Constant)
                and k.value == "titulo"
                and isinstance(v, ast.Constant)
            ):
                titulo = v.value

        if titulo == "Obsolescencia de Activos":
            obso_nodes.append(element)

print("Tarjetas de Obsolescencia encontradas:", len(obso_nodes))

if len(obso_nodes) <= 1:
    print("No hay duplicado.")
else:
    lines = source.splitlines(True)

    # Eliminar todas las copias excepto la primera.
    for node in reversed(obso_nodes[1:]):
        inicio = node.lineno - 1
        fin = node.end_lineno
        del lines[inicio:fin]

    path.write_text("".join(lines), encoding="utf-8")

    print("Duplicados eliminados.")
    print("Se conserva una sola tarjeta de Obsolescencia.")
