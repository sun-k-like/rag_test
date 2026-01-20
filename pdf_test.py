import pdfplumber
from langchain_core.documents import Document

file_path = "2026년+꼭+알아야+할+청년정책.pdf"
docs = []

print("이미지 스캔 방식으로 분석 중...")

# pdfplumber로 이미지 내 텍스트 레이어 강제 추출
with pdfplumber.open(file_path) as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        if text:
            docs.append(Document(
                page_content=text,
                metadata={"source": file_path, "page": i}
            ))

# 📊 결과 확인 (KPI 스타일)
print("\n" + "="*50)
if docs:
    print(f"{'1. 총 페이지 수':<20} | {len(docs)} pages")
    print(f"{'2. 추출된 글자 수':<20} | {len(docs[0].page_content)}자")
    print(f"{'3. 메타데이터':<20} | {docs[0].metadata}")
    print("="*50 + "\n")
    print("### 추출 내용 미리보기 ###")
    print(docs[0].page_content[:500] + "...")
else:
    print("❌ 텍스트 추출에 실패했습니다. 파일이 완전한 이미지입니다.")
    print("="*50)