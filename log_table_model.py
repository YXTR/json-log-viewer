from typing import Any, Optional
from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from pandas import DataFrame


class LogTableModel(QAbstractTableModel):
    def __init__(self, data: DataFrame):
        super().__init__()
        self._data = data

    def column_names(self):
        return self._data.columns.tolist()

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid():
            return None
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            if isinstance(value, float):
                return f"{value:.2f}"
            return str(value)
        return None

    def rowCount(self, index: QModelIndex = QModelIndex()) -> int:
        return self._data.shape[0]

    def columnCount(self, index: QModelIndex = QModelIndex()) -> int:
        return self._data.shape[1]

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole) -> Optional[str]:
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return str(self._data.columns[section])
        return None
