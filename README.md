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
---

# BJJ Training Program Generator 🥋

An AI-powered Gradio 6 application that generates personalized 4-week Brazilian Jiu-Jitsu training programs using Pydantic AI agents and the BJJ Coach MCP server.

## Features

- 🎯 **Smart Position Search**: Autocomplete dropdown with common BJJ positions
- 🤖 **AI-Powered Planning**: Uses GPT-5 with Pydantic AI agents
- 📚 **Real BJJ Data**: Connects to BJJ Coach MCP server for positions and videos
- 📅 **Structured Programs**: 4-week programs with 5 training days per week (20 sessions)
- 🎥 **Video Integration**: Clickable links to instructional videos with instructor info
- 🔄 **Progressive Training**: Organized from fundamentals to advanced techniques
- 🔗 **Chain Positions**: Fetches videos for related positions in the technique chain

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

1. **User Input**: Select a BJJ position from the dropdown or type a custom one
2. **MCP Connection**: App connects to BJJ Coach MCP server using Streamable HTTP transport
3. **Agent Creation**: Pydantic AI agent initialized with GPT-5 and MCP server as toolset
4. **Program Generation**: Agent follows this workflow:
   - Searches for the position using `search_positions` tool
   - Gets metadata including chain of related positions with `get_position_metadata`
   - Fetches videos for the original position using `search_videos_for_position`
   - Fetches videos for first 3-5 chain positions (related techniques)
   - Creates a structured 4-week program from all collected videos
5. **Output**: Formatted markdown with clickable video links organized by week

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

## MCP Tools Available

The BJJ Coach MCP server provides:

1. **search_positions**: Search for BJJ positions by name
2. **get_position_metadata**: Get detailed info about a position including:
   - Category
   - Synonyms
   - Transitions to/from other positions
3. **search_videos_for_position**: Find instructional videos with:
   - Title
   - URL (YouTube links)
   - Instructor name
   - Duration
   - Difficulty level

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

---

Built with ❤️ for the BJJ community

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference
