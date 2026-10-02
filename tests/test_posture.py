from desk_coach.posture import Proximity


def test_no_face_result_is_explicit():
    result = Proximity(False, False, None)
    assert result.face_detected is False
    assert result.face_width_ratio is None


def test_close_face_hint_has_a_bounded_width_ratio():
    result = Proximity(True, True, 0.42)
    assert result.face_detected and result.too_close
    assert 0 < result.face_width_ratio < 1
