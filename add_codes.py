#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量新增希腊女神测试激活码（本地脚本，用 service_role 直连 Supabase）

用法：
  1. 把下面 SUPABASE_URL、SERVICE_ROLE_KEY 填成你自己的
  2. 终端运行：python3 add_codes.py

说明：
  - service_role key 在 Supabase → Settings → API，以 eyJ 开头
  - 它绕过 RLS，能直接 INSERT；用完别泄露
  - 新增的码 status 默认 unused，product_type 固定 goddess（前端激活查询依赖它）
"""

import json
import os
import urllib.request
import urllib.error

SUPABASE_URL = "https://rfqgzegjpfgmimfvbtcc.supabase.co"
# 优先读环境变量，避免把敏感 key 写进文件：SERVICE_ROLE_KEY=xxx python3 add_codes.py
SERVICE_ROLE_KEY = os.environ.get("SERVICE_ROLE_KEY", "在此粘贴你的 service_role key")

CODES = [
    "GODDESS-K2YN-UL0C",
    "GODDESS-47S5-13MQ",
    "GODDESS-GRMH-HTN0",
    "GODDESS-TJRM-SBQJ",
    "GODDESS-DT0S-P36G",
    "GODDESS-6ZPM-T7DE",
    "GODDESS-Y2S6-8RON",
    "GODDESS-IXYX-ZUBI",
    "GODDESS-J3M0-RE06",
    "GODDESS-BOM7-BPDR",
    "GODDESS-VOCR-37JB",
    "GODDESS-LMRP-93GT",
    "GODDESS-FCEJ-C9X4",
    "GODDESS-0PEN-YEZ9",
    "GODDESS-W8PG-FVQU",
    "GODDESS-7QVC-TKXW",
    "GODDESS-AAU4-4ND8",
    "GODDESS-Z0QT-E3AP",
    "GODDESS-QRU9-GX42",
    "GODDESS-XNN0-LCUC",
    "GODDESS-18CQ-GJJT",
    "GODDESS-432D-1LE2",
    "GODDESS-51UK-K5TZ",
    "GODDESS-LBOJ-PCNY",
    "GODDESS-I0PY-RKMF",
    "GODDESS-AMAR-I4CH",
    "GODDESS-WM5I-OKX2",
    "GODDESS-9IVF-JKU0",
    "GODDESS-U4TR-UU1V",
    "GODDESS-177H-E8JP",
]

URL = f"{SUPABASE_URL}/rest/v1/activation_codes"

rows = [
    {"code": c, "status": "unused", "product_type": "goddess"}
    for c in CODES
]

req = urllib.request.Request(
    URL,
    data=json.dumps(rows).encode("utf-8"),
    headers={
        "apikey": SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SERVICE_ROLE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    },
    method="POST",
)

try:
    with urllib.request.urlopen(req) as resp:
        body = resp.read().decode("utf-8")
        print("HTTP", resp.status)
        inserted = json.loads(body)
        print(f"成功插入 {len(inserted)} 个码：")
        for r in inserted:
            print("  ", r.get("code"), "->", r.get("status"))
except urllib.error.HTTPError as e:
    print("HTTP Error", e.code)
    print(e.read().decode("utf-8"))
except Exception as e:
    print("Error:", e)
