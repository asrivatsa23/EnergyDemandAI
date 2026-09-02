import {
  Bar,
  BarChart,
  Cell,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
  ReferenceLine,
} from "recharts";

const POSITIVE_COLOR = "#dc2626"; // pushes prediction up
const NEGATIVE_COLOR = "#2563eb"; // pushes prediction down

export default function ShapExplanation({ shap, prediction }) {
  if (!shap) return null;

  const { base_value, values, labels } = shap;

  const data = values.map((value, idx) => ({
    label: labels ? labels[idx] : `t-${values.length - idx}`,
    contribution: value,
  }));

  // Rank the hours by absolute impact so the most influential ones are
  // easy to spot, in addition to seeing them in chronological order.
  const ranked = [...data]
    .sort((a, b) => Math.abs(b.contribution) - Math.abs(a.contribution))
    .slice(0, 5);

  return (
    <div className="card">
      <h2>Why this forecast? (SHAP explanation)</h2>
      <p className="muted">
        Each bar shows how much that hour pushed the prediction above (red)
        or below (blue) the model's baseline expectation of{" "}
        <strong>{base_value?.toLocaleString()} MW</strong>. The final
        forecast of <strong>{prediction?.toLocaleString()} MW</strong> is the
        baseline plus the sum of all contributions.
      </p>

      <ResponsiveContainer width="100%" height={320}>
        <BarChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 30 }}>
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
            label={{ value: "MW contribution", angle: -90, position: "insideLeft" }}
          />
          <ReferenceLine y={0} stroke="#94a3b8" />
          <Tooltip formatter={(value) => `${value > 0 ? "+" : ""}${value} MW`} />
          <Bar dataKey="contribution">
            {data.map((entry, index) => (
              <Cell
                key={index}
                fill={entry.contribution >= 0 ? POSITIVE_COLOR : NEGATIVE_COLOR}
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>

      <div className="shap-top-list">
        <h3>Most influential hours</h3>
        <ul>
          {ranked.map((item, idx) => (
            <li key={idx}>
              <span className="shap-rank-label">{item.label}</span>
              <span
                className={`shap-rank-value ${
                  item.contribution >= 0 ? "positive" : "negative"
                }`}
              >
                {item.contribution >= 0 ? "+" : ""}
                {item.contribution} MW
              </span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
