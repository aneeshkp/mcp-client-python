# MCP Client Python

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![MCP](https://img.shields.io/badge/protocol-MCP-orange.svg)](https://modelcontextprotocol.io)

A flexible Python client for the Model Context Protocol (MCP) with support for multiple LLM backends and Kubernetes environments.

## 🚀 Features

- 🤖 **Multiple LLM Backends**: Ollama, OpenAI-compatible APIs, local models
- 🔧 **Full MCP Support**: All MCP tools, resources, and prompts
- 💬 **Interactive Interface**: Natural language conversations with AI
- ☸️ **Kubernetes Ready**: Built-in support for kubeconfig and environment variables
- 📚 **Conversation History**: Maintains context across interactions
- 🎛️ **Highly Configurable**: Flexible configuration options

## 🏗️ Perfect for MCP Servers

This client works seamlessly with any MCP server, including:
- [PTP Operator MCP Server](https://github.com/aneeshkp/ptp-operator-mcp-server) - For Precision Time Protocol management
- MongoDB MCP servers
- File system MCP servers
- Custom Kubernetes operators
- And any other MCP-compatible server!

## 📦 Installation

```bash
git clone https://github.com/aneeshkp/mcp-client-python.git
cd mcp-client-python
pip install -r requirements.txt
```

Or install directly:
```bash
pip install -e .
```

## 🚀 Quick Start

### Basic Usage
```bash
python -m mcp_client --server "node" --server-args "your-mcp-server.js" --llm ollama --model "llama3.1:8b"
```

### With Kubernetes (PTP Operator Example)
```bash
python -m mcp_client \
  --server "node" \
  --server-args "server.js" \
  --kubeconfig ~/.kube/config \
  --env "NAMESPACE=openshift-ptp" \
  --llm ollama \
  --model "codellama:13b"
```

### Using Environment File
```bash
# Create .env file with your settings
python -m mcp_client --server "node" --server-args "server.js" --env-file .env --llm ollama
```

## 🔧 Configuration

### LLM Backends

**Ollama (Local)**
```bash
--llm ollama --model "llama3.1:8b" --base-url "http://localhost:11434"
```

**OpenAI API**
```bash
--llm openai --model "gpt-4" --api-key "your-key" --base-url "https://api.openai.com"
```

**Local vLLM/Text Generation WebUI**
```bash
--llm openai --model "your-model" --api-key "dummy" --base-url "http://localhost:8000"
```

### Environment Variables

```bash
--kubeconfig ~/.kube/config                    # Kubernetes config
--env "NAMESPACE=production"                   # Individual variables
--env "CLUSTER=my-cluster"                     # Multiple env vars
--env-file .env                               # Load from file
```

## 💡 Example Conversations

### PTP Operator Management
```
🚀 You: Show me the current PTP configuration on my cluster
🤖 Assistant: I'll check the PTP configurations across your cluster...

[Uses PTP tools to analyze configurations]

🤖 Assistant: Found 3 PTP configurations:
- grandmaster-profile: Applied to master nodes, GPS sync enabled
- slave-profile: Applied to worker nodes, synced to grandmaster
- edge-profile: Custom profile for edge computing nodes

All configurations are active and timing is within ±100ns tolerance.
```

## 🛠️ Commands

Interactive commands available during chat:
- `quit/exit/bye` - Exit the client  
- `tools` - List available MCP tools
- `history` - Show conversation history
- `clear` - Clear conversation history

## 📁 Project Structure

```
mcp-client-python/
├── src/mcp_client/          # Main package
│   ├── client.py            # Core MCP client
│   ├── backends.py          # LLM backend implementations  
│   └── cli.py               # Command-line interface
├── examples/                # Usage examples
├── tests/                   # Unit tests
└── docs/                   # Documentation
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Run tests: `python -m pytest`
5. Submit a pull request

## 📋 Requirements

- Python 3.8+
- MCP SDK
- aiohttp
- Access to an LLM backend (Ollama, OpenAI, etc.)

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🔗 Related Projects

- [PTP Operator MCP Server](https://github.com/aneeshkp/ptp-operator-mcp-server) - Kubernetes PTP management
- [Model Context Protocol](https://modelcontextprotocol.io) - Official MCP documentation

## 🐛 Issues & Support

Found a bug or need help? [Open an issue](https://github.com/aneeshkp/mcp-client-python/issues) on GitHub.

---

**Built with ❤️ for the MCP community**
