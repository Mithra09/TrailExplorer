const form = document.getElementById('recommendation-form');
const submitButton = document.getElementById('submit-button');
const recommendationsDiv = document.getElementById('recommendations');

form.addEventListener('submit', (e) => {
    e.preventDefault();
    const location = document.getElementById('location').value;
    const price = document.getElementById('price').value;
    const activityType = document.getElementById('activity-type').value;
    const difficultyLevel = document.getElementById('difficulty-level').value;

    const data = {
        location,
        price,
        activity_type: activityType,
        difficulty_level: difficultyLevel
    };

    fetch('/recommend', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then((response) => response.json())
    .then((recommendations) => {
        const recommendationsHtml = recommendations.map((recommendation) => {
            return `
                <div>
                    <h2>${recommendation.location}</h2>
                    <p>Price: ${recommendation.price}</p>
                    <p>Activity Type: ${recommendation.activity_type}</p>
                    <p>Difficulty Level: ${recommendation.difficulty_level}</p>
                </div>
            `;
        }).join('');

        recommendationsDiv.innerHTML = recommendationsHtml;
    })
    .catch((error) => console.error(error));
});

