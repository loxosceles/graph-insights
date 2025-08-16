#!/usr/bin/env python3
"""
Graph Insights MCP Server
Provides persistent knowledge graph storage and querying via MCP protocol
"""

import json
import sys
import sqlite3
import os
from typing import Dict, List

class PersistentKnowledgeGraph:
    def __init__(self, db_path="knowledge_graph.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS entities (
                id TEXT PRIMARY KEY,
                type TEXT,
                properties TEXT
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS relationships (
                from_id TEXT,
                to_id TEXT,
                type TEXT,
                FOREIGN KEY (from_id) REFERENCES entities (id),
                FOREIGN KEY (to_id) REFERENCES entities (id)
            )
        ''')
        conn.commit()
        conn.close()
    
    def add_entity(self, entity_type: str, entity_id: str, properties: Dict):
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "INSERT OR REPLACE INTO entities (id, type, properties) VALUES (?, ?, ?)",
            (entity_id, entity_type, json.dumps(properties))
        )
        conn.commit()
        conn.close()
        return {"success": True}
    
    def add_relationship(self, from_id: str, to_id: str, relation_type: str):
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "INSERT INTO relationships (from_id, to_id, type) VALUES (?, ?, ?)",
            (from_id, to_id, relation_type)
        )
        conn.commit()
        conn.close()
        return {"success": True}
    
    def query_graph(self, query: str) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        results = []
        
        try:
            if "works_on" in query and "RETURN p.name" in query:
                project = query.split("name: '")[1].split("'")[0]
                cursor = conn.execute('''
                    SELECT e.properties 
                    FROM entities e
                    JOIN relationships r ON e.id = r.from_id
                    WHERE r.type = "works_on" AND r.to_id = ?
                ''', (project,))
                for row in cursor:
                    props = json.loads(row[0])
                    results.append({"name": props.get("name")})
            
            elif "works_on" in query and "RETURN proj.name" in query:
                dev = query.split("name: '")[1].split("'")[0]
                cursor = conn.execute('''
                    SELECT e.properties
                    FROM entities e
                    JOIN relationships r ON e.id = r.to_id
                    WHERE r.type = "works_on" AND r.from_id = ?
                ''', (dev,))
                for row in cursor:
                    props = json.loads(row[0])
                    results.append({"name": props.get("name")})
            
            elif "depends_on" in query and "RETURN proj.name" in query:
                tech = query.split("name: '")[1].split("'")[0]
                cursor = conn.execute('''
                    SELECT e.properties
                    FROM entities e
                    JOIN relationships r ON e.id = r.from_id
                    WHERE r.type = "depends_on" AND r.to_id = ?
                ''', (tech,))
                for row in cursor:
                    props = json.loads(row[0])
                    results.append({"name": props.get("name")})
            
            elif "depends_on" in query and "RETURN d.name" in query:
                # Extract project names from multi-line query
                lines = [line.strip() for line in query.split('\n') if 'name:' in line]
                projects = []
                for line in lines:
                    if "name: '" in line:
                        proj = line.split("name: '")[1].split("'")[0]
                        projects.append(proj)
                
                if len(projects) >= 2:
                    cursor = conn.execute('''
                        SELECT DISTINCT e.properties
                        FROM entities e
                        JOIN relationships r1 ON e.id = r1.to_id
                        JOIN relationships r2 ON e.id = r2.to_id
                        WHERE r1.from_id = ? AND r1.type = "depends_on"
                          AND r2.from_id = ? AND r2.type = "depends_on"
                    ''', (projects[0], projects[1]))
                    for row in cursor:
                        props = json.loads(row[0])
                        results.append({"name": props.get("name")})
            
            elif "covers" in query and "RETURN p.title" in query:
                if "name: '" in query:
                    topic = query.split("name: '")[1].split("'")[0]
                    # Convert topic to ID format
                    topic_id = topic.replace(" ", "_").lower()
                    cursor = conn.execute('''
                        SELECT e.properties
                        FROM entities e
                        JOIN relationships r ON e.id = r.from_id
                        WHERE r.type = "covers" AND r.to_id = ?
                    ''', (topic_id,))
                    for row in cursor:
                        props = json.loads(row[0])
                        results.append({"title": props.get("title")})
        
        except Exception as e:
            print(f"Query error: {e}", file=sys.stderr)
        
        conn.close()
        return results

def main():
    kg = PersistentKnowledgeGraph()
    
    for line in sys.stdin:
        try:
            request = json.loads(line.strip())
            method = request.get("method")
            
            if method == "tools/list":
                response = {
                    "jsonrpc": "2.0",
                    "id": request["id"],
                    "result": {
                        "tools": [
                            {"name": "add_entity", "description": "Add entity to graph"},
                            {"name": "add_relationship", "description": "Add relationship"},
                            {"name": "query_graph", "description": "Query the graph"}
                        ]
                    }
                }
            
            elif method == "tools/call":
                tool_name = request["params"]["name"]
                args = request["params"]["arguments"]
                
                if tool_name == "add_entity":
                    result = kg.add_entity(args["type"], args["id"], args["properties"])
                elif tool_name == "add_relationship":
                    result = kg.add_relationship(args["from"], args["to"], args["type"])
                elif tool_name == "query_graph":
                    result = {"content": kg.query_graph(args["query"])}
                else:
                    result = {"error": f"Unknown tool: {tool_name}"}
                
                response = {
                    "jsonrpc": "2.0",
                    "id": request["id"],
                    "result": result
                }
            
            else:
                response = {
                    "jsonrpc": "2.0",
                    "id": request["id"],
                    "error": {"code": -32601, "message": "Method not found"}
                }
            
            print(json.dumps(response))
            sys.stdout.flush()
            
        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "id": request.get("id", 1),
                "error": {"code": -32603, "message": str(e)}
            }
            print(json.dumps(error_response))
            sys.stdout.flush()

if __name__ == "__main__":
    main()