from langchain_community.document_loaders import WebBaseLoader

# 1. 대상 URL 설정
url = "https://www.korea.kr/multi/visualNewsView.do?newsId=148924647&cateId=cardnews&pWise=main&pWiseMain=C1_1"

# 2. Loader 설정 (차단 방지 및 타임아웃 적용)
loader = WebBaseLoader(
    web_path=url,
    header_template={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    },
    requests_kwargs={"timeout": 10}
)

# 3. 데이터 로드
print(f"로드 시작: {url}")
docs = loader.load()

# 4. 정량적 결과 요약 (KPI 관리 스타일)
print("\n" + "="*50)
print(f"{'항목':<20} | {'데이터 내용'}")
print("-" * 50)
print(f"{'1. 로드 성공 여부':<20} | {'성공' if len(docs) > 0 else '실패'}")
print(f"{'2. 문서 개수':<20} | {len(docs)} docs")
print(f"{'3. 전체 글자 수':<20} | {len(docs[0].page_content)}자")
print(f"{'4. 메타데이터 출처':<20} | {docs[0].metadata.get('source')}")
print(f"{'5. 페이지 제목':<20} | {docs[0].metadata.get('title')}")
print("="*50 + "\n")

# 5. 추출된 텍스트 일부 출력 (정상 로드 확인용)
print("추출 내용 요약 (앞부분 300자):")
print("-" * 50)
print(docs[0].page_content.replace('\n', ' ').strip()[:300] + "...")