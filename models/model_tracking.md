
# FRAMEWORK 	    TASK	        APPROACH	GCM	    REGION	    VARIABLE
----------------------------------------------------------------------------

----------------------------------------------------------------------------
# AutoGLUON	        Classification	Ensembling	ECMWF	NNI	        TMEAN

shuffle = True

## cross validated leaderboard on the training set

	model	                                score_val	fit_time	pred_time_val	stack_level
10	weighted_ensemble_k0_l1	                0.674825	0.330029	0.000870	    1
8	NeuralNetClassifier_STACKER_l0	        0.639860	13.523044	0.508255	    0
6	LightGBMClassifier_STACKER_l0	        0.639860	2.006419	0.025753	    0
7	CatboostClassifier_STACKER_l0	        0.639860	4.361887	0.028371	    0
3	ExtraTreesClassifierEntr_STACKER_l0	    0.615385	2.120452	0.544922	    0
1	RandomForestClassifierEntr_STACKER_l0	0.608392	2.684364	0.631651	    0
5	KNeighborsClassifierDist_STACKER_l0	    0.608392	0.204707	0.589822	    0
0	RandomForestClassifierGini_STACKER_l0	0.604895	2.647515	0.970814	    0
2	ExtraTreesClassifierGini_STACKER_l0	    0.604895	2.158305	0.678390	    0
9	LightGBMClassifierCustom_STACKER_l0	    0.597902	4.932908	0.026050	    0
4	KNeighborsClassifierUnif_STACKER_l0	    0.580420	0.183394	0.583565	    0

## evaluation on the test data

Evaluation: accuracy on test data: 0.8484848484848485

## SCO accuracy on the test data

SCO accuracy on the test data 0.8484848484848485

----------------------------------------------------------------------------
# AutoGLUON	        Classification	Ensembling	ECMWF	WNI	        TMEAN

shuffle = True

## cross validated leaderboard on the training set

model	score_val	fit_time	pred_time_val	stack_level
10	weighted_ensemble_k0_l1	0.648438	0.357394	0.000781	1
10	weighted_ensemble_k0_l1	0.656250	0.360466	0.000746	1
10	weighted_ensemble_k0_l1	0.614786	0.409272	0.000743	1
10	weighted_ensemble_k0_l1	0.626459	0.320619	0.000720	1
10	weighted_ensemble_k0_l1	0.622568	0.350498	0.000759	1
10	weighted_ensemble_k0_l1	0.658915	0.381852	0.000823	1
10	weighted_ensemble_k0_l1	0.639535	0.378286	0.000748	1
10	weighted_ensemble_k0_l1	0.639535	0.359996	0.000746	1
10	weighted_ensemble_k0_l1	0.658915	0.390783	0.000730	1
10	weighted_ensemble_k0_l1	0.671815	0.381317	0.000777	1

## evaluation on the test data

Evaluation: accuracy on test data: 0.5151515151515151

## SCO accuracy on the test data

SCO accuracy on the test data 0.5454545454545454

----------------------------------------------------------------------------
# AutoGLUON	        Classification	Ensembling	ECMWF	NSI	        TMEAN

shuffle = True

## cross validated leaderboard on the training set

model	score_val	fit_time	pred_time_val	stack_level
10	weighted_ensemble_k0_l1	0.675781	0.397212	0.000923	1
10	weighted_ensemble_k0_l1	0.652344	0.365507	0.000733	1
10	weighted_ensemble_k0_l1	0.648438	0.344641	0.000782	1
10	weighted_ensemble_k0_l1	0.667969	0.399247	0.000833	1
10	weighted_ensemble_k0_l1	0.661479	0.340867	0.000749	1
10	weighted_ensemble_k0_l1	0.678295	0.361691	0.000743	1
10	weighted_ensemble_k0_l1	0.674419	0.428211	0.000836	1
10	weighted_ensemble_k0_l1	0.694981	0.417761	0.000931	1
10	weighted_ensemble_k0_l1	0.679537	0.400673	0.000747	1
10	weighted_ensemble_k0_l1	0.637066	0.390452	0.000829	1

## evaluation on the test data

Evaluation: accuracy on test data: 0.6060606060606061

## SCO accuracy on the test data

SCO accuracy on the test data 0.6363636363636364

----------------------------------------------------------------------------
# AutoGLUON	        Classification	Ensembling	ECMWF	WSI	        TMEAN

shuffle = True

## cross validated leaderboard on the training set

	model	score_val	fit_time	pred_time_val	stack_level
10	weighted_ensemble_k0_l1	0.635294	0.376105	0.000801	1
10	weighted_ensemble_k0_l1	0.597656	0.388626	0.000796	1
10	weighted_ensemble_k0_l1	0.607004	0.334271	0.000849	1
10	weighted_ensemble_k0_l1	0.616279	0.373659	0.000762	1
10	weighted_ensemble_k0_l1	0.589147	0.373688	0.000776	1
10	weighted_ensemble_k0_l1	0.620155	0.340920	0.000751	1
10	weighted_ensemble_k0_l1	0.616279	0.365451	0.000757	1
10	weighted_ensemble_k0_l1	0.624031	0.384156	0.000740	1
10	weighted_ensemble_k0_l1	0.589147	0.370661	0.000735	1
10	weighted_ensemble_k0_l1	0.589147	0.394797	0.000734	1

## evaluation on the test data

Evaluation: accuracy on test data: 0.7878787878787878

## SCO accuracy on the test data

SCO accuracy on the test data 0.8181818181818182

----------------------------------------------------------------------------
# AutoGLUON	        Classification	Ensembling	ECMWF	ESI	        TMEAN

shuffle = True

## cross validated leaderboard on the training set

	model	score_val	fit_time	pred_time_val	stack_level
10	weighted_ensemble_k0_l1	0.539062	0.346458	0.000752	1
10	weighted_ensemble_k0_l1	0.568093	0.314494	0.000737	1
10	weighted_ensemble_k0_l1	0.544747	0.320862	0.000742	1
10	weighted_ensemble_k0_l1	0.552529	0.363015	0.000749	1
10	weighted_ensemble_k0_l1	0.552529	0.397145	0.000762	1
10	weighted_ensemble_k0_l1	0.554264	0.329660	0.000755	1
10	weighted_ensemble_k0_l1	0.546512	0.369132	0.000746	1
10	weighted_ensemble_k0_l1	0.554264	0.389943	0.000807	1
10	weighted_ensemble_k0_l1	0.565891	0.420420	0.000771	1
10	weighted_ensemble_k0_l1	0.593023	0.378965	0.000784	1

## evaluation on the test data

Evaluation: accuracy on test data: 0.48484848484848486

## SCO accuracy on the test data

SCO accuracy on the test data 0.5757575757575758

--> interesting large difference between the SCO accuracy and the 'true' accuracy on the test data
