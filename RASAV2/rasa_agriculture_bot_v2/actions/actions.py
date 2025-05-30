
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, EventType, FollowupAction
from rasa_sdk.types import DomainDict


class ActionSetRequestedInfo(Action):
    """Sets the requested_info slot based on the intent of the user's message."""

    def name(self) -> Text:
        return "action_set_requested_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        intent = tracker.latest_message['intent']['name']
        requested_info = None
        
        # Map intents to requested_info values
        intent_to_info = {
            'crop_info_query': 'crop_info',
            'disease_control_query': 'disease_control',
            'nutrient_requirement_query': 'nutrient_requirement',
            'pest_control_query': 'pest_control',
            'ask_fertilizer_requirements': 'fertilizer_requirement',
            'variety_yield_query': 'variety_yield',
            'deficiency_related_query': 'deficiency_info',
            'ask_best_practices': 'best_practices',
            'ask_crop_rotation': 'crop_rotation',
            'ask_harvesting_time': 'harvesting_time',
            'ask_insecticide_info': 'insecticide_info',
            'ask_disease_prevention': 'disease_prevention',
            'ask_natural_pest_control': 'natural_pest_control',
            'ask_fungicide_info': 'fungicide_info',
            'ask_pest_detection': 'pest_detection',
            'ask_fertilizer_schedule': 'fertilizer_schedule',
            'ask_fertilizer_application_method': 'fertilizer_application_method',
            'ask_organic_fertilizer': 'organic_fertilizer',
            'ask_water_requirement': 'water_requirement',
            'ask_irrigation_methods': 'irrigation_methods',
            'ask_drainage': 'drainage',
            'ask_climate_requirements': 'climate_requirements',
            'ask_weather_impact': 'weather_impact',
            'ask_drought_management': 'drought_management',
            'ask_crop_rotation_benefits': 'crop_rotation_benefits',
            'ask_mixed_farming_techniques': 'mixed_farming_techniques',
            'ask_crop_compatibility': 'crop_compatibility',
            'ask_soil_type': 'soil_type',
            'ask_soil_preparation': 'soil_preparation'
        }
        
        if intent in intent_to_info:
            requested_info = intent_to_info[intent]
        
        # Check if we need to activate the form
        events = [SlotSet("requested_info", requested_info)]
        
        # Extract entities from the message
        entities = tracker.latest_message.get('entities', [])
        crop = next((e['value'] for e in entities if e['entity'] == 'crop'), None)
        variety = next((e['value'] for e in entities if e['entity'] == 'variety'), None)
        
        # Set slots based on entities
        if crop:
            events.append(SlotSet("crop", crop))
        if variety:
            events.append(SlotSet("variety", variety))
        
        # Determine if we need to activate the form
        if requested_info == 'variety_yield' and (not crop or not variety):
            # For variety yield queries, we need both crop and variety
            return events + [FollowupAction("agriculture_form")]
        elif requested_info and not crop:
            # For other queries, we at least need the crop
            return events + [FollowupAction("agriculture_form")]
        elif requested_info:
            # We have all the information we need
            return events + [FollowupAction("action_submit_agriculture_form")]
        
        return events


class ValidateAgricultureForm(FormValidationAction):
    """Validates the slots filled in the agriculture form."""

    def name(self) -> Text:
        return "validate_agriculture_form"

    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Text]:
        """Returns the list of slots that the form has to fill."""
        requested_info = tracker.get_slot("requested_info")
        
        if requested_info == "variety_yield":
            return ["crop", "variety"]
        return ["crop"]

    async def validate_crop(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate crop value."""
        supported_crops = ["brinjal", "capsicum", "potato", "rice", "wheat", "maize", 
                         "barley", "sunflower", "chickpeas", "cotton", "sugarcane",
                         "lentils", "sorghum", "groundnut", "mustard", "millet", "soybean"]
        
        if slot_value.lower() in supported_crops:
            return {"crop": slot_value.lower()}
        
        dispatcher.utter_message(text=f"I don't have information about {slot_value}. Please choose from our supported crops.")
        return {"crop": None}

    async def validate_variety(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate variety value."""
        if slot_value:
            return {"variety": slot_value}
        
        dispatcher.utter_message(text="Please provide a valid variety name.")
        return {"variety": None}


class ActionSubmitAgricultureForm(Action):
    """Defines what to do after all the form slots are filled."""

    def name(self) -> Text:
        return "action_submit_agriculture_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        requested_info = tracker.get_slot("requested_info")
        crop = tracker.get_slot("crop")
        variety = tracker.get_slot("variety")
        
        # Map requested_info to appropriate utterance
        info_to_utterance = {
            'crop_info': 'utter_crop_info',
            'disease_control': 'utter_disease_control',
            'nutrient_requirement': 'utter_nutrient_requirement',
            'pest_control': 'utter_pest_control',
            'fertilizer_requirement': 'utter_fertilizer_requirement',
            'variety_yield': 'utter_variety_yield',
            'deficiency_info': 'utter_deficiency_info',
            'best_practices': 'utter_best_practices',
            'crop_rotation': 'utter_crop_rotation',
            'harvesting_time': 'utter_harvesting_time',
            'insecticide_info': 'utter_insecticide_info',
            'disease_prevention': 'utter_disease_prevention',
            'natural_pest_control': 'utter_natural_pest_control',
            'fungicide_info': 'utter_fungicide_info',
            'pest_detection': 'utter_pest_detection',
            'fertilizer_schedule': 'utter_fertilizer_schedule',
            'fertilizer_application_method': 'utter_fertilizer_application_method',
            'organic_fertilizer': 'utter_organic_fertilizer',
            'water_requirement': 'utter_water_requirement',
            'irrigation_methods': 'utter_irrigation_methods',
            'drainage': 'utter_drainage',
            'climate_requirements': 'utter_climate_requirements',
            'weather_impact': 'utter_weather_impact',
            'drought_management': 'utter_drought_management',
            'crop_rotation_benefits': 'utter_crop_rotation_benefits',
            'mixed_farming_techniques': 'utter_mixed_farming_techniques',
            'crop_compatibility': 'utter_crop_compatibility',
            'soil_type': 'utter_soil_type',
            'soil_preparation': 'utter_soil_preparation'
        }
        
        # Get the appropriate utterance based on requested_info
        utterance = info_to_utterance.get(requested_info)
        
        if utterance:
            # Call the appropriate utterance
            dispatcher.utter_message(response=utterance)
        else:
            # Default response if no matching utterance is found
            dispatcher.utter_message(text=f"I have information about {crop}, but I'm not sure what specific information you're looking for.")
        
        # Clear the slots for the next conversation
        return [SlotSet("requested_slot", None)]
