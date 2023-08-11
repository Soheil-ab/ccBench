# ccBench
The ccBench repository intends to offer a first suite of congestion control benchmarks as detailed in the paper titled [Internet Congestion Control Benchmarking](https://arxiv.org/abs/2307.10054).

# Outline
- [What Is Included](#what-is-included)
- [Preparations](#preparations)
- [Installing Mahimahi's Patches](#installing-mahimahis-patches)
- [Installing Pantheon-Modified](#installing-pantheon-modified)
- [Installing Different CC Schemes](#installing-different-cc-schemes)
- [Running the Benchmarks](#running-the-benchmarks)
- [Reproducing Fig 1 and Fig 2](#reproducing-fig-1-and-fig-2)
- [Citation Guidelines](#citation-guidelines)

# What Is Included
This repository includes five main parts: 
1) Patched versions of [Mahimahi](https://github.com/ravinet/mahimahi), featuring a core patch (debugging original version) and AQM patches introducing two more queue management techs [BoDe](https://github.com/Soheil-ab/bode) and strict-priority queue management schemes.
2) Benchmarking environments, including traces that outline link capacity variations over time.
3) A modified version of [Pantheon](https://github.com/StanfordSNR/pantheon), modified scripts and codes to generate/process the required formats
4) Codes required to execute the benchmarking processes, prepare the required outputs, and generate the rankings.
5) Required codes/scripts to reproduce Figures 1 and 2 appeared in [Internet Congestion Control Benchmarking](https://arxiv.org/abs/2307.10054).

# Preparations
To prepare for the benchmarking process, we need to bring up at least three things:
1) The patched version of the emulator (Mahimahi)
2) The Pantheon-modified 
3) The schemes that are going to be included in the benchmarks

Begin by cloning the repository:

```bash
cd ~
git clone https://github.com/Soheil-ab/ccBench.git
cd ccBench
git submodule update --init --recursive
```

## Installing Mahimahi's Patches
We assume that you have not installed Mahimahi before on your system. Otherwise, uninstall it before continuing with the following steps.
1. Obtain Mahimahi's source code:
```bash
cd ~/ccBench
sudo apt-get install build-essential git debhelper autotools-dev dh-autoreconf iptables protobuf-compiler libprotobuf-dev pkg-config libssl-dev dnsmasq-base ssl-cert libxcb-present-dev libcairo2-dev libpango1.0-dev iproute2 apache2-dev apache2-bin iptables dnsmasq-base gnuplot iproute2 apache2-api-20120211 libwww-perl
git clone https://github.com/ravinet/mahimahi
```

2. Apply the provided patches:
```bash
cd mahimahi/
patch -p1 < ../patches/mahimahi.core.v2.2.patch 
patch -p1 < ../patches/mahimahi.extra.aqm.v1.5.patch
./autogen.sh && ./configure && make
sudo make install
sudo sysctl -w net.ipv4.ip_forward=1
```

If everything goes well, we should have Mahimahi patches installed. Make sure that no errors occurred during these steps.

## Installing Pantheon-Modified
Now, we install Pantheon-modified. 
```bash
cd ~/ccBench/pantheon-modified/tools/
./install_deps.sh
```

## Installing Different CC Schemes
This part can become __a little bit messy__, because each scheme may require certain libraries/packages to be installed! 
So, to make the story short here, you need to check out __the original instructions__ provided by the creators of different CC schemes to install them.
For instance, to install [Sage](https://github.com/Soheil-ab/sage), [Orca](https://github.com/Soheil-ab/Orca), [DeepCC](https://github.com/Soheil-ab/DeepCC.v1.0), & [C2TCP](https://github.com/Soheil-ab/c2tcp), you need to install the provided Linux kernel (4.19.112-0062), install certain python packages, and then compile and make the source code.  

We have already provided you with some simple wrappers that you can utilize to benchmark the CC schemes that are currently implemented in Linux Kernel (e.g. Cubic, Vegas, Westwood, Reno, Illinois, YeAH, ...) without installing extra packages.

# Running the Benchmarks
For now, let's assume that the list of CC schemes to be benchmarked is "cubic vegas" (after installing other schemes properly, you can simply add their names to this list).  

First, we copy the benchmark environments to the appropriate location:
```bash
cp -r ~/ccBench/traces ~/ccBench/pantheon-modified/src/experiments/
```
Now, we can start running the benchmarks. 
## ccBench1 (single-flow/solo benchmark) 
The process is quite simple. For instance, the following will start the ccBench1 (single-flow/solo benchmark):
```bash
cd ~/ccBench/pantheon-modified/src/experiments/
chmod +x solo_runall.sh
./solo_runall.sh
```

Notes: 
1) To change the list of CC schemes, simply edit the solo_runall.sh file (__schemes__ list therein). 
2) The overall runtime depends on the number of schemes in this list, the number of CPUs, the amount of available memory, etc., and can take up to at least a few hours. A good suggestion is always to start with one or two schemes in the list to get a proper sense of the required overall time and storage, before running them for a big set of schemes.
3) A rough estimation is that you'll need ~11GB and 27GB for the __final__ raw data results of __a__ CC scheme in ccBench1 and ccBench2, respectively. Although the current scripts already try to minimize the storage usage throughout the runs and clean up the temporary files, during the runs, you may still need 2X more than that.
4) Roughly speaking, 6 cores will be dedicated to any scenario, and bash scripts try to fully utilize all your available CPUs by running tests in parallel. In case, you wish to limit this, manually specify the desired maximum available cores.

When finished, the raw results will be stored in ```ccBench/pantheon-modified/src/experiments/data``` folder. Assuming everything goes well, at the end of the solo_runall.sh script, the raw results are already preprocessed. So now, we need to use them and generate the ranking of the CC schemes.

```bash
cd ~/ccBench/pantheon-modified/src/experiments/
chmod +x league.sh
./league.sh
```

This will start examining the raw results, create proper scores for each scheme on individual scenarios, and make the final ranking among the CC schemes. 

```bash
cat ~/ccBench/pantheon-modified/src/experiments/data/charts-overall-ranking-single-flow-10
```

## ccBench2 (multi-flow/friendliness benchmark) 
The process is similar to ccBench1, except you need to run the following.
```bash
cd ~/ccBench/pantheon-modified/src/experiments/
chmod +x multi_runall.sh league-2flows.sh
./multi_runall.sh
./league-2flows.sh
```

## Draw the ranking

```bash
cd ~/ccBench/pantheon-modified/src/experiments/
chmod +x plot.rankings.sh
./plot.rankings.sh data/charts-overall-ranking-single-flow-10 ranking-single-flow 3
```

The resulting figure is saved as __ranking-single-flow.svg__.

# Reproducing Fig 1 and Fig 2
Put the provided files in the proper places!
```bash
cd ~/ccBench
cp fig1/* pantheon-modified/src/experiments/
cp fig2/* pantheon-modified/src/experiments/
```

Now, for Fig 1:
```bash
cd pantheon-modified/src/experiments/
chmod +x run_score_buffer.sh
./run_score_buffer.sh
```
The figure is saved as ```score_buffer_v3.svg```. You can also see the results in ```data/buffersize_results```

For Fig 2:
```bash
chmod +x run_score_rtt.sh 
./run_score_rtt.sh
```
The figure is saved as ```score_mrtt_v3.svg```. You can also see the results in ```data/rtt_results```

# Citation Guidelines
 
Please use the following format to cite this repository: 

```bib
@article{ccBench,
  title={Internet Congestion Control Benchmarking},
  author={Abbasloo, Soheil},
  journal={arXiv preprint arXiv:2307.10054},
  year={2023}
}
```
