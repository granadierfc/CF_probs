function fetchProblems() {
    const handle = document.getElementById("handle").value;
    const tags = document.getElementById("tags").value;
    const minRating = document.getElementById("min_rating").value;

    const url = `/api/solved_problems?handle=${handle}&tags=${tags}&min_rating=${minRating}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const resultsList = document.getElementById("results");
            resultsList.innerHTML = "";

            if (data.problems.length === 0) {
                resultsList.innerHTML = "<li>No problems found.</li>";
            } else {
                data.problems.forEach(problem => {
                    const listItem = document.createElement("li");
                    const link = document.createElement("a");
                    link.href = problem.url;
                    link.textContent = problem.name;
                    link.target = "_blank";
                    listItem.appendChild(link);
                    resultsList.appendChild(listItem);
                });
            }
        })
        .catch(error => console.error("Error:", error));
}