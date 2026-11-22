#!/usr/bin/env python3
"""Build a packaged Tableau workbook from a public, published Tableau XML reference.

The workbook is adapted from the Kilo-Org Tableau-dashboard-creator multi-sheet
layout and action-filter snippets, with original Superstore data, geographic role,
month trends, a discount sheet, and a category cross-filter action.

The TWBX is assembled programmatically and XML/ZIP validated. No Tableau Desktop
executable is available in the Linux workspace to confirm interactive rendering.
"""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from urllib.request import urlopen
from uuid import uuid4
from zipfile import ZipFile, ZIP_DEFLATED, is_zipfile
from lxml import etree
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DASH = ROOT / "dashboard"
DASH.mkdir(exist_ok=True)
OUT_TWB = DASH / "Superstore_Executive_Dashboard.twb"
OUT_TWBX = DASH / "Superstore_Executive_Dashboard.twbx"
CSV = DASH / "sales_orders.csv"
ORIGINAL_CSV = ROOT / "data/raw/Sample_Superstore.csv"
TEMPLATE_URL = (
    "https://raw.githubusercontent.com/Kilo-Org/kilo-marketplace/main/"
    "skills/tableau-dashboard-creator/references/snippets/dashboard/multi-sheet-layout.twb"
)
ACTION_URL = (
    "https://raw.githubusercontent.com/Kilo-Org/kilo-marketplace/main/"
    "skills/tableau-dashboard-creator/references/snippets/dashboard/action-filter.twb"
)
DASH_TITLE = "Superstore Executive BI"

def fetch_xml(url: str) -> etree._Element:
    return etree.fromstring(urlopen(url, timeout=40).read())

def transform_dataset() -> None:
    df = pd.read_csv(ORIGINAL_CSV, encoding="utf-8-sig")
    dates = pd.to_datetime(df["Order Date"], format="%Y-%m-%d")
    discount = pd.to_numeric(df["Discount"], errors="raise")
    bands = pd.cut(
        discount, [-.001, 0, .20, .40, 1],
        labels=["0%", "0–20%", "20–40%", "40%+"],
        include_lowest=True
    )
    data = pd.DataFrame({
        "order_id": df["Order ID"],
        "order_date": dates.dt.strftime("%Y-%m-%d"),
        "customer_name": df["Customer Name"],
        "region": df["Region"],
        "state": df["State"],
        "product_category": df["Category"],
        "product_name": df["Product Name"],
        "quantity": df["Quantity"].astype("int64"),
        "unit_price": df["Sales"] / df["Quantity"],
        "discount": discount,
        "revenue": df["Sales"],
        "cost": df["Sales"] - df["Profit"],
        "profit": df["Profit"],
        "discount_band": bands.astype("string"),
    })
    assert len(data) == 9_994
    assert abs(float(data.revenue.sum()) - 2_297_200.86) < 0.02
    assert abs(float(data.profit.sum()) - 286_397.02) < 0.02
    data.to_csv(CSV, index=False, encoding="utf-8")
    print(f"Created {CSV.name}: {len(data):,} transaction lines, {len(data.columns)} fields")

def swap_subtree(node: etree._Element, pairs: list[tuple[str, str]]) -> etree._Element:
    b = etree.tostring(node, encoding="utf-8")
    for old, new in pairs:
        b = b.replace(old.encode("utf-8"), new.encode("utf-8"))
    return etree.fromstring(b)

def uniquify_ids(node: etree._Element) -> None:
    for sid in node.xpath(".//simple-id"):
        sid.set("uuid", "{" + str(uuid4()).upper() + "}")

def change_names(root: etree._Element, translations: dict[str, str]) -> None:
    for node in root.iter():
        for attr, val in tuple(node.attrib.items()):
            if val in translations:
                node.set(attr, translations[val])

def append_discount_metadata(root: etree._Element) -> None:
    ds = root.xpath("./datasources/datasource")[0]
    rel_cols = ds.xpath("./connection/relation/columns")[0]
    sample = next(x for x in rel_cols if x.get("name") == "product_category")
    n = deepcopy(sample)
    n.set("name", "discount_band")
    n.set("ordinal", str(max(int(x.get("ordinal", "0")) for x in rel_cols) + 1))
    rel_cols.append(n)
    for recs in ds.xpath(".//metadata-records"):
        base = next(
            (x for x in recs if x.get("class") == "column"
             and x.findtext("remote-name") == "product_category"), None
        )
        if base is None:
            continue
        other = deepcopy(base)
        for descendant in other.iter():
            if descendant.text:
                descendant.text = descendant.text.replace(
                    "product_category", "discount_band"
                )
            for key,val in tuple(descendant.attrib.items()):
                descendant.set(key, val.replace("product_category","discount_band"))
        ord_ = other.find("ordinal")
        if ord_ is not None:
            ord_.text = str(int(n.get("ordinal")))
        recs.append(other)
    old = next(x for x in ds.xpath("./column") if x.get("name") == "[product_category]")
    col = deepcopy(old)
    col.set("name", "[discount_band]")
    col.set("caption", "Discount Band")
    # Tableau XSD expects datasource columns before the extract/layout blocks.
    tail = next((i for i, child in enumerate(ds) if child.tag in ("extract", "layout", "semantic-values", "object-graph")), len(ds))
    ds.insert(tail, col)

