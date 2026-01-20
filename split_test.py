import os
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import AzureOpenAIEmbeddings

load_dotenv()

# 1. 분할할 데이터 준비 (PDF에서 추출했어야 할 핵심 내용)
raw_text = """
2026년 꼭 알아야 할 청년정책 요약:
1. 일자리 분야: 국민취업지원제도 구직활동지원금이 50만원에서 60만원으로 인상됩니다. 비수도권 중소기업 취업 청년에게는 720만원의 일자리도약장려금이 지원됩니다.
2. 주거 분야: 청년 주택드림 청약통장을 통해 전세자금 대출 및 저금리 대출을 지원하며, 무주택 청년에게 월 최대 20만원의 월세를 24개월간 지원합니다.
3. 금융 분야: 청년미래적금이 신설되어 19~34세 청년이 3년 동안 매월 50만원 납입 시 정부가 12%를 매칭 지원합니다.
4. 교육 분야: 국가장학금 지원이 확대되어 연간 최대 600만원까지 지원하며, 주거안정장학금이 신설되어 거주비 20만원을 지원합니다.
"""

# 2. Splitter 설정
# chunk_size: 자르는 단위(글자 수), chunk_overlap: 앞뒤 문맥 유지를 위해 겹치는 글자 수
splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20,
    length_function=len,
    separators=["\n\n", "\n", ".", " ", ""]
)

# 3. 텍스트 분할 실행
chunks = splitter.split_text(raw_text)

# 4. 정량적 결과 확인 (KPI 스타일)
print("\n" + "="*50)
print(f"{'항목':<20} | {'데이터 내용'}")
print("-" * 50)
print(f"{'1. 원본 글자 수':<20} | {len(raw_text)}자")
print(f"{'2. 분할된 조각 수':<20} | {len(chunks)}개")
print(f"{'3. 조각당 평균 길이':<20} | {len(raw_text)//len(chunks)}자")
print("="*50 + "\n")

# 5. 분할된 내용 확인
for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1}: {chunk}")
    print("-" * 30)

# Azure OpenAI 임베딩 모델 초기화
embeddings = AzureOpenAIEmbeddings(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-12-01-preview",
    model="text-embedding-3-small"
)

# ChromaDB 구축 실행 
if 'chunks' in locals() and 'embeddings' in locals():
    vectorstore = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,           # 설정하신 AzureOpenAIEmbeddings 사용
        persist_directory="./chroma_db", # 이 경로에 폴더가 생성됩니다
    )
    print("\n" + "="*50)
    print("✅ 성공: ./chroma_db 폴더가 생성되고 데이터가 저장되었습니다.")
    print("="*50)
else:
    print("❌ 실패: chunks나 embeddings 설정에 문제가 있습니다.")

# 5. Retriever 설정 및 테스트
# k=3: 가장 유사한 조각 3개를 가져오도록 설정
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# 사용자의 질문 예시
query = "청년 주거 지원 정책에 대해 알려줘"
results = retriever.invoke(query)

print(f"\n🔍 '{query}'에 대한 검색 결과:")
for i, doc in enumerate(results):
    print(f"[{i+1}] {doc.page_content}")