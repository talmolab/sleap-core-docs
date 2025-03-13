from sleap.gui.dialogs.formbuilder import FormBuilderModalDialog

def get_export_options(parent=None):
    """Show the export labels dialog and return the selected options."""
    dialog = FormBuilderModalDialog(form_name="export_labels_form", parent=parent)
    dialog.setWindowTitle("Export Labels Package")
    return dialog.get_results()