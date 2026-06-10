#!/usr/bin/env python3
"""
generate.py — Snapshot Flat File HTML Generator
================================================
Reads data.yaml and regenerates all HTML pages into the output directory.

Usage:
    python generate.py                  # outputs to ./site/
    python generate.py --out ./docs     # custom output directory

Requirements:
    pip install pyyaml
"""

import yaml
import shutil
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
CSS_SHARED = SCRIPT_DIR / "styles.css"
CSS_INDEX  = SCRIPT_DIR / "index.css"

SHARED_HEAD = """\
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">"""

PAGE_JS = """\
<script>
(function () {

  // ── Search / filter ────────────────────────────────────────────────────────
  var input = document.getElementById('field-search');
  if (input) {
    input.addEventListener('input', function () {
      var q = this.value.toLowerCase();
      var rows = document.querySelectorAll('tbody tr');
      var anyVisible = false;
      rows.forEach(function (row) {
        var match = row.textContent.toLowerCase().includes(q);
        row.style.display = match ? '' : 'none';
        if (match) anyVisible = true;
      });
      document.getElementById('no-results').style.display = anyVisible ? 'none' : '';
    });
  }

  // ── Copy-header buttons ────────────────────────────────────────────────────
  document.querySelectorAll('.hdr-code').forEach(function (el) {
    var wrapper = document.createElement('span');
    wrapper.className = 'hdr-wrap';

    var btn = document.createElement('button');
    btn.className = 'copy-btn';
    btn.title = 'Copy header';
    btn.innerHTML = '<svg width="12" height="12" viewBox="0 0 16 16" fill="currentColor"><path d="M0 6.75C0 5.784.784 5 1.75 5h1.5a.75.75 0 0 1 0 1.5h-1.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-1.5a.75.75 0 0 1 1.5 0v1.5A1.75 1.75 0 0 1 9.25 16h-7.5A1.75 1.75 0 0 1 0 14.25Z"/><path d="M5 1.75C5 .784 5.784 0 6.75 0h7.5C15.216 0 16 .784 16 1.75v7.5A1.75 1.75 0 0 1 14.25 11h-7.5A1.75 1.75 0 0 1 5 9.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"/></svg>';

    btn.addEventListener('click', function () {
      var raw = el.textContent.trim();
      var first = raw.split('/')[0].trim();
      navigator.clipboard.writeText(first).then(function () {
        btn.classList.add('copied');
        btn.title = 'Copied!';
        setTimeout(function () {
          btn.classList.remove('copied');
          btn.title = 'Copy header';
        }, 1500);
      });
    });

    el.parentNode.insertBefore(wrapper, el);
    wrapper.appendChild(el);
    wrapper.appendChild(btn);
  });

})();
</script>"""


def chip(text, cls):
    return '<span class="chip {}">{}</span>'.format(cls, text)


def field_row(f):
    name       = f.get("name", "")
    required   = f.get("required", False)
    unique     = f.get("unique", False)
    header     = str(f.get("header", "—"))
    desc       = f.get("description", "").strip()
    fmt        = f.get("format", "")
    values     = f.get("values", [])
    note       = f.get("note", "")
    deprecated = f.get("deprecated", False)

    classes = []
    if required:   classes.append("row-required")
    if deprecated: classes.append("deprecated-row")
    row_cls = ' class="{}"'.format(" ".join(classes)) if classes else ""

    dep_badge = '<span class="badge-dep">deprecated</span>' if deprecated else ""
    name_cls  = "field-name dep" if deprecated else "field-name"

    req_html  = '<span class="req-yes">Yes</span>' if required else '<span class="req-no">No</span>'
    uniq_html = '<span class="uniq-yes">Yes</span>' if unique   else '<span class="uniq-no">No</span>'

    if header == "—":
        hdr_html = '<span class="hdr-na">—</span>'
    else:
        hdr_html = '<span class="hdr-code">{}</span>'.format(header)

    if values:
        pills    = "".join('<span class="val-pill">{}</span>'.format(v) for v in values)
        vals_html = '<span class="field-values">{}</span>'.format(pills)
    else:
        vals_html = ""

    fmt_html = '<span class="field-format">{}</span>'.format(fmt) if fmt else ""
    vf_html  = (vals_html + fmt_html) if (vals_html or fmt_html) else '<span class="hdr-na">—</span>'

    note_html = '<span class="field-note">⚠ {}</span>'.format(note) if note else ""

    return """
        <tr{row_cls}>
          <td><span class="{name_cls}">{name}{dep_badge}</span></td>
          <td>{req}</td>
          <td>{uniq}</td>
          <td>{hdr}</td>
          <td>{vf}</td>
          <td><span class="desc">{desc}</span>{note}</td>
        </tr>""".format(
        row_cls=row_cls, name_cls=name_cls, name=name, dep_badge=dep_badge,
        req=req_html, uniq=uniq_html, hdr=hdr_html, vf=vf_html,
        desc=desc, note=note_html)


