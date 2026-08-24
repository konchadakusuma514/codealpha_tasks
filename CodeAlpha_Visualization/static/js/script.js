// ==========================================================================
// AI Job Market & Career Intelligence Platform (v2.0 NextGen) JavaScript
// ==========================================================================

document.addEventListener("DOMContentLoaded", () => {
    initTheme();
    initSidebar();
    initTableSearch();
});

// -------------------------------------------------------------
// 1. Theme Manager (Dark / Light Mode with LocalStorage)
// -------------------------------------------------------------
function initTheme() {
    const savedTheme = localStorage.getItem("ai_market_theme") || "light";
    document.documentElement.setAttribute("data-theme", savedTheme);
    updateThemeIcon(savedTheme);

    const themeToggleBtn = document.getElementById("themeToggle");
    if (themeToggleBtn) {
        themeToggleBtn.addEventListener("click", () => {
            const currentTheme = document.documentElement.getAttribute("data-theme");
            const newTheme = currentTheme === "dark" ? "light" : "dark";
            
            document.documentElement.setAttribute("data-theme", newTheme);
            localStorage.setItem("ai_market_theme", newTheme);
            updateThemeIcon(newTheme);
        });
    }
}

function updateThemeIcon(theme) {
    const icon = document.getElementById("themeIcon");
    if (icon) {
        if (theme === "dark") {
            icon.classList.remove("fa-moon");
            icon.classList.add("fa-sun", "text-warning");
        } else {
            icon.classList.remove("fa-sun", "text-warning");
            icon.classList.add("fa-moon");
        }
    }
}

// -------------------------------------------------------------
// 2. Responsive Sidebar Toggle
// -------------------------------------------------------------
function initSidebar() {
    const toggleBtn = document.getElementById("sidebarToggle");
    const sidebar = document.querySelector(".sidebar");
    
    if (toggleBtn && sidebar) {
        toggleBtn.addEventListener("click", () => {
            sidebar.classList.toggle("show");
        });
        
        // Close on clicking outside
        document.addEventListener("click", (e) => {
            if (sidebar.classList.contains("show") && !sidebar.contains(e.target) && !toggleBtn.contains(e.target)) {
                sidebar.classList.remove("show");
            }
        });
    }
}

// -------------------------------------------------------------
// 3. Live Table Search Filter
// -------------------------------------------------------------
function initTableSearch() {
    const searchInput = document.getElementById("searchInput");
    const table = document.getElementById("dataTable");

    if (searchInput && table) {
        searchInput.addEventListener("keyup", function() {
            const filter = this.value.toLowerCase();
            const rows = table.querySelectorAll("tbody tr");

            rows.forEach(row => {
                const text = row.innerText.toLowerCase();
                row.style.display = text.includes(filter) ? "" : "none";
            });
        });
    }
}

// -------------------------------------------------------------
// 4. AI Career Copilot ("Aria") Chat Controller
// -------------------------------------------------------------
function toggleCopilot() {
    const panel = document.getElementById("copilotPanel");
    if (panel) {
        if (panel.style.display === "flex") {
            panel.style.display = "none";
        } else {
            panel.style.display = "flex";
            const input = document.getElementById("copilotInput");
            if (input) input.focus();
        }
    }
}

function openCopilot() {
    const panel = document.getElementById("copilotPanel");
    if (panel) {
        panel.style.display = "flex";
        const input = document.getElementById("copilotInput");
        if (input) input.focus();
    }
}

async function handleCopilotSubmit(e) {
    e.preventDefault();
    const input = document.getElementById("copilotInput");
    const query = input.value.trim();
    if (!query) return;

    appendChatMessage(query, "user");
    input.value = "";

    // Show typing indicator
    const typingId = appendTypingIndicator();

    try {
        const res = await fetch("/api/advisor", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query: query })
        });
        const data = await res.json();
        removeTypingIndicator(typingId);
        
        if (data.status === "success") {
            appendChatMessage(data.response, "bot");
        } else {
            appendChatMessage("Sorry, I encountered an issue processing your query.", "bot");
        }
    } catch (err) {
        removeTypingIndicator(typingId);
        appendChatMessage("Network error connecting to AI Advisor service.", "bot");
    }
}

function sendQuickPrompt(promptText) {
    const input = document.getElementById("copilotInput");
    if (input) {
        input.value = promptText;
        const form = input.closest("form");
        if (form) {
            form.dispatchEvent(new Event("submit", { cancelable: true }));
        }
    }
}

function appendChatMessage(text, sender) {
    const chatContainer = document.getElementById("copilotChat");
    if (!chatContainer) return;

    const bubble = document.createElement("div");
    bubble.className = `chat-bubble ${sender}-bubble`;
    
    // Format simple markdown bold and linebreaks
    let formatted = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    formatted = formatted.replace(/\n/g, '<br>');
    bubble.innerHTML = formatted;

    chatContainer.appendChild(bubble);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function appendTypingIndicator() {
    const chatContainer = document.getElementById("copilotChat");
    const id = "typing-" + Date.now();
    const bubble = document.createElement("div");
    bubble.id = id;
    bubble.className = "chat-bubble bot-bubble text-muted small";
    bubble.innerHTML = '<i class="fa-solid fa-spinner fa-spin me-1"></i> Aria is thinking...';
    chatContainer.appendChild(bubble);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    return id;
}

function removeTypingIndicator(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}