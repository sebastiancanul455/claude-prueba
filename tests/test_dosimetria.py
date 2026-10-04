import numpy as np
import pytest

from claude_prueba.dosimetria import gamma_1d, perfil_gaussiano, tasa_aprobacion_gamma

X = np.arange(-50.0, 51.0, 1.0)  # mm


def test_perfil_gaussiano_maximo_en_el_centro():
    perfil = perfil_gaussiano(X, centro_mm=0.0, sigma_mm=10.0, amplitud=2.0)
    assert perfil.max() == pytest.approx(2.0)
    assert X[perfil.argmax()] == 0.0
    assert perfil[X == -10.0] == pytest.approx(perfil[X == 10.0])


def test_perfil_gaussiano_sigma_invalida():
    with pytest.raises(ValueError):
        perfil_gaussiano(X, sigma_mm=0.0)


def test_gamma_perfiles_identicos_es_cero():
    ref = perfil_gaussiano(X)
    gamma = gamma_1d(X, ref, X, ref)
    assert np.allclose(gamma, 0.0)
    assert tasa_aprobacion_gamma(gamma) == 1.0


def test_gamma_escala_dentro_de_tolerancia_aprueba():
    ref = perfil_gaussiano(X)
    gamma = gamma_1d(X, ref, X, ref * 1.02, dd=0.03, dta_mm=3.0)
    assert tasa_aprobacion_gamma(gamma) == 1.0


def test_gamma_escala_fuera_de_tolerancia_falla_en_el_pico():
    ref = perfil_gaussiano(X)
    gamma = gamma_1d(X, ref, X, ref * 1.10, dd=0.03, dta_mm=3.0)
    assert tasa_aprobacion_gamma(gamma) < 1.0
    assert gamma[X == 0.0][0] > 1.0


def test_gamma_desplazamiento_de_1_mm_aprueba_con_dta_3_mm():
    ref = perfil_gaussiano(X, centro_mm=0.0)
    desplazado = perfil_gaussiano(X, centro_mm=1.0)
    gamma = gamma_1d(X, ref, X, desplazado, dd=0.03, dta_mm=3.0)
    assert np.nanmax(gamma) <= 1.0


def test_gamma_umbral_excluye_puntos_de_baja_dosis():
    ref = perfil_gaussiano(X)
    gamma = gamma_1d(X, ref, X, ref, umbral=0.10)
    assert np.isnan(gamma[X == 50.0][0])
    assert not np.isnan(gamma[X == 0.0][0])


def test_gamma_valida_entradas():
    ref = perfil_gaussiano(X)
    with pytest.raises(ValueError):
        gamma_1d(X, ref[:-1], X, ref)
    with pytest.raises(ValueError):
        gamma_1d(X, ref, X, ref, dd=0.0)
    with pytest.raises(ValueError):
        gamma_1d(X, np.zeros_like(X), X, ref)


def test_tasa_aprobacion_sin_puntos_validos():
    with pytest.raises(ValueError):
        tasa_aprobacion_gamma(np.array([np.nan, np.nan]))
