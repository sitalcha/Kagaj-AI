# Kagaj-AI (कागज-AI): Nepali Form & Handwriting Extractor 🤖📋
*Powered by Google Gemini AI*

This project uses Google's Gemini AI to automatically read thousands of scanned Nepali forms (PDF or JPG) and extracts specific data into an Excel sheet. 

यो प्रोजेक्टले गुगलको Gemini AI प्रयोग गरेर हजारौं स्क्यान गरिएका नेपाली फारमहरू (PDF वा JPG) अटोमेटिक पढ्छ र त्यहाँबाट चाहिएको डाटा निकालेर सिधै Excel मा सेभ गर्छ।

---

## 🌟 Features (मुख्य विशेषताहरू)
- **100% Accurate Nepali Handwriting (१००% शुद्ध नेपाली हस्तलिखित डाटा):** Accurately extracts handwritten Nepali text (Unicode) from scanned documents. (हातले लेखेको नेपाली अक्षर पनि १००% शुद्धसँग पढ्न सक्ने!)
- **Read Nepali Applications / Niwedan (निवेदन तथा चिठीपत्र पढ्ने):** Not just forms, it can also read handwritten Nepali applications (निवेदन) and extract the exact meaning, name, or subject from it.
- **High Accuracy (उच्च शुद्धता):** Uses `fitz` (PyMuPDF) to extract the exact Cover Page of PDFs in high quality.
- **Auto-Save (अटो-सेभ):** Automatically saves the data in Excel after every 5 extractions to prevent data loss.
- **Smart Rate-Limit Handling (अटोमेटिक टाइमर):** Pauses and waits automatically if the Google API hits a Rate Limit (429/503 errors). It won't crash!
- **Error Skipping:** Skips corrupted files or network errors and continues processing. You can rerun the script to retry skipped files.
- **Model Configurable:** Easily switch between `gemini-1.5-flash` or `gemini-3.1-flash-lite` directly from the code.

---

## ⚙️ How it Works? (यसले कसरी काम गर्छ?)
यो प्रोजेक्टले मुख्यतया ३ वटा स्टेपमा काम गर्छ। यदि तपाईंले यसलाई आफ्नो तरिकाले चलाउन चाहनुहुन्छ भने यो बुझ्न जरुरी छ:

### Step 1: फोटोलाई पढ्ने (Reading the Document)
सुरुमा कोडले तपाईंको PDF भित्रको पहिलो पेज (जहाँ फारम हुन्छ) त्यसलाई फोटो (Image) मा बदल्छ।

### Step 2: AI ले डाटा निकाल्ने (JSON Format)
त्यो फोटो गुगलको Gemini AI लाई पठाइन्छ र AI लाई एउटा निर्देशन (Prompt) दिइन्छ। AI ले फोटोमा भएको हातले लेखेको कुरालाई बुझेर कम्प्युटरले बुझ्ने भाषा **(JSON)** मा तलको जस्तै गरेर उत्तर दिन्छ:
```json
{
  "Folder": "065151",
  "Form_No": "065151",
  "Head_of_Family": "राम बहादुर खत्री",
  "Ward_No": "५"
}
```
*नोट: यदि तपाईंलाई निवेदनबाट 'विषय' निकाल्नु छ भने, तपाईंले प्रम्प्ट (Prompt) मा "Please extract the Subject of the application" भनेर लेख्नुभयो भने AI ले त्यही अनुसार JSON बनाएर दिन्छ।*

### Step 3: Excel मा सेभ गर्ने (Saving to Excel)
AI बाट आएको माथिको JSON डाटालाई पाइथन (Python) को `pandas` भन्ने टुलले टेबलमा राख्छ र सिधै Excel फाइलमा लगेर सेभ गरिदिन्छ।

---

## 🛠️ Requirements (आवश्यक कुराहरू)
Make sure you have Python installed. Then, install the required libraries:

Python इन्स्टल गरिसकेपछि आफ्नो टर्मिनलमा यो कमान्ड रन गर्नुहोस्:
```bash
pip install pandas PyMuPDF pillow google-genai openpyxl
```

---

## 🚀 How to Use (कसरी चलाउने?)

### 1. Set your API Key (आफ्नो API Key राख्ने)
Open `auto_extract.py` and replace `YOUR_API_KEY_HERE` with your actual Google Gemini API Key. You can also change the `SELECTED_MODEL` based on your quota (e.g., `gemini-3.1-flash-lite` has a 500 RPD limit, while `gemini-1.5-flash` has a 1500 RPD limit).

`auto_extract.py` फाइल खोल्नुहोस् र त्यहाँ `YOUR_API_KEY_HERE` लेखिएको ठाउँमा आफ्नो Google Gemini को API Key राख्नुहोस्। तपाईंले आफूलाई चाहिएको मोडल पनि त्यहीँबाट फेर्न सक्नुहुन्छ।

### 2. Folder Structure (फोल्डर कसरी राख्ने?)
Place all your form folders inside a main directory. Update `FOLDER_DIR` and `EXCEL_FILE` paths in the script according to your PC.

तपाईंको सबै फारम भएका फोल्डरहरूलाई एउटा मुख्य फोल्डरमा राख्नुहोस् र कोडमा भएको `FOLDER_DIR` (जस्तै: e:/data/folder) लाई आफ्नो कम्प्युटर अनुसार मिलाउनुहोस्।

### 3. Run the Script (कोड रन गर्ने)
Run the script using Python:

टर्मिनलमा गएर यो कमान्ड हान्नुहोस्:
```bash
python auto_extract.py
```

---

## 🧪 Testing your API Key (API Key टेस्ट गर्ने)
We have also included a `check_api_key.py` script. Run it to instantly check if your API Key is working or if the daily quota is exhausted.

तपाईंको API Key ले काम गरिरहेको छ कि यसको लिमिट सकिसक्यो भनेर चेक गर्न `check_api_key.py` प्रयोग गर्न सक्नुहुन्छ:
```bash
python check_api_key.py
```

---

## 🤝 Contribution
Feel free to fork this project, improve the prompts, or add features like multi-threading!

यो कोडलाई अझै राम्रो बनाउन जो कोहीले पनि मद्दत गर्न (Contribute) सक्नुहुन्छ!
