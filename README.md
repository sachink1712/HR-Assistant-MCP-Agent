# HR Assistant MCP Agent

An agentic HR automation system built on the **Model Context Protocol (MCP)**, enabling Claude Desktop to autonomously handle HR workflows — employee onboarding, leave management, meeting scheduling, and IT/admin ticketing — through natural language.

## Overview

This project exposes a set of HR operations as MCP tools that Claude Desktop can call directly. Instead of manually running each step of a process like onboarding, you can prompt Claude with something like *"Onboard Priya as a Data Analyst under Manager E004"*, and the agent will orchestrate the full workflow: adding the employee to the HRMS, sending a welcome email, notifying the manager, raising equipment tickets, and scheduling an introductory meeting.

## Features

- **Employee Management** — add employees and fetch employee details by name
- **Leave Management** — check leave balance, apply for leave, view leave history
- **Meeting Scheduling** — schedule meetings between employees and managers
- **Ticketing** — raise IT/admin tickets (laptop, ID card, equipment) for new hires
- **Email Notifications** — send transactional emails via SMTP (Gmail)
- **Guided Onboarding Prompt** — a built-in MCP prompt (`onboard_new_employee`) that chains all of the above into a single multi-step workflow

## Architecture

```
Claude Desktop (MCP Client)
        │
        ▼
   MCP Server (src/server.py)
        │
 ┌──────┼───────┬──────────┬─────────────┐
 ▼      ▼       ▼          ▼             ▼
Employee  Leave  Ticket   Meeting    Email Sender
Manager   Manager Manager Manager    (SMTP)
 └──────────────┴──────────┴─────────────┘
              In-memory data store
```

## Project Structure

```
├── hrms/
│   ├── employee_manager.py   # Employee CRUD and lookup
│   ├── leave_manager.py      # Leave balance, application, history
│   ├── meeting_manager.py    # Meeting scheduling
│   ├── ticket_manager.py     # IT/admin ticket creation
│   └── schemas.py            # Pydantic models for requests/responses
├── src/
│   ├── server.py             # MCP server + tool/prompt definitions
│   ├── email_sender.py       # SMTP email handler
│   └── utils.py              # Data seeding helpers
├── main.py
├── pyproject.toml
└── uv.lock
```

## Available MCP Tools

| Tool | Description |
|---|---|
| `add_employee` | Add a new employee to the system |
| `get_employee_details` | Look up an employee's details by name |
| `send_email` | Send an email notification |
| `create_ticket` | Raise a ticket for equipment/access needs |
| `schedule_meeting` | Schedule a meeting for an employee |
| `get_leave_balance` | Check an employee's remaining leave balance |
| `apply_leave` | Apply leave for an employee on given dates |
| `get_leave_history` | Retrieve an employee's leave history |

**MCP Prompt:** `onboard_new_employee(employee_name, manager_name)` — chains the tools above into a complete onboarding workflow.

## Tech Stack

- Python 3.11+
- [MCP](https://modelcontextprotocol.io/) (`mcp[cli]`) with `FastMCP`
- Pydantic for schema validation
- SMTP (Gmail) for email delivery
- [uv](https://docs.astral.sh/uv/) for dependency management

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/sachink1712/HR-Assistant-MCP-Agent.git
cd HR-Assistant-MCP-Agent
```

### 2. Install dependencies
```bash
uv sync
```

### 3. Configure environment variables
Create a `.env` file in the project root:
```
CB_EMAIL=your_email@gmail.com
CB_EMAIL_PWD=your_app_password
```
> Use a [Gmail App Password](https://support.google.com/accounts/answer/185833), not your regular account password.

### 4. Connect to Claude Desktop
Add the server to your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "hr-assistant-agent": {
      "command": "uv",
      "args": ["--directory", "/absolute/path/to/HR-Assistant-MCP-Agent/src", "run", "server.py"]
    }
  }
}
```
Restart Claude Desktop. The HR tools will now be available to Claude in your conversations.

## Example Usage

```
"Onboard Shabnam Kumari as a Data Analyst under Manager Tony Sharma"
```
Claude will:
1. Add the employee to the HRMS
2. Send a welcome email with login credentials
3. Notify the manager
4. Raise tickets for laptop, ID card, and equipment
5. Schedule an introductory meeting

## License

MIT

## Author

**Sachin Kumar** — AI Engineer, building agentic AI and MCP-based automation systems.