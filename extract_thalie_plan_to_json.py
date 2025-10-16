
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extract an architectural plan (PDF) into a structured JSON usable for 3D generation.

- Detect floors (RDC, R+1, R+2) from text
- Parse vector drawings to reconstruct axis-aligned room rectangles (walls)
- Attach room labels (SALLE 101, GROUPE 2, SAN. F, etc.) to enclosing rectangles
- Derive features (TABLEAU, POSTES N, tables connectées) found inside each room
- Convert page coordinates to real-world meters using the plan's scale (default 1:150)
- Emit a JSON file: building → floors → rooms with geometry and metadata

Usage:
    python extract_thalie_plan_to_json.py \
        --pdf /path/to/PRIVE_Plans_THALIE_Montpellier.pdf \
        --out /path/to/thalie_building.json \
        --building-name "LE THALIE" \
        --default-scale "1:150"

Requires:
    PyMuPDF (fitz)
"""
import argparse
import dataclasses
import json
import math
import re
import sys
from collections import defaultdict
from typing import Dict, List, Tuple, Optional

try:
    import fitz  # PyMuPDF
except Exception as e:
    print("ERROR: PyMuPDF (fitz) is required. Install with: pip install pymupdf", file=sys.stderr)
    raise

@dataclasses.dataclass
class BBox:
    x: float
    y: float
    w: float
    h: float
    def to_dict(self):
        return {"x_m": self.x, "y_m": self.y, "w_m": self.w, "h_m": self.h}
    def contains_pt(self, px: float, py: float) -> bool:
        return (self.x <= px <= self.x + self.w) and (self.y <= py <= self.y + self.h)

@dataclasses.dataclass
class Room:
    name: str
    type: str
    bbox: BBox
    area_m2: float
    features: Dict[str, object]
    notes: List[str]
    def to_dict(self):
        return {
            "name": self.name,
            "type": self.type,
            "bbox": self.bbox.to_dict(),
            "area_m2": round(self.area_m2, 2),
            "features": self.features,
            "notes": self.notes,
        }

@dataclasses.dataclass
class Floor:
    code: str
    name: str
    surface_plancher_m2: Optional[float]
    rooms: List[Room]
    notes: List[str]
    def to_dict(self):
        return {
            "code": self.code,
            "name": self.name,
            "surface_plancher_m2": self.surface_plancher_m2,
            "rooms": [r.to_dict() for r in self.rooms],
            "notes": self.notes,
        }

def parse_scale_from_text(full_text: str, fallback="1:150") -> Tuple[int, int]:
    m = re.search(r'(\d+)\s*:\s*(\d+)', full_text)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        if a > 0 and b > 0:
            return (a, b)
    fa, fb = fallback.split(":")
    return int(fa), int(fb)

def meters_per_pt(scale_num: int, scale_den: int) -> float:
    mm_per_pt = 25.4 / 72.0
    m_per_pt = (mm_per_pt * (scale_den / scale_num)) / 1000.0
    return m_per_pt

def snap(v: float, eps: float = 0.5) -> float:
    return round(v / eps) * eps

def segment_is_horizontal(p1: Tuple[float, float], p2: Tuple[float, float], ang_eps_deg: float = 1.0) -> bool:
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    angle = math.degrees(math.atan2(dy, dx))
    angle = abs(angle) % 180.0
    return (angle < ang_eps_deg) or (abs(angle - 180.0) < ang_eps_deg)

def segment_is_vertical(p1: Tuple[float, float], p2: Tuple[float, float], ang_eps_deg: float = 1.0) -> bool:
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    angle = abs(math.degrees(math.atan2(dy, dx))) % 180.0
    return abs(angle - 90.0) < ang_eps_deg

def merge_intervals(intervals: List[Tuple[float, float]], tol: float = 0.75) -> List[Tuple[float, float]]:
    if not intervals:
        return []
    intervals = sorted((min(a, b), max(a, b)) for a, b in intervals)
    merged = [intervals[0]]
    for a, b in intervals[1:]:
        la, lb = merged[-1]
        if a <= lb + tol:
            merged[-1] = (la, max(lb, b))
        else:
            merged.append((a, b))
    return merged

def intervals_cover(segments: List[Tuple[float, float]], a: float, b: float, tol: float = 0.5) -> bool:
    if a > b:
        a, b = b, a
    merged = merge_intervals(segments, tol=tol)
    for x0, x1 in merged:
        if x0 - tol <= a and x1 + tol >= b:
            return True
    return False

def infer_room_type(name: str) -> str:
    n = name.upper()
    if re.search(r'\bSAN\b|SAN\.|SANIT', n):
        if 'F' in n and 'H' not in n: return "sanitaires_femmes"
        if 'H' in n and 'F' not in n: return "sanitaires_hommes"
        return "sanitaires"
    if 'ASC' in n: return "ascenseur"
    if 'HALL' in n: return "hall"
    if 'ACCUEIL' in n: return "accueil"
    if 'PROF' in n: return "salle_personnel"
    if 'MENAGE' in n or 'MÉNAGE' in n: return "local_menage"
    if 'SERVEUR' in n or 'BAIE' in n or 'TGBT' in n: return "local_technique"
    if 'ARCHIVE' in n: return "archives"
    if 'COPIEUR' in n: return "local_copieur"
    if 'BDE' in n: return "bureau_des_etudiants"
    if 'SAND BOX' in n or 'SANDBOX' in n: return "espace_projet"
    if 'TERRASSE' in n or 'BELV' in n: return "espace_exterieur"
    if 'CO-WORK' in n or 'COWORK' in n: return "coworking"
    if 'GROUPE' in n: return "salle_de_groupe"
    if re.search(r'\bSALLE\b', n): return "salle_de_cours"
    if 'STOCK' in n or 'CAVE' in n: return "stockage"
    if 'DIR' in n: return "direction"
    if 'ADMIN' in n: return "administration"
    if 'BUREAU' in n: return "bureau"
    return "divers"

def _collect_segments(page: "fitz.Page") -> Tuple[Dict[float, List[Tuple[float, float]]], Dict[float, List[Tuple[float, float]]]]:
    drawings = page.get_drawings()
    H: Dict[float, List[Tuple[float, float]]] = defaultdict(list)
    V: Dict[float, List[Tuple[float, float]]] = defaultdict(list)
    for d in drawings:
        items = d.get("items", [])
        for it in items:
            if it.get("type") != "l":
                continue
            x1, y1, x2, y2 = it["points"]
            p1, p2 = (x1, y1), (x2, y2)
            if segment_is_horizontal(p1, p2):
                y = snap((y1 + y2) / 2.0)
                x0, x1 = sorted([x1, x2])
                H[y].append((x0, x1))
            elif segment_is_vertical(p1, p2):
                x = snap((x1 + x2) / 2.0)
                y0, y1 = sorted([y1, y2])
                V[x].append((y0, y1))
    for y in list(H.keys()):
        H[y] = merge_intervals(H[y])
    for x in list(V.keys()):
        V[x] = merge_intervals(V[x])
    return H, V

def _find_rectangles(H: Dict[float, List[Tuple[float, float]]],
                     V: Dict[float, List[Tuple[float, float]]],
                     min_area_pt2: float = 2000.0) -> List[Tuple[float, float, float, float]]:
    ys = sorted(H.keys())
    xs = sorted(V.keys())
    rects: List[Tuple[float, float, float, float]] = []
    def horiz_covers(y: float, x0: float, x1: float) -> bool:
        return intervals_cover(H.get(y, []), x0, x1)
    def vert_covers(x: float, y0: float, y1: float) -> bool:
        return intervals_cover(V.get(x, []), y0, y1)
    for i in range(len(xs)):
        for j in range(i + 1, len(xs)):
            x0, x1 = xs[i], xs[j]
            if x1 - x0 < 10:
                continue
            for a in range(len(ys)):
                for b in range(a + 1, len(ys)):
                    y0, y1 = ys[a], ys[b]
                    if y1 - y0 < 10:
                        continue
                    if not horiz_covers(y0, x0, x1): 
                        continue
                    if not horiz_covers(y1, x0, x1): 
                        continue
                    if not vert_covers(x0, y0, y1): 
                        continue
                    if not vert_covers(x1, y0, y1): 
                        continue
                    w, h = (x1 - x0), (y1 - y0)
                    area = w * h
                    if area >= min_area_pt2:
                        rects.append((x0, y0, w, h))
    deduped: List[Tuple[float, float, float, float]] = []
    def near_equal(r1, r2, tol=1.0):
        return all(abs(a - b) <= tol for a, b in zip(r1, r2))
    for r in rects:
        if not any(near_equal(r, q) for q in deduped):
            deduped.append(r)
    return deduped

def _extract_words(page: "fitz.Page") -> List[Tuple[float, float, float, float, str]]:
    words = []
    for w in page.get_text("words"):
        x0, y0, x1, y1, text, *_ = w
        words.append((x0, y0, x1, y1, text))
    return words

def _full_text(doc: "fitz.Document") -> str:
    return "\n".join(page.get_text() for page in doc)

ROOM_LABEL_RE = re.compile(
    r'(?:(SALLE\s+\d{1,3})|(GROUPE\s+\d{1,2})|(SAN\.\s*[FH])|(SANITAIRES?)|(HALL)|(ACCUEIL)|(BDE)|(SAND\s*BOX)|(TERRASSE)|(BELVÉDÈRE|BELVEDERE)|(CO-?WORKING\s+ÉTUDIANTS|COWORKING)|(ARCHIVES?)|(SERVEUR\s*TGBT|TGBT|BAIE)|(PROFS?)|(MENAGE|MÉNAGE)|(COPIEUR)|(DIR(?:\s+\w+)?)|(ADMIN)|(BUREAU(?:\s+\d+)?)|(STOCK|CAVE))',
    flags=re.IGNORECASE
)
FEATURE_WORDS = re.compile(r'\b(TABLEAU|POSTES?|TABLES?\s+CONNECT(E|É)ES?)\b', re.IGNORECASE)
POSTES_COUNT = re.compile(r'\bPOSTES?\s*:?\s*(\d+)\b', re.IGNORECASE)

def _room_candidates_from_words(words: List[Tuple[float, float, float, float, str]]) -> List[Tuple[str, float, float]]:
    candidates = []
    for (x0, y0, x1, y1, text) in words:
        m = ROOM_LABEL_RE.search(text)
        if m:
            cx = (x0 + x1) / 2.0
            cy = (y0 + y1) / 2.0
            candidates.append((m.group(0).strip(), cx, cy))
    return candidates

def _features_inside_rect(words: List[Tuple[float, float, float, float, str]],
                          rect: Tuple[float, float, float, float]) -> Dict[str, object]:
    x, y, w, h = rect
    x1, y1 = x + w, y + h
    feats: Dict[str, object] = {}
    postes = None
    has_tableau = False
    tables_connectees = False
    texts = []
    for (wx0, wy0, wx1, wy1, text) in words:
        cx, cy = (wx0 + wx1) / 2.0, (wy0 + wy1) / 2.0
        if (x <= cx <= x1) and (y <= cy <= y1):
            texts.append(text)
            if FEATURE_WORDS.search(text):
                has_tableau = has_tableau or ('TABLEAU' in text.upper())
                if re.search(r'TABLES?\s+CONNECT(E|É)ES?', text, re.IGNORECASE):
                    tables_connectees = True
                m = POSTES_COUNT.search(text)
                if m:
                    try: postes = int(m.group(1))
                    except: pass
    if has_tableau: feats["TABLEAU"] = True
    if tables_connectees: feats["tables_connectees"] = True
    if postes is not None: feats["POSTES"] = postes
    if texts: feats["raw_text_inside"] = " ".join(texts)
    return feats

def _assign_labels_to_rects(labels: List[Tuple[str, float, float]],
                            rects: List[Tuple[float, float, float, float]]) -> Dict[int, str]:
    assigned: Dict[int, str] = {}
    for label, cx, cy in labels:
        best_idx = None
        for i, (x, y, w, h) in enumerate(rects):
            if (x <= cx <= x + w) and (y <= cy <= y + h):
                best_idx = i
                break
        if best_idx is None:
            best_d = 1e18
            for i, (x, y, w, h) in enumerate(rects):
                rx, ry = x + w / 2.0, y + h / 2.0
                d = (rx - cx) ** 2 + (ry - cy) ** 2
                if d < best_d:
                    best_d = d
                    best_idx = i
        if best_idx in assigned:
            assigned[best_idx] = assigned[best_idx] + " / " + label
        else:
            assigned[best_idx] = label
    return assigned

def _detect_floor_code(page_text: str) -> str:
    if re.search(r'\bR\+2\b', page_text): return "R+2"
    if re.search(r'\bR\+1\b', page_text): return "R+1"
    if re.search(r'\bRDC\b', page_text): return "RDC"
    return "N/A"

def _detect_surface_plancher(page_text: str) -> Optional[float]:
    m = re.search(r'(Surf\.\s*Plancher[^=\n]*=|Surface[^=\n]*=)\s*([\d\.,]+)\s*m', page_text, re.IGNORECASE)
    if m:
        val = m.group(2).replace(',', '.')
        try: return float(val)
        except: return None
    return None

def process_pdf(pdf_path: str,
                building_name: str = "LE THALIE",
                default_scale: str = "1:150") -> Dict:
    doc = fitz.open(pdf_path)
    full_text = _full_text(doc)
    s_num, s_den = parse_scale_from_text(full_text, fallback=default_scale)
    m_per_pt = meters_per_pt(s_num, s_den)

    building = {
        "building": {
            "name": building_name,
            "document": {
                "source_file": pdf_path.split("/")[-1],
                "scale": f"{s_num}:{s_den}",
            }
        },
        "floors": []
    }

    for page in doc:
        page_text = page.get_text()
        words = _extract_words(page)
        H, V = _collect_segments(page)
        rects = _find_rectangles(H, V, min_area_pt2=2000.0)

        labels = _room_candidates_from_words(words)
        label_map = _assign_labels_to_rects(labels, rects)

        floor_code = _detect_floor_code(page_text)
        floor_name = {"RDC": "Rez-de-chaussée", "R+1": "Étage 1", "R+2": "Étage 2"}.get(floor_code, floor_code)
        floor_surface = _detect_surface_plancher(page_text)

        rooms: List[Room] = []
        for i, (x, y, w, h) in enumerate(rects):
            x_m = x * m_per_pt
            y_m = y * m_per_pt
            w_m = w * m_per_pt
            h_m = h * m_per_pt
            area_m2 = (w * m_per_pt) * (h * m_per_pt)

            label = label_map.get(i, f"UNLABELED_{i+1}")
            rtype = infer_room_type(label)
            feats = _features_inside_rect(words, (x, y, w, h))

            room = Room(
                name=label,
                type=rtype,
                bbox=BBox(x=x_m, y=y_m, w=w_m, h=h_m),
                area_m2=area_m2,
                features=feats,
                notes=[]
            )
            rooms.append(room)

        floor = Floor(
            code=floor_code,
            name=floor_name,
            surface_plancher_m2=floor_surface,
            rooms=rooms,
            notes=[]
        )
        building["floors"].append(floor.to_dict())

    return building

def main():
    ap = argparse.ArgumentParser(description="Extract plan PDF into a detailed JSON for 3D generation.")
    ap.add_argument("--pdf", required=True, help="Path to the plan PDF (e.g., PRIVE_Plans_THALIE_Montpellier.pdf)")
    ap.add_argument("--out", required=True, help="Output JSON path")
    ap.add_argument("--building-name", default="LE THALIE", help="Building name to embed into JSON")
    ap.add_argument("--default-scale", default="1:150", help="Fallback scale if none is detected in the PDF text")
    args = ap.parse_args()

    data = process_pdf(args.pdf, building_name=args.building_name, default_scale=args.default_scale)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"JSON written to: {args.out}")
    for fl in data.get("floors", []):
        print(f"- {fl['code'] or 'N/A'}: {len(fl['rooms'])} rectangles/rooms")

if __name__ == "__main__":
    main()
