import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import requests
from dotenv import load_dotenv
from datetime import datetime
import random
from models.learning_engine import (
    adaptive_memory,
    pattern_recognition,
    contextual_understanding,
    intelligence_growth
)
from models.advanced_learning import (
    multi_turn_manager,
    quality_analyzer,
    learning_rate_manager,
    knowledge_tracker,
    proactive_learner
)

load_dotenv()

# Config
LOCAL_MODEL = int(os.getenv("LOCAL_MODEL", 1))
FAISS_DIM = int(os.getenv("FAISS_DIM", 384))
FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH", "memory/faiss_index.pkl")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
GOOGLE_SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID")


def load_faiss_index():
    if os.path.exists(FAISS_INDEX_PATH):
        with open(FAISS_INDEX_PATH, "rb") as f:
            index = pickle.load(f)
    else:
        index = faiss.IndexFlatL2(FAISS_DIM)
    return index


def save_faiss_index(index):
    with open(FAISS_INDEX_PATH, "wb") as f:
        pickle.dump(index, f)


# Embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")
faiss_index = load_faiss_index()
faiss_texts = []  # Keep actual texts to return


def add_to_index(texts):
    embeddings = embedder.encode(texts)
    faiss_index.add(np.array(embeddings, dtype=np.float32))
    faiss_texts.extend(texts)
    save_faiss_index(faiss_index)
    # Save texts alongside FAISS
    with open("memory/faiss_texts.pkl", "wb") as f:
        pickle.dump(faiss_texts, f)


# Load texts
if os.path.exists("memory/faiss_texts.pkl"):
    with open("memory/faiss_texts.pkl", "rb") as f:
        faiss_texts = pickle.load(f)


def search_index(query, top_k=3):
    query_vec = embedder.encode([query])
    distances, indices = faiss_index.search(
        np.array(query_vec, dtype=np.float32), top_k
    )
    results = [faiss_texts[i] if i != -1 else None
               for i in indices[0]]
    return results


def web_search(query, num_results=3):
    """Perform a Google web search"""
    if not GOOGLE_SEARCH_API_KEY or not GOOGLE_SEARCH_ENGINE_ID:
        return None

    try:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "q": query,
            "key": GOOGLE_SEARCH_API_KEY,
            "cx": GOOGLE_SEARCH_ENGINE_ID,
            "num": num_results
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            results = response.json().get("items", [])
            return [{"title": r.get("title"),
                     "snippet": r.get("snippet"),
                     "link": r.get("link")}
                    for r in results]
    except Exception as e:
        print(f"Web search error: {e}")
    return None


