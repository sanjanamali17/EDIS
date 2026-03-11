import { useState, useEffect } from "react";
import "../styles/ecosystem_map.css";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

export default function EcosystemIntelligenceMap() {
  const [cities, setCities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadEcosystemData();
  }, []);

  const loadEcosystemData = async () => {
    try {
      setLoading(true);
      
      // Try to fetch from backend first
      try {
        const response = await fetch(`${API_BASE}/ecosystem-map-data`);
        const data = await response.json();
        
        if (data.success) {
          setCities(data.data);
          console.log('Loaded', data.data.length, 'cities from backend');
          setTimeout(() => {
            initSimpleMap(data.data);
          }, 100);
          return;
        }
      } catch (backendErr) {
        console.log('Backend not available, using sample data');
      }
      
      // Use sample data if backend is not available
      const sampleData = [
        { 
          name: "Hyderabad", 
          lat: 17.3850, 
          lon: 78.4867, 
          climate_stress: 45.2, 
          soil_stress: 38.7, 
          vegetation_stress: 35.2, 
          human_pressure: 51.3, 
          biodiversity_stress: 29.8,
          ecosystem_stress_index: 40.1,
          ecosystem_status: "Moderate"
        },
        { 
          name: "Delhi", 
          lat: 28.6139, 
          lon: 77.2090, 
          climate_stress: 62.1, 
          soil_stress: 48.3, 
          vegetation_stress: 55.7, 
          human_pressure: 71.2, 
          biodiversity_stress: 41.5,
          ecosystem_stress_index: 56.2,
          ecosystem_status: "High Stress"
        },
        { 
          name: "Mumbai", 
          lat: 19.0760, 
          lon: 72.8777, 
          climate_stress: 58.4, 
          soil_stress: 42.1, 
          vegetation_stress: 38.9, 
          human_pressure: 68.5, 
          biodiversity_stress: 35.7,
          ecosystem_stress_index: 49.1,
          ecosystem_status: "Moderate"
        },
        { 
          name: "Bangalore", 
          lat: 12.9716, 
          lon: 77.5946, 
          climate_stress: 41.3, 
          soil_stress: 35.8, 
          vegetation_stress: 32.1, 
          human_pressure: 54.2, 
          biodiversity_stress: 28.4,
          ecosystem_stress_index: 38.5,
          ecosystem_status: "Moderate"
        },
        { 
          name: "Chennai", 
          lat: 13.0827, 
          lon: 80.2707, 
          climate_stress: 47.8, 
          soil_stress: 39.5, 
          vegetation_stress: 36.4, 
          human_pressure: 52.1, 
          biodiversity_stress: 31.2,
          ecosystem_stress_index: 41.6,
          ecosystem_status: "Moderate"
        },
        { 
          name: "Kolkata", 
          lat: 22.5726, 
          lon: 88.3639, 
          climate_stress: 51.6, 
          soil_stress: 43.2, 
          vegetation_stress: 39.8, 
          human_pressure: 56.7, 
          biodiversity_stress: 33.9,
          ecosystem_stress_index: 45.2,
          ecosystem_status: "Moderate"
        },
        { 
          name: "Pune", 
          lat: 18.5204, 
          lon: 73.8567, 
          climate_stress: 44.1, 
          soil_stress: 37.4, 
          vegetation_stress: 34.2, 
          human_pressure: 49.8, 
          biodiversity_stress: 30.1,
          ecosystem_stress_index: 39.3,
          ecosystem_status: "Moderate"
        },
        { 
          name: "Jaipur", 
          lat: 26.9124, 
          lon: 75.7873, 
          climate_stress: 56.3, 
          soil_stress: 46.8, 
          vegetation_stress: 42.7, 
          human_pressure: 58.9, 
          biodiversity_stress: 37.5,
          ecosystem_stress_index: 48.6,
          ecosystem_status: "Moderate"
        },
        { 
          name: "Lucknow", 
          lat: 26.8467, 
          lon: 80.9462, 
          climate_stress: 49.2, 
          soil_stress: 41.3, 
          vegetation_stress: 37.8, 
          human_pressure: 53.4, 
          biodiversity_stress: 32.6,
          ecosystem_stress_index: 43.1,
          ecosystem_status: "Moderate"
        },
        { 
          name: "Kakinada", 
          lat: 16.9890, 
          lon: 82.2474, 
          climate_stress: 43.7, 
          soil_stress: 36.9, 
          vegetation_stress: 33.5, 
          human_pressure: 47.8, 
          biodiversity_stress: 29.3,
          ecosystem_stress_index: 38.4,
          ecosystem_status: "Moderate"
        }
      ];
      
      setCities(sampleData);
      console.log('Loaded', sampleData.length, 'cities from sample data');
      setTimeout(() => {
        initSimpleMap(sampleData);
      }, 100);
      
    } catch (err) {
      console.error('Error loading data:', err);
      setError("Error loading map data: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  const initSimpleMap = (cityData) => {
    try {
      console.log('Initializing simple map with', cityData.length, 'cities');
      
      // Create a simple map container
      const mapContainer = document.getElementById('simple-map');
      if (!mapContainer) {
        console.error('Map container not found');
        return;
      }

      // Clear existing content
      mapContainer.innerHTML = '';

      // Create a proper HTML-based map with working click events
      const mapHTML = `
        <div style="width: 100%; height: 100%; position: relative; background: #f0f8ff;">
          <!-- India Map Background -->
          <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 50%, #90caf9 100%); display: flex; align-items: center; justify-content: center;">
            <div style="text-align: center; color: #1565c0; opacity: 0.3;">
              <div style="font-size: 48px; margin-bottom: 20px;">🇮🇳</div>
              <div style="font-size: 32px; font-weight: bold;">INDIA</div>
              <div style="font-size: 18px; margin-top: 10px;">Ecosystem Health Map</div>
            </div>
          </div>
          
          <!-- City Markers -->
          ${cityData.map((city, index) => {
            const color = getMarkerColor(city.ecosystem_stress_index);
            const size = getMarkerSize(city.ecosystem_stress_index);
            // Better positioning based on coordinates
            const top = 50 - (city.lat - 20) * 2.5; // Better conversion to percentage
            const left = 40 + (city.lon - 75) * 2; // Better conversion to percentage
            
            return `
              <div class="city-marker" 
                   id="marker-${index}"
                   style="position: absolute; 
                          top: ${top}%; 
                          left: ${left}%; 
                          transform: translate(-50%, -50%);
                          cursor: pointer;
                          z-index: 10;"
                   data-city='${city.name}'
                   data-esi='${city.ecosystem_stress_index}'
                   data-status='${city.ecosystem_status}'
                   data-climate='${city.climate_stress}'
                   data-soil='${city.soil_stress}'
                   data-vegetation='${city.vegetation_stress}'
                   data-human='${city.human_pressure}'
                   data-biodiversity='${city.biodiversity_stress}'>
                <div style="background: ${color}; 
                           width: ${size}px; 
                           height: ${size}px; 
                           border-radius: 50%; 
                           border: 3px solid white; 
                           box-shadow: 0 2px 8px rgba(0,0,0,0.4);
                           display: flex; 
                           align-items: center; 
                           justify-content: center;
                           font-weight: bold; 
                           color: white; 
                           font-size: ${size/3}px;
                           transition: all 0.2s ease;">
                  ${color === '#16a34a' ? '✓' : color === '#f59e0b' ? '!' : '⚠'}
                </div>
                <div style="position: absolute; top: ${size + 5}px; left: 50%; transform: translateX(-50%); background: rgba(0,0,0,0.8); color: white; padding: 2px 6px; border-radius: 4px; font-size: 10px; white-space: nowrap;">
                  ${city.name}
                </div>
              </div>
            `;
          }).join('')}
          
          <!-- Popup Container -->
          <div id="city-popup" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); background: white; border-radius: 8px; box-shadow: 0 4px 20px rgba(0,0,0,0.2); padding: 0; min-width: 280px; display: none; z-index: 100;">
            <!-- Popup content will be inserted here -->
          </div>
        </div>
      `;

      mapContainer.innerHTML = mapHTML;
      
      // Add event listeners after DOM is updated
      setTimeout(() => {
        addClickListeners();
        addHoverEffects();
      }, 100);
      
      console.log('Simple map initialized successfully');

    } catch (err) {
      console.error('Error initializing simple map:', err);
      setError("Failed to initialize map: " + err.message);
    }
  };

  const addClickListeners = () => {
    const markers = document.querySelectorAll('.city-marker');
    markers.forEach(marker => {
      marker.addEventListener('click', function(e) {
        e.preventDefault();
        const city = this.dataset.city;
        const esi = this.dataset.esi;
        const status = this.dataset.status;
        const climate = this.dataset.climate;
        const soil = this.dataset.soil;
        const vegetation = this.dataset.vegetation;
        const human = this.dataset.human;
        const biodiversity = this.dataset.biodiversity;
        
        console.log('Clicked on city:', city);
        showCityPopup(city, esi, status, climate, soil, vegetation, human, biodiversity);
      });
    });
  };

  const addHoverEffects = () => {
    const markers = document.querySelectorAll('.city-marker');
    markers.forEach(marker => {
      marker.addEventListener('mouseenter', function() {
        this.style.transform = 'translate(-50%, -50%) scale(1.2)';
      });
      marker.addEventListener('mouseleave', function() {
        this.style.transform = 'translate(-50%, -50%) scale(1)';
      });
    });
  };

  const showCityPopup = (city, esi, status, climate, soil, vegetation, human, biodiversity) => {
    try {
      const popup = document.getElementById('city-popup');
      const color = getMarkerColor(parseFloat(esi));
      
      popup.innerHTML = `
        <div style="background: ${color}; color: white; padding: 12px; border-radius: 8px 8px 0 0;">
          <h3 style="margin: 0; font-size: 16px; font-weight: bold;">📍 ${city}</h3>
        </div>
        
        <div style="background: #f8fafc; padding: 12px; border: 1px solid #e2e8f0; border-top: none;">
          <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <strong>Ecosystem Stress Index:</strong>
            <span style="background: ${color}; color: white; padding: 4px 8px; border-radius: 12px; font-weight: bold;">
              ${esi}%
            </span>
          </div>
          <div style="text-align: center; margin-bottom: 8px;">
            <span style="background: #e2e8f0; padding: 4px 8px; border-radius: 12px; font-size: 12px; font-weight: 600;">
              ${status}
            </span>
          </div>
        </div>
        
        <div style="background: white; padding: 12px; border: 1px solid #e2e8f0; border-top: none; border-radius: 0 0 8px 8px;">
          <div style="font-size: 14px;">
            <div style="display: flex; justify-content: space-between; padding: 4px 0; border-bottom: 1px solid #f1f5f9;">
              <span>🌡️ Climate:</span>
              <strong>${climate}%</strong>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 4px 0; border-bottom: 1px solid #f1f5f9;">
              <span>🌱 Soil:</span>
              <strong>${soil}%</strong>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 4px 0; border-bottom: 1px solid #f1f5f9;">
              <span>🌿 Vegetation:</span>
              <strong>${vegetation}%</strong>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 4px 0; border-bottom: 1px solid #f1f5f9;">
              <span>🏙️ Human Pressure:</span>
              <strong>${human}%</strong>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 4px 0;">
              <span>🦋 Biodiversity:</span>
              <strong>${biodiversity}%</strong>
            </div>
          </div>
        </div>
        
        <div style="padding: 8px 12px; text-align: center; background: white; border-top: 1px solid #e2e8f0; border-radius: 0 0 8px 8px;">
          <button onclick="closePopup()" style="background: #3b82f6; color: white; border: none; padding: 6px 16px; border-radius: 4px; cursor: pointer;">Close</button>
        </div>
      `;
      
      popup.style.display = 'block';
      console.log('Popup shown for city:', city);
      
      // Add closePopup function to window
      window.closePopup = () => {
        popup.style.display = 'none';
      };
      
    } catch (err) {
      console.error('Error showing popup:', err);
    }
  };

  // Make closePopup globally available
  window.closePopup = function() {
    const popup = document.getElementById('city-popup');
    if (popup) {
      popup.style.display = 'none';
    }
  };

  const getMarkerColor = (esi) => {
    if (esi < 30) return "#16a34a"; // Green - Healthy
    if (esi < 60) return "#f59e0b"; // Yellow - Moderate
    return "#dc2626"; // Red - High Stress
  };

  const getMarkerSize = (esi) => {
    if (esi < 30) return 20;
    if (esi < 60) return 25;
    return 30;
  };

  if (loading) {
    return (
      <div className="map-container">
        <div className="loading">Loading India Ecosystem Map...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="map-container">
        <div className="error">Error: {error}</div>
      </div>
    );
  }

  return (
    <div className="map-container">
      {/* Title */}
      <div className="map-title">
        <h1>🇮🇳 India Ecosystem Health Map</h1>
        <p>Click on any city to see ecosystem health results</p>
      </div>

      {/* Legend */}
      <div className="map-legend">
        <h3>Ecosystem Health</h3>
        <div className="legend-item">
          <div className="legend-color" style={{ backgroundColor: "#16a34a" }}></div>
          <span>Healthy (0-30)</span>
        </div>
        <div className="legend-item">
          <div className="legend-color" style={{ backgroundColor: "#f59e0b" }}></div>
          <span>Moderate (30-60)</span>
        </div>
        <div className="legend-item">
          <div className="legend-color" style={{ backgroundColor: "#dc2626" }}></div>
          <span>High Stress (60+)</span>
        </div>
      </div>
      
      {/* Simple Map Container */}
      <div id="simple-map" className="map-wrapper">
        <div style={{ 
          display: 'flex', 
          justifyContent: 'center', 
          alignItems: 'center', 
          height: '100%',
          fontSize: '18px',
          color: '#64748b'
        }}>
          Initializing map...
        </div>
      </div>
    </div>
  );
}
