"""
Summarization Agent - Generates TL;DR summaries
"""

import sys
import os
from typing import List, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class SummarizationAgent:
    """
    Generates concise summaries for news articles.
    Uses extractive summarization based on keyword importance.
    """

    def __init__(self, request_id: str):
        self.request_id = request_id
        self.name = "Summarizer"

    async def summarize(self, articles: List[dict], sentiments: List[dict] = None) -> List[dict]:
        """Generate summaries for all articles"""
        print(f"[{self.name}] Generating summaries. ..")

        summaries = []
        for article in articles:
            summary = await self._generate_summary(article)
            summaries.append({**article, "summary": summary})

        return summaries

    async def _generate_summary(self, article: dict) -> str:
        """Generate a concise summary using extractive method"""
        title = article.get("title", "")
        summary_text = article.get("summary", "") or article.get("title", "")

        # Use title as lead + first key sentences from summary
        sentences = self._split_into_sentences(summary_text)

        # Score sentences by importance
        scored_sentences = []
        for sentence in sentences:
            score = self._score_sentence(sentence, article.get("keywords", []))
            scored_sentences.append((sentence, score))

        # Select top sentences
        top_sentences = sorted(scored_sentences, key=lambda x: x[1], reverse=True)[:2]

        # Construct summary
        if top_sentences:
            return f"{title}: {top_sentences[0][0].strip()}{' | '.join(s[0].strip() for s in top_sentences[1:])}" if len(top_sentences) > 1 else top_sentences[0][0].strip()
        else:
            return summary_text[:200] + "..." if len(summary_text) > 200 else summary_text

    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        # Simple sentence splitting
        sentences = []
        current = []

        for char in text:
            current.append(char)
            if char in ".!?":
                sentence = " ".join(current).strip()
                if sentence:
                    sentences.append(sentence)
                current = []
        else:
            # Handle trailing text
            sentence = " ".join(current).strip()
            if sentence:
                sentences.append(sentence)

        return sentences

    def _score_sentence(self, sentence: str, keywords: List[str]) -> float:
        """Score sentence based on keyword presence"""
        score = 0
        sentence_lower = sentence.lower()

        # Boost title keywords
        title_lower = sentence.lower()
        for keyword in keywords:
            if keyword in title_lower:
                score += 2
            elif keyword in sentence_lower:
                score += 1

        # Boost if sentence contains article title
        if len(sentence) < len(title.lower()):
            if title.lower() in sentence_lower:
                score += 3

        return score
