# generate_price.py
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import random, math

INTERVAL_MIN = 5  # intervalo em minutos
DESCONTO_FIDELIDADE = 0.9  # 10% de desconto

def gerar_html(titulo, preco, slot_start, slot_end, badge):
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{titulo}</title>
  <style>
    :root {{ font-family: system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,Arial; }}
    body {{ display:flex; min-height:100dvh; margin:0; background:#0f172a; color:#e5e7eb; }}
    main {{ margin:auto; text-align:center; padding:32px; }}
    h1 {{ margin:0 0 12px; font-weight:700; letter-spacing:.3px; }}
    #price {{ font-size: clamp(40px, 9vw, 96px); font-weight:800; line-height:1; }}
    .meta {{ margin-top:12px; opacity:.85; font-size:14px; }}
    .badge {{ display:inline-block; padding:4px 8px; border:1px solid #334155; border-radius:999px; margin-bottom:10px; font-size:12px; }}
  </style>
</head>
<body>
  <main>
    <div class="badge">{badge}</div>
    <h1>{titulo}</h1>
    <div id="price">R$ {preco:.2f}</div>
    <div class="meta">Atualizado em: {slot_start.strftime("%d/%m/%Y %H:%M:%S")} (BRT)</div>
    <div class="meta">Próxima mudança até: {slot_end.strftime("%H:%M:%S")} (BRT)</div>
    <div class="meta" style="margin-top:16px;">Intervalo: {INTERVAL_MIN} min • Fuso: Brasil</div>
  </main>
</body>
</html>
"""

# --- cálculo do preço por intervalo ---
now_utc = datetime.now(timezone.utc)
slot = math.floor(now_utc.timestamp() / (INTERVAL_MIN * 60))

rng = random.Random(slot)
preco_base = round(rng.uniform(8.0, 13.0), 2)  # preço normal (R$/kg)

br_time = now_utc.astimezone(ZoneInfo("America/Sao_Paulo"))
slot_start = br_time.replace(minute=(br_time.minute // INTERVAL_MIN) * INTERVAL_MIN, second=0, microsecond=0)
slot_end = slot_start.replace(minute=slot_start.minute + INTERVAL_MIN)

# Página 1 — Preço normal
html_normal = gerar_html(
    "Preço do Café — Normal",
    preco_base,
    slot_start,
    slot_end,
    "Preço para clientes em geral"
)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_normal)

# Página 2 — Fidelidade
preco_fidelidade = round(preco_base * DESCONTO_FIDELIDADE, 2)
html_fid = gerar_html(
    "Preço do Café — Fidelidade",
    preco_fidelidade,
    slot_start,
    slot_end,
    "Preço especial para clientes fidelidade"
)

with open("fidelidade.html", "w", encoding="utf-8") as f:
    f.write(html_fid)
