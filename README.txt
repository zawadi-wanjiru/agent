Lab 2 - Multi-Agent Customer Support System
Gift Wanjiru, Nixon Masanya, Sharon Mwangi, Melissa Wachira

USE CASE: Customer Care Agent Team

I chose a customer support scenario because its a real problem companies face - handling tons of similar queries efficiently while still giving good answers. Instead of one bot trying to do everything (and probably doing it poorly), I split the work between specialized agents.

TEAM STRUCTURE

The system has 6 agents:

1. Greeter - figures out what the customer wants
2. Researcher - searches FAQ database
3. Order Specialist - looks up order info
4. Resolver - plans actions like refunds
5. Quality Reviewer - checks responses before sending (this is the reflection part)
6. Supervisor - coordinates everything

They work sequentially: Greeter → relevant specialist(s) → Quality Reviewer → done

For simple stuff (FAQ lookups, order checks) I made an optimized path that only uses 2 agents to keep things fast.

SETUP

You need:
- Python 3.12
- Node.js (for the frontend)
- Groq API key (free at console.groq.com)

Backend:
```
cd backend
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env and add your Groq key
python app_multiagent.py
```

Frontend:
```
cd frontend
npm install
npm run dev
```

Then open http://localhost:5173

EXAMPLE INTERACTIONS

Example 1: FAQ Query
User: "What is your shipping policy?"

[Greeter identifies it as a FAQ question]
[Researcher searches FAQ database]
Researcher finds: "Standard shipping takes 3-5 business days. Express shipping takes 1-2 business days."
[Quality Reviewer formats it nicely]
Response: "We ship standard orders within 3-5 business days, and express orders within 1-2 business days."

Time: ~1.5 seconds

Example 2: Order Lookup
User: "Check order 12345"

[Greeter identifies order query]
[Order Specialist looks up order in database]
Order Specialist finds: Status=Shipped, Tracking=TRK123456789, ETA=Jan 31
[Quality Reviewer formats response]
Response: "Your order 12345 has been shipped! Tracking number is TRK123456789. Expected delivery: Jan 31, 2026."

Time: ~2 seconds

Example 3: Complex Query
User: "Hi, what's your return policy and can you check order 67890?"

[Greeter identifies multiple intents]
[Researcher gets return FAQ: "30 days, unused items, original packaging"]
[Order Specialist finds order 67890: Status=Processing]
[Quality Reviewer combines both answers]
Response: "Hello! Our return policy allows returns within 30 days if items are unused and in original packaging. Your order 67890 is currently being processed and should ship soon."

Time: ~3 seconds

CHALLENGES & SOLUTIONS

1. Speed was terrible at first
   Problem: Local LLM (Ollama) took 2+ minutes per response
   Solution: Switched to Groq API - now 1-2 seconds

2. Agents being too chatty
   Problem: Quality Reviewer kept adding extra info not in the FAQ
   Solution: Added strict instructions to only use provided info, nothing extra

3. Coordination overhead
   Problem: Running all 6 agents for simple queries was slow
   Solution: Made a routing system - 2 agents for FAQ/orders, full team for complex stuff

4. Cost concerns
   Problem: Each agent call costs tokens
   Solution: Using Groq's free tier (30 req/min), optimized routing reduces calls

The agent team diagram is in agent_diagram.txt
