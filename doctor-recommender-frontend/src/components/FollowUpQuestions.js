import React, { useState, useEffect } from 'react';
import './FollowUpQuestions.css';

const FollowUpQuestions = ({ selectedSymptoms, onAnswersChange, onComplete }) => {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [questions, setQuestions] = useState([]);
  const [isComplete, setIsComplete] = useState(false);

  // Question database based on symptoms
  const questionDatabase = {
    'chest_pain': [
      {
        id: 'chest_pain_type',
        question: 'How would you describe your chest pain?',
        type: 'multiple_choice',
        options: [
          { value: 'sharp', label: 'Sharp, stabbing pain' },
          { value: 'crushing', label: 'Crushing, pressure-like pain' },
          { value: 'burning', label: 'Burning sensation' },
          { value: 'dull', label: 'Dull, aching pain' }
        ],
        importance: 'high'
      },
      {
        id: 'chest_pain_duration',
        question: 'How long does the chest pain last?',
        type: 'multiple_choice',
        options: [
          { value: 'seconds', label: 'A few seconds' },
          { value: 'minutes', label: 'Several minutes' },
          { value: 'hours', label: 'Hours at a time' },
          { value: 'constant', label: 'Constant pain' }
        ],
        importance: 'high'
      },
      {
        id: 'chest_pain_triggers',
        question: 'What triggers or worsens your chest pain?',
        type: 'multiple_select',
        options: [
          { value: 'exercise', label: 'Physical activity or exercise' },
          { value: 'stress', label: 'Emotional stress' },
          { value: 'eating', label: 'Eating or drinking' },
          { value: 'breathing', label: 'Deep breathing or coughing' },
          { value: 'position', label: 'Certain positions' },
          { value: 'nothing', label: 'Nothing specific' }
        ],
        importance: 'medium'
      }
    ],
    'headache': [
      {
        id: 'headache_location',
        question: 'Where is your headache located?',
        type: 'multiple_choice',
        options: [
          { value: 'forehead', label: 'Forehead area' },
          { value: 'temples', label: 'Temples (sides of head)' },
          { value: 'back_head', label: 'Back of head/neck' },
          { value: 'one_side', label: 'One side of head' },
          { value: 'all_over', label: 'All over head' }
        ],
        importance: 'high'
      },
      {
        id: 'headache_intensity',
        question: 'How would you rate your headache intensity?',
        type: 'scale',
        min: 1,
        max: 10,
        labels: { 1: 'Mild', 5: 'Moderate', 10: 'Severe' },
        importance: 'medium'
      },
      {
        id: 'headache_frequency',
        question: 'How often do you get these headaches?',
        type: 'multiple_choice',
        options: [
          { value: 'first_time', label: 'This is my first time' },
          { value: 'rarely', label: 'Rarely (less than once a month)' },
          { value: 'monthly', label: 'Monthly' },
          { value: 'weekly', label: 'Weekly' },
          { value: 'daily', label: 'Daily or almost daily' }
        ],
        importance: 'medium'
      }
    ],
    'abdominal_pain': [
      {
        id: 'abdominal_location',
        question: 'Where exactly is your abdominal pain?',
        type: 'multiple_choice',
        options: [
          { value: 'upper_right', label: 'Upper right abdomen' },
          { value: 'upper_left', label: 'Upper left abdomen' },
          { value: 'lower_right', label: 'Lower right abdomen' },
          { value: 'lower_left', label: 'Lower left abdomen' },
          { value: 'center', label: 'Center of abdomen' },
          { value: 'all_over', label: 'All over abdomen' }
        ],
        importance: 'high'
      },
      {
        id: 'abdominal_relation_to_eating',
        question: 'How does eating affect your abdominal pain?',
        type: 'multiple_choice',
        options: [
          { value: 'worse_after', label: 'Gets worse after eating' },
          { value: 'better_after', label: 'Gets better after eating' },
          { value: 'worse_before', label: 'Gets worse when hungry' },
          { value: 'no_relation', label: 'No relation to eating' }
        ],
        importance: 'medium'
      }
    ],
    'cough': [
      {
        id: 'cough_type',
        question: 'What type of cough do you have?',
        type: 'multiple_choice',
        options: [
          { value: 'dry', label: 'Dry cough (no mucus)' },
          { value: 'productive', label: 'Productive cough (with mucus)' },
          { value: 'barking', label: 'Barking or harsh cough' }
        ],
        importance: 'high'
      },
      {
        id: 'cough_duration',
        question: 'How long have you had this cough?',
        type: 'multiple_choice',
        options: [
          { value: 'few_days', label: 'A few days' },
          { value: 'week', label: 'About a week' },
          { value: 'weeks', label: 'Several weeks' },
          { value: 'months', label: 'Months' }
        ],
        importance: 'medium'
      }
    ],
    'fever': [
      {
        id: 'fever_temperature',
        question: 'What is your temperature (if measured)?',
        type: 'multiple_choice',
        options: [
          { value: 'low_grade', label: '99-100.4°F (37.2-38°C)' },
          { value: 'moderate', label: '100.5-102°F (38.1-38.9°C)' },
          { value: 'high', label: '102.1-104°F (38.9-40°C)' },
          { value: 'very_high', label: 'Above 104°F (40°C)' },
          { value: 'not_measured', label: 'Haven\'t measured' }
        ],
        importance: 'high'
      },
      {
        id: 'fever_pattern',
        question: 'How does your fever behave?',
        type: 'multiple_choice',
        options: [
          { value: 'constant', label: 'Constant fever' },
          { value: 'comes_goes', label: 'Comes and goes' },
          { value: 'worse_evening', label: 'Worse in the evening' },
          { value: 'worse_morning', label: 'Worse in the morning' }
        ],
        importance: 'medium'
      }
    ],
    'joint_pain': [
      {
        id: 'joint_location',
        question: 'Which joints are affected?',
        type: 'multiple_select',
        options: [
          { value: 'hands', label: 'Hands/fingers' },
          { value: 'wrists', label: 'Wrists' },
          { value: 'elbows', label: 'Elbows' },
          { value: 'shoulders', label: 'Shoulders' },
          { value: 'knees', label: 'Knees' },
          { value: 'ankles', label: 'Ankles' },
          { value: 'hips', label: 'Hips' },
          { value: 'spine', label: 'Spine/back' }
        ],
        importance: 'high'
      },
      {
        id: 'joint_stiffness',
        question: 'When is the joint stiffness worst?',
        type: 'multiple_choice',
        options: [
          { value: 'morning', label: 'In the morning' },
          { value: 'evening', label: 'In the evening' },
          { value: 'after_rest', label: 'After periods of rest' },
          { value: 'after_activity', label: 'After activity' },
          { value: 'constant', label: 'Constant stiffness' }
        ],
        importance: 'medium'
      }
    ]
  };

  // Generate questions based on selected symptoms
  useEffect(() => {
    const generatedQuestions = [];
    const symptomKeys = Object.keys(selectedSymptoms);
    
    // Add general questions first
    generatedQuestions.push({
      id: 'symptom_duration',
      question: 'How long have you been experiencing these symptoms?',
      type: 'multiple_choice',
      options: [
        { value: 'hours', label: 'A few hours' },
        { value: 'days', label: 'A few days' },
        { value: 'weeks', label: 'A few weeks' },
        { value: 'months', label: 'Several months' },
        { value: 'years', label: 'Years' }
      ],
      importance: 'high'
    });

    // Add symptom-specific questions
    symptomKeys.forEach(symptom => {
      if (questionDatabase[symptom]) {
        generatedQuestions.push(...questionDatabase[symptom]);
      }
    });

    // Add general health questions
    if (symptomKeys.length > 2) {
      generatedQuestions.push({
        id: 'symptom_onset',
        question: 'Did your symptoms start suddenly or gradually?',
        type: 'multiple_choice',
        options: [
          { value: 'sudden', label: 'Suddenly (within hours)' },
          { value: 'gradual', label: 'Gradually (over days/weeks)' },
          { value: 'unsure', label: 'Not sure' }
        ],
        importance: 'medium'
      });
    }

    // Limit to most important questions (max 5)
    const prioritizedQuestions = generatedQuestions
      .sort((a, b) => {
        const importanceOrder = { 'high': 3, 'medium': 2, 'low': 1 };
        return importanceOrder[b.importance] - importanceOrder[a.importance];
      })
      .slice(0, 5);

    setQuestions(prioritizedQuestions);
  }, [selectedSymptoms]);

  const handleAnswer = (questionId, answer) => {
    const newAnswers = { ...answers, [questionId]: answer };
    setAnswers(newAnswers);
    onAnswersChange(newAnswers);
  };

  const handleNext = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    } else {
      setIsComplete(true);
      onComplete(answers);
    }
  };

  const handlePrevious = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1);
    }
  };

  const handleSkip = () => {
    handleNext();
  };

  if (questions.length === 0) {
    return null;
  }

  if (isComplete) {
    return (
      <div className="follow-up-complete">
        <div className="complete-icon">✅</div>
        <h3>Follow-up Questions Complete</h3>
        <p>Thank you for providing additional information. This will help improve the accuracy of your recommendations.</p>
      </div>
    );
  }

  const currentQuestion = questions[currentQuestionIndex];
  const progress = ((currentQuestionIndex + 1) / questions.length) * 100;

  return (
    <div className="follow-up-questions">
      <div className="questions-header">
        <h3>Follow-up Questions</h3>
        <p>Help us provide more accurate recommendations by answering a few additional questions.</p>
        
        <div className="progress-container">
          <div className="progress-bar">
            <div 
              className="progress-fill" 
              style={{ width: `${progress}%` }}
            />
          </div>
          <span className="progress-text">
            {currentQuestionIndex + 1} of {questions.length}
          </span>
        </div>
      </div>

      <div className="question-container">
        <div className="question-header">
          <h4>{currentQuestion.question}</h4>
          {currentQuestion.importance === 'high' && (
            <span className="importance-badge high">Important</span>
          )}
        </div>

        <div className="answer-options">
          {currentQuestion.type === 'multiple_choice' && (
            <div className="radio-options">
              {currentQuestion.options.map(option => (
                <label key={option.value} className="radio-option">
                  <input
                    type="radio"
                    name={currentQuestion.id}
                    value={option.value}
                    checked={answers[currentQuestion.id] === option.value}
                    onChange={(e) => handleAnswer(currentQuestion.id, e.target.value)}
                  />
                  <span className="radio-label">{option.label}</span>
                </label>
              ))}
            </div>
          )}

          {currentQuestion.type === 'multiple_select' && (
            <div className="checkbox-options">
              {currentQuestion.options.map(option => (
                <label key={option.value} className="checkbox-option">
                  <input
                    type="checkbox"
                    value={option.value}
                    checked={(answers[currentQuestion.id] || []).includes(option.value)}
                    onChange={(e) => {
                      const currentAnswers = answers[currentQuestion.id] || [];
                      const newAnswers = e.target.checked
                        ? [...currentAnswers, option.value]
                        : currentAnswers.filter(a => a !== option.value);
                      handleAnswer(currentQuestion.id, newAnswers);
                    }}
                  />
                  <span className="checkbox-label">{option.label}</span>
                </label>
              ))}
            </div>
          )}

          {currentQuestion.type === 'scale' && (
            <div className="scale-option">
              <div className="scale-labels">
                <span>{currentQuestion.labels[currentQuestion.min]}</span>
                <span>{currentQuestion.labels[Math.floor((currentQuestion.min + currentQuestion.max) / 2)]}</span>
                <span>{currentQuestion.labels[currentQuestion.max]}</span>
              </div>
              <input
                type="range"
                min={currentQuestion.min}
                max={currentQuestion.max}
                value={answers[currentQuestion.id] || currentQuestion.min}
                onChange={(e) => handleAnswer(currentQuestion.id, parseInt(e.target.value))}
                className="scale-slider"
              />
              <div className="scale-value">
                {answers[currentQuestion.id] || currentQuestion.min}
              </div>
            </div>
          )}
        </div>

        <div className="question-actions">
          <button 
            className="btn-secondary" 
            onClick={handlePrevious}
            disabled={currentQuestionIndex === 0}
          >
            Previous
          </button>
          
          <button 
            className="btn-skip" 
            onClick={handleSkip}
          >
            Skip
          </button>
          
          <button 
            className="btn-primary" 
            onClick={handleNext}
            disabled={!answers[currentQuestion.id]}
          >
            {currentQuestionIndex === questions.length - 1 ? 'Complete' : 'Next'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default FollowUpQuestions;
