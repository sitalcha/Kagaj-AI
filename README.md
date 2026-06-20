# Kagaj-AI: Nepali Handwriting & Form Extractor 🤖📋
*Powered by Google Gemini AI*

**Kagaj-AI** is a powerful automation tool designed to process thousands of scanned Nepali forms, documents, and handwritten applications (Niwedan). It uses Google's Gemini AI to accurately extract handwritten Unicode text and exports the structured data directly into Microsoft Excel.

> 🇳🇵 **नेपाली प्रयोगकर्ताहरूको लागि:** यस डकुमेन्टको नेपाली अनुवाद सबैभन्दा तल राखिएको छ। कृपया तल (Scroll) गरेर पढ्नुहोला।

---

## 🌟 Key Features
- **Accurate Nepali Handwriting OCR:** Flawlessly reads complex handwritten Nepali scripts (Devanagari/Unicode).
- **Application (Niwedan) Processing:** Capable of reading unstructured handwritten letters to extract names, subjects, or intent.
- **High-Quality PDF Parsing:** Uses `PyMuPDF` (`fitz`) to render specific pages in high resolution before passing them to the AI.
- **Smart Rate-Limit Handling:** Automatically pauses and waits if the Google API hits a `429` (Quota Exhausted) or `503` error. 
- **Auto-Save Mechanism:** Automatically commits data to Excel after every 5 successful extractions to prevent data loss during long runs.
- **Configurable AI Models:** Easily switch between `gemini-3.1-flash-lite` (Fast, 500 RPM) or `gemini-1.5-flash` depending on your API quotas.

---

## ⚙️ How it Works?
1. **Reading the Document:** The script scans the target directory and converts the cover page of each PDF into a temporary high-quality image.
2. **AI Extraction:** The image is sent to the Gemini AI API with a strict prompt, asking it to return a clean JSON object containing the required fields.
3. **Data Export:** The returned JSON is parsed using `pandas` and appended directly into your Excel file.

---

## 🛠️ Installation
Make sure you have Python 3 installed, then run:
```bash
pip install pandas PyMuPDF pillow google-genai openpyxl
```

## 🚀 Usage Guide
1. **Configure API Key:** Open `auto_extract.py` and replace `YOUR_API_KEY_HERE` with your Gemini API key.
2. **Select Model:** By default, it uses `gemini-3.1-flash-lite`. You can change the `SELECTED_MODEL` variable in the code.
3. **Run the Script:**
```bash
python auto_extract.py
```

---
---

# 🇳🇵 नेपाली खण्ड (Nepali Section)

यो प्रोजेक्टले गुगलको **Gemini AI** प्रयोग गरेर हजारौं स्क्यान गरिएका नेपाली फारमहरू (PDF वा JPG) अटोमेटिक पढ्छ र त्यहाँबाट चाहिएको डाटा निकालेर सिधै Excel मा सेभ गर्छ।

### 🌟 मुख्य विशेषताहरू:
- **हस्तलिखित अक्षर पढ्ने:** हातले लेखेको जस्तोसुकै नेपाली अक्षर (Unicode) पनि शुद्धसँग पढ्न सक्ने।
- **निवेदन पढ्न सक्ने:** फारम मात्र नभई हातले लेखेको निवेदन (Niwedan) पढेर त्यसको 'विषय' वा 'नाम' निकाल्न सक्छ।
- **अटो-सेभ (Auto-Save):** हरेक ५ वटा डाटा निस्केपछि आफैं Excel मा सेभ हुन्छ। बत्ती गएर वा इन्टरनेट गएर डाटा उड्ने डर हुँदैन।
- **स्मार्ट टाइमर:** गुगलको लिमिट सकियो भने क्र्यास (Crash) नभईकन यो आफैं केही समय पर्खिएर फेरि सुरु हुन्छ।

### ⚙️ कसरी चलाउने?
१. आफ्नो कम्प्युटरमा माथि दिइएको `pip install...` कमान्ड हानेर टुलहरू इन्स्टल गर्नुहोस।
२. `auto_extract.py` फाइल खोलेर त्यहाँ `YOUR_API_KEY_HERE` लेखिएको ठाउँमा आफ्नो गुगलको API Key हाल्नुहोस्।
३. टर्मिनलमा गएर `python auto_extract.py` टाइप गरी इन्टर थिच्नुहोस्।
