
const API_BASE = "http://127.0.0.1:5000";

const jobsContainer = document.getElementById("jobs-container");
const jobsMessage = document.getElementById("jobs-message");
const refreshButton = document.getElementById("refresh-jobs");

function formatSalary(salary) {
    if (!salary || typeof salary !== "object") {
        return "Salary not specified";
    }

    const min = Number(salary.min);
    const max = Number(salary.max);

    if (!Number.isFinite(min) || !Number.isFinite(max)) {
        return "Salary not specified";
    }

    return `${(min / 100000).toFixed(1)}–${(max / 100000).toFixed(1)} LPA`;
}

function createJobCard(job) {
    const card = document.createElement("article");
    card.className = "job-card";

    const title = document.createElement("h3");
    title.textContent = job.title || "Untitled Job";

    const company = document.createElement("p");
    company.className = "company";
    company.textContent = job.company || "Company not specified";

    const meta = document.createElement("div");
    meta.className = "job-meta";

    [job.location, job.jobType].filter(Boolean).forEach(value => {
        const tag = document.createElement("span");
        tag.className = "tag";
        tag.textContent = value;
        meta.appendChild(tag);
    });

    const salary = document.createElement("p");
    salary.className = "salary";
    salary.textContent = formatSalary(job.salary);

    const description = document.createElement("p");
    description.className = "job-description";
    description.textContent = job.description || "No description provided.";

    const skills = document.createElement("p");
    skills.className = "skills";
    const skillList = Array.isArray(job.skills) ? job.skills : [];
    skills.textContent = "Skills: " + (skillList.join(", ") || "Not specified");

    card.append(title, company, meta, salary, description, skills);

    return card;
}

async function loadJobs() {
    jobsContainer.replaceChildren();
    jobsMessage.textContent = "Loading jobs...";

    try {
        const response = await fetch(`${API_BASE}/api/jobs`);

        if (!response.ok) {
            throw new Error(`Server returned ${response.status}`);
        }

        const jobs = await response.json();

        if (!Array.isArray(jobs) || jobs.length === 0) {
            jobsMessage.textContent = "No jobs available yet. Add jobs to MongoDB first.";
            return;
        }

        jobsMessage.textContent = `${jobs.length} job(s) found.`;

        jobs.forEach(job => {
            jobsContainer.appendChild(createJobCard(job));
        });
    } catch (error) {
        jobsMessage.textContent =
            "Could not load jobs. Make sure Flask is running on port 5000.";
        console.error("Job loading error:", error);
    }
}

refreshButton.addEventListener("click", loadJobs);

const salaryForm = document.getElementById("salary-form");
const salaryMessage = document.getElementById("salary-message");
const salaryResult = document.getElementById("salary-result");

salaryForm.addEventListener("submit", async event => {
    event.preventDefault();

    salaryResult.hidden = true;
    salaryMessage.textContent = "Predicting salary...";

    const experience = Number(document.getElementById("experience").value);
    const skillsCount = Number(document.getElementById("skills-count").value);

    if (
        !Number.isFinite(experience) ||
        !Number.isFinite(skillsCount) ||
        experience < 0 ||
        skillsCount < 0
    ) {
        salaryMessage.textContent = "Please enter valid non-negative numbers.";
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/api/predict-salary`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                experience: experience,
                skills_count: skillsCount
            })
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Salary prediction failed.");
        }

        salaryMessage.textContent = "";
        salaryResult.replaceChildren();

        const amount = document.createElement("div");
        amount.textContent = new Intl.NumberFormat("en-IN", {
            style: "currency",
            currency: "INR",
            maximumFractionDigits: 0
        }).format(result.predicted_salary);

        const note = document.createElement("small");
        note.textContent = "Estimated salary based on the current job dataset.";

        salaryResult.append(amount, note);
        salaryResult.hidden = false;
    } catch (error) {
        salaryMessage.textContent = error.message;
        console.error("Salary prediction error:", error);
    }
});

loadJobs();
