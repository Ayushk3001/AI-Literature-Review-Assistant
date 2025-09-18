# 🧠 AI Literature Review Assistant

An AI‑powered web app that lets you enter a research topic, fetch relevant papers from **arXiv**, and generate a structured literature review. Built using **Streamlit** and **Autogen**’s multi‑agent framework, with summarization done via OpenAI models.

---

## 🚀 Features

- Search arXiv for papers based on a user topic.  
- Choose how many papers (1–10) to include in the review.  
- Two‑agent architecture:  
  1. *Search Agent* — finds candidate papers via arXiv tool.  
  2. *Summarizer Agent* — crafts a markdown literature review.  
- Clean front‑end using Streamlit; results displayed chat‑style.  
- Async/streaming output so you see the review build in real time.

---

## 📁 Repository Structure

```
.
├── frontend.py             # Streamlit UI
├── backend.py              # Backend agents + orchestrator logic
├── requirements.txt        # Dependencies
└── README.md               # Project documentation
```

---

## 🛠️ Installation

1. Clone the repo:

   ```bash
   git clone https://github.com/Ayushk3001/AI-Literature-Review-Assistant.git
   cd AI-Literature-Review-Assistant
   ```

2. Create & activate a virtual environment (recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate        # macOS / Linux
   venv\Scripts\activate           # Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables by creating a `.env` file in the project root:

   ```text
   OPEN_API=your_openai_api_key_here
   ```

   Replace `your_openai_api_key_here` with your OpenAI API key.

---

## ▶️ Usage

To run the Streamlit app:

```bash
streamlit run frontend.py
```

- Enter the **research topic** in the input box.  
- Pick the **number of papers** with the slider (default ≈ 5).  
- Click **Search** ➜ wait for the review to stream in.  

You’ll see messages like `assistant: …`, etc., building up the review.

For testing via CLI (if desired), you can also run the backend directly:

```bash
python backend.py
```

---

## ⚙️ Configuration

- The OpenAI model is set to `gpt-5-nano` by default. You can override this if needed in the code.  
- Number of papers fetched is managed by the `num_papers` parameter.  
- The system uses the `FunctionTool` wrapping `arxiv_search`, so results come with title, authors, summary, published date, and PDF URL.

---

## 🤝 Contributing

Contributions are welcome!  
- Fork the repo  
- Create a feature branch (`git checkout -b feature-name`)  
- Commit changes (`git commit -m 'Added new feature'`)  
- Push branch (`git push origin feature-name`)  
- Open a Pull Request  