def entity_page(entity):
    eid        = entity["id"]
    title      = entity["title"]
    sis_obj    = entity.get("sis_object", "")
    insert     = entity.get("insert_update", "Smart Inserts or Updates")
    delete     = entity.get("delete_behavior", "Disable")
    fields     = entity.get("fields", [])
    en_note    = entity.get("entity_note", "")
    min_req    = entity.get("min_required", [])
    source_url = entity.get("source_url", "")

    req_fields = [f for f in fields if f.get("required")]
    dep_fields = [f for f in fields if f.get("deprecated")]
    opt_count  = len(fields) - len(req_fields) - len(dep_fields)

    source_html = ""
    if source_url:
        source_html = '<a class="source-link" href="{}" target="_blank" rel="noopener">Anthology docs ↗</a>'.format(source_url)

    jump_html = ""
    if req_fields:
        jump_html = '<a class="jump-link" href="#required-fields">Jump to required fields ↓</a>'

    dep_count_html = ""
    if dep_fields:
        dep_count_html = '<span class="count-chip count-dep">{} deprecated</span>'.format(len(dep_fields))

    entity_note_html = '<div class="box box-warn">⚠ {}</div>'.format(en_note.strip()) if en_note else ""

    min_req_html = ""
    if min_req:
        codes = ", ".join("<code>{}</code>".format(h) for h in min_req)
        min_req_html = '<div class="box box-info"><strong>Minimum required headers:</strong><br>{}</div>'.format(codes)

    # Build rows, stamping the first required row with the anchor id
    first_req_done = False
    rows = []
    for f in fields:
        row = field_row(f)
        if f.get("required") and not first_req_done:
            row = row.replace("<tr ", '<tr id="required-fields" ', 1)
            row = row.replace("<tr>", '<tr id="required-fields">', 1)
            first_req_done = True
        rows.append(row)
    rows_html = "".join(rows)

    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — SIS Snapshot Flat File</title>
{head}
</head>
<body>
<header>
  <div class="header-inner">
    <div class="breadcrumb"><a href="index.html">&#8592; All Entities</a><span class="sep">›</span>{title}</div>
    <div class="header-row">
      <h1>LEARN Object: {title}</h1>
      {source}
    </div>
    <div class="meta-row">
      {chip_sis}
      {chip_ins}
      {chip_del}
    </div>
  </div>
</header>
<main class="main">
  <div class="toolbar">
    <div class="toolbar-left">
      <div class="search-wrap">
        <svg class="search-icon" width="14" height="14" viewBox="0 0 16 16" fill="currentColor">
          <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001q.044.06.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1 1 0 0 0-.115-.099zm-5.242 1.656a5.5 5.5 0 1 1 0-11 5.5 5.5 0 0 1 0 11"/>
        </svg>
        <input id="field-search" type="search" placeholder="Filter fields…" autocomplete="off">
      </div>
      {jump}
    </div>
    <div class="toolbar-counts">
      <span class="count-chip count-req">{req_ct} required</span>
      <span class="count-chip count-opt">{opt_ct} optional</span>
      {dep_ct}
    </div>
  </div>
  {entity_note}{min_req}
  <table>
    <thead>
      <tr>
        <th>Field Name</th>
        <th>Required</th>
        <th>Unique</th>
        <th>Header</th>
        <th>Values / Format</th>
        <th>Description</th>
      </tr>
    </thead>
    <tbody>
      {rows}
    </tbody>
  </table>
  <div id="no-results" style="display:none" class="no-results">No fields match your filter.</div>
