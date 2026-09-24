import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from typing import Any, Dict
from utils import seed_services
from mcp.server.mcpserver import MCPServer
from hrms import *
from email_sender import EmailSender
from dotenv import load_dotenv
load_dotenv()

email_sender = EmailSender(
        smtp_server="smtp.gmail.com",
        port=587,
        username=os.getenv("CB_EMAIL"),
        password=os.getenv("CB_EMAIL_PWD"),
        use_tls=True,
    )

mcp = MCPServer("hr-assistant-agent")

employee_manager = EmployeeManager()
leave_manager = LeaveManager()
meeting_manager = MeetingManager()
ticket_manager = TicketManager()

seed_services(employee_manager, leave_manager, meeting_manager, ticket_manager)

@mcp.tool()
def add_employee(name: str, manager_id: str, email: str) -> str:
    """
    Add a new employee to the system.
    Args:
        name: str
        manager_id: str
        email: str
    Returns:
        str
    """
    emp_id = employee_manager.get_next_emp_id()
    emp = EmployeeCreate(emp_id=emp_id, name=name, manager_id=manager_id, email=email)
    employee_manager.add_employee(emp)
    return f"Employee {name} added successfully"

@mcp.tool()
def get_employee_details(name: str) -> Dict[str, Any]:
    """
    Get the details of an employee by name.
    Args:
        name: str
    Returns:
        Dict[str, Any]
    """
    matches = employee_manager.search_employee_by_name(name)
    if len(matches) == 0:
        raise ValueError(f"No Emplyees found matching {name}")
    
    emp_id = matches[0]
    return employee_manager.get_employee_details(emp_id)

@mcp.tool()
def send_email(to_email: str, subject: str, body: str) -> str:
    """
    Send an email to an employee.
    Args:
        to_email: str
        subject: str
        body: str
    Returns:
        str
    """
    
    email_sender.send_email(
        subject=subject,
        body=body,
        to_emails=to_email,
        from_email=email_sender.username,
    )

    return f"Email sent to {to_email}"

@mcp.tool()
def create_ticket(emp_id: str, item: str, reason: str) -> str:
    """
    Create a ticket for an new employees to get a new laptop, id card, and other necessary equipment.
    Args:
        emp_id: str
        item: str
        reason: str
    Returns:
        str
    """
    ticket = TicketCreate(emp_id=emp_id, item=item, reason=reason)
    return ticket_manager.create_ticket(ticket)

@mcp.tool()
def schedule_meeting(emp_id: str, meeting_dt: datetime, topic: str) -> str:
    """
    Schedule a meeting for an employee.
    Args:
        emp_id: str
        meeting_dt: datetime
        topic: str
    Returns:
        str
    """
    meeting = MeetingCreate(emp_id=emp_id, meeting_dt=meeting_dt, topic=topic)
    return meeting_manager.schedule_meeting(meeting)

@mcp.tool()
def get_leave_balance(emp_id: str) -> str:
    """
    Get the leave balance of an employee.
    Args:
        emp_id: str
    Returns:
        str
    """
    return leave_manager.get_leave_balance(emp_id)

@mcp.tool()
def apply_leave(emp_id: str, leave_dates: List[datetime]) -> str:
    """
    Apply leave for an employee.
    Args:
        emp_id: str
        leave_dates: List[datetime]
    Returns:
        str
    """
    leave_request = LeaveApplyRequest(emp_id=emp_id, leave_dates=leave_dates)
    return leave_manager.apply_leave(leave_request)

@mcp.tool()
def get_leave_history(emp_id: str) -> str:
    """
    Get the leave history of an employee.
    Args:
        emp_id: str
    Returns:
        str
    """
    return leave_manager.get_leave_history(emp_id)

@mcp.prompt("onboard_new_employee")
def onboard_new_employee(employee_name: str, manager_name: str) -> str:
    return f"""Onboard a new employee with the following details:
    - Name: {employee_name}
    - Manager Name: {manager_name}
    Steps to follow:
    - Add the employee to the HRMS system.
    - Send a welcome email to the employee with their login credentials. (Format: employee_name@atliq.com)
    - Notify the manager about the new employee's onboarding.
    - Raise tickets for a new laptop, id card, and other necessary equipment.
    - Schedule an introductory meeting between the employee and the manager.
    """


if __name__ == "__main__":
    mcp.run(transport="stdio")