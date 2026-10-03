"""games.json -> flyer.html -> flyer.pdf / flyer.png (A4 세로 통합 전단지).
게임을 games.json 에 추가하고 이 스크립트만 다시 돌리면 전단지가 늘어난다.
"""
import base64, html, io, json, subprocess, urllib.parse
from pathlib import Path

import qrcode
import qrcode.image.svg

ROOT = Path(__file__).parent
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
data = json.loads((ROOT / "games.json").read_text(encoding="utf-8"))
games = data["games"]


def qr_svg(url):
    img = qrcode.make(url, image_factory=qrcode.image.svg.SvgPathImage, box_size=10, border=0)
    buf = io.BytesIO()
    img.save(buf)
    return buf.getvalue().decode()


def icon_uri(gid):
    return "data:image/png;base64," + base64.b64encode((ROOT / "img" / f"{gid}.png").read_bytes()).decode()


cards = []
for g in games:
    ref = urllib.parse.quote(f"utm_source=flyer&utm_medium=print&utm_campaign={g['id']}", safe="")
    url = f"https://play.google.com/store/apps/details?id={g['package']}&referrer={ref}"
    cards.append(f"""
<section class="card">
  <img src="{icon_uri(g['id'])}" alt="">
  <div class="txt"><div class="genre">{html.escape(g['genre'])}</div>
    <h2>{html.escape(g['name'])}</h2><p>{html.escape(g['tagline'])}</p></div>
  <div class="qr">{qr_svg(url)}<span>스캔해서 받기</span></div>
</section>""")

page = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<style>
@page {{ size: A4; margin: 0 }}
* {{ box-sizing: border-box }}
html,body {{ margin:0 }}
body {{ width:210mm; height:297mm; background:#14110d; color:#eadfc8;
  font-family:"Malgun Gothic",system-ui,sans-serif; padding:14mm 13mm; display:flex; flex-direction:column }}
header {{ text-align:center; border-bottom:2px solid #c8a24a; padding-bottom:6mm; margin-bottom:6mm }}
header .kick {{ color:#c8a24a; letter-spacing:.3em; font-size:11pt }}
header h1 {{ margin:2mm 0 1mm; font-size:30pt; color:#f3e3b5 }}
header p {{ margin:0; font-size:12pt; color:#b3a68c }}
.list {{ flex:1; display:flex; flex-direction:column; gap:4mm }}
.card {{ flex:1; display:flex; align-items:center; gap:6mm; background:#1f1a13; border:1px solid #3a3020; border-radius:4mm; padding:4mm 5mm }}
.card img {{ width:26mm; height:26mm; border-radius:5mm; flex:none }}
.txt {{ flex:1 }}
.genre {{ color:#c8a24a; font-size:9.5pt }}
h2 {{ margin:1mm 0 1.5mm; font-size:16pt; color:#f3e3b5 }}
p {{ margin:0; font-size:10pt; line-height:1.5; color:#c9bca2 }}
.qr {{ width:29mm; flex:none; text-align:center; font-size:8pt; color:#b3a68c }}
.qr svg {{ width:29mm; height:29mm; display:block; background:#fff; padding:1.5mm; border-radius:2mm }}
footer {{ margin-top:5mm; text-align:center; font-size:9.5pt; color:#b3a68c }}
</style></head><body>
<header><div class="kick">HISTORY STRATEGY</div><h1>역사 전략 게임 모음</h1>
<p>Google Play에서 무료로 즐기세요</p></header>
<div class="list">{''.join(cards)}</div>
<footer>QR을 카메라로 비추면 Google Play 페이지로 바로 연결됩니다 · wailfate</footer>
</body></html>"""

out = ROOT / "flyer"
out.mkdir(exist_ok=True)
(out / "flyer.html").write_text(page, encoding="utf-8")
uri = (out / "flyer.html").resolve().as_uri()
base = [CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer"]
subprocess.run(base + [f"--print-to-pdf={out / 'flyer.pdf'}", uri], check=True)
subprocess.run(
    [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2",
     "--window-size=794,1123", f"--screenshot={out / 'flyer.png'}", uri], check=True)
print("done", len(games), "games")
