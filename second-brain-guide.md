# 세컨드 브레인 구축 가이드

> 작성일: 2026-10-13
> 핵심 아이디어: **뇌는 아이디어를 저장하는 곳이 아니라 만들어내는 곳이다.** 저장과 정리는 외부 시스템(세컨드 브레인)에 맡기고, 뇌는 생각과 창작에 집중한다.

---

## 1. 기본 프레임워크: BASB (Building a Second Brain)

Tiago Forte가 2017년에 공개하고 2022년에 같은 이름의 책으로 정리한 개인 지식 관리(PKM) 방법론이다. **CODE**(작업 흐름)와 **PARA**(정리 구조) 두 축으로 구성된다.

### 1-1. CODE 방법 — 정보를 결과물로 바꾸는 4단계

| 단계 | 의미 | 실천 방법 |
|------|------|-----------|
| **C**apture (수집) | 마음에 와닿는 것을 저장 | 호기심·놀라움·흥미를 느낀 부분만 저장한다. 글·영상 전체가 아니라 **가장 와닿는 발췌**만 남긴다. 너무 많이 모으지 않는 것이 핵심이다. |
| **O**rganize (정리) | 주제가 아니라 **쓰임새** 기준으로 분류 | "이 메모가 어떤 프로젝트를 진척시키는가?"를 기준으로 PARA 폴더에 넣는다. |
| **D**istill (요약) | 핵심만 남도록 점진적으로 압축 | **점진적 요약(Progressive Summarization)**: 메모를 다시 볼 때 핵심을 **굵게**, 그중 가장 중요한 부분을 ==형광펜==으로 표시하고, 맨 위에 1~2줄 요약을 단다. |
| **E**xpress (표현) | 메모를 실제 결과물로 만들기 | 보고서, 제안서, 발표 자료, 블로그 글 등. **가장 중요한 단계**이며 나머지 세 단계는 모두 이 단계를 위해 존재한다. |

### 1-2. PARA 구조 — 실행 가능성 순으로 정리

```
📁 1_Projects   (프로젝트)  기한과 목표가 있는 일    예: "OO시 DRT 제안서 작성"
📁 2_Areas      (영역)      꾸준히 책임지는 분야      예: "건강", "팀 관리", "재무"
📁 3_Resources  (자료)      관심 주제의 참고 자료     예: "교통 정책", "AI 도구"
📁 4_Archives   (보관)      끝났거나 쓰지 않는 항목   예: 완료된 프로젝트
```

- **프로젝트부터** 정리한다. 지금 진행 중인 프로젝트에 쓸 수 있는 메모는 프로젝트 폴더에 넣는다.
- 당장 쓸 프로젝트가 없으면 → 영역, 그것도 아니면 → 자료.
- 프로젝트가 끝나면 통째로 보관 폴더로 옮긴다. (지우지 않는다.)

---

## 2. 보완 방법론: 제텔카스텐 (Zettelkasten)

PARA가 **"실행"** 중심이라면 제텔카스텐은 **"생각의 연결"** 중심이다. 둘은 함께 쓸 수 있다.

- **원자적 메모**: 메모 하나에 아이디어 하나만 담는다.
- **자기 말로 쓰기**: 복사가 아니라 이해한 내용을 직접 다시 쓴다.
- **양방향 링크**: 메모끼리 `[[링크]]`로 연결해 지식 네트워크를 만든다.
- **직접 연결하기**: 두 메모를 연결하는 행위 자체가 학습이다. 이 과정을 AI에 전부 맡기지 않는다.

---

## 3. 도구 선택

> **가장 좋은 도구는 꾸준히 쓰게 되는 도구다.**

| 유형 | 대표 도구 | 잘 맞는 사람 |
|------|-----------|--------------|
| 그래프·링크형 | **Obsidian** | 개인정보를 중시하는 사람, 제텔카스텐 사용자. 로컬 저장, Markdown, 플러그인, 그래프 뷰. AI는 직접 연동해야 하고 배우는 데 시간이 걸린다. |
| 구조화형 | Notion, Microsoft Loop | 데이터베이스, 협업, 템플릿을 원하는 사람 |
| 하이브리드 | AFFiNE, Capacities, Tana | 문서·화이트보드 통합, AI 기본 내장을 원하는 사람 |
| 리서치형 | NotebookLM | 문서 기반 질의응답, 자료 조사 |

