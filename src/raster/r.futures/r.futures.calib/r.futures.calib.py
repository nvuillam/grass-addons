#!/usr/bin/env python3
#
##############################################################################
#
# MODULE:       r.futures.calib
#
# AUTHOR(S):    Anna Petrasova (kratochanna gmail.com)
#
# PURPOSE:      FUTURES patches calibration tool
#
# COPYRIGHT:    (C) 2016 by the GRASS Development Team
#
#               This program is free software under the GNU General Public
#               License (>=v2). Read the file COPYING that comes with GRASS
#               for details.
#
##############################################################################

#%module
#% description: Module for calibrating patch characteristics used as input to r.futures.pga
#% keyword: raster
#% keyword: patch
#%end
#%option G_OPT_R_INPUT
#% key: development_start
#% label: Name of input binary raster map representing development in the beginning
#% description: Raster map of developed areas (=1), undeveloped (=0) and excluded (no data)
#% guisection: Calibration
#%end
#%option G_OPT_R_INPUT
#% key: development_end
#% label: Name of input binary raster map representing development in the end
#% description: Raster map of developed areas (=1), undeveloped (=0) and excluded (no data)
#% guisection: Calibration
#%end
#%option
#% type: integer
#% key: repeat
#% description: How many times is the simulation repeated
#% required: no
#% guisection: Calibration
#%end
#%option
#% key: compactness_mean
#% type: double
#% description: Patch compactness mean to be tested
#% required: no
#% multiple: yes
#% guisection: Calibration
#%end
#%option
#% type: double
#% key: compactness_range
#% description: Patch compactness range to be tested
#% required: no
#% multiple: yes
#% guisection: Calibration
#%end
#%option
#% type: double
#% key: discount_factor
#% description: Patch size discount factor
#% key: discount_factor
#% multiple: yes
#% required: no
#% guisection: Calibration
#%end
#%option
#% type: double
#% key: patch_threshold
#% description: Minimum size of a patch in meters squared
#% required: yes
#% answer: 0
#% guisection: Calibration
#%end
#%option G_OPT_F_OUTPUT
#% key: patch_sizes
#% description: Output file with patch sizes
#% required: yes
#% guisection: Calibration
#%end
#%flag
#% key: s
#% description: Derive patch sizes per subregions
#% guisection: Calibration
#%end
#%option G_OPT_F_OUTPUT
#% key: calibration_results
#% description: Output file with calibration results
#% required: no
#% guisection: Calibration
#%end
#%option
#% key: nprocs
#% type: integer
#% description: Number of parallel processes
#% required: yes
#% answer: 1
#% guisection: Calibration
#%end
#%option
#% key: random_seed
#% type: integer
#% required: no
#% multiple: no
#% answer: 1
#% label: Seed for random number generator
#% description: The same seed can be used to obtain same results or random seed can be generated by other means.
#% guisection: Calibration
#%end
#%option G_OPT_R_INPUT
#% key: development_pressure
#% required: no
#% description: Raster map of development pressure
#% guisection: PGA
#%end
#%option
#% key: incentive_power
#% type: double
#% required: no
#% multiple: no
#% options: 0-10
#% label: Exponent to transform probability values p to p^x to simulate infill vs. sprawl
#% description: Values > 1 encourage infill, < 1 urban sprawl
#% guisection: PGA
#%end
#%option G_OPT_R_INPUT
#% key: potential_weight
#% required: no
#% label: Raster map of weights altering development potential
#% description: Values need to be between -1 and 1, where negative locally reduces probability and positive increases probability.
#% guisection: PGA
#%end
#%option G_OPT_R_INPUTS
#% key: predictors
#% required: no
#% multiple: yes
#% description: Names of predictor variable raster maps
#% guisection: PGA
#%end
#%option
#% key: n_dev_neighbourhood
#% type: integer
#% description: Size of square used to recalculate development pressure
#% required: no
#% guisection: PGA
#%end
#%option G_OPT_F_INPUT
#% key: devpot_params
#% required: no
#% multiple: yes
#% label: Development potential parameters for each region
#% description: Each line should contain region ID followed by parameters. Values are separated by whitespace (spaces or tabs). First line is ignored, so it can be used for header
#% guisection: PGA
#%end
#%option
#% key: num_neighbors
#% type: integer
#% required: no
#% multiple: no
#% options: 4,8
#% description: The number of neighbors to be used for patch generation (4 or 8)
#% guisection: PGA
#%end
#%option
#% key: seed_search
#% type: string
#% required: no
#% multiple: no
#% options: random,probability
#% description: The way location of a seed is determined
#% descriptions: random; uniform distribution; probability; development potential
#% guisection: PGA
#%end
#%option
#% key: development_pressure_approach
#% type: string
#% required: no
#% multiple: no
#% options: occurrence,gravity,kernel
#% description: Approaches to derive development pressure
#% guisection: PGA
#%end
#%option
#% key: gamma
#% type: double
#% required: no
#% multiple: no
#% description: Influence of distance between neighboring cells
#% guisection: PGA
#%end
#%option
#% key: scaling_factor
#% type: double
#% required: no
#% multiple: no
#% description: Scaling factor of development pressure
#% guisection: PGA
#%end
#%option
#% key: num_steps
#% type: integer
#% required: no
#% multiple: no
#% description: Number of steps to be simulated
#% guisection: PGA
#%end
#%option G_OPT_R_INPUT
#% key: subregions
#% required: yes
#% description: Raster map of subregions with categories starting with 1
#% guisection: PGA
#%end
#%option G_OPT_R_INPUT
#% key: subregions_potential
#% required: no
#% label: Raster map of subregions used with potential file
#% description: If not specified, the raster specified in subregions parameter is used
#% guisection: PGA
#%end
#%option G_OPT_F_INPUT
#% key: demand
#% required: no
#% description: Control file with number of cells to convert
#% guisection: PGA
#%end
#%option
#% key: memory
#% type: double
#% required: no
#% multiple: no
#% description: Memory for single run in GB
#%end
#%option G_OPT_F_SEP
#% label: Separator used in output patch file
#% answer: comma
#%end
#%flag
#% key: l
#% description: Only create patch size distribution file
#% guisection: Calibration
#%end
#%rules
#% collective: demand,scaling_factor,gamma,development_pressure_approach,seed_search,num_neighbors,devpot_params,n_dev_neighbourhood,predictors,development_pressure,calibration_results,discount_factor,compactness_range,compactness_mean,repeat
#% exclusive: -l,demand
#% exclusive: -l,num_steps
#% exclusive: -l,scaling_factor
#% exclusive: -l,gamma
#% exclusive: -l,development_pressure_approach
#% exclusive: -l,seed_search
#% exclusive: -l,num_neighbors
#% exclusive: -l,incentive_power
#% exclusive: -l,devpot_params
#% exclusive: -l,n_dev_neighbourhood
#% exclusive: -l,predictors
#% exclusive: -l,potential_weight
#% exclusive: -l,development_pressure
#% exclusive: -l,calibration_results
#% exclusive: -l,discount_factor
#% exclusive: -l,compactness_range
#% exclusive: -l,compactness_mean
#% exclusive: -l,repeat
#% exclusive: -l,memory
#% required: -l,demand
#% required: -l,scaling_factor
#% required: -l,gamma
#% required: -l,development_pressure_approach
#% required: -l,seed_search
#% required: -l,num_neighbors
#% required: -l,devpot_params
#% required: -l,n_dev_neighbourhood
#% required: -l,predictors
#% required: -l,development_pressure
#% required: -l,calibration_results
#% required: -l,discount_factor
#% required: -l,compactness_range
#% required: -l,compactness_mean
#% required: -l,repeat
#%end

