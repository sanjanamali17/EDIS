import { Bar, Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
} from "chart.js";

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
);

export default function Charts({ indices, historicalData = [] }) {
  // Ensure indices is valid and extract values properly
  const indicatorLabels = indices && Object.keys(indices) || [];
  const indicatorValues = indices && Object.values(indices) || [];
  
  // Bar Chart Configuration
  const barChartData = {
    labels: indicatorLabels.map(key => 
      key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
    ),
    datasets: [{
      label: "Environmental Stress Index",
      data: indicatorValues,
      backgroundColor: [
        'rgba(255, 99, 132, 0.8)',
        'rgba(54, 162, 235, 0.8)',
        'rgba(75, 192, 192, 0.8)',
        'rgba(255, 159, 64, 0.8)',
        'rgba(153, 102, 255, 0.8)'
      ],
      borderColor: [
        'rgba(255, 99, 132, 1)',
        'rgba(54, 162, 235, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(255, 159, 64, 1)',
        'rgba(153, 102, 255, 1)'
      ],
      borderWidth: 2,
      borderRadius: 8
    }]
  };

  const barChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false
      },
      title: {
        display: true,
        text: "Environmental Indicators Analysis",
        font: {
          size: 16,
          weight: 'bold'
        },
        color: '#e2e8f0',
        padding: 20
      },
      tooltip: {
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        titleColor: '#fff',
        bodyColor: '#fff',
        borderColor: '#10b981',
        borderWidth: 1,
        cornerRadius: 8,
        callbacks: {
          label: function(context) {
            const value = context.parsed.y;
            let status = 'Low Stress';
            if (value > 60) status = 'High Stress';
            else if (value > 30) status = 'Moderate Stress';
            return [`Value: ${value.toFixed(1)}%`, `Status: ${status}`];
          }
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
        ticks: {
          callback: function(value) {
            return value + '%';
          },
          color: '#94a3b8'
        },
        grid: {
          color: 'rgba(255, 255, 255, 0.1)'
        },
        title: {
          display: true,
          text: 'Stress Level (%)',
          color: '#e2e8f0',
          font: {
            weight: 'bold'
          }
        }
      },
      x: {
        ticks: {
          color: '#94a3b8'
        },
        grid: {
          display: false
        }
      }
    }
  };

  // Line Chart Configuration for Historical Trends
  const lineChartData = {
    labels: historicalData.map(data => data.year.toString()),
    datasets: [{
      label: "Ecosystem Stress Index",
      data: historicalData.map(data => data.esi),
      borderColor: 'rgba(16, 185, 129, 1)',
      backgroundColor: 'rgba(16, 185, 129, 0.1)',
      borderWidth: 3,
      fill: true,
      tension: 0.4,
      pointRadius: 6,
      pointHoverRadius: 8,
      pointBackgroundColor: 'rgba(16, 185, 129, 1)',
      pointBorderColor: '#fff',
      pointBorderWidth: 2
    }]
  };

  const lineChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false
      },
      title: {
        display: true,
        text: "Historical Ecosystem Trends",
        font: {
          size: 16,
          weight: 'bold'
        },
        color: '#e2e8f0',
        padding: 20
      },
      tooltip: {
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        titleColor: '#fff',
        bodyColor: '#fff',
        borderColor: '#10b981',
        borderWidth: 1,
        cornerRadius: 8,
        callbacks: {
          label: function(context) {
            const value = context.parsed.y;
            const year = context.label;
            return [
              `Year: ${year}`,
              `ESI: ${value.toFixed(1)}%`,
              `Status: ${value > 60 ? 'High Stress' : value > 30 ? 'Moderate Stress' : 'Low Stress'}`
            ];
          }
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
        ticks: {
          callback: function(value) {
            return value + '%';
          },
          color: '#94a3b8'
        },
        grid: {
          color: 'rgba(255, 255, 255, 0.1)'
        },
        title: {
          display: true,
          text: 'Ecosystem Stress Index (%)',
          color: '#e2e8f0',
          font: {
            weight: 'bold'
          }
        }
      },
      x: {
        title: {
          display: true,
          text: 'Year',
          color: '#e2e8f0',
          font: {
            weight: 'bold'
          }
        },
        ticks: {
          color: '#94a3b8'
        },
        grid: {
          display: false
        }
      }
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      {/* Only render charts if we have valid data */}
      {indicatorLabels.length > 0 && indicatorValues.length > 0 ? (
        <>
          {/* Bar Chart */}
          <div style={{ height: '300px' }}>
            <Bar data={barChartData} options={barChartOptions} />
          </div>

          {/* Line Chart for Historical Trends */}
          {historicalData.length > 0 && (
            <div style={{ height: '300px' }}>
              <Line data={lineChartData} options={lineChartOptions} />
            </div>
          )}
        </>
      ) : (
        <div style={{ 
          padding: '2rem', 
          textAlign: 'center', 
          color: '#94a3b8',
          fontSize: '1.1rem'
        }}>
          <div style={{ marginBottom: '1rem' }}>📊</div>
          <div>No environmental data available for visualization</div>
          <div style={{ fontSize: '0.9rem', marginTop: '0.5rem' }}>
            Please analyze an ecosystem to view environmental indicators and trends
          </div>
        </div>
      )}
    </div>
  );
}
