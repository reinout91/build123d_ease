"""Tests for the `fetch faces` module."""

from math import isclose, pi

import build123d as bd

import build123d_ease as bde


def test_cylindrical_faces_of_find_hole() -> None:
    """Validate finding a cylindrical face for a hole."""
    r = 10
    h = 10
    p = (
        bd.Part(None)
        + bd.Box(length=30, width=30, height=30)
        - bd.Cylinder(
            radius=r,
            height=h,
            align=bde.align.ANCHOR_TOP,
        )
    )
    cylindrical_face: bd.Face = bde.cylindrical_faces_of(p, cylinder_type="hole")[0]
    expected_face_area = 2 * pi * r * h
    assert isclose(cylindrical_face.area, expected_face_area, rel_tol=1e-6)


def test_cylindrical_faces_of_find_pin() -> None:
    """Validate finding a cylindrical face for a pin."""
    r = 10
    h = 10
    p = (
        bd.Part(None)
        + bd.Box(length=30, width=60, height=30, align=bde.align.ANCHOR_BOTTOM)
        + bd.Cylinder(
            radius=r,
            height=h,
            align=bde.align.ANCHOR_TOP,
        )
    )
    cylindrical_face = bde.cylindrical_faces_of(p, cylinder_type="pin")[0]
    expected_face_area = 2 * pi * r * h
    assert isclose(cylindrical_face.area, expected_face_area, rel_tol=1e-6)


def test_cylindrical_faces_of_find_all() -> None:
    """Validate finding cylindrical faces, one hole and one pin."""
    r = 10
    h = 10
    p = (
        bd.Part(None)
        + bd.Box(length=30, width=60, height=30, align=bde.align.ANCHOR_BOTTOM)
        + bd.Cylinder(
            radius=r,
            height=h,
            align=bde.align.ANCHOR_TOP,
        )
        - bd.Cylinder(radius=0.5 * r, height=h, align=bde.align.ANCHOR_TOP)
    )
    cylindrical_faces_of = bde.cylindrical_faces_of(p)
    expected_face_area_pin = 2 * pi * r * h
    expected_face_area_hole = 2 * pi * 0.5 * r * h

    assert isclose(cylindrical_faces_of[0].area, expected_face_area_pin, rel_tol=1e-6)
    assert isclose(cylindrical_faces_of[1].area, expected_face_area_hole, rel_tol=1e-6)
