async function translate() {
    const sourceText = document.getElementById('sourceText').value;
    const sourceLanguage = document.getElementById('sourceLanguage').value;
    const targetLanguage = document.getElementById('targetLanguage').value;
    
    if (!sourceText.trim()) {
        alert('Please enter text to translate');
        return;
    }
    
    try {
        const response = await fetch('/translate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: sourceText,
                source_language: sourceLanguage,
                target_language: targetLanguage
            })
        });
        
        const data = await response.json();
        if (data.success) {
            document.getElementById('translatedText').value = data.translation;
        } else {
            alert('Translation failed: ' + data.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
} 