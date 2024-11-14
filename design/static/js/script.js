document.getElementById("spellCheckForm").onsubmit = async function(event) {
    event.preventDefault();
    const formData = new FormData(this);

    const response = await fetch(this.action, {
        method: 'POST',
        body: formData,
    });
    const data = await response.json();
    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "";

    for (const [word, suggestions] of Object.entries(data.misspelled_words)) {
        resultsDiv.innerHTML += `<p>Word: ${word} | Suggestions: ${suggestions.join(", ")}</p>`;
    }
};