import { useEffect, useState } from "react";
import { API_BASE_URL } from "./config";
import "./App.css";

function App() {
  const [shipments, setShipments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");

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
    } catch (error) {
      setErrorMessage("No se han podido cargar los envíos desde la API.");
      console.error(error);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadShipments();
  }, []);

  return (
    <main className="page">
      <section className="hero">
        <p className="eyebrow">DEV Intelligence Factory Lab</p>
        <h1>Shipment Tracking Dashboard</h1>
        <p className="description">
          Dashboard DEV para visualizar el seguimiento de mercancías desde FastAPI y PostgreSQL local.
        </p>
      </section>

      {loading && <p className="info">Cargando envíos...</p>}

      {errorMessage && <p className="error">{errorMessage}</p>}

      {!loading && !errorMessage && (
        <section className="card">
          <div className="card-header">
            <h2>Mercancías monitorizadas</h2>
            <button onClick={loadShipments}>Refrescar</button>
          </div>

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
                  <td><span className="status">{shipment.status}</span></td>
                  <td>{shipment.transport_service}</td>
                  <td>{shipment.eta}</td>
                  <td>{shipment.temperature_current} ºC</td>
                  <td><span className="alert">{shipment.alert_status}</span></td>
                  <td>{shipment.last_logistic_event}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      )}
    </main>
  );
}

export default App;
