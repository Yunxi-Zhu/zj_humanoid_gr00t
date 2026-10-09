# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from gr00t.configs.data.embodiment_configs import register_modality_config
from gr00t.data.embodiment_tags import EmbodimentTag
from gr00t.data.types import (
    ActionConfig,
    ActionFormat,
    ActionRepresentation,
    ActionType,
    ModalityConfig,
)


black_cloth_config = {
    # Video: current frame only; keys must match "video" entries in meta/modality.json
    "video": ModalityConfig(
        delta_indices=[0],
        modality_keys=["chest", "left"],
    ),
    # State: current proprioceptive reading; keys must match "state" entries in meta/modality.json
    "state": ModalityConfig(
        delta_indices=[0],
        modality_keys=[
            "left_tcp",
            "left_pinch_raw",
            "left_finger_pressure",
            "left_wrist_force",
            "right_tcp",
            "right_pinch_raw",
            "right_finger_pressure",
            "right_wrist_force",
        ],
    ),
    # Action: 16-step prediction horizon; one ActionConfig per modality key.
    # left/right_delta_tcp are already stored as deltas (xyz + rotvec, 6D), so keep
    # ABSOLUTE to avoid a second relative conversion in the processor. State TCP is
    # 7D (xyz + quat) and does not match the 6D action, so EEF relative conversion
    # cannot be used without converting the dataset.
    "action": ModalityConfig(
        delta_indices=list(range(0, 16)),
        modality_keys=[
            "left_delta_tcp",
            "left_pinch_raw",
            "right_delta_tcp",
            "right_pinch_raw",
        ],
        action_configs=[
            ActionConfig(
                rep=ActionRepresentation.ABSOLUTE,
                type=ActionType.NON_EEF,
                format=ActionFormat.DEFAULT,
            ),
            ActionConfig(
                rep=ActionRepresentation.ABSOLUTE,
                type=ActionType.NON_EEF,
                format=ActionFormat.DEFAULT,
            ),
            ActionConfig(
                rep=ActionRepresentation.ABSOLUTE,
                type=ActionType.NON_EEF,
                format=ActionFormat.DEFAULT,
            ),
            ActionConfig(
                rep=ActionRepresentation.ABSOLUTE,
                type=ActionType.NON_EEF,
                format=ActionFormat.DEFAULT,
            ),
        ],
    ),
    # Language: episodes.jsonl "tasks" is currently empty; fill it in for language following.
    "language": ModalityConfig(
        delta_indices=[0],
        modality_keys=["task"],
    ),
}

register_modality_config(black_cloth_config, embodiment_tag=EmbodimentTag.NEW_EMBODIMENT)
