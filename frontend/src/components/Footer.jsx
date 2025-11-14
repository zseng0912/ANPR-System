import logo from "../assets/logo1.png"; // Ensure you have a logo image
import dev1 from "../assets/dev1.png"; // Replace with actual developer images
import dev2 from "../assets/dev2.png";
import reactLogo from "../assets/react.svg"; // Add tech logos
import tailwindLogo from "../assets/tailwind.svg";
import fastapiLogo from "../assets/fastapi.svg";
import pythonLogo from "../assets/python.svg";
import yoloLogo from "../assets/yolo.svg";
import ocrLogo from "../assets/ocr.svg";

const Footer = () => {
  return (
    <footer id="developer" className="mt-20 border-t py-10 border-neutral-700 px-6">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-center text-center lg:text-left">

        {/* Left: Logo & Project Name */}
        <div className="flex items-center space-x-3">
          <img src={logo} alt="Project Logo" className="h-16" />
          <h2 className="text-lg font-semibold text-neutral-300">PlateVision ©2025</h2>
        </div>

        {/* Center: Technologies Used (Title + 3 Columns, Bigger Icons, Justified Center) */}
        <div className="flex flex-col items-center text-neutral-300">
          <h3 className="text-xl font-semibold mb-4">Technologies Used</h3>
          <div className="grid grid-cols-3 gap-6 text-xs">
            <div className="flex items-center gap-3">
              <img src={reactLogo} alt="React" className="h-7" /> <span>React.js</span>
            </div>
            <div className="flex items-center gap-2">
              <img src={tailwindLogo} alt="TailwindCSS" className="h-8" /> <span>TailwindCSS</span>
            </div>
            <div className="flex items-center gap-3">
              <img src={fastapiLogo} alt="FastAPI" className="h-8" /> <span>FastAPI</span>
            </div>
            <div className="flex items-center gap-3">
              <img src={pythonLogo} alt="Python" className="h-8" /> <span>Python</span>
            </div>
            <div className="flex items-center gap-3">
              <img src={yoloLogo} alt="YOLO" className="h-8" /> <span>YOLO</span>
            </div>
            <div className="flex items-center gap-3">
              <img src={ocrLogo} alt="OCR" className="h-8" /> <span>OCR</span>
            </div>
          </div>
        </div>



        {/* Right: Developer Profiles */}
        <div className="flex flex-col items-center">
          <h3 className="text-xl font-semibold text-neutral-300 mb-4">Developers</h3>
          <div className="flex flex-col gap-6">
            <div className="flex items-center gap-4">
              <img src={dev1} alt="Developer 1" className="h-14 w-14 rounded-full border" />
              <div>
                <p className="text-neutral-300">Tan Zu Seng</p>
                <p className="text-sm text-neutral-500">Developer</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <img src={dev2} alt="Developer 2" className="h-14 w-14 rounded-full border" />
              <div>
                <p className="text-neutral-300">Voon Jin Hui</p>
                <p className="text-sm text-neutral-500">Developer</p>
              </div>
            </div>
          </div>
        </div>

      </div>
    </footer>
  );
};

export default Footer;
