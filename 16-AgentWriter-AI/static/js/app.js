const runForm = document.getElementById("runForm");
const topicInput = document.getElementById("topicInput");
const runButton = document.getElementById("runButton");
const cancelButton = document.getElementById("cancelButton");
const newRunButton = document.getElementById("newRunButton");

const timeline = document.getElementById("timeline");
const activityEmpty = document.getElementById("activityEmpty");

const planList = document.getElementById("planList");
const planEmpty = document.getElementById("planEmpty");
const planMeta = document.getElementById("planMeta");
const taskCount = document.getElementById("taskCount");

const progressRing = document.getElementById("progressRing");
const progressText = document.getElementById("progressText");
const runBadge = document.getElementById("runBadge");

const articlePreview = document.getElementById("articlePreview");
const markdownOutput = document.getElementById("markdownOutput");

const previewTab = document.getElementById("previewTab");
const markdownTab = document.getElementById("markdownTab");

const copyButton = document.getElementById("copyButton");
const downloadButton = document.getElementById("downloadButton");

const healthDot = document.getElementById("healthDot");
const healthText = document.getElementById("healthText");
const toast = document.getElementById("toast");

let abortController = null;
let finalMarkdown = "";
let totalTasks = 0;
let completedTasks = 0;

const stageProgress = {
    router: 10,
    research: 25,
    orchestrator: 35,
    workers: 75,
    reducer: 100,
};


function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


function showToast(message) {
    toast.textContent = message;
    toast.classList.add("show");

    window.setTimeout(() => {
        toast.classList.remove("show");
    }, 2200);
}


function updateProgress(value) {
    const progress = Math.max(
        0,
        Math.min(100, Math.round(value)),
    );

    progressRing.style.setProperty(
        "--progress",
        progress,
    );

    progressText.textContent = `${progress}%`;
}


function resetInterface() {
    finalMarkdown = "";
    totalTasks = 0;
    completedTasks = 0;

    timeline.innerHTML = "";
    planList.innerHTML = "";

    activityEmpty.hidden = false;
    planEmpty.hidden = false;

    timeline.appendChild(activityEmpty);
    planList.appendChild(planEmpty);

    planMeta.innerHTML = "";
    planMeta.hidden = true;

    taskCount.textContent = "0 tasks";

    articlePreview.innerHTML = `
        <div class="empty-state">
            <div class="empty-icon">✎</div>
            <h3>Your article will appear here</h3>
            <p>
                The final result appears after every
                section is completed.
            </p>
        </div>
    `;

    markdownOutput.textContent = "";
    markdownOutput.hidden = true;
    articlePreview.hidden = false;

    previewTab.classList.add("active");
    markdownTab.classList.remove("active");

    copyButton.disabled = true;

    downloadButton.href = "#";
    downloadButton.classList.add("disabled");
    downloadButton.setAttribute(
        "aria-disabled",
        "true",
    );

    runBadge.textContent = "Ready";
    runBadge.className = "run-badge";

    updateProgress(0);
}


function setRunningState(isRunning) {
    topicInput.disabled = isRunning;
    runButton.disabled = isRunning;

    cancelButton.hidden = !isRunning;

    if (isRunning) {
        runBadge.textContent = "Running";
        runBadge.className = "run-badge running";
    }
}


function getStageElement(stageId) {
    return document.querySelector(
        `[data-stage-id="${stageId}"]`,
    );
}


function createStageElement(stageId) {
    const element = document.createElement("div");

    element.className = "timeline-item";
    element.dataset.stageId = stageId;

    element.innerHTML = `
        <div class="timeline-marker">
            <span></span>
        </div>

        <div class="timeline-content">
            <div class="timeline-title"></div>
            <div class="timeline-detail"></div>
        </div>
    `;

    timeline.appendChild(element);

    return element;
}


