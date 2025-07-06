import sys
import os
import pytest
from pathlib import Path

# Добавляем корневую директорию проекта в sys.path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

# Это позволит импортировать main и app в тестах