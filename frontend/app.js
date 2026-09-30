function formatMessage(content) {
    const div = document.createElement("div");
    div.textContent = content;

    let safe = div.innerHTML;

    // **텍스트** → 굵게
    safe = safe.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");

    // 줄바꿈 유지
    safe = safe.replace(/\n/g, "<br>");

    return safe;
}

function addMessage(role, content, extra = "") {
    const e = document.createElement("div");

    e.className = `message ${role} ${extra}`;

    if (role === "assistant") {
        e.innerHTML = formatMessage(content);
    } else {
        e.textContent = content;
    }

    messages.appendChild(e);
    messages.scrollTop = messages.scrollHeight;

    return e;
}