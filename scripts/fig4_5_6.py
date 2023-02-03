import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cm as cm
import os, sys, pdb, csv, glob
import pandas as pd

from sdo_pypline.paths import root

# use style
plt.style.use("my.mplstyle"); plt.ioff()

# get color palette (seaborn colorblind hex)
colors = ['#0173b2', '#de8f05', '#029e73', '#d55e00', '#cc78bc',
          '#ca9161', '#fbafe4', '#949494', '#ece133', '#56b4e9']

pl_color = "tab:purple" # colors[4]
nw_color = "tab:pink" # colors[6]
qs_color = "tab:orange" # colors[1]
rp_color = "tab:red" # colors[3]
bp_color = "tab:blue" # colors[9]
pu_color = "sienna" # colors[5]
um_color = "tab:gray" # colors[7]

pl_marker = "s"
nw_marker = "p"
qs_marker = "o"
rp_marker = "v"
bp_marker = "^"
pu_marker = "X"
um_marker = "D"


def calc_region_stats(region_df, colname="v_hat"):
    # get number elements
    lo_mus = np.unique(region_df.lo_mu[~np.isnan(region_df.lo_mu)])
    nn = len(lo_mus)

    # allocate memory
    reg_avg = np.zeros(nn)
    reg_std = np.zeros(nn)
    reg_err = np.zeros(nn)

    # loop over mu rings
    for i in range(nn):
        # get idx
        idx = region_df.lo_mu == lo_mus[i]

        # calculate the stats
        reg_avg[i] = np.mean(region_df[colname][idx])
        reg_std[i] = np.std(region_df[colname][idx])
        reg_err[i] = reg_avg[i]/np.sqrt(len(region_df[colname][idx]))
    return reg_avg, reg_std, reg_err

# sort out paths
datadir = str(root / "data") + "/"
plotdir = str(root / "figures") + "/"
procdir = datadir + "processed/"

# read in by region
df_vels_full = pd.read_csv(procdir + "full_disk_vels.csv")
plage = pd.read_csv(procdir + "plage_vels.csv")
network = pd.read_csv(procdir + "network_vels.csv")
quiet_sun = pd.read_csv(procdir + "quiet_sun_vels.csv")
penumbrae = pd.read_csv(procdir + "penumbrae_vels.csv")
red_penumbrae = pd.read_csv(procdir + "red_penumbrae_vels.csv")
blu_penumbrae = pd.read_csv(procdir + "blu_penumbrae_vels.csv")
umbrae = pd.read_csv(procdir + "umbrae_vels.csv")

# get centers of mu bins
lo_mus = np.unique(plage.lo_mu)
hi_mus = np.unique(plage.hi_mu)
mu_bin = (lo_mus + hi_mus) / 2.0

