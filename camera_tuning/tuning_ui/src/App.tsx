import "./App.css"
import CaptureButton from "./components/captureButton"
import ImageStream from "./components/imageStream"

function App() {
    return (
        <>
            <div>
                <p>Camera Tuning UI</p>
                <div
                    style={{
                        display: "flex",
                        flexDirection: "column",
                        alignItems: "center",
                        gap: "10px",
                    }}
                >
                    <CaptureButton
                        url="http://localhost:8085/calibrate/calibrate"
                        text="Calibrate Camera"
                    />
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
                </div>
                <ImageStream />
            </div>
        </>
    )
}

export default App
