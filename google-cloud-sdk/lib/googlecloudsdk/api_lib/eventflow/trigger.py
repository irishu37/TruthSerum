# -*- coding: utf-8 -*- #
# Copyright 2019 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Wraps an Eventflow Trigger message, making fields more convenient."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.run import k8s_object


class Trigger(k8s_object.KubernetesObject):
  """Wraps an Eventflow Trigger message, making fields more convenient."""

  API_CATEGORY = 'eventing.knative.dev'
  KIND = 'Trigger'
  READY_CONDITION = 'Ready'
  TERMINAL_CONDITIONS = {
      READY_CONDITION,
  }

  @property
  def broker(self):
    return self._m.spec.broker

  @property
  def subscriber(self):
    return self._m.spec.subscriber.ref.name