def update_single_sheet(root: etree._Element) -> None:
    ws = root.xpath("./worksheets/worksheet")
    bar, line, geo = ws

    # 2015–2018 monthly SALES, replacing weekly PROFIT from the published template.
    modified = swap_subtree(line, [
        ("[sum:profit:qk]", "[sum:revenue:qk]"),
        ("[profit]", "[revenue]"),
        ('caption="Profit"', 'caption="Revenue"'),
        ('derivation="Week-Trunc"', 'derivation="Month-Trunc"'),
        ("[twk:order_date:qk]", "[tmn:order_date:qk]"),
    ])
    modified.find("./table/panes/pane/mark").set("class", "Line")
    ws_parent = root.find("worksheets")
    ws_parent.replace(line,modified)
    line = modified

    # State/province geography, rather than the template's country-only map.
    for rule in geo.xpath("./table/style/style-rule[@element='axis']"):
        rule.getparent().remove(rule)
    dep = geo.xpath("./table/view/datasource-dependencies")[0]
    for column in dep.xpath("./column[@name='[state]']"):
        column.set("caption", "State")
        column.set("semantic-role", "[State].[Name]")
    geo = swap_subtree(geo, [
        ("[sum:revenue:qk]", "[sum:profit:qk]"),
        ("[revenue]", "[profit]"),
        ('caption="Revenue"', 'caption="Profit"'),
    ])
    ws_parent.replace(ws_parent[2],geo)

    # Add a fourth bar chart to show profit by discount band.
    discount = swap_subtree(bar, [
        ("[product_category]", "[discount_band]"),
        ("none:product_category:nk", "none:discount_band:nk"),
        ("Product Category", "Discount Band"),
    ])
    discount.set("name","Discount Band Profit")
    discount.find("./table/panes/pane/mark").set("class","Bar")
    uniquify_ids(discount)
    ws_parent.append(discount)

    change_names(root, {
        "bar-chart": "Category Profit",
        "line-chart": "Monthly Sales",
        "map-chart": "US State Profit",
        "Dashboard 2": DASH_TITLE,
    })

def add_discount_zone(root: etree._Element) -> None:
    dashboard = root.xpath("./dashboards/dashboard")[0]
    # The published example reserves a lower row as an empty zone.
    empty = dashboard.xpath("./zones//zone[@type-v2='empty']")[0]
    empty.attrib.pop("type-v2")
    empty.set("name", "Discount Band Profit")
    empty.set("show-title", "true")
    idx = list(empty).index(empty.find("zone-style")) if empty.find("zone-style") is not None else 0
    empty.insert(idx, etree.Element("layout-cache", attrib={
        "minheight": "130",
        "minwidth": "152",
        "type-h": "scalable",
        "type-w": "scalable",
    }))
    # Rename worksheet zones so Tableau displays their native titles.
    for zone in dashboard.xpath(".//zone[@name]"):
        if zone.get("name") in (
            "Category Profit", "Monthly Sales", "US State Profit"
        ):
            zone.set("show-title", "true")
    # Maintain a scrollable mobile layout.
    phone = dashboard.xpath("./devicelayouts/devicelayout/zones//zone[@param='vert']")
    if phone:
        z=etree.Element("zone", attrib={
            "id":"30","name":"Discount Band Profit",
            "h":"29913","w":"98698","x":"651","y":"105003",
            "show-title":"true","fixed-size":"250","is-fixed":"true",
        })
        phone[0].append(z)
    # Template dashboard window must have the new viewpoint.
    win=root.xpath("./windows/window[@class='dashboard']")[0]
    vp=win.find("viewpoints")
    v=etree.SubElement(vp,"viewpoint",name="Discount Band Profit")
    etree.SubElement(v,"zoom",type="entire-view")
    # New worksheet needs a real window; copy only cards from an existing one.
    example = root.xpath("./windows/window[@class='worksheet']")[0]
    copied=deepcopy(example)
    copied.set("name","Discount Band Profit")
    uniquify_ids(copied)
    for field in copied.xpath(".//highlight/descendant::field"):
        field.getparent().remove(field)
    root.find("windows").insert(-1,copied)

