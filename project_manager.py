#!/usr/bin/env python3
"""
Project Management Module
Manages project teams, dependencies, and organizational relationships
"""

from typing import Dict, List
from persistent_client import KnowledgeGraphClient

class ProjectManager:
    def __init__(self):
        self.kg = KnowledgeGraphClient()
    
    def setup_project(self, project_name: str, team_members: List[str], dependencies: List[str]):
        """Initialize project in knowledge graph"""
        # Add project entity
        self.kg.add_entity("project", project_name, {
            "name": project_name,
            "status": "active",
            "created_date": "2024-01-01"
        })
        
        # Add team members and relationships
        for member in team_members:
            self.kg.add_entity("person", member, {"name": member, "role": "developer"})
            self.kg.add_relationship(member, project_name, "works_on")
        
        # Add dependencies
        for dep in dependencies:
            self.kg.add_entity("dependency", dep, {"name": dep, "type": "library"})
            self.kg.add_relationship(project_name, dep, "depends_on")
    
    def find_project_team(self, project_name: str) -> List[str]:
        """Find all team members working on a project"""
        query = f"MATCH (p:person)-[:works_on]->(proj:project {{name: '{project_name}'}}) RETURN p.name"
        results = self.kg.query_graph(query)
        return [r.get("name") for r in results]
    
    def find_shared_dependencies(self, project1: str, project2: str) -> List[str]:
        """Find dependencies shared between projects"""
        query = f"""
        MATCH (p1:project {{name: '{project1}'}})-[:depends_on]->(d:dependency),
              (p2:project {{name: '{project2}'}})-[:depends_on]->(d)
        RETURN d.name
        """
        results = self.kg.query_graph(query)
        return [r.get("name") for r in results]
    
    def find_shared_team_members(self, project1: str, project2: str) -> List[str]:
        """Find team members working on both projects"""
        team1 = set(self.find_project_team(project1))
        team2 = set(self.find_project_team(project2))
        return list(team1 & team2)
    
    def find_developer_projects(self, developer: str) -> List[str]:
        """Find all projects a developer works on"""
        query = f"MATCH (p:person {{name: '{developer}'}})-[:works_on]->(proj:project) RETURN proj.name"
        results = self.kg.query_graph(query)
        return [r.get("name") for r in results]
    
    def find_projects_using_tech(self, technology: str) -> List[str]:
        """Find all projects using a specific technology"""
        query = f"MATCH (proj:project)-[:depends_on]->(d:dependency {{name: '{technology}'}}) RETURN proj.name"
        results = self.kg.query_graph(query)
        return [r.get("name") for r in results]

if __name__ == "__main__":
    pm = ProjectManager()
    
    # Example usage
    pm.setup_project("web-app", ["alice", "bob"], ["react", "nodejs"])
    pm.setup_project("mobile-app", ["bob", "charlie"], ["react-native", "nodejs"])
    
    # Query relationships
    print("Web-app team:", pm.find_project_team("web-app"))
    print("Shared deps:", pm.find_shared_dependencies("web-app", "mobile-app"))