import atexit
import os
import sys
from io import StringIO
from multiprocessing import Process, Queue

import grass.script.core as gcore
import grass.script.raster as grast
import grass.script.utils as gutils
import numpy as np
from grass.exceptions import CalledModuleError

TMP = []


def cleanup(tmp=None):
    if tmp:
        maps = tmp
    else:
        maps = TMP
    gcore.run_command(
        "g.remove", flags="f", type=["raster", "vector"], name=maps, quiet=True
    )


def check_addon_installed(addon, fatal=True):
    if not gcore.find_program(addon, "--help"):
        call = gcore.fatal if fatal else gcore.warning
        call(
            _(
                "Addon {a} is not installed." " Please install it using g.extension."
            ).format(a=addon)
        )


def run_one_combination(
    comb_count,
    comb_all,
    repeat,
    seed,
    development_start,
    compactness_mean,
    compactness_range,
    discount_factor,
    patches_file,
    fut_options,
    threshold,
    hist_bins_area_orig,
    hist_range_area_orig,
    hist_bins_compactness_orig,
    hist_range_compactness_orig,
    cell_size,
    histogram_area_orig,
    histogram_compactness_orig,
    tmp_name,
    queue,
):
    TMP_PROCESS = []
    # unique name, must be sql compliant
    suffix = (
        str(discount_factor) + str(compactness_mean) + str(compactness_range)
    ).replace(".", "")
    simulation_dev_end = tmp_name + "simulation_dev_end_" + suffix
    simulation_dev_diff = tmp_name + "simulation_dev_diff" + suffix
    tmp_clump = tmp_name + "tmp_clump" + suffix
    TMP_PROCESS.append(simulation_dev_diff)
    TMP_PROCESS.append(simulation_dev_end)
    TMP_PROCESS.append(tmp_clump)

    sum_dist_area = 0
    sum_dist_compactness = 0
    # offset seed
    seed *= 10000
    for i in range(repeat):
        f_seed = seed + i
        gcore.message(
            _(
                "Running calibration combination {comb_count}/{comb_all}"
                " of simulation attempt {i}/{repeat} with random seed {s}...".format(
                    comb_count=comb_count,
                    comb_all=comb_all,
                    i=i + 1,
                    repeat=repeat,
                    s=f_seed,
                )
            )
        )
        try:
            run_simulation(
                development_start=development_start,
                development_end=simulation_dev_end,
                compactness_mean=compactness_mean,
                compactness_range=compactness_range,
                discount_factor=discount_factor,
                patches_file=patches_file,
                seed=f_seed,
                fut_options=fut_options,
            )
        except CalledModuleError as e:
            queue.put(None)
            cleanup(tmp=TMP_PROCESS)
            gcore.error(_("Running r.futures.pga failed. Details: {e}").format(e=e))
            return
        new_development(simulation_dev_end, simulation_dev_diff)

        data = patch_analysis(simulation_dev_diff, threshold, tmp_clump)
        sim_hist_area, sim_hist_compactness = create_histograms(
            data,
            hist_bins_area_orig,
            hist_range_area_orig,
            hist_bins_compactness_orig,
            hist_range_compactness_orig,
            cell_size,
        )

        sum_dist_area += compare_histograms(histogram_area_orig, sim_hist_area)
        sum_dist_compactness += compare_histograms(
            histogram_compactness_orig, sim_hist_compactness
        )

    mean_dist_area = sum_dist_area / repeat
    mean_dist_compactness = sum_dist_compactness / repeat

    data = {}
    data["input_discount_factor"] = discount_factor
    data["input_compactness_mean"] = compactness_mean
    data["input_compactness_range"] = compactness_range
    data["area_distance"] = mean_dist_area
    data["compactness_distance"] = mean_dist_compactness
    queue.put(data)
    cleanup(tmp=TMP_PROCESS)


