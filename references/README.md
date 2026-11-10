# 이브리프 장표·쇼츠 기준 아티팩트

새 이브리프 장표나 쇼츠를 만들 때 매번 이 폴더를 먼저 열어 본다.
스킬(`ebrief-cardnews-shorts`) 문서에 적힌 기준 회차와 사용자가 직접 지정한 최근 2개 회차를 claude.ai 아티팩트에서 그대로 받아 둔 사본이다.
2026-11-10에 받았다.

- 폴더마다 `index.html`(장표 페이지 원본), `logo_red.png`, 사용 이미지가 들어 있다. `preview_fullpage.png`는 한눈에 보기용 캡처다.
- 새 회차는 이 사본을 덮어쓰지 말고, `<style>`과 마크업을 복사해 새 폴더에서 내용만 바꾼다.
- 지도 SVG 경로 데이터 때문에 01, 03, X1, X2의 `index.html`은 60~85KB다. 구조만 볼 때는 `sed -E 's/ d="[^"]{80,}"/ d="…"/g' index.html`로 경로 데이터를 지우고 본다.

## 목록

| 폴더 | 회차 | 역할 | 원본 아티팩트 (slug) |
|---|---|---|---|
| `01_기준본_中조사선_해저케이블_20261102` | 中 조사선 대만 해저케이블 4장 | **기준본**. 쇼츠 스타일·긴 페이지 구조의 출발점. 지도(.map)·사진(.photo) 장표 예시 | https://claude.ai/artifact/Npw4BC9QLyHnZxh9Mgz7pF (b0c12e75-2d3b-4aeb-a148-c398facfbb64) |
| `02_최신정방형_특전사_모델워킹_20261105` | 특전사 모델 워킹 교육 논란 4장 | 스킬이 꼽은 **최신 정방형 결과물**. 상단바·카테고리바 10% 확대 반영. 사실 정리표(.facts), 발언 모음(.voices), 해명→인정(.turn) 예시 | https://claude.ai/artifact/ULjXAYNEdeotgAtVYq9ye2 (dd681452-26a1-4fe4-902a-33f8f2d47c63) |
| `03_마크업참고_北대남확성기_20261101` | 北 대남 확성기 5장 | **타임라인(.tl)·인용(.verdict) 마크업만** 참고. 장마다 붙은 하단바·쪽수·장표 간격·그림자는 옛 방식이라 가져오지 않는다 | https://claude.ai/artifact/AA97ERf1WZnrS5PrNh2gRi (4a28f031-9865-4183-a94e-c9648998641d) |
| `04_최근회차_北자폭드론_軍드론추락_20261107` | 北 자폭드론 vs 우리 군 드론 추락 6장 | **사용자 지정 최근 기준**. 수치 강조(.stat)+도식 SVG(.launch), 프로필 박스(.duo), 기종 타일(.spec) 예시 | https://claude.ai/artifact/H9L5aNS1uekPZMVNMune13 (82bbed2f-239d-4b1c-9222-0f94c5fdf43e) |
| `05_최근회차_北해커_평양아파트_20261109` | 해킹 성공하면 평양 40평 아파트 5장 | **사용자 지정 최근 기준**(가장 최신). 선발 깔때기(.funnel), 보상 목록(.perks) 예시 | https://claude.ai/artifact/JEEddZsCmABbUNN3ixNSYi (8b846d4e-5c2e-493b-ad3f-68c605131e0b) |
| `X1_폐기_4x3_北강철비_20261106` | 北 강철비 비행장 타격 4장 | **폐기된 가로 4:3·큰 글자판.** 무엇을 하지 말아야 하는지 확인하는 용도. 따라 하지 않는다 | https://claude.ai/artifact/D1TTiKsFm4ez2fjduAkjYW (613df887-a2a1-41c5-8c67-6b13e7fa63d3) |
| `X2_폐기_4x3_울릉도北어선표류_20261106` | 울릉도 북방 北 어선 표류 4장 | **폐기된 가로 4:3·큰 글자판** (X1과 같음) | https://claude.ai/artifact/NyEYDgH9dyspst3J38BEaf (b1e9e7fe-440d-47ac-9743-80546de950f4) |

## 최근 회차(04·05)에서 스킬 문서와 다르게 바뀐 점

스킬 문서보다 나중에 만든 회차라 문서에 없는 변경이 있다. 아래 줄들은 04·05의 `<style>` 끝부분에 공통으로 들어 있다.

```css
.cover .headline{font-size:32.4px}      /* 표지 헤드라인: 스킬 문서 40px → 32.4px (표지 section에 class="card cover") */
#card1 .headline{font-size:32.4px}
.tl li{grid-template-columns:92px 1fr!important;column-gap:12px!important}   /* 타임라인 날짜 칸 74px → 92px */
.tl .d{font-size:18.5px!important;white-space:nowrap}                         /* 날짜 줄바꿈 금지 */
.tl + .lede{margin-top:14px;font-size:18px;line-height:1.65}
.facts + .lede{margin-top:16px}
```

- 타임라인 날짜는 `8.25`, `9.16`, `10.1`처럼 짧은 점 표기를 쓴다(03 확성기도 `10.21` 표기).
- 사진 캡션은 `<figure class="photo"><img …><figcaption>…</figcaption></figure>`처럼 figure 안에 둔다.
- AI 생성 이미지 캡션: `이해를 돕기 위한 AI 생성 이미지`.
- 표지 분류·기자명 예: `정치 › 북한`, `이브리프 국방부`.
- 매 장의 레이아웃이 모두 다르고, 소재에 맞춰 새 부품(.stat, .duo, .spec, .funnel, .perks)을 직접 짠다.

## 공통 스타일 (모든 정방형 회차 동일)

- 캔버스 논리 480×480 (1080×1080 = 2.25배), 바탕 `#f9f7f2`, 포인트 빨강 `#C8161D`, 하이라이트 `rgba(255,165,0,.68)`를 글자 아래 절반에만 칠한다.
- 제목은 Noto Serif KR 900, 본문은 Noto Sans KR.
- 상단바(.mast)·카테고리바(.nav)는 1장에만, 하단바(.foot, `자료: ○○ 보도 종합`, 쪽수 없음)는 마지막 장에만 둔다.
- 장마다 `<mark>`는 0~1개, 나레이션이 실제로 읽는 구절에만 친다.
