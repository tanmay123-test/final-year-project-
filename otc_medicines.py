# OTC MEDICINES RECOMMENDATIONS
# ==============================================

OTC_MEDICINES = {
    "fever": {
        "primary": "Crocin (Paracetamol 500mg)",
        "alternatives": ["Calpol", "Paracetamol", "Tylenol"],
        "dosage": "1 tablet every 4-6 hours (max 4 tablets/day)",
        "notes": "Take with food, avoid alcohol"
    },
    "headache": {
        "primary": "Crocin (Paracetamol 500mg)",
        "alternatives": ["Aspirin", "Ibuprofen", "Disprin"],
        "dosage": "1 tablet every 4-6 hours as needed",
        "notes": "Take after food, rest in quiet room"
    },
    "cold": {
        "primary": "Vicks Action 500",
        "alternatives": ["D-Cold", "Coryzal", "Sinarest"],
        "dosage": "1 tablet twice daily after meals",
        "notes": "Avoid driving, may cause drowsiness"
    },
    "cough": {
        "primary": "Benadryl Cough Syrup",
        "alternatives": ["Corex", "Ascoril", "Dabur Honitus"],
        "dosage": "2 teaspoons 2-3 times daily",
        "notes": "Take after meals, avoid alcohol"
    },
    "stomach_pain": {
        "primary": "Digene (Antacid)",
        "alternatives": ["Gelusil", "Eno", "Pepcid"],
        "dosage": "1-2 tablets as needed after meals",
        "notes": "Avoid spicy food, take with water"
    },
    "body_ache": {
        "primary": "Ibuprofen 400mg",
        "alternatives": ["Combiflam", "Brufen", "Volini Spray"],
        "dosage": "1 tablet every 6-8 hours with food",
        "notes": "Take with food, avoid if stomach issues"
    },
    "sore_throat": {
        "primary": "Betadine Gargle",
        "alternatives": ["Strepsils", "Vicks VapoRub", "Himalaya Koflet"],
        "dosage": "Gargle 2-3 times daily",
        "notes": "Warm water gargle, avoid cold drinks"
    },
    "allergy": {
        "primary": "Cetrizine 10mg",
        "alternatives": ["Avil", "Allegra", "Loratadine"],
        "dosage": "1 tablet daily at night",
        "notes": "May cause drowsiness, avoid driving"
    },
    "indigestion": {
        "primary": "Eno (Antacid)",
        "alternatives": ["Digene", "Pudin Hara", "Hajmola"],
        "dosage": "1 sachet in water as needed",
        "notes": "Take after meals, avoid heavy food"
    },
    "diarrhea": {
        "primary": "Electral (ORS)",
        "alternatives": ["Norflox-TZ", "Enterogermina", "Zincovit"],
        "dosage": "1 sachet in 1 liter water, sip throughout day",
        "notes": "Maintain hydration, avoid dairy products"
    },
    "tooth_pain": {
        "primary": "Orajel (Benzocaine Gel)",
        "alternatives": ["Colgate Pain Out", "Anbesol", "Clove Oil"],
        "dosage": "Apply small amount to affected area 3-4 times daily",
        "notes": "For temporary relief only. See dentist if pain persists"
    },
    "eye_pain": {
        "primary": "Lubricating Eye Drops",
        "alternatives": ["Refresh Tears", "Systane Ultra", "Artificial Tears"],
        "dosage": "1-2 drops in each eye 3-4 times daily",
        "notes": "For dryness and irritation. See doctor if pain persists"
    },
    "ear_pain": {
        "primary": "Otocalm Ear Drops",
        "alternatives": ["Ciplox Ear Drops", "Sofradex", "Gentamicin Ear Drops"],
        "dosage": "2-3 drops in affected ear 2-3 times daily",
        "notes": "For external ear infections only. See doctor if severe"
    }
}

