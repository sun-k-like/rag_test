from langchain_community.document_loaders import WebBaseLoader

# 1. WebBaseLoader 설정
# 실무에서는 봇 차단 방지를 위해 User-Agent 설정이 필수입니다.
loader = WebBaseLoader(
    web_path="https://docs.smith.langchain.com",
    header_template={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    },
    requests_kwargs={"timeout": 10} # 10초 대기 설정
)

# 2. 문서 로드 실행
print("데이터를 불러오는 중입니다...")
docs = loader.load()

# 3. 결과 및 메타데이터 확인 (KPI 관리처럼 정량적 확인)
print("-" * 30)
print(f"1. 로드된 문서 개수: {len(docs)}개")
print(f"2. 첫 번째 문서 글자 수: {len(docs[0].page_content)}자")
print(f"3. 메타데이터(출처): {docs[0].metadata.get('source')}")
print(f"4. 문서 제목: {docs[0].metadata.get('title')}")
print("-" * 30)

# 첫 200자만 미리보기
print("내용 미리보기:")
print(docs[0].page_content[:200].strip())