import os
import pickle
import pandas as pd
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelHandler:
    """
    Handles loading and prediction for ML models used in virtual patient recruitment
    """
    
    def __init__(self, model_paths=None):
        """
        Initialize ModelHandler with model paths
        
        Args:
            model_paths (dict): Dictionary mapping model names to file paths
        """
        self.model_paths = model_paths or {}
        self.models = {}
        self.feature_orders = {}
        
    def load_models(self):
        """Load all ML models from specified paths"""
        loaded_count = 0
        
        for model_name, path in self.model_paths.items():
            try:
                if os.path.exists(path):
                    with open(path, 'rb') as f:
                        self.models[model_name] = pickle.load(f)
                    logger.info(f"✓ Loaded {model_name} model successfully from {path}")
                    loaded_count += 1
                else:
                    logger.warning(f"⚠ Warning: {model_name} model file not found at {path}")
            except Exception as e:
                logger.error(f"❌ Error loading {model_name} model: {e}")
        
        logger.info(f"📊 Loaded {loaded_count}/{len(self.model_paths)} models successfully")
        return loaded_count
    
    def get_loaded_models(self):
        """Return list of successfully loaded model names"""
        return list(self.models.keys())
    
    def is_model_loaded(self, model_name):
        """Check if a specific model is loaded"""
        return model_name in self.models
    
    def predict_eligibility(self, model_name, features):
        """
        Predict patient eligibility for a specific trial
        
        Args:
            model_name (str): Name of the model to use
            features (dict): Dictionary of feature names and values
            
        Returns:
            str: 'Eligible' or 'Ineligible'
        """
        if model_name not in self.models:
            logger.error(f"Model {model_name} not found in loaded models")
            return 'Ineligible'
        
        try:
            model = self.models[model_name]
            
            # Convert features to the format expected by the model
            # Features should be in the same order as training data
            feature_array = [list(features.values())]
            
            # Make prediction
            prediction = model.predict(feature_array)[0]
            
            # Convert prediction to eligibility status
            eligibility = 'Eligible' if prediction == 1 else 'Ineligible'
            
            logger.info(f"Prediction for {model_name}: {eligibility}")
            return eligibility
            
        except Exception as e:
            logger.error(f"Prediction error for {model_name}: {e}")
            return 'Ineligible'
    
    def batch_predict(self, model_name, features_list):
        """
        Predict eligibility for multiple patients at once
        
        Args:
            model_name (str): Name of the model to use
            features_list (list): List of feature dictionaries
            
        Returns:
            list: List of eligibility predictions
        """
        if model_name not in self.models:
            logger.error(f"Model {model_name} not found in loaded models")
            return ['Ineligible'] * len(features_list)
        
        results = []
        for i, features in enumerate(features_list):
            try:
                result = self.predict_eligibility(model_name, features)
                results.append(result)
            except Exception as e:
                logger.error(f"Error predicting for patient {i+1}: {e}")
                results.append('Ineligible')
        
        return results
    
    def get_model_info(self, model_name):
        """
        Get information about a loaded model
        
        Args:
            model_name (str): Name of the model
            
        Returns:
            dict: Model information
        """
        if model_name not in self.models:
            return {"error": f"Model {model_name} not loaded"}
        
        model = self.models[model_name]
        
        info = {
            "model_name": model_name,
            "model_type": type(model).__name__,
            "is_loaded": True
        }
        
        # Try to get additional model information
        try:
            if hasattr(model, 'n_features_in_'):
                info['n_features'] = model.n_features_in_
            if hasattr(model, 'classes_'):
                info['classes'] = model.classes_.tolist()
            if hasattr(model, 'feature_importances_'):
                info['has_feature_importance'] = True
        except Exception as e:
            logger.debug(f"Could not extract additional info for {model_name}: {e}")
        
        return info
    
    def validate_features(self, model_name, features):
        """
        Validate that features are in the correct format for the model
        
        Args:
            model_name (str): Name of the model
            features (dict): Feature dictionary
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if model_name not in self.models:
            return False, f"Model {model_name} not loaded"
        
        if not isinstance(features, dict):
            return False, "Features must be a dictionary"
        
        if not features:
            return False, "Features dictionary is empty"
        
        # Check for None or NaN values
        for key, value in features.items():
            if value is None:
                return False, f"Feature '{key}' has None value"
            if pd.isna(value):
                return False, f"Feature '{key}' has NaN value"
        
        return True, "Features are valid"
    
    def reload_model(self, model_name):
        """
        Reload a specific model
        
        Args:
            model_name (str): Name of the model to reload
            
        Returns:
            bool: True if successful, False otherwise
        """
        if model_name not in self.model_paths:
            logger.error(f"No path configured for model {model_name}")
            return False
        
        path = self.model_paths[model_name]
        
        try:
            if os.path.exists(path):
                with open(path, 'rb') as f:
                    self.models[model_name] = pickle.load(f)
                logger.info(f"✓ Reloaded {model_name} model successfully")
                return True
            else:
                logger.error(f"Model file not found at {path}")
                return False
        except Exception as e:
            logger.error(f"Error reloading {model_name} model: {e}")
            return False

# Global model handler instance
_model_handler = None

def get_model_handler():
    """
    Get the global model handler instance
    
    Returns:
        ModelHandler: The global model handler
    """
    global _model_handler
    if _model_handler is None:
        from config import MODEL_PATHS
        _model_handler = ModelHandler(MODEL_PATHS)
        _model_handler.load_models()
    return _model_handler

def predict_eligibility(model_name, features):
    """
    Convenience function for making predictions
    
    Args:
        model_name (str): Name of the model to use
        features (dict): Dictionary of features
        
    Returns:
        str: 'Eligible' or 'Ineligible'
    """
    handler = get_model_handler()
    return handler.predict_eligibility(model_name, features)

def get_loaded_models():
    """
    Get list of loaded model names
    
    Returns:
        list: List of loaded model names
    """
    handler = get_model_handler()
    return handler.get_loaded_models()

# Example usage and testing
if __name__ == "__main__":
    # Test the model handler
    try:
        from config import MODEL_PATHS
        
        handler = ModelHandler(MODEL_PATHS)
        loaded = handler.load_models()
        
        print(f"Loaded {loaded} models")
        print(f"Available models: {handler.get_loaded_models()}")
        
        # Test with sample data (you can customize this)
        sample_features = {
            'age': 45,
            'gender': 'Male',
            'bmi': 25.5,
            'glucose': 120,
            'lifestyle_risk': 1,
            'stress_level': 5,
            'systolic_bp': 140,
            'diastolic_bp': 90,
            'cholesterol_total': 200,
            'comorbidities': 1,
            'consent': 'Yes'
        }
        
        if handler.is_model_loaded('hypertension'):
            result = handler.predict_eligibility('hypertension', sample_features)
            print(f"Hypertension prediction: {result}")
        
    except ImportError:
        print("Config module not found - this is normal when testing standalone")
