import { useState } from 'react';
import './App.css';
import { scanCode } from './api';

function App() {
  const [code, setCode] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  const handleScan = async () => {
    if (!code.trim()) return;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const { data } = await scanCode(code);
      setResult(data);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Scan failed');
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setCode('');
    setError(null);
    setResult(null);
  };

  const mlFinding = result?.ml_findings;
  const isVulnerable = mlFinding?.label === 'vulnerable';
  const staticFindings = result?.static_findings || [];
  const mlUnified = (result?.unified_findings || []).filter(f => f.source === 'ml');

  return (
    <div className="App">
      <header>
        <h1>CodeGuard</h1>
        <p className="subtitle">AI-Powered Code Vulnerability Scanner</p>
      </header>

      <div className="scan-card">
        <label htmlFor="code-input">Paste your code below</label>
        <textarea
          id="code-input"
          value={code}
          onChange={(e) => setCode(e.target.value)}
          placeholder="print(eval(input()))"
          disabled={loading}
        />

        <div className="button-row">
          <button className="btn-scan" onClick={handleScan} disabled={loading || !code.trim()}>
            {loading && <span className="spinner" />}
            {loading ? 'Scanning...' : 'Scan Code'}
          </button>
          <button className="btn-clear" onClick={handleClear} disabled={loading}>
            Clear
          </button>
        </div>

        {error && <div className="error-msg">{error}</div>}
      </div>

      {result && (
        <div className="results">
          <div className="result-header">
            <span className={`badge ${isVulnerable ? 'unsafe' : 'safe'}`}>
              {isVulnerable ? '⚠ UNSAFE' : '✓ SAFE'}
            </span>
            {mlFinding?.confidence && (
              <span className="confidence">
                {Math.round(mlFinding.confidence * 100)}% confidence
              </span>
            )}
          </div>

          {staticFindings.length > 0 && (
            <>
              <h3 style={{ margin: '1rem 0 0.5rem', fontSize: '0.95rem', color: '#94a3b8' }}>
                Findings ({staticFindings.length})
              </h3>
              <div className="finding-list">
                {staticFindings.map((f, i) => (
                  <div key={i} className="finding-item">
                    <span className="finding-line">L{f.line}</span>
                    <span className={`finding-severity severity-${f.severity}`}>{f.severity}</span>
                    <span className="finding-cwe">{f.cwe}</span>
                    <span className="finding-msg">{f.message}</span>
                  </div>
                ))}
              </div>
            </>
          )}

          {mlUnified.length > 0 && (
            <div className="ml-summary">
              <strong>ML Analysis:</strong>{' '}
              {mlUnified[0]?.label === 'vulnerable'
                ? 'Model detected potentially unsafe patterns.'
                : 'Model found no unsafe patterns.'}{' '}
              (confidence: {Math.round((mlUnified[0]?.confidence || 0) * 100)}%)
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
