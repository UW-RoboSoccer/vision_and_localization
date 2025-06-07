type CaptureButtonProps = {
    url: string
    text: string
}

const CaptureButton = ({ url, text }: CaptureButtonProps) => {
    const handleCapture = () => {
        fetch(url, {
            method: "POST",
        })
    }

    return (
        <button onClick={handleCapture} className="capture-button">
            {text}
        </button>
    )
}

export default CaptureButton