def run_simulation(
    development_start,
    development_end,
    compactness_mean,
    compactness_range,
    discount_factor,
    patches_file,
    seed,
    fut_options,
):
    parameters = dict(
        compactness_mean=compactness_mean,
        compactness_range=compactness_range,
        discount_factor=discount_factor,
        patch_sizes=patches_file,
        developed=development_start,
    )
    futures_parameters = dict(
        development_pressure=fut_options["development_pressure"],
        predictors=fut_options["predictors"],
        n_dev_neighbourhood=fut_options["n_dev_neighbourhood"],
        devpot_params=fut_options["devpot_params"],
        num_neighbors=fut_options["num_neighbors"],
        seed_search=fut_options["seed_search"],
        development_pressure_approach=fut_options["development_pressure_approach"],
        gamma=fut_options["gamma"],
        scaling_factor=fut_options["scaling_factor"],
        subregions=fut_options["subregions"],
        demand=fut_options["demand"],
        separator=fut_options["separator"],
        output=development_end,
        random_seed=seed,
        quiet=True,
    )
    parameters.update(futures_parameters)
    for not_required in (
        "potential_weight",
        "num_steps",
        "incentive_power",
        "subregions_potential",
    ):
        if fut_options[not_required]:
            parameters.update({not_required: fut_options[not_required]})

    gcore.run_command("r.futures.pga", overwrite=True, **parameters)


