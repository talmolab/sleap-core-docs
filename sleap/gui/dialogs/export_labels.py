"""
Dialog for exporting labels; shows options for export type and camera category.
"""

from sleap.gui.dialogs.formbuilder import FormBuilderModalDialog
from sleap import Labels
from qtpy.QtWidgets import QComboBox


class ExportLabelsDialog(FormBuilderModalDialog):
    """Dialog for exporting labels with options for export type and camera category."""

    def __init__(self, labels: Labels):
        """Initialize the export labels dialog.

        Args:
            labels: The Labels object containing camera categories to populate dropdown.
        """
        # Initialize parent class first
        super().__init__(form_name="export_labels_form", which_form="main")

        # Find the camera category combobox in the form layout
        camera_combo = None
        for widget in self.findChildren(QComboBox):
            if widget.objectName() == "camera_category":
                camera_combo = widget
                break

        if camera_combo:
            # Clear existing items
            camera_combo.clear()

            # Build list of available camera categories
            camera_options = []

            # Always add "All Cameras" option
            camera_options.append(("All Cameras", "all"))

            # Add available camera categories
            if (
                labels and labels.camera_categories
            ):  # Direct access to camera_categories list
                for category in labels.camera_categories:
                    if category.cameras:  # Only add categories that have cameras
                        camera_options.append((category.name, category.name))

            # Populate the combobox with available options
            for display_text, data in camera_options:
                camera_combo.addItem(display_text, data)

        self.setWindowTitle("Export Labels Options")
