/**
 * Kagaj-AI — Client-Side App Logic
 * No server needed! Calls Gemini API directly from the browser.
 */

// ═══════════════════════════════════════════════
// ELEMENTS
// ═══════════════════════════════════════════════
const $ = (id) => document.getElementById(id);

const dropZone = $('dropZone');
const fileInput = $('fileInput');
const filePreview = $('filePreview');
const previewName = $('previewName');
const previewSize = $('previewSize');
const previewImage = $('previewImage');
const removeFile = $('removeFile');
const promptInput = $('promptInput');
const extractBtn = $('extractBtn');
const btnLoader = $('btnLoader');
const btnIcon = $('btnIcon');
const btnLabel = $('btnLabel');
const resultsSection = $('resultsSection');
const resultCards = $('resultCards');
const fullTextContent = $('fullTextContent');
const errorBanner = $('errorBanner');
const errorMsg = $('errorMsg');
const toast = $('toast');
const toastMsg = $('toastMsg');
const apiKeyInput = $('apiKeyInput');
const apiKeySave = $('apiKeySave');
const apiKeyStatus = $('apiKeyStatus');

let selectedFile = null;
let selectedBase64 = null;
let selectedMimeType = null;

// ═══════════════════════════════════════════════
// API KEY MANAGEMENT
// ═══════════════════════════════════════════════
const STORAGE_KEY = 'kagaj_ai_api_key';

function loadApiKey() {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
        apiKeyInput.value = saved;
        apiKeyStatus.textContent = '✓ Key saved in browser';
        apiKeyStatus.style.color = '#10b981';
    }
}

apiKeySave.addEventListener('click', () => {
    const key = apiKeyInput.value.trim();
    if (!key) {
        apiKeyStatus.textContent = '❌ Please enter an API key';
        apiKeyStatus.style.color = '#ef4444';
        return;
    }
    localStorage.setItem(STORAGE_KEY, key);
    apiKeyStatus.textContent = '✓ Key saved in browser';
    apiKeyStatus.style.color = '#10b981';
});

function getApiKey() {
    return apiKeyInput.value.trim() || localStorage.getItem(STORAGE_KEY) || '';
}

loadApiKey();

// ═══════════════════════════════════════════════
// FILE HANDLING
// ═══════════════════════════════════════════════
dropZone.addEventListener('click', () => fileInput.click());

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
});

dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    if (e.dataTransfer.files.length) handleFile(e.dataTransfer.files[0]);
});

fileInput.addEventListener('change', () => {
    if (fileInput.files.length) handleFile(fileInput.files[0]);
});

function handleFile(file) {
    // Validate
    const validTypes = ['image/jpeg', 'image/png', 'image/webp', 'image/bmp', 'image/tiff'];
    if (!validTypes.includes(file.type)) {
        showError('Only image files are supported: JPG, PNG, WebP, BMP');
        return;
    }
    if (file.size > 15 * 1024 * 1024) {
        showError('File too large! Maximum 15 MB.');
        return;
    }

    selectedFile = file;
    selectedMimeType = file.type;

    // Read as base64
    const reader = new FileReader();
    reader.onload = (e) => {
        const dataUrl = e.target.result;
        selectedBase64 = dataUrl.split(',')[1]; // Remove "data:image/...;base64,"

        // Show preview
        previewImage.src = dataUrl;
        previewName.textContent = file.name;
        previewSize.textContent = formatSize(file.size);
        filePreview.classList.add('visible');
        dropZone.classList.add('hidden');
        extractBtn.disabled = false;
        hideError();
        resultsSection.classList.remove('visible');
    };
    reader.readAsDataURL(file);
}

removeFile.addEventListener('click', resetUpload);

function resetUpload() {
    selectedFile = null;
    selectedBase64 = null;
    fileInput.value = '';
    filePreview.classList.remove('visible');
    dropZone.classList.remove('hidden');
    extractBtn.disabled = true;
    resultsSection.classList.remove('visible');
    hideError();
}

// ═══════════════════════════════════════════════
// EXTRACTION (Direct Gemini REST API Call)
// ═══════════════════════════════════════════════
extractBtn.addEventListener('click', extract);