function updateStage(event) {
    activityEmpty.hidden = true;

    let element = getStageElement(event.id);

    if (!element) {
        element = createStageElement(event.id);
    }

    element.classList.remove(
        "running",
        "completed",
        "failed",
    );

    element.classList.add(
        event.status || "running",
    );

    const title = element.querySelector(
        ".timeline-title",
    );

    const detail = element.querySelector(
        ".timeline-detail",
    );

    title.textContent = event.label;
    detail.textContent = event.detail || "";

    if (
        event.status === "completed"
        && stageProgress[event.id] !== undefined
    ) {
        updateProgress(stageProgress[event.id]);
    }
}


function addSubstage(event) {
    activityEmpty.hidden = true;

    const element = document.createElement("div");

    element.className =
        "timeline-item substage completed";

    element.innerHTML = `
        <div class="timeline-marker">
            <span></span>
        </div>

        <div class="timeline-content">
            <div class="timeline-title">
                ${escapeHtml(event.label)}
            </div>

            <div class="timeline-detail">
                Completed
            </div>
        </div>
    `;

    timeline.appendChild(element);
}


function showRouting(event) {
    const modeLabels = {
        closed_book: "Evergreen topic",
        hybrid: "Research-assisted topic",
        open_book: "Current information topic",
    };

    const detail =
        modeLabels[event.mode]
        || event.mode;

    const element = getStageElement("router");

    if (element) {
        const detailElement = element.querySelector(
            ".timeline-detail",
        );

        detailElement.textContent =
            `${detail}. Research: ${
                event.needs_research
                    ? "required"
                    : "not required"
            }.`;
    }

    if (
        Array.isArray(event.queries)
        && event.queries.length
    ) {
        const queriesElement = document.createElement(
            "div",
        );

        queriesElement.className = "query-list";

        queriesElement.innerHTML = event.queries
            .map(
                query => `
                    <span>
                        ${escapeHtml(query)}
                    </span>
                `,
            )
            .join("");

        if (element) {
            element
                .querySelector(".timeline-content")
                .appendChild(queriesElement);
        }
    }
}


function showResearch(event) {
    if (!event.evidence?.length) {
        return;
    }

    const stage = getStageElement("research");

    if (!stage) {
        return;
    }

    const sources = document.createElement("div");
    sources.className = "source-list";

    sources.innerHTML = event.evidence
        .slice(0, 5)
        .map(source => `
            <a
                href="${escapeHtml(source.url)}"
                target="_blank"
                rel="noopener noreferrer"
            >
                ${escapeHtml(
                    source.title || source.url,
                )}
            </a>
        `)
        .join("");

    stage
        .querySelector(".timeline-content")
        .appendChild(sources);
}


function showPlan(plan) {
    planEmpty.hidden = true;
    planList.innerHTML = "";

    const tasks = plan.tasks || [];

    totalTasks = tasks.length;
    completedTasks = 0;

    taskCount.textContent =
        `${tasks.length} ${
            tasks.length === 1 ? "task" : "tasks"
        }`;

    planMeta.hidden = false;

    planMeta.innerHTML = `
        <div>
            <span>Audience</span>
            <strong>
                ${escapeHtml(plan.audience || "Developers")}
            </strong>
        </div>

        <div>
            <span>Format</span>
            <strong>
                ${escapeHtml(
                    (plan.blog_kind || "explainer")
                        .replaceAll("_", " "),
                )}
            </strong>
        </div>

        <div>
            <span>Tone</span>
            <strong>
                ${escapeHtml(plan.tone || "Technical")}
            </strong>
        </div>
    `;

    tasks.forEach((task, index) => {
        const item = document.createElement("article");

        item.className = "plan-item";
        item.dataset.taskId = String(task.id);

        const tags = [];

        if (task.requires_research) {
            tags.push("Research");
        }

        if (task.requires_citations) {
            tags.push("Citations");
        }

        if (task.requires_code) {
            tags.push("Code");
        }

        item.innerHTML = `
            <div class="plan-number">
                ${String(index + 1).padStart(2, "0")}
            </div>

            <div class="plan-content">
                <div class="plan-title-row">
                    <h3>
                        ${escapeHtml(task.title)}
                    </h3>

                    <span class="plan-status">
                        Waiting
                    </span>
                </div>

                <p>
                    ${escapeHtml(task.goal)}
                </p>

                <div class="plan-tags">
                    <span>
                        ${escapeHtml(task.target_words)}
                        words
                    </span>

                    ${tags.map(
                        tag => `
                            <span>
                                ${escapeHtml(tag)}
                            </span>
                        `,
                    ).join("")}
                </div>

                <div class="task-progress">
                    <span></span>
                </div>
            </div>
        `;

        planList.appendChild(item);
    });
}


