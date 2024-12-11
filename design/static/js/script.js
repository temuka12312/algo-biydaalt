function updateWordCount() {
    const text = document.getElementById('text').value;
    const words = text.trim().split(/\s+/).filter(Boolean); // Үгсийг хуваах
    const wordCount = words.length;
    document.getElementById('word-count').textContent = wordCount;

    // Үгийн тоог 400-аас илүү болгохгүй байх
    if (wordCount > 400) {
      document.getElementById('text').value = words.slice(0, 400).join(' ');
      document.getElementById('word-count').textContent = 400;
    }
  }

document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const textArea = document.getElementById('text');
    const suggestionsDiv = document.querySelector('.suggestions');
    
    // Optionally, listen for form submission and perform any client-side actions
    form.addEventListener('submit', function (e) {
        const text = textArea.value.trim();
        
        if (!text) {
            alert("Текстээ оруулна уу.");
            e.preventDefault();
        }
    });

    // Handle displaying suggestions if they exist
    if (suggestionsDiv && suggestionsDiv.querySelector('ul').children.length === 0) {
        // Display message if no suggestions found
        const noErrorsMessage = document.createElement('p');
        noErrorsMessage.classList.add('no-errors');
        noErrorsMessage.textContent = "Алдаа олсонгүй";
        suggestionsDiv.appendChild(noErrorsMessage);
    }
});
