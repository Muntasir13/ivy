"""Collection of tests for sorting functions."""

# global
from hypothesis import strategies as st
import numpy as np

# local
import ivy_tests.test_ivy.helpers as helpers
from ivy_tests.test_ivy.helpers import handle_test


# argsort
@handle_test(
    fn_tree="functional.ivy.argsort",
    dtype_x_axis=helpers.dtype_values_axis(
        available_dtypes=helpers.get_dtypes("numeric"),
        min_num_dims=1,
        min_dim_size=1,
        min_axis=-1,
        max_axis=0,
    ),
    descending=st.booleans(),
    stable=st.booleans(),
)
def test_argsort(
    *,
    dtype_x_axis,
    descending,
    stable,
    as_variable,
    num_positional_args,
    native_array,
    container_flags,
    with_out,
    instance_method,
    backend_fw,
    fn_name,
    on_device,
    ground_truth_backend,
):
    dtype, x, axis = dtype_x_axis
    helpers.test_function(
        ground_truth_backend=ground_truth_backend,
        input_dtypes=dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        container_flags=container_flags,
        instance_method=instance_method,
        fw=backend_fw,
        fn_name=fn_name,
        on_device=on_device,
        x=x[0],
        axis=axis,
        descending=descending,
        stable=stable,
    )


# sort
@handle_test(
    fn_tree="functional.ivy.sort",
    dtype_x_axis=helpers.dtype_values_axis(
        available_dtypes=helpers.get_dtypes("numeric"),
        min_num_dims=1,
        min_dim_size=1,
        min_axis=-1,
        max_axis=0,
    ),
    descending=st.booleans(),
    stable=st.booleans(),
)
def test_sort(
    *,
    dtype_x_axis,
    descending,
    stable,
    as_variable,
    num_positional_args,
    native_array,
    container_flags,
    with_out,
    instance_method,
    backend_fw,
    fn_name,
    on_device,
    ground_truth_backend,
):
    dtype, x, axis = dtype_x_axis
    helpers.test_function(
        ground_truth_backend=ground_truth_backend,
        input_dtypes=dtype,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        container_flags=container_flags,
        instance_method=instance_method,
        fw=backend_fw,
        fn_name=fn_name,
        on_device=on_device,
        x=x[0],
        axis=axis,
        descending=descending,
        stable=stable,
    )


@st.composite
def _searchsorted_case1(draw):
    # 1-D for x, N-D for v
    dtype_x, x = draw(
        helpers.dtype_and_values(
            dtype=draw(helpers.get_dtypes("numeric", full=False, key="searchsorted")),
            shape=(draw(st.integers(min_value=1, max_value=5)),),
        )
    )
    dtype_v, v = draw(
        helpers.dtype_and_values(
            dtype=draw(helpers.get_dtypes("numeric", full=False, key="searchsorted")),
            min_num_dims=1,
        )
    )
    return dtype_x + dtype_v, x + v


@st.composite
def _searchsorted_case2(draw):
    # N-D for x, N-D for v
    arb_leading_dims = draw(
        helpers.get_shape(
            min_num_dims=1,
        )
    )
    nx = draw(st.integers(min_value=1, max_value=5))
    nv = draw(st.integers(min_value=1, max_value=5))
    dtype_x, x = draw(
        helpers.dtype_and_values(
            dtype=draw(helpers.get_dtypes("numeric", full=False, key="searchsorted")),
            shape=arb_leading_dims + (nx,),
        )
    )
    dtype_v, v = draw(
        helpers.dtype_and_values(
            dtype=draw(helpers.get_dtypes("numeric", full=False, key="searchsorted")),
            shape=arb_leading_dims + (nv,),
        )
    )
    return dtype_x + dtype_v, x + v


@handle_test(
    fn_tree="functional.ivy.searchsorted",
    data=st.data(),
    dtypes_and_xs=st.one_of(_searchsorted_case1(), _searchsorted_case2()),
    side=st.sampled_from(["left", "right"]),
    use_sorter=st.booleans(),
    ret_dtype=helpers.get_dtypes("integer", full=False),
)
def test_searchsorted(
    *,
    data,
    dtypes_and_xs,
    side,
    use_sorter,
    ret_dtype,
    as_variable,
    num_positional_args,
    native_array,
    container_flags,
    with_out,
    instance_method,
    backend_fw,
    fn_name,
    on_device,
    ground_truth_backend,
):
    dtypes, xs = dtypes_and_xs
    if use_sorter:
        sorter_dtype = data.draw(helpers.get_dtypes("signed_integer", full=False))
        dtypes += sorter_dtype
        sorter = np.argsort(xs[0]).astype(sorter_dtype[0])
    else:
        sorter = None
        xs[0] = np.sort(xs[0])
    helpers.test_function(
        ground_truth_backend=ground_truth_backend,
        input_dtypes=dtypes,
        as_variable_flags=as_variable,
        with_out=with_out,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        container_flags=container_flags,
        instance_method=instance_method,
        fw=backend_fw,
        fn_name=fn_name,
        on_device=on_device,
        x=xs[0],
        v=xs[1],
        side=side,
        sorter=sorter,
        ret_dtype=ret_dtype[0],
    )
