def get_css() -> str:
    return """
<style>
/* ── Sidebar ─────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: #EDEAD9;
    border-right: 1px solid #D5D0C0;
}
[data-testid="stSidebar"] hr {
    border-color: #C8C4B4;
    margin: 0.75rem 0;
}

/* ── Assistant bubble ────────────────────────────────────── */
[data-testid="stChatMessage"] {
    background-color: #EDEAD9;
    border-left: 3px solid #C8C4B4;
    border-radius: 12px;
    padding: 4px 8px;
    margin-bottom: 4px;
}

/* ── User bubble (custom HTML) ───────────────────────────── */
.user-row {
    display: flex;
    justify-content: flex-end;
    align-items: flex-start;
    gap: 10px;
    margin: 8px 0 12px 0;
    padding: 0 8px;
}
.user-bubble {
    background-color: rgba(45, 106, 79, 0.10);
    border: 1px solid rgba(45, 106, 79, 0.22);
    border-radius: 16px 4px 16px 16px;
    padding: 10px 14px;
    max-width: 75%;
    color: #1C1C1C;
    font-size: 0.95rem;
    line-height: 1.5;
    word-wrap: break-word;
}
.user-avatar {
    width: 36px;
    min-width: 36px;
    height: 36px;
    border-radius: 50%;
    background-color: #2D6A4F;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: 700;
    font-size: 0.85rem;
    margin-top: 2px;
}

/* ── Thought process expander ────────────────────────────── */
[data-testid="stExpander"] {
    background-color: #F0EDE0;
    border: 1px solid #D5D0C0 !important;
    border-radius: 8px !important;
    margin-top: 6px;
}
[data-testid="stExpander"] summary p {
    color: #7A7A6E;
    font-size: 0.78rem;
}

/* ── Thought process sections ────────────────────────────── */
.thought-section {
    margin-bottom: 10px;
}
.thought-label {
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 4px;
    padding: 2px 8px;
    border-radius: 4px;
    display: inline-block;
}
.thought-label-thinking {
    color: #5A4FCF;
    background-color: rgba(90, 79, 207, 0.08);
}
.thought-label-tool {
    color: #2D6A4F;
    background-color: rgba(45, 106, 79, 0.08);
}
.thought-label-result {
    color: #8B5E00;
    background-color: rgba(139, 94, 0, 0.08);
}
.thought-content {
    font-size: 0.82rem;
    color: #3A3A2E;
    line-height: 1.55;
    padding: 6px 10px;
    background-color: #F7F5ED;
    border-left: 2px solid #D5D0C0;
    border-radius: 0 6px 6px 0;
    white-space: pre-wrap;
    word-wrap: break-word;
}
.thought-divider {
    border: none;
    border-top: 1px dashed #D5D0C0;
    margin: 8px 0;
}

/* ── Chat input ──────────────────────────────────────────── */
[data-testid="stChatInput"] textarea {
    background-color: #EDEAD9 !important;
    border-radius: 12px !important;
    border-color: #C8C4B4 !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: #2D6A4F !important;
    box-shadow: none !important;
    outline: none !important;
}

/* ── Scrollbar ───────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #F5F2EB; }
::-webkit-scrollbar-thumb { background: #C8C4B4; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #2D6A4F; }
</style>
"""
