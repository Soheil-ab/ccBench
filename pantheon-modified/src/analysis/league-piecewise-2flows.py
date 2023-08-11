import json
import argparse
from os import path
import os
import numpy as np

SAGE_SETUP_TIME=10
CC_SETUP_TIME=2

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--win-margin', metavar='WIN-MARGIN', type=float, required=True,
                        default=10.0,help='win margin in % -> 10 means 10%')
    parser.add_argument('--win-start', metavar='WIN-BEGIN-TIME', type=int, required=True,
                        default=0,help='start time in second (default 0)')
    parser.add_argument('--win-end', metavar='WIN-BEGIN-TIME', type=int,required=True,
                        default=100,help='start time in second (default 0)')
    parser.add_argument("--datadir", "-d", help="datadirectory containing json files for the evaluation")
    parser.add_argument("--prefix", help="common prefix of result dir folders: e.g. dataset-gen",required=True)
    parser.add_argument('--interval', metavar='INTERVAL', type=int, required=True,
                        default=0,help='interval between flows (Default 0)')
    parser.add_argument('--schemes', metavar='"SCHEME1 SCHEME2..."',
                        help='analyze a space-separated list of schemes',required=True)

    args = parser.parse_args()
    win_start = args.win_start
    win_end = args.win_end
    win_margin = args.win_margin
    schemes = args.schemes.split()
    num_env = 0

    dataset_path = path.join(args.datadir,"dataset-gen-league-multiflows-"+str(win_start)+"_"+str(win_end))
    cmd = "mkdir -p %s" % (dataset_path)
    os.system(cmd)
    cmd='cd %s ;rm winners;cd -;' % (dataset_path)
    os.system(cmd)

    links =  [12,24,48,96,192]
    uni_delays = [5,10,20,40,80]
    scheme_keys={}

    for cc in schemes:
        if cc in {"pure"}:
            scheme_keys[cc]="sage"
        else:
            scheme_keys[cc]=str(cc)

    for num_flows in [2]:
        for interval in [args.interval]:
            for loss in ["0"]:
                link_posts = [""]
                for link_post in link_posts:
                    for link in links:
                        for uni_del in uni_delays:
                            bdp=2*link*uni_del/12
                            for qs in [bdp,2*bdp,4*bdp,8*bdp,16*bdp]:
                                dir_post="wired"+str(link)+link_post+"-"+str(uni_del)+"-"+str(qs)+"-"+loss+"-"+str(interval)
                                out_post="wired"+str(link)+link_post+"_"+str(uni_del)+"_"+str(qs)+"_"+loss+"_"+str(interval)

                                min_mean=999999.0
                                final={}
                                winners=[]
                                winners_bw=[]
                                winners_scores=[]

                                for cc in schemes:
                                    dir_name=args.prefix+"-"+str(num_flows-1)+"-cubic-added-"+cc+"-"+dir_post
                                    data_dir = path.join(args.datadir, dir_name)
                                    info_path = path.join(data_dir, 'pantheon_metadata.json')
                                    data_path = path.join(data_dir,'piecewise_perf_'+str(win_start)+'_'+str(win_end)+'.json')

                                    with open(info_path) as json_file:
                                        try:
                                            info = json.load(json_file)
                                        except:
                                            print ("no valid json file\n")

                                    run_times   = info['run_times']

                                    with open(data_path) as json_file:
                                        meta = json.load(json_file)

                                    #Avg:
                                    final[cc]={}
                                    final[cc]['samples']=0
                                    final[cc]['tput']=[]
                                    final[cc]['score']=0

                                    for run_id in xrange(1, 1 + run_times):
                                        for flow_id in xrange(2,3):
                                            try:
                                                if meta[scheme_keys[cc]][str(run_id)][str(flow_id)]['delay_avg']>0:
                                                    final[cc]['samples']+=1
                                                    final[cc]['tput'].append(round(meta[scheme_keys[cc]][str(run_id)][str(flow_id)]['tput']))
                                            except:
                                                print(str(data_dir)+":no valid data for "+str(cc))
                                                final[cc]['tput'].append(0)

                                    np_arr = np.array(final[cc]['tput'])
                                    final[cc]['mean']=np.mean(np.sqrt(np.power(link/num_flows-np_arr,2)))
                                    final[cc]['std']=np.mean(np_arr)
                                for cc in schemes:
                                    if min_mean>final[cc]['mean']:
                                        min_mean=final[cc]['mean']
                                        cc_tput=cc

                                for cc in schemes:
                                    if ((link/num_flows+min_mean)*(1.+win_margin/100.0))>=final[cc]['std'] and ((link/num_flows-min_mean)*(1.-win_margin/100.0))<=final[cc]['std']:
                                        winners.append(cc)
                                        winners_scores.append(final[cc]['mean'])
                                        winners_bw.append(final[cc]['tput'])
                                print('%s -> winners:%s  --- scores: %s  --- BWs: %s '%(dir_post, winners,winners_scores,winners_bw))

                                dataset_path = path.join(args.datadir,"dataset-gen-league-multiflows-"+str(win_start)+"_"+str(win_end))
                                cmd = "mkdir -p %s" % (dataset_path)
                                os.system(cmd)

                                dataset_log_path = path.join(dataset_path,"log")
                                cmd = "mkdir -p %s" % (dataset_log_path)
                                os.system(cmd)

                                tmp_file = path.join(dataset_path, 'tmp')
                                perf_sum_abs = path.join(dataset_log_path, 'dataset-gen-multiflows-all-'+dir_post+'-sum-abs')

                                final_file= open(tmp_file,"w")
                                final_file.write("scheme \t mean_throughput \t std \n")

                                for cc in schemes:
                                    final_file.write("{:s} \t {:.3f} \t {:.3f}\n".format(cc_tput,final[cc_tput]['mean'], final[cc_tput]['std']))

                                final_file.close()

                                cmd = "column -t %s > %s && rm %s" % (tmp_file,perf_sum_abs,tmp_file)
                                os.system(cmd)
                                cmd="a=0"
                                for winner_ in winners:
                                    cmd = "%s;echo %s >> %s/winners" % (cmd,winner_+"_"+str(num_flows)+"-cubic-added_"+out_post+"_cwnd.txt",dataset_path)

                                os.system(cmd)
                                num_env = num_env + 1

    #Total number of games/environments
    cmd='echo "total %d" > %s/num_env' %(num_env,dataset_path)
    os.system(cmd)

if __name__== "__main__":
    main()
