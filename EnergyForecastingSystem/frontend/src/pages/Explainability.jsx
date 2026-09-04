import React from 'react';
import ModelSelector from '../components/ModelSelector';
import ShapExplanation from '../components/ShapExplanation';

const Explainability = ({ models, selectedModel, onSelectModel, explanationData }) => {
  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Explainable AI (XAI) & Decision Interpretability</h1>
          <p className="page-subtitle">
            Model-specific SHAP values, feature importance waterfall attributions, and LIME local explanation insights
          </p>
        </div>
      </div>

      <div className="controls-bar">
        <ModelSelector models={models} selectedModel={selectedModel} onSelectModel={onSelectModel} />
      </div>

      <ShapExplanation explanation={explanationData} />
    </div>
  );
};

export default Explainability;