# get stats
def clv_plot(fname=None):
    # set error bar props
    capsize = 0.0
    capthick = 0.0
    elinewidth = 0.0

    # make figure objects
    fig, axs = plt.subplots(nrows=2, ncols=2, sharex=True, figsize=(12.8, 7.2))
    fig.subplots_adjust(hspace=0.05, wspace=0.1)

    # get stats in v_hat
    umbrae_avg, umbrae_std, umbrae_err = calc_region_stats(umbrae, colname="v_hat")
    blue_penumbrae_avg, blue_penumbrae_std, blue_penumbrae_err = calc_region_stats(blu_penumbrae, colname="v_hat")
    red_penumbrae_avg, red_penumbrae_std, red_penumbrae_err = calc_region_stats(red_penumbrae, colname="v_hat")
    penumbrae_avg, penumbrae_std, penumbrae_err = calc_region_stats(penumbrae, colname="v_hat")
    quiet_sun_avg, quiet_sun_std, quiet_sun_err = calc_region_stats(quiet_sun, colname="v_hat")
    network_avg, network_std, network_err = calc_region_stats(network, colname="v_hat")
    plage_avg, plage_std, plage_err = calc_region_stats(plage, colname="v_hat")

    # plot v_hat
    axs[0,0].errorbar(mu_bin, quiet_sun_avg, yerr=quiet_sun_err, fmt=qs_marker, capsize=capsize,
                      capthick=capthick, elinewidth=elinewidth, color=qs_color, label=r"${\rm Quiet\ Sun}$")
    axs[0,0].fill_between(mu_bin, quiet_sun_avg - quiet_sun_std, quiet_sun_avg + quiet_sun_std, color=qs_color, alpha=0.5)

    axs[0,0].errorbar(mu_bin, plage_avg, yerr=plage_err, fmt=pl_marker, capsize=capsize,
                      capthick=capthick, elinewidth=elinewidth, color=pl_color, label=r"${\rm Plage}$")
    axs[0,0].fill_between(mu_bin, plage_avg - plage_std, plage_avg + plage_std, color=pl_color, alpha=0.4)

    axs[0,0].errorbar(mu_bin, network_avg, yerr=network_err, fmt=nw_marker, capsize=capsize,
                      capthick=capthick, elinewidth=elinewidth, color=nw_color, label=r"${\rm Network}$")
    axs[0,0].fill_between(mu_bin, network_avg - network_std, network_avg + network_std, color=nw_color, alpha=0.4)

    axs[1,0].errorbar(mu_bin, red_penumbrae_avg, yerr=red_penumbrae_err, fmt=rp_marker, capsize=capsize,
                      capthick=capthick, elinewidth=elinewidth, color=rp_color, label=r"${\rm Red\ Penumbrae}$")
    axs[1,0].fill_between(mu_bin, red_penumbrae_avg - red_penumbrae_std, red_penumbrae_avg + red_penumbrae_std, color=rp_color, alpha=0.4)

    axs[1,0].errorbar(mu_bin, blue_penumbrae_avg, yerr=blue_penumbrae_err, fmt=bp_marker, capsize=capsize,
                      capthick=capthick, elinewidth=elinewidth, color=bp_color, label=r"${\rm Blue\ Penumbrae}$")
    axs[1,0].fill_between(mu_bin, blue_penumbrae_avg - blue_penumbrae_std, blue_penumbrae_avg + blue_penumbrae_std, color=bp_color, alpha=0.4)

    axs[1,0].errorbar(mu_bin, penumbrae_avg, yerr=penumbrae_err, fmt=pu_marker, capsize=capsize,
                      capthick=capthick, elinewidth=elinewidth, color=pu_color, label=r"${\rm Penumbrae}$")
    axs[1,0].fill_between(mu_bin, penumbrae_avg - penumbrae_std, penumbrae_avg + penumbrae_std, color=pu_color, alpha=0.4)

    axs[1,0].errorbar(mu_bin, umbrae_avg, yerr=umbrae_err, fmt=um_marker, capsize=capsize,
                      capthick=capthick, elinewidth=elinewidth, color=um_color, label=r"${\rm Umbrae}$")
    axs[1,0].fill_between(mu_bin, umbrae_avg - umbrae_std, umbrae_avg + umbrae_std, color=um_color, alpha=0.4)

    # get stats for v_conv
    umbrae_avg, umbrae_std, umbrae_err = calc_region_stats(umbrae, colname="v_conv")
    blue_penumbrae_avg, blue_penumbrae_std, blue_penumbrae_err = calc_region_stats(blu_penumbrae, colname="v_conv")
    red_penumbrae_avg, red_penumbrae_std, red_penumbrae_err = calc_region_stats(red_penumbrae, colname="v_conv")
    penumbrae_avg, penumbrae_std, penumbrae_err = calc_region_stats(penumbrae, colname="v_conv")
    quiet_sun_avg, quiet_sun_std, quiet_sun_err = calc_region_stats(quiet_sun, colname="v_conv")
    network_avg, network_std, network_err = calc_region_stats(network, colname="v_conv")
    plage_avg, plage_std, plage_err = calc_region_stats(plage, colname="v_conv")

    axs[0,1].errorbar(mu_bin, plage_avg, yerr=plage_err, fmt=pl_marker, capsize=capsize,
                 capthick=capthick, elinewidth=elinewidth, color=pl_color, label=r"${\rm Plage}$")
    axs[0,1].fill_between(mu_bin, plage_avg - plage_std, plage_avg + plage_std, color=pl_color, alpha=0.4)

    axs[0,1].errorbar(mu_bin, network_avg, yerr=network_err, fmt=nw_marker, capsize=capsize,
                 capthick=capthick, elinewidth=elinewidth, color=nw_color, label=r"${\rm Network}$")
    axs[0,1].fill_between(mu_bin, network_avg - network_std, network_avg + network_std, color=nw_color, alpha=0.4)

    axs[1,1].errorbar(mu_bin, red_penumbrae_avg, yerr=red_penumbrae_err, fmt=rp_marker, capsize=capsize,
                 capthick=capthick, elinewidth=elinewidth, color=rp_color, label=r"${\rm Red\ Penumbrae}$")
    axs[1,1].fill_between(mu_bin, red_penumbrae_avg - red_penumbrae_std, red_penumbrae_avg + red_penumbrae_std, color=rp_color, alpha=0.4)

    axs[1,1].errorbar(mu_bin, blue_penumbrae_avg, yerr=blue_penumbrae_err, fmt=bp_marker, capsize=capsize,
                 capthick=capthick, elinewidth=elinewidth, color=bp_color, label=r"${\rm Blue\ Penumbrae}$")
    axs[1,1].fill_between(mu_bin, blue_penumbrae_avg - blue_penumbrae_std, blue_penumbrae_avg + blue_penumbrae_std, color=bp_color, alpha=0.4)

    axs[1,1].errorbar(mu_bin, penumbrae_avg, yerr=penumbrae_err, fmt=pu_marker, capsize=capsize,
                 capthick=capthick, elinewidth=elinewidth, color=pu_color, label=r"${\rm Penumbrae}$")
    axs[1,1].fill_between(mu_bin, penumbrae_avg - penumbrae_std, penumbrae_avg + penumbrae_std, color=pu_color, alpha=0.4)

    axs[1,1].errorbar(mu_bin, umbrae_avg, yerr=umbrae_err, fmt=um_marker, capsize=capsize,
                 capthick=capthick, elinewidth=elinewidth, color=um_color, label=r"${\rm Umbrae}$")
    axs[1,1].fill_between(mu_bin, umbrae_avg - umbrae_std, umbrae_avg + umbrae_std, color=um_color, alpha=0.4)

    # set limits
    axs[0,0].set_ylim(-210, 260)
    axs[0,1].set_ylim(-210, 260)
    axs[1,0].set_ylim(-1000, 1000)
    axs[1,1].set_ylim(-1000, 1000)

    # deal with xlabels
    axs[1,0].set_xlabel(r"$\mu$")
    axs[1,1].set_xlabel(r"$\mu$")
    axs[0,0].set_xticks(np.arange(0.1, 1.1, 0.1))
    axs[0,0].invert_xaxis()

    # deal with ylabels
    ylabel1 = r"$\hat{v}\ {\rm(m\ s}^{-1}{\rm )}$"
    ylabel2 = r"$\Delta \hat{v}_{\rm conv}\ {\rm(m\ s}^{-1}{\rm )}$"
    axs[0,0].set_ylabel(ylabel1)
    axs[1,0].set_ylabel(ylabel1)
    axs[0,1].set_ylabel(ylabel2)
    axs[1,1].set_ylabel(ylabel2)
    axs[0,1].yaxis.tick_right()
    axs[1,1].yaxis.tick_right()
    # axs[0,1].set_yticklabels([])
    # axs[1,1].set_yticklabels([])

    # make the legend
    lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
    lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
    _, idx = np.unique(labels, return_index=True)
    fig.legend([lines[i] for i in np.sort(idx)],
               [labels[i] for i in np.sort(idx)],
               ncol=7, fontsize=11.5, loc='upper center',
               handletextpad=0.15, bbox_to_anchor=(0.51, 0.94))

    # save the figure
    plt.savefig(plotdir + fname, bbox_inches="tight")
    plt.clf(); plt.close()
    return None

