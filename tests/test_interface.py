# This file is part of xtb.
#
# Copyright (C) 2020 Sebastian Ehlert
#
# xtb is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# xtb is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with xtb.  If not, see <https://www.gnu.org/licenses/>.

from xtb.interface import (
    XTBException,
    Molecule,
    Calculator,
    Results,
    Param,
    VERBOSITY_MINIMAL,
)
from pytest import approx, raises
import numpy as np


def test_molecule():
    """check if the molecular structure data is working as expected."""

    numbers = np.array(
        [6, 7, 6, 7, 6, 6, 6, 8, 7, 6, 8, 7, 6, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    )
    positions = np.array(
        [
            [ 2.02799738646442, 0.09231312124713,-0.14310895950963],
            [ 4.75011007621000, 0.02373496014051,-0.14324124033844],
            [ 6.33434307654413, 2.07098865582721,-0.14235306905930],
            [ 8.72860718071825, 1.38002919517619,-0.14265542523943],
            [ 8.65318821103610,-1.19324866489847,-0.14231527453678],
            [ 6.23857175648671,-2.08353643730276,-0.14218299370797],
            [ 5.63266886875962,-4.69950321056008,-0.13940509630299],
            [ 3.44931709749015,-5.48092386085491,-0.14318454855466],
            [ 7.77508917214346,-6.24427872938674,-0.13107140408805],
            [10.30229550927022,-5.39739796609292,-0.13672168520430],
            [12.07410272485492,-6.91573621641911,-0.13666499342053],
            [10.70038521493902,-2.79078533715849,-0.14148379504141],
            [13.24597858727017,-1.76969072232377,-0.14218299370797],
            [ 7.40891694074004,-8.95905928176407,-0.11636933482904],
            [ 1.38702118184179, 2.05575746325296,-0.14178615122154],
            [ 1.34622199478497,-0.86356704498496, 1.55590600570783],
            [ 1.34624089204623,-0.86133716815647,-1.84340893849267],
            [ 5.65596919189118, 4.00172183859480,-0.14131371969009],
            [14.67430918222276,-3.26230980007732,-0.14344911021228],
            [13.50897177220290,-0.60815166181684, 1.54898960808727],
            [13.50780014200488,-0.60614855212345,-1.83214617078268],
            [ 5.41408424778406,-9.49239668625902,-0.11022772492007],
            [ 8.31919801555568,-9.74947502841788, 1.56539243085954],
            [ 8.31511620712388,-9.76854236502758,-1.79108242206824],
        ]
    )
    filename = "xtb-error.log"
    message = "Expecting nuclear fusion warning"

    # Constructor should raise an error for nuclear fusion input
    with raises(XTBException, match="Could not initialize"):
        mol = Molecule(numbers, np.zeros((24, 3)))

    # The Python class should protect from garbage input like this
    with raises(ValueError, match="Dimension missmatch"):
        mol = Molecule(np.array([1, 1, 1]), positions)

    # Also check for sane coordinate input
    with raises(ValueError, match="Expected tripels"):
        mol = Molecule(numbers, np.random.rand(7))

    # Construct real molecule
    mol = Molecule(numbers, positions)

    # Try to update a structure with missmatched coordinates
    with raises(ValueError, match="Dimension missmatch for positions"):
        mol.update(np.random.rand(7))

    # Try to add a missmatched lattice
    with raises(ValueError, match="Invalid lattice provided"):
        mol.update(positions, np.random.rand(7))

    # Try to update a structure with nuclear fusion coordinates
    with raises(XTBException, match="Could not update"):
        mol.update(np.zeros((24, 3)))

    # Redirect API output to file
    mol.set_output(filename)

    # Flush the error from the environment log
    mol.show(message)

    # Reset to correct positions, Molecule object should still be intact
    mol.update(positions, np.zeros((3, 3)))


def test_gfn2_xtb_0d():
    """check if the GFN2-xTB interface is working correctly."""
    thr = 1.0e-8
    thr2 = 1.0e-6

    numbers = np.array(
        [6, 7, 6, 7, 6, 6, 6, 8, 7, 6, 8, 7, 6, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    )
    positions = np.array(
        [
            [ 2.02799738646442, 0.09231312124713,-0.14310895950963],
            [ 4.75011007621000, 0.02373496014051,-0.14324124033844],
            [ 6.33434307654413, 2.07098865582721,-0.14235306905930],
            [ 8.72860718071825, 1.38002919517619,-0.14265542523943],
            [ 8.65318821103610,-1.19324866489847,-0.14231527453678],
            [ 6.23857175648671,-2.08353643730276,-0.14218299370797],
            [ 5.63266886875962,-4.69950321056008,-0.13940509630299],
            [ 3.44931709749015,-5.48092386085491,-0.14318454855466],
            [ 7.77508917214346,-6.24427872938674,-0.13107140408805],
            [10.30229550927022,-5.39739796609292,-0.13672168520430],
            [12.07410272485492,-6.91573621641911,-0.13666499342053],
            [10.70038521493902,-2.79078533715849,-0.14148379504141],
            [13.24597858727017,-1.76969072232377,-0.14218299370797],
            [ 7.40891694074004,-8.95905928176407,-0.11636933482904],
            [ 1.38702118184179, 2.05575746325296,-0.14178615122154],
            [ 1.34622199478497,-0.86356704498496, 1.55590600570783],
            [ 1.34624089204623,-0.86133716815647,-1.84340893849267],
            [ 5.65596919189118, 4.00172183859480,-0.14131371969009],
            [14.67430918222276,-3.26230980007732,-0.14344911021228],
            [13.50897177220290,-0.60815166181684, 1.54898960808727],
            [13.50780014200488,-0.60614855212345,-1.83214617078268],
            [ 5.41408424778406,-9.49239668625902,-0.11022772492007],
            [ 8.31919801555568,-9.74947502841788, 1.56539243085954],
            [ 8.31511620712388,-9.76854236502758,-1.79108242206824],
        ]
    )
    gradient = np.array(
        [
            [-4.48702270e-03,-7.11501681e-04, 4.42250727e-06],
            [ 5.63520998e-03,-2.63277841e-02,-5.47551032e-05],
            [ 4.94394513e-03, 1.91697172e-02, 5.20296937e-05],
            [ 4.14320227e-03, 3.78985927e-03,-3.26124506e-05],
            [-3.44924840e-02,-8.30763633e-03,-3.85476373e-05],
            [ 6.09858493e-03,-4.02776651e-03, 3.46142461e-05],
            [ 1.74698961e-02, 7.91501928e-03, 3.75246600e-05],
            [-1.44268345e-02, 7.07857171e-03,-1.12175048e-04],
            [-5.07088926e-04,-1.13149559e-02, 7.28999985e-05],
            [-1.55778036e-02, 1.26994854e-02,-2.82633017e-05],
            [ 2.84123935e-02,-2.38401320e-02,-3.96858051e-05],
            [ 2.52730535e-03, 1.36557434e-02,-1.07970323e-05],
            [-1.61957397e-03,-2.96924390e-03, 2.89329075e-06],
            [-6.51526117e-03, 7.90714240e-03,-5.83689564e-05],
            [-1.45365262e-03, 2.78387473e-03, 4.39889933e-06],
            [ 2.59676642e-03, 9.07269292e-04, 3.98184821e-03],
            [ 2.59860253e-03, 9.08300767e-04,-3.98462262e-03],
            [-3.77425616e-03, 8.36833530e-03, 2.89789639e-05],
            [ 7.86820850e-03, 2.13957196e-03, 7.31459251e-07],
            [ 9.32145702e-04,-1.65668033e-04, 3.24917573e-03],
            [ 9.57211265e-04,-1.41846051e-04,-3.25368821e-03],
            [-2.06937754e-03,-9.28913451e-03, 1.03587348e-04],
            [ 3.58598494e-04,-9.82977790e-05, 2.38378001e-03],
            [ 3.81284918e-04,-1.28923994e-04,-2.34336886e-03],
        ]
    )
    charges = np.array([
        -0.05445590, -0.00457526,  0.08391889, -0.27870751,  0.11914924,
        -0.02621044,  0.26115960, -0.44071824, -0.10804747,  0.30411699,
        -0.44083760, -0.07457706, -0.04790859, -0.03738239,  0.06457802,
         0.08293905,  0.08296802,  0.05698136,  0.09025556,  0.07152988,
         0.07159003,  0.08590674,  0.06906357,  0.06926350,
    ])

    calc = Calculator(Param.GFN2xTB, numbers, positions)
    calc.set_verbosity(VERBOSITY_MINIMAL)
    assert calc.check() == 0

    res = calc.singlepoint()

    assert approx(res.get_energy(), thr) == -42.14746312757416
    assert approx(res.get_gradient(), thr) == gradient
    assert approx(res.get_charges(), thr2) == charges


def test_gfn1_xtb_0d():
    """check if the GFN1-xTB interface is working correctly."""
    thr = 1.0e-8
    thr2 = 1.0e-6

    numbers = np.array(
        [6, 7, 6, 7, 6, 6, 6, 8, 7, 6, 8, 7, 6, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    )
    positions = np.array(
        [
            [ 2.02799738646442, 0.09231312124713,-0.14310895950963],
            [ 4.75011007621000, 0.02373496014051,-0.14324124033844],
            [ 6.33434307654413, 2.07098865582721,-0.14235306905930],
            [ 8.72860718071825, 1.38002919517619,-0.14265542523943],
            [ 8.65318821103610,-1.19324866489847,-0.14231527453678],
            [ 6.23857175648671,-2.08353643730276,-0.14218299370797],
            [ 5.63266886875962,-4.69950321056008,-0.13940509630299],
            [ 3.44931709749015,-5.48092386085491,-0.14318454855466],
            [ 7.77508917214346,-6.24427872938674,-0.13107140408805],
            [10.30229550927022,-5.39739796609292,-0.13672168520430],
            [12.07410272485492,-6.91573621641911,-0.13666499342053],
            [10.70038521493902,-2.79078533715849,-0.14148379504141],
            [13.24597858727017,-1.76969072232377,-0.14218299370797],
            [ 7.40891694074004,-8.95905928176407,-0.11636933482904],
            [ 1.38702118184179, 2.05575746325296,-0.14178615122154],
            [ 1.34622199478497,-0.86356704498496, 1.55590600570783],
            [ 1.34624089204623,-0.86133716815647,-1.84340893849267],
            [ 5.65596919189118, 4.00172183859480,-0.14131371969009],
            [14.67430918222276,-3.26230980007732,-0.14344911021228],
            [13.50897177220290,-0.60815166181684, 1.54898960808727],
            [13.50780014200488,-0.60614855212345,-1.83214617078268],
            [ 5.41408424778406,-9.49239668625902,-0.11022772492007],
            [ 8.31919801555568,-9.74947502841788, 1.56539243085954],
            [ 8.31511620712388,-9.76854236502758,-1.79108242206824],
        ]
    )
    gradient = np.array(
        [
            [ 3.87497169e-03, 1.05883022e-03, 4.01012413e-06],
            [-6.82002304e-03,-2.54686427e-02,-4.74713878e-05],
            [ 1.06489319e-02, 8.83656933e-03, 4.79964506e-05],
            [ 3.19138203e-04, 7.42440606e-03,-2.84972366e-05],
            [-2.62085234e-02,-9.01316371e-03,-3.86695635e-05],
            [-1.75094079e-03, 3.66993588e-03, 3.41186057e-05],
            [ 1.94850127e-02, 4.74199522e-03, 4.04729092e-05],
            [-1.17234487e-02, 7.48238018e-03,-1.16123385e-04],
            [-1.22410371e-03,-1.91329992e-02, 1.24615909e-04],
            [-1.67669061e-02, 1.21039811e-02,-3.45753133e-05],
            [ 2.48445184e-02,-1.92875717e-02,-4.91970983e-05],
            [ 1.10842561e-02, 1.70041879e-02,-3.22098294e-06],
            [-6.45913430e-03,-4.28606740e-03,-4.08606798e-06],
            [-6.58997261e-03, 1.32209050e-02,-9.01648028e-05],
            [-1.32693744e-03, 2.12474694e-03, 4.09305030e-06],
            [ 1.72269615e-03, 1.17167501e-03, 2.68453033e-03],
            [ 1.72536326e-03, 1.17100604e-03,-2.68802212e-03],
            [-1.55002130e-03, 3.93152833e-03, 2.52250090e-05],
            [ 6.35716726e-03, 2.28982657e-03, 3.48062215e-06],
            [ 5.17423565e-04,-5.06087446e-04, 1.94245792e-03],
            [ 5.40636707e-04,-4.85737643e-04,-1.94565875e-03],
            [-1.26772106e-03,-7.65879097e-03, 8.49174054e-05],
            [ 2.77976049e-04,-1.82969944e-04, 1.40041971e-03],
            [ 2.89640303e-04,-2.09943109e-04,-1.35065134e-03],
        ]
    )
    dipole = np.array([-0.81941935,  1.60912848,  0.00564382])


    calc = Calculator(Param.GFN1xTB, numbers, positions)

    res = Results(calc)

    # check if we cannot retrieve properties from the unallocated result
    with raises(XTBException, match="Virial is not available"):
        res.get_virial()
    res.show("Release error log")
    with raises(XTBException, match="Bond orders are not available"):
        res.get_bond_orders()
    res.show("Release error log")

    # Start calculation by restarting with result
    res = calc.singlepoint(res)

    assert approx(res.get_energy(), thr) == -44.509702418208896
    assert approx(res.get_gradient(), thr) == gradient
    assert approx(res.get_dipole(), thr2) == dipole


def test_gfn2_xtb_3d():
    """Test if GFN2-xTB correctly fails for periodic input"""

    numbers = np.array(
        [6, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 7, 7, 7, 7]
    )
    positions = np.array([
        [ 9.77104501e-01,  1.24925555e-01,  8.22139769e+00],
        [ 8.37995371e-01,  8.23489051e+00,  3.74893761e+00],
        [ 4.62693404e+00, -2.45721089e+00,  8.22052352e+00],
        [ 4.62532610e+00,  1.41051267e+00,  5.97940016e+00],
        [ 9.71618351e-01,  1.17570237e-01,  3.75065164e+00],
        [-2.80917006e+00,  6.94865315e+00,  5.99166085e+00],
        [ 4.06610161e+00,  4.51252077e+00,  6.46827038e-01],
        [ 2.76223056e-01, -8.50055887e-01,  2.06420987e+00],
        [ 2.84806942e-01,  2.07039689e+00,  8.22836360e+00],
        [ 2.90284064e+00,  8.22939158e+00,  3.73820878e+00],
        [ 6.69188274e+00, -2.46191735e+00,  8.22593771e+00],
        [ 6.69035555e+00,  1.41863696e+00,  5.97712614e+00],
        [ 7.73011343e+00,  1.91963880e+00,  6.45533278e-01],
        [ 3.94842571e+00,  3.36121142e+00,  5.97668593e+00],
        [-3.49960564e+00,  5.97197638e+00,  7.67502785e+00],
        [ 2.79250975e-01,  2.06298102e+00,  3.73907675e+00],
        [-3.50586965e+00,  5.96534053e+00,  4.31491171e+00],
        [ 1.56432603e-01,  7.25773353e+00,  2.06229892e+00],
        [-4.98732693e-02,  6.88619344e+00,  5.98746725e+00],
        [-4.50657119e-03, -1.16906911e+00,  5.98934273e+00],
        [ 3.73678498e+00,  1.55157272e-01,  8.27155126e+00],
        [ 3.73119434e+00,  1.47879860e-01,  3.69345547e+00],
        ])
    lattice = np.array([
        [ 1.13437228e+01, -1.84405404e-03,  1.33836685e-05],
        [-3.78300868e+00,  1.06992286e+01, -1.04202175e-03],
        [-3.78025723e+00, -5.34955718e+00,  9.26593601e+00],
        ])
    periodic = np.array([True, True, True])

    # GFN2-xTB does not support periodic boundary conditions,
    # yet the constructor should not flag this error to keep the interface uniform
    calc = Calculator(
        Param.GFN2xTB, numbers, positions, lattice=lattice, periodic=periodic
    )

    res = Results(calc)

    with raises(XTBException, match="Single point calculation failed"):
        calc.singlepoint(res)


def test_gfn1_xtb_3d():
    """Test GFN1-xTB for periodic input"""
    thr = 1.0e-8
    thr2 = 1.0e-6

    numbers = np.array(
        [6, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 7, 7, 7, 7]
    )
    positions = np.array([
        [ 9.77104501e-01,  1.24925555e-01,  8.22139769e+00],
        [ 8.37995371e-01,  8.23489051e+00,  3.74893761e+00],
        [ 4.62693404e+00, -2.45721089e+00,  8.22052352e+00],
        [ 4.62532610e+00,  1.41051267e+00,  5.97940016e+00],
        [ 9.71618351e-01,  1.17570237e-01,  3.75065164e+00],
        [-2.80917006e+00,  6.94865315e+00,  5.99166085e+00],
        [ 4.06610161e+00,  4.51252077e+00,  6.46827038e-01],
        [ 2.76223056e-01, -8.50055887e-01,  2.06420987e+00],
        [ 2.84806942e-01,  2.07039689e+00,  8.22836360e+00],
        [ 2.90284064e+00,  8.22939158e+00,  3.73820878e+00],
        [ 6.69188274e+00, -2.46191735e+00,  8.22593771e+00],
        [ 6.69035555e+00,  1.41863696e+00,  5.97712614e+00],
        [ 7.73011343e+00,  1.91963880e+00,  6.45533278e-01],
        [ 3.94842571e+00,  3.36121142e+00,  5.97668593e+00],
        [-3.49960564e+00,  5.97197638e+00,  7.67502785e+00],
        [ 2.79250975e-01,  2.06298102e+00,  3.73907675e+00],
        [-3.50586965e+00,  5.96534053e+00,  4.31491171e+00],
        [ 1.56432603e-01,  7.25773353e+00,  2.06229892e+00],
        [-4.98732693e-02,  6.88619344e+00,  5.98746725e+00],
        [-4.50657119e-03, -1.16906911e+00,  5.98934273e+00],
        [ 3.73678498e+00,  1.55157272e-01,  8.27155126e+00],
        [ 3.73119434e+00,  1.47879860e-01,  3.69345547e+00],
        ])
    lattice = np.array([
        [ 1.13437228e+01, -1.84405404e-03,  1.33836685e-05],
        [-3.78300868e+00,  1.06992286e+01, -1.04202175e-03],
        [-3.78025723e+00, -5.34955718e+00,  9.26593601e+00],
    ])
    periodic = np.array([True, True, True])
    gradient = np.array([
        [ 5.46952312e-03, -3.12525543e-03, -6.52896786e-03],
        [-5.71285287e-03,  4.38725269e-03,  6.32349907e-03],
        [-5.02173630e-03,  4.34885633e-03, -7.00803496e-03],
        [-4.87551596e-03, -7.09454257e-03,  3.77244368e-04],
        [ 5.02630829e-03, -3.79620239e-03,  6.30421751e-03],
        [ 4.91374216e-03,  8.09631816e-03, -3.68676539e-04],
        [-7.28717739e-05,  1.30568980e-03, -6.38908884e-04],
        [ 9.79695284e-05,  1.46129903e-03,  1.04762274e-03],
        [ 7.73360338e-05, -1.75682759e-03,  7.51987006e-04],
        [-1.23628606e-03, -4.69633640e-04, -7.39566395e-04],
        [-1.91940111e-03, -4.73100704e-04,  6.08278469e-04],
        [-1.77181502e-03,  7.83050332e-04, -4.59767804e-06],
        [ 1.17661172e-03,  2.89377463e-04, -9.14361241e-04],
        [ 1.34273926e-03, -1.27328012e-03, -1.21190000e-04],
        [ 7.78894324e-05, -2.90779544e-05, -1.64479354e-03],
        [ 2.01000804e-04, -1.68099958e-03, -7.42723431e-04],
        [-6.00020414e-05,  2.71877066e-05,  1.56139664e-03],
        [ 1.25834445e-03,  4.52585494e-04,  7.01094853e-04],
        [-1.59037639e-03,  6.66092068e-03,  1.53044955e-03],
        [ 6.42180919e-03, -6.01295157e-04, -1.95941235e-04],
        [-1.85390467e-03, -4.18967639e-03, -5.23581022e-03],
        [-1.94851179e-03, -3.32264614e-03,  4.93778178e-03],
    ])
    charges = np.array([
        0.06182382,  0.06099432,  0.03885390,  0.06788916,  0.06428087,
        0.05876764,  0.03243010,  0.02574899,  0.02339485,  0.03323515,
        0.02257734,  0.02147826,  0.03444456,  0.02614362,  0.03103734,
        0.02593346,  0.03068062,  0.03220337, -0.16214463, -0.17714762,
       -0.17554024, -0.17708487,
    ])


    calc = Calculator(
        Param.GFN1xTB, numbers, positions, lattice=lattice, periodic=periodic
    )

    res = Results(calc)

    # Start calculation by restarting with result
    calc.singlepoint(res)

    assert approx(res.get_energy(), thr) == -31.906084801853034
    assert approx(res.get_gradient(), thr) == gradient
    assert approx(res.get_charges(), thr2) == charges
