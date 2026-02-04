SCREENSHOT INSTRUCTIONS

For complete submission, take these screenshots while system is running:

1. screenshot_ui_faq.png
   - Browser showing "What is your shipping policy?" query and response
   - Shows clean UI and fast response

2. screenshot_ui_order.png
   - Browser showing "Check order 12345" query
   - Shows order tracking working

3. screenshot_ui_complex.png
   - Browser showing the complex multi-part query
   - Demonstrates agent coordination

4. screenshot_terminal.png
   - Backend terminal showing agent activity
   - Shows which agents activated for each query
   - Proves multi-agent orchestration is working

5. screenshot_architecture.png (optional)
   - Could be a simple diagram drawn in any tool
   - Or just use the agent_diagram.txt

To run the system for screenshots:
- Backend: cd backend && source venv/bin/activate && python app_multiagent.py
- Frontend: cd frontend && npm run dev
- Open http://localhost:5173
- Type queries and screenshot results
