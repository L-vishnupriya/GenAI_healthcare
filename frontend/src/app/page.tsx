"use client";
import React, { useState, useMemo, useEffect } from 'react';
import { CopilotChat } from '@copilotkit/react-ui';
import { useCopilotAction } from '@copilotkit/react-core';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, BarChart, Bar } from 'recharts';
import { BarChart as BarIcon, Heart, BookOpen, Clock } from 'lucide-react';

// --- Placeholder Data & Types ---
interface LogData {
  timestamp: string;
  value: number;
}
interface MoodCount {
  name: string;
  count: number;
}
type Meal = {
  meal: string;
  description: string;
  macros: string;
};

// Mock data (In a real AG-UI app, this would be populated by events from the backend agent)
const mockData = {
  cgm: [{ timestamp: "Day 1", value: 120 }, { timestamp: "Day 7", value: 135 }],
  mood: [{ name: 'Happy', count: 3 }, { name: 'Tired', count: 2 }],
  mealPlan: [] as Meal[],
  userName: "User"
};

// --- Custom Components for Generative UI ---

const CgmChart: React.FC<{ data: LogData[] }> = ({ data }) => (
  <div className="p-4 border rounded-lg shadow-md bg-white">
    <h3 className="text-lg font-semibold mb-2 flex items-center"><Heart className="w-5 h-5 mr-2 text-red-500" /> CGM History</h3>
    <LineChart width={400} height={200} data={data} margin={{ top: 5, right: 20, left: 10, bottom: 5 }}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="timestamp" />
      <YAxis domain={[50, 350]} />
      <Tooltip />
      <Line type="monotone" dataKey="value" stroke="#8884d8" name="Glucose (mg/dL)" />
    </LineChart>
  </div>
);

const MoodChart: React.FC<{ data: MoodCount[] }> = ({ data }) => (
  <div className="p-4 border rounded-lg shadow-md bg-white">
      <h3 className="text-lg font-semibold mb-2 flex items-center"><BarIcon className="w-5 h-5 mr-2 text-yellow-600" /> Mood Trend</h3>
      <BarChart width={300} height={200} data={data}>
          <XAxis dataKey="name" />
          <YAxis allowDecimals={false} />
          <Tooltip />
          <Bar dataKey="count" fill="#82ca9d" />
      </BarChart>
  </div>
);

const MealPlanCard: React.FC<{ plan: Meal[] }> = ({ plan }) => (
  <div className="p-6 border-2 border-indigo-500 rounded-lg shadow-lg bg-indigo-50 space-y-4">
    <h2 className="text-2xl font-bold text-indigo-700 flex items-center">
      <BookOpen className="w-6 h-6 mr-2" /> Adaptive Meal Plan
    </h2>
    {plan.length > 0 ? (
      plan.map((item, index) => (
        <div key={index} className="border-b pb-2 last:border-b-0">
          <h4 className="font-semibold text-lg">{item.meal}</h4>
          <p className="text-sm text-gray-700">{item.description}</p>
          <p className="text-xs text-indigo-600 font-medium mt-1">Macros Focus: {item.macros}</p>
        </div>
      ))
    ) : (
      <p>Ask the Meal Planner Agent to generate a plan based on your latest logs!</p>
    )}
  </div>
);

// --- Main Application Component ---

