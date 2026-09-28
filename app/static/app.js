// Pestañas, editor CodeMirror y autoguardado del capítulo.
(() => {
  const main = document.querySelector("main.capitulo");
  if (!main) return;
  const idCap = main.dataset.cap;
  let editor = null;

  // ---------- Pestañas ----------
  const tabs = [...document.querySelectorAll(".tab")];
  const clave = `tab:${idCap}`;

  function mostrar(nombre, { guardar = true } = {}) {
    for (const t of tabs) {
      const activa = t.dataset.tab === nombre;
      t.setAttribute("aria-selected", String(activa));
      document.getElementById(`panel-${t.dataset.tab}`).hidden = !activa;
    }
    if (nombre === "codigo") iniciarEditor();
    if (guardar) {
      history.replaceState(null, "", `#${nombre}`);
      try { sessionStorage.setItem(clave, nombre); } catch {}
    }
  }

  tabs.forEach((t) => t.addEventListener("click", () => mostrar(t.dataset.tab)));
  document.addEventListener("click", (e) => {
    const destino = e.target.closest("[data-ir-a]");
    if (!destino) return;
    mostrar(destino.dataset.irA);
    window.scrollTo({ top: 0 });
  });

  let inicial = location.hash.slice(1);
  if (!tabs.some((t) => t.dataset.tab === inicial)) {
    try { inicial = sessionStorage.getItem(clave) || "leccion"; } catch { inicial = "leccion"; }
  }
  // CodeMirror se carga con defer: esperamos al load para poder crear el editor.
  window.addEventListener("load", () => mostrar(inicial, { guardar: false }));
  window.addEventListener("hashchange", () => {
    const nombre = location.hash.slice(1);
    if (tabs.some((t) => t.dataset.tab === nombre)) mostrar(nombre);
  });

  // ---------- Editor ----------
  const indicador = document.getElementById("guardado");
  let temporizador = null;

  function guardar() {
    const datos = new FormData();
    datos.append("codigo", codigoActual());
    fetch(`/c/${idCap}/codigo`, { method: "POST", body: datos })
      .then((r) => { indicador.textContent = r.ok ? "Guardado" : "No se pudo guardar"; })
      .catch(() => { indicador.textContent = "No se pudo guardar"; });
  }

  function codigoActual() {
    return editor ? editor.getValue() : document.getElementById("editor").value;
  }

  function iniciarEditor() {
    if (editor || !window.CodeMirror) return;
    const form = document.getElementById("form-codigo");
    editor = CodeMirror.fromTextArea(document.getElementById("editor"), {
      mode: "python",
      lineNumbers: true,
      indentUnit: 4,
      tabSize: 4,
      indentWithTabs: false,
      matchBrackets: true,
      autoCloseBrackets: true,
      styleActiveLine: true,
      extraKeys: {
        Tab: (cm) => cm.somethingSelected()
          ? cm.indentSelection("add")
          : cm.replaceSelection(" ".repeat(cm.getOption("indentUnit"))),
        "Shift-Tab": (cm) => cm.indentSelection("subtract"),
        "Cmd-Enter": () => htmx.trigger(form, "submit"),
        "Ctrl-Enter": () => htmx.trigger(form, "submit"),
        "Cmd-/": "toggleComment",
      },
    });
    editor.on("change", () => {
      indicador.textContent = "Sin guardar…";
      clearTimeout(temporizador);
      temporizador = setTimeout(guardar, 800);
    });
  }

  // HTMX manda el textarea: nos aseguramos de que tenga lo último del editor.
  document.body.addEventListener("htmx:configRequest", (e) => {
    if (e.detail.elt.id === "form-codigo") {
      e.detail.parameters.codigo = codigoActual();
      indicador.textContent = "Guardado";
      clearTimeout(temporizador);
    }
  });

  document.getElementById("boton-restaurar").addEventListener("click", async () => {
    if (!confirm("¿Reemplazar tu código por el código inicial del ejercicio?")) return;
    const texto = await fetch(`/c/${idCap}/inicial`).then((r) => r.text());
    if (editor) editor.setValue(texto);
    else document.getElementById("editor").value = texto;
    guardar();
  });
})();
