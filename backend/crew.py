"""
Multi-Agent Crew for Customer Care
Orchestrates the team of agents to handle customer inquiries
"""

from crewai import Crew, Task, Process
from agents import (
    greeter_agent,
    researcher_agent,
    order_specialist_agent,
    resolver_agent,
    quality_reviewer_agent,
    supervisor_agent
)


def create_customer_care_crew(user_message: str, conversation_history: list = None):
    """
    Create a crew to handle a customer inquiry
    
    Args:
        user_message: The customer's message
        conversation_history: Previous messages in the conversation
        
    Returns:
        Configured Crew ready to process the inquiry
    """
    
    # Build context from conversation history
    context = ""
    if conversation_history:
        context = "\n\nPrevious conversation:\n"
        for msg in conversation_history[-5:]:  # Last 5 messages for context
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            context += f"{role}: {content}\n"
    
    # Task 1: Greet and classify intent
    greet_task = Task(
        description=f"""Analyze the customer's message and identify their intent.
        
        Customer message: {user_message}
        {context}
        
        Determine:
        1. What type of help does the customer need? (order inquiry, general question, complaint, etc.)
        2. What is the customer's emotional state? (frustrated, neutral, happy)
        3. What information might we need to help them?
        
        Provide a brief classification and warm greeting.""",
        agent=greeter_agent,
        expected_output="Intent classification and greeting message"
    )
    
    # Task 2: Research information (if needed)
    research_task = Task(
        description=f"""Based on the customer's inquiry, search for relevant information.
        
        Customer message: {user_message}
        
        If the question is about shipping, returns, payments, or tracking policies,
        use the FAQ Search Tool to find accurate information.
        
        If no FAQ search is needed, explain what information you have or what's needed.""",
        agent=researcher_agent,
        expected_output="Relevant FAQ information or explanation of what's needed",
        context=[greet_task]
    )
    
    # Task 3: Handle order inquiries (if applicable)
    order_task = Task(
        description=f"""Check if the customer mentioned an order number.
        
        Customer message: {user_message}
        {context}
        
        If an order number is mentioned (look for 5-digit numbers), use the Order Lookup Tool.
        If no order number is found but they're asking about an order, politely ask for it.
        If this isn't about an order, state that clearly.""",
        agent=order_specialist_agent,
        expected_output="Order information or request for order number or confirmation this isn't order-related",
        context=[greet_task, research_task]
    )
    
    # Task 4: Resolve issues (if needed)
    resolve_task = Task(
        description=f"""Determine if any action needs to be taken to resolve the customer's issue.
        
        Based on the customer's message and previous findings:
        - Should we log a refund request?
        - Should we escalate to a human agent?
        - Should we schedule a callback?
        - Is the issue already resolved with information provided?
        
        If action is needed and it's sensitive (refund, cancellation), note that human approval is required.
        Use the Action Logger Tool if appropriate.""",
        agent=resolver_agent,
        expected_output="Action plan or confirmation that no action is needed",
        context=[greet_task, research_task, order_task]
    )
    
    # Task 5: Quality review (reflection/critique)
    quality_task = Task(
        description=f"""Review the team's work and prepare the final response to the customer.
        
        Customer's original message: {user_message}
        
        Review what the team has found and done:
        - Greeter's intent classification
        - Researcher's findings
        - Order specialist's information
        - Resolver's action plan
        
        Create a final, cohesive response that:
        1. Addresses all the customer's questions
        2. Is warm and professional
        3. Is clear and concise (2-4 sentences)
        4. Includes any actions being taken
        5. Asks for confirmation if needed
        
        If information is missing or unclear, note what else is needed.""",
        agent=quality_reviewer_agent,
        expected_output="Final polished response ready to send to customer",
        context=[greet_task, research_task, order_task, resolve_task]
    )
    
    # Create the crew with hierarchical process (supervisor manages)
    crew = Crew(
        agents=[
            greeter_agent,
            researcher_agent,
            order_specialist_agent,
            resolver_agent,
            quality_reviewer_agent
        ],
        tasks=[
            greet_task,
            research_task,
            order_task,
            resolve_task,
            quality_task
        ],
        process=Process.sequential,  # Tasks run in order
        verbose=True,
        manager_llm=supervisor_agent.llm  # Supervisor oversees
    )
    
    return crew


def process_customer_inquiry(user_message: str, conversation_history: list = None) -> dict:
    """
    Process a customer inquiry using the multi-agent crew
    
    Args:
        user_message: The customer's message
        conversation_history: Previous conversation messages
        
    Returns:
        dict with 'response' and 'metadata' about the agents' work
    """
    try:
        # Create and run the crew
        crew = create_customer_care_crew(user_message, conversation_history)
        result = crew.kickoff()
        
        # Extract the final response (from quality review task)
        final_response = str(result)
        
        return {
            "response": final_response,
            "metadata": {
                "agents_involved": ["greeter", "researcher", "order_specialist", "resolver", "quality_reviewer"],
                "status": "success"
            }
        }
        
    except Exception as e:
        return {
            "response": f"I apologize, but I'm having trouble processing your request right now. Please try again or contact support. Error: {str(e)}",
            "metadata": {
                "status": "error",
                "error": str(e)
            }
        }