async function extract() {
    const apiKey = getApiKey();
    if (!apiKey) {
        showError('Please enter your Gemini API Key first! (Get free key from aistudio.google.com)');
        return;
    }
    if (!selectedBase64) {
        showError('Please upload an image first!');
        return;
    }

    // UI: Loading state
    setLoading(true);
    hideError();
    resultsSection.classList.remove('visible');

    let userPrompt = promptInput.value.trim();
    if (!userPrompt) {
        userPrompt = `Extract ALL text from this image. Read everything carefully including handwritten text.
If the content is structured (like a form), return as JSON with field names as keys.
If it's general text or a letter/application, return the full text content.
Always preserve the original language (Nepali, English, or mixed).
Be thorough — do not miss any text.`;
    }

    const model = 'gemini-2.0-flash';
    const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`;

    const body = {
        contents: [{
            parts: [
                { text: userPrompt },
                {
                    inline_data: {
                        mime_type: selectedMimeType,
                        data: selectedBase64
                    }
                }
            ]
        }]
    };

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });

        const data = await response.json();

        if (!response.ok) {
            const errMsg = data?.error?.message || 'Unknown error from API';
            if (response.status === 429) {
                throw new Error('API लिमिट सकियो! केही मिनेट पछि प्रयास गर्नुहोस्। (Rate Limit Exceeded)');
            }
            if (response.status === 400 && errMsg.includes('API_KEY')) {
                throw new Error('Invalid API Key! Please check your key.');
            }
            throw new Error(errMsg);
        }

        // Extract text from response
        const candidates = data?.candidates;
        if (!candidates || !candidates.length) {
            throw new Error('AI returned empty response. Try with a clearer image.');
        }

        const text = candidates[0]?.content?.parts?.map(p => p.text).join('\n') || '';
        if (!text.trim()) {
            throw new Error('No text could be extracted from this image.');
        }

        displayResults(text);

    } catch (err) {
        showError(err.message);
    } finally {
        setLoading(false);
    }
}

// ═══════════════════════════════════════════════
// DISPLAY RESULTS
// ═══════════════════════════════════════════════
function displayResults(text) {
    resultCards.innerHTML = '';

    // Try parsing as JSON
    const cleanText = text.replace(/```json\s*/gi, '').replace(/```\s*/g, '').trim();
    let jsonData = null;

    try {
        jsonData = JSON.parse(cleanText);
    } catch {
        // Not JSON, that's fine
    }

    if (jsonData && typeof jsonData === 'object' && !Array.isArray(jsonData)) {
        // Render as clickable cards
        Object.entries(jsonData).forEach(([key, value]) => {
            const card = document.createElement('div');
            card.className = 'result-card';
            card.innerHTML = `
                <div class="card-label">${escapeHtml(key)}</div>
                <div class="card-value">${escapeHtml(String(value))}</div>
                <span class="card-copy-hint">Click to copy</span>
                <span class="card-copied-badge">✓ Copied</span>
            `;
            card.addEventListener('click', () => {
                copyToClipboard(String(value));
                const badge = card.querySelector('.card-copied-badge');
                const hint = card.querySelector('.card-copy-hint');
                badge.style.display = 'block';
                hint.style.display = 'none';
                setTimeout(() => {
                    badge.style.display = 'none';
                    hint.style.display = '';
                }, 2000);
            });
            resultCards.appendChild(card);
        });
    }

    // Always show full text
    fullTextContent.textContent = text;
    resultsSection.classList.add('visible');

    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ═══════════════════════════════════════════════
// COPY FUNCTIONS
// ═══════════════════════════════════════════════
$('copyAllBtn').addEventListener('click', () => {
    // Copy all as formatted text
    let allText = '';
    const cards = resultCards.querySelectorAll('.result-card');
    if (cards.length) {
        cards.forEach(card => {
            const label = card.querySelector('.card-label').textContent;
            const value = card.querySelector('.card-value').textContent;
            allText += `${label}: ${value}\n`;
        });
    }
    allText += '\n' + fullTextContent.textContent;
    copyToClipboard(allText.trim());

    const btn = $('copyAllBtn');
    const label = $('copyAllLabel');
    btn.classList.add('copied');
    label.textContent = '✓ Copied!';
    setTimeout(() => {
        btn.classList.remove('copied');
        label.textContent = 'Copy All';
    }, 2000);
});

$('copyTextBtn').addEventListener('click', () => {
    copyToClipboard(fullTextContent.textContent);
    const btn = $('copyTextBtn');
    const label = $('copyTextLabel');
    btn.classList.add('copied');
    label.textContent = '✓ Copied!';
    setTimeout(() => {
        btn.classList.remove('copied');
        label.textContent = 'Copy';
    }, 2000);
});

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => showToast('Copied to clipboard!'));
}

// ═══════════════════════════════════════════════
// UI HELPERS
// ═══════════════════════════════════════════════
function setLoading(loading) {
    extractBtn.disabled = loading;
    extractBtn.classList.toggle('loading', loading);
    btnLabel.textContent = loading ? 'AI is reading...' : 'Extract with AI';
}

function showError(msg) {
    errorMsg.textContent = msg;
    errorBanner.classList.add('visible');
}

function hideError() {
    errorBanner.classList.remove('visible');
}

function showToast(msg) {
    toastMsg.textContent = msg;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 2500);
}

function formatSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / 1048576).toFixed(1) + ' MB';
}

function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}
