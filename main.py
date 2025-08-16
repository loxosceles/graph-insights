#!/usr/bin/env python3
"""
Graph Insights - Main Application
Analyzes organizational relationships and dependencies
"""

from project_manager import ProjectManager
from code_analyzer import CodeAnalyzer  
from research_assistant import ResearchAssistant

def main():
    print("🧠 Graph Insights - Relationship Analysis")
    print("=" * 50)
    
    # Load sample organizational data
    print("\n🔧 Loading sample data...")
    pm = ProjectManager()
    
    # Create realistic projects with overlapping teams and dependencies
    pm.setup_project("e-commerce-web", ["alice", "bob", "carol"], ["react", "nodejs", "postgresql", "redis"])
    pm.setup_project("mobile-app", ["bob", "david", "eve"], ["react-native", "nodejs", "postgresql"])
    pm.setup_project("analytics-service", ["carol", "frank", "alice"], ["python", "pandas", "postgresql", "redis"])
    pm.setup_project("payment-gateway", ["david", "grace"], ["java", "spring", "postgresql"])
    
    print("✅ Analyzed 4 projects with 7 developers and 8 technologies")
    
    # 1. Project Management Insights
    print("\n📋 PROJECT MANAGEMENT INSIGHTS")
    print("-" * 40)
    
    print("\n🔍 Team Compositions:")
    for project in ["e-commerce-web", "mobile-app", "analytics-service", "payment-gateway"]:
        team = pm.find_project_team(project)
        print(f"  {project}: {team} ({len(team)} members)")
    
    print("\n🔗 Cross-Project Collaborations:")
    collaborations = [
        ("e-commerce-web", "mobile-app"),
        ("e-commerce-web", "analytics-service"),
        ("mobile-app", "payment-gateway")
    ]
    
    for p1, p2 in collaborations:
        shared_team = pm.find_shared_team_members(p1, p2)
        shared_deps = pm.find_shared_dependencies(p1, p2)
        print(f"  {p1} ↔ {p2}:")
        print(f"    Shared team: {shared_team}")
        print(f"    Shared tech: {shared_deps}")
    
    print("\n👥 Developer Workload:")
    for dev in ["alice", "bob", "carol", "david"]:
        projects = pm.find_developer_projects(dev)
        print(f"  {dev}: {len(projects)} projects → {projects}")
    
    print("\n🛠️ Technology Usage:")
    for tech in ["postgresql", "nodejs", "react"]:
        projects = pm.find_projects_using_tech(tech)
        print(f"  {tech}: used in {len(projects)} projects → {projects}")
    
    # 2. Research Demo with meaningful connections
    print("\n\n📚 RESEARCH COLLABORATION NETWORK")
    print("-" * 40)
    
    assistant = ResearchAssistant()
    
    # Load research collaboration data
    assistant.add_paper("Graph Neural Networks Survey", ["Dr. Alice Chen", "Prof. Bob Wilson"], ["graph theory", "deep learning", "neural networks"], 2023)
    assistant.add_paper("Knowledge Graphs in Enterprise", ["Dr. Carol Davis", "Dr. Alice Chen"], ["knowledge representation", "enterprise systems", "graph databases"], 2023)
    assistant.add_paper("Deep Learning for NLP", ["Prof. Bob Wilson", "Dr. Eve Martinez"], ["deep learning", "natural language processing", "transformers"], 2024)
    assistant.add_paper("Graph Databases at Scale", ["Dr. Frank Thompson", "Dr. Carol Davis"], ["graph databases", "scalability", "distributed systems"], 2024)
    
    print("\n🔬 Research Topics & Papers:")
    for topic in ["deep learning", "graph databases", "knowledge representation"]:
        papers = assistant.find_related_papers(topic)
        print(f"  {topic}: {len(papers)} papers → {papers}")
    
    print("\n🤝 Potential Collaborations:")
    for author in ["Dr. Alice Chen", "Prof. Bob Wilson"]:
        collabs = assistant.find_author_collaborations(author)
        if collabs:
            print(f"  {author} could collaborate with:")
            for collab in collabs[:2]:  # Show top 2
                print(f"    → {collab.get('name')} (shared interest: {collab.get('topic')})")
    
    print("\n💡 Research Suggestions:")
    suggestions = assistant.suggest_research_directions(["deep learning", "graph databases"])
    print(f"  Based on current trends: {suggestions[:3]}")
    
    print("\n\n⭐ GRAPH INSIGHTS CAPABILITIES")
    print("=" * 50)
    print("\n🎯 What traditional databases struggle with:")
    print("  • Finding indirect connections (Alice works with Bob, Bob works with David)")
    print("  • Multi-hop relationships (shared technologies across project chains)")
    print("  • Dynamic recommendations (suggest collaborators based on research overlap)")
    print("  • Impact analysis (if PostgreSQL has issues, which projects are affected?)")
    
    print("\n🚀 Knowledge Graph advantages:")
    print("  ✅ Natural relationship modeling")
    print("  ✅ Flexible schema evolution")
    print("  ✅ Complex query patterns")
    print("  ✅ Recommendation engines")
    print("  ✅ Network analysis capabilities")

if __name__ == "__main__":
    main()