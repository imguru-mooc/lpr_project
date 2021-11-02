#!/bin/bash

# Environment
export EII_HOME=$HOME/edge_insights_industrial/Edge_Insights_for_Industrial_2.6
export EII_BUILD=$HOME/edge_insights_industrial/Edge_Insights_for_Industrial_2.6/IEdgeInsights/build
export DAY01=$PWD/Day.01-Deep_Learning
export DAY02=$PWD/Day.02-OpenVINO
export DAY03=$PWD/Day.03-OpenVINO-Smart_Toll_Gate
export DAY04=$PWD/Day.04-EII
export DAY05=$PWD/Day.05-EII-Smart_Toll_Gate
export PYTHONPATH=$PYTHONPATH:$HOME/Desktop/training/01.EII_SmartTallGate/python/common

# Openvino
source /opt/intel/openvino_2021/bin/setupvars.sh

# IPython magic function
cp utils/eiimagics.py ${HOME}/.ipython/profile_default/startup

jupyter notebook
