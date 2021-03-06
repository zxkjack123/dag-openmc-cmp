#! /usr/bin/env python
import os
import sys

import numpy as np
import openmc
import matplotlib.pyplot as plt
from math import*

from argparse import ArgumentParser


e_bins =np.array(
        [1.00001E-007, 4.13994E-007, 5.31579E-007, 6.82560E-007, 8.76425E-007,
         1.12535E-006, 1.44498E-006, 1.85539E-006, 2.38237E-006, 3.05902E-006,
         3.92786E-006, 5.04348E-006, 6.47595E-006, 8.31529E-006, 1.06770E-005,
         1.37096E-005, 1.76035E-005, 2.26033E-005, 2.90232E-005, 3.72665E-005,
         4.78512E-005, 6.14421E-005, 7.88932E-005, 1.01301E-004, 1.30073E-004,
         1.67017E-004, 2.14454E-004, 2.75364E-004, 3.53575E-004, 4.53999E-004,
         5.82947E-004, 7.48518E-004, 9.61117E-004, 1.23410E-003, 1.58461E-003,
         2.03468E-003, 2.24867E-003, 2.48517E-003, 2.61259E-003, 2.74654E-003,
         3.03539E-003, 3.35463E-003, 3.70744E-003, 4.30742E-003, 5.53084E-003,
         7.10174E-003, 9.11882E-003, 1.05946E-002, 1.17088E-002, 1.50344E-002,
         1.93045E-002, 2.18749E-002, 2.35786E-002, 2.41755E-002, 2.47875E-002,
         2.60584E-002, 2.70001E-002, 2.85011E-002, 3.18278E-002, 3.43067E-002,
         4.08677E-002, 4.63092E-002, 5.24752E-002, 5.65622E-002, 6.73795E-002,
         7.20245E-002, 7.94987E-002, 8.25034E-002, 8.65170E-002, 9.80365E-002,
         1.11090E-001, 1.16786E-001, 1.22773E-001, 1.29068E-001, 1.35686E-001,
         1.42642E-001, 1.49956E-001, 1.57644E-001, 1.65727E-001, 1.74224E-001,
         1.83156E-001, 1.92547E-001, 2.02419E-001, 2.12797E-001, 2.23708E-001,
         2.35177E-001, 2.47235E-001, 2.73237E-001, 2.87246E-001, 2.94518E-001,
         2.97211E-001, 2.98491E-001, 3.01974E-001, 3.33733E-001, 3.68832E-001,
         3.87742E-001, 4.07622E-001, 4.50492E-001, 4.97871E-001, 5.23397E-001,
         5.50232E-001, 5.78443E-001, 6.08101E-001, 6.39279E-001, 6.72055E-001,
         7.06512E-001, 7.42736E-001, 7.80817E-001, 8.20850E-001, 8.62936E-001,
         9.07180E-001, 9.61672E-001, 1.00259E+000, 1.10803E+000, 1.16484E+000,
         1.22456E+000, 1.28735E+000, 1.35335E+000, 1.42274E+000, 1.49569E+000,
         1.57237E+000, 1.65299E+000, 1.73774E+000, 1.82684E+000, 1.92050E+000,
         2.01897E+000, 2.12248E+000, 2.23130E+000, 2.30693E+000, 2.34570E+000,
         2.36533E+000, 2.38513E+000, 2.46597E+000, 2.59240E+000, 2.72532E+000,
         2.86505E+000, 3.01194E+000, 3.16637E+000, 3.32871E+000, 3.67879E+000,
         4.06570E+000, 4.49329E+000, 4.72367E+000, 4.96585E+000, 5.22046E+000,
         5.48812E+000, 5.76950E+000, 6.06531E+000, 6.37628E+000, 6.59241E+000,
         6.70320E+000, 7.04688E+000, 7.40818E+000, 7.78801E+000, 8.18731E+000,
         8.60708E+000, 9.04837E+000, 9.51229E+000, 1.00000E+001, 1.05127E+001,
         1.10517E+001, 1.16183E+001, 1.22140E+001, 1.25232E+001, 1.28403E+001,
         1.34986E+001, 1.38403E+001, 1.41907E+001, 1.45499E+001, 1.49182E+001,
         1.56831E+001, 1.64872E+001, 1.69046E+001, 1.73325E+001, 1.96403E+001])

def histogram_indicator(indicator, title, label='', figname="similarity.png"):
    plt.hist(indicator, bins=20)
    plt.xlabel(label)
    plt.ylabel("Number of Mesh Voxels")
    plt.title(title)
    plt.savefig(figname, dpi=300)
    plt.close()

def n_flux_difference_analysis(model_name, n_flux1, n_flux2):
    """
    n_flux1 is the openmc
    n_flux2 is the dagopenmc,
    item could be 'flux' or 'flux_rel_err'
    """
    # calculate cosine similarity for each volume element
    zeros_shape = (n_flux1.shape[0],)
    similarities = np.zeros(zeros_shape)
    mse = np.zeros(zeros_shape)
    for i in range(mse.size):
        similarities[i] = cosine_similarity(n_flux1[i], n_flux2[i])
        mse[i] = mean_squared_error(n_flux1[i], n_flux2[i])

    similarity_title = "CSG to DGAMC Geometry Comparison - {}".format(model_name)
    mse_title = "CSG to DAGMC Geometry Comparison - {}".format(model_name)
    histogram_indicator(similarities, similarity_title, label='Cosine Similarity')
    histogram_indicator(mse, mse_title, label='Mean Squared Error', figname="mse.png")

