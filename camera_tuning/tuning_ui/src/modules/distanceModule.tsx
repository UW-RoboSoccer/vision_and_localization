import { useState } from "react"
import ImageStream from "../components/imageStream"

const DistanceModule = () => {
    const [calibrationSaveIndex, setCalibrationSaveIndex] = useState("0")
    const [calibrationLoaded, setCalibrationLoaded] = useState(false)

    const handleOnSaveIndexChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const value = event.target.value
        setCalibrationSaveIndex(value)
    }

    const handleLoad = () => {
        fetch(
            `http://localhost:8085/distance/load_calibration?save_index=${calibrationSaveIndex}`,
            {
                method: "POST",
            }
        )
            .then((response) => response.json())
            .then((data) => {
                setCalibrationLoaded(data.success)
            })
    }

    return (
        <div
            style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                gap: "20px",
            }}
        >
            <p>Distance Testing</p>
            <input type="text" value={calibrationSaveIndex} onChange={handleOnSaveIndexChange} />
            <button onClick={handleLoad} className="calibrate-button">
                Load Calibration
            </button>
            {calibrationLoaded ? (
                <div>
                    <ImageStream
                        socketUrl="ws://localhost:8085/distance/ws"
                        width={640}
                        height={360}
                    />
                    <ImageStream
                        socketUrl="ws://localhost:8085/camera/ws"
                        width={1280}
                        height={360}
                    />
                </div>
            ) : (
                <p>Load a calibration first</p>
            )}
        </div>
    )
}

export default DistanceModule

