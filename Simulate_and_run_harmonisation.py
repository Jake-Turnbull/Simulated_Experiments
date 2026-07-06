"""
Simulate and run harmonisation of data constructed in different ways:

Data harmonisation is the process by which technical differences are estimated and removed from data
collected from different sources, or originating from different batches.

Most common tabular methods use linear regression or location and scale adjustments to remove technical differences.

Here, we simulate six different data sets, each with a different technical bias and then test harmonisation methods:


1. Standard batch model (linear combination of variables, ComBat form):


2. Non-linear covariate effects for one or more continuous covariate, with this effect being non-specific for different features


3. Interaction between biological covariates (eg sex * age, age* disease), with similar mixture of covariate effects across features


4. Covariate distribution is dependant on batch. For continuous covariates (though we could also vary this for more than just normal distributions, e.g. bimodal in one site, disease vs no disease)
For categorical: 𝑃(X^categorical=1│b)=p_b i.e probability of X being being 1 is dependant on batch


5. Account for additional covariate and batch interactions combining above scenarios

 
6. Simulating the most complicated scenario, 

	Additive and multiplicative batch effects

	Uneven covariate distributions that can be expressed as functions of batch b

	Potential non-linear covariate effects

	Interactions between covariates and/or covariate and batch

    
Finally, as image derived metrics are likely to have a spatial (image) dependant component, we will also simulate a spatially dependant covariate effect, and test harmonisation methods that can account for this.
Note, this will be done on the feature data (N x F) rather than the image data (N x X x Y x Z), 
as we are testing tabular harmonisation methods and not image based.
The stratergy will be to have a spatially dependant covariate effect and batch effects drawn from different distributions depending on the 'simulated' feature location (e.g. different distributions for different brain regions). This will be done by simulating a spatially dependant covariate effect and batch effects drawn from different distributions depending on the 'simulated' feature location (e.g. different distributions for different brain regions).

To implement this, we will give each feature a 'location' in x, y and z space and then simulate a spatially depended batch effect.



"""