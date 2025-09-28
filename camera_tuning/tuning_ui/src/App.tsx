import { useState } from "react"
import "./App.css"
import CalibrationModule from "./modules/calibrationModule"
import DistanceModule from "./modules/distanceModule"

function App() {
    const [mode, setMode] = useState(true)
    return (
        <>
            <button onClick={() => setMode(!mode)} className="capture-button">
                Toggle Mode
            </button>

            {mode ? <CalibrationModule /> : <DistanceModule />}
        </>
    )
}

export default App
