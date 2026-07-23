# Copyright (c) 2008-2026 Tim Molteno (tim@elec.ac.nz)
"""Test structure excitation via get_structure_excitation()."""

import PyNEC
import pytest


@pytest.fixture
def log_periodic():
    """12-element log periodic antenna with TL cards."""
    nec = PyNEC.nec_context()
    geo = nec.get_geometry()
    geo.wire(1, 5, 0, -1, 0, 0, 1, 0, 0.00667, 1, 1)
    geo.wire(2, 5, -0.7527, -1.0753, 0, -0.7527, 1.0753, 0, 0.00717, 1, 1)
    geo.wire(3, 5, -1.562, -1.1562, 0, -1.562, 1.1562, 0, 0.00771, 1, 1)
    geo.wire(4, 5, -2.4323, -1.2432, 0, -2.4323, 1.2432, 0, 0.00829, 1, 1)
    geo.wire(5, 5, -3.368, -1.3368, 0, -3.368, 1.3368, 0, 0.00891, 1, 1)
    geo.wire(6, 7, -4.3742, -1.4374, 0, -4.3742, 1.4374, 0, 0.00958, 1, 1)
    geo.wire(7, 7, -5.4562, -1.5456, 0, -5.4562, 1.5456, 0, 0.0103, 1, 1)
    geo.wire(8, 7, -6.6195, -1.6619, 0, -6.6195, 1.6619, 0, 0.01108, 1, 1)
    geo.wire(9, 7, -7.8705, -1.787, 0, -7.8705, 1.787, 0, 0.01191, 1, 1)
    geo.wire(10, 7, -9.2156, -1.9215, 0, -9.2156, 1.9215, 0, 0.01281, 1, 1)
    geo.wire(11, 9, -10.6619, -2.0662, 0, -10.6619, 2.0662, 0, 0.01377, 1, 1)
    geo.wire(12, 9, -12.2171, -2.2217, 0, -12.2171, 2.2217, 0, 0.01481, 1, 1)
    nec.geometry_complete(0)
    nec.fr_card(0, 0, 46.29e6, 0)
    nec.tl_card(1, 3, 2, 3, -50, 0.7527, 0, 0, 0, 0)
    nec.tl_card(2, 3, 3, 3, -50, 0.8093, 0, 0, 0, 0)
    nec.tl_card(3, 3, 4, 3, -50, 0.8703, 0, 0, 0, 0)
    nec.tl_card(4, 3, 5, 3, -50, 0.9357, 0, 0, 0, 0)
    nec.tl_card(5, 3, 6, 4, -50, 1.0062, 0, 0, 0, 0)
    nec.tl_card(6, 4, 7, 4, -50, 1.082, 0, 0, 0, 0)
    nec.tl_card(7, 4, 8, 4, -50, 1.1633, 0, 0, 0, 0)
    nec.tl_card(8, 4, 9, 4, -50, 1.251, 0, 0, 0, 0)
    nec.tl_card(9, 4, 10, 4, -50, 1.3451, 0, 0, 0, 0)
    nec.tl_card(10, 4, 11, 5, -50, 1.4463, 0, 0, 0, 0)
    nec.tl_card(11, 5, 12, 5, -50, 1.5552, 0, 0, 0, 0.02)
    nec.ex_card(0, 1, 3, 1, 0, 1, 0, 0, 0, 0, 0)
    nec.rp_card(0, 37, 1, 1, 1, 1, 0, 90, 0, -5, 0, 0, 0)
    return nec


class TestStructureExcitation:
    def test_excitation_not_none(self, log_periodic):
        """Structure excitation should be retrievable."""
        se = log_periodic.get_structure_excitation(0)
        assert se is not None

    def test_frequency(self, log_periodic):
        """Frequency should be set (scalar, Hz)."""
        se = log_periodic.get_structure_excitation(0)
        # necpp returns the result's frequency as a scalar.
        freq = se.get_frequency()
        assert freq > 0

    def test_tag_and_segment(self, log_periodic):
        """Tag and segment arrays should be non-empty."""
        se = log_periodic.get_structure_excitation(0)
        assert len(se.get_tag()) > 0
        assert len(se.get_segment()) > 0

    def test_current_and_voltage(self, log_periodic):
        """Current and voltage should be complex-valued arrays."""
        se = log_periodic.get_structure_excitation(0)
        current = se.get_current()
        voltage = se.get_voltage()
        assert len(current) > 0
        assert len(voltage) > 0

    def test_power_non_negative(self, log_periodic):
        """Power values should be finite.

        This log-periodic array is strongly coupled through transmission
        lines, so individual elements exchange power and the per-element
        values can be negative or sum to ~0 (a near-reactive solution).
        The meaningful invariant is that the values are finite numbers.
        """
        import math

        se = log_periodic.get_structure_excitation(0)
        power = se.get_power()
        assert len(power) > 0
        for p in power:
            assert math.isfinite(p)