**추천 조합**: Obsidian(원본 저장소, 로컬 Markdown) + AI 도구(수집·요약·검색 보조)

---

## 4. AI 시대의 세컨드 브레인 운영 원칙

1. **문제는 시스템이 아니라 유지 관리다.** 지루한 일(분류, 태깅, 요약, 녹취 정리)은 AI에 맡긴다.
2. **생각과 연결은 사람이 한다.** AI가 자동으로 만든 연결은 근거 없는 엉뚱한 연결일 수 있으니 반드시 검토한다.
3. **정보는 넘치니 맥락이 가치다.** AI로 정보를 찾기는 쉬워졌다. "이 정보가 내 일에 어떤 의미인가"라는 맥락을 메모에 남긴다.
4. **데이터는 내가 소유한다.** 로컬 우선, Markdown 같은 개방형 포맷을 쓰면 도구를 바꿔도 지식이 남는다.

---

## 5. 실천 루틴 (바로 시작하기)

### 1주차: 세팅
- [ ] 도구 하나 고르기 (추천: Obsidian)
- [ ] PARA 폴더 4개 만들기
- [ ] 현재 진행 중인 프로젝트 목록을 `1_Projects`에 폴더로 만들기
- [ ] 수집 통로 하나로 모으기 (모바일 빠른 메모, 웹 클리퍼, 받은편지함 노트)

### 매일 (5분)
- [ ] 와닿은 내용만 `Inbox`에 빠르게 수집 (정리는 나중에)

### 매주 (30분 주간 리뷰)
- [ ] Inbox 비우기 → PARA 폴더로 분류
- [ ] 이번 주 다시 본 메모에 점진적 요약 한 단계 적용
- [ ] 끝난 프로젝트는 Archives로 이동
- [ ] 관련 메모끼리 링크 연결

### 매월
- [ ] 메모로 결과물 하나 만들기 (Express) — 보고서, 발표, 글
- [ ] 영역(Areas) 점검: 소홀했던 책임 영역 확인

---

## 6. 메모 작성 팁

- **미래의 나를 위해 쓴다.** 출처, 저장 이유, 한 줄 요약을 남겨 나중에 바로 이해할 수 있게 한다.
- **메모 템플릿 예시**

```markdown
---
created: 2026-10-13
source: (URL / 책 / 회의)
project: [[프로젝트명]]
tags: [주제]
---
## 한 줄 요약
(가장 중요한 내용 1~2문장)

## 핵심 내용
- **굵게 표시한 핵심**
- ==가장 중요한 부분==

## 내 생각 / 활용 아이디어
(이 정보를 어디에 어떻게 쓸지)

## 관련 메모
- [[관련 메모 1]]
```

---

## 참고 자료

- [Book summary: Building a Second Brain (mmapped.blog)](https://mmapped.blog/posts/16-building-a-second-brain)
- ['Building a Second Brain' by Tiago Forte (Charter)](https://www.charterworks.com/building-second-brain-tiago-forte/)
- [What Is a Second Brain? How To Build One (Management Consulted)](https://managementconsulted.com/what-is-a-second-brain/)
- [The P.A.R.A Method Explained (Substack)](https://thevicmontano.substack.com/p/get-organized-like-a-pro-the-para)
- [Build a second brain (Fabric)](https://developers.fabric.so/learn/build-a-second-brain)
- [Summary: Building a Second Brain (Medium)](https://medium.com/@subin.khullar/summary-building-a-second-brain-dd80989b1f87)
- [Best second brain apps (AFFiNE)](https://affine.pro/blog/best-second-brain-apps)
- [The Second Brain Playbook 2026 Edition (Viblo)](https://viblo.asia/p/the-second-brain-playbook-2026-edition-1XVOW7MXVMz)
- [AI Personal Knowledge Management System 2026 (Nexasphere)](https://nexasphere.io/blog/ai-personal-knowledge-management-system-2026)
- [PKM 세컨드 브레인 AI Obsidian 2026 (youngju.dev)](https://www.youngju.dev/blog/culture/2026-03-16-pkm-second-brain-ai-obsidian-2026)
- [AI-first knowledge base: OpenKnowledge vs Notion vs Obsidian (AI Indigo)](https://aiindigo.com/blog/the-ai-first-knowledge-base-comparing-openknowledge-to-notion-and-obsidian)
- [Second Brain & PKM (BibiGPT)](https://growth.bibigpt.co/en/blog/topics/pkm-second-brain)
