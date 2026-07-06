# Copyright (c) 2008-2026 Tim Molteno (tim@elec.ac.nz)
"""Test antenna input parameters via get_input_parameters()."""

import PyNEC
import pytest


@pytest.fixture
def simple_dipole():
    """Simple center-fed dipole at 200 MHz, two excitations."""
    nec = PyNEC.nec_context()
    geo = nec.get_geometry()
    geo.wire(0, 8, 0, 0, -0.25, 0, 0, 0.25, 0.00001, 1, 1)
    nec.geometry_complete(0)
    nec.fr_card(0, 3, 200.0, 50.0)
    nec.ex_card(5, 0, 5, 0, 0, 1, 0, 0, 0, 0, 0)
    nec.ex_card(5, 0, 4, 0, 0, 1, 0, 0, 0, 0, 0)
    nec.xq_card(0)
    return nec


class TestInputParameters:
    def test_multiple_excitations(self, simple_dipole):
        """Two excitations should produce two input parameter sets."""
        ai0 = simple_dipole.get_input_parameters(0)
        ai1 = simple_dipole.get_input_parameters(1)

        assert ai0 is not None
        assert ai1 is not None

    def test_impedance_is_finite(self, simple_dipole):
        """Impedance values should be finite complex numbers."""
        ai = simple_dipole.get_input_parameters(0)
        z = ai.get_impedance()

        assert len(z) > 0
        for val in z:
            assert abs(val.real) < 1e6
            assert abs(val.imag) < 1e6

    def test_current_and_voltage(self, simple_dipole):
        """Current and voltage arrays should be non-empty."""
        ai = simple_dipole.get_input_parameters(0)
        current = ai.get_current()
        voltage = ai.get_voltage()

        assert len(current) > 0
        assert len(voltage) > 0

    def test_power_non_negative(self, simple_dipole):
        """Power should be non-negative."""
        ai = simple_dipole.get_input_parameters(0)
        power = ai.get_power()

        assert len(power) > 0
        for p in power:
            assert p >= 0

    def test_frequency_matches(self, simple_dipole):
        """Returned frequency should match the FR card."""
        ai = simple_dipole.get_input_parameters(0)
        freqs = ai.get_frequency()

        assert len(freqs) > 0
        # FR card set 200 MHz with 50 MHz step, 3 frequencies
        assert abs(freqs[0] - 200.0) < 1.0

    def test_tag_and_segment(self, simple_dipole):
        """Tag and segment arrays should be non-empty."""
        ai = simple_dipole.get_input_parameters(0)
        tags = ai.get_tag()
        segs = ai.get_segment()

        assert len(tags) > 0
        assert len(segs) > 0
