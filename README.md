# 🤖 AI BASED STORY GENERATOR CHATBOT

An intelligent chatbot that creates personalized stories for children using advanced AI techniques including **Prompt Engineering**, **Fine-tuned LLM**, and **RAG (Retrieval-Augmented Generation)**.

## 🎯 Features

- 🗣️ **Interactive Chat Interface** - Natural conversation flow for story creation
- 🎨 **Personalized Stories** - Custom characters, genres, and age-appropriate content
- 🤖 **Advanced AI Pipeline** - Combines Prompt Engineering + Fine-tuning + RAG
- 🛡️ **Child Safety** - Built-in content filtering and safety measures
- 🚀 **No Database Required** - In-memory session management
- 🌍 **Turkish Language Support** - Optimized for Turkish children's stories

## 🏗️ Architecture

### AI Pipeline
```
User Message → Chat State Machine → RAG Context → Fine-tuned LLM → Safe Story Output
```

### Tech Stack
- **Backend**: FastAPI + PyTorch + Transformers
- **LLM**: Fine-tuned Mistral/DialoGPT model
- **RAG**: ChromaDB + Sentence Transformers
- **Frontend**: Vue.js 3 + Tailwind CSS
- **Memory**: In-memory conversation storage

## 📁 Project Structure

```
childrens-ai-story-chatbot/
├── backend/
│   ├── app/
│   │   ├── api/              # FastAPI endpoints
│   │   ├── services/         # Business logic (Chat, LLM, RAG, Story)
│   │   ├── core/             # Core components (Prompts, State Machine, Config)
│   │   ├── models/           # Data models
│   │   ├── utils/            # Utilities (Validation, Text Processing)
│   │   └── config/           # Configuration
│   ├── data/                 # Datasets and prompts
│   ├── models/               # Trained model files
│   ├── notebooks/            # Jupyter notebooks for experimentation
│   └── scripts/              # Training and data processing scripts
└── frontend/
    └── src/
        ├── components/       # Vue components (Chat Interface, Messages)
        ├── services/         # API communication
        └── stores/           # State management
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- CUDA (optional, for GPU acceleration)

### Backend Setup

1. **Clone and navigate to backend**
   ```bash
   git clone <repository-url>
   cd childrens-ai-story-chatbot/backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configurations
   ```

5. **Download and setup your story dataset**
   ```bash
   # Place your story.csv file in data/ directory
   # The CSV should have a 'text' column with story content
   ```

6. **Initialize RAG system**
   ```bash
   python scripts/build_rag_index.py
   ```

7. **Run the backend**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. **Navigate to frontend**
   ```bash
   cd ../frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Run development server**
   ```bash
   npm run dev
   ```

4. **Open browser**
   ```
   http://localhost:5173
   ```

## 🎮 Usage

### Chat Flow Example

```
👤 User: Merhaba!
🤖 Bot:  Merhaba! Ben hikaye yaratma asistanınım. Nasıl bir hikaye istiyorsun?

👤 User: Kedilerle ilgili bir hikaye
🤖 Bot:  Harika! Kaç yaşındaki çocuklar için olsun?
         [3-5] [6-10] [11-15]

👤 User: 6-10 yaş arası
🤖 Bot:  Mükemmel! Ana karakterin adı ne olsun?

👤 User: Minnoş
🤖 Bot:  Çok güzel isim! Hangi türde bir hikaye istiyorsun?
         [Macera] [Dostluk] [Fantastik] [Eğitici]

👤 User: Macera
🤖 Bot:  Hikayeni hazırlıyorum... ✨

🤖 Bot:  📖 İşte senin için özel hazırladığım hikaye:
         
         # Minnoş'un Büyük Macerası
         
         Bir zamanlar Minnoş adında çok meraklı bir kedi yaşarmış...
         [Full story appears here]
         
         Başka bir hikaye ister misin? 😊
```

## 🔧 Configuration

