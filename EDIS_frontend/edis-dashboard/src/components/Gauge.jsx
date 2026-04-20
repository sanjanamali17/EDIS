import { Doughnut } from "react-chartjs-2";

function getColor(v) {
  if (v < 30) return "green";
  if (v < 60) return "orange";
  return "red";
}

export default function EcosystemGauge({ value, status }) {
  return (
    <div className="gauge-box">
      <Doughnut
        data={{
          datasets: [
            {
              data: [value, 100 - value],
              backgroundColor: [getColor(value), "#eee"],
              borderWidth: 0,
            },
          ],
        }}
        options={{
          cutout: "75%",
          plugins: { legend: { display: false } },
        }}
      />

      <h2>{value}%</h2>
      <p style={{ color: getColor(value) }}>{status}</p>

      <p className="simple-text">
        {status === "Low Stress"
          ? "The ecosystem is safe"
          : status === "Moderate Stress"
          ? "The ecosystem needs care"
          : "The ecosystem is in danger"}
      </p>
    </div>
  );
}
