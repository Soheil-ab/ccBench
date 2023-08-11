import json
import argparse
from os import path
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--win-margin', metavar='WIN-MARGIN', type=float, required=True,
            default=10.0,help='win margin in % -> 10 means 10%')
    parser.add_argument('--win-start', metavar='WIN-BEGIN-TIME', type=int, required=True,
            default=0,help='start time in second (default 0)')
    parser.add_argument('--win-end', metavar='WIN-BEGIN-TIME', type=int,required=True,
            default=100,help='start time in second (default 0)')
    parser.add_argument("--datadir", "-d", help="datadirectory containing json files for the evaluation")
    parser.add_argument('--schemes', metavar='"SCHEME1 SCHEME2..."',help='analyze a space-separated list of schemes',required=True)

    args = parser.parse_args()
    win_start = args.win_start
    win_end = args.win_end
    win_margin = args.win_margin
    schemes = args.schemes.split()
    num_env = 0
    num_env_lossy = 0
    num_env_noloss = 0

    scheme_keys={}
    ml_schemes={}
    ml_schemes={"aurora","indigo","dcubic","dbbr","orca","pure"}
    for cc in schemes:
        #if cc in {"pure"}:
        #    scheme_keys[cc]="sage"
        #else:
        scheme_keys[cc]=str(cc)

    for time in [""]:
        for loss in ["-0"]:
            for link in [12,24,48,96,192]:
                #FIXME: Mahimahi had an issue with higher than 250/300Mbps links! (This is resolved in our Remi Patch now!)
                if link==192:
                    link_posts = ["","-2x-d-7s","-4x-d-7s"]
                elif link==96:
                    link_posts = ["","-2x-u-7s","-2x-d-7s","-4x-d-7s"]
                else:
                    link_posts = ["","-2x-u-7s","-4x-u-7s","-2x-d-7s","-4x-d-7s"]

                for link_post in link_posts:
                    for uni_del in [5,10,20,40,80]:
                        bdp=2*link*uni_del/12
                        for qs in [int(bdp/2),bdp,2*bdp,4*bdp,8*bdp,16*bdp]:
                            dir_post="wired"+str(link)+link_post+"-"+str(uni_del)+"-"+str(qs)+loss+time

                            min_del_95=999999.0
                            min_del_avg=999999.0
                            min_del_90=999999.0
                            max_tput=0.0
                            final={}

                            winners=[]
                            max_score=0.0

                            for cc in schemes:
                                dir_post="wired"+str(link)+link_post+"-plus-10-"+str(uni_del)+"-"+str(qs)+loss+time
                                dir_name="dataset-gen-"+cc+"-"+dir_post
                                data_dir = path.join(args.datadir, dir_name)
                                info_path = path.join(data_dir, 'pantheon_metadata.json')
                                data_path = path.join(data_dir,'piecewise_perf_'+str(win_start)+'_'+str(win_end)+'.json')

                                with open(info_path) as json_file:
                                    info = json.load(json_file)

                                run_times   = info['run_times']
                                flows       = info['flows']

                                with open(data_path) as json_file:
                                    meta = json.load(json_file)

                                #Avg:
                                final[cc]               = {}
                                final[cc]['samples']    = 0
                                final[cc]['tput']       = 0
                                final[cc]['delay_95']   = 0
                                final[cc]['delay_90']   = 0
                                final[cc]['delay_avg']  = 0
                                final[cc]['jindex']     = 0
                                final[cc]['score']      = 0

                                for run_id in xrange(1, 1 + run_times):
                                    for flow_id in xrange(1, flows + 1):
                                        try:
                                            if meta[scheme_keys[cc]][str(run_id)][str(flow_id)]['delay_avg']>0:
                                                final[cc]['samples']+= 1
                                                final[cc]['tput']+=meta[scheme_keys[cc]][str(run_id)][str(flow_id)]['tput']
                                                final[cc]['delay_avg']+=meta[scheme_keys[cc]][str(run_id)][str(flow_id)]['delay_avg']+uni_del
                                                final[cc]['delay_90']+=meta[scheme_keys[cc]][str(run_id)][str(flow_id)]['delay_90']+uni_del
                                                final[cc]['delay_95']+=meta[scheme_keys[cc]][str(run_id)][str(flow_id)]['delay']+uni_del
                                                tput_tmp=round(meta[scheme_keys[cc]][str(run_id)][str(flow_id)]['tput'])
                                                final[cc]['score']+=tput_tmp*tput_tmp/(round((meta[scheme_keys[cc]][str(run_id)][str(flow_id)]['delay_avg']+uni_del)))
                                                final[cc]['jindex']=(meta[scheme_keys[cc]][str(run_id)][str(flow_id)]['tput']*meta[scheme_keys[cc]][str(run_id)][str(flow_id)]['tput'])+final[cc]['jindex']
                                        except:
                                            print("calculating stuff @"+str(data_dir)+":no valid data for "+str(cc))

                                    total=final[cc]['samples']
                                    if total!=0:
                                        try:
                                            final[cc]['jindex'] = (final[cc]['tput']*final[cc]['tput'])/(final[cc]['jindex'])
                                        except:
                                            final[cc]['jindex'] = 0

                                        final[cc]['jindex']/=total
                                        final[cc]['tput']/=total
                                        final[cc]['delay_95']/=total
                                        final[cc]['delay_90']/=total
                                        final[cc]['delay_avg']/=total
                                        final[cc]['score']/=total

                            for cc in schemes:
                                for run_id in xrange(1, run_times+1):
                                    for flow_id in xrange(1, flows+1):
                                        if final[cc]['delay_avg']>0:
                                            if max_tput<final[cc]['tput']:
                                                max_tput=final[cc]['tput']

                                            if min_del_95>final[cc]['delay_95']:
                                                min_del_95=final[cc]['delay_95']

                                            if min_del_avg>final[cc]['delay_avg']:
                                                min_del_avg=final[cc]['delay_avg']

                                            if min_del_90>final[cc]['delay_90']:
                                                min_del_90=final[cc]['delay_90']

                                            if max_score<final[cc]['score']:
                                                max_score=final[cc]['score']

                            for cc in schemes:
                                for run_id in xrange(1, run_times+1):
                                    for flow_id in xrange(1, flows+1):
                                        if final[cc]['delay_avg']>0:
                                            if (max_score*(1-win_margin/100.0))<=final[cc]['score']:
                                                winners.append(cc)
                            print('%s -> winners:%s'%(dir_post, winners))

                            for cc in schemes:

                                final[cc]['tput_abs']=final[cc]['tput']
                                final[cc]['delay_95_abs']=final[cc]['delay_95']
                                final[cc]['delay_90_abs']=final[cc]['delay_90']
                                final[cc]['delay_avg_abs']=final[cc]['delay_avg']

                                final[cc]['tput']/=max_tput
                                final[cc]['delay_95']/=min_del_95
                                final[cc]['delay_avg']/=min_del_avg
                                final[cc]['delay_90']/=min_del_90

                            dataset_path = path.join(args.datadir,"dataset-gen-league-"+str(win_start)+"_"+str(win_end))
                            cmd = "mkdir -p %s" % (dataset_path)
                            os.system(cmd)

                            dataset_log_path = path.join(dataset_path,"log")
                            cmd = "mkdir -p %s" % (dataset_log_path)
                            os.system(cmd)

                            tmp_file = path.join(dataset_path, 'tmp')
                            perf_sum = path.join(dataset_log_path, 'dataset-gen-all-'+dir_post+'-sum')
                            perf_sum_abs = path.join(dataset_log_path, 'dataset-gen-all-'+dir_post+'-sum-abs')
                            winner = path.join(dataset_log_path, 'dataset-gen-winner-'+dir_post)

                            final_file= open(tmp_file,"w")
                            final_file.write("scheme \t throughput \t dela_avg \t delay_95\n")

                            for cc in schemes:
                                if final[cc]['delay_avg']>0:
                                    final_file.write("{:s} \t {:.3f} \t {:.3f} \t {:.3f}\n".format(
                                        cc,final[cc]['tput'], final[cc]['delay_avg'],final[cc]['delay_95']))

                            final_file.close()

                            cmd = "column -t %s > %s && rm %s" % (tmp_file,perf_sum,tmp_file)
                            os.system(cmd)

                            final_file= open(tmp_file,"w")
                            final_file.write("scheme \t throughput \t dela_avg \t delay_95\n")
                            for cc in schemes:
                                if final[cc]['delay_avg_abs']>0:
                                    final_file.write("{:s} \t {:.3f} \t {:.3f} \t {:.3f}\n".format(
                                        cc,final[cc]['tput_abs'], final[cc]['delay_avg_abs'],final[cc]['delay_95_abs']))

                            final_file.close()
                            cmd = "column -t %s > %s && rm %s" % (tmp_file,perf_sum_abs,tmp_file)
                            os.system(cmd)

                            cmd="a=0"
                            for winner_ in winners:
                                cmd = "%s;echo %s >> %s" % (cmd,winner_,winner)
                            os.system(cmd)

                            num_env = num_env + 1
                            if loss=="-0":
                                num_env_noloss = num_env_noloss + 1
                            else:
                                num_env_lossy = num_env_lossy + 1

    #Multi Winner Case:
    cmd = 'cd %s;rm winners;for i in log/dataset-gen-winner-wired*; do for winner in `cat $i`; do  trace=`echo $i | sed "s/log\/dataset-gen-winner-/$winner-/g;s/-/_/g;s/_2x_d_7s/-2x-d-7s/g;s/_4x_d_7s/-4x-d-7s/;s/_8x_d_7s/-8x-d-7s/g;s/_8x_u_7s/-8x-u-7s/g;s/_4x_u_7s/-4x-u-7s/g;s/_2x_u_7s/-2x-u-7s/g;"`;  echo $trace"_cwnd.txt" >> winners;  done;done;' % (dataset_path)
    os.system(cmd)

    #Total number of games/environments
    cmd='echo "total %d" > %s/num_env' %(num_env,dataset_path)
    cmd='%s;echo "noloss %d" >> %s/num_env' %(cmd,num_env_noloss,dataset_path)
    os.system(cmd)

if __name__== "__main__":
    main()
