# Graph Insights

A practical knowledge graph application using Model Context Protocol (MCP) servers. Graph Insights helps organizations understand complex relationships in their data - from project teams and dependencies to research collaborations and code architecture.

## 🎯 What Graph Insights Does

Knowledge graphs are powerful for scenarios involving **complex relationships** between entities. Unlike traditional relational databases that require complex JOINs, knowledge graphs naturally model and query interconnected data.

### Real-World Problems Solved

- **Project Management**: Track team assignments, shared resources, and technology dependencies
- **Code Analysis**: Map code structure, imports, and architectural relationships  
- **Research Networks**: Connect papers, authors, topics, and collaboration opportunities
- **Impact Analysis**: Understand cascading effects of changes across systems

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────────┐    ┌─────────────────┐
│   Demo Scripts  │───▶│  Persistent Client   │───▶│  MCP Server     │
│                 │    │                      │    │                 │
│ • demo.py       │    │ • Connection mgmt    │    │ • SQLite backend│
│ • project_mgr   │    │ • Query interface    │    │ • Entity storage│
│ • code_analyzer │    │ • Error handling     │    │ • Relationship  │
│ • research_asst │    │                      │    │   queries       │
└─────────────────┘    └──────────────────────┘    └─────────────────┘
```

## 📁 Project Structure

```
graph-insights/
├── README.md                    # This documentation
├── demo.py                      # Main demonstration script
├── persistent_kg_server.py      # MCP server with SQLite backend
├── persistent_client.py         # Client for server communication
├── project_manager.py           # Project management use case
├── code_analyzer.py             # Code structure analysis
├── research_assistant.py        # Research collaboration network
├── package.json                 # Node.js dependencies
└── knowledge_graph.db           # SQLite database (auto-created)
```

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- Node.js (for MCP protocol)

### Installation

```bash
# Clone or navigate to the project directory
cd graph-insights

# Install Node.js dependencies (if needed)
npm install

# Run the application
python3 main.py
```

## 📊 Application Output

### Project Management Insights

The application analyzes 4 interconnected projects with overlapping teams and technologies:

```
🔍 Team Compositions:
  e-commerce-web: ['alice', 'bob', 'carol'] (3 members)
  mobile-app: ['bob', 'david', 'eve'] (3 members)
  analytics-service: ['carol', 'frank', 'alice'] (3 members)
  payment-gateway: ['david', 'grace'] (2 members)
```

**Key Insights:**
- **Cross-team collaboration**: Bob works on both web and mobile
- **Shared expertise**: Alice and Carol bridge web and analytics
- **Resource planning**: David connects mobile and payment systems

### Technology Dependencies

```
🔗 Cross-Project Collaborations:
  e-commerce-web ↔ mobile-app:
    Shared tech: ['nodejs', 'postgresql']
  e-commerce-web ↔ analytics-service:
    Shared tech: ['postgresql', 'redis']
```

**Business Value:**
- **Risk assessment**: PostgreSQL used across ALL projects (single point of failure)
- **Standardization opportunities**: NodeJS shared between web/mobile
- **Infrastructure planning**: Redis clustering needed for web/analytics

### Research Network Analysis

```
🔬 Research Topics & Papers:
  deep learning: 2 papers → ['Graph Neural Networks Survey', 'Deep Learning for NLP']
  graph databases: 2 papers → ['Knowledge Graphs in Enterprise', 'Graph Databases at Scale']
```

**Research Insights:**
- **Collaboration opportunities**: Authors with shared research interests
- **Trending topics**: Emerging research directions based on paper connections
- **Knowledge gaps**: Underexplored intersections between topics

## 🔧 Technical Deep Dive

### MCP Server Implementation

The `persistent_kg_server.py` implements a full MCP (Model Context Protocol) server:

```python
# Core MCP tools exposed
tools = [
    "add_entity",      # Store entities with properties
    "add_relationship", # Create connections between entities  
    "query_graph"      # Execute graph queries
]
```

**Key Features:**
- **Persistent storage**: SQLite backend survives server restarts
- **Entity management**: Flexible schema for any entity type
- **Relationship modeling**: Directed relationships with types
- **Query processing**: Cypher-like query parsing

### Client Architecture

The `persistent_client.py` maintains a persistent connection:

```python
class PersistentKGClient:
    def start_server(self):
        # Launches MCP server process
    
    def _call_server(self, request_data):
        # Handles JSON-RPC communication
    
    def add_entity(self, type, id, properties):
        # Adds entities to knowledge graph
```

**Benefits:**
- **Connection reuse**: Avoids server startup overhead
- **Error handling**: Graceful recovery from server issues
- **Type safety**: Structured API for graph operations

### Database Schema

SQLite tables store the graph structure:

```sql
-- Entities table
CREATE TABLE entities (
    id TEXT PRIMARY KEY,      -- Unique entity identifier
    type TEXT,               -- Entity type (project, person, etc.)
    properties TEXT          -- JSON properties
);