def diff_development(development_start, development_end, subregions, development_diff):
    grast.mapcalc(
        exp="{res} = if({subregions} && {dev_end} && (isnull({dev_start}) ||| !{dev_start}), 1, null())".format(
            res=development_diff,
            subregions=subregions,
            dev_end=development_end,
            dev_start=development_start,
        ),
        overwrite=True,
        quiet=True,
    )


def new_development(development_end, development_diff):
    grast.mapcalc(
        exp="{res} = if({dev_end} > 0, 1, null())".format(
            res=development_diff, dev_end=development_end
        ),
        overwrite=True,
        quiet=True,
    )


def patch_analysis_per_subregion(
    development_diff, subregions, threshold, tmp_clump, tmp_clump_cat
):
    gcore.run_command(
        "r.clump", input=development_diff, output=tmp_clump, overwrite=True, quiet=True
    )
    cats = (
        gcore.read_command("r.describe", flags="1n", map=subregions, quiet=True)
        .strip()
        .splitlines()
    )
    subregions_data = {}
    env = os.environ.copy()
    for cat in cats:
        grast.mapcalc(
            "{new} = if ({reg} == {cat}, {clump}, null())".format(
                new=tmp_clump_cat, reg=subregions, cat=cat, clump=tmp_clump
            ),
            overwrite=True,
        )
        env["GRASS_REGION"] = gcore.region_env(zoom=tmp_clump_cat)
        try:
            data = gcore.read_command(
                "r.object.geometry",
                input=tmp_clump_cat,
                flags="m",
                separator="comma",
                env=env,
                quiet=True,
            ).strip()
            data = np.loadtxt(StringIO(data), delimiter=",", usecols=(1, 2), skiprows=1)
            # in case there is just one record
            data = data.reshape((-1, 2))
            subregions_data[cat] = data[data[:, 0] > threshold]
        except CalledModuleError:
            gcore.warning(
                "Subregion {cat} has no changes in development, no patches found.".format(
                    cat=cat
                )
            )
            subregions_data[cat] = np.empty([0, 2])
    return subregions_data


def patch_analysis(development_diff, threshold, tmp_clump):
    gcore.run_command(
        "r.clump", input=development_diff, output=tmp_clump, overwrite=True, quiet=True
    )
    try:
        data = gcore.read_command(
            "r.object.geometry",
            input=tmp_clump,
            flags="m",
            separator="comma",
            quiet=True,
        ).strip()
        data = np.loadtxt(StringIO(data), delimiter=",", usecols=(1, 2), skiprows=1)
        # in case there is just one record
        data = data.reshape((-1, 2))
        data = data[data[:, 0] > threshold]
    except CalledModuleError:
        gcore.warning("No changes in development, no patches found.")
        data = np.empty([0, 2])
    return data


def create_histograms(
    data,
    hist_bins_area_orig,
    hist_range_area_orig,
    hist_bins_compactness_orig,
    hist_range_compactness_orig,
    cell_size,
):
    area, perimeter = data.T
    compact = compactness(area, perimeter)
    histogram_area, _edges = np.histogram(
        area / cell_size,
        bins=hist_bins_area_orig,
        range=hist_range_area_orig,
        density=True,
    )
    histogram_area = histogram_area * 100
    histogram_compactness, _edges = np.histogram(
        compact,
        bins=hist_bins_compactness_orig,
        range=hist_range_compactness_orig,
        density=True,
    )
    histogram_compactness = histogram_compactness * 100
    return histogram_area, histogram_compactness


