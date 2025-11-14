import { useEffect, useState } from "react";
import axios from "axios";
import Navbar from "./components/Navbar";
import HeroSection from "./components/HeroSection";
import FeatureSection from "./components/FeatureSection";
import Workflow from "./components/Workflow";
import Footer from "./components/Footer";
import Detection from "./components/Detection";
import Testimonials from "./components/Testimonials";

function App() {
  const [message, setMessage] = useState("");
  // Use environment variable for API base URL, with localhost fallback for development
  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

  useEffect(() => {
    axios
      .get(`${API_BASE_URL}/`)
      .then((response) => setMessage(response.data.message))
      .catch((error) => console.error("Error fetching data:", error));
  }, []);

  return (
    <>
      <Navbar />
      <div id="hero" className="max-w-7xl mx-auto pt-20 px-6">
        <HeroSection />
        <FeatureSection />
        <Detection />
        <Workflow />
{/*         <Testimonials /> */}
        <Footer />
      </div>
    </>
  );
}

export default App;
