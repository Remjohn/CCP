from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import yaml
import json
import os
import logging

logger = logging.getLogger(__name__)

# --- Models ---

class ShadowDistortion(BaseModel):
    description: str
    traits: List[str]

class Practice(BaseModel):
    name: str
    description: str

class IdentityPillar(BaseModel):
    id: str
    name: str
    affirmation: str
    shadow_distortion: ShadowDistortion
    signs_defenses: List[str]
    maturation_pathway: List[str]
    practices: List[Practice]
    coaching_prompts: List[str]
    description: Optional[str] = None
    keywords: Optional[List[str]] = None

class TTTLevel(BaseModel):
    code: str
    name: str
    temperature: str
    energy: str
    level: Optional[int] = None
    description: Optional[str] = None
    voice_params: Optional[Dict[str, Any]] = None
    voice_characteristics: Optional[List[str]] = None
    influencers: Optional[List[Dict[str, str]]] = None
    example_messages: Optional[List[Dict[str, str]]] = None

class PersuasionLayer(BaseModel):
    name: str
    description: str
    prompt: str
    examples: List[str]

class PersuasionAngle(BaseModel):
    angle: str
    description: str

class StoryFormula(BaseModel):
    id: int
    components: List[str]
    persuasion_angles: Optional[List[PersuasionAngle]] = None

class ContextDimension(BaseModel):
    description: str
    examples: List[str]

# --- Container Models ---

class IdentityPillarsConfig(BaseModel):
    pillars: List[IdentityPillar]

class TTTMatrixConfig(BaseModel):
    levels: List[TTTLevel]

class PersuasionLayersConfig(BaseModel):
    layers: List[PersuasionLayer]

class StoryFormulasConfig(BaseModel):
    formulas: List[StoryFormula]

class ContextPremiseMapConfig(BaseModel):
    dimensions: Dict[str, ContextDimension]
    example_segments: Optional[List[Dict[str, Any]]] = None

class TribeSoulConfig(BaseModel):
    tribe_name: str
    core_fears: List[str]
    core_desires: List[str]
    language_patterns: List[str]

# --- Library Loader ---

class IntelligenceLibrary:
    def __init__(self, library_path: str = "backend/intelligence_library"):
        self.library_path = library_path
        self.identity_pillars: Optional[IdentityPillarsConfig] = None
        self.ttt_matrix: Optional[TTTMatrixConfig] = None
        self.persuasion_layers: Optional[PersuasionLayersConfig] = None
        self.story_formulas: Optional[StoryFormulasConfig] = None
        self.context_premise_map: Optional[ContextPremiseMapConfig] = None
        self.tribe_soul: Optional[TribeSoulConfig] = None

    def load(self):
        """
        Loads and validates all configuration files.
        Raises FileNotFoundError or ValidationError if critical files are missing or invalid.
        """
        logger.info(f"Loading Intelligence Library from {self.library_path}...")
        
        try:
            self.identity_pillars = self._load_yaml("identity_pillars.yaml", IdentityPillarsConfig)
            self.ttt_matrix = self._load_yaml("ttt_matrix.yaml", TTTMatrixConfig)
            self.persuasion_layers = self._load_yaml("persuasion_layers.yaml", PersuasionLayersConfig)
            self.story_formulas = self._load_yaml("story_formulas.yaml", StoryFormulasConfig)
            self.context_premise_map = self._load_json("context_premise_map.json", ContextPremiseMapConfig)
            # Optional file for now, or create default
            try:
                self.tribe_soul = self._load_json("tribe_soul.json", TribeSoulConfig)
            except FileNotFoundError:
                logger.warning("tribe_soul.json not found. Using default.")
                self.tribe_soul = TribeSoulConfig(tribes=["Burnout", "High Achievers"])
            
            logger.info("Intelligence Library loaded successfully.")
        except Exception as e:
            logger.critical(f"Failed to load Intelligence Library: {e}")
            raise

    def _load_yaml(self, filename: str, model_class):
        path = os.path.join(self.library_path, filename)
        if not os.path.exists(path):
            logger.warning(f"File not found: {path}. Returning empty config if possible.")
            # For strictness, we might want to raise. For now, let's raise.
            raise FileNotFoundError(f"Required configuration file missing: {path}")
            
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return model_class(**data)

    def _load_json(self, filename: str, model_class):
        path = os.path.join(self.library_path, filename)
        if not os.path.exists(path):
             raise FileNotFoundError(f"Required configuration file missing: {path}")
             
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return model_class(**data)

# Global Instance
intelligence_library = IntelligenceLibrary()
