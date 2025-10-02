"use client";

import React, { useState, useEffect } from 'react';
import { CopilotKit } from '@copilotkit/react-core';
import { CopilotChat } from '@copilotkit/react-ui';
import '@copilotkit/react-ui/styles.css';
import { 
  LineChart, Line, BarChart, Bar, XAxis, YAxis, 
  CartesianGrid, Tooltip, Legend, ResponsiveContainer 
} from 'recharts';
import { 
  User, Activity, Apple, Brain, Calendar, 
  TrendingUp, AlertCircle, Send, Loader2 
} from 'lucide-react';

// Types
interface UserProfile {
  id: number;
  name: string;
  city: string;
  diet: string;
  conditions: string;
  limitations: string;
}

interface ChartData {
  day?: string;
  glucose?: number;
  target?: number;
  mood?: string;
  count?: number;
}

export default function HealthcareDashboard() {
  const [currentUser, setCurrentUser] = useState<UserProfile | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  
  const BACKEND_URL = process.env.NEXT_PUBLIC_AGNO_BACKEND_URL || "http://localhost:8000";

  // Mock data for visualization (in production, this would come from the backend)
  const cgmData: ChartData[] = [
    { day: 'Mon', glucose: 120, target: 100 },
    { day: 'Tue', glucose: 155, target: 100 },
    { day: 'Wed', glucose: 280, target: 100 },
    { day: 'Thu', glucose: 105, target: 100 },
    { day: 'Fri', glucose: 90, target: 100 },
    { day: 'Sat', glucose: 110, target: 100 },
    { day: 'Sun', glucose: 135, target: 100 }
  ];

  const moodData: ChartData[] = [
    { mood: 'Happy', count: 3 },
    { mood: 'Tired', count: 2 },
    { mood: 'Sad', count: 1 },
    { mood: 'Excited', count: 1 }
  ];

  useEffect(() => {
    // Simulate loading
    setTimeout(() => setIsLoading(false), 1000);
  }, []);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen bg-gradient-to-br from-blue-50 to-indigo-50">
        <div className="text-center">
          <Loader2 className="w-12 h-12 animate-spin text-indigo-600 mx-auto mb-4" />
          <p className="text-gray-600">Loading Healthcare System...</p>
        </div>
      </div>
    );
  }

  return (
    <CopilotKit runtimeUrl={`${BACKEND_URL}/agno`}>
      <div className="flex h-screen bg-gradient-to-br from-blue-50 to-indigo-50">
        
        {/* Main Dashboard - Left Side */}
        <div className="flex-1 overflow-y-auto p-6">
          <div className="max-w-7xl mx-auto space-y-6">
            
            {/* Header */}
            <div className="bg-white rounded-xl shadow-lg p-6 border-l-4 border-indigo-600">
              <div className="flex items-center justify-between">
                <div>
                  <h1 className="text-3xl font-bold text-gray-800 mb-2">
                    🏥 Healthcare Multi-Agent System
                  </h1>
                  <p className="text-gray-600">
                    AI-powered personalized health tracking and meal planning
                  </p>
                </div>
                {currentUser && (
                  <div className="bg-indigo-50 rounded-lg p-4 text-right">
                    <div className="flex items-center gap-2 text-indigo-700 font-semibold">
                      <User size={20} />
                      {currentUser.name}
                    </div>
                    <div className="text-sm text-gray-600 mt-1">
                      ID: {currentUser.id} | {currentUser.city}
                    </div>
                    <div className="text-xs text-gray-500 mt-1">
                      {currentUser.diet} • {currentUser.conditions}
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Instructions Card */}
            <div className="bg-gradient-to-r from-indigo-500 to-purple-600 text-white rounded-xl shadow-lg p-6">
              <h2 className="text-xl font-bold mb-3 flex items-center gap-2">
                <AlertCircle size={24} />
                Getting Started
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div>
                  <p className="font-semibold mb-2">📝 Step 1: Authenticate</p>
                  <p className="text-indigo-100">Enter your User ID (1-100) in the chat to begin</p>
                </div>
                <div>
                  <p className="font-semibold mb-2">🎯 Available Actions</p>
                  <ul className="text-indigo-100 space-y-1">
                    <li>• Log your mood</li>
                    <li>• Record CGM readings</li>
                    <li>• Track food intake</li>
                    <li>• Generate meal plans</li>
                  </ul>
                </div>
              </div>
            </div>

            {/* Charts Row */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              
              {/* CGM Chart */}
              <div className="bg-white rounded-xl shadow-lg p-6">
                <div className="flex items-center gap-2 mb-4">
                  <Activity className="text-red-500" size={24} />
                  <h2 className="text-xl font-bold text-gray-800">
                    CGM History (Past Week)
                  </h2>
                </div>
                <ResponsiveContainer width="100%" height={280}>
                  <LineChart data={cgmData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
                    <XAxis 
                      dataKey="day" 
                      stroke="#666"
                      style={{ fontSize: '12px' }}
                    />
                    <YAxis 
                      domain={[50, 350]} 
                      stroke="#666"
                      style={{ fontSize: '12px' }}
                    />
                    <Tooltip 
                      contentStyle={{ 
                        background: '#fff', 
                        border: '1px solid #ccc', 
                        borderRadius: '8px',
                        fontSize: '12px'
                      }}
                    />
                    <Legend wrapperStyle={{ fontSize: '12px' }} />
                    <Line 
                      type="monotone" 
                      dataKey="glucose" 
                      stroke="#ef4444" 
                      strokeWidth={3}
                      name="Glucose (mg/dL)" 
                      dot={{ r: 5 }}
                      activeDot={{ r: 7 }}
                    />
                    <Line 
                      type="monotone" 
                      dataKey="target" 
                      stroke="#10b981" 
                      strokeWidth={2}
                      strokeDasharray="5 5" 
                      name="Target"
                      dot={false}
                    />
                  </LineChart>
                </ResponsiveContainer>
                <div className="mt-4 bg-red-50 border-l-4 border-red-500 p-3 rounded">
                  <div className="flex items-center gap-2 text-red-700 text-sm">
                    <AlertCircle size={16} />
                    <span className="font-semibold">
                      Alert: Wednesday spike detected (280 mg/dL)
                    </span>
                  </div>
                </div>
              </div>

              {/* Mood Chart */}
              <div className="bg-white rounded-xl shadow-lg p-6">
                <div className="flex items-center gap-2 mb-4">
                  <Brain className="text-purple-500" size={24} />
                  <h2 className="text-xl font-bold text-gray-800">
                    Mood Trend (Last Week)
                  </h2>
                </div>
                <ResponsiveContainer width="100%" height={280}>
                  <BarChart data={moodData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
                    <XAxis 
                      dataKey="mood" 
                      stroke="#666"
                      style={{ fontSize: '12px' }}
                    />
                    <YAxis 
                      allowDecimals={false} 
                      stroke="#666"
                      style={{ fontSize: '12px' }}
                    />
                    <Tooltip 
                      contentStyle={{ 
                        background: '#fff', 
                        border: '1px solid #ccc', 
                        borderRadius: '8px',
                        fontSize: '12px'
                      }}
                    />
                    <Bar 
                      dataKey="count" 
                      fill="#8b5cf6" 
                      radius={[8, 8, 0, 0]}
                      name="Frequency"
                    />
                  </BarChart>
                </ResponsiveContainer>
                <div className="mt-4 bg-purple-50 border-l-4 border-purple-500 p-3 rounded">
                  <div className="flex items-center gap-2 text-purple-700 text-sm">
                    <TrendingUp size={16} />
                    <span className="font-semibold">
                      Overall positive mood trend 😊
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Food Intake Section */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <div className="flex items-center gap-2 mb-4">
                <Apple className="text-green-500" size={24} />
                <h2 className="text-xl font-bold text-gray-800">
                  Recent Food Logs
                </h2>
              </div>
              <div className="space-y-3">
                <div className="bg-gray-50 rounded-lg p-4 border-l-4 border-green-500">
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="font-semibold text-gray-800">
                        Oatmeal with berries and coffee
                      </div>
                      <div className="text-sm text-gray-600 mt-1">
                        Carbs: 45g, Protein: 8g, Fat: 5g
                      </div>
                    </div>
                    <div className="text-sm text-gray-500">8:00 AM</div>
                  </div>
                </div>
                <div className="bg-gray-50 rounded-lg p-4 border-l-4 border-green-500">
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="font-semibold text-gray-800">
                        Grilled chicken salad with quinoa
                      </div>
                      <div className="text-sm text-gray-600 mt-1">
                        Carbs: 32g, Protein: 35g, Fat: 15g
                      </div>
                    </div>
                    <div className="text-sm text-gray-500">1:00 PM</div>
                  </div>
                </div>
              </div>
              <div className="mt-4 text-center">
                <p className="text-sm text-gray-600">
                  💬 Use the chat to log new meals and get instant nutrient analysis
                </p>
              </div>
            </div>

            {/* Features Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-white rounded-lg shadow p-6 border-t-4 border-blue-500">
                <h3 className="font-bold text-gray-800 mb-2 flex items-center gap-2">
                  <User size={20} className="text-blue-500" />
                  6 AI Agents
                </h3>
                <p className="text-sm text-gray-600">
                  Specialized agents for greeting, mood, CGM, food, meals, and Q&A
                </p>
              </div>
              <div className="bg-white rounded-lg shadow p-6 border-t-4 border-green-500">
                <h3 className="font-bold text-gray-800 mb-2 flex items-center gap-2">
                  <TrendingUp size={20} className="text-green-500" />
                  Adaptive Planning
                </h3>
                <p className="text-sm text-gray-600">
                  Meal plans adjust based on CGM, mood, diet, and medical conditions
                </p>
              </div>
              <div className="bg-white rounded-lg shadow p-6 border-t-4 border-purple-500">
                <h3 className="font-bold text-gray-800 mb-2 flex items-center gap-2">
                  <Calendar size={20} className="text-purple-500" />
                  Real-time Tracking
                </h3>
                <p className="text-sm text-gray-600">
                  Log mood, glucose, and food intake with instant AI analysis
                </p>
              </div>
            </div>

          </div>
        </div>

        {/* Chat Interface - Right Side */}
        <div className="w-96 bg-white border-l shadow-2xl flex flex-col">
          <CopilotChat
            className="h-full"
            instructions="You are a helpful healthcare assistant. Help users with their health tracking needs."
            labels={{
              title: "Healthcare AI Assistant",
              initial: "Hello! Please enter your User ID (1-100) to get started. 👋",
            }}
          />
        </div>
      </div>
    </CopilotKit>
  );
}