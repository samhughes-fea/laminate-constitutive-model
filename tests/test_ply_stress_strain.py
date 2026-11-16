"""One call recovers ply stress and strain from mid-plane strain and curvature."""

import numpy as np
import pytest

from laminate_constitutive_model import (
    HygrothermalEngine,
    HygrothermalState,
    Laminate,
    integrate_abd,
    ply_stress_strain,
)


def test_ply_stress_strain_matches_hand_assembly(cfrp):
    lam = Laminate.from_angles(cfrp, [0, 45, -45, 90], 0.25e-3)
    eps0 = np.array([1.0e-4, -2.0e-5, 3.0e-5])
    kappa = np.array([0.8, -0.2, 0.1])
    recovered = ply_stress_strain(lam, eps0, kappa)
    assert recovered.ply_index.tolist() == [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3]
    assert recovered.position.tolist() == ["bottom", "mid", "top"] * 4
    row = 0
    for i, (ply, (zb, zt)) in enumerate(zip(lam.plies, lam.ply_bounds())):
        for pos, z in (("bottom", zb), ("mid", 0.5 * (zb + zt)), ("top", zt)):
            eps = eps0 + z * kappa
            sigma = ply.Q_bar @ eps
            assert recovered.ply_index[row] == i
            assert recovered.position[row] == pos
            assert recovered.z[row] == pytest.approx(z)
            assert recovered.strain_global[row] == pytest.approx(eps)
            assert recovered.strain_mechanical[row] == pytest.approx(eps)
            assert recovered.stress_global[row] == pytest.approx(sigma)
            assert recovered.strain_material[row] == pytest.approx(ply.to_material_strain(eps))
            assert recovered.stress_material[row] == pytest.approx(ply.to_material_stress(sigma))
            row += 1


def test_membrane_resultants_rebuild_from_recovered_stress(cfrp):
    lam = Laminate.from_angles(cfrp, [0, 90, 90, 0], 0.25e-3)
    abd = integrate_abd(lam)
    eps0 = np.array([2.0e-4, 0.0, 0.0])
    kappa = np.zeros(3)
    nm = abd @ np.concatenate([eps0, kappa])
    recovered = ply_stress_strain(lam, eps0, kappa, positions=("mid",))
    n_from_plies = sum(sigma * ply.thickness for ply, sigma in zip(lam.plies, recovered.stress_global))
    assert n_from_plies == pytest.approx(nm[:3], rel=1e-12)


def test_hygrothermal_state_is_taken_off_the_mechanical_strain(cfrp):
    lam = Laminate.from_angles(cfrp, [0, 90], 0.5e-3)
    state = HygrothermalState(delta_temperature=40.0)
    recovered = ply_stress_strain(lam, np.zeros(3), np.zeros(3), positions=("mid",), state=state)
    engine = HygrothermalEngine()
    for row, ply in enumerate(lam.plies):
        z = recovered.z[row]
        eps_ht = engine.global_free_strain(ply, state, z, lam.offset)
        assert recovered.strain_global[row] == pytest.approx(0.0)
        assert recovered.strain_mechanical[row] == pytest.approx(-eps_ht)
        assert recovered.stress_global[row] == pytest.approx(ply.Q_bar @ (-eps_ht))


def test_unknown_position_is_refused(cfrp):
    lam = Laminate.from_angles(cfrp, [0], 1e-3)
    with pytest.raises(ValueError, match="positions"):
        ply_stress_strain(lam, np.zeros(3), np.zeros(3), positions=("centre",))
