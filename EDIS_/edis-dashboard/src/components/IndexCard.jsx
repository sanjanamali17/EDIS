import Sparkline from "./Sparkline";

function color(status) {
  if (status === "Low Stress") return "green";
  if (status === "Moderate Stress") return "orange";
  return "red";
}

export default function IndexCard({ name, value, status }) {
  // Fake trend for now (replace later with real history)
  const trend = [
    value - 10,
    value - 5,
    value - 3,
    value,
  ];

  return (
    <div className="card">
      <h3>{name}</h3>

      <p className="value">{value}%</p>

      <p className="status" style={{ color: color(status) }}>
        {status}
      </p>

      <Sparkline data={trend} />

      <small>
        {status === "Low Stress"
          ? "Environment is healthy"
          : status === "Moderate Stress"
          ? "Needs attention"
          : "Environment under pressure"}
      </small>
    </div>
  );
}
