import { useState } from "react";
import Sidebar from "./components/sidebar";
import About from "./pages/about";
import EcosystemAnalysis from "./pages/EcosystemAnalysis";
import EcosystemIntelligenceMap from "./pages/EcosystemIntelligenceMap";
import FutureEcosystemPredictor from "./pages/FutureEcosystemPredictor";
import EdisAssistant from "./pages/EdisAssistant";

export default function App() {
  const [active, setActive] = useState("about");

  return (
    <div className="app">
      <Sidebar active={active} setActive={setActive} />

      <main className="main-content">
        {active === "about" && <About />}

        {active === "ecosystem" && <EcosystemAnalysis setActive={setActive} />}

        {active === "map" && <EcosystemIntelligenceMap />}

        {active === "predictor" && <FutureEcosystemPredictor />}

        {active === "assistant" && <EdisAssistant />}
      </main>
    </div>
  );
}
