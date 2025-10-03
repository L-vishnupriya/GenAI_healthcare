# 🏥 GenAI Healthcare Multi-Agent System

A sophisticated AI-powered healthcare tracking and meal planning system built with specialized AI agents, real-time data processing, and adaptive decision-making capabilities.

## 🚀 Features

- **6 Specialized AI Agents**: Greeting, Mood Tracker, CGM Monitor, Food Intake, Meal Planner, and Q&A
- **Real-time Health Tracking**: Mood, glucose, and food intake logging
- **Adaptive Meal Planning**: Personalized plans based on medical conditions and glucose levels
- **Interactive Dashboard**: Modern React interface with data visualization
- **AI Chat Interface**: Powered by CopilotKit for natural language interaction

## 🏗️ Architecture

### Backend
- **FastAPI** server with multi-agent orchestration
- **Agno/Phidata** framework for agent management
- **Groq** LLM provider (Llama 3.1 70B)
- **SQLite** database for user data and logs

### Frontend
- **Next.js** React application
- **CopilotKit** for AI chat interface
- **Tailwind CSS** for styling
- **Recharts** for data visualization

## 📋 Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose (optional)
- GROQ API Key (required)

## 🛠️ Setup Instructions

### 1. Environment Configuration

```bash
# Copy environment template
cp env.example .env

# Edit .env file and add your GROQ API key
GROQ_API_KEY=your_groq_api_key_here
```

### 2. Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Generate synthetic data
python data_generator.py

# Start the server
python main.py
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 4. Docker Setup (Alternative)

```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

## 🎯 Usage

1. **Start the system**: Both backend (port 8000) and frontend (port 3000)
2. **Open browser**: Navigate to `http://localhost:3000`
3. **Authenticate**: Enter a User ID (1-100) in the chat interface
4. **Interact**: Use natural language commands:
   - "log my mood"
   - "record glucose reading"
   - "log food intake"
   - "generate meal plan"

## 🤖 AI Agents

### Greeting Agent
- User authentication and validation
- Personalized welcome messages

### Mood Tracker Agent
- Emotional state monitoring
- Trend analysis and insights

### CGM Agent
- Blood glucose monitoring
- Alert system for dangerous readings

### Food Intake Agent
- Meal logging and nutrient analysis
- AI-powered categorization

### Meal Planner Agent
- Adaptive meal planning
- Considers medical conditions and glucose levels

### Interrupt Agent
- General Q&A and conversation handling

## 📊 Database Schema

- **users**: Profile data (name, city, diet, medical conditions)
- **mood_logs**: Emotional state tracking
- **cgm_logs**: Glucose readings with timestamps
- **food_logs**: Meal descriptions and nutrient analysis

## 🔧 Configuration

### Environment Variables

```bash
# Required
GROQ_API_KEY=your_groq_api_key_here

# Optional
OPENAI_API_KEY=your_openai_api_key_here
AGNO_HOST=0.0.0.0
AGNO_PORT=8000
DB_FILE=./backend/data/user_data.db
NEXT_PUBLIC_AGNO_BACKEND_URL=http://localhost:8000
```

### API Endpoints

- `GET /health` - Health check
- `GET /agno` - CopilotKit endpoint
- `POST /agno` - CopilotKit requests

## 🧪 Testing

### Backend Testing
```bash
cd backend
python -m pytest tests/
```

### Frontend Testing
```bash
cd frontend
npm test
```

### End-to-End Testing
1. Start both services
2. Open browser to `http://localhost:3000`
3. Enter User ID 1-100
4. Test all agent functionalities

## 🚨 Troubleshooting

### Common Issues

1. **GROQ API Key Missing**
   - Ensure `.env` file exists with valid GROQ_API_KEY
   - Get API key from: https://console.groq.com/keys

2. **Database Connection Issues**
   - Run `python data_generator.py` to create database
   - Check file permissions for database directory

3. **Frontend Connection Issues**
   - Verify backend is running on port 8000
   - Check CORS configuration in backend

4. **Docker Issues**
   - Ensure Docker and Docker Compose are installed
   - Check port availability (3000, 8000)

### Logs

- **Backend**: Check console output for FastAPI logs
- **Frontend**: Check browser console for React errors
- **Docker**: Use `docker-compose logs [service]`

## 📈 Performance

- **Backend**: Handles 100+ concurrent users
- **Database**: Optimized SQLite with proper indexing
- **Frontend**: Responsive design with lazy loading
- **AI Agents**: Efficient prompt engineering for fast responses

## 🔒 Security

- Environment variables for sensitive data
- CORS configuration for frontend access
- Input validation and sanitization
- SQL injection prevention

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📞 Support

For issues and questions:
- Check the troubleshooting section
- Review logs for error messages
- Ensure all prerequisites are met
- Verify API keys are correctly configured