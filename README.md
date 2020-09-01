# Google Summer of Code'20 Highlights with NumFOCUS

This post is meant to summarize the work done over the GSoC coding period. Let's get started real quick.

## About the project

My GSoC proposal was about adding a Variational Inference interface to PyMC4. Apart from MCMC algorithms, VI proposes an approximating distribution to fit the posterior. The whole plan was to implement two Variational Inference algorithms - Mean Field ADVI and Full Rank ADVI.

## Resolving Key challenges

| Key Challenges | Solutions proposed | How its resolved |
| --- | --- | --- |
| `theano.clone` equivalent for TF2 | Model execution with replaced inputs | Normal distribution's sample method is executed over flattened view of parameters |
| Flattened view of parameters | Use `tf.reshape()` | Used `tf.concat()` with `tf.reshape()` |
| Optimizers for ELBO | Use tf.keras.optimizers | Optimizers either from TFv1 or TFv2 with defaults from pymc3.updates can be used |
| Initialization of MeanField and Full Rank ADVI | Manually set bijectors | Relied on `tfp.TransformedVariable` |
| Progress bar | Use `tqdm` or `​tf.keras.utils.Progbar` | A small hack over `tf.print` |
| Minibatch processing of data | Capture slice in memory | This is the only incomplete feature. Maybe `tf.Dataset` API has to explored more or implement our own `tfp.vi.fit_surrogate_posterior` function.

## Community Bounding Period

