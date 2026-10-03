# 게임 상점 (game-shop)

플레이 스토어에 **프로덕션**으로 올라간 게임만 모은 홍보 페이지.

## 게임 추가
1. `games.json` 의 `games` 맨 끝에 한 칸 추가 (id·package·name·tagline·genre·added)
2. 아이콘 256px 을 `img/<id>.png` 로 저장
3. 푸시하면 끝 — 화면은 `games.json` 을 읽어 그린다 (코드 수정 없음)

## 공유 주소
- `https://wailfate.github.io/games/` , 채널별은 `?src=kakao` 처럼 붙인다
- 설치 출처는 플레이 콘솔 획득 통계에 `utm_campaign=<게임 id>` 로 남는다
