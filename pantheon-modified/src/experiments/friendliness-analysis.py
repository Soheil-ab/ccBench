import numpy as np
import json
import argparse
from os import path
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--datadir", "-d", help="datadirectory containing json files for the evaluation")
    #parser.add_argument("--metainfo", "-md", help="information json file name for the evaluation")
    #parser.add_argument("--metadata", "-md", help="metadata json file name for the evaluation")

    args = parser.parse_args()
    data_path = path.join(args.datadir, 'pantheon_perf.json')
    info_path = path.join(args.datadir, 'pantheon_metadata.json')

    with open(info_path) as json_file:
        info = json.load(json_file)
    all_schemes = info['cc_schemes']
    run_times   = info['run_times']
    flows       = info['flows']

    with open(data_path) as json_file:
        meta = json.load(json_file)

    min_del_95=999999.0
    min_del_avg=999999.0
    min_del_90=999999.0
    min_del_mean=999999.0
    min_del_jitter=999999.0
    max_gput=0.0
    max_tput=0.0
    min_p=999999.0
    min_p90=999999.0
    min_p95=999999.0
    min_loss=0.0
    final={}
    #Avg:
    for cc in all_schemes:
        final[cc]={}
        final[cc]['samples']=0
        final[cc]['gput']=[]
        final[cc]['tput']=[]
        final[cc]['delay_95']=[]
        final[cc]['delay_avg']=[]
        final[cc]['delay_90']=[]
        final[cc]['delay_mean']=[]
        final[cc]['loss']=[]
        final[cc]['jitter']=[]
        final[cc]['power']=[]
        final[cc]['power_95']=[]
        final[cc]['power_90']=[]
        for run_id in xrange(1, 1 + run_times):
            for flow_id in xrange(2, 3):
                try:
                    #if meta[cc][str(run_id)][str(flow_id)]['delay_avg']>0:
                    final[cc]['samples']+=1
                    final[cc]['gput'].append(meta[cc][str(run_id)][str(flow_id)]['gput'])
                    final[cc]['tput'].append(meta[cc][str(run_id)][str(flow_id)]['tput'])
                    final[cc]['delay_95'].append(meta[cc][str(run_id)][str(flow_id)]['delay'])
                    final[cc]['delay_avg'].append(meta[cc][str(run_id)][str(flow_id)]['delay_avg'])
                    final[cc]['delay_90'].append(meta[cc][str(run_id)][str(flow_id)]['delay_90'])
                    final[cc]['jitter'].append(meta[cc][str(run_id)][str(flow_id)]['jitter'])
                    final[cc]['delay_mean'].append(meta[cc][str(run_id)][str(flow_id)]['delay_mean'])
                    final[cc]['loss'].append(meta[cc][str(run_id)][str(flow_id)]['loss'])
                    final[cc]['power'].append(meta[cc][str(run_id)][str(flow_id)]['tput']/meta[cc][str(run_id)][str(flow_id)]['delay_avg'])
                    final[cc]['power_90'].append(meta[cc][str(run_id)][str(flow_id)]['tput']/meta[cc][str(run_id)][str(flow_id)]['delay_90'])
                    final[cc]['power_95'].append(meta[cc][str(run_id)][str(flow_id)]['tput']/meta[cc][str(run_id)][str(flow_id)]['delay'])
                except:
                    print("no valid data for "+str(cc)+"\n")

        total=final[cc]['samples']

        final[cc]['mean']=np.mean(final[cc]['tput'])
        final[cc]['std']=np.std(final[cc]['tput'])


    tmp_file = path.join(args.datadir, 'tmp')
    perf_sum_abs = path.join(args.datadir, 'perf_friendliness.txt')

    final_file= open(tmp_file,"w")
    final_file.write("scheme \t mean_thr \t std \n")

    for cc in all_schemes:
       #final_file.write("{:s} \t {:.3f} \t {:.3f} \t {:.3f} \t {:.3f} \t {:.3f} \t {:.3f} \t {:.3f} \t {:.3f} \t {:.3f} \t {:.3f} \n".format(cc,final[cc]['tput_abs'], final[cc]['delay_avg_abs'],final[cc]['delay_90_abs'],final[cc]['delay_95_abs'],final[cc]['delay_mean_abs'],final[cc]['jitter_abs'],final[cc]['power_abs'],final[cc]['power_90_abs'],final[cc]['power_95_abs'],final[cc]['loss_abs']))
        final_file.write("{:s} \t {:.3f} \t {:.3f}\n".format(cc,final[cc]['mean'], final[cc]['std']))


    final_file.close()
    cmd = "column -t %s > %s && rm %s" % (tmp_file,perf_sum_abs,tmp_file)
    os.system(cmd)

if __name__== "__main__":
    main()

