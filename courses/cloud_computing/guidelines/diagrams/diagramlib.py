"""Tiny diagram toolkit: one spec -> draw.io XML + SVG (PNG is rendered from the SVG with Inkscape).

Stdlib only. Used by build_diagrams.py.
"""
import html
import math

# AWS category colours (header band of each service box).
CAT = {
    'compute': '#ED7100', 'storage': '#7AA116', 'db': '#C925D1', 'net': '#8C4FFF',
    'sec': '#DD344C', 'integ': '#E7157B', 'ml': '#01A88D', 'mgmt': '#E7157B',
    'ext': '#5F6B7A',
}
FONT = 'Arimo, Liberation Sans, Helvetica, Arial, sans-serif'


class Diagram:
    def __init__(self, name, width, height):
        self.name, self.w, self.h = name, width, height
        self.boxes, self.nodes, self.edges, self.badges, self.texts = [], {}, [], [], []
        self.legend_steps = []

    # --- containers (dashed groups) -------------------------------------
    def group(self, gid, title, x, y, w, h, stroke='#7D8998', fill='none', dashed=True, tcolor='#37474F', right=False):
        self.boxes.append(dict(id=gid, title=title, x=x, y=y, w=w, h=h, stroke=stroke,
                               fill=fill, dashed=dashed, tcolor=tcolor, right=right))

    # --- service nodes ---------------------------------------------------
    def node(self, nid, title, lines, x, y, w=170, h=76, cat='compute'):
        self.nodes[nid] = dict(id=nid, title=title, lines=lines, x=x, y=y, w=w, h=h, color=CAT[cat])

    @staticmethod
    def _fs(n):
        return round(min(12.5, (n['w'] - 14) / (0.6 * max(len(n['title']), 1))), 1)

    def anchor(self, nid, side, off=0.5):
        n = self.nodes[nid]
        if side == 'l': return (n['x'], n['y'] + n['h'] * off)
        if side == 'r': return (n['x'] + n['w'], n['y'] + n['h'] * off)
        if side == 't': return (n['x'] + n['w'] * off, n['y'])
        return (n['x'] + n['w'] * off, n['y'] + n['h'])

    # --- edges -----------------------------------------------------------
    def edge(self, src, ss, dst, ds, label='', dashed=False, via=(), so=0.5, do=0.5, color='#37474F', lseg=None):
        self.edges.append(dict(src=src, ss=ss, dst=dst, ds=ds, label=label, dashed=dashed,
                               via=list(via), so=so, do=do, color=color, lseg=lseg))

    def path(self, e):
        p0 = self.anchor(e['src'], e['ss'], e['so'])
        p1 = self.anchor(e['dst'], e['ds'], e['do'])
        pts = [p0] + e['via'] + [p1]
        if not e['via'] and p0[0] != p1[0] and p0[1] != p1[1]:
            if e['ss'] in 'lr':
                mx = (p0[0] + p1[0]) / 2
                pts = [p0, (mx, p0[1]), (mx, p1[1]), p1]
            else:
                my = (p0[1] + p1[1]) / 2
                pts = [p0, (p0[0], my), (p1[0], my), p1]
        return pts

    def badge(self, nid, n, dx=-8, dy=-8):
        nd = self.nodes[nid]
        self.badges.append(dict(n=n, x=nd['x'] + dx, y=nd['y'] + dy, nid=nid))

    def text(self, x, y, s, size=12, bold=False, color='#37474F', anchor='start'):
        self.texts.append(dict(x=x, y=y, s=s, size=size, bold=bold, color=color, anchor=anchor))

    def step(self, n, s):
        self.legend_steps.append((n, s))

    # ====================================================================
    def _label_pos(self, pts, lseg=None):
        """Return ((x, y), rel) where rel in [-1, 1] is draw.io's position along the edge."""
        segs = [(math.dist(a, b), a, b) for a, b in zip(pts, pts[1:])]
        total = sum(s[0] for s in segs) or 1
        if lseg is None:
            target = total / 2
        else:
            i = lseg if lseg >= 0 else len(segs) + lseg
            target = sum(s[0] for s in segs[:i]) + segs[i][0] / 2
        acc = 0
        for ln, a, b in segs:
            if acc + ln >= target and ln > 0:
                t = (target - acc) / ln
                return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t), 2 * target / total - 1
            acc += ln
        return pts[0], 0

    # --------------------------------------------------------------------
    def svg(self):
        o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
             f'viewBox="0 0 {self.w} {self.h}" font-family="{FONT}">',
             f'<rect width="{self.w}" height="{self.h}" fill="#ffffff"/>',
             '<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" '
             'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#37474F"/></marker></defs>']
        for b in self.boxes:
            fill = b['fill'] if b['fill'] != 'none' else 'none'
            dash = ' stroke-dasharray="7,4"' if b['dashed'] else ''
            o.append(f'<rect x="{b["x"]}" y="{b["y"]}" width="{b["w"]}" height="{b["h"]}" rx="6" fill="{fill}" '
                     f'stroke="{b["stroke"]}" stroke-width="1.5"{dash}/>')
            tx, ta = (b['x'] + b['w'] - 10, 'end') if b['right'] else (b['x'] + 10, 'start')
            o.append(f'<text x="{tx}" y="{b["y"]+18}" font-size="12.5" font-weight="bold" text-anchor="{ta}" '
                     f'fill="{b["tcolor"]}">{html.escape(b["title"])}</text>')
        labels = []
        for e in self.edges:
            pts = self.path(e)
            d = 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts)
            dash = ' stroke-dasharray="6,4"' if e['dashed'] else ''
            o.append(f'<path d="{d}" fill="none" stroke="{e["color"]}" stroke-width="1.6"{dash} marker-end="url(#ar)"/>')
            if e['label']:
                labels.append((self._label_pos(pts, e['lseg'])[0], e['label']))
        for n in self.nodes.values():
            o.append(f'<rect x="{n["x"]}" y="{n["y"]}" width="{n["w"]}" height="{n["h"]}" rx="5" fill="#ffffff" '
                     f'stroke="{n["color"]}" stroke-width="2"/>')
            o.append(f'<path d="M{n["x"]},{n["y"]+24} V{n["y"]+5} a5,5 0 0 1 5,-5 H{n["x"]+n["w"]-5} a5,5 0 0 1 5,5 V{n["y"]+24} z" '
                     f'fill="{n["color"]}"/>')
            o.append(f'<text x="{n["x"]+n["w"]/2}" y="{n["y"]+16}" font-size="{self._fs(n)}" font-weight="bold" fill="#fff" '
                     f'text-anchor="middle">{html.escape(n["title"])}</text>')
            ly = n['y'] + 24 + (n['h'] - 24 - 14 * len(n['lines'])) / 2 + 11
            for i, ln in enumerate(n['lines']):
                o.append(f'<text x="{n["x"]+n["w"]/2}" y="{ly+14*i:.1f}" font-size="11" fill="#455A64" '
                         f'text-anchor="middle">{html.escape(ln)}</text>')
        for (x, y), s in labels:
            w = 6.1 * len(s) + 8
            o.append(f'<rect x="{x-w/2:.1f}" y="{y-9:.1f}" width="{w:.1f}" height="17" rx="3" fill="#fff" fill-opacity="0.95"/>')
            o.append(f'<text x="{x:.1f}" y="{y+4:.1f}" font-size="10.5" fill="#263238" text-anchor="middle">{html.escape(s)}</text>')
        for t in self.texts:
            wt = ' font-weight="bold"' if t['bold'] else ''
            o.append(f'<text x="{t["x"]}" y="{t["y"]}" font-size="{t["size"]}"{wt} fill="{t["color"]}" '
                     f'text-anchor="{t["anchor"]}">{html.escape(t["s"])}</text>')
        for b in self.badges:
            o.append(f'<circle cx="{b["x"]+9}" cy="{b["y"]+9}" r="10" fill="#263238"/>')
            o.append(f'<text x="{b["x"]+9}" y="{b["y"]+13.5}" font-size="12" font-weight="bold" fill="#fff" '
                     f'text-anchor="middle">{b["n"]}</text>')
        o.append('</svg>')
        return '\n'.join(o)

    # --------------------------------------------------------------------
    def drawio(self):
        cells, nid = [], [100]

        def nxt():
            nid[0] += 1
            return f'c{nid[0]}'

        def esc(s):
            return html.escape(s, quote=True)

        for b in self.boxes:
            dash = 'dashed=1;' if b['dashed'] else ''
            fill = 'fillColor=none;' if b['fill'] == 'none' else f'fillColor={b["fill"]};'
            cells.append(f'<mxCell id="{b["id"]}" value="{esc(b["title"])}" style="rounded=1;arcSize=2;whiteSpace=wrap;html=1;'
                         f'{fill}{dash}strokeColor={b["stroke"]};verticalAlign=top;align={'right' if b['right'] else 'left'};spacingLeft=8;spacingRight=8;spacingTop=2;'
                         f'fontStyle=1;fontSize=12;fontColor={b["tcolor"]};" vertex="1" parent="1">'
                         f'<mxGeometry x="{b["x"]}" y="{b["y"]}" width="{b["w"]}" height="{b["h"]}" as="geometry"/></mxCell>')
        for n in self.nodes.values():
            body = '<br>'.join(esc(l) for l in n['lines'])
            cells.append(f'<mxCell id="{n["id"]}" value="{esc(body)}" style="rounded=1;arcSize=6;whiteSpace=wrap;html=1;'
                         f'fillColor=#ffffff;strokeColor={n["color"]};strokeWidth=2;fontSize=11;fontColor=#455A64;'
                         f'verticalAlign=middle;spacingTop=22;" vertex="1" parent="1">'
                         f'<mxGeometry x="{n["x"]}" y="{n["y"]}" width="{n["w"]}" height="{n["h"]}" as="geometry"/></mxCell>')
            cells.append(f'<mxCell id="{n["id"]}_h" value="{esc(n["title"])}" style="rounded=1;arcSize=20;whiteSpace=wrap;html=1;'
                         f'fillColor={n["color"]};strokeColor={n["color"]};fontColor=#ffffff;fontStyle=1;fontSize={self._fs(n)};" '
                         f'vertex="1" parent="{n["id"]}"><mxGeometry width="{n["w"]}" height="24" as="geometry"/></mxCell>')
        sides = {'l': (0, None), 'r': (1, None), 't': (None, 0), 'b': (None, 1)}

        def xy(side, off):
            if side == 'l': return (0, off)
            if side == 'r': return (1, off)
            if side == 't': return (off, 0)
            return (off, 1)

        for i, e in enumerate(self.edges):
            ex, ey = xy(e['ss'], e['so'])
            nx, ny = xy(e['ds'], e['do'])
            pts = self.path(e)
            wp = ''.join(f'<mxPoint x="{x:.1f}" y="{y:.1f}"/>' for x, y in pts[1:-1])
            dash = 'dashed=1;' if e['dashed'] else ''
            cells.append(f'<mxCell id="e{i}" value="{esc(e["label"])}" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;'
                         f'endArrow=block;endFill=1;labelBackgroundColor=#ffffff;fontSize=10;strokeWidth=1.6;{dash}'
                         f'strokeColor={e["color"]};exitX={ex};exitY={ey};exitPerimeter=0;entryX={nx};entryY={ny};entryPerimeter=0;" '
                         f'edge="1" parent="1" source="{e["src"]}" target="{e["dst"]}"><mxGeometry x="{self._label_pos(pts, e["lseg"])[1]:.3f}" relative="1" as="geometry">'
                         f'<Array as="points">{wp}</Array></mxGeometry></mxCell>')
        for t in self.texts:
            fs = 'fontStyle=1;' if t['bold'] else ''
            al = {'start': 'left', 'middle': 'center', 'end': 'right'}[t['anchor']]
            cells.append(f'<mxCell id="{nxt()}" value="{esc(t["s"])}" style="text;html=1;strokeColor=none;fillColor=none;{fs}'
                         f'align={al};verticalAlign=middle;fontSize={t["size"]};fontColor={t["color"]};" vertex="1" parent="1">'
                         f'<mxGeometry x="{t["x"] - (0 if al == "left" else 300)}" y="{t["y"] - t["size"]}" width="600" '
                         f'height="{t["size"] + 6}" as="geometry"/></mxCell>')
        for b in self.badges:
            cells.append(f'<mxCell id="{nxt()}" value="{b["n"]}" style="ellipse;whiteSpace=wrap;html=1;fillColor=#263238;'
                         f'strokeColor=#263238;fontColor=#ffffff;fontStyle=1;fontSize=12;aspect=fixed;" vertex="1" parent="1">'
                         f'<mxGeometry x="{b["x"]-1}" y="{b["y"]-1}" width="20" height="20" as="geometry"/></mxCell>')
        return ('<mxfile host="app.diagrams.net"><diagram name="' + esc(self.name) + '" id="arch">'
                f'<mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" '
                f'fold="1" page="1" pageScale="1" pageWidth="{self.w}" pageHeight="{self.h}" math="0" shadow="0">'
                '<root><mxCell id="0"/><mxCell id="1" parent="0"/>' + ''.join(cells) +
                '</root></mxGraphModel></diagram></mxfile>')

    # --------------------------------------------------------------------
    def add_steps_panel(self, y0, title='Flow'):
        """Numbered step captions drawn as text at the bottom of the canvas."""
        self.text(24, y0, title, size=13, bold=True)
        for i, (n, s) in enumerate(self.legend_steps):
            self.text(24, y0 + 22 + 19 * i, f'{n}.  {s}', size=12)
