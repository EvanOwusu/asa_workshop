from mymodule.sky_sim import get_radec#, segadecimal_to_float, float_to_segadecimal
import pytest
from mymodule.sky_sim import make_stars
def test_module_import():
    try:
        import mymodule.sky_sim
    except Exception as e:
        raise AssertionError("Failed to import mymodule")
    return

def test_get_radec_values():
    """
    This checks that get_radec gives back the correct values of Andromeda in decimal degrees
    """
   
    ra, dec = get_radec() 
    assert ra == pytest.approx(14.215420962967535, rel=10e-30)
    assert dec == pytest.approx(41.26916666666667)

def test_make_stars():
    """
    This checks that make_stars gives back the correct number of stars
    """
    ra, dec = get_radec()
    nsrc = 1000000 
    ras, decs = make_stars(ra, dec, nsrc=nsrc)
    assert len(ras) == nsrc
    assert len(decs) == nsrc



# @pytest.mark.parametrize("ra, dec", [(14.215420962967535,41.26916666666667)])
# def test_segadecimal_to_float(ra, dec):
#     new_ra, new_dec = segadecimal_to_float(*float_to_segadecimal(ra, dec)
#                                            )
#     assert new_ra == pytest.approx(ra)
#     assert new_dec == pytest.approx(dec)
    