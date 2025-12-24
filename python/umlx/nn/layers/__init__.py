# Copyright © 2023 Apple Inc.

from umlx.nn.layers.activations import (
    CELU,
    ELU,
    GELU,
    GLU,
    SELU,
    HardShrink,
    Hardswish,
    HardTanh,
    LeakyReLU,
    LogSigmoid,
    LogSoftmax,
    Mish,
    PReLU,
    ReLU,
    ReLU2,
    ReLU6,
    Sigmoid,
    SiLU,
    Softmax,
    Softmin,
    Softplus,
    Softshrink,
    Softsign,
    Step,
    Tanh,
    celu,
    elu,
    gelu,
    gelu_approx,
    gelu_fast_approx,
    glu,
    hard_shrink,
    hard_tanh,
    hardswish,
    leaky_relu,
    log_sigmoid,
    log_softmax,
    mish,
    prelu,
    relu,
    relu2,
    relu6,
    selu,
    sigmoid,
    silu,
    softmax,
    softmin,
    softplus,
    softshrink,
    softsign,
    step,
    tanh,
)
from umlx.nn.layers.base import Module
from umlx.nn.layers.containers import Sequential
from umlx.nn.layers.convolution import Conv1d, Conv2d, Conv3d
from umlx.nn.layers.convolution_transpose import (
    ConvTranspose1d,
    ConvTranspose2d,
    ConvTranspose3d,
)
from umlx.nn.layers.distributed import (
    AllToShardedLinear,
    QuantizedAllToShardedLinear,
    QuantizedShardedToAllLinear,
    ShardedToAllLinear,
)
from umlx.nn.layers.dropout import Dropout, Dropout2d, Dropout3d
from umlx.nn.layers.embedding import Embedding
from umlx.nn.layers.linear import Bilinear, Identity, Linear
from umlx.nn.layers.normalization import (
    BatchNorm,
    GroupNorm,
    InstanceNorm,
    LayerNorm,
    RMSNorm,
)
from umlx.nn.layers.pooling import (
    AvgPool1d,
    AvgPool2d,
    AvgPool3d,
    MaxPool1d,
    MaxPool2d,
    MaxPool3d,
)
from umlx.nn.layers.positional_encoding import ALiBi, RoPE, SinusoidalPositionalEncoding
from umlx.nn.layers.quantized import QuantizedEmbedding, QuantizedLinear, quantize
from umlx.nn.layers.recurrent import GRU, LSTM, RNN
from umlx.nn.layers.transformer import (
    MultiHeadAttention,
    Transformer,
    TransformerDecoder,
    TransformerDecoderLayer,
    TransformerEncoder,
    TransformerEncoderLayer,
)
from umlx.nn.layers.upsample import Upsample
