# -*- coding: utf-8 -*-
"""Diagnóstico local del repositorio central de ponderación METRO_RCM."""
import json
import sys
import requests

ENDPOINT = "https://script.google.com/macros/s/AKfycbx7WSRa1-uPUl2ThljERCQPV996Rnl5Uim8AHQ_PJlXcRDBO4DOjia4TuRcFB1BIxr7vQ/exec"

try:
    r = requests.get(
        ENDPOINT,
        params={"action": "list", "t": "diagnostico"},
        timeout=20,
        allow_redirects=True,
        headers={"Accept": "application/json", "User-Agent": "METRO_RCM/2026"},
    )
    print(f"HTTP: {r.status_code}")
    print(f"URL final: {r.url}")
    print(f"Content-Type: {r.headers.get('content-type', 'no informado')}")
    print(f"Bytes recibidos: {len(r.content)}")
    r.raise_for_status()
    data = r.json()
    print(json.dumps({
        "ok": data.get("ok"),
        "total": data.get("total"),
        "promedios": data.get("promedios"),
        "error": data.get("error"),
    }, ensure_ascii=False, indent=2))
    if not data.get("ok"):
        sys.exit(2)
except Exception as exc:
    print("DIAGNÓSTICO FALLÓ:")
    print(repr(exc))
    sys.exit(1)
