# 🦚 Krishna AI: Your Personal Hinglish Voice Assistant


Krishna is a high-performance, voice-first AI companion built for the modern Indian context. He doesn't just process commands; he understands your culture, speaks your language (**Hinglish**), and remembers who you are.

---

## ✨ Why Krishna?

Most AI assistants feel formal and robotic. Krishna is built to be a **companion**.
- **Natural Hinglish:** Seamlessly switches between Hindi and English just like we do.
- **Persistent Memory:** He remembers your name and context across different sessions using a local profile system.
- **Low Latency:** Optimized with **Groq** and **WebSockets** for a conversational flow that feels real-time.
- **Authentic Voice:** Integrated with **Sarvam AI** to provide high-quality STT and TTS specifically tuned for Indian accents.

---

## 🛠️ The Tech Stack

Krishna’s "Brain" and "Ears" are powered by the best in the industry:

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Brain** | [Groq](https://groq.com/) (Llama-3.3-70B) | Lightning-fast LLM responses. |
| **Ears & Voice** | [Sarvam AI](https://www.sarvam.ai/) | High-accuracy Indian STT & TTS. |
| **Backend** | [FastAPI](https://fastapi.tiangolo.com/) | WebSocket-based real-time audio server. |
| **Memory** | Local JSON & SQLite | Persistent user profiles and analytics. |

---

## 🏗️ Project Structure

```bash
Krishna/
├── data/               # Persistent memory and analytics DB
├── frontend/           # (In Progress) Premium web interface
├── modules/            # Core logic (LLM, Voice, Memory, Analytics)
├── tests/              # Automated test suite for all modules
├── server.py           # FastAPI WebSocket entry point
└── requirements.txt    # Python dependencies
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.9+
- API Keys for **Groq** and **Sarvam AI**.

### 2. Installation
```bash
# Clone the repo
git clone https://github.com/parthsahay24/Krishna-AI.git
cd Krishna

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Setup
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_key
SARVAM_API_KEY=your_sarvam_key
SERVER_PORT=8000
```

### 4. Run the Server
```bash
python server.py
```
Krishna is now live at `ws://localhost:8000/ws`.

---

## 🎯 Future Roadmap
- [ ] **Phase 4:** Premium Glassmorphic Web UI.
- [ ] **Phase 5:** Mobile app integration.
- [ ] **Phase 6:** Advanced long-term RAG memory.

---

## 🤝 Contributing
Krishna is an open-source project! If you have ideas to make him smarter or more "Bhai-like," feel free to open a PR.

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