def cosine_similarity(x,y):
    numerator = np.dot(x, y)
    denominator = np.linalg.norm(x) * np.linalg.norm(y)
    return numerator/ denominator

def mean_squared_error(x, y):
    if len(x) != len(y):
        raise ValueError("arrays have different length")
    diff = x-y
    numerator = np.sum(diff * diff)
    denominator = len(x)
    return numerator/denominator

def get_tally_results(statepoint_path, tally_id):
    """
    Get tally results.
    """
    sp = openmc.StatePoint(statepoint_path)
    tally = sp.get_tally(id=tally_id)
    return tally

def get_flux_res_rel_err(tally):
    """
    Get tally flux and convert to the shape od dims
    """

    # determine the number of energy groups from the tally
    for f in tally.filters:
        if isinstance(f, openmc.EnergyFilter):
            num_e_groups = f.num_bins

    # determine the voxel volumes from the mesh
    for f in tally.filters:
        if isinstance(f, openmc.MeshFilter):
            mesh = f.mesh
            num_ves = f.num_bins

    voxel_dims = (mesh.upper_right - mesh.lower_left) / mesh.dimension
    vol = np.prod(voxel_dims)

    flux = tally.get_slice(scores=['flux'])
    res = flux.mean
    rel_err = np.zeros_like(flux.std_dev)
    nonzero = flux.mean > 0
    rel_err[nonzero] = flux.std_dev[nonzero] / flux.mean[nonzero]

    std_dev = np.zeros_like(flux.std_dev)
    std_dev[nonzero] = flux.std_dev[nonzero]
    std_dev = np.divide(std_dev, vol)
    std_dev = np.reshape(std_dev, newshape=(num_e_groups, num_ves))
    std_dev = std_dev.transpose()

    res = np.divide(res, vol)
    res = np.reshape(res, newshape=(num_e_groups, num_ves))
    res = res.transpose()

    rel_err = np.reshape(rel_err, newshape=(num_e_groups, num_ves))
    rel_err = np.divide(rel_err, vol)
    rel_err = rel_err.transpose()
    return res, rel_err, std_dev

def get_res_rel_err_from_file(statepoint_path, tally_id):
    tally = get_tally_results(statepoint_path, tally_id=tally_id)
    res, rel_err, std_dev = get_flux_res_rel_err(tally)
    return res, rel_err, std_dev

def plot_new(model_name,
             flux,
             std_dev,
             dag_flux,
             dag_std_dev,
             figname='test.png'):

    ax1 = plt.subplot(211)
    ax2 = plt.subplot(212, sharex=ax1)

    legend_props = {'size' : 6}

    # Plot the spectra
    title = "Mesh Voxel Spectrum Comparison - {}".format(model_name)
    ax1.set_title(title)
    ax1.step(e_bins, flux, color='red', label='OpenMC')
    ax1.step(e_bins, dag_flux, color='blue', linestyle=':', label='DAG-OpenMC')
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_ylabel(r'Flux ($\frac{particle-cm}{source particle})$')
    ax1.legend(prop=legend_props, frameon=False)

    # compute the error of the relative difference
    nonzero = flux != 0
    err_bound = np.sqrt(std_dev**2 + dag_std_dev**2)
    err_bound[nonzero] /= flux[nonzero]
    err_bound *= 100.0

    rel_diff = (dag_flux - flux)
    rel_diff[nonzero] /= flux[nonzero]
    rel_diff *= 100.0

    ax2.step(e_bins, 2 * err_bound, color='black', linestyle=':', label='+/- 2 Std. Dev.')
    ax2.step(e_bins, -2 * err_bound, color='black',linestyle=':')
    ax2.step(e_bins, rel_diff, color='green')
    ax2.set_ylabel('Relative Difference (%)')
    ax2.set_xlabel('Energy (MeV)')
    ax2.legend(prop=legend_props, frameon=False)

    plt.savefig(figname, dpi=300)
    plt.close()

def perform_comparison(model_name, csg_statepoint, dagmc_statepoint, tally_id=1, summary_only=False):
    print("Compiling results...")

    csg_mean, csg_rel_err, csg_std_dev = get_res_rel_err_from_file(csg_statepoint, tally_id)

    dag_mean, dag_rel_err, dag_std_dev = get_res_rel_err_from_file(dagmc_statepoint, tally_id)

    print("Generating plots...")


    # analyze the difference
    n_flux_difference_analysis(model_name, csg_mean, dag_mean)

    # compare the n_flux of each voxel
    for i in range(csg_mean.shape[0]):
        figname = ''.join(['Neutron flux of mesh voxel', str(i), '.png'])
        plot_new(model_name,
                 csg_mean[i],
                 csg_std_dev[i],
                 dag_mean[i],
                 dag_std_dev[i],
                 figname=figname)


if __name__ == "__main__":
    ap = ArgumentParser(description="Comparison Script use of DAGMC geometry "
                                    "in OpenMC.")

    ap.add_argument("model_name", type=str, help="Name of the model to be used in plot titles")
    ap.add_argument("csg_statepoint", type=str, help="Path to the statepoint file generated using CSG")
    ap.add_argument("dagmc_statepoint", type=str, help="Path to the statepoint file generated using DAGMC")
    ap.add_argument("-tid", "--tally_id", type=int, default=1, help="Tally ID")
    ap.add_argument("-s", "--summary-only", action='store_true', default=False, help="Generate summary plots only.")

    args = ap.parse_args(sys.argv[1:])

    perform_comparison(args.model_name,
                       args.csg_statepoint,
                       args.dagmc_statepoint,
                       args.tally_id,
                       args.summary_only)
