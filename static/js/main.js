const activityCatalog = JSON.parse(document.getElementById("activity-catalog-data").textContent);
const modulos = activityCatalog.map((item) => ({ cod: item.cod, nombre: item.nombre }));
const moduloRaMap = Object.fromEntries(
    activityCatalog.map((item) => [item.cod, item.ras])
);

const maxActividades = 8;
const actividadesContainer = document.getElementById("actividades-container");
const agregarActividadBtn = document.getElementById("agregar-actividad");

function buildModuloOptions(selectedCod = "") {
            const baseOption = `<option value="" ${selectedCod ? "" : "selected"}>Seleccionar módulo...</option>`;
            const moduloOptions = modulos.map((modulo) => {
                const selected = modulo.cod === selectedCod ? "selected" : "";
                return `<option value="${modulo.cod}" ${selected}>${modulo.nombre} (${modulo.cod})</option>`;
            }).join("");
            return baseOption + moduloOptions;
        }

function buildRaOptions(moduloCod, selectedRaId = "") {
    const ras = moduloRaMap[moduloCod] || [];
    const baseOption = '<option value="">Selecciona un R.A</option>';
    const options = ras.map((ra) => {
        const selected = String(ra.id) === String(selectedRaId) ? "selected" : "";
        return `<option value="${ra.id}" ${selected}>${ra.codigo} - ${ra.descripcion}</option>`;
    }).join("");
    return baseOption + options;
}

function crearFilaActividad(index) {
    const moduloInicial = "";
    const fila = document.createElement("div");
    fila.className = "row g-3 border rounded p-3";
    fila.dataset.index = index;
    fila.innerHTML = `
                <div class="col-md-5">
                    <label for="actividad_formativa_${index}" class="form-label">Actividad formativa desarrollada</label>
                    <textarea class="form-control" id="actividad_formativa_${index}" name="actividad_formativa_${index}" rows="2" required></textarea>
                </div>
                <div class="col-md-3">
                    <label for="modulo_profesional_${index}" class="form-label">Código módulo profesional</label>
                    <select class="form-select modulo-select" id="modulo_profesional_${index}" name="modulo_profesional_${index}" required>
                        ${buildModuloOptions(moduloInicial)}
                    </select>
                </div>
                <div class="col-md-4">
                    <label for="ra_${index}" class="form-label">R.A</label>
                    <select class="form-select ra-select" id="ra_${index}" name="ra_${index}" required>
                        ${buildRaOptions(moduloInicial)}
                    </select>
                </div>
            `;

    const moduloSelect = fila.querySelector(".modulo-select");
    const raSelect = fila.querySelector(".ra-select");
    moduloSelect.addEventListener("change", (event) => {
        raSelect.innerHTML = buildRaOptions(event.target.value);
    });

    return fila;
}

function actualizarEstadoBotonActividades() {
    const total = actividadesContainer.children.length;
    agregarActividadBtn.disabled = total >= maxActividades;
}

function agregarActividad() {
    const totalActual = actividadesContainer.children.length;
    if (totalActual >= maxActividades) {
        return;
    }
    const nuevoIndice = totalActual + 1;
    actividadesContainer.appendChild(crearFilaActividad(nuevoIndice));
    actualizarEstadoBotonActividades();
}

agregarActividadBtn.addEventListener("click", agregarActividad);
agregarActividad();

document.getElementById("documento-form").addEventListener("submit", async (event) => {
    event.preventDefault();

    const alumno = {
        nombre: document.getElementById("alumno-nombre").value,
        apellidos: document.getElementById("alumno-apellidos").value,
        curso_academico: [
            document.getElementById("alumno-curso-inicio").value,
            document.getElementById("alumno-curso-fin").value
        ].join("/"),
        email: document.getElementById("alumno-email").value,
        num_convenio: document.getElementById("alumno-num-convenio").value,
        num_anexo: document.getElementById("alumno-num-anexo").value
    };

    const centro = {
        nombre: document.getElementById("centro-nombre").value,
        nombre_tutor: document.getElementById("centro-nombre-tutor").value,
        apellidos_tutor: document.getElementById("centro-apellidos-tutor").value,
        email_tutor: document.getElementById("tutor-email").value
    };

    const periodo_seguimiento_inicio = document.getElementById("periodo-seguimiento-inicio").value;
    const periodo_seguimiento_fin = document.getElementById("periodo-seguimiento-fin").value;

    const activity_catalog = Array.from(actividadesContainer.children).map((fila) => {
        const id = `actividad_formativa_${fila.dataset.index}`;
        const descripcion = fila.querySelector("textarea").value;
        const cod_modulo = fila.querySelector(".modulo-select").value;
        const cod_ra = fila.querySelector(".ra-select").value;
        return { id, descripcion, cod_modulo, cod_ra };
    });

    const payload = {
        alumno: alumno,
        centro: centro,
        periodo_seguimiento_inicio: periodo_seguimiento_inicio,
        periodo_seguimiento_fin: periodo_seguimiento_fin,
        activity_catalog: activity_catalog
    };

    console.log("Payload a enviar para generación:", payload);

    try {
        const response = await fetch("/generate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Error al generar documento");
        }

        const result = await response.json();
        alert("Documento generado correctamente");
        console.log("Respuesta del servidor:", result);
        document.getElementById("mensaje-exito").textContent = "Datos guardados y documento generado";
        document.getElementById("mensaje-exito").classList.add("text-success", "border", "border-success", "p-2");

        setTimeout(() => {
            document.getElementById("mensaje-exito").textContent = "";
            document.getElementById("mensaje-exito").classList.remove("text-success", "border", "border-success", "p-2");
        }, 3000);
    } catch (error) {
        console.error(error);
        alert("Error al generar documento");
        document.getElementById("mensaje-exito").textContent = "Error al guardar o generar";
        document.getElementById("mensaje-exito").classList.add("text-danger", "border", "border-danger", "p-2");
        setTimeout(() => {
            document.getElementById("mensaje-exito").textContent = "";
            document.getElementById("mensaje-exito").classList.remove("text-danger", "border", "border-danger", "p-2");
        }, 3000);
    }
});
