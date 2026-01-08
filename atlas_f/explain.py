import numpy as np


def _explain_model_choice(regime : str)-> str:
        if regime == "Stable":
            return "Simple ES used - stable regime expects flat trajectory"
        elif regime == "Transitional":
            return "Double ES used - transitional regime may have trend component"
        else:
            return f"No Model - {regime} regime"
        

def _assess_quality(residuals: np.ndarray, confidence: float) -> str:
    #Assess forecast quality based on residuals and confidence

    std = np.std(residuals)
    mae = np.mean(np.abs(residuals))

    if confidence >= 0.8 and mae < 0.5:
        return "High Quality - low historical error and high confidence"
    elif confidence >= 0.6 and mae < 1.0:
        return "Medium Quality - moderate error and confidence"
    else:
        return "Low quality - high historical error or low confidence"
    

def _calculate_errors(forecast: list, actual: list) -> dict:
    forecast = np.array(forecast)
    actual = np.array(actual)

    errors = actual - forecast

    return {
        "MAE" : float(np.mean(np.abs(errors))),
        "RMSE" : float(np.sqrt(np.mean(errors**2))),
        "MAPE" : float(np.mean(np.abs(errors/actual))*100),
        "errors" : errors.tolist()
    }