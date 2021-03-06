import sys
sys.path.insert(0, '..') # add config to path
import config
import train as tr
import os
import json
import random
import numpy as np
import argparse
import datetime

class Namespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Run HSGNN")
    parser.add_argument('-task', type=str, default=None, help='Task name (e.g. hpo_metab)')
    parser.add_argument('-tb_name', type=str, default="sg", help='Base Model Name for Tensorboard Log')
    parser.add_argument('-restoreModelPath', type=str, default=None, help='Parent directory of model, hparams, kwargs')
    parser.add_argument("-max_epochs", type=int, default=300, help="Max number of epochs to train")
    parser.add_argument("-random_seeds", action="store_true", help="Use random seeds from 0-9. Otherwise use random random seeds")
    parser.add_argument('-tb_dir', default="tensorboard_test", type=str)
    parser.add_argument('-no_train', action="store_true")
    args = parser.parse_args()
    return args

def main(args_script):
    args_to_function = {
        "task" : args_script.task,
        "tb_name" : args_script.tb_name,
        "restoreModelPath" : args_script.restoreModelPath,
        "max_epochs" : args_script.max_epochs,
        "tb_dir" : args_script.tb_dir,

        ## Defaults
        "checkpoint_k": 1,
        "no_checkpointing" : False, #0 and True or 1 and False
        "tb_logging": True,
        "runTest" :  False, 
        "no_save" : False,
        "print_train_times" : False,
        "monitor_metric":'val_auroc',
        "opt_n_trials":None,
        "debug_mode":False,
        "subset_data":False,
        "restoreModelName":None,
        "noTrain": True,
        "log_path":None
    }
    args = Namespace(**args_to_function)

    # dict to keep track of results
    exp_results = {
        "test_acc_mean":0, "test_acc_sd":0,"test_micro_f1_mean":0,"test_micro_f1_sd":0,
        "test_auroc_mean":0, "test_auroc_sd":0,
        "test_acc" : [], "test_micro_f1": [], "test_auroc" : [],
        "call" : args_to_function
    }

    # seed = 2022
    # args.seed = seed
    args.tb_dir = os.path.join(config.PROJECT_ROOT, args.tb_dir)
    args.tb_version = "version_time"
    args.max_epochs = 450
    if not args_script.no_train: #train the model from scratch
        print('Train model from scratch')
        args.noTrain = False
        args.runTest = True
        # for eary stopping
        args.opt_prune = False
        args.opt_patience = 450
        test_results = tr.train_model(args)
    else: #read in the model - NOTE that this doesn't differentiaate .ckpt files if multiple are saved
        model_path = os.path.join(config.PROJECT_ROOT,args.tb_dir, args.tb_name, args.tb_version)
        for file in os.listdir(model_path):
            if file.endswith(".ckpt") and file.startswith("epoch"):
                outpath = file 
        args.noTrain = True
        args.no_save = True
        args.restoreModelPath = model_path
        args.restoreModelName = outpath
        test_results = tr.train_model(args)

    # keep track of test results for each random seed run
    exp_results['test_micro_f1'].append(float(test_results['test_micro_f1']))
    exp_results['test_acc'].append(float(test_results['test_acc']))
    exp_results['test_auroc'].append(float(test_results['test_auroc']))
    
    exp_results["test_acc_mean"] = np.mean(exp_results['test_acc'])
    exp_results["test_acc_sd"] = np.std(exp_results['test_acc'])
    exp_results["test_micro_f1_mean"] = np.mean(exp_results['test_micro_f1'])
    exp_results["test_micro_f1_sd"] = np.std(exp_results['test_micro_f1'])
    exp_results["test_auroc_mean"] = np.mean(exp_results['test_auroc'])
    exp_results["test_auroc_sd"] = np.std(exp_results['test_auroc'])
   
    print("OVERALL RESULTS:") # across all random seeds
    print(exp_results)

    # write results for all runs to file
    exp_results_file = open(os.path.join(config.PROJECT_ROOT, args.tb_dir, args.tb_name, "experiment_results_time.json"),"w")
    exp_results_file.write(json.dumps(exp_results, indent=4))
    exp_results_file.close()

if __name__ == "__main__":
    starting_time = datetime.datetime.now()
    print('Starting time:', starting_time.strftime("%m/%d/%Y, %H:%M:%S"))
    args = parse_arguments()
    main(args)
    ending_time = datetime.datetime.now()
    print('Starting time:', starting_time.strftime("%m/%d/%Y, %H:%M:%S"))
    print('Ending time:', ending_time.strftime("%m/%d/%Y, %H:%M:%S"))
    print('Execution time:', ending_time - starting_time)