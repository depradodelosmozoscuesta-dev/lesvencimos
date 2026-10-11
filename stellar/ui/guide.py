"""Guía paso a paso (render de texto; en una UI real se pinta como overlay)."""


def render_guide(repo, node_id, buffer_len=0):
    node = repo.node(node_id)
    lines = [f"[{node['label']}]", node["hint"] or "Apunta a una estrella"]
    cands = repo.candidates(node_id)
    if cands:
        lines.append("Candidatas: " + ", ".join(f"{c['name']} ({c['constel']})" for c in cands))
    lines.append(f"Pasos: {buffer_len}")
    return "\n".join(lines)