def write_patches_file(data, cell_size, output_file, separator):
    if isinstance(data, dict):
        array_list = []
        keys = list(data.keys())
        for key in keys:
            areas = data[key][:, 0]
            areas = np.round(areas / cell_size)
            areas = np.sort(areas.astype(int))
            array_list.append(areas)

        max_patches = max([len(x) for x in array_list])
        new_array_list = []
        for array in array_list:
            new_array_list.append(
                np.pad(
                    array, (0, max_patches - len(array)), "constant", constant_values=-1
                )
            )
        data = np.column_stack(new_array_list)
        np.savetxt(output_file, X=data, fmt="%u")
        data = np.loadtxt(output_file, dtype=str)
        data[data == "-1"] = ""
        with open(output_file, "wb") as f:
            f.write(separator.join(keys).encode())
            f.write(b"\n")
            np.savetxt(f, X=data, delimiter=separator, fmt="%s")
    else:
        areas = data[:, 0]
        areas = np.round(areas / cell_size)
        np.savetxt(
            fname=output_file,
            X=np.sort(areas.astype(int)),
            delimiter=separator,
            fmt="%u",
        )


def compare_histograms(hist1, hist2):
    """
    >>> hist1, edg = np.histogram(np.array([1, 1, 2, 2.5, 2.4]), bins=3, range=(0, 6))
    >>> hist2, edg = np.histogram(np.array([1, 1, 3 ]), bins=3, range=(0, 6))
    >>> compare_histograms(hist1, hist2)
    0.5
    """
    mask = np.logical_not(np.logical_or(hist1, hist2))
    hist1 = np.ma.masked_array(hist1, mask=mask)
    hist2 = np.ma.masked_array(hist2, mask=mask)
    res = 0.5 * np.sum(np.power(hist1 - hist2, 2) / (hist1.astype(float) + hist2))
    return res


def compactness(area, perimeter):
    return perimeter / (2 * np.sqrt(np.pi * area))


def process_calibration(calib_file):
    disc, area_err, compact_mean, compact_range, compact_err = np.loadtxt(
        calib_file, unpack=True, delimiter=","
    )
    norm_area_err = area_err / np.max(area_err)
    norm_compact_err = compact_err / np.max(compact_err)
    averaged_error = (norm_area_err + norm_compact_err) / 2
    res = np.column_stack(
        (
            disc,
            compact_mean,
            compact_range,
            norm_area_err,
            norm_compact_err,
            averaged_error,
        )
    )
    res = res[res[:, 5].argsort()]
    header = ",".join(
        [
            "discount_factor",
            "compactness_mean",
            "compactness_range",
            "area_error",
            "compactness_error",
            "combined_error",
        ]
    )
    with open(calib_file, "wb") as f:
        f.write(header.encode())
        f.write(b"\n")
        np.savetxt(f, res, delimiter=",", fmt="%.2f")


