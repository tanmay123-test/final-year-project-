# AI-DRIVEN DOCTOR SPECIALIZATION ANALYZER
# ==============================================

import json
from typing import List, Dict, Optional

class AIDoctorAnalyzer:
    def __init__(self):
        self.medical_specialization_map = {
            # Dental issues
            'dental': 'Dentist',
            'tooth': 'Dentist',
            'gum': 'Dentist',
            'oral': 'Dentist',
            'mouth': 'Dentist',
            
            # Eye issues
            'eye': 'Eye Specialist',
            'vision': 'Eye Specialist',
            'sight': 'Eye Specialist',
            'retina': 'Eye Specialist',
            'cataract': 'Eye Specialist',
            
            # Ear/Nose/Throat
            'ear': 'ENT',
            'nose': 'ENT',
            'throat': 'ENT',
            'sinus': 'ENT',
            'hearing': 'ENT',
            'tonsils': 'ENT',
            
            # Heart/Cardiovascular
            'heart': 'Cardiologist',
            'chest': 'Cardiologist',
            'cardiac': 'Cardiologist',
            'blood pressure': 'Cardiologist',
            'hypertension': 'Cardiologist',
            'palpitation': 'Cardiologist',
            
            # Brain/Nervous System
            'brain': 'Neurologist',
            'head': 'Neurologist',
            'migraine': 'Neurologist',
            'seizure': 'Neurologist',
            'neural': 'Neurologist',
            'numbness': 'Neurologist',
            
            # Skin
            'skin': 'Dermatologist',
            'rash': 'Dermatologist',
            'acne': 'Dermatologist',
            'eczema': 'Dermatologist',
            'psoriasis': 'Dermatologist',
            'itching': 'Dermatologist',
            
            # Bones/Joints
            'bone': 'Orthopedic',
            'joint': 'Orthopedic',
            'back': 'Orthopedic',
            'spine': 'Orthopedic',
            'fracture': 'Orthopedic',
            'arthritis': 'Orthopedic',
            
            # Mental Health
            'mental': 'Psychiatrist',
            'depression': 'Psychiatrist',
            'anxiety': 'Psychiatrist',
            'stress': 'Psychiatrist',
            'psychological': 'Psychiatrist',
            
            # Women's Health
            'pregnancy': 'Gynecologist',
            'period': 'Gynecologist',
            'menstrual': 'Gynecologist',
            'uterine': 'Gynecologist',
            'ovarian': 'Gynecologist',
            
            # Children
            'child': 'Pediatrician',
            'baby': 'Pediatrician',
            'infant': 'Pediatrician',
            'pediatric': 'Pediatrician',
            
            # Urinary/Kidney
            'urine': 'Urologist',
            'urinary': 'Urologist',
            'kidney': 'Urologist',
            'bladder': 'Urologist',
            'prostate': 'Urologist',
            
            # Cancer
            'cancer': 'Oncologist',
            'tumor': 'Oncologist',
            'chemotherapy': 'Oncologist',
            'radiation': 'Oncologist',
            
            # General/Multiple symptoms
            'fever': 'General Physician',
            'cough': 'General Physician',
            'cold': 'General Physician',
            'stomach': 'General Physician',
            'body': 'General Physician',
            'fatigue': 'General Physician',
            'weakness': 'General Physician'
        }
    
    def analyze_symptoms_for_specialization(self, symptoms: str) -> List[str]:
        """Analyze symptoms and suggest appropriate specializations using AI logic"""
        symptoms_lower = symptoms.lower()
        
        # Count matches for each specialization
        specialization_scores = {}
        
        for keyword, specialization in self.medical_specialization_map.items():
            if keyword in symptoms_lower:
                if specialization not in specialization_scores:
                    specialization_scores[specialization] = 0
                specialization_scores[specialization] += 1
        
        # Sort by score (most relevant first)
        sorted_specializations = sorted(
            specialization_scores.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        # Return top specializations
        if sorted_specializations:
            return [spec for spec, score in sorted_specializations[:3]]
        else:
            # Default to General Physician if no specific matches
            return ['General Physician']
    
    def get_medical_context(self, symptoms: str) -> Dict:
        """Get medical context for symptoms analysis"""
        symptoms_lower = symptoms.lower()
        
        context = {
            'severity': 'mild',
            'urgency': 'low',
            'body_parts': [],
            'symptoms': [],
            'recommendations': []
        }
        
        # Analyze severity indicators
        severe_indicators = ['severe', 'extreme', 'unbearable', 'intense', 'excruciating']
        moderate_indicators = ['moderate', 'medium', 'some', 'quite', 'significant']
        
        for indicator in severe_indicators:
            if indicator in symptoms_lower:
                context['severity'] = 'severe'
                context['urgency'] = 'high'
                break
        else:
            for indicator in moderate_indicators:
                if indicator in symptoms_lower:
                    context['severity'] = 'moderate'
                    context['urgency'] = 'medium'
                    break
        
        # Identify body parts
        body_parts = ['head', 'chest', 'stomach', 'back', 'neck', 'arm', 'leg', 'eye', 'ear', 'nose', 'throat', 'tooth', 'gum', 'skin', 'bone', 'joint']
        for part in body_parts:
            if part in symptoms_lower:
                context['body_parts'].append(part)
        
        # Identify specific symptoms
        specific_symptoms = ['pain', 'ache', 'fever', 'cough', 'cold', 'headache', 'migraine', 'rash', 'swelling', 'bleeding', 'nausea', 'vomiting', 'diarrhea']
        for symptom in specific_symptoms:
            if symptom in symptoms_lower:
                context['symptoms'].append(symptom)
        
        return context
    
    def should_refer_to_specialist(self, symptoms: str) -> bool:
        """Determine if symptoms require specialist consultation"""
        symptoms_lower = symptoms.lower()
        
        # High urgency indicators
        high_urgency = [
            'severe', 'unbearable', 'excruciating', 'intense',
            'bleeding', 'blood', 'vomiting blood', 'chest pain',
            'difficulty breathing', 'shortness of breath',
            'sudden', 'acute', 'emergency'
        ]
        
        for indicator in high_urgency:
            if indicator in symptoms_lower:
                return True
        
        # Chronic indicators
        chronic_indicators = [
            'chronic', 'persistent', 'ongoing', 'weeks', 'months',
            'recurring', 'frequent', 'regular'
        ]
        
        for indicator in chronic_indicators:
            if indicator in symptoms_lower:
                return True
        
        return False

# Global AI doctor analyzer instance
ai_doctor_analyzer = AIDoctorAnalyzer()

def analyze_symptoms_for_doctors(symptoms: str) -> List[str]:
    """Analyze symptoms and suggest doctor specializations"""
    return ai_doctor_analyzer.analyze_symptoms_for_specialization(symptoms)

def get_medical_context(symptoms: str) -> Dict:
    """Get medical context for symptoms"""
    return ai_doctor_analyzer.get_medical_context(symptoms)

def needs_specialist_referral(symptoms: str) -> bool:
    """Check if symptoms require specialist referral"""
    return ai_doctor_analyzer.should_refer_to_specialist(symptoms)
