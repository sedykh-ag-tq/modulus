# Copyright (c) 2023, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import torch

from modulus.metrics.diffusion import (
    EDMLoss,
    VELoss,
    VPLoss,
)

# VPLoss tests


def test_vploss_initialization():
    loss_func = VPLoss()
    assert loss_func.beta_d == 19.9
    assert loss_func.beta_min == 0.1
    assert loss_func.epsilon_t == 1e-5

    loss_func = VPLoss(beta_d=10.0, beta_min=0.5, epsilon_t=1e-4)
    assert loss_func.beta_d == 10.0
    assert loss_func.beta_min == 0.5
    assert loss_func.epsilon_t == 1e-4


def test_sigma_method():
    loss_func = VPLoss()

    # Scalar input
    sigma_val = loss_func.sigma(1.0)
    assert isinstance(sigma_val, torch.Tensor)
    assert sigma_val.item() > 0

    # Tensor input
    t = torch.tensor([1.0, 2.0])
    sigma_vals = loss_func.sigma(t)
    assert sigma_vals.shape == t.shape


def fake_net(y, sigma, labels, augment_labels=None):
    return torch.tensor([1.0])


def test_call_method_vp():
    loss_func = VPLoss()

    images = torch.tensor([[[[1.0]]]])
    labels = None

    # Without augmentation
    loss_value = loss_func(fake_net, images, labels)
    assert isinstance(loss_value, torch.Tensor)

    # With augmentation
    def mock_augment_pipe(imgs):
        return imgs, None

    loss_value_with_augmentation = loss_func(
        fake_net, images, labels, mock_augment_pipe
    )
    assert isinstance(loss_value_with_augmentation, torch.Tensor)


# VELoss tests


def test_veloss_initialization():
    loss_func = VELoss()
    assert loss_func.sigma_min == 0.02
    assert loss_func.sigma_max == 100.0

    loss_func = VELoss(sigma_min=0.01, sigma_max=50.0)
    assert loss_func.sigma_min == 0.01
    assert loss_func.sigma_max == 50.0


def test_call_method_ve():
    loss_func = VELoss()

    images = torch.tensor([[[[1.0]]]])
    labels = None

    # Without augmentation
    loss_value = loss_func(fake_net, images, labels)
    assert isinstance(loss_value, torch.Tensor)

    # With augmentation
    def mock_augment_pipe(imgs):
        return imgs, None

    loss_value_with_augmentation = loss_func(
        fake_net, images, labels, mock_augment_pipe
    )
    assert isinstance(loss_value_with_augmentation, torch.Tensor)


# EDMLoss tests


def test_edmloss_initialization():
    loss_func = EDMLoss()
    assert loss_func.P_mean == -1.2
    assert loss_func.P_std == 1.2
    assert loss_func.sigma_data == 0.5

    loss_func = EDMLoss(P_mean=-2.0, P_std=2.0, sigma_data=0.3)
    assert loss_func.P_mean == -2.0
    assert loss_func.P_std == 2.0
    assert loss_func.sigma_data == 0.3


def test_call_method_edm():
    loss_func = EDMLoss()

    img = torch.tensor([[[[1.0]]]])
    labels = None

    # Without augmentation
    loss_value = loss_func(fake_net, img, labels)
    assert isinstance(loss_value, torch.Tensor)

    # With augmentation
    def mock_augment_pipe(imgs):
        return imgs, None

    loss_value_with_augmentation = loss_func(fake_net, img, labels, mock_augment_pipe)
    assert isinstance(loss_value_with_augmentation, torch.Tensor)


# RegressionLoss tests


# def test_regressionloss_initialization():
#     loss_func = RegressionLoss()
#     assert loss_func.P_mean == -1.2
#     assert loss_func.P_std == 1.2
#     assert loss_func.sigma_data == 0.5

#     loss_func = RegressionLoss(P_mean=-2.0, P_std=2.0, sigma_data=0.3)
#     assert loss_func.P_mean == -2.0
#     assert loss_func.P_std == 2.0
#     assert loss_func.sigma_data == 0.3


# def fake_net(input, y_lr, sigma, labels, augment_labels=None):
#     return torch.tensor([1.0])


# def test_call_method():
#     loss_func = RegressionLoss()

#     img_clean = torch.tensor([[[[1.0]]]])
#     img_lr = torch.tensor([[[[0.5]]]])
#     labels = None

#     # Without augmentation
#     loss_value = loss_func(fake_net, img_clean, img_lr, labels)
#     assert isinstance(loss_value, torch.Tensor)

#     # With augmentation
#     def mock_augment_pipe(imgs):
#         return imgs, None

#     loss_value_with_augmentation = loss_func(
#         fake_net, img_clean, img_lr, labels, mock_augment_pipe
#     )
#     assert isinstance(loss_value_with_augmentation, torch.Tensor)


# MixtureLoss tests


# def test_mixtureloss_initialization():
#     loss_func = MixtureLoss()
#     assert loss_func.P_mean == -1.2
#     assert loss_func.P_std == 1.2
#     assert loss_func.sigma_data == 0.5

#     loss_func = MixtureLoss(P_mean=-2.0, P_std=2.0, sigma_data=0.3)
#     assert loss_func.P_mean == -2.0
#     assert loss_func.P_std == 2.0
#     assert loss_func.sigma_data == 0.3


# def fake_net(latent, y_lr, sigma, labels, augment_labels=None):
#     return torch.tensor([1.0])


# def test_call_method():
#     loss_func = MixtureLoss()

#     img_clean = torch.tensor([[[[1.0]]]])
#     img_lr = torch.tensor([[[[0.5]]]])
#     labels = None

#     # Without augmentation
#     loss_value = loss_func(fake_net, img_clean, img_lr, labels)
#     assert isinstance(loss_value, torch.Tensor)

#     # With augmentation
#     def mock_augment_pipe(imgs):
#         return imgs, None

#     loss_value_with_augmentation = loss_func(
#         fake_net, img_clean, img_lr, labels, mock_augment_pipe
#     )
#     assert isinstance(loss_value_with_augmentation, torch.Tensor)


# ResLoss tests


# def test_resloss_initialization():
#     # Mock the model loading
#     ResLoss.unet = torch.nn.Linear(1, 1).cuda()

#     loss_func = ResLoss()
#     assert loss_func.P_mean == 0.0
#     assert loss_func.P_std == 1.2
#     assert loss_func.sigma_data == 0.5

#     loss_func = ResLoss(P_mean=-2.0, P_std=2.0, sigma_data=0.3)
#     assert loss_func.P_mean == -2.0
#     assert loss_func.P_std == 2.0
#     assert loss_func.sigma_data == 0.3


# def fake_net(latent, y_lr, sigma, labels, augment_labels=None):
#     return torch.tensor([1.0])


# def test_call_method():
#     # Mock the model loading
#     ResLoss.unet = torch.nn.Linear(1, 1).cuda()

#     loss_func = ResLoss()

#     img_clean = torch.tensor([[[[1.0]]]])
#     img_lr = torch.tensor([[[[0.5]]]])
#     labels = None

#     # Without augmentation
#     loss_value = loss_func(fake_net, img_clean, img_lr, labels)
#     assert isinstance(loss_value, torch.Tensor)

#     # With augmentation
#     def mock_augment_pipe(imgs):
#         return imgs, None

#     loss_value_with_augmentation = loss_func(
#         fake_net, img_clean, img_lr, labels, mock_augment_pipe
#     )
#     assert isinstance(loss_value_with_augmentation, torch.Tensor)
