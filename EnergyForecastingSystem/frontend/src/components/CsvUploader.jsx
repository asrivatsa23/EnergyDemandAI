import { useCallback, useRef, useState } from "react";
import { downloadSampleCsvUrl } from "../api";

const ACCEPTED_EXTENSION = ".csv";

function isCsvFile(file) {
  if (!file) return false;
  const nameOk = file.name.toLowerCase().endsWith(ACCEPTED_EXTENSION);
  // Some browsers report an empty type for CSV; only reject when the
  // browser is confident it's something else.
  const typeOk =
    file.type === "" ||
    file.type === "text/csv" ||
    file.type === "application/vnd.ms-excel";
  return nameOk && typeOk;
}

export default function CsvUploader({ onUpload, isLoading }) {
  const [isDragging, setIsDragging] = useState(false);
  const [localError, setLocalError] = useState(null);
  const [fileName, setFileName] = useState(null);
  const inputRef = useRef(null);

  const handleFiles = useCallback(
    (fileList) => {
      const file = fileList?.[0];
      if (!file) return;

      if (!isCsvFile(file)) {
        setLocalError("Only .csv files are accepted. Please choose a CSV file.");
        setFileName(null);
        return;
      }

      setLocalError(null);
      setFileName(file.name);
      onUpload(file);
    },
    [onUpload]
  );

  const onDrop = useCallback(
    (e) => {
      e.preventDefault();
      setIsDragging(false);
      handleFiles(e.dataTransfer.files);
    },
    [handleFiles]
  );

  return (
    <div className="card uploader-card">
      <div className="uploader-header">
        <h2>Upload energy data</h2>
        <p className="muted">
          CSV upload only &mdash; the file must include an{" "}
          <code>AEP_MW</code> column with at least 24 rows. Models other
          than LSTM also need a <code>Datetime</code> column.
        </p>
      </div>

      <div
        className={`dropzone ${isDragging ? "dragging" : ""}`}
        onDragOver={(e) => {
          e.preventDefault();
          setIsDragging(true);
        }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={onDrop}
        onClick={() => inputRef.current?.click()}
        role="button"
        tabIndex={0}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".csv,text/csv"
          hidden
          onChange={(e) => handleFiles(e.target.files)}
        />
        <div className="dropzone-icon">CSV</div>
        <p>
          <strong>Drag & drop</strong> a CSV file here, or click to browse
        </p>
        {fileName && <p className="filename">Selected: {fileName}</p>}
      </div>

      {localError && <div className="error-banner">{localError}</div>}

      <div className="uploader-footer">
        <a href={downloadSampleCsvUrl()} className="link-button">
          Download a sample CSV
        </a>
        {isLoading && <span className="status-pill">Running prediction…</span>}
      </div>
    </div>
  );
}
