import asyncio
import hashlib
import time
from dataclasses import dataclass, field
from typing import List, Dict, Optional, AsyncGenerator

@dataclass
class DocumentChunk:
    chunk_id: str
    source_url: str
    text_content: str
    token_estimate: int
    metadata: Dict[str, str] = field(default_factory=dict)

@dataclass
class VectorRecord:
    chunk_id: str
    embedding: List[float]
    metadata: Dict[str, str]

class TextProcessor:
    @staticmethod
    def chunk_text(text: str, chunk_size: int = 200, overlap: int = 40) -> List[str]:
        words = text.split()
        if not words:
            return []
        
        chunks = []
        step = chunk_size - overlap
        for i in range(0, len(words), step):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append(chunk)
            if i + chunk_size >= len(words):
                break
        return chunks

    @staticmethod
    def compute_hash(text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]

class MockEmbeddingEngine:
    DIMENSION = 384

    async def generate_batch_embeddings(self, texts: List[str]) -> List[List[float]]:
        await asyncio.sleep(0.05 * (len(texts) / 10 + 0.1))
        
        embeddings = []
        for text in texts:
            seed = sum(ord(c) for c in text[:20]) % 100
            vec = [(seed + i) / 1000.0 for i in range(self.DIMENSION)]
            norm = (sum(x**2 for x in vec)) ** 0.5 or 1.0
            normalized = [round(x / norm, 5) for x in vec]
            embeddings.append(normalized)
        return embeddings

class AsyncIngestionPipeline:
    def __init__(self, max_concurrency: int = 4, batch_size: int = 16):
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.batch_size = batch_size
        self.text_processor = TextProcessor()
        self.embedding_engine = MockEmbeddingEngine()

    async def fetch_document(self, url: str) -> Optional[str]:
        async with self.semaphore:
            try:
                await asyncio.sleep(0.08)
                return f"Simulated technical documentation content fetched from {url}. " * 15
            except Exception as e:
                print(f"[ERROR] Failed to fetch {url}: {e}")
                return None

    async def process_url(self, url: str) -> List[DocumentChunk]:
        raw_text = await self.fetch_document(url)
        if not raw_text:
            return []

        raw_chunks = self.text_processor.chunk_text(raw_text, chunk_size=50, overlap=10)
        chunks = []
        for idx, text in enumerate(raw_chunks):
            chunk_hash = self.text_processor.compute_hash(text)
            chunks.append(
                DocumentChunk(
                    chunk_id=f"{chunk_hash}_{idx}",
                    source_url=url,
                    text_content=text,
                    token_estimate=len(text.split()),
                    metadata={"source": url, "index": str(idx)}
                )
            )
        return chunks

    async def batch_generator(self, chunks: List[DocumentChunk]) -> AsyncGenerator[List[DocumentChunk], None]:
        for i in range(0, len(chunks), self.batch_size):
            yield chunks[i:i + self.batch_size]

    async def run(self, urls: List[str]) -> List[VectorRecord]:
        start_time = time.perf_counter()
        print(f"[PIPELINE] Starting ingestion across {len(urls)} target URLs...")

        tasks = [self.process_url(url) for url in urls]
        chunk_lists = await asyncio.gather(*tasks)
        all_chunks = [chunk for sublist in chunk_lists for chunk in sublist]
        print(f"[PIPELINE] Extracted {len(all_chunks)} chunks across all sources.")

        vector_index: List[VectorRecord] = []
        async for batch in self.batch_generator(all_chunks):
            texts = [c.text_content for c in batch]
            embeddings = await self.embedding_engine.generate_batch_embeddings(texts)
            for chunk, emb in zip(batch, embeddings):
                vector_index.append(
                    VectorRecord(
                        chunk_id=chunk.chunk_id,
                        embedding=emb,
                        metadata=chunk.metadata
                    )
                )

        elapsed = time.perf_counter() - start_time
        print(f"[PIPELINE] Successfully indexed {len(vector_index)} vectors in {elapsed:.2f}s.")
        return vector_index

async def main():
    sample_urls = [
        f"https://docs.example.org/ml/section_{i}"
        for i in range(1, 9)
    ]
    pipeline = AsyncIngestionPipeline(max_concurrency=4, batch_size=8)
    indexed_records = await pipeline.run(sample_urls)
    
    print("\n--- Pipeline Sample Output ---")
    if indexed_records:
        sample = indexed_records[0]
        print(f"Sample Record ID: {sample.chunk_id}")
        print(f"Embedding Dims  : {len(sample.embedding)}")
        print(f"Vector Slice    : {sample.embedding[:5]}...")
        print(f"Metadata        : {sample.metadata}")

if __name__ == "__main__":
    asyncio.run(main())
