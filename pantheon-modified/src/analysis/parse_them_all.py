import json
import argparse
from os import path
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--datadir", "-d", help="datadirectory containing json files for the evaluation")
    parser.add_argument("--metainfo", "-mi", help="information json file name for the evaluation",default="pantheon_perf.json")
    parser.add_argument("--metadata", "-md", help="metadata json file name for the evaluation",default="pantheon_metadata.json")
    parser.add_argument("--output", "-out", help="output prefix for the results",default="perf_norm")

    args = parser.parse_args()
    data_path = path.join(args.datadir, args.metainfo)
    info_path = path.join(args.datadir, args.metadata)

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
    max_gput=0.0
    max_tput=0.0
    min_loss=999999.0
    final={}
    #Avg:
    for cc in all_schemes:
        final[cc]={}
        final[cc]['samples']=0
        final[cc]['gput']=0
        final[cc]['tput']=0
        final[cc]['delay_95']=0
        final[cc]['delay_avg']=0
        final[cc]['delay_90']=0
        final[cc]['delay_mean']=0
        final[cc]['loss']=0
        final[cc]['score']=0
        final[cc]['jindex']=0
        for run_id in xrange(1, 1 + run_times):
            for flow_id in xrange(1, flows + 1):
                try:
                    if meta[cc][str(run_id)][str(flow_id)]['delay_avg']>0:
                        final[cc]['samples']+=1
                        final[cc]['gput']+=meta[cc][str(run_id)][str(flow_id)]['gput']
                        final[cc]['tput']+=meta[cc][str(run_id)][str(flow_id)]['tput']
                        final[cc]['jindex']=(meta[cc][str(run_id)][str(flow_id)]['tput']*meta[cc][str(run_id)][str(flow_id)]['tput'])+final[cc]['jindex']
                        final[cc]['delay_95']+=meta[cc][str(run_id)][str(flow_id)]['delay']
                        final[cc]['delay_avg']+=meta[cc][str(run_id)][str(flow_id)]['delay_avg']
                        final[cc]['delay_90']+=meta[cc][str(run_id)][str(flow_id)]['delay_90']
                        final[cc]['delay_mean']+=meta[cc][str(run_id)][str(flow_id)]['delay_mean']
                        final[cc]['loss']+=meta[cc][str(run_id)][str(flow_id)]['loss']
                        final[cc]['score']+=meta[cc][str(run_id)][str(flow_id)]['tput']*meta[cc][str(run_id)][str(flow_id)]['tput']/(meta[cc][str(run_id)][str(flow_id)]['delay_avg'])

                except:
                    print("no valid data for "+str(cc)+"\n")

        total=final[cc]['samples']
        if total!=0:
            final[cc]['gput']/=total
            try:
                final[cc]['jindex']=(final[cc]['tput']*final[cc]['tput'])/(final[cc]['jindex'])
            except:
                final[cc]['jindex']= 0
            final[cc]['jindex']/=total

            final[cc]['tput']/=total
            final[cc]['delay_95']/=total
            final[cc]['delay_avg']/=total
            final[cc]['delay_90']/=total
            final[cc]['delay_mean']/=total
            final[cc]['loss']/=total
            final[cc]['score']/=total

    for cc in all_schemes:
        for run_id in xrange(1, run_times+1):
            for flow_id in xrange(1, flows+1):
                if final[cc]['delay_avg']>0:
                    if max_gput<final[cc]['gput']:
                        max_gput=final[cc]['gput']
                    if max_tput<final[cc]['tput']:
                        max_tput=final[cc]['tput']
                    if min_del_95>final[cc]['delay_95']:
                        min_del_95=final[cc]['delay_95']
                    if min_del_avg>final[cc]['delay_avg']:
                        min_del_avg=final[cc]['delay_avg']
                    if min_del_90>final[cc]['delay_90']:
                        min_del_90=final[cc]['delay_90']
                    if min_del_mean>final[cc]['delay_mean']:
                        min_del_mean=final[cc]['delay_mean']
                    if min_loss>final[cc]['loss']:
                        min_loss=final[cc]['loss']

    for cc in all_schemes:
        for run_id in xrange(1, 1 + run_times):
            for flow_id in xrange(1, flows + 1):
                try:
                    meta[cc][str(run_id)][str(flow_id)]['gput'] =  meta[cc][str(run_id)][str(flow_id)]['gput']/max_gput
                    meta[cc][str(run_id)][str(flow_id)]['tput'] = meta[cc][str(run_id)][str(flow_id)]['tput']/max_tput
                    meta[cc][str(run_id)][str(flow_id)]['delay'] = meta[cc][str(run_id)][str(flow_id)]['delay']/min_del_95
                    meta[cc][str(run_id)][str(flow_id)]['delay_avg'] =   meta[cc][str(run_id)][str(flow_id)]['delay_avg']/min_del_avg
                    meta[cc][str(run_id)][str(flow_id)]['delay_90'] = meta[cc][str(run_id)][str(flow_id)]['delay_90']/min_del_90
                    meta[cc][str(run_id)][str(flow_id)]['delay_mean'] = meta[cc][str(run_id)][str(flow_id)]['delay_mean']/min_del_mean

                except:
                    print("no valid data for "+str(cc)+"\n")

        final[cc]['gput_abs']=final[cc]['gput']
        final[cc]['tput_abs']=final[cc]['tput']
        final[cc]['delay_95_abs']=final[cc]['delay_95']
        final[cc]['delay_avg_abs']=final[cc]['delay_avg']
        final[cc]['delay_90_abs']=final[cc]['delay_90']
        final[cc]['delay_mean_abs']=final[cc]['delay_mean']
        final[cc]['score_abs']=final[cc]['score']
        final[cc]['loss_abs']=final[cc]['loss']

        final[cc]['gput']/=max_gput
        final[cc]['tput']/=max_tput
        final[cc]['delay_95']/=min_del_95
        final[cc]['delay_avg']/=min_del_avg
        final[cc]['delay_90']/=min_del_90
        final[cc]['delay_mean']/=min_del_mean
        if min_loss!=0:
            final[cc]['loss']/=min_loss

    out_sum= args.output+'_sum.txt'
    out_json= args.output+'.json'
    out_sum_abs= args.output+'_sum_abs.txt'

    tmp_file = path.join(args.datadir, 'tmp')
    perf_sum = path.join(args.datadir, out_sum)
    perf_sum_abs = path.join(args.datadir, out_sum_abs)
    final_file= open(tmp_file,"w")
    final_file.write("scheme \t throughput \t dela_avg \t delay_95 \t loss\n")

    for cc in all_schemes:
        if final[cc]['delay_avg']>0:
            final_file.write("{:s} \t {:.3f} \t {:.3f} \t {:.3f} \t {:.3f}\n".format(
                cc,final[cc]['tput'], final[cc]['delay_avg'],final[cc]['delay_95'],
                final[cc]['loss']))

    final_file.close()

    #perf_path = path.join(args.datadir, 'perf_norm.json')
    perf_path = path.join(args.datadir, out_json)
    with open(perf_path, 'w') as fh:
        json.dump(meta, fh,indent=4)

    cmd = "column -t %s > %s && rm %s" % (tmp_file,perf_sum,tmp_file)
    os.system(cmd)

    final_file= open(tmp_file,"w")
    final_file.write("scheme \t throughput \t dela_avg \t delay_95 \t loss \n")

    for cc in all_schemes:
        if final[cc]['delay_avg_abs']>0:
            final_file.write("{:s} \t {:.3f} \t {:.3f} \t {:.3f} \t {:.3f} \n".format(
                cc,final[cc]['tput_abs'], final[cc]['delay_avg_abs'],final[cc]['delay_95_abs'],
                final[cc]['loss_abs']))

    final_file.close()
    cmd = "column -t %s > %s && rm %s" % (tmp_file,perf_sum_abs,tmp_file)
    os.system(cmd)

if __name__== "__main__":
    main()
