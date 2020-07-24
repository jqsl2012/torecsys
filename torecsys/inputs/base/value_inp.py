import torch

from torecsys.utils.decorator import no_jit_experimental_by_namedtensor
from . import Inputs


class ValueInputs(Inputs):
    r"""Base Inputs class for value to be passed directly.
    
    :Todo:

    #. add transforms for value inputs to do pre-processing

    """

    @no_jit_experimental_by_namedtensor
    def __init__(self, num_fields: int):
        r"""Initialize ValueInputs
        
        Args:
            num_fields (int): Number of inputs' fields.

        Attributes:
            length (int): Number of inputs' fields.
        """
        # refer to parent class
        super(ValueInputs, self).__init__()

        # bind length to length of inp_fields 
        self.num_fields = num_fields
        self.length = 1

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        r"""Forward calculation of ValueInputs.
        
        Args:
            inputs (T), shape = (B, N): Tensor of values in input fields.
        
        Returns:
            T, shape = (B, 1, N): Outputs of ValueInputs
        """
        # reshape from dim 2 to dim 3
        if inputs.dim() == 2:
            inputs = inputs.unsqueeze(dim=-1)

        inputs.names = ("B", "N", "E")
        return inputs
