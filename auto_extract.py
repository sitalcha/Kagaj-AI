import os
import time
import json
import re
import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

import pandas as pd
import fitz  # PDF बाट page 0 निकाल्न (सबैभन्दा सुरक्षित तरिका)
import google.genai as genai
from PIL import Image
import io

# ═══════════════════════════════════════════════════════════════
# १. API Key र Model (यहाँबाट सजिलै परिवर्तन गर्न मिल्ने)
# ═══════════════════════════════════════════════════════════════
ALL_API_KEYS = [
    "YOUR_API_KEY_HERE", # Replace with your actual Gemini API Key
]

# तपाईंले गुगलको ड्यासबोर्डमा हेरेर आफूलाई चाहिएको मोडलको नाम यहाँ फेर्न सक्नुहुन्छ
SELECTED_MODEL = 'gemini-3.1-flash-lite'

API_KEYS = [k for k in ALL_API_KEYS if k.strip()]
if not API_KEYS:
    print("ERROR: कुनै पनि API Key राखिएको छैन!")
    sys.exit(1)

print(f"[✓] {len(API_KEYS)} वटा API Key लोड भयो।")
print(f"[✓] प्रयोग भइरहेको मोडल: {SELECTED_MODEL}")

current_key_index = 0
client = genai.Client(api_key=API_KEYS[current_key_index])

def switch_api_key():
    global current_key_index, client
    old = current_key_index
    current_key_index = (current_key_index + 1) % len(API_KEYS)
    if current_key_index == old:
        print(f"\n[!] सबै Key मा Limit! 60s पर्खिँदैछ...")
        time.sleep(60)
    else:
        print(f"\n[→] Key {old+1} → Key {current_key_index+1}")
    client = genai.Client(api_key=API_KEYS[current_key_index])
    time.sleep(1)

EXCEL_FILE = 'e:/data/dataseet.xlsx'
FOLDER_DIR = 'e:/data/folder'

