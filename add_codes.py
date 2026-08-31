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
import urllib.request
import urllib.error

SUPABASE_URL = "https://rfqgzegjpfgmimfvbtcc.supabase.co"
SERVICE_ROLE_KEY = "在此粘贴你的 service_role key"  # TODO: 替换成真实 key

CODES = [
    "GODDESS-9EX7-FWHQ",
    "GODDESS-5DLV-6YU5",
    "GODDESS-EUBN-WYVR",
    "GODDESS-4WVZ-L593",
    "GODDESS-WPJP-5ENW",
    "GODDESS-EF4D-6MR5",
    "GODDESS-9HGE-GBBN",
    "GODDESS-C7UY-H9QD",
    "GODDESS-CSFN-X2KA",
    "GODDESS-G275-KRD5",
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
