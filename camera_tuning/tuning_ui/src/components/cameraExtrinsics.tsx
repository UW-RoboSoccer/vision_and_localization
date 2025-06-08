interface CameraExtrinsicsProps {
    R: number[][]
    T: number[][]
}

const CameraExtrinsics = ({ R, T }: CameraExtrinsicsProps) => {
    return (
        <div>
            <h2>Camera Extrinsics</h2>
            <div
                style={{
                    display: "flex",
                    flexDirection: "row",
                    gap: "10px",
                    justifyContent: "center",
                }}
            >
                <div>
                    <h3>Rotation Matrix R</h3>
                    <p>Rotation X: {R[0][0].toFixed(2)}</p>
                    <p>Rotation Y: {R[1][0].toFixed(2)}</p>
                    <p>Rotation Z: {R[2][0].toFixed(2)}</p>
                </div>
                <div>
                    <h3>Translation Vector T:</h3>
                    <p>Translation X: {T[0][0].toFixed(2)}</p>
                    <p>Translation Y: {T[1][0].toFixed(2)}</p>
                    <p>Translation Z: {T[2][0].toFixed(2)}</p>
                </div>
            </div>
        </div>
    )
}

export default CameraExtrinsics

