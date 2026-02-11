# LANGUAGE DETECTION AND RESPONSE SYSTEM
# ==============================================

import re
from typing import Dict, Tuple

class LanguageDetector:
    def __init__(self):
        self.language_patterns = {
            'mr': {
                'patterns': [
                    r'[ऀ-ॿ]+',  # Devanagari script
                    r'\b(मला|मी|तुम्ही|आहे|आहे|झाले|आहे|करते|आहे)\b',  # Common Marathi words
                    r'\b(दुखत|आजीब|ताप|थक्व|सर्दी|खांब|डोके)\b'  # Medical terms in Marathi
                ],
                'response_prefix': 'मराठीत:',
                'greeting': 'नमस्कार!'
            },
            'hi': {
                'patterns': [
                    r'[ऀ-ॿ]+',  # Devanagari script (Hindi)
                    r'\b(मुझे|मैं|तुम|है|गया|होता|करता)\b',  # Common Hindi words
                    r'\b(दर्द|बुखार|खांसी|पेट|सिर|गला)\b'  # Medical terms in Hindi
                ],
                'response_prefix': 'हिंदी में:',
                'greeting': 'नमस्ते!'
            },
            'en': {
                'patterns': [
                    r'[a-zA-Z]+',  # English script
                    r'\b(I|me|you|we|they|is|are|have|pain|fever)\b',  # Common English words
                    r'\b(stomach|head|body|pain|fever|cough|cold)\b'  # Medical terms in English
                ],
                'response_prefix': 'In English:',
                'greeting': 'Hello!'
            }
        }
    
    def detect_language(self, text: str) -> str:
        """Detect the primary language of the input text"""
        if not text:
            return 'en'  # Default to English
        
        text_lower = text.lower()
        language_scores = {}
        
        for lang, config in self.language_patterns.items():
            score = 0
            for pattern in config['patterns']:
                matches = re.findall(pattern, text_lower, re.IGNORECASE)
                score += len(matches)
            language_scores[lang] = score
        
        # Return language with highest score
        detected_lang = max(language_scores, key=language_scores.get)
        
        # Special handling for Devanagari script (distinguish Hindi vs Marathi)
        if detected_lang in ['mr', 'hi'] and re.search(r'[ऀ-ॿ]+', text):
            # Check for Marathi-specific indicators
            marathi_indicators = ['मला', 'मी', 'तुम्ही', 'आहे', 'झाले', 'आहे', 'करते', 'आहे', 'दुखत', 'दुखत', 'ताप', 'थक्व', 'सर्दी', 'खांब', 'डोके', 'दात', 'दुखत']
            hindi_indicators = ['मुझे', 'मैं', 'तुम', 'है', 'गया', 'होता', 'करता', 'दर्द', 'बुखार', 'खांसी', 'पेट', 'सिर', 'गला']
            
            marathi_count = sum(1 for word in marathi_indicators if word in text_lower)
            hindi_count = sum(1 for word in hindi_indicators if word in text_lower)
            
            # If Marathi indicators are found, prioritize Marathi
            if marathi_count > 0:
                return 'mr'
            elif hindi_count > 0:
                return 'hi'
        
        return detected_lang
    
    def get_response_language_config(self, detected_lang: str) -> Dict:
        """Get language-specific response configuration"""
        return self.language_patterns.get(detected_lang, self.language_patterns['en'])
    
    def create_multilingual_prompt(self, original_text: str, detected_lang: str, base_prompt: str) -> str:
        """Create a prompt that ensures response in the detected language"""
        lang_config = self.get_response_language_config(detected_lang)
        
        language_instructions = {
            'mr': """
CRITICAL: You MUST respond in MARATHI language ONLY.
Use Devanagari script (मराठी) for ALL responses.
DO NOT respond in English under any circumstances.
Be empathetic and caring in your responses.
Example responses:
- For pain: "मला समजले की तुम्हाले दुखत आहे. किती दिवसापासून हे दुखत आहे?"
- For advice: "कृपया घेऊ प्रयत्न करून्यास."
- For medicine: "आपण क्रोसिन (पॅरासिटामॉल ५००मग) घ्या."
""",
            'hi': """
CRITICAL: You MUST respond in HINDI language ONLY.
Use Devanagari script (हिंदी) for ALL responses.
DO NOT respond in English under any circumstances.
Be empathetic and caring in your responses.
Example responses:
- For pain: "मुझे समझ में आया कि आपको सिर दर्द है."
- For advice: "कृपया घेओ प्रयत्न करें।"
- For medicine: "आप पैरासिटामॉल लें।"
""",
            'en': """
Respond in ENGLISH language only.
Be empathetic and caring in your responses.
Example: "I understand you have a headache..."
"""
        }
        
        instruction = language_instructions.get(detected_lang, language_instructions['en'])
        
        return f"""
{base_prompt}

{instruction}

Original user input (in {detected_lang.upper()}): "{original_text}"
"""

# Global language detector instance
language_detector = LanguageDetector()

def detect_and_prepare_response(user_input: str, base_prompt: str) -> Tuple[str, str]:
    """Detect language and prepare multilingual prompt"""
    detected_lang = language_detector.detect_language(user_input)
    multilingual_prompt = language_detector.create_multilingual_prompt(user_input, detected_lang, base_prompt)
    
    return detected_lang, multilingual_prompt
