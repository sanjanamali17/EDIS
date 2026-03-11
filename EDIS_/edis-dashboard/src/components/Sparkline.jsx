import { Line } from "react-chartjs-2";

export default function Sparkline({ data }) {
  return (
    <Line
      height={40}
      data={{
        labels: data.map((_, i) => i + 1),
        datasets: [
          {
            data,
            tension: 0.4,
          },
        ],
      }}
      options={{
        plugins: { legend: { display: false } },
        scales: {
          x: { display: false },
          y: { display: false },
        },
      }}
    />
  );
}
