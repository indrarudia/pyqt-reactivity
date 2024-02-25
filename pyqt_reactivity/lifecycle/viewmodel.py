from PyQt6.QtCore import QObject


class ViewModel(QObject):
    """
    The purpose of the ViewModel is to acquire and keep the information that is
    necessary for an View or UI. The UI should be able to observe changes in the
    ViewModel. ViewModels usually expose this information via reactive state. You
    can also use any observability construct from your favorite framework.

    ViewModel's only responsibility is to manage the data for the UI. It should
    never access your view hierarchy or hold a reference back to the View or the UI.
    """

    pass