def get_otc_medicine(symptoms: str) -> dict:
    """Get medically accurate OTC medicine recommendation based on symptoms"""
    symptoms_lower = symptoms.lower()
    
    # Medically accurate symptom analysis with proper recommendations
    medical_guidelines = {
        # Dental issues - Usually require dental consultation, not self-medication
        'tooth pain': {
            "action": "refer_dentist",
            "primary": "Orajel (Benzocaine Gel) - Temporary Only",
            "alternatives": ["Colgate Pain Out", "Clove Oil"],
            "dosage": "Apply small amount to affected area 3-4 times daily",
            "notes": "TEMPORARY RELIEF ONLY. See dentist within 24 hours. Do not rely on painkillers for dental issues.",
            "condition": "Dental Pain - Requires Dental Consultation"
        },
        'toothache': {
            "action": "refer_dentist", 
            "primary": "Orajel (Benzocaine Gel) - Temporary Only",
            "alternatives": ["Colgate Pain Out", "Clove Oil"],
            "dosage": "Apply small amount to affected area 3-4 times daily",
            "notes": "TEMPORARY RELIEF ONLY. See dentist within 24 hours. Do not rely on painkillers for dental issues.",
            "condition": "Dental Pain - Requires Dental Consultation"
        },
        'dental pain': {
            "action": "refer_dentist",
            "primary": "Orajel (Benzocaine Gel) - Temporary Only", 
            "alternatives": ["Colgate Pain Out", "Clove Oil"],
            "dosage": "Apply small amount to affected area 3-4 times daily",
            "notes": "TEMPORARY RELIEF ONLY. See dentist within 24 hours. Do not rely on painkillers for dental issues.",
            "condition": "Dental Pain - Requires Dental Consultation"
        },
        'gum pain': {
            "action": "refer_dentist",
            "primary": "Orajel (Benzocaine Gel) - Temporary Only",
            "alternatives": ["Colgate Pain Out", "Clove Oil"], 
            "dosage": "Apply small amount to affected area 3-4 times daily",
            "notes": "TEMPORARY RELIEF ONLY. See dentist within 24 hours. Do not rely on painkillers for dental issues.",
            "condition": "Dental Pain - Requires Dental Consultation"
        },
        
        # Fever - Only recommend if actually feverish
        'fever': {
            "action": "otc_safe",
            "primary": "Crocin (Paracetamol 500mg)",
            "alternatives": ["Calpol", "Paracetamol"],
            "dosage": "1 tablet every 4-6 hours (max 4 tablets/day)",
            "notes": "Take with food. Monitor temperature. See doctor if fever > 102°F or lasts > 3 days.",
            "condition": "Fever"
        },
        'temperature': {
            "action": "otc_safe",
            "primary": "Crocin (Paracetamol 500mg)",
            "alternatives": ["Calpol", "Paracetamol"],
            "dosage": "1 tablet every 4-6 hours (max 4 tablets/day)",
            "notes": "Take with food. Monitor temperature. See doctor if fever > 102°F or lasts > 3 days.",
            "condition": "Fever"
        },
        
        # Headache - Differentiate types
        'headache': {
            "action": "otc_safe",
            "primary": "Crocin (Paracetamol 500mg)",
            "alternatives": ["Aspirin", "Ibuprofen"],
            "dosage": "1 tablet every 4-6 hours as needed",
            "notes": "Take with food. See doctor if severe, sudden, or accompanied by other symptoms.",
            "condition": "Headache"
        },
        'migraine': {
            "action": "refer_doctor",
            "primary": "No OTC - Requires Medical Evaluation",
            "alternatives": [],
            "dosage": "Do not self-medicate",
            "notes": "Migraine requires prescription medication. See doctor for proper treatment.",
            "condition": "Migraine - Medical Consultation Required"
        },
        
        # Cold/Cough - Symptom-specific
        'cold': {
            "action": "otc_safe",
            "primary": "Vicks Action 500",
            "alternatives": ["D-Cold", "Coryzal"],
            "dosage": "1 tablet twice daily after meals",
            "notes": "May cause drowsiness. Avoid driving. See doctor if symptoms worsen or last > 7 days.",
            "condition": "Common Cold"
        },
        'cough': {
            "action": "otc_safe",
            "primary": "Benadryl Cough Syrup",
            "alternatives": ["Corex", "Ascoril"],
            "dosage": "2 teaspoons 2-3 times daily",
            "notes": "Take after meals. See doctor if cough lasts > 1 week or produces blood/discolored phlegm.",
            "condition": "Cough"
        },
        'dry cough': {
            "action": "otc_safe",
            "primary": "Benadryl Cough Syrup",
            "alternatives": ["Corex", "Ascoril"],
            "dosage": "2 teaspoons 2-3 times daily",
            "notes": "Take after meals. See doctor if cough lasts > 1 week or produces blood/discolored phlegm.",
            "condition": "Dry Cough"
        },
        
        # Stomach/GI issues
        'stomach pain': {
            "action": "symptom_specific",
            "primary": "Digene (Antacid)",
            "alternatives": ["Gelusil", "Eno"],
            "dosage": "1-2 tablets as needed after meals",
            "notes": "For mild indigestion only. See doctor if severe, persistent, or accompanied by fever/vomiting.",
            "condition": "Stomach Pain"
        },
        'indigestion': {
            "action": "otc_safe",
            "primary": "Eno (Antacid)",
            "alternatives": ["Digene", "Pudin Hara"],
            "dosage": "1 sachet in water as needed",
            "notes": "Take after meals. See doctor if frequent or severe.",
            "condition": "Indigestion"
        },
        'acidity': {
            "action": "otc_safe",
            "primary": "Digene (Antacid)",
            "alternatives": ["Gelusil", "Eno"],
            "dosage": "1-2 tablets as needed after meals",
            "notes": "Avoid spicy foods. See doctor if chronic or severe.",
            "condition": "Acidity"
        },
        
        # Body pain
        'body ache': {
            "action": "otc_safe",
            "primary": "Ibuprofen 400mg",
            "alternatives": ["Combiflam", "Brufen"],
            "dosage": "1 tablet every 6-8 hours with food",
            "notes": "Take with food to avoid stomach irritation. See doctor if pain is severe or persistent.",
            "condition": "Body Ache"
        },
        'muscle pain': {
            "action": "otc_safe",
            "primary": "Ibuprofen 400mg",
            "alternatives": ["Combiflam", "Brufen"],
            "dosage": "1 tablet every 6-8 hours with food",
            "notes": "Take with food. Apply warm compress if localized. See doctor if severe.",
            "condition": "Muscle Pain"
        },
        
        # Sore throat
        'sore throat': {
            "action": "otc_safe",
            "primary": "Betadine Gargle",
            "alternatives": ["Strepsils", "Himalaya Koflet"],
            "dosage": "Gargle 2-3 times daily",
            "notes": "Warm water gargle. Avoid cold drinks. See doctor if severe or lasts > 3 days.",
            "condition": "Sore Throat"
        },
        'throat pain': {
            "action": "otc_safe",
            "primary": "Betadine Gargle",
            "alternatives": ["Strepsils", "Himalaya Koflet"],
            "dosage": "Gargle 2-3 times daily",
            "notes": "Warm water gargle. Avoid cold drinks. See doctor if severe or lasts > 3 days.",
            "condition": "Sore Throat"
        },
        
        # Allergy
        'allergy': {
            "action": "otc_safe",
            "primary": "Cetrizine 10mg",
            "alternatives": ["Avil", "Loratadine"],
            "dosage": "1 tablet daily at night",
            "notes": "May cause drowsiness. Avoid driving. See doctor if severe reaction.",
            "condition": "Allergy"
        },
        
        # Eye issues - Usually require medical consultation
        'eye pain': {
            "action": "refer_doctor",
            "primary": "No OTC - Requires Medical Evaluation",
            "alternatives": [],
            "dosage": "Do not self-medicate eye issues",
            "notes": "Eye pain requires immediate medical evaluation. See ophthalmologist.",
            "condition": "Eye Pain - Medical Consultation Required"
        },
        
        # Ear issues - Usually require medical consultation  
        'ear pain': {
            "action": "refer_doctor",
            "primary": "No OTC - Requires Medical Evaluation",
            "alternatives": [],
            "dosage": "Do not self-medicate ear issues",
            "notes": "Ear pain requires medical evaluation. See ENT specialist.",
            "condition": "Ear Pain - Medical Consultation Required"
        },
        
        # Diarrhea
        'diarrhea': {
            "action": "otc_safe",
            "primary": "Electral (ORS)",
            "alternatives": ["Zincovit", "Enterogermina"],
            "dosage": "1 sachet in 1 liter water, sip throughout day",
            "notes": "Maintain hydration. See doctor if bloody, severe, or lasts > 2 days.",
            "condition": "Diarrhea"
        }
    }
    
    # Check for specific symptoms with medical accuracy
    for symptom_pattern, medical_data in medical_guidelines.items():
        if symptom_pattern in symptoms_lower:
            return medical_data
    
    # Default for general pain - conservative approach
    return {
        "action": "otc_safe",
        "primary": "Crocin (Paracetamol 500mg)",
        "alternatives": ["Paracetamol", "Calpol"],
        "dosage": "1 tablet every 4-6 hours as needed",
        "notes": "Take with food. See doctor if symptoms persist or worsen.",
        "condition": "General Pain"
    }

def format_otc_recommendation(medicine_data: dict) -> str:
    """Format OTC medicine recommendation for display"""
    return f"""
💊 Recommended Medicine: {medicine_data['primary']}
🔄 Alternatives: {', '.join(medicine_data['alternatives'])}
📏 Dosage: {medicine_data['dosage']}
⚠️ Notes: {medicine_data['notes']}
🏷️ For: {medicine_data['condition']}
"""
