import CalibrateCard from "../components/calibrateCard"
import CaptureButton from "../components/captureButton"
import ImageStream from "../components/imageStream"

const CalibrationModule = () => {
    return (
        <div
            style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                gap: "20px",
            }}
        >
            <p>Camera Tuning UI</p>

            <CalibrateCard />
            <div
                style={{
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                    gap: "10px",
                }}
            >
                <CaptureButton url="http://localhost:8085/capture/capture" text="Capture" />
                <CaptureButton url="http://localhost:8085/capture/save" text="Save" />
                <CaptureButton url="http://localhost:8085/capture/clear" text="Clear" />
            </div>
            <ImageStream />
        </div>
    )
}

export default CalibrationModule

