document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("srsForm");
    const loading = document.getElementById("loading");
    const result = document.getElementById("result");
    const srsContent = document.getElementById("srsContent");
    const downloadBtn = document.getElementById("downloadBtn");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        
        const formData = {
            projectName: document.getElementById("projectName").value,
            targetUsers: document.getElementById("targetUsers").value,
            projectGoals: document.getElementById("projectGoals").value,
            projectScope: document.getElementById("projectScope").value
        };

        try {
            loading.style.display = "block";
            result.style.display = "none";

            const response = await fetch("/api/v1/generate_srs", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "Failed to generate SRS");
            }

            srsContent.innerHTML = formatSRSContent(data);
            result.style.display = "block";
        } catch (error) {
            alert(`Error: ${error.message}`);
        } finally {
            loading.style.display = "none";
        }
    });

    downloadBtn.addEventListener("click", () => {
        const content = srsContent.innerText;
        const blob = new Blob([content], { type: "text/plain" });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "srs_document.md";
        a.click();
        window.URL.revokeObjectURL(url);
    });

    function formatSRSContent(data) {
        // TODO: Implement proper formatting of the SRS content
        return `<pre>${JSON.stringify(data, null, 2)}</pre>`;
    }
});
