"""games.json -> 게임별 홍보 랜딩 페이지 games/<id>/ (og 태그 + og.jpg + 스토어 버튼).
새 게임: games.json 에 칸을 더하고 아래 FEATURE 에 피처 그래픽(1024x500) 경로를 한 줄 더한 뒤 이 스크립트를 돌린다.
공유 주소: https://wailfate.github.io/games/<id>/?src=kakao
"""
import html, json
from pathlib import Path

from PIL import Image, ImageFilter

ROOT = Path(__file__).parent
DEV = Path(r"C:\Users\wailf\Desktop\dev")
SITE = "https://wailfate.github.io/games"
FEATURE = {
    "aod2": "aod2/store_play/play_feature_1024x500.png",
    "samguk": "samguk-web/store_play/feature_graphic_1024x500.png",
    "sengoku": "sengoku/store/feature_1024x500.png",
    "husamguk": "husamguk/build/play/feature-1024x500-ko.png",
    "ohosipyukguk": "ohosipyukguk/store_play/play_feature_1024x500.png",
}
games = json.loads((ROOT / "games.json").read_text(encoding="utf-8"))["games"]

TEMPLATE = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{name}</title>
<meta name="description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{name}">
<meta property="og:title" content="{name}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{site}/{id}/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{name}">
<meta property="og:locale" content="ko_KR">
<meta property="og:url" content="{site}/{id}/">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="icon.png">
<style>
body{{margin:0;background:#14110d;color:#eadfc8;font-family:system-ui,"Malgun Gothic",sans-serif;text-align:center}}
main{{max-width:560px;margin:0 auto;padding:32px 16px}}
img.hero{{width:100%;border-radius:12px;display:block}}
h1{{font-size:1.5rem;margin:20px 0 8px}}
p{{line-height:1.6;color:#c9bca2}}
a.btn{{display:inline-block;margin-top:16px;padding:14px 28px;border-radius:10px;background:#c8a24a;color:#1a1408;font-weight:700;text-decoration:none}}
</style>
</head>
<body>
<main>
<img class="hero" src="og.jpg" alt="{name}">
<h1>{name}</h1>
<p>{desc}</p>
<a class="btn" id="go" href="https://play.google.com/store/apps/details?id={package}&referrer=utm_source%3Dlanding%26utm_medium%3Dshare%26utm_campaign%3D{id}">Google Play에서 받기</a>
</main>
<script>
// 공유 채널 구분: 주소 뒤에 ?src=kakao 처럼 붙이면 플레이 설치 통계에 그 이름이 남는다
var src=new URLSearchParams(location.search).get("src");
if(src){{var g=document.getElementById("go");g.href=g.href.replace("utm_medium%3Dshare","utm_medium%3D"+encodeURIComponent(src));}}
</script>
</body>
</html>
"""

for g in games:
    out = ROOT / g["id"]
    out.mkdir(exist_ok=True)
    f = Image.open(DEV / FEATURE[g["id"]]).convert("RGB")
    bg = f.resize((1200, 630)).filter(ImageFilter.GaussianBlur(24))
    bg.paste(f.resize((1200, 586)), (0, 22))
    bg.save(out / "og.jpg", quality=88)
    Image.open(ROOT / "img" / f"{g['id']}.png").convert("RGBA").resize((256, 256)).save(out / "icon.png")
    page = TEMPLATE.format(name=html.escape(g["name"]), desc=html.escape(g["tagline"]),
                           site=SITE, id=g["id"], package=g["package"])
    (out / "index.html").write_text(page, encoding="utf-8")
    print(g["id"], "->", f"{SITE}/{g['id']}/")
