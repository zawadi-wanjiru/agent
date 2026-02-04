"""
Multi-Agent Customer Care Backend (Lab 2)
Flask API that uses CrewAI multi-agent system
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from crew_optimized import process_customer_inquiry  # OPTIMIZED VERSION

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Store conversation history per session (in-memory for demo)
# In production, use Redis or database
conversation_sessions = {}


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Handle customer messages using multi-agent crew
    """
    try:
        data = request.json
        user_message = data.get('message', '')
        session_id = data.get('session_id', 'default')  # Track conversation sessions
        
        if not user_message.strip():
            return jsonify({'response': 'Please enter a message.'}), 400
        
        # Get or create conversation history for this session
        if session_id not in conversation_sessions:
            conversation_sessions[session_id] = []
        
        conversation_history = conversation_sessions[session_id]
        
        # Add user message to history
        conversation_history.append({
            'role': 'user',
            'content': user_message
        })
        
        # Process with multi-agent crew
        print(f"\n{'='*60}")
        print(f"Processing customer inquiry: {user_message}")
        print(f"{'='*60}\n")
        
        result = process_customer_inquiry(user_message, conversation_history)
        
        response_text = result['response']
        metadata = result.get('metadata', {})
        
        # Add assistant response to history
        conversation_history.append({
            'role': 'assistant',
            'content': response_text
        })
        
        # Keep only last 20 messages to prevent memory bloat
        if len(conversation_history) > 20:
            conversation_sessions[session_id] = conversation_history[-20:]
        
        return jsonify({
            'response': response_text,
            'metadata': metadata,
            'session_id': session_id
        })
        
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            'response': 'Sorry, I encountered an error. Please try again.',
            'error': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'system': 'multi-agent',
        'agents': 6
    })


@app.route('/api/reset', methods=['POST'])
def reset_session():
    """Reset conversation history for a session"""
    try:
        data = request.json
        session_id = data.get('session_id', 'default')
        
        if session_id in conversation_sessions:
            del conversation_sessions[session_id]
        
        return jsonify({'status': 'session reset'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("="*60)
    print("Starting Multi-Agent Customer Care System (Lab 2)")
    print("="*60)
    print("\nAgent Team:")
    print("  1. Greeter / Intent Classifier")
    print("  2. Researcher / Knowledge Retriever")
    print("  3. Order Specialist")
    print("  4. Resolver / Action Taker")
    print("  5. Quality Reviewer (Reflection)")
    print("  6. Supervisor (Orchestrator)")
    print("\nPowered by Groq API (ultra-fast inference)")
    print("="*60)
    print()
    
    app.run(debug=True, port=5000)
