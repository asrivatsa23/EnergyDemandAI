import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

export default function ForecastChart({ inputValues, timestamps, prediction }) {
  if (!inputValues || inputValues.length === 0) return null;

  const data = inputValues.map((value, idx) => ({
    label: timestamps ? timestamps[idx] : `t-${inputValues.length - idx}`,
    actual: value,
    predicted: null,
  }));

  data.push({
    label: "forecast",
    actual: null,
    predicted: prediction,
  });

  return (
    <div className="card">
      <h2>24-hour history &amp; forecast</h2>
      <ResponsiveContainer width="100%" height={340}>
        <LineChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 30 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis
            dataKey="label"
            tick={{ fontSize: 11 }}
            angle={-35}
            textAnchor="end"
            height={60}
          />
          <YAxis
            tick={{ fontSize: 12 }}
            domain={["auto", "auto"]}
            label={{ value: "MW", angle: -90, position: "insideLeft" }}
          />
          <Tooltip formatter={(value) => (value === null ? "—" : `${value} MW`)} />
          <Line
            type="monotone"
            dataKey="actual"
            name="Previous 24 hours"
            stroke="#2563eb"
            strokeWidth={2}
            dot={{ r: 2 }}
            connectNulls={false}
          />
          <Line
            type="monotone"
            dataKey="predicted"
            name="Prediction"
            stroke="#dc2626"
            strokeWidth={0}
            dot={{ r: 6 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