def main():
    check_addon_installed("r.object.geometry", fatal=True)

    dev_start = options["development_start"]
    dev_end = options["development_end"]
    only_file = flags["l"]
    patches_per_subregion = flags["s"]
    if not only_file:
        repeat = int(options["repeat"])
        compactness_means = [
            float(each) for each in options["compactness_mean"].split(",")
        ]
        compactness_ranges = [
            float(each) for each in options["compactness_range"].split(",")
        ]
        discount_factors = [
            float(each) for each in options["discount_factor"].split(",")
        ]
    patches_file = options["patch_sizes"]
    threshold = float(options["patch_threshold"])
    sep = gutils.separator(options["separator"])
    # v.clean removes size <= threshold, we want to keep size == threshold
    threshold -= 1e-6

    # compute cell size
    region = gcore.region()
    res = (region["nsres"] + region["ewres"]) / 2.0
    coeff = float(gcore.parse_command("g.proj", flags="g")["meters"])
    cell_size = res * res * coeff * coeff

    tmp_name = "tmp_futures_calib_" + str(os.getpid()) + "_"
    global TMP

    orig_patch_diff = tmp_name + "orig_patch_diff"
    TMP.append(orig_patch_diff)
    tmp_clump = tmp_name + "tmp_clump"
    TMP.append(tmp_clump)
    if patches_per_subregion:
        tmp_cat_clump = tmp_name + "tmp_cat_clump"
        TMP.append(tmp_cat_clump)

    gcore.message(_("Analyzing original patches..."))
    diff_development(dev_start, dev_end, options["subregions"], orig_patch_diff)
    data = write_data = patch_analysis(orig_patch_diff, threshold, tmp_clump)
    if patches_per_subregion:
        subregions_data = patch_analysis_per_subregion(
            orig_patch_diff, options["subregions"], threshold, tmp_clump, tmp_cat_clump
        )
        # if there is just one column, write the previous analysis result
        if len(subregions_data.keys()) > 1:
            write_data = subregions_data
    write_patches_file(write_data, cell_size, patches_file, sep)

    if only_file:
        return

    area, perimeter = data.T
    compact = compactness(area, perimeter)

    # area histogram
    area = area / cell_size
    bin_width = (
        1.0  # automatic ways to determine bin width do not perform well in this case
    )
    hist_bins_area_orig = int(np.ptp(area) / bin_width)
    hist_range_area_orig = (np.min(area), np.max(area))
    histogram_area_orig, _edges = np.histogram(
        area, bins=hist_bins_area_orig, range=hist_range_area_orig, density=True
    )
    histogram_area_orig = histogram_area_orig * 100  # to get percentage for readability

    # compactness histogram
    bin_width = 0.1
    hist_bins_compactness_orig = int(np.ptp(compact) / bin_width)
    hist_range_compactness_orig = (np.min(compact), np.max(compact))
    histogram_compactness_orig, _edges = np.histogram(
        compact,
        bins=hist_bins_compactness_orig,
        range=hist_range_compactness_orig,
        density=True,
    )
    histogram_compactness_orig = (
        histogram_compactness_orig * 100
    )  # to get percentage for readability

    seed = int(options["random_seed"])
    nprocs = int(options["nprocs"])
    count = 0
    proc_count = 0
    queue_list = []
    proc_list = []
    num_all = len(compactness_means) * len(compactness_ranges) * len(discount_factors)
    with open(options["calibration_results"], "w") as f:
        for com_mean in compactness_means:
            for com_range in compactness_ranges:
                for discount_factor in discount_factors:
                    count += 1
                    q = Queue()
                    p = Process(
                        target=run_one_combination,
                        args=(
                            count,
                            num_all,
                            repeat,
                            seed,
                            dev_start,
                            com_mean,
                            com_range,
                            discount_factor,
                            patches_file,
                            options,
                            threshold,
                            hist_bins_area_orig,
                            hist_range_area_orig,
                            hist_bins_compactness_orig,
                            hist_range_compactness_orig,
                            cell_size,
                            histogram_area_orig,
                            histogram_compactness_orig,
                            tmp_name,
                            q,
                        ),
                    )
                    p.start()
                    queue_list.append(q)
                    proc_list.append(p)
                    proc_count += 1
                    seed += 1
                    if proc_count == nprocs or count == num_all:
                        for i in range(proc_count):
                            proc_list[i].join()
                            data = queue_list[i].get()
                            if not data:
                                continue
                            f.write(
                                ",".join(
                                    [
                                        str(data["input_discount_factor"]),
                                        str(data["area_distance"]),
                                        str(data["input_compactness_mean"]),
                                        str(data["input_compactness_range"]),
                                        str(data["compactness_distance"]),
                                    ]
                                )
                            )
                            f.write("\n")
                        f.flush()
                        proc_count = 0
                        proc_list = []
                        queue_list = []
    # compute combined normalized error
    process_calibration(options["calibration_results"])


if __name__ == "__main__":
    options, flags = gcore.parser()
    atexit.register(cleanup)
    sys.exit(main())
