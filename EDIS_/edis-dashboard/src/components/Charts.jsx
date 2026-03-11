import { Bar } from "react-chartjs-2";

export default function Charts({ indices }) {
  return (
    <Bar
      data={{
        labels: Object.keys(indices),
        datasets: [{
          label: "Stress Index",
          data: Object.values(indices).map(i => i.value)
        }]
      }}
    />
  );
}
