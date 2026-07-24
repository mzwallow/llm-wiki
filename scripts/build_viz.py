#!/usr/bin/env python3
import json
import re
from pathlib import Path

WIKI_DIR = Path(__file__).parent.parent / "wiki"
OUTPUT_HTML = Path(__file__).parent.parent / "viz.html"

COLOR_MAP = {
    "Concept": "#3b82f6",
    "Tool": "#10b981",
    "System": "#8b5cf6",
    "Architecture": "#f59e0b",
    "Guide": "#ec4899",
    "Default": "#64748b"
}

def parse_frontmatter(content):
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            fm_text = parts[1]
            body = parts[2]
            meta = {}
            for line in fm_text.splitlines():
                if ":" in line and not line.strip().startswith("#"):
                    k, v = line.split(":", 1)
                    k = k.strip()
                    v = v.strip().strip('"\'')
                    if v.startswith("[") and v.endswith("]"):
                        v = [x.strip().strip('"\'') for x in v[1:-1].split(",") if x.strip()]
                    meta[k] = v
            return meta, body
    return {}, content

def extract_title_and_links(body, default_title):
    title = default_title
    for line in body.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            break

    # Extract [[wikilink]] and standard markdown links
    wiki_links = set(re.findall(r"\[\[([^\]\|]+)(?:\|[^\]]+)?\]\]", body))
    md_links = set(re.findall(r"\[[^\]]+\]\(([a-zA-Z0-9_\-]+\.md)\)", body))

    targets = set()
    for link in wiki_links:
        targets.add(link.strip().replace(".md", ""))
    for link in md_links:
        targets.add(link.strip().replace(".md", ""))

    return title, list(targets)

def main():
    nodes = []
    edges = []
    file_map = {}

    if not WIKI_DIR.exists():
        print(f"Directory {WIKI_DIR} not found.")
        return

    md_files = list(WIKI_DIR.glob("*.md"))

    for filepath in md_files:
        rel_id = filepath.stem
        content = filepath.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(content)
        title, links = extract_title_and_links(body, rel_id.replace("-", " ").title())

        node_type = meta.get("type", "Concept")
        color = COLOR_MAP.get(node_type, COLOR_MAP["Default"])

        file_map[rel_id] = {
            "id": rel_id,
            "label": meta.get("title", title),
            "type": node_type,
            "status": meta.get("status", "stable"),
            "color": color,
            "size": 30 + len(links) * 2,
            "description": meta.get("description", f"Wiki page for {title}"),
            "tags": meta.get("tags", []),
            "links": links,
            "body": body[:500] + "..." if len(body) > 500 else body
        }

    for src_id, data in file_map.items():
        nodes.append({"data": data})
        for target in data["links"]:
            if target in file_map:
                edges.append({
                    "data": {
                        "id": f"{src_id}->{target}",
                        "source": src_id,
                        "target": target
                    }
                })

    bundle_json = json.dumps({"nodes": nodes, "edges": edges}, indent=2)

    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>LLM Wiki Visualizer</title>
