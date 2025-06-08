export interface CalibrationData {
    ret_left: number
    ret_right: number
    ret_calibrate: number
    K_left: number[][]
    K_right: number[][]
    D_left: number[][]
    D_right: number[][]
    R: number[][]
    T: number[][]
    Q: number[]
    save_result_index: number
}

export interface CalibrationResponse {
    error: Record<string, string>
    data: CalibrationData
}

