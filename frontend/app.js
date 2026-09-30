const API = (window.API_BASE_URL || "http://localhost:8000").replace(/\/$/, "");

let conversationId = null;
let editingId = null;


// ==============================
// 공통 API 요청
// ==============================

async function request(path, options = {}) {
    const r = await fetch(API + path, {
        headers: {
            "Content-Type": "application/json",
            ...(options.headers || {})
        },
        ...options
    });

    if (!r.ok) {
        let d = await r.text();

        try {
            d = JSON.parse(d).detail || d;
        } catch {}

        throw new Error(d);
    }

    return r.json();
}


// ==============================
// 채팅 메시지 표시
// ==============================

function addMessage(role, content, extra = "") {
    const e = document.createElement("div");

    e.className = `message ${role} ${extra}`;

    if (role === "assistant") {
        const safe = document.createElement("div");
        safe.textContent = content;

        let formatted = safe.innerHTML;

        // **텍스트**를 굵게 표시
        formatted = formatted.replace(
            /\*\*(.*?)\*\*/g,
            "<strong>$1</strong>"
        );

        // AI 답변의 줄바꿈 유지
        formatted = formatted.replace(/\n/g, "<br>");

        e.innerHTML = formatted;
    } else {
        e.textContent = content;
    }

    messages.appendChild(e);
    messages.scrollTop = messages.scrollHeight;

    return e;
}


// ==============================
// 데이터 요약
// ==============================

async function loadSummary() {
    try {
        const s = await request("/api/data/summary");
        const m = s.metrics;

        summary.innerHTML = `
            <div class="metric">
                <b>기간</b>
                <span>${s.period || "-"}</span>
            </div>

            <div class="metric">
                <b>개수</b>
                <span>${s.count}개</span>
            </div>

            <div class="metric">
                <b>평균</b>
                <span>${m.average ?? "-"}°C</span>
            </div>

            <div class="metric">
                <b>최고</b>
                <span>${m.max ?? "-"}°C</span>
            </div>

            <div class="metric">
                <b>최저</b>
                <span>${m.min ?? "-"}°C</span>
            </div>

            <div class="metric">
                <b>최근 추세</b>
                <span>${s.trend}</span>
            </div>
        `;
    } catch (e) {
        summary.innerHTML = `<p class="error">${e.message}</p>`;
    }
}


// ==============================
// 데이터 목록
// ==============================

async function loadData() {
    try {
        const rows = await request("/api/data");

        dataRows.innerHTML = "";

        rows
            .slice(-30)
            .reverse()
            .forEach(x => {

                const tr = document.createElement("tr");

                // 날짜
                const dateTd = document.createElement("td");
                dateTd.textContent = x.date;

                // 값
                const valueTd = document.createElement("td");
                valueTd.textContent = `${x.value}°C`;

                // 메모
                const memoTd = document.createElement("td");
                memoTd.textContent = x.memo || "";

                // 관리
                const manageTd = document.createElement("td");


                // 수정 버튼
                const editButton = document.createElement("button");

                editButton.textContent = "수정";
                editButton.className = "edit";

                editButton.onclick = () => {
                    editingId = x.id;

                    date.value = x.date;
                    value.value = x.value;
                    memo.value = x.memo || "";

                    const submitButton =
                        dataForm.querySelector('button[type="submit"]');

                    submitButton.textContent = "수정 완료";

                    dataForm.scrollIntoView({
                        behavior: "smooth",
                        block: "center"
                    });
                };


                // 삭제 버튼
                const deleteButton = document.createElement("button");

                deleteButton.textContent = "삭제";
                deleteButton.className = "danger";

                deleteButton.onclick = async () => {

                    if (!confirm(`${x.date} 데이터를 삭제할까요?`)) {
                        return;
                    }

                    try {
                        await request(
                            `/api/data/${x.id}`,
                            {
                                method: "DELETE"
                            }
                        );

                        // 수정 중이던 데이터를 삭제했다면
                        // 수정 모드 해제
                        if (editingId === x.id) {
                            cancelEdit();
                        }

                        await loadData();
                        await loadSummary();

                    } catch (e) {
                        alert(`삭제 실패: ${e.message}`);
                    }
                };


                manageTd.appendChild(editButton);
                manageTd.appendChild(
                    document.createTextNode(" ")
                );
                manageTd.appendChild(deleteButton);

                tr.appendChild(dateTd);
                tr.appendChild(valueTd);
                tr.appendChild(memoTd);
                tr.appendChild(manageTd);

                dataRows.appendChild(tr);
            });

    } catch (e) {

        dataRows.innerHTML = `
            <tr>
                <td colspan="4" class="error">
                    ${e.message}
                </td>
            </tr>
        `;
    }
}