function completeSection(event) {
    const taskElement = document.querySelector(
        `[data-task-id="${event.task_id}"]`,
    );

    if (taskElement) {
        taskElement.classList.add("completed");

        const status = taskElement.querySelector(
            ".plan-status",
        );

        status.textContent = "Completed";

        const progressBar = taskElement.querySelector(
            ".task-progress span",
        );

        progressBar.style.width = "100%";
    }

    completedTasks = event.completed || (
        completedTasks + 1
    );

    totalTasks = event.total || totalTasks;

    const workerProgress = totalTasks
        ? 35 + (
            completedTasks / totalTasks
        ) * 40
        : 35;

    updateProgress(workerProgress);

    const workerStage = getStageElement("workers");

    if (workerStage) {
        const detail = workerStage.querySelector(
            ".timeline-detail",
        );

        detail.textContent =
            `${completedTasks} of ${totalTasks} sections completed.`;
    }
}


function displayFinalResult(event) {
    finalMarkdown = event.markdown || "";

    markdownOutput.textContent = finalMarkdown;

    const rendered = marked.parse(finalMarkdown);

    articlePreview.innerHTML = DOMPurify.sanitize(
        rendered,
    );

    copyButton.disabled = false;

    downloadButton.href = event.download_url;
    downloadButton.classList.remove("disabled");
    downloadButton.setAttribute(
        "aria-disabled",
        "false",
    );

    runBadge.textContent = "Completed";
    runBadge.className = "run-badge completed";

    updateProgress(100);

    document
        .getElementById("resultCard")
        .scrollIntoView({
            behavior: "smooth",
            block: "start",
        });
}


function displayError(message) {
    runBadge.textContent = "Failed";
    runBadge.className = "run-badge failed";

    const errorItem = document.createElement("div");

    errorItem.className =
        "timeline-item failed";

    errorItem.innerHTML = `
        <div class="timeline-marker">
            <span></span>
        </div>

        <div class="timeline-content">
            <div class="timeline-title">
                Agent execution failed
            </div>

            <div class="timeline-detail">
                ${escapeHtml(message)}
            </div>
        </div>
    `;

    timeline.appendChild(errorItem);

    showToast("Agent execution failed");
}


function handleEvent(event) {
    switch (event.type) {
        case "run_started":
            runBadge.textContent = "Running";
            break;

        case "stage":
            updateStage(event);
            break;

        case "substage":
            addSubstage(event);
            break;

        case "routing":
            showRouting(event);
            break;

        case "research_complete":
            showResearch(event);
            break;

        case "plan":
            showPlan(event.plan || {});
            break;

        case "section_complete":
            completeSection(event);
            break;

        case "images_planned":
            showToast(
                `${event.count} visual${
                    event.count === 1 ? "" : "s"
                } planned`,
            );
            break;

        case "final":
            displayFinalResult(event);
            break;

        case "error":
            displayError(event.message);
            break;

        case "done":
            setRunningState(false);
            break;
    }
}


