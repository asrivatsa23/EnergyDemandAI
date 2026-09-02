export default function Header() {
  return (
    <header className="app-header">
      <h1>⚡ Energy Consumption Forecasting</h1>
      <p className="muted">
        Upload historical hourly load data and get an explainable
        next-hour forecast powered by an LSTM model and SHAP.
      </p>
    </header>
  );
}