// ==============================
// 수정 모드 종료
// ==============================

function cancelEdit() {
    editingId = null;

    dataForm.reset();

    const submitButton =
        dataForm.querySelector('button[type="submit"]');

    submitButton.textContent = "추가";
}


// ==============================
// 데이터 추가 / 수정
// ==============================

dataForm.onsubmit = async e => {
    e.preventDefault();

    const payload = {
        date: date.value,
        value: Number(value.value),
        memo: memo.value
    };

    try {

        // 수정 모드
        if (editingId) {

            await request(
                `/api/data/${editingId}`,
                {
                    method: "PUT",
                    body: JSON.stringify(payload)
                }
            );

        }

        // 추가 모드
        else {

            await request(
                "/api/data",
                {
                    method: "POST",
                    body: JSON.stringify(payload)
                }
            );

        }

        cancelEdit();

        await loadData();
        await loadSummary();

    } catch (e) {
        alert(`저장 실패: ${e.message}`);
    }
};


// ==============================
// 대화 목록
// ==============================

async function loadConversations() {
    try {
        const a = await request("/api/conversations");

        conversationList.innerHTML =
            a.length ? "" : "저장된 대화가 없습니다.";

        a.slice()
            .reverse()
            .forEach(x => {

                const row = document.createElement("div");
                row.className = "conv";

                const t = document.createElement("div");
                t.className = "conv-title";
                t.textContent = x.title || "새 대화";

                // 저장된 대화 불러오기
                t.onclick = async () => {
                    try {
                        const c = await request(
                            `/api/conversations/${x.id}`
                        );

                        conversationId = c.id;
                        messages.innerHTML = "";

                        (c.messages || []).forEach(m => {
                            addMessage(
                                m.role,
                                m.content
                            );
                        });

                    } catch (e) {
                        alert(`대화 불러오기 실패: ${e.message}`);
                    }
                };


                // 대화 삭제
                const b = document.createElement("button");

                b.textContent = "삭제";
                b.className = "danger";

                b.onclick = async () => {

                    if (!confirm("이 대화를 삭제할까요?")) {
                        return;
                    }

                    try {
                        await request(
                            `/api/conversations/${x.id}`,
                            {
                                method: "DELETE"
                            }
                        );

                        // 현재 보고 있던 대화를 삭제한 경우
                        if (conversationId === x.id) {
                            conversationId = null;
                            messages.innerHTML = "";

                            addMessage(
                                "assistant",
                                "저장된 서울 기온 데이터에 대해 질문해보세요."
                            );
                        }

                        await loadConversations();

                    } catch (e) {
                        alert(`대화 삭제 실패: ${e.message}`);
                    }
                };

                row.append(t, b);
                conversationList.appendChild(row);
            });

    } catch (e) {
        conversationList.innerHTML =
            `<p class="error">${e.message}</p>`;
    }
}


// ==============================
// AI 채팅
// ==============================

send.onclick = async () => {

    const q = question.value.trim();

    if (!q) {
        return;
    }

    addMessage("user", q);

    question.value = "";

    const loading = addMessage(
        "assistant",
        "답변을 생성하는 중...",
        "loading"
    );

    try {

        const r = await request(
            "/api/chat",
            {
                method: "POST",
                body: JSON.stringify({
                    message: q,
                    conversation_id: conversationId
                })
            }
        );

        loading.remove();

        addMessage(
            "assistant",
            r.answer
        );

        conversationId = r.conversation_id;

        await loadConversations();

    } catch (e) {

        loading.textContent =
            `오류: ${e.message}`;

        loading.className =
            "message assistant error";
    }
};


// Enter로 메시지 전송
question.addEventListener(
    "keydown",
    e => {
        if (e.key === "Enter") {
            e.preventDefault();
            send.click();
        }
    }
);


// ==============================
// 최초 화면 로딩
// ==============================

Promise.all([
    loadSummary(),
    loadData(),
    loadConversations()
]);