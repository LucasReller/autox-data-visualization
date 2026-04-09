document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("driverSearch");
    const seasonSelect = document.getElementById("seasons");
    const results = document.querySelectorAll("#driverResults .result");
    const driverCount = document.getElementById("driverCount");

function filterDrivers() {
    const searchValue = searchInput.value.toLowerCase();
    const selectedSeason = seasonSelect.value;
    let visibleResults = [];

    results.forEach(result => {
        const name = result.querySelector("strong").textContent.toLowerCase();
        const links = Array.from(result.querySelectorAll("a"));

        const matchesSearch = name.includes(searchValue);

        let matchesSeason = selectedSeason === "all";
        let placement = null;

        // 👇 NEW: filter links inside each driver
        links.forEach(link => {
            const linkSeason = link.dataset.season;

            const showLink = selectedSeason === "all" || linkSeason === selectedSeason;
            link.style.display = showLink ? "inline" : "none";

            if (selectedSeason !== "all" && linkSeason === selectedSeason) {
                matchesSeason = true;
                placement = parseInt(link.dataset.placement);
            }
        });

        const isVisible = matchesSearch && matchesSeason;
        result.style.display = isVisible ? "block" : "none";

        if (isVisible) {
            visibleResults.push({
                element: result,
                placement: placement ?? 9999
            });
        }
    });

    // Sort when filtering by a specific season
    if (selectedSeason !== "all") {
        visibleResults.sort((a, b) => a.placement - b.placement);
    }

    // Re-append sorted results
    const container = document.getElementById("driverResults");
    visibleResults.forEach(item => {
        container.appendChild(item.element);
    });

    driverCount.textContent = visibleResults.length.toString();
}

    // Attach events
    searchInput.addEventListener("input", filterDrivers);
    seasonSelect.addEventListener("change", filterDrivers);

    // Reset on page load + initial count
    searchInput.value = "";
    seasonSelect.value = "all";
    filterDrivers();
});