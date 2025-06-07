import { useState } from "react"
import { CalibrationData, CalibrationResponse } from "../types/calibrationResponse"
import CalibrationResult from "./calibrationResult"

const CalibrateCard = () => {
    const [calibrationData, setcalibrationData] = useState<CalibrationData | null>(null)
    const [calibrationDataIndex, setCalibrationDataIndex] = useState<number | undefined>(undefined)

    const handleCalibrate = async () => {
        console.log("Starting calibration with index:", calibrationDataIndex)
        fetch(`http://localhost:8085/calibrate/calibrate?save_index=${calibrationDataIndex}`, {
            method: "POST",
        })
            .then((response) => response.json())
            .then((data) => {
                console.log("Calibration response received:", data)
                data = data as CalibrationResponse
                if (data.error) {
                    console.error("Calibration error:", data.error)
                    setcalibrationData(null)
                    return
                }
                console.log("Calibration successful:", data.result)
                setcalibrationData(data.data as CalibrationData)
            })
            .catch((error) => {
                console.error("Error during calibration:", error)
                setcalibrationData(null)
            })
    }

    const handleOnChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const value = event.target.value
        setCalibrationDataIndex(value ? parseInt(value, 10) : undefined)
    }

    return (
        <div
            style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: "10px" }}
        >
            <div
                style={{ display: "flex", flexDirection: "row", alignItems: "center", gap: "10px" }}
            >
                <input type="text" value={calibrationDataIndex} onChange={handleOnChange} />
                <button onClick={handleCalibrate} className="calibrate-button">
                    Calibrate
                </button>
            </div>
            <div>
                {calibrationData ? (
                    <CalibrationResult calibrationData={calibrationData} />
                ) : (
                    <p>No calibration result</p>
                )}
            </div>
        </div>
    )
}
export default CalibrateCard

