from sleap.gui.widgets.slider import VideoSlider, set_slider_marks_from_labels
import pytest


def test_slider(qtbot, centered_pair_predictions):

    labels = centered_pair_predictions

    slider = VideoSlider(min=0, max=1200, val=15, marks=(10, 15))

    assert slider.value_range == 1200

    assert slider.value() == 15
    slider.setValue(20)
    assert slider.value() == 20

    assert slider.getSelection() == (0, 0)
    slider.startSelection(3)
    slider.endSelection(5)
    assert slider.getSelection() == (3, 5)
    slider.clearSelection()
    assert slider.getSelection() == (0, 0)

    initial_height = slider.maximumHeight()
    slider.setNumberOfTracks(20)
    assert slider.maximumHeight() != initial_height

    set_slider_marks_from_labels(slider, labels, labels.videos[0])
    assert len(slider.getMarks("track")) == 40

    slider.moveSelectionAnchor(5, 5)
    slider.releaseSelectionAnchor(100, 15)
    assert slider.getSelection() == (slider._toVal(5), slider._toVal(100))

    slider.setSelection(20, 30)
    assert slider.getSelection() == (20, 30)

    slider.setEnabled(False)
    assert not slider.enabled()

    slider.setEnabled(True)
    assert slider.enabled()


@pytest.mark.parametrize(
    "slider_width, x_value, min_value, max_value",
    [
        # Values within range
        (1000, 500, 0, 1000),  # Midpoint with no offset
        (800, 400, 0, 800),  # Exact midpoint within smaller range
        (1500, 750, 100, 1200),  # Midpoint with offset range
        (2000, 1000, 50, 1950),  # Large width and offset range
        # Values below range (no clamping expected)
        (1000, -100, 0, 1000),  # Below minimum
        # Values above range (no clamping expected)
        (1000, 1200, 0, 1000),  # Above maximum
    ],
)
def test_toVal(qtbot, slider_width, x_value, min_value, max_value):
    """
    Test _toVal scaling and transformation for varying slider widths and ranges,
    without expecting clamping behavior.

    Args:
        qtbot: The pytest-qt bot fixture.
        slider_width (int): The width of the slider in pixels.
        x_value (float): The x-coordinate on the slider to be converted to a value.
        min_value (int): The minimum value of the slider.
        max_value (int): The maximum value of the slider.
    """
    slider = VideoSlider(min=0, max=1000, val=15, marks=(10, 15))  # Initialize slider

    slider.setMinimum(min_value)  # Set slider range
    slider.setMaximum(max_value)

    slider.box_rect.setWidth(slider_width)  # Simulate visual width

    # Compute the expected raw transformed value
    expected_value = round(
        (x_value / slider_width) * (max_value - min_value) + min_value
    )

    # Assert that the raw transformation matches the expected value
    assert slider._toVal(x_value) == expected_value


def test_slider_width_property(qtbot):
    """
    Test the _slider_width property to ensure it accurately reflects
    the visual width of the slider's box_rect.
    """
    slider = VideoSlider(min=0, max=1000, val=15, marks=(10, 15))  # Initialize slider

    # Test various box_rect widths
    for width in [800, 1000, 1200, 1500]:
        slider.box_rect.setWidth(width)  # Simulate setting the visual width
        assert (
            slider._slider_width == width
        ), f"Expected _slider_width to be {width}, but got {slider._slider_width}"

    # Test edge cases with very small and large widths
    slider.box_rect.setWidth(0)
    assert (
        slider._slider_width == 1
    ), "Expected _slider_width to be 1 when box_rect width is 0"

    slider.box_rect.setWidth(10000)
    assert (
        slider._slider_width == 10000
    ), "Expected _slider_width to handle large values correctly"

@pytest.mark.parametrize(
    "invalid_value, expected_error_msg",
    [
        (None, "x position cannot be None"),
        ("invalid", "x position must be a number, got invalid"),
        ([], "x position must be a number, got []"),
        ({}, "x position must be a number, got {}"),
    ]
)
def test_toVal_invalid_input(qtbot, invalid_value, expected_error_msg):
    """
    Tests _toVal for invalid inputs to ensure ValueError is raised 
    with the correct message.

    Args:
        qtbot: Pytest fixture for Qt applications.
        invalid_value: The invalid value for x.
        expected_error_msg: The exact error message expected.

    Returns:
        None
    """
    # We use tqdm to track progress across multiple invalid inputs (optional).
    for _ in range(1):
        slider = VideoSlider(min=0, max=1000, val=15)

        with pytest.raises(ValueError) as excinfo:
            slider._toVal(invalid_value)

        # Verify the exact error message
        assert str(excinfo.value) == expected_error_msg

@pytest.mark.parametrize(
    "slider_width, x_value, handle_width, min_value, max_value",
    [
        (1000,  500,  10,   0, 1000),
        (1000,    0,  10,   0, 1000),   # Minimum x
        (1000, 1000,  10,   0, 1000),   # Maximum x
        ( 500,  250,   5, 100,  200),   # Different min/max
    ]
)
def test_toVal_center_true(qtbot, slider_width, x_value, handle_width, min_value, max_value):
    """
    Tests that _toVal correctly accounts for handle width offset when center=True.

    Args:
        qtbot: Pytest fixture for Qt applications.
        slider_width: The width of the slider box_rect.
        x_value: The x position being converted to a slider value.
        handle_width: The desired width of the slider handle rect.
        min_value: The slider's minimum value.
        max_value: The slider's maximum value.

    Returns:
        None
    """
    slider = VideoSlider(min=min_value, max=max_value, val=(min_value + max_value)//2)
    slider.box_rect.setWidth(slider_width)

    # Manually set the handle's bounding rect to the desired width.
    current_handle_rect = slider.handle.rect()
    slider.handle.setRect(
        current_handle_rect.x(),
        current_handle_rect.y(),
        handle_width,
        current_handle_rect.height()
    )

    # Read back the *actual* handle width.
    actual_handle_width = slider.handle.rect().width()

    # Manually compute the expected slider value for center=True.
    val = float(x_value) - (actual_handle_width / 2.0)
    effective_width = max(1.0, slider_width)  # Prevent zero-division
    val /= effective_width
    val *= max(1, max_value - min_value)
    val += min_value
    expected_val = round(val)

    # Call the actual function.
    actual_val = slider._toVal(x_value, center=True)

    assert actual_val == expected_val, (
        f"For x={x_value}, handle_width={actual_handle_width}, slider_width={slider_width}, "
        f"expected {expected_val}, but got {actual_val}."
    )