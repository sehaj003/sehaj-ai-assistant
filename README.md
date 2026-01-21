# 🤖 Personal AI Assistant Using RAG

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An intelligent assistant that transforms traditional resumes into interactive conversations. Built with LangChain, OpenAI, and Streamlit to enable natural language queries about professional background, skills, and experience.

## Features

- **Natural Language Queries**: Ask questions in plain English about education, experience, and skills
- **Intelligent Retrieval**: RAG (Retrieval-Augmented Generation) architecture for accurate, context-aware responses
- **Source Attribution**: Transparent sourcing shows which profile sections inform each answer
- **Real-time Processing**: Sub-3-second response times with OpenAI integration

## Architecture

```
User Query → Streamlit UI → LangChain → ChromaDB → OpenAI GPT → Response
     ↓           ↓            ↓          ↓         ↓          ↓
 Natural      Interface   Orchestration Vector   Language   Contextual
 Language                              Search    Model      Answer
```

**Tech Stack**: Streamlit • LangChain • OpenAI • ChromaDB • Python

## Project Structure

```
My-AI-Assistant/
├── main.py                    # Main Streamlit application
├── data/
│   └── sehaj_profile.yaml     # Structured profile data
├── requirements.txt           # Dependencies
├── .env                       # Environment variables
├── .env.example              # Environment template
└── README.md                 # Documentation
```

## Quick Start

1. **Clone and setup**
   ```bash
   git clone https://github.com/yourusername/personal-ai-assistant.git
   cd personal-ai-assistant
   python -m venv ai_assistant_env
   source ai_assistant_env/bin/activate  # Windows: ai_assistant_env\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env: OPENAI_API_KEY=your_key_here
   ```

4. **Run application**
   ```bash
   streamlit run main.py
   ```

## Usage Examples

**Educational Background**
```
Q: "What's Sehaj's educational background?"
A: "Sehaj is pursuing a Master's in Data Analytics Engineering at Northeastern University (May 2025) and holds a Bachelor's in Computer Science Engineering from GGSIPU (June 2023)."
```

**Technical Skills**
```
Q: "What programming languages does he know?"
A: "Sehaj is proficient in Python, SQL, and data visualization tools including Power BI and Tableau."
```

## Data Structure

Profile data is stored in YAML format:

```yaml
name: Sehaj Malhotra
education:
  - degree: Master's in Data Analytics Engineering
    university: Northeastern University
    graduation: May 2025
skills:
  - Python
  - SQL
  - Power BI
  - Tableau
experience:
  - role: Data Analyst Intern
    company: DataTouch Solutions
    description: Developed ETL pipelines and automated data cleaning
```

## Deployment

### Streamlit Cloud (Recommended)
1. Push code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect repository and add `OPENAI_API_KEY` in secrets
4. Deploy with one click

### Local Development
```bash
streamlit run main.py  # Access at http://localhost:8501
```

## Configuration

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API authentication | Yes |
| `OPENAI_MODEL` | GPT model (default: gpt-3.5-turbo) | No |
| `TEMPERATURE` | Response creativity 0-1 (default: 0.3) | No |

## Dependencies

```
streamlit>=1.28.0      # Web framework
langchain>=0.0.350     # LLM orchestration
openai>=1.3.5          # GPT integration
chromadb>=0.4.18       # Vector database
pyyaml>=6.0.1          # YAML parsing
python-dotenv>=1.0.0   # Environment management
```

## Customization

To adapt for your own profile:

1. **Update profile data**: Edit `data/sehaj_profile.yaml` with your information
2. **Modify branding**: Change app title and description in `main.py`
3. **Adjust parameters**: Update chunk size, temperature, or model in configuration

## Performance

- **Response Time**: <3 seconds average
- **Scalability**: Stateless design supports concurrent users
- **Cost Optimization**: Caching and token limits minimize API usage

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Open Pull Request

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contact

**Sehaj Malhotra**
- **Live Demo**: [Try the AI Assistant](https://your-app-url.streamlit.app)
- **LinkedIn**: [sehajmalhotra](https://linkedin.com/in/sehajmalhotra)
- **GitHub**: [@sehajmalhotra](http://github.com/sehaj003)
- **Email**: malhotra.se@northeastern.edu
- **Email**: sehaj.malhotra37@gmail.com

---

*Built with Python, Streamlit, LangChain, and OpenAI*
