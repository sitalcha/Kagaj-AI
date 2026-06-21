<p align="center">
  <h1 align="center">📋 Kagaj-AI (कागज-AI)</h1>
  <p align="center">
    <strong>AI-Powered Nepali Handwriting & Form Extractor</strong><br>
    <em>Turn thousands of scanned Nepali forms into structured Excel data — automatically.</em>
  </p>
  <p align="center">
    <a href="#-key-features"><img src="https://img.shields.io/badge/✨_Features-6-blue?style=for-the-badge" alt="Features"></a>
    <a href="https://ai.google.dev/"><img src="https://img.shields.io/badge/Powered_by-Google_Gemini_AI-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="Gemini AI"></a>
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"></a>
    <a href="https://github.com/sitalcha/Kagaj-AI/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License"></a>
  </p>
</p>

---

> 🇳🇵 **नेपाली प्रयोगकर्ताहरूको लागि:** यस डकुमेन्टको नेपाली अनुवाद [सबैभन्दा तल](#-नेपाली-खण्ड-nepali-section) राखिएको छ।

---

## 📖 Table of Contents
- [Key Features](#-key-features)
- [Demo Output](#-demo-output)
- [How it Works](#️-how-it-works)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [Configuration](#️-configuration)
- [API Key Testing](#-api-key-testing)
- [Supported Models](#-supported-models)
- [Contributing](#-contributing)
- [नेपाली खण्ड (Nepali Section)](#-नेपाली-खण्ड-nepali-section)

---

## ✨ Key Features

| Feature | Description |
|:---|:---|
| 🖊️ **Nepali Handwriting OCR** | Accurately reads complex handwritten Devanagari/Unicode text from scanned documents |
| 📄 **Niwedan (Application) Reading** | Extracts names, subjects, and intent from unstructured handwritten Nepali letters |
| 📑 **High-Quality PDF Parsing** | Uses `PyMuPDF` to render cover pages at 150 DPI for crystal-clear AI input |
| ⏸️ **Smart Rate-Limit Handling** | Auto-pauses on `429`/`503` errors and resumes when quota resets — never crashes |
| 💾 **Auto-Save Every 5 Records** | Commits data to Excel periodically to prevent data loss during long runs |
| 🔄 **Multi-Key Rotation** | Supports multiple API keys and rotates automatically when one hits its limit |

---

## 📊 Demo Output

When you run the script, you'll see real-time progress like this:

```
[✓] 1 API Key loaded.
[✓] Model in use: gemini-3.1-flash-lite
Total folders: 1372
Already processed: 106
Remaining: 1266

[1/1266] Folder 143695... ✓ पविर बुढाथोकी
[2/1266] Folder 143754... ✓ यादव थारु
[3/1266] Folder 143756... ✓ उषा कुमारी थापा
[4/1266] Folder 143757... ✓ लालीकला जैशी
[5/1266] Folder 143759... ✓ सावित्रा कुमारी खत्री
--- Saved! Total: 112 ---
```

**Excel Output:**

| फोल्डर | फारम नं. | परिवारमुलीको नाम | वडा नं. |
|:---|:---|:---|:---|
| 143695 | 143695 | पविर बुढाथोकी | 5 |
| 143754 | 143754 | यादव थारु | 8 |
| 143756 | 143756 | उषा कुमारी थापा | 3 |

---

## ⚙️ How it Works

```
┌──────────────┐     ┌──────────────────┐     ┌──────────────┐
│  📄 PDF      │ ──▶ │ 🤖 Gemini AI     │ ──▶ │ 📊 Excel     │
│  Cover Page  │     │ Reads Handwriting│     │ Structured   │
│  (150 DPI)   │     │ Returns JSON     │     │ Data Output  │
└──────────────┘     └──────────────────┘     └──────────────┘
```

1. **PDF → Image:** The script converts the first page (cover) of each PDF to a high-quality 150 DPI image.
2. **Image → AI:** The image is sent to Google Gemini AI with a strict prompt, asking it to return a clean JSON object.
3. **JSON → Excel:** The returned JSON is parsed by `pandas` and appended directly into the Excel file.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- A free [Google Gemini API Key](https://aistudio.google.com/apikey)

### Installation

```bash
# Clone the repository
git clone https://github.com/sitalcha/Kagaj-AI.git
cd Kagaj-AI

# Install all dependencies (one command!)
pip install -r requirements.txt
```

### Run

```bash
python Kagaj_AI.py
```

---

## 📁 Project Structure

```
Kagaj-AI/
├── Kagaj_AI.py          # Main extraction script
├── check_api_key.py     # API key testing utility
├── requirements.txt     # Python dependencies
├── dataseet.xlsx        # Output Excel file (sample)
├── README.md            # This file
└── folder/              # Sample PDF folders for demo
    ├── 065151/
    │   └── 065151.pdf
    ├── 065152/
    │   └── 065152.pdf
    └── ...
```

---

## 🛠️ Configuration

Open `Kagaj_AI.py` and edit these variables at the top:

```python
# Add your API Key(s) here
ALL_API_KEYS = [
    "YOUR_API_KEY_HERE",      # Get from: https://aistudio.google.com/apikey
]

# Choose your AI model
SELECTED_MODEL = 'gemini-3.1-flash-lite'

# Set your file paths
EXCEL_FILE = 'path/to/your/output.xlsx'
FOLDER_DIR = 'path/to/your/pdf/folders'
```

---

## 🧪 API Key Testing

Before running the main script, test if your API key is working:

```bash
python check_api_key.py
```

This will instantly tell you if your key is active or if the daily quota is exhausted.

---

## 📋 Supported Models

| Model | Daily Limit (RPD) | Per Minute (RPM) | Best For |
|:---|:---:|:---:|:---|
| `gemini-3.1-flash-lite` | **500** | 15 | ⭐ Recommended for this project |
| `gemini-2.5-flash-lite` | 20 | 10 | Low volume tasks |
| `gemini-2.5-flash` | 20 | 5 | Low volume tasks |

> 💡 **Tip:** With 3 API keys using `gemini-3.1-flash-lite`, you can process **1,500 forms per day** for free!

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- 🐛 Report bugs via [Issues](https://github.com/sitalcha/Kagaj-AI/issues)
- 💡 Suggest features
- 🔀 Submit pull requests

---
---

## 🇳🇵 नेपाली खण्ड (Nepali Section)

यो प्रोजेक्टले गुगलको **Gemini AI** प्रयोग गरेर हजारौं स्क्यान गरिएका नेपाली फारमहरू (PDF वा JPG) अटोमेटिक पढ्छ र त्यहाँबाट चाहिएको डाटा निकालेर सिधै Excel मा सेभ गर्छ।

### 🌟 मुख्य विशेषताहरू:
- **🖊️ हस्तलिखित अक्षर पढ्ने:** हातले लेखेको जस्तोसुकै नेपाली अक्षर (Unicode) पनि १००% शुद्धसँग पढ्न सक्ने।
- **📄 निवेदन पढ्न सक्ने:** फारम मात्र नभई हातले लेखेको निवेदन (Niwedan) पढेर त्यसको 'विषय' वा 'नाम' निकाल्न सक्छ।
- **💾 अटो-सेभ (Auto-Save):** हरेक ५ वटा डाटा निस्केपछि आफैं Excel मा सेभ हुन्छ। बत्ती गएर वा इन्टरनेट गएर डाटा उड्ने डर हुँदैन।
- **⏸️ स्मार्ट टाइमर:** गुगलको लिमिट सकियो भने क्र्यास (Crash) नभईकन यो आफैं केही समय पर्खिएर फेरि सुरु हुन्छ।
- **🔄 बहु-Key सपोर्ट:** एकभन्दा बढी API Key राख्न सकिन्छ। एउटाको लिमिट सकिएपछि अर्कोमा आफैं जान्छ।

### ⚙️ कसरी चलाउने? (सजिलो तरिका)

**१.** सुरुमा आफ्नो कम्प्युटरमा Python इन्स्टल भएको हुनुपर्छ।

**२.** तलको कमान्ड कपी गरेर CMD मा पेस्ट गर्नुहोस् (सबै कुरा एकैपटक इन्स्टल हुन्छ):
```bash
pip install -r requirements.txt
```

**३.** `Kagaj_AI.py` फाइल खोलेर त्यहाँ `YOUR_API_KEY_HERE` लेखिएको ठाउँमा आफ्नो गुगलको API Key हाल्नुहोस्।

**४.** टर्मिनलमा गएर यो कमान्ड हान्नुहोस्:
```bash
python Kagaj_AI.py
```
कोड चल्न सुरु हुनेछ! 🎉

---

<p align="center">
  Made with ❤️ in Nepal 🇳🇵
</p>