### Environment Variables (.env)

```bash
# LLM Settings
LLM_MODEL_NAME=microsoft/DialoGPT-medium
EMBEDDING_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2
USE_FINE_TUNED_MODEL=false
FINE_TUNED_MODEL_PATH=./models/fine_tuned/

# RAG Settings
STORY_DATASET_PATH=./data/story.csv
CHROMA_PERSIST_DIRECTORY=./chroma_db
MAX_RAG_RESULTS=5

# API Settings
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true

# Story Generation
MAX_STORY_LENGTH=2000
MIN_STORY_LENGTH=100
MAX_CHARACTERS_PER_STORY=5
```

## 🎯 API Endpoints

### Chat Endpoints
- `POST /api/chat` - Send message to chatbot
- `GET /api/chat/history/{session_id}` - Get conversation history
- `POST /api/chat/reset/{session_id}` - Reset conversation
- `GET /api/chat/suggestions` - Get quick reply suggestions

### Utility Endpoints
- `GET /api/health` - Health check
- `GET /api/parameters` - Get available story parameters
- `GET /api/genres` - Get story genres and descriptions

### Example API Usage

```javascript
// Send message to chatbot
const response = await fetch('/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: "Merhaba!",
    session_id: "user_123",
    user_context: {}
  })
});

const data = await response.json();
console.log(data.response); // Bot's response
```

## 🧠 AI Components

### 1. Prompt Engineering
- **Dynamic prompts** based on conversation context
- **Age-appropriate** language adaptation
- **Genre-specific** storytelling styles
- **Character integration** prompts

### 2. Fine-tuned LLM
- Custom model trained on children's stories
- **Safe content generation**
- **Turkish language optimization**
- Quality-focused training pipeline

### 3. RAG System
- **2M+ story dataset** for context retrieval
- **Semantic search** using sentence transformers
- **Contextual story enhancement**
- Real-time similar story finding

## 🛡️ Safety Features

- **Content filtering** for inappropriate material
- **Child-safe vocabulary** enforcement
- **Violence/horror detection** and prevention
- **Input sanitization** and validation
- **Output quality control**

## 🧪 Development

### Running Tests
```bash
cd backend
python -m pytest tests/
```

### Model Training
```bash
# Prepare fine-tuning data
python scripts/prepare_data.py

# Train the model
python scripts/fine_tune_model.py

# Evaluate model performance
python scripts/evaluate_model.py
```

### Building RAG Index
```bash
# Build ChromaDB index from story dataset
python scripts/build_rag_index.py
```

## 📊 Monitoring

### Chat Analytics
- Conversation success rates
- Average story generation time
- Popular story themes
- User engagement metrics

### Performance Metrics
- Response time monitoring
- Memory usage tracking
- Model inference speed
- RAG retrieval accuracy

## 🚀 Deployment

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d
```

### Production Setup
1. Set `DEBUG=false` in environment
2. Configure proper CORS origins
3. Set up reverse proxy (nginx)
4. Enable monitoring and logging
5. Configure auto-scaling

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Add tests for new features
- Update documentation
- Ensure child safety compliance
- Test with multiple age groups

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Hugging Face** for transformer models
- **ChromaDB** for vector storage
- **FastAPI** for backend framework
- **Vue.js** for frontend framework
- **Turkish AI community** for language support

## 📞 Support

For questions and support:
- Create an [Issue](https://github.com/your-repo/issues)
- Check [Documentation](./docs/)
- Review [Chat Flow Guide](./docs/chat_flow_guide.md)

---

**Made with ❤️ for children's education and imagination** 🌟

## 📈 Roadmap

- [ ] Multi-language support (English, German)
- [ ] Voice chat integration
- [ ] Image generation for stories
- [ ] Mobile app development
- [ ] Teacher dashboard
- [ ] Story sharing platform
- [ ] Advanced analytics
- [ ] Personalization engine

---

*Last updated: December 2024*