clv_plot("fig4.pdf")

# get distributions of velocities at different mu positions
mu_samps = [0.9, 0.8, 0.4, 0.2]
n_mu_samps = len(mu_samps)

# create figure objects
colname = "v_hat"
xlabel = r"$\hat{v}\ {\rm(m\ s}^{-1}{\rm )}$"
fig, axs = plt.subplots(figsize=(11, 8.5), nrows=3, ncols=n_mu_samps)
fig.subplots_adjust(wspace=0.07, hspace=0.15)

# loop over valus
ylims = np.zeros(n_mu_samps)
for i in range(n_mu_samps):
    # do all regs
    idx1 = umbrae.lo_mu == mu_samps[i]
    idx2 = red_penumbrae.lo_mu == mu_samps[i]
    idx3 = blu_penumbrae.lo_mu == mu_samps[i]
    idx4 = penumbrae.lo_mu == mu_samps[i]

    # plot this mu
    axs[0,i].hist(umbrae[colname][idx1], bins="auto", density=True, color=um_color, histtype="step", label=r"{\rm Umbrae}")
    axs[0,i].hist(red_penumbrae[colname][idx2], bins="auto", density=True, color=rp_color, histtype="step", label=r"{\rm Red\ Penumbrae}")
    axs[0,i].hist(blu_penumbrae[colname][idx3], bins="auto", density=True, color=bp_color, histtype="step", label=r"{\rm Blue\ Penumbrae}")
    axs[0,i].hist(penumbrae[colname][idx4], bins="auto", density=True, color=pu_color, histtype="step", label=r"{\rm Penumbrae}")

    # label stuff
    axs[0,i].set_title(r"$\mu = " + str(mu_samps[i] + 0.05)[0:4]+ r"$")
    axs[0,i].set_xlim(-1200, 1200)

    ylims[i] = axs[0,i].get_ylim()[1]

    if i > 0:
        axs[0,i].set_yticklabels([])

    if i == n_mu_samps - 1:
        axs[0,i].legend(fontsize=10)

