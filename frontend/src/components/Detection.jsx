import { useState } from "react";
import axios from "axios";

const Detection = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [imageUrl, setImageUrl] = useState("");
  const [plates, setPlates] = useState([]);
  const [detectedClasses, setDetectedClasses] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

  const handleImageUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setSelectedImage(URL.createObjectURL(file));
    setIsLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post(`${API_BASE_URL}/detect/`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      const { image_url = "", detections } = response.data || {};
      setImageUrl(`${API_BASE_URL}${image_url || ""}`);
      setPlates(detections?.plates || []);
      setDetectedClasses(detections?.detected_classes || []);
    } catch (error) {
      console.error("Error uploading image:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div id="detection" className="scroll-mt-20 my-20">
      <h2 className="text-3xl font-bold mb-6">Upload an image for License Plate Detection</h2>
      
      <input
        type="file"
        accept="image/*,video/*"
        onChange={handleImageUpload}
        className="mb-6"
      />

      {isLoading && <p>Processing image, please wait...</p>}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
        {/* Original Preview */}
        {selectedImage && (
          <div>
            <h3 className="text-xl font-semibold mb-2">Original Image</h3>
            <img src={selectedImage} alt="Uploaded" className="w-full rounded-lg shadow-lg" />
          </div>
        )}

        {/* Processed Image */}
        {imageUrl && imageUrl !== API_BASE_URL && (
          <div>
            <h3 className="text-xl font-semibold mb-2">Processed Image</h3>
            <img src={imageUrl} alt="Processed" className="w-full rounded-lg shadow-lg" />
          </div>
        )}
      </div>

      {/* Detected Plates */}
      {plates.length > 0 && (
        <div className="mt-10">
          <h3 className="text-2xl font-semibold mb-4">Detected License Plates</h3>
          <ul className="space-y-4">
            {plates.map((plate, index) => (
              <li key={index} className="border p-4 rounded-lg bg-neutral-800">
                <p><strong>Plate Number:</strong> {plate.plate_number || "N/A"}</p>
                <p><strong>State:</strong> {plate.state || "Unknown"}</p>
                {plate.crop_url && (
                  <img
                    src={`${API_BASE_URL}${plate.crop_url}`}
                    alt="Cropped plate"
                    className="mt-2 w-48 rounded"
                  />
                )}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Detected Classes */}
      {detectedClasses.length > 0 && (
        <div className="mt-10">
          <h3 className="text-2xl font-semibold mb-4">Detected Objects</h3>
          <ul className="space-y-2">
            {detectedClasses.map((item, index) => (
              <li key={index}>
                <strong>Class:</strong> {item.class} | <strong>BBox:</strong> [{item.bbox.join(", ")}]
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default Detection;
