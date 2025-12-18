"""Learning module for LUMO - tracks interactions & policy."""

from learning.logger import log_interaction, get_recent_logs, get_log_path
from learning.analyzer import (
    analyze_failures,
    analyze_success_rate,
    analyze_wake_word_detection,
    find_improvement_opportunities,
)
from learning.tuner import (
    load_tuning_config,
    auto_tune,
    get_current_thresholds,
)
from learning.feedback import (
    print_improvement_status,
    check_improvement_needed,
)

__all__ = [
    "log_interaction",
    "get_recent_logs",
    "get_log_path",
    "analyze_failures",
    "analyze_success_rate",
    "analyze_wake_word_detection",
    "find_improvement_opportunities",
    "load_tuning_config",
    "auto_tune",
    "get_current_thresholds",
    "print_improvement_status",
    "check_improvement_needed",
]