# loop again to set yvals
for i in range(n_mu_samps):
    axs[0,i].set_ylim(0.0, np.max(ylims))

# loop over valus
ylims = np.zeros(n_mu_samps)
for i in range(n_mu_samps):
    # do all regs
    idx1 = plage.lo_mu == mu_samps[i]
    idx2 = network.lo_mu == mu_samps[i]

    # pl1,ot this mu
    axs[1,i].hist(plage[colname][idx1], bins="auto", density=True, color=pl_color, histtype="step", label=r"{\rm Plage}")
    axs[1,i].hist(network[colname][idx2], bins="auto", density=True, color=nw_color, histtype="step", label=r"{\rm Network}")

    # label stuff
    axs[1,i].set_xlim(-250,250)

    ylims[i] = axs[1,i].get_ylim()[1]

    if i > 0:
        axs[1,i].set_yticklabels([])

    if i == n_mu_samps - 1:
        axs[1,i].legend(fontsize=10)

# loop again to set yvals
for i in range(n_mu_samps):
    axs[1,i].set_ylim(0.0, np.max(ylims))

# loop over valus
ylims = np.zeros(n_mu_samps)
for i in range(n_mu_samps):
    # do all regs
    idx3 = quiet_sun.lo_mu == mu_samps[i]
    axs[2,i].hist(quiet_sun[colname][idx3], bins="auto", density=True, color=qs_color, histtype="step", label=r"{\rm Quiet Sun}")

    # label stuff
    axs[2,i].set_xlabel(xlabel)
    axs[2,i].set_xlim(-150,150)

    ylims[i] = axs[2,i].get_ylim()[1]

    if i > 0:
        axs[2,i].set_yticklabels([])

    if i == n_mu_samps - 1:
        axs[2,i].legend(fontsize=10)

