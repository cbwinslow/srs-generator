function formatSRSContent(data) {
    if (!data.sections) {
        return `<pre>${JSON.stringify(data, null, 2)}</pre>`;
    }

    return `
        <div class="srs-document">
            <section class="srs-section">
                <h3>1. Introduction</h3>
                <div class="section-content">${markdownToHtml(data.sections.introduction)}</div>
            </section>

            <section class="srs-section">
                <h3>2. Functional Requirements</h3>
                <div class="section-content">${markdownToHtml(data.sections.functional_requirements)}</div>
            </section>

            <section class="srs-section">
                <h3>3. Non-Functional Requirements</h3>
                <div class="section-content">${markdownToHtml(data.sections.non_functional_requirements)}</div>
            </section>

            <section class="srs-section">
                <h3>4. Constraints</h3>
                <div class="section-content">${markdownToHtml(data.sections.constraints)}</div>
            </section>
        </div>
    `;
}

function markdownToHtml(markdown) {
    if (!markdown) return "";
    
    // Basic Markdown to HTML conversion
    return markdown
        .replace(/

/g, "</p><p>")
        .replace(/
/g, "<br>")
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
        .replace(/\*(.*?)\*/g, "<em>$1</em>")
        .replace(/^- (.*)/gm, "• $1");
}

function downloadMarkdown(data) {
    const sections = data.sections;
    const markdown = `# Software Requirements Specification

## 1. Introduction
${sections.introduction}

## 2. Functional Requirements
${sections.functional_requirements}

## 3. Non-Functional Requirements
${sections.non_functional_requirements}

## 4. Constraints
${sections.constraints}
`;

    const blob = new Blob([markdown], { type: "text/markdown" });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    const timestamp = new Date().toISOString().split("T")[0];
    a.href = url;
    a.download = `srs_document_${timestamp}.md`;
    a.click();
    window.URL.revokeObjectURL(url);
}

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("srsForm");
    const loading = document.getElementById("loading");
    const result = document.getElementById("result");
    const srsContent = document.getElementById("srsContent");
    const downloadBtn = document.getElementById("downloadBtn");
    let currentData = null;

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

            currentData = data;
            srsContent.innerHTML = formatSRSContent(data);
            result.style.display = "block";
        } catch (error) {
            alert(`Error: ${error.message}`);
        } finally {
            loading.style.display = "none";
        }
    });

    downloadBtn.addEventListener("click", () => {
        if (currentData) {
            downloadMarkdown(currentData);
        }
    });
});
