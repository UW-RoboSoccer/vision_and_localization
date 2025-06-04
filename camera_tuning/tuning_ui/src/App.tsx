import "./App.css"
import CaptureButton from "./components/captureButton"
import ImageStream from "./components/imageStream"

function App() {
    return (
        <>
            <div>
                <p>Camera Tuning UI</p>
                <div style={{ display: "flex", justifyContent: "center" }}>
                    <CaptureButton />
                </div>
                <ImageStream />
            </div>
        </>
    )
}

export default App
