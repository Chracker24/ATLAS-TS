import pandas as pd

from .validation import find_error_inInput
from .confidence import confidenceScore, forecastingAllowed, confidenceBand

from ..regime.regime_instantaneous import classify_regimes
from ..regime.regime_persistance import regime_persistance

from ..explainability.explainability import reasons, summary

SENSITIVITY_BAND= {
    "strict": {
        "alpha": 0.1,
        "beta": 1.5,
        "confirm": 2,
        "decay": 0,
        "baseline_method": "q25",
        "smooth_baseline": False
    },
    "normal": {
        "alpha": 0.2,
        "beta": 2.0,
        "confirm": 3,
        "decay": 1,
        "baseline_method": "median",
        "smooth_baseline": True
    },
    "loose": {
        "alpha": 0.3,
        "beta": 3.0,
        "confirm": 4,
        "decay": 2,
        "baseline_method": "q75",
        "smooth_baseline": True
    }
}


DOMAINS = {
    "f1": {
        "window": 5,
        "baseline_method": "median",
        "smooth_baseline": True,
        "sensitivity": "normal"
    },
    "investment_long_term": {
        "window": 30,
        "baseline_method": "median",
        "smooth_baseline": True,
        "sensitivity": "normal"
    },
    "investment_intraday": {
        "window": 20,
        "baseline_method": "q25",
        "smooth_baseline": False,
        "sensitivity": "strict"
    },
    "health_epidemic": {
        "window": 14,
        "baseline_method": "q75",
        "smooth_baseline": True,
        "sensitivity": "strict"
    }
}


class ATLASIntelligenceEngine:
    """
    Core Multi-Domain Time Series Intelligence Engine (ATLAS-IE)

    Stateless
    Rolling-statistics based
    Deterministic and explainable
    """

    def __init__(
        self,
        window: int = 5,
        sensitivity: str = "normal",
        domain: str | None = None
    ):
        # --- Domain override ---
        if domain:
            if domain not in DOMAINS:
                raise ValueError(f"Unknown domain '{domain}'. Choose from {list(DOMAINS.keys())}")
            
            domain_config = DOMAINS[domain]
            self.domain = domain
            window = domain_config["window"]
            sensitivity = domain_config["sensitivity"]
            baseline_method = domain_config["baseline_method"]
            smooth_baseline = domain_config["smooth_baseline"]
        else:
            baseline_method = SENSITIVITY_BAND[sensitivity]["baseline_method"]
            smooth_baseline = SENSITIVITY_BAND[sensitivity]["smooth_baseline"]

        # --- Sensitivity validation ---
        if sensitivity not in SENSITIVITY_BAND:
            raise ValueError(
                f"Sensitivity must be one of {list(SENSITIVITY_BAND.keys())}"
            )

        # --- Final assignments ---
        self.window = window
        self.sensitivity = sensitivity
        self.alpha = SENSITIVITY_BAND[sensitivity]["alpha"]
        self.beta = SENSITIVITY_BAND[sensitivity]["beta"]
        self.confirm = SENSITIVITY_BAND[sensitivity]["confirm"]
        self.decay = SENSITIVITY_BAND[sensitivity]["decay"]

        self.baseline_method = baseline_method
        self.smooth_baseline = smooth_baseline

    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Analyze a time-series DataFrame and return intelligence output.
        """

        print(f"Running ATLAS-IE with sensitivity='{self.sensitivity}' with {self.domain if self.domain else "no"} domain")

        # Input validation
        find_error_inInput(df, self.window)

        result = df.copy()

        # Signal Column
        signal_col = result.select_dtypes(include="number").columns[0]

        # Rolling statistics
        result["Rolling_Mean"] = result[signal_col].rolling(window=self.window,min_periods=self.window).mean()

        result["Rolling_Variance"] = result[signal_col].rolling(window=self.window,min_periods=self.window).var()

        # Regime Classification
        result["Regime_Raw"] = classify_regimes(
            result["Rolling_Variance"],
            self.window,
            alpha=self.alpha,
            beta=self.beta,
            baseline_method=self.baseline_method,
            smooth_baseline=self.smooth_baseline
        )

        result["Regime_Final"] = regime_persistance(
            result["Regime_Raw"],
            confirm=self.confirm,
            decay=self.decay
        )

        result["Confidence"] = confidenceScore(result["Regime_Final"])

        result["Forecasting_Allowed"] = forecastingAllowed(result["Confidence"], threshold=0.7,window=5)

        result["Confidence_Band"] = confidenceBand(result["Confidence"])

        # Reasons and Summary
        result["Reasons"] = reasons(result["Regime_Final"])
        result["Summary"] = result["Reasons"].apply(summary)

        return result

    def results_schema(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Produce a schema of the results that is human Readable.
        """

        result = df.copy()
        signal_col = result.select_dtypes(include="number").columns[0]

        return result[[signal_col, "Confidence_Band", "Forecasting_Allowed", "Reasons", "Summary"]].rename(
            columns={
                signal_col: f"Signal ({signal_col})",
                "Confidence_Band": "FORECASTING_STATE",
                "Forecasting_Allowed": "Forecasting_Allowed",
                "Reasons": "Forecasting_Reasons"
            }
        )
