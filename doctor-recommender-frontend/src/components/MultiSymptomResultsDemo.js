import React, { useState } from 'react';
import MultiSymptomResults from './MultiSymptomResults';

const MultiSymptomResultsDemo = () => {
  // Sample data that mimics the multi_symptom_api.py response
  const sampleResult = {
    diagnoses: [
      {
        disease: "Pneumonia",
        probability: 0.8,
        specialist: "Pulmonology",
        alternative_specialists: ["Internal Medicine", "General Practitioner"],
        confidence: 0.85,
        explanation: "Based on your symptoms of cough, fever, and shortness of breath, pneumonia is a likely diagnosis that requires a pulmonologist's expertise.",
        matching_symptoms: ["cough", "fever", "shortness_of_breath"],
        source: "symptom_mapping"
      },
      {
        disease: "Condition requiring Pulmonology consultation",
        probability: 0.75,
        specialist: "Pulmonology",
        alternative_specialists: ["Internal Medicine"],
        confidence: 0.8,
        explanation: "Your respiratory symptoms indicate a condition that should be evaluated by a pulmonologist.",
        source: "ml_model"
      },
      {
        disease: "Common Cold",
        probability: 0.7,
        specialist: "General Practitioner",
        alternative_specialists: ["Internal Medicine"],
        confidence: 0.6,
        explanation: "Your symptoms could indicate a common cold, which can be initially evaluated by a general practitioner.",
        matching_symptoms: ["cough", "fever"],
        source: "symptom_mapping"
      }
    ],
    predicted_specialist: "Pulmonology",
    confidence: 0.85,
    suggested_diseases: ["Pneumonia", "Condition requiring Pulmonology consultation", "Common Cold"],
    active_symptoms: ["cough", "fever", "shortness_of_breath"],
    ml_prediction: "Pulmonology",
    disease_based_specialists: ["Pulmonology", "General Practitioner"]
  };

  // State to hold the result
  const [result, setResult] = useState(sampleResult);

  // Function to simulate fetching new results
  const fetchGastroResults = () => {
    const gastroResult = {
      diagnoses: [
        {
          disease: "Gastroenteritis",
          probability: 0.8,
          specialist: "Gastroenterology",
          alternative_specialists: ["Internal Medicine", "General Practitioner"],
          confidence: 0.85,
          explanation: "Based on your symptoms of abdominal pain, nausea, and vomiting, gastroenteritis is a likely diagnosis that requires a gastroenterologist's expertise.",
          matching_symptoms: ["abdominal_pain", "nausea", "vomiting"],
          source: "symptom_mapping"
        },
        {
          disease: "Condition requiring Gastroenterology consultation",
          probability: 0.75,
          specialist: "Gastroenterology",
          alternative_specialists: ["Internal Medicine"],
          confidence: 0.8,
          explanation: "Your gastrointestinal symptoms indicate a condition that should be evaluated by a gastroenterologist.",
          source: "ml_model"
        }
      ],
      predicted_specialist: "Gastroenterology",
      confidence: 0.85,
      suggested_diseases: ["Gastroenteritis", "Condition requiring Gastroenterology consultation"],
      active_symptoms: ["abdominal_pain", "nausea", "vomiting"],
      ml_prediction: "Gastroenterology",
      disease_based_specialists: ["Gastroenterology", "General Practitioner"]
    };
    setResult(gastroResult);
  };

  const fetchNeuroResults = () => {
    const neuroResult = {
      diagnoses: [
        {
          disease: "Migraine",
          probability: 0.85,
          specialist: "Neurology",
          alternative_specialists: ["Internal Medicine", "General Practitioner"],
          confidence: 0.9,
          explanation: "Based on your symptoms of headache, sensitivity to light, and nausea, migraine is a likely diagnosis that requires a neurologist's expertise.",
          matching_symptoms: ["headache", "sensitivity_to_light", "nausea"],
          source: "symptom_mapping"
        },
        {
          disease: "Condition requiring Neurology consultation",
          probability: 0.8,
          specialist: "Neurology",
          alternative_specialists: ["Internal Medicine"],
          confidence: 0.85,
          explanation: "Your neurological symptoms indicate a condition that should be evaluated by a neurologist.",
          source: "ml_model"
        }
      ],
      predicted_specialist: "Neurology",
      confidence: 0.9,
      suggested_diseases: ["Migraine", "Condition requiring Neurology consultation"],
      active_symptoms: ["headache", "sensitivity_to_light", "nausea"],
      ml_prediction: "Neurology",
      disease_based_specialists: ["Neurology", "General Practitioner"]
    };
    setResult(neuroResult);
  };

  const fetchRespResults = () => {
    setResult(sampleResult);
  };

  return (
    <div className="multi-symptom-demo">
      <div className="demo-controls" style={{ marginBottom: '20px', padding: '20px', background: '#f0f4f8', borderRadius: '8px' }}>
        <h2>Multi-Symptom API Results Demo</h2>
        <p>Click the buttons below to view different sample results:</p>
        <div style={{ display: 'flex', gap: '10px' }}>
          <button 
            onClick={fetchRespResults}
            style={{ padding: '10px 15px', background: '#3B82F6', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}
          >
            Respiratory Symptoms
          </button>
          <button 
            onClick={fetchGastroResults}
            style={{ padding: '10px 15px', background: '#10B981', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}
          >
            Gastrointestinal Symptoms
          </button>
          <button 
            onClick={fetchNeuroResults}
            style={{ padding: '10px 15px', background: '#8B5CF6', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}
          >
            Neurological Symptoms
          </button>
        </div>
      </div>
      
      <MultiSymptomResults result={result} />
    </div>
  );
};

export default MultiSymptomResultsDemo;