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
      <motion.h1
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        EDIS
      </motion.h1>

      <nav>
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

      <p>© 2026 EDIS</p>
    </div>
  );
}
