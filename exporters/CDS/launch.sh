#!/bin/bash 


for year in $(seq 1993 2016)
	do  
	for month in $(seq 1 12) 
		do /home/nicolasf/anaconda3/envs/climlab/bin/python CDS_download_year_multiprocessing_year_month.py ${year} ${month} Z500; 
	done 
done