function parseSSEChunk(buffer) {
    const events = buffer.split("\n\n");
    const remaining = events.pop() || "";

    events.forEach(block => {
        const dataLines = block
            .split("\n")
            .filter(line => line.startsWith("data:"))
            .map(line => line.slice(5).trim());

        if (!dataLines.length) {
            return;
        }

        const rawData = dataLines.join("\n");

        try {
            const event = JSON.parse(rawData);
            handleEvent(event);
        } catch (error) {
            console.error(
                "Could not parse stream event:",
                rawData,
                error,
            );
        }
    });

    return remaining;
}


async function executeAgent(topic) {
    abortController = new AbortController();

    const response = await fetch("/api/run", {
        method: "POST",

        headers: {
            "Content-Type": "application/json",
        },

        body: JSON.stringify({
            topic,
        }),

        signal: abortController.signal,
    });

    if (!response.ok) {
        const message = await response.text();

        throw new Error(
            message || "Could not start the agent.",
        );
    }

    if (!response.body) {
        throw new Error(
            "Streaming is not supported by this browser.",
        );
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    let buffer = "";

    while (true) {
        const {
            done,
            value,
        } = await reader.read();

        if (done) {
            break;
        }

        buffer += decoder.decode(
            value,
            {
                stream: true,
            },
        );

        buffer = parseSSEChunk(buffer);
    }

    buffer += decoder.decode();

    if (buffer.trim()) {
        parseSSEChunk(`${buffer}\n\n`);
    }
}


runForm.addEventListener(
    "submit",
    async event => {
        event.preventDefault();

        const topic = topicInput.value.trim();

        if (topic.length < 3) {
            showToast(
                "Enter a more detailed topic.",
            );
            return;
        }

        resetInterface();
        setRunningState(true);

        activityEmpty.hidden = true;
        planEmpty.hidden = false;

        try {
            await executeAgent(topic);
        } catch (error) {
            if (error.name === "AbortError") {
                runBadge.textContent = "Stopped";
                runBadge.className =
                    "run-badge stopped";

                showToast(
                    "Generation stopped.",
                );
            } else {
                displayError(
                    error.message
                    || "Unexpected error.",
                );
            }
        } finally {
            setRunningState(false);
            abortController = null;
        }
    },
);


cancelButton.addEventListener(
    "click",
    () => {
        if (abortController) {
            abortController.abort();
        }
    },
);


newRunButton.addEventListener(
    "click",
    () => {
        if (abortController) {
            abortController.abort();
        }

        resetInterface();

        topicInput.disabled = false;
        topicInput.value = "";
        topicInput.focus();
    },
);


document
    .querySelectorAll("[data-topic]")
    .forEach(button => {
        button.addEventListener(
            "click",
            () => {
                topicInput.value =
                    button.dataset.topic || "";

                topicInput.focus();
            },
        );
    });


previewTab.addEventListener(
    "click",
    () => {
        previewTab.classList.add("active");
        markdownTab.classList.remove("active");

        articlePreview.hidden = false;
        markdownOutput.hidden = true;
    },
);


markdownTab.addEventListener(
    "click",
    () => {
        markdownTab.classList.add("active");
        previewTab.classList.remove("active");

        markdownOutput.hidden = false;
        articlePreview.hidden = true;
    },
);


copyButton.addEventListener(
    "click",
    async () => {
        if (!finalMarkdown) {
            return;
        }

        await navigator.clipboard.writeText(
            finalMarkdown,
        );

        showToast(
            "Markdown copied.",
        );
    },
);


downloadButton.addEventListener(
    "click",
    event => {
        if (
            downloadButton.classList.contains(
                "disabled",
            )
        ) {
            event.preventDefault();
        }
    },
);


async function checkHealth() {
    try {
        const response = await fetch(
            "/api/health",
        );

        if (!response.ok) {
            throw new Error("Server unavailable");
        }

        healthDot.classList.add("online");
        healthText.textContent = "Server online";
    } catch {
        healthDot.classList.remove("online");
        healthText.textContent = "Server offline";
    }
}


resetInterface();
checkHealth();