-- Relationships table  
CREATE TABLE relationships (
    from_id TEXT,            -- Source entity
    to_id TEXT,              -- Target entity
    type TEXT                -- Relationship type (works_on, depends_on)
);
```

## 💡 Use Case Examples

### 1. Project Management

**Problem**: "Which developers work on projects using PostgreSQL?"

**Traditional SQL** (complex):
```sql
SELECT DISTINCT p.name 
FROM persons p
JOIN project_assignments pa ON p.id = pa.person_id
JOIN projects pr ON pa.project_id = pr.id  
JOIN project_dependencies pd ON pr.id = pd.project_id
JOIN dependencies d ON pd.dependency_id = d.id
WHERE d.name = 'postgresql';
```

**Knowledge Graph** (natural):
```cypher
MATCH (p:person)-[:works_on]->(proj:project)-[:depends_on]->(d:dependency {name: 'postgresql'})
RETURN p.name
```

### 2. Code Analysis

**Problem**: "Find files that import similar modules"

**Knowledge Graph Approach**:
```python
# Automatically extract and store code structure
analyzer.analyze_python_file("my_module.py")

# Query for similar files
similar = analyzer.find_similar_files("my_module.py")
# Returns: [("other_module.py", 5), ("utils.py", 3)]
```

### 3. Research Networks

**Problem**: "Suggest collaboration opportunities based on shared research interests"

**Knowledge Graph Solution**:
```python
# Store research papers and topics
assistant.add_paper("AI Survey", ["Dr. Smith"], ["machine learning", "AI"])

# Find potential collaborators
collabs = assistant.find_author_collaborations("Dr. Smith")
# Returns authors with shared research topics
```

## 🔍 Query Patterns

### Basic Entity Queries

```python
# Find all projects a developer works on
query = "MATCH (p:person {name: 'alice'})-[:works_on]->(proj:project) RETURN proj.name"

# Find all technologies used by a project
query = "MATCH (proj:project {name: 'web-app'})-[:depends_on]->(d:dependency) RETURN d.name"
```

### Relationship Queries

```python
# Find shared dependencies between projects
query = """
MATCH (p1:project {name: 'web-app'})-[:depends_on]->(d:dependency),
      (p2:project {name: 'mobile-app'})-[:depends_on]->(d)
RETURN d.name
"""

# Find research papers on specific topics
query = "MATCH (p:paper)-[:covers]->(t:topic {name: 'deep learning'}) RETURN p.title"
```

## 🆚 Knowledge Graphs vs Traditional Databases

| Aspect | Traditional DB | Knowledge Graph |
|--------|---------------|-----------------|
| **Schema** | Fixed, rigid | Flexible, evolving |
| **Relationships** | Foreign keys, JOINs | Native, first-class |
| **Queries** | Complex SQL JOINs | Natural graph traversal |
| **Performance** | Degrades with JOINs | Optimized for relationships |
| **Use Cases** | Transactional data | Connected, relationship-heavy data |

### When to Use Knowledge Graphs

✅ **Good for:**
- Social networks and recommendations
- Fraud detection and pattern analysis  
- Knowledge management and discovery
- Impact analysis and dependency tracking
- Research and collaboration networks

❌ **Not ideal for:**
- Simple CRUD operations
- High-volume transactional systems
- Well-structured, stable schemas
- Financial transactions requiring ACID

## 🛠️ Extending the Demo

### Adding New Entity Types

```python
# Add a new entity type
kg.add_entity("skill", "python", {
    "name": "Python",
    "category": "programming_language",
    "difficulty": "intermediate"
})

# Create relationships
kg.add_relationship("alice", "python", "has_skill")
```

### Custom Query Patterns

```python
# Extend the server's query_graph method
def query_graph(self, query: str):
    if "has_skill" in query:
        # Add custom query logic
        return self.handle_skill_query(query)
```

### Integration with Real Systems

```python
# Connect to external APIs
def sync_from_github(self, repo_url):
    # Extract contributors, files, dependencies
    # Store in knowledge graph
    
def sync_from_jira(self, project_key):
    # Extract issues, assignees, components
    # Model as graph entities
```

## 🔧 Troubleshooting

### Common Issues

**Server Connection Errors**:
```bash
# Check if server process is running
ps aux | grep persistent_kg_server

# Restart the demo
python3 demo.py
```

**Empty Query Results**:
- Verify entity IDs match exactly (case-sensitive)
- Check relationship directions in queries
- Ensure data was properly inserted

**Database Issues**:
```bash
# Reset database
rm knowledge_graph.db
python3 demo.py  # Recreates database
```

## 📚 Further Reading

- [Neo4j Graph Database Concepts](https://neo4j.com/docs/getting-started/)
- [Cypher Query Language](https://neo4j.com/docs/cypher-manual/current/)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [Graph Database Use Cases](https://neo4j.com/use-cases/)

## 🤝 Contributing

Graph Insights can be extended with:
- Additional use cases (supply chain, social networks)
- More sophisticated query patterns
- Integration with real knowledge graph databases
- Performance optimizations for large datasets
- Web interface for graph visualization

## 📄 License

Graph Insights is a practical tool for relationship analysis in organizational data. Feel free to adapt and extend for your own use cases.