# loop again to set yvals
for i in range(n_mu_samps):
    axs[2,i].set_ylim(0.0, np.max(ylims))

# set axes labels
for i in range(3):
    axs[i, 0].set_ylabel(r"${\rm Probability\ Density}$")

# save the figure
fig.savefig(plotdir + "fig5.pdf")
plt.clf(); plt.close()

# create figure objects
colname = "v_conv"
xlabel = r"$\Delta \hat{v}_{\rm conv}\ {\rm(m\ s}^{-1}{\rm )}$"
fig, axs = plt.subplots(figsize=(11, 5.8), nrows=2, ncols=n_mu_samps)
fig.subplots_adjust(wspace=0.07, hspace=0.15)

# loop over values
ylims = np.zeros(n_mu_samps)
for i in range(n_mu_samps):
    # do all regs
    idx1 = umbrae.lo_mu == mu_samps[i]
    idx2 = red_penumbrae.lo_mu == mu_samps[i]
    idx3 = blu_penumbrae.lo_mu == mu_samps[i]
    idx4 = penumbrae.lo_mu == mu_samps[i]

    # plot this mu
    axs[0,i].hist(umbrae[colname][idx1], bins="auto", density=True, color=um_color, histtype="step", label=r"{\rm Umbrae}")
    axs[0,i].hist(red_penumbrae[colname][idx2], bins="auto", density=True, color=rp_color, histtype="step", label=r"{\rm Red\ Penumbrae}")
    axs[0,i].hist(blu_penumbrae[colname][idx3], bins="auto", density=True, color=bp_color, histtype="step", label=r"{\rm Blue\ Penumbrae}")
    axs[0,i].hist(penumbrae[colname][idx4], bins="auto", density=True, color=pu_color, histtype="step", label=r"{\rm Penumbrae}")

    # label stuff
    axs[0,i].set_title(r"$\mu = " + str(mu_samps[i] + 0.05)[0:4]+ r"$")
    axs[0,i].set_xlim(-1200, 1200)

    ylims[i] = axs[0,i].get_ylim()[1]

    if i > 0:
        axs[0,i].set_yticklabels([])

# loop again to set yvals
for i in range(n_mu_samps):
    axs[0,i].set_ylim(0.0, np.max(ylims))

# loop over values
ylims = np.zeros(n_mu_samps)
for i in range(n_mu_samps):
    # do all regs
    idx1 = plage.lo_mu == mu_samps[i]
    idx2 = network.lo_mu == mu_samps[i]

    # plot this mu
    axs[1,i].hist(plage[colname][idx1], bins="auto", density=True, color=pl_color, histtype="step", label=r"{\rm Plage}")
    axs[1,i].hist(network[colname][idx2], bins="auto", density=True, color=nw_color, histtype="step", label=r"{\rm Network}")

    # label stuff
    axs[1,i].set_xlabel(xlabel)
    axs[1,i].set_xlim(-250,250)

    ylims[i] = axs[1,i].get_ylim()[1]

    if i > 0:
        axs[1,i].set_yticklabels([])

# loop again to set yvals
for i in range(n_mu_samps):
    axs[1,i].set_ylim(0.0, np.max(ylims))

# set axes labels
axs[0,0].set_ylabel(r"${\rm Probability\ Density}$")
axs[1,0].set_ylabel(r"${\rm Probability\ Density}$")
# axs[-1].legend(fontsize=10)
fig.savefig(plotdir + "fig6.pdf")
plt.clf(); plt.close()