export default function Home() {
  const [userName, setUserName] = useState(mockData.userName);
  const [cgmData, setCgmData] = useState(mockData.cgm);
  const [moodData, setMoodData] = useState(mockData.mood);
  const [mealPlan, setMealPlan] = useState(mockData.mealPlan);

  // 1. Frontend Tool (Action): Log Food Intake
  useCopilotAction({
    name: "logUserFood",
    description: "Logs the user's food intake when they submit the form. This triggers the Food Intake Agent.",
    parameters: [
      { name: "mealDescription", type: "string", description: "The free-text description of the meal/snack." }
    ],
    handler: async ({ mealDescription }) => {
      // Send the meal description as a user message to the Food Intake Agent
      const message = `Log Meal: ${mealDescription}.`;
      
      // In a CopilotKit/AG-UI setup, sending a message can trigger the Food Intake Agent based on a prompt/intent.
      // This is simulated by using a chat function.
      alert(`Simulated: Meal "${mealDescription}" submitted for logging and nutrient categorization.`);
    }
  });

  // 2. Frontend Tool (Action): Request Meal Plan
  useCopilotAction({
    name: "requestMealPlan",
    description: "Requests the Meal Planner Agent to generate a new adaptive plan.",
    parameters: [],
    handler: async () => {
      // Simulate sending a direct command to the Meal Planner Agent
      alert("Simulated: Requesting new Adaptive Meal Plan from the Meal Planner Agent.");
    }
  });

  // 3. Frontend Tool (Action): Log CGM Reading
  useCopilotAction({
    name: "logCgmReading",
    description: "Logs a new CGM reading for the CGM Agent to process.",
    parameters: [
      { name: "reading", type: "number", description: "The current glucose reading in mg/dL." }
    ],
    handler: async ({ reading }) => {
      alert(`Simulated: CGM reading of ${reading} mg/dL submitted for logging.`);
    }
  });


  // --- Helper Components ---
  const DataLogForm: React.FC = () => {
    const [meal, setMeal] = useState('');
    const [cgm, setCgm] = useState<number | ''>('');
    
    const handleMealSubmit = async (e: React.FormEvent) => {
      e.preventDefault();
      if (meal.trim()) {
        alert(`Simulated: Meal "${meal}" submitted for logging and nutrient categorization.`);
        setMeal('');
      }
    };

    const handleCgmSubmit = async (e: React.FormEvent) => {
      e.preventDefault();
      if (cgm !== '') {
        alert(`Simulated: CGM reading of ${cgm} mg/dL submitted for logging.`);
        setCgm('');
      }
    };

    const handleMealPlanRequest = async () => {
      alert("Simulated: Requesting new Adaptive Meal Plan from the Meal Planner Agent.");
    };
    
    return (
      <div className="bg-white p-6 rounded-lg shadow-xl space-y-6">
        <h2 className="text-xl font-bold border-b pb-2 text-gray-700">Data Logging Forms</h2>
        
        {/* Food Intake Form */}
        <form onSubmit={handleMealSubmit} className="border p-4 rounded-md space-y-3">
          <h3 className="font-semibold flex items-center"><Clock className="w-4 h-4 mr-2" /> Log Food Intake</h3>
          <textarea
            value={meal}
            onChange={(e) => setMeal(e.target.value)}
            placeholder="e.g., 'Chicken salad with olive oil dressing and a small apple'"
            className="w-full p-2 border rounded resize-none"
            rows={2}
            required
          />
          <button type="submit" className="w-full px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">
            Log Meal & Categorize Nutrients
          </button>
        </form>

        {/* CGM Logging Form */}
        <form onSubmit={handleCgmSubmit} className="border p-4 rounded-md space-y-3">
          <h3 className="font-semibold flex items-center"><Heart className="w-4 h-4 mr-2" /> Log CGM Reading</h3>
          <input
            type="number"
            value={cgm}
            onChange={(e) => setCgm(Number(e.target.value))}
            placeholder="Glucose Reading (mg/dL)"
            className="w-full p-2 border rounded"
            required
          />
          <button type="submit" className="w-full px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
            Log Reading
          </button>
        </form>

        {/* Meal Plan Request */}
        <button 
          onClick={handleMealPlanRequest}
          className="w-full px-4 py-3 text-lg font-bold bg-indigo-600 text-white rounded hover:bg-indigo-700 shadow-md transition-colors"
        >
          Generate Adaptive Meal Plan 🍽️
        </button>
      </div>
    );
  };

  return (
    <div className="flex h-screen bg-gray-50">
      
      {/* DASHBOARD SECTION (2/3 width) */}
      <div className="w-2/3 p-8 space-y-8 overflow-y-auto">
        <h1 className="text-4xl font-extrabold text-gray-900 border-b pb-2">
          Hello, {userName}! Personalized Health Demo
        </h1>
        
        {/* CHART & FORM GRID */}
        <div className="grid grid-cols-2 gap-8">
          <div className="col-span-1 space-y-8">
            <CgmChart data={cgmData} />
            <MoodChart data={moodData} />
          </div>
          <div className="col-span-1">
            <DataLogForm />
          </div>
        </div>
        
        {/* MEAL PLAN SECTION (Generative UI Output) */}
        <MealPlanCard plan={mealPlan} />
      </div>

      {/* CHAT INTERFACE SECTION (1/3 width) */}
      <div className="w-1/3 border-l bg-white flex flex-col h-full">
        <div className="p-4 text-center border-b bg-gray-100">
          <h2 className="text-lg font-bold">Health Assistant Chat</h2>
          <p className="text-sm text-gray-500">Enter User ID (1-100) to start.</p>
        </div>
        <CopilotChat 
          className="flex-1"
          // This component handles the AG-UI protocol communication with the Agno backend
        />
      </div>
    </div>
  );
}