"""
Advanced Learning Engine for the Lumo AI
Enables self-learning, memory, pattern recognition, and intelligence growth
"""

import os
import json
import pickle
import numpy as np
from datetime import datetime
from collections import defaultdict
from sentence_transformers import SentenceTransformer


class AdaptiveMemory:
    """Manages conversation history and learns from interactions"""
    
    def __init__(self, memory_path="memory/conversation_history.json"):
        self.memory_path = memory_path
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        self.conversations = []
        self.user_preferences = defaultdict(int)
        self.interaction_count = 0
        self.learned_topics = set()
        
        # Ensure memory directory exists
        os.makedirs(os.path.dirname(memory_path), exist_ok=True)
        self.load_memory()
    
    def load_memory(self):
        """Load previous conversation history and learned patterns"""
        try:
            if os.path.exists(self.memory_path):
                with open(self.memory_path, 'r') as f:
                    data = json.load(f)
                    self.conversations = data.get("conversations", [])
                    self.user_preferences = defaultdict(int, data.get("preferences", {}))
                    self.interaction_count = data.get("interaction_count", 0)
                    self.learned_topics = set(data.get("learned_topics", []))
        except Exception as e:
            print(f"Error loading memory: {e}")
    
    def save_memory(self):
        """Save conversation history and learned patterns"""
        try:
            data = {
                "conversations": self.conversations[-100:],  # Keep last 100 conversations
                "preferences": dict(self.user_preferences),
                "interaction_count": self.interaction_count,
                "learned_topics": list(self.learned_topics)
            }
            with open(self.memory_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving memory: {e}")
    
    def add_interaction(self, user_input, ai_response, feedback=None):
        """Record a conversation interaction for learning"""
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "ai_response": ai_response,
            "feedback": feedback,
            "user_satisfaction": feedback.get("satisfaction", 5) if feedback else 5
        }
        
        self.conversations.append(interaction)
        self.interaction_count += 1
        
        # Extract topics from user input
        self._extract_topics(user_input)
        
        # Learn preferences
        self._update_preferences(user_input, feedback)
        
        self.save_memory()
    
    def _extract_topics(self, text):
        """Extract and learn topics from user input"""
        keywords = text.lower().split()
        for keyword in keywords:
            if len(keyword) > 4:  # Filter out small words
                self.learned_topics.add(keyword)
    
    def _update_preferences(self, user_input, feedback):
        """Learn user preferences from feedback"""
        if feedback:
            satisfaction = feedback.get("satisfaction", 5)
            words = user_input.lower().split()
            for word in words:
                if len(word) > 3:
                    self.user_preferences[word] += (satisfaction - 3)  # -2 to +2 scale
    
    def get_context_from_history(self, query, top_k=3):
        """Retrieve relevant previous conversations as context"""
        if not self.conversations:
            return []
        
        # Find similar conversations
        query_embedding = self.embedder.encode([query])[0]
        similarities = []
        
        for i, conv in enumerate(self.conversations):
            conv_embedding = self.embedder.encode([conv["user_input"]])[0]
            similarity = np.dot(query_embedding, conv_embedding)
            similarities.append((similarity, i))
        
        similarities.sort(reverse=True)
        similar_convs = [self.conversations[i] for _, i in similarities[:top_k]]
        
        return similar_convs
    
    def get_confidence_score(self):
        """Calculate AI's confidence based on interactions"""
        if self.interaction_count == 0:
            return 50
        
        total_satisfaction = sum(
            conv.get("user_satisfaction", 5) 
            for conv in self.conversations[-50:]
        )
        avg_satisfaction = total_satisfaction / min(50, len(self.conversations))
        confidence = (avg_satisfaction / 5) * 100
        
        return min(100, max(0, confidence))
    
    def get_learned_knowledge(self):
        """Return knowledge learned so far"""
        return {
            "total_interactions": self.interaction_count,
            "topics_learned": len(self.learned_topics),
            "confidence_score": self.get_confidence_score(),
            "key_topics": sorted(list(self.learned_topics))[:10]
        }


class PatternRecognition:
    """Identifies patterns in user queries and learns response patterns"""
    
    def __init__(self, patterns_path="memory/patterns.pkl"):
        self.patterns_path = patterns_path
        self.query_patterns = defaultdict(int)
        self.response_patterns = defaultdict(list)
        self.user_behavior = defaultdict(int)
        
        os.makedirs(os.path.dirname(patterns_path), exist_ok=True)
        self.load_patterns()
    
    def load_patterns(self):
        """Load learned patterns"""
        try:
            if os.path.exists(self.patterns_path):
                with open(self.patterns_path, 'rb') as f:
                    data = pickle.load(f)
                    self.query_patterns = data.get("query_patterns", defaultdict(int))
                    self.response_patterns = data.get("response_patterns", defaultdict(list))
                    self.user_behavior = data.get("user_behavior", defaultdict(int))
        except Exception as e:
            print(f"Error loading patterns: {e}")
    
    def save_patterns(self):
        """Save learned patterns"""
        try:
            data = {
                "query_patterns": dict(self.query_patterns),
                "response_patterns": dict(self.response_patterns),
                "user_behavior": dict(self.user_behavior)
            }
            with open(self.patterns_path, 'wb') as f:
                pickle.dump(data, f)
        except Exception as e:
            print(f"Error saving patterns: {e}")
    
    def learn_from_interaction(self, query, response, success=True):
        """Learn patterns from successful interactions"""
        # Extract key words from query
        keywords = [w for w in query.lower().split() if len(w) > 3]
        pattern_key = " ".join(keywords[:3])
        
        self.query_patterns[pattern_key] += 1
        if success:
            self.response_patterns[pattern_key].append(response)
        
        self.save_patterns()
    
    def get_suggested_response(self, query):
        """Get learned response patterns for similar queries"""
        keywords = [w for w in query.lower().split() if len(w) > 3]
        pattern_key = " ".join(keywords[:3])
        
        if pattern_key in self.response_patterns:
            responses = self.response_patterns[pattern_key]
            return responses[-1] if responses else None
        
        return None


