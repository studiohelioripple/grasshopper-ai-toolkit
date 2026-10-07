# Magpie Component Reference

Comprehensive reference for **Magpie** (v0.4.4) in Grasshopper.
Total verified components: **14**.
Synthesized directly via offline assembly analysis and runtime parameter reflection.

## Table of Contents

- [Others](#others) — 2 components
- [Tools](#tools) — 3 components
- [Machines](#machines) — 6 components
- [Exteras](#exteras) — 3 components

---

## Others

### Correlation Matrix
- **Tab**: Magpie > Others | **Type GUID**: `06e60a13-0994-4d55-823d-f2ccc8bec38b`
- **Alias**: `CorrelationMatrix`
- **Inputs**:
  - `Data` (`D`): Number [tree] — Data to analyze
- **Outputs**:
  - `Matrix` (`M`): Number [tree] — Correlation Matrix
- **Behavior**: Creates Correlation-Matrix for the given matrix of samples
- **Provenance**: [VERIFIED, Magpie.gha v0.4.4 Assembly Reflection]

### T-SNE
- **Tab**: Magpie > Others | **Type GUID**: `0073d98c-d0a2-49e4-a1ff-2b21670e1961`
- **Inputs**:
  - `Data` (`X`): Number [tree] — number[][] To do analysis on
  - `Dimension` (`D`): Integer [item] — The length of output vectors
  - `Perplexity` (`P`): Number [item] — [5-50] The balancing attention between local and global aspects of data
  - `Theta` (`T`): Number [item] — [0-1] The Trade-Off between preserving small and large distances
  - `Seed` (`S`): Integer [item] — Generator Seed
- **Outputs**:
  - `Result Vectors` (`R`): Number [tree] — The result of the applying the transformation (Computing Process of the Kernel) to given data
- **Behavior**: Solves a T-Distributed-Stochastic-Neighbor-Embedding model by given data
- **Provenance**: [VERIFIED, Magpie.gha v0.4.4 Assembly Reflection]

## Tools

### Computer
- **Tab**: Magpie > Tools | **Type GUID**: `c4c6d847-219d-4017-aae6-9081f01b1da7`
- **Inputs**:
  - `Machine` (`M`): Machine [item] — Machine
  - `Input` (`I`): Number [list] — Input Data to compute values from
- **Outputs**:
  - `Output` (`O`): Number [list] — Computed Data (For Boltzmann and NeuralNetwork machines)
- **Behavior**: Computes values with test-data
- **Provenance**: [VERIFIED, Magpie.gha v0.4.4 Assembly Reflection]

### Tuner
- **Tab**: Magpie > Tools | **Type GUID**: `77ce132d-9687-457e-9226-104d5907303f`
- **Alias**: `Details for tuning the machine`
- **Inputs**:
  - `Iteration`: Integer [item]
  - `LearningRate`: Number [item] — The value determines speed of learning. It would be also equivalent the Levenberg's damping factor (lambda) 
- **Outputs**:
  - `Tuner` (`T`): Tuner [item] — Tuner
- **Behavior**: Refresh !!
- **Provenance**: [VERIFIED, Magpie.gha v0.4.4 Assembly Reflection]

### Report
- **Tab**: Magpie > Tools | **Type GUID**: `9bddd0a5-787d-4aaf-b8d6-1668b75d763a`
- **Inputs**:
  - `Machine` (`M`): Machine [item] — Machine
- **Outputs**:
  - `Report`: Text [item] — Details about the machine
  - `Loss`: Number [item] — Details about the machine
  - `Iteration`: Integer [item] — Details about the machine
- **Behavior**: Creates Report out of a machine
- **Provenance**: [VERIFIED, Magpie.gha v0.4.4 Assembly Reflection]

## Machines

### Boltzmann Machine
- **Tab**: Magpie > Machines | **Type GUID**: `26523c4e-4d7a-420c-8aca-d79cd8705370`
- **Alias**: `Boltzmann`
- **Inputs**:
  - `Inputs` (`X`): Number [tree] — Kernel Input Data for training
  - `Dimension`: Integer [item] — Output Dimensionality
  - `Tuner` (`T`): Tuner [item] — Tuner
- **Outputs**:
  - `Machine` (`M`): Machine [item] — Machine
  - `Input Dimensions` (`D`): Number [tree] — New  dimensions of initial given features
- **Behavior**: Creating a Bernouli-Restricted-Boltzmann Kernel for Dimension Reduction
- **Provenance**: [VERIFIED, Magpie.gha v0.4.4 Assembly Reflection]

### Classification Machine
- **Tab**: Magpie > Machines | **Type GUID**: `4772636d-0cd1-4081-bd33-5cecbc4514ee`
- **Alias**: `Classifier`
- **Inputs**:
  - `Inputs` (`X`): Number [tree] — Kernel Input Data for training
  - `Labels`: Text [list] — The list of Labels.
  - `Hidden Neurons` (`Hidden`): Integer [item] — Number of Hidden Neurons.
  - `Tuner` (`T`): Tuner [item] — Tuner
- **Outputs**:
  - `Machine` (`M`): Machine [item] — Machine
  - `Table` (`T`): Text [list] — Table of Labels
- **Behavior**: Classification Machine
- **Provenance**: [VERIFIED, Magpie.gha v0.4.4 Assembly Reflection]

### KohMap Machine
- **Tab**: Magpie > Machines | **Type GUID**: `05fda739-a77d-4027-9ec5-03ffe6c402e5`
- **Alias**: `Koh-Map`
- **Inputs**:
  - `Inputs` (`X`): Number [tree] — Kernel Input Data for training
  - `Column Count` (`Columns`): Integer [item] — The number of neurons existing in a row
  - `Rows Count` (`Rows`): Integer [item] — The number of rows of neurons,  set it 1 for 1D 'Kohonen Map', and set it 0 for 1D 'Elastic Trainer'
  - `Tuner` (`T`): Tuner [item] — Tuner
- **Outputs**:
  - `Machine` (`M`): Machine [item] — Machine
  - `Neurons` (`N`): Number [tree] — Neurons Weights
  - `Winners` (`W`): Integer [list] — The GetWinner (Best Matched) neuron's index'
  - `Nodes` (`V`): Vector [tree] — Translation Vectors of the neurons
- **Behavior**: Creates a Distance-Network with Kohonen SelfOrganizing Map with SOM learning algorithm
- **Provenance**: [VERIFIED, Magpie.gha v0.4.4 Assembly Reflection]

### Vanilla Machine
- **Tab**: Magpie > Machines | **Type GUID**: `3cb560b3-aa1f-4d75-8c6f-bfbcb82e802e`
- **Alias**: `Vanilla`
- **Inputs**:
  - `Inputs` (`X`): Number [tree] — Kernel Input Data for training
  - `Output` (`Y`): Number [tree] — Kernel Output Data for training
  - `0` (`7`): Integer [list] — 7
  - `ActivationFunction` (`Activation`): Integer [item]
  - `LearnerType` (`Learner`): Integer [item]
  - `Tuner` (`T`): Tuner [item] — Tuner
- **Outputs**:
  - `Machine` (`M`): Machine [item] — Machine
- **Behavior**: Creating a Vanilla Neural-Network machine
- **Provenance**: [VERIFIED, Magpie.gha v0.4.4 Assembly Reflection]

### Clustering Machine
- **Tab**: Magpie > Machines | **Type GUID**: `4248a633-3952-4dc2-bb35-ccc42ffa033e`
- **Alias**: `Clustering`
- **Inputs**:
  - `Inputs` (`X`): Number [tree] — Kernel Input Data for clustering
  - `Clusters` (`N`): Integer [item] — Number of clusters
  - `Random Seed` (`S`): Integer [item] — Seed value for the Accord.
- **Outputs**:
  - `Machine` (`M`): Machine [item] — Machine
  - `ClusterNumber` (`I`): Integer [list] — Resultant prediction
  - `Scores` (`S`): Number [item] — Scores (Probabilities) is the probability of belonging to each cluster per each input item.
  - `Mean` (`M`): Number [tree] — The centroids of the clusters.
- **Behavior**: Solver for Gaussian-Mixture and K-Means Clustering (Right-Click to choose)
- **Provenance**: [VERIFIED, Magpie.gha v0.4.4 Assembly Reflection]

### PCA Machine
- **Tab**: Magpie > Machines | **Type GUID**: `e3df43dd-dae5-40db-af17-31bab5aedace`
- **Alias**: `PCA`
- **Inputs**:
  - `Data` (`X`): Number [tree] — number[][] To do analysis on
  - `Dimension` (`D`): Integer [item] — The length of output vectors
- **Outputs**:
  - `Machine` (`M`): Machine [item] — Machine
  - `Result Vectors` (`R`): Number [tree] — The result of the applying the transformation (Computing Process of the Kernel) to given vectors (InputData)
  - `Mean` (`M`): Number [item] — The vectors of Start and End of the Axises
  - `EigenVector` (`A`): Number [tree] — The vectors of Start and End of the Axises
  - `Proportions` (`P`): Number [list] — The respective role each component plays in the data set.
- **Behavior**: Create a Principal-Component-Analysis Machine
- **Provenance**: [VERIFIED, Magpie.gha v0.4.4 Assembly Reflection]

## Exteras

### Dispatch DataSet
- **Tab**: Magpie > Exteras | **Type GUID**: `d2a2c2b9-d13a-4c66-a57e-63ea7ac3639a`
- **Alias**: `Dispatch`
- **Inputs**:
  - `DataSet` (`D`): Number [tree] — Initial Data-set to dispatch
  - `Indexes` (`I`): Integer [list] — Here is a list of indexes corresponding to each data point, indicating where it should be allocated in the related set.
- **Outputs**:
  - `DataSets` (`D`): Number [tree] — A list of Dispatched Data-sets within a single DataTree
- **Behavior**: Dispatches a data-set to several data-sets. 
- **Provenance**: [VERIFIED, Magpie.gha v0.4.4 Assembly Reflection]

### Mean Tensor
- **Tab**: Magpie > Exteras | **Type GUID**: `be27d9a7-460b-4e0f-81e8-4b4241867de2`
- **Alias**: `Mean`
- **Inputs**:
  - `DataCluster` (`X`): Number [tree] — Given Tensors
- **Outputs**:
  - `Mean` (`M`): Number [list] — Mean Tensor
- **Behavior**: Calculates the mean tensor of the given tensors.
- **Provenance**: [VERIFIED, Magpie.gha v0.4.4 Assembly Reflection]

### Winner Index
- **Tab**: Magpie > Exteras | **Type GUID**: `1306c992-3bea-45d5-ae33-4b786aefc3c7`
- **Alias**: `Winner`
- **Inputs**:
  - `Tensor` (`T`): Number [list] — Given Tensor
- **Outputs**:
  - `Index` (`I`): Integer [item] — Winner Feature's Index
- **Behavior**: Gets the index of the max value in a tensor.
- **Provenance**: [VERIFIED, Magpie.gha v0.4.4 Assembly Reflection]
