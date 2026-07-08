import { useEffect, useState } from "react";
import {
  API_BASE_URL,
  DASHBOARD_REFRESH_INTERVAL_SECONDS,
} from "./config";
import "./App.css";

function App() {
  const [shipments, setShipments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");
  const [lastRefresh, setLastRefresh] = useState("");

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

  useEffect(() => {
    loadShipments();

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
        <h1>Shipment Tracking Dashboard</h1>
        <p className="description">
          Vista ejecutiva DEV para seguimiento de mercancías, temperatura,
          alertas logísticas y estado operativo desde FastAPI y PostgreSQL local.
        </p>
        <p className="info">
          Refresco automático cada {DASHBOARD_REFRESH_INTERVAL_SECONDS} segundos.
          {lastRefresh && ` Última actualización: ${lastRefresh}.`}
        </p>
      </section>

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
                        <span className="alert">{shipment.alert_status}</span>
                      </td>
                      <td className="event">{shipment.last_logistic_event}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        </>
      )}
    </main>
  );
}

export default App;
