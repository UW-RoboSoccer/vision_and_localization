interface CameraIntrinsincsProps {
    K: number[][]
    D: number[][]
    side: "Left" | "Right"
}

const CameraIntrinsincs = ({ K, D, side }: CameraIntrinsincsProps) => {
    const D_squeezed = D[0]
    return (
        <div>
            <h2>{side} Camera Intrinsics</h2>
            <div
                style={{
                    display: "flex",
                    flexDirection: "row",
                    gap: "25px",
                    justifyContent: "center",
                }}
            >
                <div>
                    <h3>Camera Matrix K</h3>
                    <p>F_x: {(K[0][0] / 1000).toFixed(2)} m</p>
                    <p>F_y: {(K[1][1] / 1000).toFixed(2)} m</p>
                    <p>C_x: {(K[0][2] / 1000).toFixed(2)} m</p>
                    <p>C_y: {(K[1][2] / 1000).toFixed(2)} m</p>
                </div>
                <div>
                    <h3>Distortion Coefficients D</h3>
                    <p>k1: {D_squeezed[0].toFixed(2)}</p>
                    <p>k2: {D_squeezed[1].toFixed(2)}</p>
                    <p>p1: {D_squeezed[2].toFixed(2)}</p>
                    <p>p2: {D_squeezed[3].toFixed(2)}</p>
                    <p>k3: {D_squeezed[4].toFixed(2)}</p>
                </div>
            </div>
        </div>
    )
}

export default CameraIntrinsincs

