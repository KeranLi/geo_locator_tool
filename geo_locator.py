#!/usr/bin/env python3
"""Natural-language place name -> longitude/latitude."""
from __future__ import annotations
import argparse, json, os, sys
from typing import Any
import requests

def get_json(url: str, params: dict[str, Any]) -> Any:
    r = requests.get(url, params=params, headers={"User-Agent": "geo-locator/1.0"}, timeout=15)
    r.raise_for_status()
    return r.json()

def amap(q: str, key: str):
    d = get_json("https://restapi.amap.com/v3/geocode/geo", {"address": q, "output": "json", "key": key})
    return [{"provider":"amap", "address": x.get("formatted_address", q), "location":x["location"], "coordinate_system":"GCJ-02"}
            for x in d.get("geocodes", []) if x.get("location")]

def nominatim(q: str):
    d = get_json("https://nominatim.openstreetmap.org/search", {"q":q,"format":"jsonv2","limit":5,"accept-language":"zh-CN"})
    return [{"provider":"nominatim", "address":x.get("display_name",q), "location":f"{x['lon']},{x['lat']}", "coordinate_system":"WGS84"}
            for x in d if x.get("lat") and x.get("lon")]

def tianditu(q: str, token: str):
    d = get_json("https://api.tianditu.gov.cn/geocoder", {"ds":json.dumps({"keyWord":q},ensure_ascii=False),"tk":token})
    p = d.get("location") or {}
    return [{"provider":"tianditu", "address":q, "location":f"{p['lon']},{p['lat']}", "coordinate_system":"CGCS2000/经纬度"}] if p.get("lon") and p.get("lat") else []

def locate(q: str, country: str = ""):
    q = f"{q}, {country}" if country and country not in q else q
    out, errors = [], []
    if os.getenv("AMAP_KEY"):
        try: out += amap(q, os.environ["AMAP_KEY"])
        except Exception as e: errors.append(f"amap: {e}")
    try: out += nominatim(q)
    except Exception as e: errors.append(f"nominatim: {e}")
    if os.getenv("TDT_TOKEN"):
        try: out += tianditu(q, os.environ["TDT_TOKEN"])
        except Exception as e: errors.append(f"tianditu: {e}")
    if not out and errors: raise RuntimeError("所有服务均不可用：" + " | ".join(errors))
    return out

def main():
    p = argparse.ArgumentParser(description="按照自然语言检索地点经纬度")
    p.add_argument("query", nargs="?", help="地点名称或自然语言地址")
    p.add_argument("--country", default="", help="可选国家/地区")
    p.add_argument("--format", choices=("text","json"), default="text")
    a = p.parse_args(); q = a.query or input("请输入地点：").strip()
    if not q: p.error("地点不能为空")
    try: rows = locate(q, a.country)
    except Exception as e: print(f"查询失败：{e}", file=sys.stderr); return 2
    if a.format == "json": print(json.dumps(rows, ensure_ascii=False, indent=2)); return 0
    if not rows: print("没有找到匹配地点，请补充省、市、县、乡等信息。"); return 0
    for i, x in enumerate(rows, 1): print(f"[{i}] {x['address']}\n    {x['location']} ({x['coordinate_system']}) [{x['provider']}]")
    return 0

if __name__ == "__main__": raise SystemExit(main())