def add_interactivity(root: etree._Element) -> None:
    reference=fetch_xml(ACTION_URL)
    action=deepcopy(reference.xpath("./actions/action")[0])
    action.set("caption","Select a product category to cross-filter the dashboard")
    action.set("name","[Action1_" + uuid4().hex.upper() + "]")
    source=action.find("source")
    source.set("dashboard", DASH_TITLE)
    source.set("worksheet","Category Profit")
    for param in action.xpath("./command/param"):
        if param.get("name") == "exclude": param.set("value","Category Profit")
        if param.get("name") == "target": param.set("value",DASH_TITLE)
    actions=etree.Element("actions")
    actions.append(action)
    root.insert(list(root).index(root.find("worksheets")),actions)

def main() -> None:
    transform_dataset()
    raw = urlopen(TEMPLATE_URL,timeout=40).read()
    # Field "country" in the published example is changed to a genuine US state field.
    raw=raw.replace(b"country",b"state").replace(b"Country",b"State")
    raw=raw.replace(b"[State].[ISO3166_2]",b"[State].[Name]")
    root=etree.fromstring(raw)
    # The renamed Tableau datasources should list our data, not the template's URL.
    connection = root.xpath("./datasources/datasource/connection/named-connections/named-connection/connection")[0]
    connection.set("directory", ".")
    connection.set("filename", CSV.name)
    connection.set("server", "")
    # The upstream example points at an old Windows Hyper extract. Remove it:
    # this workbook must query the packaged CSV, not a missing sample extract.
    for extract in root.xpath("./datasources/datasource/extract"):
        extract.getparent().remove(extract)
    append_discount_metadata(root)
    update_single_sheet(root)
    add_discount_zone(root)
    add_interactivity(root)
    # Remove a legacy source-template FCP attribute that 2026.1 rejects.
    for element in root.iter():
        for attr in list(element.attrib):
            if attr.startswith("_.fcp."):
                del element.attrib[attr]
    # Official Tableau 2026.1 workbook schema expects this top-level node.
    explain = etree.Element("explain-data", {
        "enabled-for-viewer": "false",
        "extreme-values-enabled-for-all": "false",
    })
    etree.SubElement(explain, "explanation-types")
    root.append(explain)
    # Remove reference workbook previews, which depict unrelated sample data.
    for thumbnail_node in root.xpath("./thumbnails"):
        root.remove(thumbnail_node)
    # Ensure workbook's metadata is clear and there are no dangling sheet references.
    for src in root.xpath(".//connection[@class='textscan']"):
        assert src.get("filename")==CSV.name
    for sheet in root.xpath("./worksheets/worksheet"):
        assert sheet.get("name")
    names={x.get("name") for x in root.xpath("./worksheets/worksheet")}
    zone_sheets={z.get("name") for z in root.xpath("./dashboards/dashboard//zone[@name]")}
    assert zone_sheets <= names, (zone_sheets, names)
    assert len(names)==4
    content=etree.tostring(root,encoding="utf-8",xml_declaration=True,pretty_print=True)
    etree.fromstring(content)
    OUT_TWB.write_bytes(content)
    with ZipFile(OUT_TWBX,"w",compression=ZIP_DEFLATED,compresslevel=6) as out:
        out.write(OUT_TWB,arcname=OUT_TWB.name)
        out.write(CSV,arcname=CSV.name)
    assert is_zipfile(OUT_TWBX)
    with ZipFile(OUT_TWBX) as z:
        assert z.testzip() is None
        assert set(z.namelist())=={OUT_TWB.name,CSV.name}
        embedded=etree.fromstring(z.read(OUT_TWB.name))
        assert len(embedded.xpath("./worksheets/worksheet")) == 4
        assert len(embedded.xpath("./dashboards/dashboard")) == 1
        assert len(embedded.xpath("./actions/action")) == 1
    print(f"Created TWB: {OUT_TWB} ({OUT_TWB.stat().st_size:,} bytes)")
    print(f"Created TWBX: {OUT_TWBX} ({OUT_TWBX.stat().st_size:,} bytes)")
    print("Contents: 4 live sheets, 1 executive dashboard, category selection action, embedded CSV")
    print("Caution: ZIP/XML structure checked; still needs a semantic open test in Tableau.")

if __name__ == "__main__":
    main()
