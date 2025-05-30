#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import unittest
from rasa.shared.importers.rasa import RasaFileImporter
from rasa.shared.core.domain import Domain
from rasa.shared.core.training_data.structures import StoryGraph
from rasa.shared.nlu.training_data.training_data import TrainingData
from rasa.shared.importers.importer import TrainingDataImporter

class TestRasaFiles(unittest.TestCase):
    """Test class to verify that all RASA files are valid and consistent."""

    async def test_domain_is_valid(self):
        """Test that the domain file is valid."""
        importer = RasaFileImporter()
        domain = await importer.get_domain()
        self.assertIsInstance(domain, Domain)
        
    async def test_nlu_data_is_valid(self):
        """Test that the NLU data is valid."""
        importer = RasaFileImporter()
        nlu_data = await importer.get_nlu_data()
        self.assertIsInstance(nlu_data, TrainingData)
        
    async def test_stories_are_valid(self):
        """Test that the stories are valid."""
        importer = RasaFileImporter()
        story_graph = await importer.get_stories()
        self.assertIsInstance(story_graph, StoryGraph)
        
    async def test_intents_have_examples(self):
        """Test that all intents have training examples."""
        importer = RasaFileImporter()
        domain = await importer.get_domain()
        nlu_data = await importer.get_nlu_data()
        
        for intent in domain.intents:
            # Skip default intents that might not have examples
            if intent in ["out_of_scope", "nlu_fallback", "restart", "back", "session_start"]:
                continue
            self.assertTrue(
                any(example.get("intent") == intent for example in nlu_data.intent_examples),
                f"Intent '{intent}' has no training examples"
            )
            
    async def test_all_utterances_are_used(self):
        """Test that all utterances defined in the domain are used in stories or rules."""
        importer = RasaFileImporter()
        domain = await importer.get_domain()
        story_graph = await importer.get_stories()
        
        # Extract all utterances from stories
        story_utterances = set()
        for story in story_graph.story_steps:
            for event in story.events:
                if event.type_name == "action" and event.action_name.startswith("utter_"):
                    story_utterances.add(event.action_name)
        
        # Check that all domain utterances are used
        for utterance in domain.templates.keys():
            if utterance.startswith("utter_"):
                self.assertIn(
                    utterance, 
                    story_utterances, 
                    f"Utterance '{utterance}' is defined in domain but not used in stories or rules"
                )

if __name__ == "__main__":
    unittest.main()