def generate_response(prompt):
    """
    Generate intelligent responses with conditional logic, learning
    capabilities, and adaptive intelligence that grows over time
    """
    try:
        prompt_lower = prompt.lower().strip()

        # Update contextual understanding with user input
        contextual_understanding.user_mood = (
            contextual_understanding.analyze_sentiment(prompt)
        )
        _ = contextual_understanding.get_contextual_response()

        # Add to multi-turn context manager
        multi_turn_manager.add_turn(prompt, "")  # Will update with response

        # Check for knowledge gaps - ask clarifying questions if needed
        if proactive_learner.identify_gap(prompt):
            _ = proactive_learner.generate_clarification(prompt)
            # Don't interrupt with clarification unless confidence low
            pass

        # Check for learned patterns first
        learned_response = pattern_recognition.get_suggested_response(prompt)
        if learned_response and len(prompt) > 3:  # Avoid single words
            adaptive_memory.add_interaction(prompt, learned_response)
            return learned_response

        # ===== CONDITIONAL HOW ARE YOU =====
        how_are_you_keywords = ["how are you", "how's it going",
                                "how do you feel", "how you doing"]
        if any(keyword in prompt_lower for keyword in how_are_you_keywords):
            responses = [
                "I'm doing great, thanks for asking! Ready to help.",
                "I'm functioning perfectly and here to assist!",
                "All systems running smoothly! What can I do for you?"
            ]
            response = random.choice(responses)
            adaptive_memory.add_interaction(prompt, response)
            pattern_recognition.learn_from_interaction(
                prompt, response, True)
            return response

        # ===== CONDITIONAL GREETINGS =====
        if any(keyword in prompt_lower
               for keyword in ["hello", "hi", "hey", "greetings"]):
            greetings = [
                "Hello! How can I help you today?",
                "Hi there! What would you like to know?",
                "Hey! I'm here to assist you. What do you need?",
                "Greetings! How can I be of service?"
            ]
            response = random.choice(greetings)
            adaptive_memory.add_interaction(prompt, response)
            pattern_recognition.learn_from_interaction(
                prompt, response, True)
            return response

        # ===== CONDITIONAL AI STATUS =====
        status_keywords = ["status", "intelligence level", "how smart",
                           "tell me about yourself", "ai status",
                           "whats your"]
        if any(keyword in prompt_lower for keyword in status_keywords):
            # Make sure it's actually asking about status
            if any(word in prompt_lower for word in
                   ["status", "smart", "intelligent", "level",
                    "yourself", "ability", "capabilities as"]):
                growth = intelligence_growth.get_growth_status()
                knowledge = adaptive_memory.get_learned_knowledge()

                status_message = f"""🤖 AI Intelligence Status:
━━━━━━━━━━━━━━━━━━━━━━
Intelligence Level: {growth['intelligence_level']}/100
Accuracy: {growth['accuracy']}/100
Concepts Learned: {growth['concepts_learned']}
Status: {growth['status']}

📚 Knowledge Stats:
Total Interactions: {knowledge['total_interactions']}
Topics Learned: {knowledge['topics_learned']}
Confidence Score: {knowledge['confidence_score']:.1f}%

I'm constantly learning and improving!"""

                adaptive_memory.add_interaction(prompt, status_message)
                return status_message

        # ===== CONDITIONAL WEB SEARCH CAPABILITY =====
        ws_cap_keywords = ["can you do a web search",
                           "web search capability",
                           "can you search the web",
                           "do you support web search"]
        if any(keyword in prompt_lower for keyword in ws_cap_keywords):
            if GOOGLE_SEARCH_API_KEY and GOOGLE_SEARCH_ENGINE_ID:
                response = ("Yes! I can perform web searches. Just ask "
                            "me to 'search for' or 'find' something!")
            else:
                response = ("I can do web searches, but need API keys first."
                            "\n\n1. Get a Google Custom Search API key\n"
                            "2. Create a Custom Search Engine\n"
                            "3. Add to .env file")

            adaptive_memory.add_interaction(prompt, response)
            return response

        # ===== CONDITIONAL HELP REQUEST =====
        if any(keyword in prompt_lower
               for keyword in ["help", "what can you do",
                               "what are your features"]):
            help_text = ("I can help you with:\n"
                         "✓ Answer questions about various topics\n"
                         "✓ Search the web for current information\n"
                         "✓ Retrieve information from knowledge base\n"
                         "✓ Have intelligent conversations\n"
                         "✓ Learn and grow from interactions\n"
                         "✓ Adapt to your preferences and style\n"
                         "✓ Provide summaries and explanations")
            adaptive_memory.add_interaction(prompt, help_text)
            return help_text

        # ===== CONDITIONAL SELF-IMPROVEMENT DISCUSSION =====
        improve_keywords = ["improve your intelligence", "build on yourself",
                            "how can you improve", "how do you learn",
                            "how else can you", "ways to improve",
                            "improve yourself"]
        if any(keyword in prompt_lower for keyword in improve_keywords):
            growth = intelligence_growth.get_growth_status()

            improvement_response = f"""🚀 Ways I Build & Improve Myself:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Current Status: {growth['status']}
Learning Rate: {growth['learning_rate']}

📈 HOW I IMPROVE:

1️⃣ LEARNING FROM INTERACTIONS
   • Every conversation teaches me something new
   • I analyze what responses work

2️⃣ MEMORY & PATTERN RECOGNITION
   • I remember past conversations
   • I identify patterns in successful responses

3️⃣ ADAPTIVE LEARNING
   • Learning rate adjusts based on performance

4️⃣ SEMANTIC UNDERSTANDING
   • Build relationships between concepts

5️⃣ MULTI-TURN CONTEXT
   • Maintain conversation history

6️⃣ KNOWLEDGE GRAPH BUILDING
   • Build networks of related concepts

📊 MY CURRENT IMPROVEMENT PATH:
• Concepts Learned: {growth['concepts_learned']}
• Intelligence Level: {growth['intelligence_level']}/100
• Accuracy: {growth['accuracy']}/100"""

            adaptive_memory.add_interaction(prompt, improvement_response)
            pattern_recognition.learn_from_interaction(
                prompt, improvement_response, True)
            contextual_understanding.update_context(
                prompt, improvement_response)
            intelligence_growth.learn_from_feedback(5)

            return improvement_response

        # ===== CONDITIONAL COMPREHENSIVE DEMO =====
        demo_keywords = ["do all of that", "demonstrate",
                         "show me everything", "give me your feedback"]
        if any(keyword in prompt_lower for keyword in demo_keywords):
            growth = intelligence_growth.get_growth_status()
            knowledge = adaptive_memory.get_learned_knowledge()

            demo_response = f"""🎯 Comprehensive AI Demonstration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 CURRENT PERFORMANCE METRICS:
• Intelligence Level: {growth['intelligence_level']}/100
• Accuracy Score: {growth['accuracy']}/100
• Total Interactions: {knowledge['total_interactions']}
• Topics Learned: {knowledge['topics_learned']}
• Confidence: {knowledge['confidence_score']:.1f}%

🚀 CAPABILITIES DEMONSTRATED:
✓ Natural language understanding
✓ Contextual awareness
✓ Adaptive responses
✓ Learning system
✓ Pattern recognition
✓ Real-time metrics
✓ Persistent memory"""

            adaptive_memory.add_interaction(prompt, demo_response)
            pattern_recognition.learn_from_interaction(
                prompt, demo_response, True)
            contextual_understanding.update_context(
                prompt, demo_response)
            intelligence_growth.learn_from_feedback(5)

            return demo_response

        # ===== CONDITIONAL TIME/DATE =====
        if any(keyword in prompt_lower
               for keyword in ["what time", "current time",
                               "what's the time", "date"]):
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            response = f"The current time is: {current_time}"
            adaptive_memory.add_interaction(prompt, response)
            return response

        # ===== CONDITIONAL APPRECIATION =====
        if any(keyword in prompt_lower
               for keyword in ["thank", "thanks", "appreciate",
                               "thank you"]):
            thanks_responses = [
                "You're welcome! Happy to help!",
                "Glad I could help! Anything else?",
                "My pleasure! Let me know if you need anything.",
                "You're welcome! Feel free to ask more."
            ]
            response = random.choice(thanks_responses)
            adaptive_memory.add_interaction(prompt, response)
            intelligence_growth.learn_from_feedback(5)
            return response

        # ===== CONDITIONAL SIMPLE AGREEMENT =====
        simple_agreements = ["alright", "great", "sounds good", "ok",
                             "okay", "yes", "yep", "sure", "cool",
                             "nice", "awesome"]
        if prompt_lower in simple_agreements:
            agreement_responses = [
                "Great! I'm ready to help. What do you need?",
                "Awesome! What's on your mind?",
                "Perfect! How can I assist you next?",
                "Glad you're satisfied! Ask me anything.",
                "Ready when you are! What do you need?"
            ]
            response = random.choice(agreement_responses)
            adaptive_memory.add_interaction(prompt, response)
            return response

        # ===== CONDITIONAL ASK QUESTIONS =====
        if any(keyword in prompt_lower
               for keyword in ["ask me questions", "ask me something",
                               "question time", "quiz me", "test me"]):
            questions = [
                "What's your favorite programming language and why?",
                "If you could learn any skill instantly, "
                "what would it be?",
                "What's the most interesting thing you've learned?",
                "How do you usually approach solving problems?",
                "What motivates you most in your work?",
                "If you could teach me one thing, what would it be?",
                "What's the biggest challenge you're facing?",
                "How do you prefer to learn new information?"
            ]
            question = random.choice(questions)
            response = f"Sure! Here's a question for you:\n\n{question}"
            adaptive_memory.add_interaction(prompt, response)
            return response

        # ===== CONDITIONAL WEB SEARCH REQUEST =====
        search_keywords = ["search the web", "web search", "search online",
                           "google", "find online", "look it up",
                           "increase your knowledge"]
        if any(keyword in prompt_lower for keyword in search_keywords):
            if GOOGLE_SEARCH_API_KEY and GOOGLE_SEARCH_ENGINE_ID:
                search_query = prompt.replace(
                    "search the web for", "").replace(
                    "search the web", "").replace(
                    "search online", "").strip()
                if not search_query or search_query in prompt_lower:
                    search_query = "latest technology trends"

                search_results = web_search(search_query)
                if search_results:
                    response = (f"🔍 Web Search Results for: "
                                f"'{search_query}'\n"
                                f"━━━━━━━━━━━━━━━━━━━━━━\n")
                    for i, result in enumerate(search_results, 1):
                        response += (f"\n{i}. {result['title']}\n"
                                     f"   {result['snippet']}\n"
                                     f"   🔗 {result['link']}\n")

                    response += ("\n✅ Knowledge increased! I've learned "
                                 "from these sources.")
                    adaptive_memory.add_interaction(prompt, response)
                    intelligence_growth.learn_from_feedback(4)
                    return response

            response = ("I can search the web, but I need API keys first.\n"
                        "To enable web search:\n"
                        "1. Get an API key\n"
                        "2. Create a Custom Search Engine\n"
                        "3. Add to .env file")
            adaptive_memory.add_interaction(prompt, response)
            return response

        # ===== WEB SEARCH DETECTION =====
        web_search_keywords = ["search", "find", "look up", "web",
                               "latest", "current", "news", "recent",
                               "google"]
        is_web_search_query = any(keyword in prompt_lower
                                  for keyword in web_search_keywords)

        context = ""

        # Get similar past interactions for context (limited)
        past_interactions = (
            adaptive_memory.get_context_from_history(prompt, top_k=1)
        )
        if (past_interactions and
                past_interactions[0].get("user_satisfaction", 5) > 3):
            context += (f"Previous similar: "
                        f"{past_interactions[0]['ai_response'][:100]}...")

        # Try local FAISS first (simplified)
        if LOCAL_MODEL and not is_web_search_query:
            hits = search_index(prompt)
            if hits and hits[0]:
                context += f"Knowledge: {hits[0]}\n"

        # Do web search if requested or if local search didn't help
        if is_web_search_query or not context:
            search_results = web_search(prompt)
            if search_results:
                context = "Web results:\n"
                for i, result in enumerate(search_results, 1):
                    context += (f"{i}. {result['title']}: "
                                f"{result['snippet']}\n")

        # ===== GENERATE RESPONSE WITH LEARNING =====
        if OPENAI_API_KEY:
            try:
                growth_info = intelligence_growth.get_growth_status()
                system_prompt = (
                    f"You are an intelligent AI assistant that learns "
                    f"and grows over time.\n"
                    f"Intelligence level: {growth_info['intelligence_level']}"
                    f"/100\n"
                    f"Accuracy rating: {growth_info['accuracy']}/100\n"
                    f"Status: {growth_info['status']}\n\n"
                    f"Adapt your response based on conversation context. "
                    f"Be helpful, accurate, and continue learning.\n"
                    f"Use the provided context to answer accurately."
                )

                if context:
                    system_prompt += f"\nContext available:\n{context}"

                headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
                json_data = {
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                }
                r = requests.post(OPENAI_API_URL, headers=headers,
                                  json=json_data, timeout=10)

                if r.status_code != 200:
                    error_detail = r.text
                    try:
                        error_json = r.json()
                        error_detail = (
                            error_json.get("error", {}).get("message",
                                                            error_detail)
                        )
                    except Exception:
                        pass
                    raise Exception(
                        f"OpenAI API error (status {r.status_code}): "
                        f"{error_detail}"
                    )

                response_json = r.json()
                if "choices" not in response_json:
                    raise Exception(
                        f"Unexpected API response: {response_json}"
                    )

                response = response_json["choices"][0]["message"]["content"]

                # Learn from successful response
                adaptive_memory.add_interaction(prompt, response)
                pattern_recognition.learn_from_interaction(
                    prompt, response, True)
                contextual_understanding.update_context(
                    prompt, response)

                # Update advanced learning systems
                multi_turn_manager.conversation_history[-1]["ai"] = response
                quality_analyzer.analyze_response(prompt, response, 4)
                learning_rate_manager.update_learning_rate(4)
                knowledge_tracker.record_learning(
                    prompt.split()[0] if prompt.split() else "general",
                    prompt, 0.8)
                intelligence_growth.learn_from_feedback(4)

                return response

            except Exception as e:
                print(f"OpenAI API error: {e}")
                if context:
                    response = context.split('\n')[0]
                else:
                    response = "I encountered an error. Try rephrasing."

                adaptive_memory.add_interaction(prompt, response)
                return response
        else:
            # No OpenAI key - return concise response
            if context:
                context_lines = context.split('\n')[:3]
                response = '\n'.join(context_lines)
            else:
                response = ("I need OPENAI_API_KEY in .env for better "
                            "responses. Ask me anything!")

            adaptive_memory.add_interaction(prompt, response)
            intelligence_growth.learn_from_feedback(3)
            return response

    except Exception as e:
        print(f"Error in generate_response: {e}")
        error_response = f"Error: {str(e)}"
        adaptive_memory.add_interaction(prompt, error_response)
        return error_response
