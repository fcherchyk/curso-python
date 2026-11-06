// Chapter tabs, CodeMirror editor and autosave.
(() => {
  const main = document.querySelector("main.chapter");
  if (!main) return;
  const chapterId = main.dataset.chapter;
  const useTabs = main.dataset.tabs === "yes";
  let editor = null;

  // ---------- Tabs ----------
  const tabs = [...document.querySelectorAll(".tab")];
  const storageKey = `tab:${chapterId}`;

  function show(name, { remember = true } = {}) {
    for (const t of tabs) {
      const active = t.dataset.tab === name;
      t.setAttribute("aria-selected", String(active));
      document.getElementById(`panel-${t.dataset.tab}`).hidden = !active;
    }
    if (name === "code") startEditor();
    if (remember) {
      history.replaceState(null, "", `#${name}`);
      try { sessionStorage.setItem(storageKey, name); } catch {}
    }
  }

  tabs.forEach((t) => t.addEventListener("click", () => show(t.dataset.tab)));
  document.addEventListener("click", (e) => {
    const target = e.target.closest("[data-go-to]");
    if (!target) return;
    show(target.dataset.goTo);
    window.scrollTo({ top: 0 });
  });

  let initial = location.hash.slice(1);
  if (!tabs.some((t) => t.dataset.tab === initial)) {
    try { initial = sessionStorage.getItem(storageKey) || "lesson"; } catch { initial = "lesson"; }
  }
  // CodeMirror loads with defer: wait for load before creating the editor.
  window.addEventListener("load", () => show(initial, { remember: false }));
  window.addEventListener("hashchange", () => {
    const name = location.hash.slice(1);
    if (tabs.some((t) => t.dataset.tab === name)) show(name);
  });

  // ---------- Editor ----------
  const saveStatus = document.getElementById("save-status");
  let timer = null;

  function save() {
    const data = new FormData();
    data.append("code", currentCode());
    fetch(`/c/${chapterId}/code`, { method: "POST", body: data })
      .then((r) => { saveStatus.textContent = r.ok ? "Saved" : "Could not save"; })
      .catch(() => { saveStatus.textContent = "Could not save"; });
  }

  function currentCode() {
    return editor ? editor.getValue() : document.getElementById("editor").value;
  }

  function startEditor() {
    if (editor || !window.CodeMirror) return;
    const form = document.getElementById("code-form");
    editor = CodeMirror.fromTextArea(document.getElementById("editor"), {
      mode: main.dataset.mode || "python",
      lineNumbers: true,
      indentUnit: 4,
      tabSize: 4,
      indentWithTabs: useTabs,
      matchBrackets: true,
      autoCloseBrackets: true,
      styleActiveLine: true,
      extraKeys: {
        Tab: (cm) => cm.somethingSelected()
          ? cm.indentSelection("add")
          : cm.replaceSelection(useTabs ? "\t" : " ".repeat(cm.getOption("indentUnit"))),
        "Shift-Tab": (cm) => cm.indentSelection("subtract"),
        "Cmd-Enter": () => htmx.trigger(form, "submit"),
        "Ctrl-Enter": () => htmx.trigger(form, "submit"),
        "Cmd-/": "toggleComment",
      },
    });
    editor.on("change", () => {
      saveStatus.textContent = "Unsaved…";
      clearTimeout(timer);
      timer = setTimeout(save, 800);
    });
  }

  // HTMX sends the textarea: make sure it holds the editor's latest content.
  document.body.addEventListener("htmx:configRequest", (e) => {
    if (e.detail.elt.id === "code-form") {
      e.detail.parameters.code = currentCode();
      saveStatus.textContent = "Saved";
      clearTimeout(timer);
    }
  });

  document.getElementById("reset-button").addEventListener("click", async () => {
    if (!confirm("Replace your code with the exercise's starter code?")) return;
    const text = await fetch(`/c/${chapterId}/starter`).then((r) => r.text());
    if (editor) editor.setValue(text);
    else document.getElementById("editor").value = text;
    save();
  });
})();
