## Pending Model Build

This folder will house the provider price sensitivity model, which will be a probability of job acceptance model trained at the level of the individual provider interaction at the job level throughout the season.

The target variable would be the likelihood of job acceptance. This means that I would use a target variable such as binary 0/1 for job acceptance, or possibly time to fill as a fraction of the total posting window. The key point is that I would want to be able to model the likelihood of a job being filled within the desired cutoff time and within certain quality constraints, at any posted rate - allowing the engine to predict the minimum viable posting rate to reliably fill a job.