class ContextualUnderstanding:
    """Maintains conversation context and adapts responses"""
    
    def __init__(self):
        self.current_context = {}
        self.user_mood = "neutral"
        self.conversation_flow = []
    
    def analyze_sentiment(self, text):
        """Simple sentiment analysis to understand user mood"""
        positive_words = ["good", "great", "excellent", "happy", "love", "awesome", "wonderful"]
        negative_words = ["bad", "terrible", "hate", "awful", "horrible", "sad", "angry"]
        
        text_lower = text.lower()
        
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if pos_count > neg_count:
            return "positive"
        elif neg_count > pos_count:
            return "negative"
        else:
            return "neutral"
    
    def update_context(self, user_input, ai_response):
        """Update conversation context based on interaction"""
        self.user_mood = self.analyze_sentiment(user_input)
        self.conversation_flow.append({
            "input": user_input,
            "output": ai_response,
            "mood": self.user_mood
        })
        
        # Keep only last 10 interactions
        if len(self.conversation_flow) > 10:
            self.conversation_flow = self.conversation_flow[-10:]
    
    def get_contextual_response(self):
        """Adapt response based on conversation context"""
        if self.user_mood == "negative":
            return "supportive"
        elif self.user_mood == "positive":
            return "enthusiastic"
        else:
            return "neutral"
    
    def get_previous_context(self, depth=3):
        """Get previous conversation context"""
        return self.conversation_flow[-depth:] if self.conversation_flow else []


class IntelligenceGrowth:
    """Tracks and manages AI intelligence growth over time"""
    
    def __init__(self, growth_path="memory/intelligence_metrics.json"):
        self.growth_path = growth_path
        self.intelligence_score = 50  # 0-100 scale
        self.accuracy_score = 50
        self.learning_rate = 0.05
        self.total_learned_concepts = 0
        
        os.makedirs(os.path.dirname(growth_path), exist_ok=True)
        self.load_metrics()
    
    def load_metrics(self):
        """Load previous intelligence metrics"""
        try:
            if os.path.exists(self.growth_path):
                with open(self.growth_path, 'r') as f:
                    data = json.load(f)
                    self.intelligence_score = data.get("intelligence_score", 50)
                    self.accuracy_score = data.get("accuracy_score", 50)
                    self.total_learned_concepts = data.get("total_learned_concepts", 0)
        except Exception as e:
            print(f"Error loading metrics: {e}")
    
    def save_metrics(self):
        """Save intelligence metrics"""
        try:
            data = {
                "intelligence_score": self.intelligence_score,
                "accuracy_score": self.accuracy_score,
                "total_learned_concepts": self.total_learned_concepts,
                "last_updated": datetime.now().isoformat()
            }
            with open(self.growth_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving metrics: {e}")
    
    def learn_from_feedback(self, feedback_score):
        """Update intelligence based on user feedback"""
        # feedback_score: 1-5 scale
        improvement = (feedback_score - 3) * self.learning_rate
        
        self.accuracy_score = min(100, max(0, self.accuracy_score + improvement))
        self.intelligence_score = min(100, max(0, self.intelligence_score + improvement * 0.7))
        self.total_learned_concepts += 1
        
        self.save_metrics()
    
    def get_growth_status(self):
        """Return current growth status"""
        return {
            "intelligence_level": round(self.intelligence_score, 1),
            "accuracy": round(self.accuracy_score, 1),
            "concepts_learned": self.total_learned_concepts,
            "learning_rate": self.learning_rate,
            "status": self._get_status_message()
        }
    
    def _get_status_message(self):
        """Generate status message based on current intelligence"""
        if self.intelligence_score < 30:
            return "Learning stage - still building foundational knowledge"
        elif self.intelligence_score < 60:
            return "Growing - becoming more capable"
        elif self.intelligence_score < 80:
            return "Advanced - highly capable and knowledgeable"
        else:
            return "Expert level - vast knowledge and high accuracy"


# Initialize all learning components
adaptive_memory = AdaptiveMemory()
pattern_recognition = PatternRecognition()
contextual_understanding = ContextualUnderstanding()
intelligence_growth = IntelligenceGrowth()