</main>
{js}
</body>
</html>""".format(
        title=title, head=SHARED_HEAD,
        source=source_html,
        chip_sis=chip("SIS: {}".format(sis_obj), "chip-sis"),
        chip_ins=chip("Insert/Update: {}".format(insert), "chip-insert"),
        chip_del=chip("Delete: {}".format(delete), "chip-delete"),
        jump=jump_html,
        req_ct=len(req_fields), opt_ct=opt_count, dep_ct=dep_count_html,
        entity_note=entity_note_html, min_req=min_req_html,
        rows=rows_html, js=PAGE_JS)


def index_page(entities):
    cards = ""
    for e in entities:
        eid     = e["id"]
        icon    = e.get("icon", "📄")
        title   = e["title"]
        sis_obj = e.get("sis_object", "")
        summary = e.get("summary", "").strip()
        fields  = e.get("fields", [])
        req_ct  = sum(1 for f in fields if f.get("required"))
        dep_ct  = sum(1 for f in fields if f.get("deprecated"))
        opt_ct  = len(fields) - req_ct - dep_ct

        dep_badge = '<span class="badge badge-dep-warn">{} deprecated</span>'.format(dep_ct) if dep_ct else ""

        cards += """
    <a class="card" href="{eid}.html">
      <div class="card-icon">{icon}</div>
      <div class="card-title">{title}</div>
      <div class="card-sis">SIS: {sis}</div>
      <div class="card-desc">{summary}</div>
      <div class="card-meta">
        <span class="badge badge-req">{req} required</span>
        <span class="badge badge-opt">{opt} optional</span>
        {dep}
      </div>
      <span class="arrow">&#x2197;</span>
    </a>""".format(eid=eid, icon=icon, title=title, sis=sis_obj,
                   summary=summary, req=req_ct, opt=opt_ct, dep=dep_badge)

    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Snapshot Flat File Header Descriptions</title>
{head}
<link rel="stylesheet" href="index.css">
</head>
<body>
<header>
  <div class="header-inner">
    <div class="breadcrumb">Blackboard Administrator<span class="sep">›</span>Integrations<span class="sep">›</span>SIS<span class="sep">›</span><span style="color:rgba(255,255,255,0.85)">Snapshot Flat File</span></div>
    <h1>Snapshot Flat File<br>Header Descriptions</h1>
    <p class="subtitle">Comprehensive reference for all supported LEARN data objects, their feed header naming conventions, usage descriptions, and data requirements.</p>
  </div>
</header>
<main class="main">
  <div class="grid">{cards}
  </div>
</main>
</body>
</html>""".format(head=SHARED_HEAD, cards=cards)


def main():
    parser = argparse.ArgumentParser(description="Generate SIS Snapshot Flat File HTML pages from data.yaml")
    parser.add_argument("--data", default="data.yaml", help="Path to YAML data file (default: data.yaml)")
    parser.add_argument("--out",  default="site",      help="Output directory (default: ./site)")
    args = parser.parse_args()

    data_path = Path(args.data)
    out_dir   = Path(args.out)

    if not data_path.exists():
        print("ERROR: Data file not found: {}".format(data_path))
        return

    with open(data_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    entities = data.get("entities", [])
    out_dir.mkdir(parents=True, exist_ok=True)

    for css_src in (CSS_SHARED, CSS_INDEX):
        shutil.copy2(css_src, out_dir / css_src.name)
        print("  ✓ {}".format(css_src.name))

    (out_dir / "index.html").write_text(index_page(entities), encoding="utf-8")
    print("  ✓ index.html")

    for entity in entities:
        eid = entity["id"]
        (out_dir / "{}.html".format(eid)).write_text(entity_page(entity), encoding="utf-8")
        print("  ✓ {}.html".format(eid))

    print("\nDone — {} pages written to ./{}/" .format(1 + len(entities), out_dir))


if __name__ == "__main__":
    main()
