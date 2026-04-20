import { motion } from "framer-motion";
import { useState, useEffect, useRef } from "react";
import "../styles/index.css";

export default function About() {
  const fullText = "Earth’s Digital Immune System";
  const [typedText, setTypedText] = useState("");
  const indexRef = useRef(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setTypedText(fullText.slice(0, indexRef.current + 1));
      indexRef.current += 1;

      if (indexRef.current === fullText.length) {
        clearInterval(interval);
      }
    }, 90);

    return () => clearInterval(interval);
  }, []);

  return (
    <motion.div
      className="main"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.7, ease: "easeOut" }}
    >
      {/* Title */}
      <motion.h2
        initial={{ y: -16, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        About EDIS
      </motion.h2>

      {/* Typed Subtitle */}
      <motion.h3
        initial={{ x: -30, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        transition={{ duration: 0.6, delay: 0.1 }}
      >
        {typedText}
        <span className="cursor">|</span>
      </motion.h3>

      {/* Description */}
      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3 }}
      >
        EDIS is a data-driven platform designed to assess ecosystem stress and
        resilience using environmental indicators such as climate, soil,
        vegetation, biodiversity, and human pressure.
      </motion.p>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.45 }}
      >
        Similar to how an immune system detects early signs of illness, EDIS
        identifies early ecological stress signals to support decision-makers,
        researchers, and policymakers.
      </motion.p>

      {/* Cards */}
      <div className="card-container">
        <motion.div
          className="card"
          initial={{ y: 18, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.6 }}
          whileHover={{ scale: 1.04 }}
        >
          <h4>What EDIS Does</h4>
          <ul>
            <li>Monitors ecosystem stress</li>
            <li>Identifies dominant risk factors</li>
            <li>Supports data-driven decisions</li>
          </ul>
        </motion.div>

        <motion.div
          className="card"
          initial={{ y: 18, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.7 }}
          whileHover={{ scale: 1.04 }}
        >
          <h4>Who It’s For</h4>
          <ul>
            <li>Researchers</li>
            <li>Urban planners</li>
            <li>Environmental policymakers</li>
          </ul>
        </motion.div>
      </div>
    </motion.div>
  );
}
