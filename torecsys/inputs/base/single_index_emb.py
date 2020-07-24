import torch
import torch.nn as nn

from torecsys.utils.decorator import no_jit_experimental_by_namedtensor
from . import Inputs


class SingleIndexEmbedding(Inputs):
    r"""Base Inputs class for embedding a single index of a input field.
    """

    @no_jit_experimental_by_namedtensor
    def __init__(self,
                 embed_size: int,
                 field_size: int,
                 padding_idx: int = None,
                 nn_embedding: nn.Parameter = None,
                 **kwargs):
        r"""Initialize SingleIndexEmbedding
        
        Args:
            embed_size (int): Size of embedding tensor
            field_size (int): Size of inputs field
            padding_idx (int, optional): Padding index. 
                Defaults to None.
            nn_embedding (nn.Parameter, optional): Pretrained embedding values. 
                Defaults to None.
        
        Arguments:
            length (int): Size of embedding tensor.
            embedding (torch.nn.Module): Embedding layer.
            schema (namedtuple): List of string of field names to be embedded.
        """
        # refer to parent class
        super(SingleIndexEmbedding, self).__init__()

        # bind embedding to pre-trained embedding module if nn_embedding is not None
        if nn_embedding is not None:
            embed_size = nn_embedding.size("E")
            self.embedding = nn.Embedding.from_pretrained(nn_embedding)
        # else, create a embedding module with the given arguments
        else:
            embed_size = embed_size
            self.embedding = nn.Embedding(field_size, embed_size, padding_idx=padding_idx, **kwargs)

        # bind length to embed_size
        self.length = embed_size

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        r"""Forward calculation of SingleIndexEmbedding
        
        Args:
            inputs (T), shape = (B, 1), dtype = torch.long: Tensor of indices in inputs fields.
        
        Returns:
            T, (B, 1, E): Outputs of SingleIndexEmbedding.
        """
        # get embedding tensor from embedding module
        embedded_tensor = self.embedding(inputs.rename(None))
        embedded_tensor.names = ('B', 'N', 'E')
        return embedded_tensor
