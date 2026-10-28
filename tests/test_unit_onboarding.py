#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tests/test_unit_onboarding.py — Unit test cho OnboardingWizard (Preflight checks, Brand setup, Asset verification).
"""

import os
import sys
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from workflows.onboarding import OnboardingWizard


class TestOnboarding(unittest.TestCase):
    def test_preflight_environment(self):
        wizard = OnboardingWizard()
        res = wizard.check_preflight_environment()
        self.assertIn("python", res)
        self.assertTrue(res["python"]["ok"])
        self.assertIn("ffmpeg", res)
        self.assertIn("capcut", res)

    def test_verify_assets(self):
        wizard = OnboardingWizard()
        has_assets = wizard.verify_assets_and_models()
        self.assertTrue(has_assets)


if __name__ == "__main__":
    unittest.main()
