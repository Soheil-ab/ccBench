# Pantheon-modified
## Disclaimer
The base code here is a patched version of [Pantheon](https://github.com/StanfordSNR/pantheon.git).

# Installing & Executing Some Sample CC Schemes

## TcpDataGen
This is the policy collector engine used in the [Sage (SIGCOMM'23)](https://github.com/Soheil-ab/sage/) paper. Moreover, it can be used as a base code to run different Kernel-implemented CC schemes and add customized/desired stuff around them!

To install it, after installing the patched Mahimahi (check [ccBench](https://github.com/Soheil-ab/ccBench) for installation instructions), you can simply do the following:
```bash
cd ~/pantheon-modified/src/experiments/
./setup.py --setup --schemes tcpdatagen
```

Note: tcpdatagen requires the patched Mahimahi installed.

Now, you can run a sample experiment with TcpDataGen:
```bash
./cc_dataset_gen_solo.sh vegas single-flow-scenario 1 1 0 10 1000 0 48 30 48 48
```
This experiment will bring up a network with 48Mbps link capacity, a fifo bottleneck queue with a size of 1000 packets, and a one-way delay of 10ms. Then, it sends one flow for the 30s using TCP Vegas as its CC scheme. The raw dataset will be generated and located at ~/pantheon-modified/third_party/tcpdatagen/dataset/
Moreover, the general log of the experiment will be at ~/pantheon-modified/src/experiments/data/ 

```bash
./cc_dataset_gen_multi.sh vegas multi-flow-scenario 2 1 0 10 1000 48 120 48 48
```
This experiment will bring up the same network mentioned above. However, this time, it makes two flows sharing this bottleneck link for 120s, one using TCP Vegas as its CC scheme, and the other one using default TCP (cubic). Once again, the raw generated dataset will be at ~/pantheon-modified/third_party/tcpdatagen/dataset/, and the general log of the experiment will be put at ~/pantheon-modified/src/experiments/data/ 

Note: In a normal wired scenario, the last two inputs should be equal to the link capacity (i.e., the fourth-to-last input). You can check out cc_dataset_gen_multi.sh script to understand its inputs. 


__Stay Tuned! More schemes will be added soon!__

## To be continued ...!