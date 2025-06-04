const CaptureButton = () => {
    const handleCapture = () => {
        // send post request to capture image
        fetch("http://localhost:8085/capture/capture", {
            method: "POST",
        })
    }

    return (
        <button onClick={handleCapture} className="capture-button">
            Capture
        </button>
    )
}

export default CaptureButton

