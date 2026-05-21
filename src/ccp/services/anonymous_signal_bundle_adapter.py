class AnonymousSignalBundleAdapter:
    def adapt(self, audit_asset):
        # Mocks a SignalBundle for the TraitScoringEngine
        return {"type": "mock_signal_bundle", "asset": audit_asset}
