#!/usr/bin/env python3
"""
Persistent Knowledge Graph Client - maintains connection
"""

import json
import subprocess
import time
from typing import Dict, List

class PersistentKGClient:
    def __init__(self):
        self.server = None
        self.start_server()
    
    def start_server(self):
        if self.server and self.server.poll() is None:
            return
        
        self.server = subprocess.Popen(
            ["python3", "persistent_kg_server.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        time.sleep(0.1)  # Let server initialize
    
    def _call_server(self, request_data):
        if not self.server or self.server.poll() is not None:
            self.start_server()
        
        try:
            self.server.stdin.write(json.dumps(request_data) + "\n")
            self.server.stdin.flush()
            
            response_line = self.server.stdout.readline()
            return json.loads(response_line.strip())
        except Exception as e:
            return {"error": str(e)}
    
    def add_entity(self, entity_type: str, entity_id: str, properties: Dict) -> bool:
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "add_entity",
                "arguments": {
                    "type": entity_type,
                    "id": entity_id,
                    "properties": properties
                }
            }
        }
        response = self._call_server(request)
        return "error" not in response
    
    def add_relationship(self, from_id: str, to_id: str, relation_type: str) -> bool:
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "add_relationship",
                "arguments": {
                    "from": from_id,
                    "to": to_id,
                    "type": relation_type
                }
            }
        }
        response = self._call_server(request)
        return "error" not in response
    
    def query_graph(self, query: str) -> List[Dict]:
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "query_graph",
                "arguments": {"query": query}
            }
        }
        response = self._call_server(request)
        return response.get("result", {}).get("content", [])
    
    def close(self):
        if self.server:
            self.server.terminate()
            self.server.wait()

class KnowledgeGraphClient(PersistentKGClient):
    pass