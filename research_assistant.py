#!/usr/bin/env python3
"""
Research Collaboration Module
Analyzes research networks, papers, and collaboration opportunities
"""

from persistent_client import KnowledgeGraphClient
from typing import List, Dict

class ResearchAssistant:
    def __init__(self):
        self.kg = KnowledgeGraphClient()
    
    def add_paper(self, title: str, authors: List[str], topics: List[str], year: int):
        """Add research paper to knowledge graph"""
        paper_id = title.replace(" ", "_").lower()
        
        self.kg.add_entity("paper", paper_id, {
            "title": title,
            "year": year,
            "type": "research_paper"
        })
        
        # Add authors
        for author in authors:
            author_id = author.replace(" ", "_").lower()
            self.kg.add_entity("author", author_id, {"name": author})
            self.kg.add_relationship(author_id, paper_id, "authored")
        
        # Add topics
        for topic in topics:
            topic_id = topic.replace(" ", "_").lower()
            self.kg.add_entity("topic", topic_id, {"name": topic})
            self.kg.add_relationship(paper_id, topic_id, "covers")
    
    def add_concept(self, concept: str, related_papers: List[str], description: str = ""):
        """Add research concept and link to papers"""
        concept_id = concept.replace(" ", "_").lower()
        
        self.kg.add_entity("concept", concept_id, {
            "name": concept,
            "description": description
        })
        
        for paper_title in related_papers:
            paper_id = paper_title.replace(" ", "_").lower()
            self.kg.add_relationship(concept_id, paper_id, "discussed_in")
    
    def find_related_papers(self, topic: str) -> List[str]:
        """Find papers covering a specific topic"""
        topic_id = topic.replace(" ", "_").lower()
        query = f"""
        MATCH (p:paper)-[:covers]->(t:topic {{name: '{topic}'}})
        RETURN p.title
        """
        results = self.kg.query_graph(query)
        return [r.get("title") for r in results]
    
    def find_author_collaborations(self, author: str) -> List[Dict]:
        """Find potential collaborators based on shared topics"""
        author_id = author.replace(" ", "_").lower()
        query = f"""
        MATCH (a1:author {{name: '{author}'}})-[:authored]->(p1:paper)-[:covers]->(t:topic),
              (a2:author)-[:authored]->(p2:paper)-[:covers]->(t)
        WHERE a1 <> a2
        RETURN a2.name, t.name, count(*) as shared_topics
        ORDER BY shared_topics DESC
        """
        results = self.kg.query_graph(query)
        return results
    
    def suggest_research_directions(self, current_topics: List[str]) -> List[str]:
        """Suggest new research directions based on current interests"""
        suggestions = []
        for topic in current_topics:
            topic_id = topic.replace(" ", "_").lower()
            query = f"""
            MATCH (t1:topic {{name: '{topic}'}})<-[:covers]-(p:paper)-[:covers]->(t2:topic)
            WHERE t1 <> t2
            RETURN t2.name, count(*) as frequency
            ORDER BY frequency DESC
            LIMIT 5
            """
            results = self.kg.query_graph(query)
            suggestions.extend([r.get("name") for r in results])
        
        return list(set(suggestions))

if __name__ == "__main__":
    assistant = ResearchAssistant()
    
    # Add sample research data
    assistant.add_paper(
        "Deep Learning for NLP",
        ["John Smith", "Jane Doe"],
        ["machine learning", "natural language processing"],
        2023
    )
    
    assistant.add_paper(
        "Transformer Architecture",
        ["Jane Doe", "Bob Wilson"],
        ["machine learning", "attention mechanisms"],
        2022
    )
    
    assistant.add_concept(
        "attention mechanism",
        ["Deep Learning for NLP", "Transformer Architecture"],
        "Key component in modern neural networks"
    )
    
    # Query research connections
    print("ML papers:", assistant.find_related_papers("machine learning"))
    print("Collaborators for Jane Doe:", assistant.find_author_collaborations("Jane Doe"))
    print("Research suggestions:", assistant.suggest_research_directions(["machine learning"]))