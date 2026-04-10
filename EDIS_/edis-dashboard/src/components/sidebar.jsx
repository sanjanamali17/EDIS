import { motion } from "framer-motion";
import { FaInfoCircle, FaChartLine, FaRobot, FaMap, FaEye } from "react-icons/fa";

export default function Sidebar({ active, setActive }) {
  const menu = [
    { id: "about", label: "About", icon: <FaInfoCircle /> },
    { id: "ecosystem", label: "Ecosystem Analysis", icon: <FaChartLine /> },
    { id: "map", label: "Ecosystem Intelligence Map", icon: <FaMap /> },
    { id: "predictor", label: "Future Ecosystem Predictor", icon: <FaEye /> },
    { id: "assistant", label: "EDIS Assistant", icon: <FaRobot /> },
  ];

  return (
    <div className="sidebar">
      {/* Clean Program Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="program-header"
      >
        <div className="program-name-container">
          <h1 className="program-name">EDIS</h1>
        </div>
        <div className="guide-section">
          <div className="guide-label">Environmental Intelligence</div>
          <div className="guide-name">Command Center</div>
        </div>
      </motion.div>

      {/* Navigation Menu */}
      <nav className="navigation-menu">
        {menu.map((item) => (
          <motion.button
            key={item.id}
            onClick={() => setActive(item.id)}
            className={active === item.id ? "active" : ""}
            whileHover={{ scale: 1.05 }}
            transition={{ type: "spring", stiffness: 300 }}
          >
            <span className="icon">{item.icon}</span>
            {item.label}
          </motion.button>
        ))}
      </nav>

      {/* Clean Footer */}
      <div className="credits-footer">
        <div className="credits-divider"></div>
        <div className="copyright">© 2026 EDIS</div>
      </div>
    </div>
  );
}
