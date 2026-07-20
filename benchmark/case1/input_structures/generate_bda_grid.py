#!/usr/bin/env python3
"""Generate biphenyl diamine conformers by scanning torsions θ and φ.

Starting geometry: theta_000_phi_000.xyz (1-based atom indices).
 - Set θ via dihedral(9,13,14,17) by rotating atoms 14–26 about bond 13–14.
 - Set φ simultaneously on both terminal groups:
     * dihedral(1,3,4,7): rotate atoms [1,2,3] about bond 3–4.
     * dihedral(25,24,23,19): rotate atoms [24,25,26] about bond 24–23.
Outputs are written as structures/theta_XXX_phi_YYY.xyz for θ in [0,90] step 5
and φ in [0,180] step 10.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import List, Tuple

import numpy as np


def read_xyz(path: Path) -> Tuple[List[str], np.ndarray, str]:
    lines = path.read_text().splitlines()
    try:
        natoms = int(lines[0].strip())
    except Exception as exc:  # pragma: no cover - defensive parse
        raise ValueError(f"Cannot read atom count from {path}") from exc

    comment = lines[1].strip() if len(lines) > 1 else ""
    entries = lines[2 : 2 + natoms]
    if len(entries) != natoms:
        raise ValueError(f"Expected {natoms} atom lines in {path}, found {len(entries)}")

    symbols: List[str] = []
    coords = np.zeros((natoms, 3), dtype=float)
    for i, line in enumerate(entries):
        parts = line.split()
        if len(parts) < 4:
            raise ValueError(f"Bad atom line {i+3} in {path}: {line}")
        symbols.append(parts[0])
        coords[i] = [float(x) for x in parts[1:4]]
    return symbols, coords, comment


def write_xyz(path: Path, symbols: List[str], coords: np.ndarray, comment: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    natoms = len(symbols)
    with path.open("w") as f:
        f.write(f"{natoms}\n")
        f.write(f"{comment}\n")
        for sym, (x, y, z) in zip(symbols, coords):
            f.write(f"{sym:2s}  {x: .8f}  {y: .8f}  {z: .8f}\n")


def rotation_matrix(axis: np.ndarray, angle_rad: float) -> np.ndarray:
    axis = axis / np.linalg.norm(axis)
    x, y, z = axis
    c = math.cos(angle_rad)
    s = math.sin(angle_rad)
    C = 1 - c
    # Rodrigues rotation matrix
    return np.array(
        [
            [c + x * x * C, x * y * C - z * s, x * z * C + y * s],
            [y * x * C + z * s, c + y * y * C, y * z * C - x * s],
            [z * x * C - y * s, z * y * C + x * s, c + z * z * C],
        ]
    )


def dihedral_deg(coords: np.ndarray, i: int, j: int, k: int, l: int) -> float:
    p1, p2, p3, p4 = coords[[i, j, k, l]]
    b1 = p2 - p1
    b2 = p3 - p2
    b3 = p4 - p3

    # Normalize b2 for projection
    b2_unit = b2 / np.linalg.norm(b2)
    v = b1 - np.dot(b1, b2_unit) * b2_unit
    w = b3 - np.dot(b3, b2_unit) * b2_unit

    x = np.dot(v, w)
    y = np.dot(np.cross(b2_unit, v), w)
    angle = math.degrees(math.atan2(y, x))
    return angle


def wrap_delta(target: float, current: float) -> float:
    """Smallest signed delta (degrees) to reach target from current."""
    delta = target - current
    while delta <= -180:
        delta += 360
    while delta > 180:
        delta -= 360
    return delta


def rotate_subset(coords: np.ndarray, pivot_a: int, pivot_b: int, indices: List[int], angle_deg: float) -> None:
    axis = coords[pivot_b] - coords[pivot_a]
    norm = np.linalg.norm(axis)
    if norm < 1e-8:
        raise ValueError("Pivot atoms are coincident; cannot define rotation axis")
    R = rotation_matrix(axis, math.radians(angle_deg))
    origin = coords[pivot_a]
    for idx in indices:
        coords[idx] = origin + R @ (coords[idx] - origin)


def generate_grid(base: Path, out_dir: Path) -> None:
    symbols, base_coords, comment = read_xyz(base)

    theta_targets = list(range(0, 91, 5))  # 0..90 inclusive
    phi_targets = list(range(0, 181, 10))  # 0..180 inclusive

    # 1-based to 0-based indices for internal use
    theta_mobile = [i - 1 for i in range(14, 27)]
    theta_pivots = (12, 13)  # atoms 13 and 14

    phi_top_mobile = [i - 1 for i in [1, 2, 3]]
    phi_top_pivots = (2, 3)  # atoms 3 and 4

    phi_bottom_mobile = [i - 1 for i in [24, 25, 26]]
    phi_bottom_pivots = (23, 22)  # atoms 24 and 23

    comment_base = comment or "generated torsion scan"

    for theta in theta_targets:
        for phi in phi_targets:
            coords = base_coords.copy()

            # Apply φ to top amine (1,3,4,7)
            current_phi_top = dihedral_deg(coords, 0, 2, 3, 6)
            delta_phi_top = wrap_delta(phi, current_phi_top)
            rotate_subset(coords, phi_top_pivots[0], phi_top_pivots[1], phi_top_mobile, delta_phi_top)

            # Apply the same φ to bottom amine (25,24,23,19)
            current_phi_bottom = dihedral_deg(coords, 24, 23, 22, 18)
            delta_phi_bottom = wrap_delta(phi, current_phi_bottom)
            rotate_subset(coords, phi_bottom_pivots[0], phi_bottom_pivots[1], phi_bottom_mobile, delta_phi_bottom)

            # Apply θ to the biphenyl bond (9,13,14,17)
            current_theta = dihedral_deg(coords, 8, 12, 13, 16)
            delta_theta = wrap_delta(theta, current_theta)
            rotate_subset(coords, theta_pivots[0], theta_pivots[1], theta_mobile, delta_theta)

            outfile = out_dir / f"theta_{theta:03d}_phi_{phi:03d}.xyz"
            comment_line = f"theta={theta} phi={phi} | {comment_base}"
            write_xyz(outfile, symbols, coords, comment_line)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate θ/φ conformer grid for BDA")
    parser.add_argument(
        "--base",
        type=Path,
        default=Path("theta_000_phi_000.xyz"),
        help="Input XYZ with θ=0, φ=0 reference geometry",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("structures"),
        help="Output directory for generated XYZ files",
    )
    args = parser.parse_args()

    generate_grid(args.base, args.out)


if __name__ == "__main__":
    main()
