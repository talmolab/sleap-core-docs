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
        camera_combo = self.form_widget.fields.get("camera_category", None)

        if camera_combo:
            # Build list of available camera categories
            camera_options = []

            # Always add "All Cameras" option
            default_option = "All Cameras"
            camera_options.append(default_option)

            # Add available camera categories
            if labels.camera_categories:  # Direct access to camera_categories list
                for category in labels.camera_categories:
                    if category.cameras:  # Only add categories that have cameras
                        camera_options.append(category.name)

            # Populate the combobox with available options
            self.form_widget.fields["camera_category"].set_options(
                camera_options, default_option
            )

        self.setWindowTitle("Export Labels Options")
