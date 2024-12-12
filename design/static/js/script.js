function updateWordCount() {
    const text = document.getElementById('text').value;
    const words = text.trim().split(/\s+/).filter(Boolean);
    const wordCount = words.length;
    document.getElementById('word-count').textContent = wordCount;

    if (wordCount > 400) {
      document.getElementById('text').value = words.slice(0, 400).join(' ');
      document.getElementById('word-count').textContent = 400;
    }
  }

document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const textArea = document.getElementById('text');
    const suggestionsDiv = document.querySelector('.suggestions');
    
    form.addEventListener('submit', function (e) {
        const text = textArea.value.trim();
        
        if (!text) {
            alert("Текстээ оруулна уу.");
            e.preventDefault();
        }
    });

    if (suggestionsDiv && suggestionsDiv.querySelector('ul').children.length === 0) {
        const noErrorsMessage = document.createElement('p');
        noErrorsMessage.classList.add('no-errors');
        noErrorsMessage.textContent = "Алдаа олсонгүй";
        suggestionsDiv.appendChild(noErrorsMessage);
    }
});
