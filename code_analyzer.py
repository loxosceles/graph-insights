#!/usr/bin/env python3
"""
Code Analysis Module
Extracts and analyzes code structure, dependencies, and relationships
"""

import ast
import os
from typing import Set, Dict, List
from persistent_client import KnowledgeGraphClient

class CodeAnalyzer:
    def __init__(self):
        self.kg = KnowledgeGraphClient()
        
    def analyze_python_file(self, filepath: str):
        """Extract classes, functions, and imports from Python file"""
        with open(filepath, 'r') as f:
            tree = ast.parse(f.read())
        
        filename = os.path.basename(filepath)
        
        # Add file entity
        self.kg.add_entity("file", filename, {
            "path": filepath,
            "type": "python"
        })
        
        # Extract and add classes
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                self.kg.add_entity("class", f"{filename}::{node.name}", {
                    "name": node.name,
                    "file": filename
                })
                self.kg.add_relationship(f"{filename}::{node.name}", filename, "defined_in")
                
            elif isinstance(node, ast.FunctionDef):
                self.kg.add_entity("function", f"{filename}::{node.name}", {
                    "name": node.name,
                    "file": filename
                })
                self.kg.add_relationship(f"{filename}::{node.name}", filename, "defined_in")
                
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    self.kg.add_entity("module", alias.name, {"name": alias.name})
                    self.kg.add_relationship(filename, alias.name, "imports")
    
    def find_function_dependencies(self, function_name: str) -> List[str]:
        """Find what modules a function depends on"""
        query = f"""
        MATCH (f:function {{name: '{function_name}'}})-[:defined_in]->(file:file),
              (file)-[:imports]->(m:module)
        RETURN m.name
        """
        results = self.kg.query_graph(query)
        return [r.get("name") for r in results]
    
    def find_similar_files(self, filename: str) -> List[str]:
        """Find files that import similar modules"""
        query = f"""
        MATCH (f1:file {{name: '{filename}'}})-[:imports]->(m:module),
              (f2:file)-[:imports]->(m)
        WHERE f1 <> f2
        RETURN f2.name, count(m) as shared_imports
        ORDER BY shared_imports DESC
        """
        results = self.kg.query_graph(query)
        return [(r.get("name"), r.get("shared_imports")) for r in results]

if __name__ == "__main__":
    analyzer = CodeAnalyzer()
    
    # Analyze current Python files
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".py"):
                analyzer.analyze_python_file(os.path.join(root, file))
    
    print("Code analysis complete - relationships stored in graph")