* This was a super interesting period. I got to know about many PyMC core developers through slack.
* I spent the entire time learning about the basics of Bayesian statistics, prior, posterior predictive checks, and the theory of Variational Inference.
* I had also written a blog post during this interval about the nuts and bolts of VI and the implementation of Mean Field ADVI as well in Tensorflow Probability. Here is the blog post - [Demystify Variational Inference](https://www.codingpaths.com/gsoc/variational-inference/).
* The most difficult part of learning VI was to understand the transformations because PyMC3 and TFP handle transformations differently.

## Month 1

The coding period started from June 1 and my intention for this period was to add a very basic and general Variational Inference interface to PyMC4.
Here is the PR [#280](https://github.com/pymc-devs/pymc4/pull/280/) and workflow of the basic interface was -

* Get the vectorized `log prob` of the model.
* For each parameter of the model, have a Normal Distribution with the same shape and then build a posterior using `tfd.JointDistributionSequential`.
* Add optimizers with defaults from PyMC3 and perform VI using `tfp.fit_surrogate_posterior`.
* Sample from `tfd.JointDistributionSequential` and there is no need of equivalent of `theano.clone`.
* Transform the samples by quering the `SamplingState` but `Deterministics` have to be added as well.
* Resolve shape issues with ArviZ. In short, making `chains=1`.

I got the basic interface merged by late June and now, it was time to work upon Full Rank ADVI. I managed to open a PR [#289](https://github.com/pymc-devs/pymc4/pull/289) with Full Rank ADVI interface by the end of June.

## Month 2

This was the most dramatic month of GSoC coding period. Because Full Rank ADVI proposed in PR [#289](https://github.com/pymc-devs/pymc4/pull/289) resulted in errors most of the time. Here is the gist of workflow that was followed to get some useful insights about the errors -

* Instead of solving the shape issues independently and posing a `MvNormal` distribution for each parameter, build the posterior using flattened view of parameters.
* There were lots of NaNs in the ELBO, because of improper handling of transformations. As a result, `Interval`, `LowerBounded` and `UpperBounded` transformations were added as well.
* Then came the issue of `Cholesky Decomposition errors` while working with Gaussian Processes and Variational Inference. Here are my few insights after rigorous testing with different inputs -
    + Use dtype `tf.float64` with FullRank ADVI to maintain positive definiteness of covariance matrix.
    + Avoid aggressive optimization of ELBO. Maintain learning rates around `1e-3`.
    + Stabilize the diagonal of covariance matrix by adding a small jitter.
    + Double check for NaNs in the data.
* Here the results after trying reparametrization and different jitter amounts while doing VI.
![Testing ADVI](https://user-images.githubusercontent.com/11705326/88572649-2da17480-d048-11ea-952e-bbc472360438.png)

I got this PR merged by the end of July. And now, it was time to work on adding some features to ADVI.

## Month 3

After adding missing transformations in PR [#289](https://github.com/pymc-devs/pymc4/pull/289), my mentor asked me to write a proposal so as the Bounded Distributions are inherited instead of we applying transformations manually to each distribution. I explored each possibility to make a generalized version of transformations as it is done in PyMC3 using `tf.cond`. Since, we do not have values before model execution, it was difficult to use `tf.cond`. Here is the proposal's [source](https://gist.github.com/Sayam753/f434492fc19f78bb93f3002cdecfd002).

After getting an interface to use MeanField and FullRank ADVI, some features that are included in the PR [#310](https://github.com/pymc-devs/pymc4/pull/310) -

* Add a progress bar. (This is small hack over `tf.print`)
* Test progress bar in different OS.
* Add `ParameterConvergence` criteria to test convergence.
* Add LowRank Approximation.

I am still working on adding examples on hierarchical models and I hope to get it merged soon.

## Contributions

The Pull Requests I have opened and got merged during GSoC. I have explained each one above but here I try to summarize.

* Add Variational Inference Interface: [#280](https://github.com/pymc-devs/pymc4/pull/280)
* Add Full Rank Approximation: [#289](https://github.com/pymc-devs/pymc4/pull/289)
* Add features to ADVI: [#310](https://github.com/pymc-devs/pymc4/pull/310) (WIP)
* Remove transformations for Discrete distributions: [#314](https://github.com/pymc-devs/pymc4/pull/314)

## Gists created

Whatever experiments I perform to aid my learnings, I polish them out and share through GitHub gists. I do not why but I started loving to share code through GitHub gists rather than Colab or GitHub repo. Here are all the experiments I performed with ADVI during this summer.

* Comparison of MeanField ADVI in TFP, PyMC3, PyMC4: [Source](https://gist.github.com/Sayam753/df2d11b6b5a1e875710656ecc013fad5)
* Demonstration of shape issues while working with InferenceData: [Source](https://gist.github.com/Sayam753/36bf35c482b705545eecb5353a8f8f6a)
* Playing around Convergence and Optimizers: [Source](https://gist.github.com/Sayam753/080a8daca8cadd30b350d7fb88cff293)
* Tracking all parameters including deterministics: [Source](https://gist.github.com/Sayam753/130f91ae60175ba277a4b358575eac75)
* Implementation of FullRank ADVI in TFP: [Source](https://gist.github.com/Sayam753/4e10b6a62da994470a245f843b9ef648)
* Comparison of MeanField and FullRank ADVI over correlated Gaussians: [Source](https://gist.github.com/Sayam753/23592188b951bdeb53029eb0c4f4f2c3)
* Model flattening and Full Rank ADVI in PyMC4: [Source](https://gist.github.com/Sayam753/cc5126279932cffd65064bdc44754c2a)
* Missing transformations in PyMC4: [Source](https://gist.github.com/Sayam753/50a1966172ed712d3974d007280fb0ae)
* Testing transformations in PyMC4: [Source](https://gist.github.com/Sayam753/1a014bbc1afcf4dea0bb5e946e2e103f)
* Distribution Enhancement Proposal: [Source](https://gist.github.com/Sayam753/f434492fc19f78bb93f3002cdecfd002)
* Hacking `tf.print` for progress bar: [Source](https://gist.github.com/Sayam753/34e3ad014424ebd2902727114520a582)
* Parameter Convergence Checks in TFP: [Source](https://gist.github.com/Sayam753/82e2dcd2b1807c18c71df88d16003072)

## Future Goals

Some future tasks I would like to work upon -

* Configure Mini Batch processing of data.
* Add Normalizing Flows to variational inference interface.
* Add support of Variational AutoEncoders to PyMC4.

## Conclusion

It was an incredible experience contributing to open source. I have improved my Python skills. I want to thank my mentors [@ferrine](https://github.com/ferrine) and [@twiecki](https://github.com/twiecki) for being extremely supportive throughout this entire journey. I am loving my time with the PyMC community. Next, I also want to thank [@numfocus](https://github.com/numfocus) community for sharing this opportunity via Google Summer of Code.

Thank you for being a part of this fantastic summer.

With :heart:, Sayam Kumar
