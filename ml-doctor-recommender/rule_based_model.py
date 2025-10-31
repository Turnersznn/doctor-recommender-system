class RuleBasedSpecialistPredictor:
    def __init__(self, rules):
        self.rules = rules
    
    def predict(self, symptoms):
        """
        Predict specialist based on symptoms.
        symptoms: dict with symptom names (with leading space) as keys and 1/0 as values
        """
        present_symptoms = [symptom for symptom, value in symptoms.items() if value == 1]
        
        if not present_symptoms:
            return 'Internal Medcine'  # Default
        
        # Find the most specific specialist for the present symptoms
        specialist_counts = {}
        for symptom in present_symptoms:
            if symptom in self.rules:
                specialist = self.rules[symptom]
                specialist_counts[specialist] = specialist_counts.get(specialist, 0) + 1
        
        if specialist_counts:
            # Return the specialist with the most matching symptoms
            return max(specialist_counts.items(), key=lambda x: x[1])[0]
        else:
            return 'Internal Medcine'  # Default 