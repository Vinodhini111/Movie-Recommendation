async function getRecommendations() {
    const input = document.getElementById('movieInput').value;
    const resultsDiv = document.getElementById('results');
    const loader = document.getElementById('loader');

    if (!input) {
        alert("Please enter a movie name!");
        return;
    }

    resultsDiv.innerHTML = "";
    loader.classList.remove('hidden');

    try {
        const response = await fetch('/recommend', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ movie_input: input })
        });

        const data = await response.json();
        loader.classList.add('hidden');

        if (data.status === 'success') {
            data.rec_movies.forEach(movie => {
                const card = document.createElement('div');
                card.className = 'card';
                card.innerText = movie;
                resultsDiv.appendChild(card);
            });
        } else {
            resultsDiv.innerHTML = `<p style="color: #ff6b6b;">${data.message}</p>`;
        }
    } catch (error) {
        console.error(error);
        loader.classList.add('hidden');
        resultsDiv.innerHTML = `<p style="color: red;">Something went wrong!</p>`;
    }
}