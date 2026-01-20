📝 행정 공고문 순화 및 정보 접근성 향상 서비스
LangChain 기반의 RAG 파이프라인을 활용한 행정 용어 자동 순화 및 요약 시스템

🎯 1. 프로젝트 목적 (Project Objective)
기존의 행정 공고문과 포스터는 축약된 정보와 어려운 행정 전문 용어로 인해 일반 시민, 특히 정보 취약 계층이 구체적인 복지 혜택을 파악하는 데 높은 진입장벽이 존재합니다.

본 프로젝트는 AI 에이전트 체인을 통해 다음과 같은 문제를 해결합니다:

정보 장벽 해소: 난해한 행정 용어를 초등학생도 이해할 수 있는 쉬운 우리말로 순화.

가독성 극대화: 핵심 내용을 추출하여 요약된 형태로 제공.

신뢰성 보장: RAG(검색 증강 생성)를 통해 공신력 있는 행정 가이드라인에 근거한 정보 제공 및 의미 왜곡 검증.

🛠 2. 핵심 기술 스택 (Tech Stack)
Orchestration: LangChain (LCEL 문법 사용)

LLM: Azure OpenAI (GPT-4o)

RAG Infrastructure:

WebBaseLoader (공공 정책 데이터 크롤링)

PyPDFLoader (행정 가이드라인 분석)

Vector Store (Supabase 기반 지식 베이스 구축 예정)

Validation: PydanticOutputParser를 이용한 구조화된 데이터 검증

🏗 3. 시스템 아키텍처 (Architecture)
본 프로젝트는 실용적 계층형 아키텍처를 따르며, 각각의 에이전트가 체인으로 연결되어 작동합니다.

Extractor: Pydantic을 활용하여 문서 내 어려운 용어 및 핵심 정보 구조화.

Translator: Few-Shot Prompting 기법을 적용하여 행정 용어를 순화어로 변환.

Validator: 원문과 순화문을 대조하여 의미 왜곡 여부를 정밀 검증(Hallucination Check).

Workflow Service: 모든 에이전트의 흐름을 제어하는 컨트롤 타워.

🚀 4. 현재 진행 상황 (Current Progress)
[x] LangChain 환경 설정 및 Azure OpenAI 연동

[x] LCEL 기반의 기본 invoke, stream, batch 파이프라인 구축

[x] Pydantic을 활용한 행정 용어 정보 추출기(Schema Parser) 구현

[x] WebBaseLoader를 이용한 공공 정책 데이터 수집 테스트 성공

📥 설치 및 실행 방법
# 저장소 복제
git clone https://github.com/사용자명/프로젝트명.git

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
# .env 파일 생성 후 AZURE_OPENAI_API_KEY 등을 입력하세요.

## 🛠 Troubleshooting Log: PDF Text Extraction
### ❌ 문제 상황 (Problem)
- [cite_start]일반적인 `PyPDFLoader` 사용 시 이미지로 구성된 행정 공고문 PDF에서 텍스트 추출 실패. [cite: 1349, 1395]
- [cite_start]윈도우 환경에서 `Unstructured` 로더 사용 시 Poppler 및 Tesseract OCR 엔진 설치가 필수적이며, 시스템 환경 변수 설정 등 의존성 관리가 매우 까다로움. [cite: 1481]

### 🔍 원인 분석 (Analysis)
- [cite_start]행정 공고문 PDF는 텍스트 레이어가 없는 '통 이미지' 형태가 많아 OCR 엔진 없이는 일반적인 라이브러리로 읽을 수 없음. [cite: 1469, 1479]

### ✅ 해결 방안 (Solution)
- 외부 엔진 설치 없이 파이썬 라이브러리 수준에서 이미지 레이어를 강제로 분석하는 `pdfplumber`를 대안으로 채택.
- [cite_start]`pdf_test.py`를 통해 텍스트 레이어를 강제 추출하고 이를 LangChain의 `Document` 객체로 정형화하는 데 성공. [cite: 1336, 1386]
