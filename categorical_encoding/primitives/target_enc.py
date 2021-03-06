from featuretools.primitives.base.transform_primitive_base import (
    TransformPrimitive
)
from featuretools.variable_types import Categorical, Numeric


class TargetEnc(TransformPrimitive):
    """Applies a fitted Target Encoder to the values.
    Requires an already fitted encoder.

    Parameters:
        fitted_encoder: encoder
            Encoder that has already learned encoding mappings from fitting to a data table.
        category: str or int
            String or integer corresponding to the name of the particular category.
            If integer, is the nth category encoded in the data table.

    Examples:
        >>> enc = Encoder(method='target')
        >>> enc.fit_transform(feature_matrix, features)
        >>> encoder = OrdinalEnc(fitted_encoder=enc, category='product_id')
        >>> encoded = encoder(['car', 'toothpaste', 'coke zero', 'coke zero'])
        [2, 3, 1, 1]
    """
    name = "target_enc"
    input_types = [Categorical]
    return_type = Numeric

    def __init__(self, fitted_encoder, category):
        self.mapping, self.mapping_ord = fitted_encoder.get_mapping(category)

    def get_function(self):
        def transform(X):
            return X.map(self.mapping_ord).map(self.mapping)
        return transform

    def generate_name(self, base_feature_names):
        return u"%s_%s" % (base_feature_names[0].upper(), 'target')
