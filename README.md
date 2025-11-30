---
title: Bjjagent
emoji: 🏢
colorFrom: red
colorTo: purple
sdk: gradio
sdk_version: 6.0.1
app_file: app.py
pinned: false
license: mit
tags:
  - mcp-in-action-track-consumer
---

# BJJ Training Program Generator 🥋

An AI-powered Gradio 6 application that generates personalized 4-week Brazilian Jiu-Jitsu training programs using Pydantic AI agents and the BJJ Coach MCP server.

## 🏆 Hackathon Submission

**Track**: Track 2 - MCP in Action

**Demo Video**: [Demo Video (1-5 minutes)](YOUR_VIDEO_URL_HERE) - *Coming soon*

**Social Media Post**: [Social Media Post](https://x.com/tspenov/status/1995185770555211933) - *Coming soon*

**Original Work**: This project was created during the hackathon period (November 14-30, 2025).

**Participation**: Solo project by [@tspenov](https://huggingface.co/tspenov)

### Why This Project Fits Track 2

This application demonstrates **autonomous AI agent behavior** using:
- **Planning & Reasoning**: Agent declares its strategy and uses OpenAI GPT-5 Responses API with reasoning enabled
- **Multi-step Execution**: Autonomous workflow (search positions → fetch metadata → retrieve videos → analyze chains → generate recommendations)
- **MCP Integration**: Uses BJJ Coach MCP server as primary tool source with 3 specialized tools
- **Real-world Value**: Provides personalized BJJ training analysis with position chain discovery and curated video recommendations for practitioners

## Features

- 🎯 **Smart Position Search**: Autocomplete dropdown with common BJJ positions
- 🤖 **AI-Powered Planning**: Uses GPT-5 with Pydantic AI agents
- 📚 **Real BJJ Data**: Connects to BJJ Coach MCP server for positions and videos
- 📅 **Structured Programs**: 4-week programs with 5 training days per week (20 sessions)
- 🎥 **Video Integration**: Clickable links to instructional videos with instructor info
- 🔄 **Progressive Training**: Organized from fundamentals to advanced techniques
- 🔗 **Chain Positions**: Fetches videos for related positions in the technique chain

## Real-World Value

### For BJJ Practitioners

This application solves a real problem for Brazilian Jiu-Jitsu practitioners:

**The Problem**: When learning a new position, students often don't know:
- What related positions connect to it
- How to progress from basics to advanced applications
- Which instructional videos are most relevant
- How to structure their training systematically

**The Solution**: This AI agent autonomously:
1. **Discovers Position Chains**: Identifies positions that lead to and from your target position, giving you strategic understanding
2. **Curates Learning Resources**: Finds and filters the most relevant instructional videos from YouTube
3. **Provides Training Context**: Adds drill notes and focus cues for each video
4. **Structures Your Learning**: Organizes content into a progressive training plan

**Use Cases**:
- **Competition Prep**: Focus on a specific position chain for upcoming tournaments
- **Skill Development**: Systematically improve weak areas in your game
- **Teaching**: Instructors can quickly generate structured lesson plans
- **Self-Study**: Independent learners get expert-level guidance on what to practice

## Architecture

```
┌─────────────────┐
│   Gradio 6 UI   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────────┐
│ Pydantic AI     │◄────►│  OpenAI GPT-5    │
│ Agent           │      └──────────────────┘
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────────┐
│ MCP Streamable  │◄────►│ BJJ Coach Server │
│ HTTP Client     │      └──────────────────┘
└─────────────────┘
```

## Prerequisites

- Python 3.8+
- OpenAI API key
- BJJ Coach MCP API token

## Installation

1. **Clone the repository**:
```bash
cd bjjresearch
```

2. **Create a virtual environment** (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**:

Create a `.env` file in the project root:

```bash
# BJJ Coach MCP API Token
MCP_TOKEN=your_bjj_coach_mcp_token_here

# OpenAI API Key
OPENAI_API_KEY=your_openai_api_key_here

# Logfire Token (optional - for production deployments)
LOGFIRE_TOKEN=your_logfire_write_token_here
```

### Getting Your API Keys

#### BJJ Coach MCP Token
1. Visit https://bjjcoach.ai/admin
2. Navigate to "MCP Tokens"
3. Click "Create New Token"
4. Copy the token (shown only once!)

#### OpenAI API Key
1. Visit https://platform.openai.com/api-keys
2. Create a new API key
3. Copy the key

#### Logfire Token (Optional - for Telemetry)
Logfire provides monitoring and observability. For local development, you can use `logfire auth`. For production deployments (like Hugging Face Spaces):
1. Install Logfire CLI: `pip install logfire`
2. Authenticate locally: `logfire auth`
3. Create a write token: `logfire projects tokens create`
4. Copy the write token
5. Add it to your deployment environment as `LOGFIRE_TOKEN`

**Note**: The app works fine without Logfire - it's optional for monitoring.

## Usage

### Local Development

1. **Start the application**:
```bash
python app.py
```

2. **Open your browser**:
Navigate to http://localhost:7860

3. **Generate a program**:
   - Select or type a BJJ position (e.g., "Closed Guard")
   - Click "Generate Program"
   - Wait for the AI agent to research and create your program
   - View your personalized 4-week training plan with video links

### Deploying to Hugging Face Spaces

1. **Create a new Space** at https://huggingface.co/spaces
2. **Select Gradio as SDK** with SDK version 6.0.1
3. **Add secrets** in Settings → Repository secrets:
   - `MCP_TOKEN`: Your BJJ Coach MCP token
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `LOGFIRE_TOKEN`: (Optional) Your Logfire write token for monitoring
4. **Push your code** to the Space repository

The app automatically detects if it's running in production and uses the write token for Logfire instead of requiring interactive authentication.

## How It Works

### Autonomous Agent Workflow

This application showcases **autonomous AI agent behavior** with planning, reasoning, and execution:

1. **User Input**: Select a BJJ position from the dropdown or type a custom one

2. **MCP Connection**: App connects to BJJ Coach MCP server using Streamable HTTP transport

3. **Agent Creation**: Pydantic AI agent initialized with:
   - **OpenAI GPT-5 Responses API** with reasoning enabled
   - **MCP Toolset**: BJJ Coach MCP server providing 3 specialized tools
   - **Planning Tools**: `declare_plan()` and `summarize_findings()` for autonomous behavior

4. **Autonomous Program Generation**: The agent independently executes a multi-step workflow:
   
   **Step 0 - Planning**: Agent calls `declare_plan()` to announce its strategy (2-3 sentence approach)
   
   **Step 1 - Search**: Uses `search_positions` MCP tool to find the position ID
   
   **Step 2 - Metadata Retrieval**: Calls `get_position_metadata` to get detailed information including:
   - Position category and synonyms
   - Chain of related positions (from/to positions)
   - Transition information
   
   **Step 3 - Position Chain Analysis**: Agent autonomously identifies and analyzes the chain of positions
   
   **Step 4 - Video Collection**: Uses `search_videos_for_position` to fetch:
   - 20 videos for the original position
   - Videos for related chain positions
   
   **Step 5 - Summarization**: Agent calls `summarize_findings()` with learned information
   
   **Step 6 - Intelligent Curation**: Agent selects the 10 most relevant videos and creates structured recommendations with:
   - Drill notes for each video
   - Focus cues for practice
   - Progressive organization

5. **Real-time Streaming**: User sees the agent's thought process through:
   - Tool calls and responses
   - Reasoning steps (when using GPT-5 Responses API)
   - Status updates via custom event handler

6. **Output**: Formatted markdown with:
   - Position chain analysis
   - Clickable video links with instructional context
   - Organized training recommendations

## Program Structure

Each generated program includes:

```
# 4-Week Training Program: [Position]

## Week 1: Fundamentals
Monday: [Video] - Instructor - Duration
Tuesday: [Video] - Instructor - Duration
...

## Week 2: Building Technique
...

## Week 3: Advanced Applications
...

## Week 4: Integration & Mastery
...
```

## MCP Integration

This application uses the **BJJ Coach MCP server** as its primary tool source, demonstrating how MCP enables AI agents to access specialized domain knowledge.

### MCP Server Details

- **Server**: BJJ Coach MCP Server
- **Endpoint**: `https://bjjcoach.ai/mcp`
- **Transport**: Streamable HTTP (SSE-based)
- **Authentication**: Bearer token
- **Integration**: Via `pydantic-ai[mcp]` with `MCPServerStreamableHTTP`

### Available MCP Tools

The agent has access to 3 specialized MCP tools from the BJJ Coach server:

1. **`search_positions`**: Search for BJJ positions by name
   - Input: Position name query
   - Output: List of matching positions with IDs
   - Use case: Initial position discovery

2. **`get_position_metadata`**: Get detailed position information
   - Input: Position ID
   - Output: Complete position data including:
     - Category (guard, top position, submission, etc.)
     - Synonyms and alternative names
     - Position chains (from/to positions)
     - Transition information
   - Use case: Understanding position relationships and chains

3. **`search_videos_for_position`**: Find instructional videos
   - Input: Position ID
   - Output: Curated YouTube videos with:
     - Video title and URL
     - Instructor name
     - Duration
     - Difficulty level (beginner/intermediate/advanced)
   - Use case: Finding learning resources

### Why MCP Matters

Using MCP allows the agent to:
- Access real-time BJJ position data without hardcoding
- Leverage domain-specific tools maintained by experts
- Scale to new positions and videos as they're added to the server
- Maintain separation between AI logic and domain data

## Troubleshooting

### "MCP_TOKEN not found"
- Ensure `.env` file exists in the project root
- Check that `MCP_TOKEN` is set correctly
- Verify the token hasn't been revoked at https://bjjcoach.ai/admin

### "OPENAI_API_KEY not found"
- Ensure `.env` file contains `OPENAI_API_KEY`
- Verify the key is valid at https://platform.openai.com/api-keys

### "Rate limit exceeded"
- BJJ Coach tokens have rate limits (default: 100 requests/hour)
- Wait for the rate limit to reset
- Check usage in the admin panel

### "No tools available"
- Verify your MCP token is valid and not expired
- Check network connectivity to https://bjjcoach.ai/mcp
- Ensure the token has proper permissions

### Agent errors
- If the agent fails, check the Debug Information accordion
- Verify the position name is valid
- Try a more common position name

## Development

### Project Structure

```
bjjresearch/
├── app.py              # Main Gradio application
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (not in git)
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

### Key Dependencies

- **gradio>=6.0.0**: Modern UI framework
- **pydantic-ai[openai,mcp]>=1.22.0**: Agent orchestration with MCP support
- **python-dotenv**: Environment variable management

## Gradio 6 Features Used

This app uses Gradio 6 best practices:

- ✅ `gr.Blocks()` for custom layouts
- ✅ `gr.Dropdown(allow_custom_value=True)` for autocomplete
- ✅ `buttons=["copy"]` parameter (not deprecated `show_copy_bu 
- ✅ Async event handlers for MCP operations

## API Reference

### MCP Server Endpoint
```
https://bjjcoach.ai/mcp
```

### Authentication
```
Authorization: Bearer YOUR_MCP_TOKEN
```

### Rate Limits
- Default: 100 requests per hour per token
- Configurable in admin panel

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License - See LICENSE file for details

## Support

For BJJ Coach MCP API issues:
- Check https://bjjcoach.ai/admin for token status
- Review the MCP API documentation

For app issues:
- Check the Debug Information in the UI
- Verify environment variables are set correctly
- Ensure all dependencies are installed

## Acknowledgments

- **BJJ Coach** for the MCP server and BJJ data
- **Gradio** for the amazing UI framework
- **Pydantic AI** for modern agent orchestration
- **OpenAI** for GPT models

## Track 2 Requirements Checklist

This project meets all requirements for **Track 2: MCP in Action**:

### General Requirements
- ✅ **Published as HuggingFace Space**: This Space is in the hackathon organization
- ✅ **Track Tag Added**: `mcp-in-action-track-consumer` in README frontmatter
- ✅ **Social Media Post**: Placeholder link included (to be updated)
- ✅ **Demo Video**: Placeholder link included (to be updated, 1-5 minutes)
- ✅ **Original Work**: Created during hackathon period (Nov 14-30, 2025)
- ✅ **Solo Participation**: Single developer (@tspenov)

### Track 2 Specific Requirements
- ✅ **Demonstrates Autonomous Agent Behavior**: 
  - Planning: Agent uses `declare_plan()` to announce strategy
  - Reasoning: GPT-5 Responses API with reasoning enabled
  - Execution: Multi-step autonomous workflow with 6 distinct phases
  
- ✅ **Uses MCP Servers as Tools**: 
  - BJJ Coach MCP server at `https://bjjcoach.ai/mcp`
  - 3 specialized tools: `search_positions`, `get_position_metadata`, `search_videos_for_position`
  - Integrated via `pydantic-ai[mcp]` with Streamable HTTP transport
  
- ✅ **Is a Gradio App**: 
  - Built with Gradio 6.0.1
  - Uses `gr.Blocks()` for custom UI
  - Async event handlers for streaming agent execution
  
- ✅ **Shows Clear User Value and Practical Application**:
  - Solves real problem for BJJ practitioners
  - Discovers position chains for strategic understanding
  - Curates learning resources with instructional context
  - Use cases: competition prep, skill development, teaching, self-study

### Advanced Features (Bonus Points)
- ✅ **Context Engineering**: Custom event handler for real-time streaming of agent thoughts
- ✅ **Advanced Agent Features**: 
  - Planning tools (`declare_plan`, `summarize_findings`)
  - Multi-step reasoning workflow
  - Intelligent video curation (filters 20 down to 10 most relevant)
- ✅ **Observability**: Logfire integration for telemetry and monitoring

---

Built with ❤️ for the BJJ community

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference
