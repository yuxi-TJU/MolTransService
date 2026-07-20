#!/usr/bin/env python3

from __future__ import annotations

import math
from pathlib import Path


SOURCE_FILE = Path(__file__).with_name("dpdp_0_0_0.xyz")
ANGLE_VALUES = list(range(0, 91, 15))
TORSION_BONDS = {
    "A": (12, 13),
    "B": (22, 23),
    "C": (30, 31),
}
EPSILON = 1.0e-8


def read_xyz(path: Path) -> tuple[list[str], list[list[float]], str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    atom_count = int(lines[0].strip())
    comment = lines[1] if len(lines) > 1 else ""
    atom_lines = lines[2 : 2 + atom_count]
    symbols: list[str] = []
    coords: list[list[float]] = []
    for line in atom_lines:
        fields = line.split()
        if len(fields) != 4:
            raise ValueError(f"Unexpected XYZ line: {line!r}")
        symbols.append(fields[0])
        coords.append([float(fields[1]), float(fields[2]), float(fields[3])])
    if len(symbols) != atom_count:
        raise ValueError("XYZ atom count does not match the number of coordinate lines.")
    return symbols, coords, comment


def write_xyz(path: Path, symbols: list[str], coords: list[list[float]], comment: str) -> None:
    lines = [str(len(symbols)), comment]
    for symbol, (x, y, z) in zip(symbols, coords):
        lines.append(f"{symbol:<2} {x:16.8f} {y:16.8f} {z:16.8f}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def vec_sub(a: list[float], b: list[float]) -> list[float]:
    return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]


def vec_add(a: list[float], b: list[float]) -> list[float]:
    return [a[0] + b[0], a[1] + b[1], a[2] + b[2]]


def vec_scale(v: list[float], scalar: float) -> list[float]:
    return [v[0] * scalar, v[1] * scalar, v[2] * scalar]


def vec_dot(a: list[float], b: list[float]) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def vec_cross(a: list[float], b: list[float]) -> list[float]:
    return [
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    ]


def vec_norm(v: list[float]) -> float:
    return math.sqrt(vec_dot(v, v))


def vec_unit(v: list[float]) -> list[float]:
    norm = vec_norm(v)
    if norm < EPSILON:
        raise ValueError("Cannot normalize a near-zero vector.")
    return [v[0] / norm, v[1] / norm, v[2] / norm]


def rotate_point_around_axis(
    point: list[float],
    axis_start: list[float],
    axis_end: list[float],
    angle_deg: float,
) -> list[float]:
    if abs(angle_deg) < EPSILON:
        return point[:]

    axis_vector = vec_unit(vec_sub(axis_end, axis_start))
    shifted = vec_sub(point, axis_start)
    angle_rad = math.radians(angle_deg)
    cos_theta = math.cos(angle_rad)
    sin_theta = math.sin(angle_rad)

    term1 = vec_scale(shifted, cos_theta)
    term2 = vec_scale(vec_cross(axis_vector, shifted), sin_theta)
    term3 = vec_scale(axis_vector, vec_dot(axis_vector, shifted) * (1.0 - cos_theta))
    rotated = vec_add(vec_add(term1, term2), term3)
    return vec_add(axis_start, rotated)


def build_torsion_groups(base_coords: list[list[float]]) -> dict[str, dict[str, list[int] | tuple[int, int]]]:
    groups: dict[str, dict[str, list[int] | tuple[int, int]]] = {}
    for label, (atom1, atom2) in TORSION_BONDS.items():
        idx1 = atom1 - 1
        idx2 = atom2 - 1
        if base_coords[idx1][2] <= base_coords[idx2][2]:
            low_idx, high_idx = idx1, idx2
        else:
            low_idx, high_idx = idx2, idx1

        low_z = base_coords[low_idx][2]
        high_z = base_coords[high_idx][2]
        lower_group = [i for i, coord in enumerate(base_coords) if coord[2] < low_z - EPSILON]
        upper_group = [i for i, coord in enumerate(base_coords) if coord[2] > high_z + EPSILON]
        between = [
            i
            for i, coord in enumerate(base_coords)
            if low_z + EPSILON < coord[2] < high_z - EPSILON
        ]
        if between:
            raise ValueError(
                f"Unexpected atoms located between torsion-axis atoms for {label}: "
                + ", ".join(str(i + 1) for i in between)
            )

        groups[label] = {
            "axis": (low_idx, high_idx),
            "lower_group": lower_group,
            "upper_group": upper_group,
        }
    return groups


def apply_symmetric_torsion(
    coords: list[list[float]],
    axis_indices: tuple[int, int],
    lower_group: list[int],
    upper_group: list[int],
    angle_deg: float,
) -> None:
    if abs(angle_deg) < EPSILON:
        return

    axis_start = coords[axis_indices[0]][:]
    axis_end = coords[axis_indices[1]][:]
    lower_rotation = -angle_deg / 2.0
    upper_rotation = angle_deg / 2.0

    for idx in lower_group:
        coords[idx] = rotate_point_around_axis(coords[idx], axis_start, axis_end, lower_rotation)
    for idx in upper_group:
        coords[idx] = rotate_point_around_axis(coords[idx], axis_start, axis_end, upper_rotation)


def generate_structure(
    base_coords: list[list[float]],
    groups: dict[str, dict[str, list[int] | tuple[int, int]]],
    angle_a: int,
    angle_b: int,
    angle_c: int,
) -> list[list[float]]:
    coords = [coord[:] for coord in base_coords]
    for label, angle in (("A", angle_a), ("B", angle_b), ("C", angle_c)):
        group = groups[label]
        apply_symmetric_torsion(
            coords,
            group["axis"],  # type: ignore[arg-type]
            group["lower_group"],  # type: ignore[arg-type]
            group["upper_group"],  # type: ignore[arg-type]
            angle,
        )
    return coords


def main() -> None:
    symbols, base_coords, source_comment = read_xyz(SOURCE_FILE)
    groups = build_torsion_groups(base_coords)
    source_stem = SOURCE_FILE.stem
    if source_stem.endswith("_0_0_0"):
        output_stem = source_stem[: -len("_0_0_0")]
    else:
        output_stem = source_stem

    structure_count = 0
    for angle_a in ANGLE_VALUES:
        a_dir = SOURCE_FILE.parent / f"A_{angle_a:03d}"
        for angle_b in ANGLE_VALUES:
            b_dir = a_dir / f"B_{angle_b:03d}"
            for angle_c in ANGLE_VALUES:
                c_dir = b_dir / f"C_{angle_c:03d}"
                c_dir.mkdir(parents=True, exist_ok=True)

                coords = generate_structure(base_coords, groups, angle_a, angle_b, angle_c)
                filename = f"{output_stem}_A{angle_a:03d}_B{angle_b:03d}_C{angle_c:03d}.xyz"
                comment = (
                    f"{source_comment.strip()} | "
                    f"A={angle_a:03d} B={angle_b:03d} C={angle_c:03d} | "
                    "symmetric torsion rotation"
                )
                write_xyz(c_dir / filename, symbols, coords, comment)
                structure_count += 1

    print(f"Generated {structure_count} structures under {SOURCE_FILE.parent}")


if __name__ == "__main__":
    main()
