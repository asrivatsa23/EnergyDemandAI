import React from 'react';
import ModelComparisonComponent from '../components/ModelComparison';

const ModelComparisonPage = ({ comparisonData }) => {
  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Model Evaluation & Performance Benchmarking</h1>
          <p className="page-subtitle">
            Rigorous evaluation of baseline, tree-based, statistical, LSTM, and Hybrid Ensemble models on test split
          </p>
        </div>
      </div>

      <ModelComparisonComponent comparison={comparisonData} />
    </div>
  );
};

export default ModelComparisonPage;
