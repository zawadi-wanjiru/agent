"""
Custom tools for the Customer Care Multi-Agent System
These tools will be used by various agents to perform their tasks
"""

from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

# FAQ Database (from Lab 1)
FAQ_DATABASE = {
    "shipping": "Standard shipping takes 3-5 business days. Express shipping takes 1-2 business days.",
    "returns": "You can return items within 30 days of purchase. Items must be unused and in original packaging.",
    "payment": "We accept credit cards, debit cards, and PayPal.",
    "tracking": "You can track your order using the tracking number sent to your email."
}

# Order Database (from Lab 1 - mock data)
ORDER_DATABASE = {
    "12345": {"status": "Shipped", "tracking": "TRK123456789", "eta": "Jan 31, 2026"},
    "67890": {"status": "Processing", "tracking": None, "eta": "Feb 2, 2026"}
}

class FAQSearchInput(BaseModel):
    """Input for FAQ Search Tool"""
    query: str = Field(..., description="The user's question or keywords to search for")

class FAQSearchTool(BaseTool):
    name: str = "FAQ Search Tool"
    description: str = "Search the FAQ database for answers to common questions about shipping, returns, payments, or tracking."
    args_schema: Type[BaseModel] = FAQSearchInput

    def _run(self, query: str) -> str:
        query_lower = query.lower()
        
        # Check for return/returns
        if "return" in query_lower:
            return FAQ_DATABASE["returns"]
        
        # Check other keywords
        for key, answer in FAQ_DATABASE.items():
            if key in query_lower:
                return f"FAQ Answer: {answer}"
        
        return "No FAQ match found. This may require further research or escalation."

class OrderLookupInput(BaseModel):
    """Input for Order Lookup Tool"""
    order_number: str = Field(..., description="The order number to look up (e.g., '12345')")

class OrderLookupTool(BaseTool):
    name: str = "Order Lookup Tool"
    description: str = "Look up order status, tracking information, and estimated delivery using the order number."
    args_schema: Type[BaseModel] = OrderLookupInput

    def _run(self, order_number: str) -> str:
        order_info = ORDER_DATABASE.get(order_number)
        
        if order_info:
            result = f"Order #{order_number} - Status: {order_info['status']}, ETA: {order_info['eta']}"
            if order_info['tracking']:
                result += f", Tracking: {order_info['tracking']}"
            return result
        else:
            return f"Order #{order_number} not found in system. Please verify the order number or suggest customer contact support."

class ActionLoggerInput(BaseModel):
    """Input for Action Logger Tool"""
    action_type: str = Field(..., description="Type of action (e.g., 'refund', 'escalation', 'callback')")
    details: str = Field(..., description="Details about the action taken")

class ActionLoggerTool(BaseTool):
    name: str = "Action Logger Tool"
    description: str = "Log actions taken during the customer interaction such as refunds, escalations, or callbacks."
    args_schema: Type[BaseModel] = ActionLoggerInput

    def _run(self, action_type: str, details: str) -> str:
        # In a real system, this would write to a database
        log_entry = f"[ACTION LOGGED] {action_type.upper()}: {details}"
        print(log_entry)  # For visibility during development
        return f"Action logged successfully: {action_type}"

# Create tool instances
search_faq = FAQSearchTool()
lookup_order = OrderLookupTool()
log_action = ActionLoggerTool()

# Export all tools
ALL_TOOLS = [search_faq, lookup_order, log_action]
