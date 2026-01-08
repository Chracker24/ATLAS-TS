"""
Domain-aware Horizon selection for ATLAS-Forecasting
"""

HORIZON_MAP={
    'f1' : {
        'Stable' : 10,
        'Transitional' : 3,
        'Unstable' : 0,
        'Unknown' : 0
    },
    'investment_intraday': {
        'Stable' : 5,
        'Transitional' : 2,
        'Unstable' : 0,
        'Unknown' : 0
    },
    'investment_long_term' : {
        'Stable' : 30,
        'Transitional' : 10,
        'Unstable' : 0,
        'Unknown' : 0
    },
    'health_epidemic' : {
        'Stable' : 7,
        'Transitional' : 3,
        'Unstable' : 0,
        'Unknown' : 0
    }
}


MODEL_PARAMS = {
    'f1' : {
        'Stable' : {
            'alpha' : 0.7,
            'beta' : 0.3,
        },
        'Transitional' : {
            'alpha' : 0.8,
            'beta' : 0.4
        },
    },
    'investment_intraday' : {
        'Stable' : {
            'alpha' : 0.8,
            'beta' : 0.4
        },
        'Transitional' : {
            'alpha' : 0.9,
            'beta' : 0.5
        }
    },
    'investment_long_term' : {
        'Stable' : {
            'alpha' : 0.3, 
            'beta' : 0.2
        },
        'Transitional' : {
            'alpha' : 0.5,
            'beta' : 0.3
        }
    },
    'health_epidemic' : {
        'Stable' : {
            'alpha' : 0.5,
            'beta' : 0.3
        },
        'Transitional' : {
            'alpha' : 0.6,
            'beta' : 0.4
        }
    }
}


def select_horizon (
        regime: str,
        domain : str | None
) -> int:
    #Select forecast horizon based on regime and domain
    if domain == None:
        raise ValueError("No Domain found")
    if domain not in HORIZON_MAP:
        raise ValueError(f"Unknown domain '{domain}'")
    
    return HORIZON_MAP[domain].get(regime, 0)

def get_model_params (
        regime : str,
        domain : str
) -> dict:
    #To get Alpha and Beta
    if domain not in MODEL_PARAMS:
        return {"alpha": 0.5, "beta": 0.3}  # Default params
    
    return MODEL_PARAMS[domain].get(regime, {'alpha' : 0.5, 'beta' : 0.3})

def explain_horizon(
        regime : str,
        domain : str
) ->str:
    horizon = select_horizon(regime, domain)

    if horizon == 0:
        return f"No forecasting - {regime} regime detected"
    elif regime == "Stable":
        return f"Long Horizon ({horizon} steps) - sustained stability detected"
    elif regime == "Transitional":
        return f"Short Horizon ({horizon} steps) - conditions changing"
    else:
        return f"No forecast - {regime} regime"
    
    