# ═══════════════════════════════════════════════════════════════
# २. Cover Page Image प्राप्त गर्ने (PDF Page 0 = 100% सही)
# ═══════════════════════════════════════════════════════════════
def get_cover_image(folder_path, folder_name):
    """
    सबैभन्दा सुरक्षित तरिकाले Cover Page image फिर्ता गर्ने।
    
    प्राथमिकता:
      1. PDF को Page 0 (150 DPI) → 100% Cover Page ग्यारेन्टी!
      2. Fallback: JPG (यदि PDF नभएमा वा corrupt भएमा)
    
    किन PDF Page 0 सबैभन्दा सुरक्षित?
      - 204 फोल्डरमा JPG नै छैन, PDF मात्र छ
      - 5 फोल्डरमा JPG Alphabetical sort ले गलत क्रम दिन्छ
      - PDF मा Page 0 = सधैं Cover Page (100% ग्यारेन्टी)
    
    किन 150 DPI?
      - Default 72 DPI = 612x792 px (अस्पष्ट)
      - 150 DPI = 1275x1650 px (एकदम स्पष्ट, Original JPG जस्तै)
      - 300 DPI = 2550x3300 px (अनावश्यक ठूलो, token बर्बाद)
    """
    
    # === तरिका 1: PDF को Page 0 (सबैभन्दा सुरक्षित) ===
    pdf_path = os.path.join(folder_path, f"{folder_name}.pdf")
    if os.path.exists(pdf_path):
        try:
            doc = fitz.open(pdf_path)
            page = doc.load_page(0)  # Page 0 = Cover Page = सधैं सही
            # 150 DPI मा image बनाउने (स्पष्ट तर token-efficient)
            pix = page.get_pixmap(dpi=150)
            img = Image.open(io.BytesIO(pix.tobytes()))
            doc.close()
            # Token बचतको लागि resize
            img.thumbnail((700, 700))
            return img, "PDF"
        except Exception as e:
            print(f"  ⚠ PDF corrupt/error: {e}")
    
    # === तरिका 2: Fallback - JPG (PDF नभएमा मात्र) ===
    jpgs = sorted([f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
    if jpgs:
        try:
            img = Image.open(os.path.join(folder_path, jpgs[0]))
            img.thumbnail((700, 700))
            return img, "JPG"
        except Exception as e:
            print(f"  ⚠ JPG error: {e}")
    
    return None, None

# ═══════════════════════════════════════════════════════════════
# ३. AI बाट डाटा निकाल्ने (१ फारम = १ API Call)
# ═══════════════════════════════════════════════════════════════
def extract_data(folder_path, folder_name, flush_callback=None):
    max_retries = 100
    
    img, source = get_cover_image(folder_path, folder_name)
    if img is None:
        print(f"  ✗ कुनै image/PDF भेटिएन!")
        return None
    
    prompt = """Extract from this Nepali form:
1. Form Number (फारम नं.) - 6 digits, zero-padded (e.g., 065174).
2. Head of Family Name (परिवारमुलीको नाम) - from section "१.१".
3. Ward Number (वडा नं.) - from section 1.10 or 1.12.

Return ONLY raw JSON. Example:
{"फारम नं.": "065174", "परिवारमुलीको नाम": "राम बहादुर", "वडा नं.": 6}"""
    
    keys_tried = 0
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=SELECTED_MODEL,
                contents=[prompt, img]
            )
            text = response.text.replace('```json', '').replace('```', '').strip()
            data = json.loads(text)
            return data
        except Exception as e:
            error_msg = str(e)
            if '429' in error_msg or 'Quota' in error_msg or 'RESOURCE_EXHAUSTED' in error_msg or '503' in error_msg or 'UNAVAILABLE' in error_msg:
                keys_tried += 1
                if len(API_KEYS) > 1:
                    switch_api_key()
                    if keys_tried >= len(API_KEYS):
                        print(f"\n[!] सबै Key limit! 60s पर्खिँदैछ... (Attempt {attempt+1})")
                        if flush_callback: flush_callback()
                        time.sleep(60)
                        keys_tried = 0
                    continue
                match = re.search(r'retry in ([\d\.]+)s', error_msg)
                wait_time = int(float(match.group(1))) + 2 if match else 60
                print(f"\n[!] Rate Limit! {wait_time}s पर्खिँदैछ...")
                if flush_callback: flush_callback()
                time.sleep(wait_time)
            else:
                print(f"  Error: {e}")
                return None
    return None

# ═══════════════════════════════════════════════════════════════
# ४. मुख्य कार्यक्रम
# ═══════════════════════════════════════════════════════════════
def main():
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE, dtype={'फोल्डर': str})
        if 'फोल्डर' in df.columns:
            processed_folders = set(str(x).split('.')[0].zfill(6) for x in df['फोल्डर'].dropna().tolist())
        else:
            df['फोल्डर'] = ''
            processed_folders = set()
    else:
        df = pd.DataFrame(columns=['फोल्डर', 'फारम नं.', 'परिवारमुलीको नाम', 'वडा नं.'])
        processed_folders = set()
    
    all_dirs = sorted([d for d in os.listdir(FOLDER_DIR) if os.path.isdir(os.path.join(FOLDER_DIR, d))])
    remaining_dirs = [d for d in all_dirs if str(d).strip() not in processed_folders]
    
    print(f"Total folders: {len(all_dirs)}")
    print(f"Already processed: {len(processed_folders)}")
    print(f"Remaining: {len(remaining_dirs)}")
    print()
    
    new_rows = []
    skipped = 0
    
    def force_save():
        nonlocal df, new_rows
        if new_rows:
            df_new = pd.DataFrame(new_rows)
            df = pd.concat([df, df_new], ignore_index=True)
            df.drop_duplicates(subset=['फोल्डर'], keep='last', inplace=True)
            while True:
                try:
                    df.to_excel(EXCEL_FILE, index=False)
                    print(f"\n--- [Auto-Save] Limit अघि सुरक्षित गरियो! Total: {len(df)} ---")
                    break
                except PermissionError:
                    print(f"\n[!] एक्सेल बन्द गर्नुहोस्! 10s...")
                    time.sleep(10)
            new_rows.clear()
            
    for idx, d in enumerate(remaining_dirs):
        print(f"[{idx+1}/{len(remaining_dirs)}] Folder {d}...", end=" ")
        
        folder_path = os.path.join(FOLDER_DIR, d)
        data = extract_data(folder_path, d, flush_callback=force_save)
        
        if data:
            data['फोल्डर'] = str(d).strip()
            print(f"✓ {data.get('परिवारमुलीको नाम', '?')}")
            new_rows.append(data)
            
            if len(new_rows) >= 5:
                df_new = pd.DataFrame(new_rows)
                df = pd.concat([df, df_new], ignore_index=True)
                df.drop_duplicates(subset=['फोल्डर'], keep='last', inplace=True)
                while True:
                    try:
                        df.to_excel(EXCEL_FILE, index=False)
                        print(f"--- Saved! Total: {len(df)} ---")
                        break
                    except PermissionError:
                        print(f"\n[!] एक्सेल बन्द गर्नुहोस्! 10s...")
                        time.sleep(10)
                new_rows = []
        else:
            skipped += 1
                
        time.sleep(7)
        
    if new_rows:
        df_new = pd.DataFrame(new_rows)
        df = pd.concat([df, df_new], ignore_index=True)
        df.drop_duplicates(subset=['फोल्डर'], keep='last', inplace=True)
        while True:
            try:
                df.to_excel(EXCEL_FILE, index=False)
                break
            except PermissionError:
                print(f"\n[!] एक्सेल बन्द गर्नुहोस्! 10s...")
                time.sleep(10)

    print(f"\n{'='*50}")
    print(f"✅ काम पूरा! Total: {len(df)} | Skipped: {skipped}")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
