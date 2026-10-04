"""Utilidades de dosimetría con datos sintéticos.

EJEMPLO EDUCATIVO: no está validado para uso clínico.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray


def perfil_gaussiano(
    x_mm: ArrayLike,
    centro_mm: float = 0.0,
    sigma_mm: float = 10.0,
    amplitud: float = 1.0,
) -> NDArray[np.float64]:
    """Perfil de dosis gaussiano sintético (útil para probar sin datos de pacientes).

    Args:
        x_mm: posiciones en milímetros.
        centro_mm: posición del máximo, en milímetros.
        sigma_mm: desviación estándar, en milímetros.
        amplitud: dosis máxima (unidades arbitrarias).
    """
    if sigma_mm <= 0:
        raise ValueError("sigma_mm debe ser positiva")
    x = np.asarray(x_mm, dtype=float)
    return np.asarray(amplitud * np.exp(-((x - centro_mm) ** 2) / (2 * sigma_mm**2)))


def gamma_1d(
    x_ref_mm: ArrayLike,
    dosis_ref: ArrayLike,
    x_eval_mm: ArrayLike,
    dosis_eval: ArrayLike,
    dd: float = 0.03,
    dta_mm: float = 3.0,
    umbral: float = 0.0,
) -> NDArray[np.float64]:
    """Índice gamma 1D global (sin interpolación) de un perfil evaluado vs. uno de referencia.

    El criterio de dosis es relativo al máximo de la referencia (normalización global).
    Sin interpolar, el resultado depende de la resolución de la malla: con mallas gruesas
    el gamma queda sobreestimado.

    Args:
        x_ref_mm: posiciones de la referencia, en milímetros.
        dosis_ref: dosis de la referencia.
        x_eval_mm: posiciones del perfil evaluado, en milímetros.
        dosis_eval: dosis del perfil evaluado (mismas unidades que la referencia).
        dd: diferencia de dosis, como fracción del máximo de la referencia (3 % -> 0.03).
        dta_mm: distancia de acuerdo (distance-to-agreement), en milímetros.
        umbral: fracción del máximo de la referencia por debajo de la cual el punto se
            excluye (se devuelve NaN).

    Returns:
        Gamma de cada punto de la referencia (NaN en los puntos excluidos por el umbral).
    """
    if dd <= 0 or dta_mm <= 0:
        raise ValueError("dd y dta_mm deben ser positivos")
    x_ref = np.asarray(x_ref_mm, dtype=float)
    d_ref = np.asarray(dosis_ref, dtype=float)
    x_eval = np.asarray(x_eval_mm, dtype=float)
    d_eval = np.asarray(dosis_eval, dtype=float)
    if x_ref.shape != d_ref.shape or x_eval.shape != d_eval.shape:
        raise ValueError("Las posiciones y las dosis deben tener la misma forma")
    if x_ref.ndim != 1 or x_eval.ndim != 1:
        raise ValueError("Se esperan perfiles 1D")

    dosis_norm = float(d_ref.max())
    if dosis_norm <= 0:
        raise ValueError("El máximo de la dosis de referencia debe ser positivo")

    dist2 = ((x_eval[None, :] - x_ref[:, None]) / dta_mm) ** 2
    dif2 = ((d_eval[None, :] - d_ref[:, None]) / (dd * dosis_norm)) ** 2
    gamma = np.sqrt((dist2 + dif2).min(axis=1))
    gamma[d_ref < umbral * dosis_norm] = np.nan
    return np.asarray(gamma)


def tasa_aprobacion_gamma(gamma: ArrayLike) -> float:
    """Fracción de puntos con gamma <= 1, ignorando los NaN (puntos excluidos)."""
    g = np.asarray(gamma, dtype=float)
    validos = g[~np.isnan(g)]
    if validos.size == 0:
        raise ValueError("No hay puntos válidos para evaluar")
    return float(np.mean(validos <= 1.0))
