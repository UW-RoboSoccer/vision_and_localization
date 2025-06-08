import { CalibrationData } from "../types/calibrationResponse"
import CameraExtrinsics from "./cameraExtrinsics"
import CameraIntrinsincs from "./cameraIntrinsics"

interface CalibrationResultProps {
    calibrationData: CalibrationData
}

const CalibrationResult = ({ calibrationData }: CalibrationResultProps) => {
    return (
        <div
            style={{
                display: "flex",
                flexDirection: "column",
            }}
        >
            <div
                style={{
                    display: "flex",
                    flexDirection: "row",
                    alignItems: "center",
                    justifyContent: "center",
                    gap: "20px",
                }}
            >
                <h2>Calibration Metrics</h2>
                <p>Left Camera Ret: {calibrationData.ret_left.toFixed(2)}</p>
                <p>Right Camera Ret: {calibrationData.ret_right.toFixed(2)}</p>
                <p>Calibration Ret: {calibrationData.ret_calibrate.toFixed(2)}</p>
                <p>Save Result Index: {calibrationData.save_result_index}</p>
            </div>
            <div>
                <div
                    style={{
                        display: "flex",
                        flexDirection: "row",
                        gap: "50px",
                        justifyContent: "center",
                    }}
                >
                    <CameraIntrinsincs
                        K={calibrationData.K_left}
                        D={calibrationData.D_left}
                        side="Left"
                    />
                    <CameraIntrinsincs
                        K={calibrationData.K_right}
                        D={calibrationData.D_right}
                        side="Right"
                    />
                    <CameraExtrinsics R={calibrationData.R} T={calibrationData.T} />
                </div>
            </div>
        </div>
    )
}

export default CalibrationResult

