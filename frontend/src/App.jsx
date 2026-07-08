import { useEffect, useState } from "react";
import {
  API_BASE_URL,
  DASHBOARD_REFRESH_INTERVAL_SECONDS,
} from "./config";
import "./App.css";

const initialChangeRequestForm = {
  title: "",
  requester: "CIO",
  request_type: "FUNCTIONAL",
  priority: "MEDIUM",
  description: "",
  constraints: "DEV only. No secrets. No production. Pipeline and human review required.",
};

function App() {
  const [activeView, setActiveView] = useState("shipments");

  const [shipments, setShipments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");
  const [lastRefresh, setLastRefresh] = useState("");

  const [changeRequests, setChangeRequests] = useState([]);
  const [changeRequestForm, setChangeRequestForm] = useState(
    initialChangeRequestForm
  );
  const [factoryMessage, setFactoryMessage] = useState("");

  async function loadShipments() {
    try {
      setLoading(true);
      setErrorMessage("");

      const response = await fetch(`${API_BASE_URL}/shipments`);

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const data = await response.json();
      setShipments(data);
      setLastRefresh(new Date().toLocaleTimeString());
    } catch (error) {
      setErrorMessage("No se han podido cargar los envíos desde la API.");
      console.error(error);
    } finally {
      setLoading(false);
    }
  }

  async function loadChangeRequests() {
    try {
      const response = await fetch(`${API_BASE_URL}/ai/change-requests`);

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const data = await response.json();
      setChangeRequests(data);
    } catch (error) {
      setFactoryMessage("No se han podido cargar las solicitudes IA.");
      console.error(error);
    }
  }

  async function createChangeRequest(event) {
    event.preventDefault();

    try {
      setFactoryMessage("");

      const response = await fetch(`${API_BASE_URL}/ai/change-requests`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(changeRequestForm),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      setChangeRequestForm(initialChangeRequestForm);
      setFactoryMessage("Solicitud registrada correctamente para revisión DEV.");
      await loadChangeRequests();
    } catch (error) {
      setFactoryMessage("No se ha podido registrar la solicitud.");
      console.error(error);
    }
  }

  function updateChangeRequestForm(event) {
    const { name, value } = event.target;

    setChangeRequestForm((currentForm) => ({
      ...currentForm,
      [name]: value,
    }));
  }

  useEffect(() => {
    loadShipments();
    loadChangeRequests();

    const intervalId = setInterval(
      loadShipments,
      DASHBOARD_REFRESH_INTERVAL_SECONDS * 1000
    );

    return () => clearInterval(intervalId);
  }, []);

  const totalShipments = shipments.length;

  const inTransitShipments = shipments.filter(
    (shipment) => shipment.status === "IN_TRANSIT"
  ).length;

  const activeAlerts = shipments.filter(
    (shipment) => shipment.alert_status !== "NORMAL"
  ).length;

  const averageTemperature =
    shipments.length > 0
      ? shipments.reduce(
          (sum, shipment) => sum + Number(shipment.temperature_current || 0),
          0
        ) / shipments.length
      : 0;

  return (
    <main className="page">
      <section className="hero">
        <p className="eyebrow">DEV Intelligence Factory Lab</p>
        <h1>
          {activeView === "shipments"
            ? "Shipment Tracking Dashboard"
            : "AI Intelligent Factory"}
        </h1>
        <p className="description">
          {activeView === "shipments"
            ? "Vista ejecutiva DEV para seguimiento de mercancías, temperatura, alertas logísticas y estado operativo desde FastAPI y PostgreSQL local."
            : "Canal gobernado para registrar solicitudes funcionales o técnicas que podrá procesar un agente IA local bajo control DevOps/DevSecOps."}
        </p>
        <p className="info">
          Refresco automático cada {DASHBOARD_REFRESH_INTERVAL_SECONDS} segundos.
          {lastRefresh && ` Última actualización: ${lastRefresh}.`}
        </p>

        <div className="view-tabs">
          <button
            className={activeView === "shipments" ? "tab active" : "tab"}
            onClick={() => setActiveView("shipments")}
          >
            Shipment Dashboard
          </button>
          <button
            className={activeView === "factory" ? "tab active" : "tab"}
            onClick={() => setActiveView("factory")}
          >
            AI Intelligent Factory
          </button>
        </div>
      </section>

      {activeView === "shipments" && (
        <>
          {loading && <p className="info">Cargando envíos...</p>}

          {errorMessage && <p className="error">{errorMessage}</p>}

          {!loading && !errorMessage && (
            <>
              <section className="summary-grid">
                <article className="summary-card">
                  <span className="summary-label">Total mercancías</span>
                  <strong>{totalShipments}</strong>
                  <p>Envíos monitorizados en DEV</p>
                </article>

                <article className="summary-card">
                  <span className="summary-label">En tránsito</span>
                  <strong>{inTransitShipments}</strong>
                  <p>Mercancías actualmente en movimiento</p>
                </article>

                <article className="summary-card">
                  <span className="summary-label">Alertas activas</span>
                  <strong>{activeAlerts}</strong>
                  <p>Envíos con estado distinto de NORMAL</p>
                </article>

                <article className="summary-card">
                  <span className="summary-label">Temperatura media</span>
                  <strong>{averageTemperature.toFixed(1)} ºC</strong>
                  <p>Media calculada sobre los envíos actuales</p>
                </article>
              </section>

              <section className="card">
                <div className="card-header">
                  <h2>Mercancías monitorizadas</h2>
                  <button onClick={loadShipments}>Refrescar</button>
                </div>

                <div className="table-wrapper">
                  <table>
                    <thead>
                      <tr>
                        <th>Cliente</th>
                        <th>Destino</th>
                        <th>Ubicación</th>
                        <th>Estado</th>
                        <th>Servicio</th>
                        <th>ETA</th>
                        <th>Temperatura</th>
                        <th>Alerta</th>
                        <th>Último evento</th>
                      </tr>
                    </thead>

                    <tbody>
                      {shipments.map((shipment) => (
                        <tr key={shipment.id}>
                          <td>{shipment.client}</td>
                          <td>{shipment.destination}</td>
                          <td>{shipment.location}</td>
                          <td>
                            <span className="status">{shipment.status}</span>
                          </td>
                          <td>{shipment.transport_service}</td>
                          <td>{shipment.eta}</td>
                          <td className="temperature">
                            {shipment.temperature_current} ºC
                          </td>
                          <td>
                            <span className="alert">
                              {shipment.alert_status}
                            </span>
                          </td>
                          <td className="event">
                            {shipment.last_logistic_event}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </section>
            </>
          )}
        </>
      )}

      {activeView === "factory" && (
        <section className="factory-layout">
          <form className="card factory-form" onSubmit={createChangeRequest}>
            <div className="card-header">
              <h2>Nueva solicitud para agente IA</h2>
            </div>

            <label>
              Título
              <input
                name="title"
                value={changeRequestForm.title}
                onChange={updateChangeRequestForm}
                placeholder="Ej. Añadir logo corporativo al dashboard"
                required
              />
            </label>

            <label>
              Solicitante
              <input
                name="requester"
                value={changeRequestForm.requester}
                onChange={updateChangeRequestForm}
                required
              />
            </label>

            <div className="form-grid">
              <label>
                Tipo
                <select
                  name="request_type"
                  value={changeRequestForm.request_type}
                  onChange={updateChangeRequestForm}
                >
                  <option value="FUNCTIONAL">Funcional</option>
                  <option value="TECHNICAL">Técnico</option>
                  <option value="INFRASTRUCTURE">Infraestructura</option>
                  <option value="DEPENDENCY">Dependencia</option>
                </select>
              </label>

              <label>
                Prioridad
                <select
                  name="priority"
                  value={changeRequestForm.priority}
                  onChange={updateChangeRequestForm}
                >
                  <option value="LOW">Baja</option>
                  <option value="MEDIUM">Media</option>
                  <option value="HIGH">Alta</option>
                  <option value="CRITICAL">Crítica</option>
                </select>
              </label>
            </div>

            <label>
              Descripción
              <textarea
                name="description"
                value={changeRequestForm.description}
                onChange={updateChangeRequestForm}
                placeholder="Describe la petición del CIO o del equipo técnico."
                rows="5"
                required
              />
            </label>

            <label>
              Restricciones
              <textarea
                name="constraints"
                value={changeRequestForm.constraints}
                onChange={updateChangeRequestForm}
                rows="4"
              />
            </label>

            <button type="submit">Registrar solicitud</button>

            {factoryMessage && <p className="info">{factoryMessage}</p>}
          </form>

          <section className="card">
            <div className="card-header">
              <h2>Solicitudes registradas</h2>
              <button onClick={loadChangeRequests}>Actualizar</button>
            </div>

            <div className="request-list">
              {changeRequests.map((request) => (
                <article className="request-item" key={request.id}>
                  <div>
                    <span className="summary-label">
                      {request.request_type} · {request.priority}
                    </span>
                    <h3>{request.title}</h3>
                    <p>{request.description}</p>
                    <small>{request.constraints}</small>
                  </div>
                  <span className="status">{request.status}</span>
                </article>
              ))}
            </div>
          </section>
        </section>
      )}
    </main>
  );
}

export default App;