<script src="https://cdn.jsdelivr.net/npm/cytoscape@3.28.1/dist/cytoscape.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/marked@12.0.0/marked.min.js"></script>
<style>
* {{ box-sizing: border-box; }}
body {{ margin: 0; font-family: system-ui, sans-serif; font-size: 14px; background: #f8fafc; display: flex; flex-direction: column; height: 100vh; }}
header {{ display: flex; align-items: center; justify-content: space-between; padding: 10px 16px; background: #fff; border-bottom: 1px solid #e2e8f0; }}
.title strong {{ font-size: 16px; margin-right: 8px; }}
.muted {{ color: #64748b; font-size: 12px; }}
.controls {{ display: flex; gap: 8px; }}
.controls input, .controls select, .controls button {{ font-size: 13px; padding: 5px 8px; border: 1px solid #cbd5e1; border-radius: 4px; }}
main {{ display: flex; flex: 1; min-height: 0; }}
#graph {{ flex: 1 1 65%; background: #fff; border-right: 1px solid #e2e8f0; position: relative; }}
#detail {{ flex: 0 0 35%; overflow-y: auto; padding: 18px 22px; background: #fff; }}
.type-chip {{ display: inline-block; padding: 2px 8px; border-radius: 10px; font-size: 11px; color: #fff; font-weight: 600; text-transform: uppercase; }}
#detail-body {{ font-size: 13px; line-height: 1.5; margin-top: 12px; }}
</style>
</head>
<body>
<header>
  <div class="title">
    <strong>LLM Wiki Graph</strong>
    <span class="muted">OKF Bundle Visualizer</span>
  </div>
  <div class="controls">
    <input id="search" type="search" placeholder="Filter nodes...">
    <select id="layout">
      <option value="cose">Force (cose)</option>
      <option value="concentric">Concentric</option>
      <option value="circle">Circle</option>
      <option value="grid">Grid</option>
    </select>
    <button id="reset">Reset View</button>
  </div>
</header>
<main>
  <div id="graph"></div>
  <div id="detail">
    <div id="detail-empty" class="muted">Click a node to view details.</div>
    <div id="detail-content" hidden>
      <span class="type-chip" id="detail-type"></span>
      <h2 id="detail-title" style="margin: 6px 0 2px;"></h2>
      <div class="muted" id="detail-id"></div>
      <div id="detail-body"></div>
    </div>
  </div>
</main>
<script>
const BUNDLE = {bundle_json};

let cy = cytoscape({{
  container: document.getElementById('graph'),
  elements: [...BUNDLE.nodes, ...BUNDLE.edges],
  style: [
    {{
      selector: 'node',
      style: {{
        'label': 'data(label)',
        'background-color': 'data(color)',
        'width': 'data(size)',
        'height': 'data(size)',
        'color': '#1e293b',
        'font-size': '11px',
        'text-valign': 'bottom',
        'text-margin-y': 4
      }}
    }},
    {{
      selector: 'edge',
      style: {{
        'width': 1.5,
        'line-color': '#cbd5e1',
        'target-arrow-color': '#cbd5e1',
        'target-arrow-shape': 'triangle',
        'curve-style': 'bezier'
      }}
    }},
    {{
      selector: ':selected',
      style: {{
        'border-width': 3,
        'border-color': '#0284c7'
      }}
    }}
  ],
  layout: {{ name: 'cose', animate: false }}
}});

cy.on('tap', 'node', function(evt) {{
  const d = evt.target.data();
  document.getElementById('detail-empty').hidden = true;
  document.getElementById('detail-content').hidden = false;
  document.getElementById('detail-title').textContent = d.label;
  document.getElementById('detail-id').textContent = d.id;
  document.getElementById('detail-type').textContent = d.type;
  document.getElementById('detail-type').style.backgroundColor = d.color;
  document.getElementById('detail-body').innerHTML = marked.parse(d.body || '');
}});

document.getElementById('search').addEventListener('input', (e) => {{
  const q = e.target.value.toLowerCase();
  cy.nodes().forEach(n => {{
    const label = (n.data('label') || '').toLowerCase();
    const id = (n.data('id') || '').toLowerCase();
    n.style('display', (label.includes(q) || id.includes(q)) ? 'element' : 'none');
  }});
}});

document.getElementById('layout').addEventListener('change', (e) => {{
  cy.layout({{ name: e.target.value, animate: true }}).run();
}});

document.getElementById('reset').addEventListener('click', () => {{
  cy.fit();
}});
</script>
</body>
</html>
"""

    OUTPUT_HTML.write_text(html_template, encoding="utf-8")
    print(f"Generated {OUTPUT_HTML} with {len(nodes)} nodes and {len(edges)} edges.")

if __name__ == "__main__":
    main()
