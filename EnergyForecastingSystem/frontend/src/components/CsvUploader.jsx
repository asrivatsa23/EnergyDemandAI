import React, { useState } from 'react';
import { UploadCloud, FileText, CheckCircle, AlertCircle } from 'lucide-react';
import { uploadAndPredict } from '../api';

const CsvUploader = ({ onPredictionComplete, models = [], selectedModel }) => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [successMsg, setSuccessMsg] = useState(null);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setError(null);
      setSuccessMsg(null);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a valid .csv file first.");
      return;
    }

    setLoading(true);
    setError(null);
    setSuccessMsg(null);

    try {
      const res = await uploadAndPredict(file, selectedModel);
      if (res.success) {
        setSuccessMsg(`Successfully processed ${res.rows_processed} rows with model '${res.model_used}'.`);
        if (onPredictionComplete) {
          onPredictionComplete(res);
        }
      } else {
        setError(res.error || "Upload and prediction failed.");
      }
    } catch (err) {
      setError(err.response?.data?.error || "Network or backend error during CSV upload.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chart-card">
      <div className="card-header">
        <h3 className="card-title">
          <UploadCloud className="text-cyan-400" size={18} />
          Upload Custom Indian Electricity Demand CSV Data
        </h3>
      </div>

      <div style={{
        border: '2px dashed var(--border-bright)',
        borderRadius: '12px',
        padding: '2.5rem 1.5rem',
        textAlign: 'center',
        background: 'rgba(6, 182, 212, 0.02)',
        marginBottom: '1rem'
      }}>
        <FileText size={36} className="text-cyan-400" style={{ margin: '0 auto 0.75rem auto' }} />
        <p style={{ color: '#fff', fontWeight: '600', marginBottom: '0.25rem' }}>
          Select or drag your CSV file here
        </p>
        <p style={{ color: '#9ca3af', fontSize: '0.85rem', marginBottom: '1.25rem' }}>
          Requires a Datetime column and an Energy Demand column (e.g. 'Energy Required (MU)' or 'Demand (MW)')
        </p>

        <input
          type="file"
          accept=".csv"
          onChange={handleFileChange}
          style={{ display: 'none' }}
          id="csv-input"
        />
        <label htmlFor="csv-input" className="btn-primary" style={{ display: 'inline-flex', cursor: 'pointer' }}>
          Browse Files
        </label>

        {file && (
          <div style={{ marginTop: '1rem', color: '#10b981', fontWeight: '600', fontSize: '0.9rem' }}>
            Selected: {file.name} ({(file.size / 1024).toFixed(1)} KB)
          </div>
        )}
      </div>

      {error && (
        <div style={{ background: 'rgba(244, 63, 94, 0.1)', border: '1px solid rgba(244, 63, 94, 0.3)', padding: '0.8rem 1rem', borderRadius: '8px', color: '#f43f5e', fontSize: '0.9rem', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <AlertCircle size={18} />
          <span>{error}</span>
        </div>
      )}

      {successMsg && (
        <div style={{ background: 'rgba(16, 185, 129, 0.1)', border: '1px solid rgba(16, 185, 129, 0.3)', padding: '0.8rem 1rem', borderRadius: '8px', color: '#10b981', fontSize: '0.9rem', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <CheckCircle size={18} />
          <span>{successMsg}</span>
        </div>
      )}

      <button
        className="btn-primary"
        onClick={handleUpload}
        disabled={loading || !file}
        style={{ width: '100%', justifyContent: 'center', opacity: (loading || !file) ? 0.6 : 1 }}
      >
        {loading ? 'Processing & Predicting...' : 'Upload & Generate 24h Forecast'}
      </button>
    </div>
  );
};

export default CsvUploader;
