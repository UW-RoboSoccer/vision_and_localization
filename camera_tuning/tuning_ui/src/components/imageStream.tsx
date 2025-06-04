import { useEffect, useRef, useState } from "react"

const ImageStream = () => {
    const [imgSrc, setImgSrc] = useState<string | null>(null)
    const wsRef = useRef<WebSocket | null>(null)

    useEffect(() => {
        const ws = new WebSocket("ws://localhost:8085/camera/ws")
        ws.binaryType = "arraybuffer"

        ws.onopen = () => {
            console.log("WebSocket connected")
        }

        ws.onmessage = (event) => {
            const blob = new Blob([event.data], { type: "image/jpeg" })
            const url = URL.createObjectURL(blob)
            setImgSrc(url)

            // Revoke old object URLs to prevent memory leaks
            setTimeout(() => URL.revokeObjectURL(url), 100)
        }

        ws.onerror = (err) => {
            console.error("WebSocket error", err)
        }

        wsRef.current = ws

        return () => {
            ws.close()
        }
    }, [])

    return (
        <div>
            {imgSrc ? (
                <img src={imgSrc} width={1280} height={360} alt="Camera Stream" />
            ) : (
                <p>Connecting to camera...</p>
            )}
        </div>
    )
}

export default ImageStream

