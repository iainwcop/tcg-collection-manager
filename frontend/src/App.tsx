import { useEffect, useState } from "react";

type HealthResponse = {
  status: string;
  service: string;
};

export default function App() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("/api/health/")
      .then((response) => {
        if (!response.ok) {
          throw new Error(`API returned ${response.status}`);
        }
        return response.json() as Promise<HealthResponse>;
      })
      .then(setHealth)
      .catch((err: Error) => setError(err.message));
  }, []);

  return (
    <main className="app">
      <header>
        <h1>TCG Collection Manager</h1>
        <p>Organize, scan, and value your trading card collections.</p>
      </header>

      <section className="status-card">
        <h2>System status</h2>
        {health && (
          <p className="status-ok">
            Backend connected — {health.service} ({health.status})
          </p>
        )}
        {error && <p className="status-error">Backend unreachable — {error}</p>}
        {!health && !error && <p>Checking API connection…</p>}
      </section>
    </main>
  );
}
